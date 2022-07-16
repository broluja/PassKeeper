import uuid

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

    def register(self):
        self.user_manager.connect()
        email = self.ids.email.text
        if not email:
            self.notifier.notify(text='PLease enter valid email.')
            return
        if self.check_email_usage(email):
            self.notifier.notify(text='User with this email already exists.')
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

    def check_email_usage(self, email):
        search = self.user_manager.cursor.execute(f'SELECT * FROM users WHERE email=?;', (email, ))
        user = search.fetchone()
        return user
