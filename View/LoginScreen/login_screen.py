from kivymd.uix.screen import MDScreen

from Model.data_manager import data_manager
from View.Managers.notification_manager import NotificationManager


class LoginScreenView(MDScreen):
    """ Screen for loging in. """
    def __init__(self, **kwargs):
        super(LoginScreenView, self).__init__(**kwargs)
        self.data_manager = data_manager
        self.notifier = NotificationManager()

    def login(self):
        username = self.ids.user.text
        password = self.ids.code.text
        if not username or not password:
            self.notifier.notify(text='Please fill out all fields.')
            return
        if username == self.data_manager.username and password == self.data_manager.password:
            self.parent.switch_screen('main')
            return
        else:
            self.notifier.notify(text='Please check your credentials.')
            return
