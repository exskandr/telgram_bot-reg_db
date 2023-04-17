
from aiogram import types
from aiogram.dispatcher import FSMContext

from loader import dp
from states.take_turn import StatusPass, SendMessage
import kyeboards as kb
from config import admins, channel_id
from utils.db_api.db_commands import update_status, next_in_line


@dp.callback_query_handler(user_id=admins, text='admin_menu')
async def admin_menu(call: types.CallbackQuery):
    text = """Ви знаходитесь в адміністративному меню. Виберіть наступні дії"""
    await call.message.answer(text, reply_markup=kb.inline_kb_admin_3)


# change status reg->Pass
@dp.callback_query_handler(user_id=admins, text="change_status")
async def change_status_number(call: types.CallbackQuery):
    text = f"""Введіть номер, якмй пройшов до реєстраторів, або натисніть /cancel"""
    await call.message.answer(text, reply_markup=kb.inline_back)
    await StatusPass.Number.set()


@dp.message_handler(user_id=admins, state=StatusPass.Number)
async def update_status_to_pass(message: types.Message, state: FSMContext):
    answer = message.text
    await update_status(answer)
    await message.answer('запит в процесі...')
    text = f"""
    Статус номеру {answer} змінено!
    Наступний номер в черзі - {(await next_in_line())[1]}.
    Для введення наступного номера натисни Change Status"
    """
    text_to_chat = f"Наступний до реєстратора {(await next_in_line())[0]}. Номер в черзі №{(await next_in_line())[1]}."
    await dp.bot.send_message(chat_id=channel_id, text=text_to_chat)
    await message.answer(text, reply_markup=kb.inline_kb_admin_2)
    await state.finish()


# send message to chat
@dp.callback_query_handler(user_id=admins, text="send_message")
async def ready_to_send_messages(call: types.CallbackQuery):
    text = f"""Введіть повідомлення, яке Ви хочете відправити, або натисніть /cancel"""
    await call.message.answer(text, reply_markup=kb.inline_back)
    await SendMessage.M.set()


@dp.message_handler(user_id=admins, state=SendMessage.M)
async def send_message(message: types.Message, state: FSMContext):
    answer = message.text
    await dp.bot.send_message(chat_id=channel_id, text=answer)
    await message.answer(answer, reply_markup=kb.inline_kb_admin_3)
    await state.finish()
