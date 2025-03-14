import sqlite3

from dto import UserRegisterDTO


class DatabaseHandler:
    database: sqlite3.Connection
    cursor: sqlite3.Cursor

    def __init__(self):
        self.database = sqlite3.connect("database.db")
        self.cursor = self.database.cursor()
        self.cursor.execute("""CREATE TABLE IF NOT EXISTS Users (
            id INTEGER PRIMARY KEY,
            username TEXT NOT NULL,
            description TEXT,
            age INTEGER,
            interests TEXT,
            rating INTEGER NOT NULL,
            type TEXT,
            image_url TEXT,
            tags TEXT
        )
                            """)
        self.database.commit()

    def add_user(self, user: UserRegisterDTO):
        self.cursor.execute(
            (
                "INSERT INTO Users "
                "(username, description, age, "
                "interests, rating, type, image_url, tags) "
                "VALUES (?, ?, ?, ?, ?, ?, ?, ?)"
            ),
            (
                user.username,
                user.description,
                user.age,
                user.interests,
                user.rating,
                user.type,
                user.image_url,
                "",
            ),
        )
        self.database.commit()

    def add_tags_to_user(self, username: str, tags: list[str]):
        self.cursor.execute(
            """UPDATE Users
                            SET tags = ?
                            WHERE username = ?
                            """,
            (
                ", ".join(tags),
                username,
            ),
        )
        self.database.commit()

    def find_users_by_username(self, username: str) -> UserRegisterDTO | None:
        self.cursor.execute(
            "SELECT * FROM Users WHERE username = ?",
            (username,),
        )
        data = self.cursor.fetchall()
        if len(data) == 0:
            return None
        user_data = data[0]
        user_response = UserRegisterDTO(*user_data[1:])
        return user_response

    def find_users_by_type(self, type: str):
        self.cursor.execute("SELECT * FROM Users WHERE type = ?", (type))
        return self.cursor.fetchall()

    def find_users_by_rating(self, rating: int):
        self.cursor.execute(
            "SELECT * FROM Users WHERE rating = ?",
            [rating],
        )
        return self.cursor.fetchall()

    def __del__(self):
        self.database.close()
