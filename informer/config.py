from os import getenv

from betterlogging import get_colorized_logger, INFO
from yaml import load, Loader


def get_yaml() -> dict:
    with open('../config.yaml', encoding='utf-8') as f:
        return load(f, Loader=Loader)


yaml = get_yaml()

TG_USERS_LIST = set()
CHILD_INFO = {}

for child_info in yaml['children']:
    for tg_id in child_info['tg_user_list']:
        TG_USERS_LIST.add(tg_id)
        CHILD_INFO[tg_id] = child_info['data']


BOT_TOKEN = getenv('BOT_TOKEN')

logger = get_colorized_logger()
logger.setLevel(INFO)
