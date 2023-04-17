from aiogram import types
from aiogram.dispatcher import FSMContext

from loader import dp
from utils.db_api.db_commands import select_user, next_in_line
import kyeboards as kb
from states.take_turn import NumberTurn


@dp.callback_query_handler(text="what are your number")
async def number_turn(call: types.CallbackQuery):
    await call.message.answer('очікуйте, йде обробка даних...')
    text = f"Введіть номер паспорта, який зареєстрований в системі, або натисніть /cancel"
    await call.message.answer(text)
    await NumberTurn.Passport.set()


@dp.message_handler(state=NumberTurn.Passport)
async def add_passport(message: types.Message, state: FSMContext):
    answer = message.text.upper()
    await message.answer('очікуйте, йде обробка даних...')
    try:
        txt = f"""
                Ваш номер в черзі № {await select_user(answer)}!
                Наступний номер до реєстратора - №{(await next_in_line())[1]}.
                Натисніть на кнопку для повернення в головне меню ⬇
        """
        await message.answer(txt, reply_markup=kb.inline_back)
        await state.finish()
    except AttributeError:
        msg_er = "Таких даних немає в базі 🙈. Натисніть на кнопку BACK"
        await message.answer(msg_er, reply_markup=kb.inline_back)
        await state.finish()

