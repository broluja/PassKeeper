from kivy.properties import ObjectProperty
from kivy.uix.boxlayout import BoxLayout
from kivymd.uix.screen import MDScreen
from kivymd.uix.dialog import MDDialog
from kivymd.uix.button import MDRectangleFlatIconButton

from Model.data_manager import data_manager
from View.Managers.notification_manager import NotificationManager


class Content(BoxLayout):
    """ Content for Main Screen`s Dialog box for deleting passwords. """
    def __init__(self, **kwargs):
        super(Content, self).__init__(**kwargs)
        self.data_manager = data_manager

    def remove_record(self):
        platform = self.ids.platform.text
        if not platform:
            self.ids.label_info.text = 'Field cannot be empty.'
            return

        with self.data_manager as deleter:
            deleter.delete_credential(platform, self.data_manager.user_id)
            if self.data_manager.cursor.rowcount:
                self.ids.label_info.text = 'Removed.'
            else:
                self.ids.label_info.text = f'No such platform - {platform}.'
            self.ids.platform.text = ''


class MainScreenView(MDScreen):
    """ APP`s main screen. """
    data = {
        'Create Password': 'folder-plus',
        'Credentials': 'recycle',
        'Remove': 'card-remove',
        'Back': 'keyboard-backspace'
    }
    dialog = ObjectProperty()

    def __init__(self, **kwargs):
        super(MainScreenView, self).__init__(**kwargs)
        self.data_manager = data_manager
        self.notifier = NotificationManager()

    def paste_password(self):
        try:
            third_screen = self.parent.get_screen('generator')
            my_password = third_screen.my_pass
            self.ids.password.text = my_password
        except Exception as e:
            print(e)
            self.notifier.notify('Nothing to paste')

    def get_users_data(self):
        site = self.ids.platform.text
        username = self.ids.username.text
        password = self.ids.password.text
        return (site, username, password) if site and username and password else False

    def add_data(self):
        data = self.get_users_data()
        if not data:
            self.ids.info.text = 'Please fill out all fields'
            return
        with self.data_manager as adder:
            adder.add_new_credential(*data, self.data_manager.user_id)
        self.clear_data()
        self.ids.info.text = 'Committed'

    def clear_data(self):
        for widget in self.ids.values():
            widget.text = ''

    def open_dialog(self):
        self.dialog = MDDialog(
            title='Delete',
            text='Enter name of the platform',
            type='custom',
            content_cls=Content(),
            buttons=[
                MDRectangleFlatIconButton(text="CLOSE", on_press=self.close),
                ]
        )
        self.dialog.open()

    def close(self, widget):
        self.dialog.remove_widget(self.dialog.content_cls)
        self.dialog.dismiss()

    def callback(self, instance):
        if instance.icon == 'recycle':
            self.parent.switch_screen('credentials')
        elif instance.icon == 'folder-plus':
            self.parent.switch_screen('generator')
        elif instance.icon == 'card-remove':
            self.open_dialog()
        elif instance.icon == 'keyboard-backspace':
            self.parent.switch_screen('login')
