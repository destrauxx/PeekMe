from aiogram.fsm.state import State, StatesGroup


class UserRegister(StatesGroup):
    name = State()
    profile = State()
    academic_pros = State()
