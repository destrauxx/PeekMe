import asyncio

from aiogram import Bot, Dispatcher
from aiogram.filters import Command
from aiogram.types import Message, User
from aiogram.fsm.context import FSMContext
from dto import UserRegisterDTO
from api import YandexGPTAPI

from database import DatabaseHandler
from config import TG_TOKEN, YA_FOLDER_ID, YA_GPT_API
from states import UserRegister


class Handler:
    databaseHandler = DatabaseHandler()
    ya_gpt = YandexGPTAPI(YA_GPT_API, YA_FOLDER_ID)
    tests = ya_gpt.get_test()

    async def start(self, message: Message) -> None:
        await message.answer("Привет! Добро пожаловать в PickMe BOT")
        await message.answer(
            "Пожалуйста, пройди процесс регистрации по команде /register"
        )

    async def login(self, message: Message) -> None:
        data = self.databaseHandler.find_users_by_username("voutoad")
        await message.answer(str(data))

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

        await message.answer("Отправь ссылку на картинку")

    async def set_image_url_to_profile(
        self, message: Message, state: FSMContext
    ) -> None:
        data = await state.update_data(image_url=message.text)

        data["age"] = int(data["age"])
        data["rating"] = int(data["rating"])
        data["tags"] = ""
        user_dto = UserRegisterDTO(**data)
        self.databaseHandler.add_user(user_dto)
        await state.set_state(UserRegister.testing)
        await message.answer(
            "Успешно зарегистрированы! Теперь пройдите тест для определения ваших личных тегов"
        )

    async def search(self, message: Message) -> None:
        if (
            self.databaseHandler.find_users_by_username(message.from_user.username)
            is None
        ):
            await message.answer(
                "Вы не зарегистрированы, пройдите регистрацию через /register"
            )
            return
        username = message.text.removeprefix("/search ")
        user = self.databaseHandler.find_users_by_username(username)
        if user is None:
            await message.answer("Такой пользователь не найден")
            return
        await message.answer(str(user))

    async def test(self, message: Message, state: FSMContext) -> None:
        text = ""
        for k, v in enumerate(self.tests):
            text += f"1) {v['question']}"
            text += f"\nОтветы: {k + 1}. {v['options'][0]}\t2. {v['options'][0]}\n3. {v['options'][0]}\t4. {v['options'][0]}\n"
        text += "Отправьте ответы в формате: `номер вопроса`) `номер ответа`.\nОтправьте ответы все в одном сообщении (точка на каждой строчке обязательна)"
        await state.set_state(UserRegister.test_passed)
        await message.answer(text)

    async def test_passed(self, message: Message, state: FSMContext) -> None:
        text = message.text.split(".\n")
        sp = []
        for i in text:
            data = i.rstrip(".")
            data = data.split(") ")
            data[0] = int(data[0]) - 1
            data[1] = int(data[1]) - 1
            sp.append(data)
        ll = []
        for i in sp:
            ll.append(
                f"Вопрос: {self.tests[i[0]]['question']} Ответ: {self.tests[i[0]]['options'][i[1]]}"
            )
        s = "\n".join(ll)

        response = self.ya_gpt.get_tags(s)["tags"]

        self.databaseHandler.add_tags_to_user(message.from_user.username, response)
        await message.answer(f"Выши тэги: {', '.join(response)}")
        await state.clear()


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
    dp.message.register(handler.test, UserRegister.testing)

    dp.message.register(handler.test_passed, UserRegister.test_passed)

    dp.message.register(handler.search, Command("search"))

    bot = Bot(TG_TOKEN)
    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())
