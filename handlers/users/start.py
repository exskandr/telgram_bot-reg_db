import logging

from aiogram import types
from aiogram.dispatcher import FSMContext

from loader import dp
from states.take_turn import NewGroup, StatusPass, NumberTurn
import kyeboards as kb


@dp.message_handler(commands=['start'])
async def process_start_command(message: types.Message):
    await message.reply("Бот РЕЄСТРАТОР-Байдена чекає на команди 😉 \n ⬇",
                        reply_markup=kb.kb_user(message.from_user.id)
                        )
    # print(message.from_user.values)
    logging.info(message.from_user.values)


@dp.message_handler(commands=["cancel"], state=(NewGroup, StatusPass, NumberTurn))
async def cancel(message: types.Message, state: FSMContext):
    text = "Ви відмінили дію! Для повернення в головне меню нажміть BACK"
    await message.answer(text, reply_markup=kb.inline_back)
    await state.reset_state()
