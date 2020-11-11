from aiogram import Dispatcher, Bot, executor
from aiogram.types import Message, ParseMode, Update

from informer.config import BOT_TOKEN, TG_USERS_LIST, logger
from informer.form_sender import send_form


bot = Bot(BOT_TOKEN)
dp = Dispatcher(bot)


@dp.errors_handler()
async def handle_error(upd: Update, e: Exception):
    logger.exception(e)
    return True


@dp.message_handler(commands='start')
async def handle_start(msg: Message):
    await msg.reply('Welcome to covid informer bot! If you want to send daily report to Ministry of health, use command /send')


@dp.message_handler(lambda msg: msg.from_user.id in TG_USERS_LIST, commands='send')
async def handle_send(msg: Message):
    logger.info(f'RECEIVED COMMAND SEND FROM TG USER {msg.from_user.id}')
    resp = await send_form(bot.session, msg.from_user.id)
    await msg.reply(f'Successfully sent!\nServer response:\n{resp}', parse_mode=ParseMode.HTML)


@dp.message_handler(lambda msg: msg.from_user.id in TG_USERS_LIST)
async def handle_start(msg: Message):
    await msg.reply('If you want to send daily report to Ministry of health, use command /send')


@dp.message_handler(lambda msg: msg.from_user.id not in TG_USERS_LIST)
async def handle_start(msg: Message):
    await msg.reply('Access forbidden! If you want to use the bot, please contact @benyomin')


executor.start_polling(dp, skip_updates=True)

