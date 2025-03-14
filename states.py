from aiogram.fsm.state import State, StatesGroup


class UserRegister(StatesGroup):
    username = State()
    age = State()
    description = State()
    type = State()
    interests = State()
    rating = State()
    image_url = State()
