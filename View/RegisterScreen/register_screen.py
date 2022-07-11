from kivy.properties import ObjectProperty
from kivymd.uix.screen import MDScreen

from View.widgets.custom_widgets import CodeDialog
from View.Managers.notification_manager import NotificationManager


class RegisterScreenView(MDScreen):
    dialog = ObjectProperty()

    def __init__(self, **kwargs):
        super(RegisterScreenView, self).__init__(**kwargs)
        self.notifier = NotificationManager()

    def verify_code(self):
        email = self.ids.email.text
        password1 = self.ids.password1.text
        password2 = self.ids.password2.text
        self.http_manager.register_user(self.success, self.failure, self.failure, email, password1, password2)

    def failure(self, result):
        self.notifier.notify(text=result, duration=4)

    def success(self, result):
        if not result['success']:
            self.notifier.notify(text=result['message'], duration=4)
            return
        self.ids.email.text = ''
        self.ids.password1.text = ''
        self.ids.password2.text = ''
        self.code_dialog_box()

    def code_dialog_box(self):
        self.dialog = CodeDialog()
        self.dialog.open()