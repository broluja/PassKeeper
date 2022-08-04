import sqlite3
import os

home_location = os.environ['PASS_APP']


class UserManager(object):
    """ Class for interaction with database table 'users'. """
    INSTRUCTION = 'CREATE TABLE IF NOT EXISTS users(id TEXT, email TEXT, password_hashed TEXT)'

    def __init__(self):
        self.conn = sqlite3.connect(f'{home_location}/passwords.db')
        self.cursor = self.conn.cursor()
        self.cursor.execute(self.INSTRUCTION)
        self.commit()

    def __enter__(self):
        self.connect()
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        if exc_type is None:
            self.commit()
            print('Data stored.')
        else:
            self.commit()
            print(f'File closed but an exception appeared: {str(exc_type)}')
            return False

    def __str__(self):
        return f'User Manager for {self.conn}'

    def commit(self):
        self.conn.commit()
        self.conn.close()

    def connect(self):
        self.conn = sqlite3.connect('passwords.db')
        self.cursor = self.conn.cursor()

    def check_email_usage(self, email: str):
        sql_command = 'SELECT * FROM users WHERE email=?;'
        self.cursor.execute(sql_command, (email,))
        return self.cursor.fetchone()

    def register_user(self, user_id: str, email: str, password: str):
        sql_command = 'INSERT INTO users VALUES(?, ?, ?);'
        self.cursor.execute(sql_command, (user_id, email, password))


user_manager = UserManager()
