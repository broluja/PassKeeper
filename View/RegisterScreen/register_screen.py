import uuid
from email_validator import validate_email, EmailNotValidError

from kivymd.uix.screen import MDScreen

from View.Managers.notification_manager import NotificationManager
from Model.user_manager import user_manager
from utils import get_password_hash


class RegisterScreenView(MDScreen):
    """ MDScreen for registration of users. """
    INSTRUCTION = 'INSERT INTO users VALUES(?, ?, ?);'

    def __init__(self, **kwargs):
        super(RegisterScreenView, self).__init__(**kwargs)
        self.notifier = NotificationManager()
        self.user_manager = user_manager

    def on_leave(self, *args):
        for widget in self.ids.values():
            widget.text = ''

    def register(self):
        self.user_manager.connect()
        email = self.ids.email.text
        try:
            valid = validate_email(email)
            email = valid.email
        except EmailNotValidError as e:
            self.notifier.notify(str(e), background=[1, 0, 0, .7])
            return
        if self.check_email_usage(email):
            self.notifier.notify(text='User with this email already exists.', background=[1, 0, 0, .5])
            return
        password1 = self.ids.password1.text
        password2 = self.ids.password2.text
        if password1 == password2:
            password = get_password_hash(password1)
        else:
            self.notifier.notify(text='Make sure that your passwords match.')
            return
        user_id = uuid.uuid4().hex
        try:
            self.user_manager.cursor.execute(self.INSTRUCTION, (user_id, email, password))
            self.notifier.notify(text='You successfully registered. You can login now.')
        finally:
            self.user_manager.commit()

    def check_email_usage(self, email: str):
        search = self.user_manager.cursor.execute(f'SELECT * FROM users WHERE email=?;', (email,))
        user = search.fetchone()
        return user
