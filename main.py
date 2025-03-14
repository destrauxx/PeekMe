import asyncio

from aiogram import Bot, Dispatcher
from aiogram.filters import Command
from aiogram.types import Message
from aiogram.fsm.context import FSMContext

from database import DatabaseHandler
from config import TG_TOKEN
from states import UserRegister


async def start(message: Message) -> None:
    await message.answer("Привет! Добро пожаловать в PickMe BOT")


async def login(message: Message) -> None: ...


async def register(message: Message, state: FSMContext) -> None: ...


async def set_smth_to_profile(message: Message, state: FSMContext) -> None: ...


async def set_smth_to_profile2(
    message: Message,
    state: FSMContext,
) -> None: ...


async def main() -> None:
    databaseHandler = DatabaseHandler()

    dp = Dispatcher()

    dp.message.register(
        start,
        Command("start"),
    )

    dp.message.register(
        login,
        Command("login"),
    )

    dp.message.register(register, Command("register"))

    dp.message.register(
        set_smth_to_profile,
        UserRegister.name,
    )

    dp.message.register(
        set_smth_to_profile,
        UserRegister.name,
    )

    bot = Bot(TG_TOKEN)
    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())
