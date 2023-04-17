from aiogram import types
from aiogram.dispatcher import FSMContext

from loader import dp
from utils.db_api.db_commands import select_last_in_line, db_add_user, select_user, next_in_line
from states.take_turn import NewGroup
import kyeboards as kb


@dp.callback_query_handler(text="start")
async def start_btn(call: types.CallbackQuery):
    txt = "Ви повернулися в головне меню: "
    await call.message.answer(txt, reply_markup=kb.kb_user(call.from_user.id))


@dp.callback_query_handler(text="register")
async def register_to_turn(call: types.CallbackQuery):
    await call.message.answer('Очікуйте, йде обробка даних...')
    text = f"""
        Наступний номер, який має зайти до реєстратора №{(await next_in_line())[1]}
        Останій номер в черзі - {await select_last_in_line()}
        Для продовження реєстрації введіть своє П. І. Б. або натисніть /cancel для відміни.
"""
    await call.message.answer(text)
    await NewGroup.First_Name.set()


@dp.message_handler(state=NewGroup.First_Name)
async def add_name(message: types.Message, state: FSMContext):
    text = "Виберіть тип паспорту (ID CARD або паспорта), або відмініть операцію /cancel"
    first_name = message.text.title()
    new = open('E:\project\BOT_reg\Passport_of_the_Citizen_of_Ukraine_(Since_2016).jpg', 'rb')
    old = open('E:\project\BOT_reg\Passport_of_the_Citizen_of_Ukraine_(1993-2015).jpg', 'rb')
    await state.update_data(answer1=first_name)
    await message.answer('1️⃣ ID CARD')
    await dp.bot.send_photo(message.from_user.id, new)
    await message.answer('2️⃣ Паспорт старого зразка')
    await dp.bot.send_photo(message.from_user.id, old)
    await message.answer(text, reply_markup=kb.inline_kb_choose_pass)
    await NewGroup.next()


# choose new passport
@dp.callback_query_handler(text="new_pas", state=NewGroup.Type_passport)
async def choose_pas(call: types.CallbackQuery, state: FSMContext):
    txt = "Ви вибрали тип ID CARD"
    await call.message.answer(txt)
    text = "Введіть номер ID CARD, або відмініть операцію /cancel"
    passport = call.message.text
    await state.update_data(answer2=passport)
    await call.message.answer(text)
    await NewGroup.Passport_number.set()


@dp.message_handler(state=NewGroup.Passport_number)
async def add_new_passport(message: types.Message, state: FSMContext):
    new = open('E:\project\BOT_reg\\number_new_pass.jpg', 'rb')
    try:
        if len(message.text) != 9:
            await message.answer("Некоректне введення даних, потрібно ввести 9 чисeл, або відмініть операцію /cancel")
            await dp.bot.send_photo(message.from_user.id, new)
            return
        else:
            passport_number = message.text
            passport_n = int(passport_number)  # для виникнення помилки (перевірка чи число)
            await state.update_data(answer3=passport_number)
    except ValueError:
        await message.answer("Некоректне введення даних, потрібно ввести числa, або відмініть операцію /cancel")
        await dp.bot.send_photo(message.from_user.id, new)
        return
    text = """
    Введіть номер телефону без +380
    (Наприклад: номер телефону +380671234567, то ввести потрібно 671234567), 
    або відмініть операцію /cancel
    """
    await message.answer(text)
    await NewGroup.Phone.set()


# choose old passport
@dp.callback_query_handler(text="old_pas", state=NewGroup.Type_passport)
async def choose_pas(call: types.CallbackQuery, state: FSMContext):
    txt = "Ви вибрали тип PASSPORT"
    await call.message.answer(txt)
    text = "Введіть серію паспорта, або відмініть операцію /cancel"
    passport = call.message.text
    await state.update_data(answer2=passport)
    await call.message.answer(text)
    await NewGroup.Passport_series.set()


