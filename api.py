import requests
import json


class YandexGPTAPI:
    def __init__(
        self,
        api_key,
        folder_id,
        base_url="https://llm.api.cloud.yandex.net/foundationModels/v1/completion",
    ):
        self.api_key = api_key
        self.folder_id = folder_id
        self.base_url = base_url

    def send_request(self, prompt):
        headers = {
            "Authorization": f"Api-Key {self.api_key}",
            "Content-Type": "application/json",
        }
        data = {
            "modelUri": f"gpt://{self.folder_id}/yandexgpt-lite",  # Укажите модель
            "completionOptions": {
                "stream": False,
                "temperature": 0.6,
                "maxTokens": 2000,  # Максимальное количество токенов в ответе
            },
            "messages": [
                {
                    "role": "system",
                    "text": (
                        "Ты система для создание тестов для платформы "
                        "PickMe, в которой главная цель это "
                        "персонализация обучения. Она создана "
                        "специально для учителей старшей школы "
                        "с целью помочь учителям понять младшее поколение."
                    ),
                },
                {"role": "user", "text": prompt},
            ],
        }
        response = requests.post(self.base_url, headers=headers, json=data)

        if response.status_code == 200:
            return response.json()
        else:
            raise Exception(
                f"Ошибка при запросе к API: {response.status_code}, {response.text}"
            )

    def generate_test_prompt(self):
        return (
            "Составь тест из 10 вопросов для определения качеств ученика. "
            "Каждый вопрос должен иметь 4 варианта ответа, правильного ответа нет, вопросы нужны для определения качеств человека(интроверт, экстроверт и т. д.)"
            "Правильный ответ должен быть четко обозначен. "
            "Вопросы должны быть на русском языке. "
            "Ответ предоставь в формате JSON, где каждый вопрос представлен как объект со следующими полями: "
            "'question' (текст вопроса), 'options' (массив из 4 вариантов ответа), 'correct_answer' (правильный ответ)."
        )

    def generate_text_prompt(self, user_data: str) -> str:
        return (
            "Напиши текст для начала общения с учеником старших классов школы. Данные"
            f"ученика следующие: {user_data}. В этих данных указано имя ученика, его увлечения и персональные тэги (его характеристик). Учитывай эти поля. В ответе пиши не более 30 слов."
            "Формат ответа должен представлять собой строку текста. Пиши развернуто "
        )

    def generate_tags_prompt(self):
        return "На основе данных тебе вопросов и ответов на них, составь тэги человека с его классификацией. Формат ответа должен быть ввиде JSON. В ответе должны быть поле `tags` представляющий список тегов.\n"

    def get_test(self):
        prompt = self.generate_test_prompt()
        response = self.send_request(prompt)

        data = response["result"]["alternatives"]

        return json.loads(data[0]["message"]["text"].strip("`"))

    def get_tags(self, tests):
        prompt = self.generate_tags_prompt() + tests
        response = self.send_request(prompt)

        data = json.loads(
            response["result"]["alternatives"][0]["message"]["text"].strip("`")
        )

        return data

    def generate_user_text(self, text, username):
        prompt = self.generate_text_prompt(text)
        response = self.send_request(prompt)

        data = response["result"]["alternatives"][0]["message"]["text"]
        data = data.replace("[имя]", username, 1)
        return data


class BackendApi:
    base_url: str

    def __init__(
        self,
        base_url: str,
    ):
        self.base_url = base_url

    def login_user(self, username):
        resp = requests.get(
            f"{self.base_url}/users/{username}",
            headers={"Content-Type": "application/json"},
        )
        return resp

    def register(self, userdata):
        resp = requests.post(
            f"{self.base_url}/users",
            json=userdata,
            headers={"Content-Type": "application/json"},
        )
        return resp

    def add_tags(self, userdata):
        resp = requests.patch(
            f"{self.base_url}/users",
            json=userdata,
            headers={"Content-Type": "application/json"},
        )
        return resp

    def search_with_tags(self, tags):
        resp = requests.get(
            f"{self.base_url}/users?tags={tags}",
            headers={"Content-Type": "application/json"},
        )
        return resp

    def get_user(self, username: str):
        resp = requests.get(
            f"{self.base_url}/users/{username}",
            headers={"Content-Type": "application/json"},
        )
        return resp
