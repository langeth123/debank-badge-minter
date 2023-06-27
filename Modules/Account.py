from config import *
from Modules.Captcha import CaptchaSolver


class Account:
    def __init__(self, secret_key: str, headers: dict, proxies) -> None:
        self.secret_key = secret_key
        self.headers = headers
        self.session = requests.Session()
        self.address = acc.from_key(self.secret_key).address

        self.random_nonce = None
        self.session_id = None

        if proxies is not None:

            self.session.proxies.update(
                {
                    "http": f"http://{proxies}",
                    "https": f"http://{proxies}"
                }
            )
            logger.info(f'[{self.address}] Will use: {proxies}')
    
    def get_validated_account(self):
        account_header = {
            "random_at"   : round(time.time()),
            "random_id"   : self.random_nonce,
            "session_id"  : self.session_id,
            "user_addr"   : self.address.lower(),
            "wallet_type" : "metamask",
            "is_verified" : True
        }

        self.headers["account"] = json.dumps(account_header)
        return self.headers


    def request(self, validate=False, method="post", **kwargs):
        while True:
            try:
                if validate is True:
                    kwargs["headers"] = self.get_validated_account()

                if method == "post":
                    response = self.session.post(**kwargs)
                elif method == "get":
                    response = self.session.get(**kwargs)

                if response.status_code == 200:

                    timing = uniform(TIMEOUT[0], TIMEOUT[1])
                    logger.info(f'[{self.address}] Got good response, sleeping: {timing}')
                    time.sleep(timing)

                    return response.json()

                else:
                    if response.status_code == 429:
                        logger.error(f'[{self.address} - {kwargs["url"]}] RateLimited: {response.status_code}')
                        self.headers["user-agent"] = user_agent_rotator.get_random_user_agent()
                        time.sleep(30)
                    else:
                        logger.error(f'[{self.address} - {kwargs["url"]}] Bad status code: {response.status_code}')
                        time.sleep(10)


            except Exception as error:
                logger.error(f'[{self.address} - {kwargs["url"]}] failed to make request | {error}')
                time.sleep(10)
    

    def sign_message(self, message_text: str) -> str:
        message = encode_defunct(text=message_text)
        signed_message =  w3.to_hex(w3.eth.account.sign_message(message, private_key=self.secret_key).signature)

        return signed_message
    
    def login(self):
        self.session.get("https://debank.com/badge?t=1686927046829&r=62071")

        json_data = {
            'id': self.address.lower(),
        }
    
        text_to_confirm = self.request(url=URL + Page.SIGN, json=json_data, headers=self.headers)["data"]["text"]
        logger.info(f'[{self.address}] Got text to confirm')

        self.random_nonce = text_to_confirm.split("Nonce: ")[1].split("\n")

        json_data = {
            'signature': self.sign_message(text_to_confirm),
            'id': self.address.lower()
        }

        response = self.request(url=URL + Page.LOGIN, json=json_data, headers=self.headers)
        self.session_id = response["data"]["session_id"]

        logger.success(f'[{self.address}] Was made login to acc. Session: {self.session_id}')

    def mint(self, id: int):
        # {'_cache_seconds': 0, '_seconds': 0.02199578285217285, '_use_cache': False, 'error_code': 'mint badge failed', 'error_msg': ''}
        solver = CaptchaSolver(
            {
                "api"        : rucaptcha_token,
                "google_key" : "6LfoubcmAAAAAOa4nrHIf2O8iH4W-h91QohdhXTf",
                "url"        : f"https://debank.com/badge/{id}"
            }
        )

        json_data = {
            'id'    : str(id),
            "token" : solver.get_captcha()
        }
        response = self.request(validate=True, url=URL + Page.MINT, json=json_data, headers=self.headers)
        
        if response["error_code"] == 0:
            inner_id = response["data"].get("inner_id")

            logger.success(f"[{self.address}] Minted badge. Id: {inner_id}")
        else:
            logger.error(f'[{self.address}] Failed to mint badge with id: {id}. Error: {response["error_code"]}')

    def check_eligible(self, id: int):
        while True:
            params = {
                'id': str(id),
            }
        
            response = self.request(validate=True, method="get", url=URL + Page.CHECK, params=params, headers=self.headers)

            if response["error_code"] == 0:

                return response["data"].get("can_mint")
            
            else:
                logger.error(f'[{self.address}] Failed to check badge info: {response["error_code"]}')
                time.sleep(5)
