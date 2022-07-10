import sqlite3

from kivy.properties import ObjectProperty, StringProperty
from kivy.uix.boxlayout import BoxLayout
from kivymd.uix.screen import MDScreen


class CredentialScreenView(MDScreen):
    recycleView = ObjectProperty(None)

    def __init__(self, **kwargs):
        super(CredentialScreenView, self).__init__(**kwargs)
        self.conn = sqlite3.connect('passwords.db')

    def on_parent(self, widget, parent):
        self.recycleView.data = self.load_passwords()

    def load_passwords(self):
        cursor = self.conn.cursor()
        cursor.execute('SELECT * FROM credentials')
        records = cursor.fetchall()
        recycle_dict = [{"platform": record[0] + ': ' + record[1] + ' | ' + record[2]}
                        for record in records]

        return recycle_dict


class PasswordWidget(BoxLayout):
    orientation = 'vertical'
    platform = StringProperty("")