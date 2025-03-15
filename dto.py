class UserRegisterDTO:
    username: str
    age: int
    description: str
    type: str
    interests: str
    rating: int
    image_url: str

    def __init__(
        self,
        username: str,
        age: int,
        description: str,
        type: str,
        interests: str,
        rating: int,
        image_url: str = "",
    ) -> None:
        self.username = username
        self.age = age
        self.description = description
        self.type = type
        self.interests = interests
        self.rating = rating
        self.image_url = image_url

    def __str__(self) -> str:
        return (
            f"{self.username}(age={self.age}, type={self.type}, rating={self.rating})\n"
        )


class UserSetTagsDTO:
    username: str
    tags: str

    def __init__(
        self,
        username: str,
        tags: str,
    ) -> None:
        self.username = username
        self.tags = tags

    def __str__(self) -> str:
        return f"{self.username}\nТэги: {self.tags}"

    def to_dict(self) -> dict[str, str]:
        return {
            "username": self.username,
            "tags": self.tags,
        }


class UserDTO(UserRegisterDTO):
    tags: str

    def __init__(
        self,
        username: str,
        age: int,
        description: str,
        type: str,
        interests: str,
        rating: int,
        image_url: str = "",
        tags: str = "",
    ) -> None:
        super().__init__(username, age, description, type, interests, rating, image_url)
        self.tags = tags

    def __str__(self) -> str:
        return f"{self.username}\nТэги: {self.tags}"

    def full_profile_without_image(self) -> str:
        return f"Имя - {self.username}\nТеги - {self.tags}\n\n"

    def full_profile(self) -> str:
        return (
            self.full_profile_without_image() + f"{self.description}\n"
            f"Возраст - {self.age}. "
            f"Категория - {self.type}. Рейтинг - {self.rating}.\n"
            f"Интересы - {self.interests}." + f"Сслыка на картинку - {self.image_url}"
        )
