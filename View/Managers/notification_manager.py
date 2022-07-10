from plyer import notification

from kivy import platform
from kivymd.toast import toast


class NotificationManager(object):
    """ Class for serving proper notifications, depending on platform that holds Load66App. """
    def __init__(self):
        self.platform = platform

    def __str__(self):
        return f'Notification Manager for {platform}'

    def notify(self, text, duration=4, background=None):
        if self.platform == 'android':
            notification.notify(title='Info', message=text, timeout=duration)
        else:
            toast(text=text, duration=duration, background=background)
