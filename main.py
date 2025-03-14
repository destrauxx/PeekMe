import asyncio

from aiogram import Bot, Dispatcher
from aiogram.filters import Command
from aiogram.types import Message, User
from aiogram.fsm.context import FSMContext
from dto import UserRegisterDTO

from database import DatabaseHandler
from config import TG_TOKEN
from states import UserRegister


class Handler:
    databaseHandler = DatabaseHandler()

    async def start(self, message: Message) -> None:
        await message.answer("Привет! Добро пожаловать в PickMe BOT")

    async def login(self, message: Message) -> None: ...

    async def register(self, message: Message, state: FSMContext) -> None:
        await state.update_data(username=message.from_user.username)
        await state.set_state(UserRegister.age)
        await message.answer("Введите ваш возраст")

    async def set_age_to_profile(self, message: Message, state: FSMContext) -> None:
        await state.update_data(age=message.text)
        await state.set_state(UserRegister.description)

        await message.answer("Опишите себя")

    async def set_description_to_profile(
        self, message: Message, state: FSMContext
    ) -> None:
        await state.update_data(description=message.text)
        await state.set_state(UserRegister.type)

        await message.answer("Введите свою категорию")

    async def set_type_to_profile(
        self,
        message: Message,
        state: FSMContext,
    ) -> None:
        await state.update_data(type=message.text)
        await state.set_state(UserRegister.interests)

        await message.answer(
            "Введите свои интересы(в формате `<Интерес>, <Интерес>`)",
        )

    async def set_interests_to_profile(
        self, message: Message, state: FSMContext
    ) -> None:
        await state.update_data(interests=message.text)
        await state.set_state(UserRegister.rating)

        await message.answer("Введите свой рейтинг")

    async def set_rating_to_profile(self, message: Message, state: FSMContext) -> None:
        await state.update_data(rating=message.text)
        await state.set_state(UserRegister.image_url)

        await message.answer("Добавть ссылку на картинку")

    async def set_image_url_to_profile(
        self, message: Message, state: FSMContext
    ) -> None:
        data = await state.update_data(image_url=message.text)

        data["age"] = int(data["age"])
        data["rating"] = int(data["rating"])

        user_dto = UserRegisterDTO(**data)
        self.databaseHandler.add_user(user_dto)
        await state.clear()
        await message.answer("Успшно зарегистрированы!")


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
        handler.set_age_to_profile,
        UserRegister.age,
    )

    dp.message.register(
        handler.set_description_to_profile,
        UserRegister.description,
    )

    dp.message.register(
        handler.set_type_to_profile,
        UserRegister.type,
    )

    dp.message.register(
        handler.set_interests_to_profile,
        UserRegister.interests,
    )

    dp.message.register(
        handler.set_rating_to_profile,
        UserRegister.rating,
    )

    dp.message.register(
        handler.set_image_url_to_profile,
        UserRegister.image_url,
    )

    bot = Bot(TG_TOKEN)
    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())
