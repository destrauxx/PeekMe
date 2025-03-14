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
        username: str = "",
    ) -> None:
        pass
