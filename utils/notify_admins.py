import logging

from aiogram import Dispatcher

from config import admins


async def on_startup_notify(dp: Dispatcher):
    for admin in admins:
        try:
            await dp.bot.send_message(chat_id=admin, text="Бот запущений")

        except Exception as err:
            logging.exception(err)
