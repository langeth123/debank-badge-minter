import requests
from time import sleep
import traceback


class CaptchaSolver:
    def __init__(self, data: dict):
        self.API = data.get("api")
        self.GOOGLE_KEY = data.get("google_key")
        self.URL = data.get("url")
        self.PARAMS = {
            "key": self.API,
            "method": "userrecaptcha",
            "googlekey": self.GOOGLE_KEY,
            "pageurl": self.URL,
            "json": 1
        }
        self.CAPTCHA_URL = "http://rucaptcha.com/in.php"
        self.CAPTCHA_RES = "http://rucaptcha.com/res.php"

    def create_new_solve(self, **kwargs) -> str:
        if kwargs.get("reg") is None:
            response = self._req(self.CAPTCHA_URL, params=self.PARAMS)
        print(f'New captcha was created')
        return response.get("request")

    def get_captcha_solve(self, id_request: str):
        params = {
            "key": self.API,
            "action": "get",
            "id": id_request,
            "json": 1
        }
        response = {"status": 0}
        while response["status"] == 0:
            response = self._req(self.CAPTCHA_RES, params=params)
            sleep(2)
        return response.get("request")

    def get_captcha(self, **kwargs):
        new_captcha = self.create_new_solve(**kwargs)
        return self.get_captcha_solve(new_captcha)
    
    def _req(self, url, **kwargs):
        try:
            with requests.get(url, **kwargs) as resposne:
                return resposne.json()
        except:
            print(traceback.format_exc())
            print("BAD CAPTCHA REQ, TRYING AGAIN"), sleep(2)
            return self._req(url, **kwargs)