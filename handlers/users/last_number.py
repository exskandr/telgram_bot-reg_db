from aiogram import types

from loader import dp
from utils.db_api.db_commands import next_in_line

import kyeboards as kb


@dp.callback_query_handler(text="last number")
async def last_person_in_turn(call: types.CallbackQuery):
    await call.message.answer('очікуйте, йде обробка даних...')
    text = f"Наступний до реєстратора {(await next_in_line())[0]}. Номер в черзі №{(await next_in_line())[1]}."
    await call.message.answer(text, reply_markup=kb.inline_back)