@dp.message_handler(state=NewGroup.Passport_series)
async def add_old_s_passport(message: types.Message, state: FSMContext):
    old = open('E:\project\BOT_reg\old_pass_series.jpg', 'rb')
    try:
        if len(message.text) != 2 or not message.text.isalpha():
            await message.answer("Некоректне введення даних, потрібно ввести дві літери серії паспорта, "
                                 "або відмініть операцію /cancel")
            await dp.bot.send_photo(message.from_user.id, old)
            return
        else:
            passport_series = message.text.upper()
            await state.update_data(answer3=passport_series)
    except ValueError:
        await message.answer("Некоректне введення даних, потрібно вводити літери")
        await dp.bot.send_photo(message.from_user.id, old)
        return
    text = """
    Введіть номер паспорту, 
    або відмініть операцію /cancel
    """
    await message.answer(text)
    await NewGroup.Passport_old_number.set()


@dp.message_handler(state=NewGroup.Passport_old_number)
async def add_old_n_passport(message: types.Message, state: FSMContext):
    old = open('E:\project\BOT_reg\old_pass_number.jpg', 'rb')
    try:
        if len(message.text) != 6:
            await message.answer("Некоректне введення даних, потрібно ввести 6 чисeл, або відмініть операцію /cancel")
            await dp.bot.send_photo(message.from_user.id, old)
            return
        else:
            passport_number = message.text
            passport_n = int(passport_number)  # для того щоб виникла помилка
            data = await state.get_data()
            serie = data.get("answer3")
            await state.update_data(answer3=serie + passport_number)
    except ValueError:
        await message.answer("Некоректне введення даних, потрібно ввести числa, або відмініть операцію /cancel")
        await dp.bot.send_photo(message.from_user.id, old)
        return
    text = """
    Введіть кількість осіб, які прийдуть на реєстрацію
    """
    await message.answer(text)
    await NewGroup.Num_of_people.set()


# enter number of people in the family
@dp.message_handler(state=NewGroup.Num_of_people)
async def add_old_n_passport(message: types.Message, state: FSMContext):
    try:
        n = message.text
        n_people = int(n)  # для того щоб виникла помилка
        if n_people >= 9:
            await message.answer("Ваше домогосподарство завелике, потрібно ввести чисeло менше 9,"
                                 " або відмініть операцію /cancel")
            return
    except ValueError:
        await message.answer("Некоректне введення даних, потрібно ввести числa, або відмініть операцію /cancel")
        return
    text = """
    Введіть номер телефону без +380
    (Наприклад: номер телефону +380671234567, то ввести потрібно 671234567), 
    або відмініть операцію /cancel
    """
    await message.answer(text)
    await NewGroup.Phone.set()


@dp.message_handler(state=NewGroup.Phone)
async def add_phone(message: types.Message, state: FSMContext):
    try:
        if len(message.text) != 9:
            text = """
                Некоректне введення даних, потрібно ввести 9 чисeл
                Введіть номер телефону без +380
                (Наприклад: номер телефону +380671234567, то ввести потрібно 671234567), 
                або відмініть операцію /cancel
                """
            await message.answer(text)
            return
        else:
            phone_answer = int(message.text)
    except ValueError:
        await message.answer("Некоректне введення даних, потрібно ввести числa")
        return
    data = await state.get_data()
    name = data.get("answer1")
    passport = data.get("answer3")
    phone = f"+380{phone_answer}"
    telegram = message.from_user.id
    username = message.from_user.username
    firstname = message.from_user.first_name
    lastname = message.from_user.last_name
    status = 'reg'
    num_of_people = data.get("answer4")

    # record data in DB users
    await db_add_user(f_i_o=name, passport=passport, phone_number=phone, status=status, user_id=telegram,
                      username=username, first_name=firstname, last_name=lastname, num_of_people=num_of_people)
    text = f"""
    Дякуємо за реєстрацію! Ваші дані:
    Номер в черзі  -  № {await select_user(passport)}
    П.І.Б          - {name}
    Дані паспорта  - {passport}
    Номер телефону - {phone}
    кількість осіб - {num_of_people}
    Для повернення в головне меню натиснути кнопку нижче ⬇
    """
    await message.answer(text, reply_markup=kb.inline_back)
    await state.finish()
