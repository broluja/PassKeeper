from kivymd.uix.dialog import MDDialog
from kivymd.uix.button import MDFillRoundFlatButton
from kivymd.uix.textfield import MDTextField
from kivy.uix.boxlayout import BoxLayout
from kivy.metrics import dp

from View.Managers.notification_manager import NotificationManager


class Content(BoxLayout):
    """ Content for the first MDDialog box, for verifying code during user`s registration. """
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.orientation = 'vertical'
        self.size_hint_y = None
        self.add_text_field()

    def add_text_field(self):
        text_field = MDTextField()
        text_field.hint_text = 'CODE'
        text_field.max_text_length = 5
        text_field.write_tab = False
        text_field.size_hint = (.2, None)
        text_field.font_size = dp(26)
        text_field.pos_hint = {'top': 4, 'center_x': .5}
        self.add_widget(text_field)


class CodeDialog(MDDialog):
    """ MDDialog box for code verification during registration of User. """
    def __init__(self, **kwargs):
        self.title = 'Code have been sent to your email.'
        self.type = 'custom'
        self.content_cls = Content()
        self.buttons = [
            MDFillRoundFlatButton(text="CLOSE", on_press=self.close),
            MDFillRoundFlatButton(text="CONFIRM", on_press=self.confirm),
        ]
        self.size_hint = None, None
        self.y = 1
        self.auto_dismiss = False
        super().__init__(**kwargs)
        self.notifier = NotificationManager()

    def close(self, widget):
        self.dismiss()

    def confirm(self, obj):
        pass

    def failure(self, result):
        self.notifier.notify(text=result, duration=4)

    def success(self, result):
        if not result['success']:
            self.notifier.notify(text='Wrong code. Try again.', duration=4)
            return
        self.notifier.notify(text='Verified! You can login now.', duration=4)
        self.dismiss()
