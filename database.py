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
            age INTEGER,
            interests TEXT,
            
        )
                            ''')    
        self.database.commit()
        
    def add_user(self, username, age, interests):
        self.cursor.execute('INSERT INTO Users (username, age, interests) VALUES (?, ?)', (username, age, interests))
        self.database.commit()
        
    def __del__(self):
        self.database.close()
        
    
    