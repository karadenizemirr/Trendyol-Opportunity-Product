import requests
import time
from rich.console import Console

class Telegram:
    def __init__(self, token, user_id):
        self.URL = f"https://api.telegram.org/bot{token}"
        self.USER_ID = user_id
        self.session = requests.Session()
        self.console = Console()


    def sendMessage(self, message):
        payloads = {
            "chat_id": self.USER_ID,
            "parse_mode": "HTML",
            "text": message
        }
        try:
            req = self.session.post(f"{self.URL}/sendMessage", data=payloads).json()
            if req['ok']:
                self.console.log("Mesaj gönderildi.", style="bold green")
            return True
        except:
            self.console.log("Mesaj gönderilemedi.", style="bold red")