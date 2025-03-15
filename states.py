from aiogram.fsm.state import State, StatesGroup


class UserLogin(StatesGroup):
    username = State()


class UserRegister(StatesGroup):
    username = State()
    age = State()
    description = State()
    type = State()
    interests = State()
    rating = State()
    image_url = State()
    testing = State()
    test_passed = State()


class Search(StatesGroup):
    search_tags = State()
