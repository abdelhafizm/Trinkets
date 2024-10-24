import requests
import keyring


def send_notification(message, priority=0, image_path=None):
    url = 'https://api.pushover.net/1/messages.json'
    params = {
        'token': keyring.get_password('Pushover', 'token'),
        'user': keyring.get_password('Pushover', 'user'),
        'device': keyring.get_password('Pushover', 'device'),
        'message': message,
        'priority': priority
    }
    files = {
        'attachment': ('img', open(image_path, 'rb'))
    } if image_path else {}

    r = requests.post(url=url, data=params, files=files)
