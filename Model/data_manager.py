import sqlite3
import os

from utils import verify_password

home_location = os.environ['PASS_APP']


class DataManager(object):
    """ Class for interaction with database table 'credentials'. """

    def __init__(self):
        self.conn = sqlite3.connect(f'{home_location}/passwords.db')
        self.cursor = self.conn.cursor()
        self.user_id = None

    def __str__(self):
        return f'Data Manager for {self.conn}'

    def commit(self):
        self.conn.commit()
        self.conn.close()
        print('DB closed...')

    def connect(self):
        self.conn = sqlite3.connect('passwords.db')
        self.cursor = self.conn.cursor()
        print('DB connected...')

    def get_users_credentials(self, email: str, password: str) -> bool:
        try:
            self.connect()
            self.cursor.execute('SELECT password_hashed, id FROM users WHERE email=?;', (email, ))
            data_object = self.cursor.fetchone()
            if data_object:
                password_hashed, user_id = data_object
                approved = verify_password(password, password_hashed)
                if approved:
                    self.user_id = user_id
            else:
                approved = False

        finally:
            self.commit()

        return approved


data_manager = DataManager()
