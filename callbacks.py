from aiogram.filters.callback_data import CallbackData


class UserList(CallbackData, prefix="user_account"):
    username: str


class UserGenerateResponse(CallbackData, prefix="user_ai"):
    userdata: str
