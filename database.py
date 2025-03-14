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
            image_url TEXT
        )
                            """)
        self.database.commit()

    def add_user(self, user: UserRegisterDTO):
        self.cursor.execute(
            (
                "INSERT INTO Users "
                "(username, description, age, "
                "interests, rating, type, image_url) "
                "VALUES (?, ?, ?, ?, ?, ?, ?)"
            ),
            (
                user.username,
                user.description,
                user.age,
                user.interests,
                user.rating,
                user.type,
                user.image_url,
            ),
        )
        self.database.commit()

    def find_users_by_username(self, username: str):
        self.cursor.execute(
            "SELECT * FROM Users WHERE username = ?",
            (username),
        )
        return self.cursor.fetchall()

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
