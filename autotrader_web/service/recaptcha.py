import requests
import json


class RecaptchaService:

    def __init__(self, secret):
        self.secret = secret

    def verify_token(self, *args, **kwargs):
        try:
            token = kwargs['token'] if "token" in kwargs.keys() else None
            response = requests.post("https://www.google.com/recaptcha/api/siteverify", data={
                "secret":self.secret,
                "response":token
            })
            response = json.loads(response.text).get("success")
            return response
        except Exception as e:
            print(e)
            return False
