import requests
from utils import load_settings

LINE_NOTIFY_API = "https://notify-api.line.me/api/notify"


class LineNotifier(object):

    def __init__(self, test=False):
        self.settings = load_settings("settings.yml")["line"]
        self.environment = "test" if test else "production"

    def send(self, message: str):
        token = self.settings["token"][self.environment]
        headers = {'Authorization': f'Bearer {token}'}
        data = {'message': message}
        requests.post(LINE_NOTIFY_API, headers=headers, data=data)
