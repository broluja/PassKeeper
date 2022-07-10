import sqlite3
import os
from dotenv import load_dotenv

load_dotenv()


class DataManager(object):
    """ Class for interaction with database. """
    username = os.getenv('USERNAME')
    password = os.getenv('PASSWORD')

    def __init__(self):
        self.conn = sqlite3.connect('passwords.db')
        self.cursor = self.conn.cursor()

    def __str__(self):
        return f'Data Manager for {self.conn}'

    def commit(self):
        self.conn.commit()
        self.conn.close()

    def connect(self):
        self.conn = sqlite3.connect('passwords.db')
        self.cursor = self.conn.cursor()


data_manager = DataManager()
