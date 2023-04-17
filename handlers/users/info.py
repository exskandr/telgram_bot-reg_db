from aiogram import types

import kyeboards as kb
from loader import dp


@dp.callback_query_handler(text="info")
async def last_person_in_turn(call: types.CallbackQuery):
    text = f"Тут може бути написана різна інформація по проєкту"
    await call.message.answer(text, reply_markup=kb.inline_back)
