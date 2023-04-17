from aiogram.dispatcher.filters.state import StatesGroup, State


class NewGroup(StatesGroup):
    First_Name = State()
    Type_passport = State()
    Passport_series = State()
    Passport_old_number = State()
    Passport_number = State()
    Num_of_people = State()
    Phone = State()


class StatusPass(StatesGroup):
    Number = State()


class NumberTurn(StatesGroup):
    Passport = State()


class SendMessage(StatesGroup):
    M = State()
