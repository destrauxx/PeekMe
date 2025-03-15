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


# class Test(StatesGroup):
#     case1 = State()
#     case2 = State()
#     case3 = State()
#     case4 = State()
#     case5 = State()
#     case6 = State()
#     case7 = State()
#     case8 = State()
#     case9 = State()
#     case10 = State()
