from aiogram.fsm.state import State, StatesGroup


class UserRegister(StatesGroup):
    username = State()
    email = State()
    age = State()
