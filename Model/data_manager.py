import sqlite3
import os

from utils import verify_password

home_location = os.environ['PASS_APP']


class DataManager(object):
    """ Class for interaction with database table 'credentials'. """

    def __init__(self):
        self.conn = sqlite3.connect(f'{home_location}/passwords.db')
        self.cursor = self.conn.cursor()
        self.init_credential_table()
        self.user_id = None

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
        return f'Data Manager for {self.conn}'

    def init_credential_table(self):
        sql_command = """CREATE TABLE if not exists credentials(platform TEXT, username TEXT, 
                        password TEXT, user_id TEXT, FOREIGN KEY(user_id) REFERENCES users(id))"""
        self.cursor.execute(sql_command)
        self.commit()

    def commit(self):
        self.conn.commit()
        self.conn.close()

    def connect(self):
        self.conn = sqlite3.connect('passwords.db')
        self.cursor = self.conn.cursor()

    def get_users_credentials(self, email: str, password: str) -> bool:
        self.cursor.execute('SELECT password_hashed, id FROM users WHERE email=?;', (email,))
        if data_object := self.cursor.fetchone():
            password_hashed, user_id = data_object
            if approved := verify_password(password, password_hashed):
                self.user_id = user_id
                return approved
        return False

    def get_users_passwords(self, user_id):
        sql_command = 'SELECT * FROM credentials WHERE user_id=?;'
        self.cursor.execute(sql_command, (user_id,))
        return self.cursor.fetchall()

    def add_new_credential(self, site, username, password, user_id):
        sql_command = 'INSERT INTO credentials VALUES (?,?,?,?)'
        self.cursor.execute(sql_command, (site, username, password, user_id))

    def delete_credential(self, platform, user_id):
        sql_command = 'DELETE FROM credentials WHERE platform=? AND user_id=?;'
        self.cursor.execute(sql_command, (platform, user_id))


data_manager = DataManager()
