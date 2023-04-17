from aiogram import types

from loader import dp
from config import lat, lon, address
import kyeboards as kb


@dp.callback_query_handler(text="location_office")       # локація закладу
async def location_office(call: types.CallbackQuery):
    text = f"""Щоб знайти нас, прямуйте до позначки на карті 🗺️.\n Адреса: {address}"""
    await call.message.answer(text)
    await dp.bot.send_location(chat_id=call.from_user.id, latitude=lat, longitude=lon, reply_markup=kb.inline_back)

