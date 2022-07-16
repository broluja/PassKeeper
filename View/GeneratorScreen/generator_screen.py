import string
import secrets

from kivymd.uix.screen import MDScreen
from kivy.properties import NumericProperty, ObjectProperty, StringProperty


class GeneratorScreenView(MDScreen):
    """ MDScreen for generating new passwords. """
    LEN_PASSWORD = NumericProperty(12)
    my_pass = ObjectProperty("")
    label_text = StringProperty("Enter number of characters")

    def generate_password(self):
        """ Create new password using 'string' and 'secrets' module """
        try:
            self.LEN_PASSWORD = int(self.ids.num_char.text)
            if self.LEN_PASSWORD > 24:
                self.label_text = "Maximum of characters is 24."
                self.ids.label2.text = ''
                return

            if self.LEN_PASSWORD < 6:
                self.label_text = "Minimum number of characters is 6."
                self.ids.label2.text = ''
                return
            characters = string.ascii_letters + string.digits
            generated_password = "".join(secrets.choice(characters) for _ in range(self.LEN_PASSWORD))
            self.label_text = f"\nYour password is: [ref=world][color=0000ff]\n{generated_password}[/color][/ref]" \
                              f"\nClick on password to copy."
            self.ids.label2.text = ''

        except ValueError:
            self.label_text = "Please input an integer number."

    def print_it(self, value):
        self.my_pass = value.text.split("[ref=world][color=0000ff]")[1].split("[")[0]
        self.ids.label2.text = 'Copied!'
        self.ids.num_char.text = ''
