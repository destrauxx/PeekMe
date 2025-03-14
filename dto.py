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
        image_url: str,
    ) -> None:
        self.username = username
        self.age = age
        self.description = description
        self.type = type
        self.interests = interests
        self.rating = rating
        self.image_url = image_url
