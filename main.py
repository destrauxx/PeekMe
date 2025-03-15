import asyncio
import validators

from aiogram import Bot, Dispatcher, F
from aiogram.filters import Command
import aiogram.types
from aiogram.fsm.context import FSMContext
from aiogram.utils.keyboard import InlineKeyboardBuilder
from dto import UserRegisterDTO
from api import YandexGPTAPI, BackendApi

from config import TG_TOKEN, YA_FOLDER_ID, YA_GPT_API, BACKEND_API
from states import UserRegister, UserLogin


dp = Dispatcher()
bapi = BackendApi(BACKEND_API)
ya_gpt = YandexGPTAPI(YA_GPT_API, YA_FOLDER_ID)
tests = ya_gpt.get_test()
current_tests = {}


@dp.message(Command("start"))
async def start(message: aiogram.types.Message) -> None:
    builder = InlineKeyboardBuilder()
    builder.add(aiogram.types.InlineKeyboardButton(text="Войти", callback_data="login"))
    builder.add(
        aiogram.types.InlineKeyboardButton(
            text="Зарегистрироваться", callback_data="register"
        )
    )
    await message.answer(
        "Привет! Добро пожаловать в PickMe BOT", reply_markup=builder.as_markup()
    )


@dp.callback_query(F.data == "login")
async def login(callback: aiogram.types.CallbackQuery, state: FSMContext) -> None:
    await state.set_state(UserLogin.username)
    await callback.message.answer("Введи свой tg username")


@dp.message(UserLogin.username)
async def login_username(message: aiogram.types.Message, state: FSMContext) -> None:
    username = message.text
    await state.update_data(username=username)
    resp = bapi.login_user(username)
    match resp.status_code:
        case 200:
            userdata = UserRegisterDTO(**resp.json())
            await message.answer(str(userdata))
        case 404:
            await message.answer("Такой пользователь не найден")


@dp.callback_query(F.data == "register")
async def register(callback: aiogram.types.CallbackQuery, state: FSMContext) -> None:
    await state.set_state(UserRegister.username)
    await callback.message.answer("Введи свой tg username")


@dp.message(UserRegister.username)
async def register_username(message: aiogram.types.Message, state: FSMContext) -> None:
    username = message.text
    await state.update_data(username=username)
    await state.set_state(UserRegister.age)
    await message.answer("Введите свой возраст")


@dp.message(UserRegister.age)
async def register_age(message: aiogram.types.Message, state: FSMContext) -> None:
    age = message.text
    try:
        int(age)
    except Exception:
        await message.answer("Введите число")
        return
    if int(age) > 100:
        await message.answer("У вас точно такой возраст?) Введите еще раз")
        return
    await state.update_data(age=age)
    await state.set_state(UserRegister.description)
    await message.answer("Опишите себя")


@dp.message(UserRegister.description)
async def register_description(
    message: aiogram.types.Message, state: FSMContext
) -> None:
    await state.update_data(description=message.text)
    await state.set_state(UserRegister.type)
    await message.answer("Введите вашу категорию")


@dp.message(UserRegister.type)
async def register_type(message: aiogram.types.Message, state: FSMContext) -> None:
    await state.update_data(type=message.text)
    await state.set_state(UserRegister.interests)
    await message.answer("Введите ваши интересы (в формате `<Интерес>, <Интерес>`)")


@dp.message(UserRegister.interests)
async def register_interests(message: aiogram.types.Message, state: FSMContext) -> None:
    data = message.text
    if ", ".join(data.split(", ")) != data:
        await message.answer("Вы ввели в не правильном формате, введите еще раз")
        return
    await state.update_data(interests=data)
    await state.set_state(UserRegister.rating)
    await message.answer("Введите ваши средний рейтинг, для учителей вводить 0")


@dp.message(UserRegister.rating)
async def register_rating(message: aiogram.types.Message, state: FSMContext) -> None:
    data = message.text
    try:
        int(data)
    except Exception:
        await message.answer("Введите число")
        return
    await state.update_data(rating=data)
    await state.set_state(UserRegister.image_url)
    await message.answer("Вставтье ссылку на фотографию")


@dp.message(UserRegister.image_url)
async def register_img_url(message: aiogram.types.Message, state: FSMContext) -> None:
    user_data = await state.get_data()
    data = message.text
    match data:
        case " ":
            user_data["image_url"] = ""
        case _:
            if not validators.url(data):
                await message.answer("Введите правильню ссылку")
                return
            user_data["image_url"] = data
    user_data["age"] = int(user_data["age"])
    user_data["rating"] = int(user_data["rating"])
    user_data["tags"] = ""
    resp = bapi.register(user_data)
    match resp.status_code:
        case 201:
            builder = InlineKeyboardBuilder()
            builder.add(
                aiogram.types.InlineKeyboardButton(text="Пройти", callback_data="test")
            )
            await message.answer(
                "Вы успешно зарегистророваны, теперь пройдите тест для определения личных тегов",
                reply_markup=builder.as_markup(),
            )
            await state.clear()
            await state.update_data(username=resp.json()["username"])
        case 400:
            await message.answer("В выших данных ошибка, пройди заново регистрацию")
        case 500:
            await message.answer("Ошибка на сервере")
    return


@dp.callback_query(F.data == "test")
async def test(callback: aiogram.types.CallbackQuery, state: FSMContext) -> None:
    text = ""
    for k, v in enumerate(tests):
        text += f"1) {v['question']}"
        text += f"\nОтветы: {k + 1}. {v['options'][0]}\t2. {v['options'][0]}\n3. {v['options'][0]}\t4. {v['options'][0]}\n"
    text += "Отправьте ответы в формате: `номер вопроса`) `номер ответа`.\nОтправьте ответы все в одном сообщении (точка на каждой строчке обязательна)"
    await state.set_state(UserRegister.test_passed)
    await callback.message.answer(text)


@dp.message(UserRegister.test_passed)
async def test_passed(message: aiogram.types.Message, state: FSMContext) -> None:
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
            f"Вопрос: {tests[i[0]]['question']} Ответ: {tests[i[0]]['options'][i[1]]}"
        )
    s = "\n".join(ll)

    response = ya_gpt.get_tags(s)["tags"]

    req = {"username": message.from_user.username, "tags": ", ".join(response)}
    resp = bapi.add_tags(req)
    if resp.status_code != 204:
        await message.answer("Ошибка на в сервере, попробйте ещё раз")
        return
    # self.databaseHandler.add_tags_to_user(, response)
    await message.answer(f"Выши тэги: {', '.join(response)}")
    await state.clear()


async def main() -> None:
    bot = Bot(TG_TOKEN)
    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())
