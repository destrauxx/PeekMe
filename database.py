import sqlite3


class DatabaseHandler:
    database: sqlite3.Connection
    cursor: sqlite3.Cursor

    def __init__(self):
        self.database = sqlite3.connect("database.db")
        self.cursor = self.database.cursor()
        self.cursor.execute("""CREATE TABLE IF NOT EXISTS Users (
            id INTEGER PRIMARY KEY,
            username TEXT NOT NULL,
            email TEXT NOT NULL,
            age INTEGER
        )
                            """)
        self.database.commit()

    def add_user(self, username, email, age):
        self.cursor.execute(
            "INSERT INTO Users (username, email, age) VALUES (?, ?, ?)",
            (username, email, age),
        )
        self.database.commit()

    def __del__(self):
        self.database.close()
