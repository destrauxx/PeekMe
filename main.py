import asyncio

from aiogram import Bot, Dispatcher
from aiogram.filters import Command
from aiogram.types import Message


from config import TG_TOKEN


async def start(message: Message) -> None:
    await message.answer("Привет! Добро пожаловать в PickMe BOT")


async def main() -> None:
    dp = Dispatcher()

    dp.message.register(
        start,
        Command("start"),
    )

    bot = Bot(TG_TOKEN)
    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())
