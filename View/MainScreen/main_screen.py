from kivy.properties import ObjectProperty
from kivy.uix.boxlayout import BoxLayout
from kivymd.uix.screen import MDScreen
from kivymd.uix.dialog import MDDialog
from kivymd.uix.button import MDRectangleFlatIconButton

from Model.data_manager import data_manager


class Content(BoxLayout):

    def __init__(self, **kwargs):
        super(Content, self).__init__(**kwargs)
        self.data_manager = data_manager

    def remove_record(self):
        record = self.ids.platform.text
        if not record:
            self.ids.label_info.text = 'Field cannot be empty.'
            return
        try:
            self.data_manager.connect()
            self.data_manager.cursor.execute(f'DELETE FROM credentials WHERE platform=?', (record, ))
            self.data_manager.commit()
            if self.data_manager.cursor.rowcount:
                self.ids.label_info.text = 'Removed.'
                self.ids.platform.text = ''
            else:
                self.ids.label_info.text = f'No such platform - {record}.'
                self.ids.platform.text = ''

        except Exception as e:
            self.ids.label_info.text = e


class MainScreenView(MDScreen):
    """ Main APP screen. """
    data = {
        'Create Password': 'folder-plus',
        'Credentials': 'recycle',
        'Remove': 'card-remove',
        'Back': 'keyboard-backspace'
    }
    INSTRUCTIONS = [
        'CREATE TABLE if not exists credentials(platform TEXT, username TEXT, password TEXT)',
    ]
    dialog = ObjectProperty()

    def __init__(self, **kwargs):
        super(MainScreenView, self).__init__(**kwargs)
        self.data_manager = data_manager
        self.data_manager.cursor.execute(self.INSTRUCTIONS[0])
        self.data_manager.commit()

    def paste_password(self):
        third_screen = self.parent.get_screen('generator')
        my_password = third_screen.my_pass
        self.ids.password.text = my_password

    def add_data(self):
        site = self.ids.platform.text
        username = self.ids.username.text
        password = self.ids.password.text
        if not site or not username or not password:
            self.ids.info.text = 'Please fill out all fields'
            return
        self.data_manager.connect()
        self.data_manager.cursor.execute('INSERT INTO credentials VALUES (?,?,?)', (site, username, password))
        self.data_manager.commit()
        self.clear_data()
        self.ids.info.text = 'Committed'

    def clear_data(self):
        self.ids.platform.text = ''
        self.ids.username.text = ''
        self.ids.password.text = ''
        self.ids.info.text = ''

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
