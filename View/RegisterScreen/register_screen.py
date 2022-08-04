import uuid
from email_validator import validate_email, EmailNotValidError

from kivymd.uix.screen import MDScreen

from View.Managers.notification_manager import NotificationManager
from Model.user_manager import user_manager
from utils import get_password_hash


class RegisterScreenView(MDScreen):
    """ MDScreen for registration of users. """

    def __init__(self, **kwargs):
        super(RegisterScreenView, self).__init__(**kwargs)
        self.notifier = NotificationManager()
        self.user_manager = user_manager

    def on_leave(self, *args):
        for widget in self.ids.values():
            widget.text = ''

    def validate_email(self, email):
        try:
            valid = validate_email(email)
            email = valid.email
            return email
        except EmailNotValidError as e:
            self.notifier.notify(str(e), background=[1, 0, 0, .7])

    def validate_password(self, pass1, pass2):
        if pass1 == pass2:
            return get_password_hash(pass1)
        self.notifier.notify(text='Make sure that your passwords match.')
        return False

    def register(self):
        email = self.validate_email(self.ids.email.text)
        if not email:
            return

        if self.check_email_usage(email):
            self.notifier.notify(text='User with this email already exists.', background=[1, 0, 0, .5])
            return

        password1 = self.ids.password1.text
        password2 = self.ids.password2.text
        if password := self.validate_password(password1, password2):
            user_id = uuid.uuid4().hex
            with self.user_manager as register:
                register.register_user(user_id, email, password)
                self.notifier.notify(text='You successfully registered. You can login now.')

    def check_email_usage(self, email: str):
        with self.user_manager as manager:
            return manager.check_email_usage(email)
