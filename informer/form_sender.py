import json
from datetime import date

from aiohttp import ClientSession

from .config import CHILD_INFO, logger


REQUEST_URL = 'https://govforms.gov.il/mw/forms/ChildHealthDeclaration@labor.gov.il'
POST_URL = 'https://govforms.gov.il/MW/Process/Data/'
UUID_LENGTH = 36
SEARCH_QUERY = 'requestID":"'


async def _get_form_id(session: ClientSession) -> str:
    resp = await session.get(REQUEST_URL)
    content = (await resp.content.read()).decode('utf-8')

    uuid_start = content.find(SEARCH_QUERY) + len(SEARCH_QUERY)
    uuid_end = uuid_start + UUID_LENGTH
    uuid = content[uuid_start:uuid_end]

    return uuid


def _compose_form(request_id: str, info: dict) -> dict:
    today = date.today().strftime('%d/%m/%Y')

    return {
        'requestID': request_id,
        'processID': None,
        'formData': {
            'declarationProperties': {
                'childInformation': {
                    'idNum': info['child']['id'],
                    'lastName': info['child']['last_name'],
                    'firstName': info['child']['first_name']
                },
                'parentInformation': {
                    'idNum': info['parent']['id'],
                    'lastName': info['parent']['last_name'],
                    'firstName': info['parent']['first_name']
                },
                'childBirthDate': info['child']['birth_date'],
                'daycareManager': info['kindergarten']['director_name'],
                'dayCareCity': {
                    'dataCode': info['city']['code'],
                    'dataText': info['city']['name']
                },
                'dayCareName': {
                    'dataCode': info['kindergarten']['code'],
                    'dataText': info['kindergarten']['name']
                },
                'parentMobile': info['parent']['phone'],
                'parentEmail': info['parent']['mail'],
                'parentFirstDeclaration': True,
                'parentSecondDeclaration': True,
                'parentDeclaration3': True,
                'declarationDate': today,
                'name': 'declarationProperties',
                'state': 'completed',
                'next': '',
                'prev': '',
                'isClosed': True
            },
            'containersViewModel': {
                'showPrintButton': True,
                'currentContainerName': 'declarationProperties',
                'validatedStatus': True
            },
            'formInformation': {
                'isFormSent': False,
                'loadingDate': today,
                'firstLoadingDate': '',
                'isMobile': False,
                'language': 'hebrew'
            }
        },
        'language': 'he',
        'attachments': []
    }


async def send_form(session: ClientSession, tg_user: str) -> str:
    logger.info('SENDING REQUEST...')

    info = CHILD_INFO[tg_user]
    request_id = await _get_form_id(session)
    form = _compose_form(request_id, info)

    logger.info(f'SENDING REQUEST:\n{json.dumps(form, ensure_ascii=False, indent=2)}')

    resp = await session.post(POST_URL, json=form)
    content = (await resp.json(content_type=None))
    pretty_resp = json.dumps(content, ensure_ascii=False, indent=2)

    logger.info(f'RESPONSE:\n{pretty_resp}')
    resp.raise_for_status()

    return f'<code>{pretty_resp}</code>'
