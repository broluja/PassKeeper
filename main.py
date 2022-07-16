import os
from pathlib import Path

from kivy import platform
from kivy.config import Config
if platform != 'android': Config.set("graphics", "width", "630"); Config.set("graphics", "height", "950")
else: Config.set("graphics", "width", "1500"); Config.set("graphics", "height", "900")
from kivy.metrics import dp
from kivymd.app import MDApp

from View.Managers.manager_screen import ManagerScreen

os.environ['PASS_APP'] = str(Path(__file__).parent)


class PassApp(MDApp):

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.theme_cls.theme_style = 'Light'
        self.theme_cls.primary_palette = 'LightBlue'
        self.manager_screen = ManagerScreen()
        if platform != 'android':
            self.textfield_width = dp(260)
            self.textfield_height = dp(48)
            self.textfield_font = dp(28)
            self.font_style = 'H4'
            self.button_size = dp(200)
        else:
            self.textfield_width = dp(550)
            self.textfield_height = dp(90)
            self.textfield_font = dp(46)
            self.font_style = 'H1'
            self.button_size = dp(300)

    def __str__(self):
        return 'Password App'

    def build(self):
        self.manager_screen.add_widget(self.manager_screen.create_screen('login'))
        return self.manager_screen


PassApp().run()
