from kivymd.uix.screen import MDScreen

from Model.data_manager import data_manager
from View.Managers.notification_manager import NotificationManager


class LoginScreenView(MDScreen):
    """ Screen for loging in. """

    def __init__(self, **kwargs):
        super(LoginScreenView, self).__init__(**kwargs)
        self.data_manager = data_manager
        self.notifier = NotificationManager()

    def on_leave(self, *args):
        for widget in self.ids.values():
            widget.text = ''

    def login(self):
        email = self.ids.user.text
        password = self.ids.code.text
        if not email or not password:
            self.notifier.notify(text='Please fill out all fields.')
            return
        try:
            approved = self.data_manager.get_users_credentials(email, password)
            if approved:
                self.parent.switch_screen('main')
                print(self.data_manager.user_id)
            else:
                self.notifier.notify(text='Entry denied. Check your credentials.', background=[1, 0, 0, .5])
        except Exception as e:
            print(e)
            return
