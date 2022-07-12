import sqlite3


class UserManager(object):
    """ Class for interaction with database table users. """
    INSTRUCTION = 'CREATE TABLE IF NOT EXISTS users(id TEXT, email TEXT, password_hashed TEXT)'

    def __init__(self):
        self.conn = sqlite3.connect('passwords.db')
        self.cursor = self.conn.cursor()
        self.cursor.execute(self.INSTRUCTION)

    def __str__(self):
        return f'User Manager for {self.conn}'

    def commit(self):
        self.conn.commit()
        self.conn.close()
        print('DB closed...')

    def connect(self):
        self.conn = sqlite3.connect('passwords.db')
        self.cursor = self.conn.cursor()
        print('DB connected...')


user_manager = UserManager()
