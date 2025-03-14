import asyncio

from aiogram import Bot, Dispatcher
from aiogram.filters import Command
from aiogram.types import Message
from aiogram.fsm.context import FSMContext

from database import DatabaseHandler
from config import TG_TOKEN
from states import UserRegister


class Handler:
    databaseHandler = DatabaseHandler()

    async def start(self, message: Message) -> None:
        await message.answer("Привет! Добро пожаловать в PickMe BOT")

    async def login(self, message: Message) -> None: ...

    async def register(self, message: Message, state: FSMContext) -> None:
        await state.set_state(UserRegister.username)
        await message.answer("Введите желаемый username")

    async def set_username_to_profile(
        self, message: Message, state: FSMContext
    ) -> None: ...

    async def set_email_to_profile(
        self, message: Message, state: FSMContext
    ) -> None: ...


async def main() -> None:
    dp = Dispatcher()
    handler = Handler()
    dp.message.register(
        handler.start,
        Command("start"),
    )

    dp.message.register(
        handler.login,
        Command("login"),
    )

    dp.message.register(
        handler.register,
        Command("register"),
    )

    dp.message.register(
        handler.set_username_to_profile,
        UserRegister.username,
    )

    dp.message.register(
        handler.set_email_to_profile,
        UserRegister.email,
    )

    bot = Bot(TG_TOKEN)
    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())
