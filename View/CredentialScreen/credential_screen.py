import sqlite3

from kivy.properties import ObjectProperty, StringProperty
from kivy.uix.boxlayout import BoxLayout
from kivymd.uix.screen import MDScreen

from Model.data_manager import data_manager


class CredentialScreenView(MDScreen):
    recycleView = ObjectProperty(None)

    def __init__(self, **kwargs):
        super(CredentialScreenView, self).__init__(**kwargs)
        self.conn = sqlite3.connect('passwords.db')
        self.data_manager = data_manager

    def on_parent(self, widget, parent):
        self.recycleView.data = self.load_passwords()

    def load_passwords(self):
        cursor = self.conn.cursor()
        cursor.execute('SELECT * FROM credentials WHERE user_id=?;', (self.data_manager.user_id, ))
        records = cursor.fetchall()
        recycle_dict = [{"platform": record[0] + ': ' + record[1] + ' | ' + record[2]}
                        for record in records]
        return recycle_dict


class PasswordWidget(BoxLayout):
    orientation = 'vertical'
    platform = StringProperty("")
