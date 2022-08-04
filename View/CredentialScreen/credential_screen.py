from kivy.properties import ObjectProperty, StringProperty
from kivy.uix.boxlayout import BoxLayout
from kivymd.uix.screen import MDScreen

from Model.data_manager import data_manager


class CredentialScreenView(MDScreen):
    """ RecycleView Screen for displaying all passwords. """
    recycleView = ObjectProperty(None)

    def __init__(self, **kwargs):
        super(CredentialScreenView, self).__init__(**kwargs)
        self.data_manager = data_manager

    def on_parent(self, widget, parent):
        print(widget, parent)
        self.recycleView.data = self.load_passwords()

    def load_passwords(self):
        with self.data_manager as keeper:
            passwords = keeper.get_users_passwords(self.data_manager.user_id)

        return [{"platform": f'{record[0]}: {record[1]} | {record[2]}'} for record in passwords]


class PasswordWidget(BoxLayout):
    """ RecycleView Widget """
    orientation = 'vertical'
    platform = StringProperty("")
