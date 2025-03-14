import sqlite3

class DatabaseHandler():
    database = None
    cursor = None
    
    def __init__(self):
        self.database = sqlite3.connect("database.db")
        self.cursor = self.database.cursor()
        self.cursor.execute('''CREATE TABLE IF NOT EXISTS Users (
            id INTEGER PRIMARY KEY,
            username TEXT NOT NULL,
            description TEXT,
            age INTEGER,
            interests TEXT,
            rating INTEGER NOT NULL,
            type TEXT,
            image_url TEXT
        )
                            ''')    
        self.database.commit()
        
    def add_user(self, username, description, age, interests, rating, type, image_url):
        self.cursor.execute('INSERT INTO Users (username, description, age, interests, rating, type, image_url) VALUES (?, ?, ?, ?, ?, ?, ?)', (username, description, age, interests, rating, type, image_url))
        self.database.commit()
        
    def find_users_by_username(self, username):
        self.cursor.execute("SELECT * FROM Users WHERE username = ?", (username))
        return self.cursor.fetchall()
        
    def find_users_by_type(self, type):
        self.cursor.execute("SELECT * FROM Users WHERE type = ?", (type))
        return self.cursor.fetchall()
    
    def find_users_by_rating(self, rating):
        self.cursor.execute("SELECT * FROM Users WHERE rating = ?", (rating))
        return self.cursor.fetchall()
    
    def __del__(self):
        self.database.close()
        
    
    