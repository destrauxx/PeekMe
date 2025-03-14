class UserRegisterDTO:
    username: str
    age: int
    description: str
    type: str
    interests: str
    rating: int
    image_url: str
    tags: str

    def __init__(
        self,
        username: str,
        age: int,
        description: str,
        type: str,
        interests: str,
        rating: int,
        image_url: str,
        tags: str,
    ) -> None:
        self.username = username
        self.age = age
        self.description = description
        self.type = type
        self.interests = interests
        self.rating = rating
        self.image_url = image_url
        self.tags = tags

    def __str__(self) -> str:
        return f"User(username={self.username}, age={self.age}, type={self.type}, rating={self.rating})"
