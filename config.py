import requests
import json
import time
from loguru import logger
from eth_account import Account as acc
from eth_account.messages import encode_defunct
from web3 import Web3
from random import uniform
from random_user_agent.user_agent import UserAgent
from random_user_agent.params import SoftwareName, OperatingSystem
from threading import Thread
from random import choice
autosoft = """

 _______          _________ _______  _______  _______  _______ _________
(  ___  )|\     /|\__   __/(  ___  )(  ____ \(  ___  )(  ____ \\__   __/
| (   ) || )   ( |   ) (   | (   ) || (    \/| (   ) || (    \/   ) (   
| (___) || |   | |   | |   | |   | || (_____ | |   | || (__       | |   
|  ___  || |   | |   | |   | |   | |(_____  )| |   | ||  __)      | |   
| (   ) || |   | |   | |   | |   | |      ) || |   | || (         | |   
| )   ( || (___) |   | |   | (___) |/\____) || (___) || )         | |   
|/     \|(_______)   )_(   (_______)\_______)(_______)|/          )_(   


Channel: https://t.me/swiper_tools

"""
print(autosoft)

TIMEOUT = [1, 2]
TO_MINT_BADGES = [1, 2, 3, 4]
RUN_THREAD_TIMEOUT = [30, 50]
rucaptcha_token = "ТОКЕН СЮДА ОТ https://rucaptcha.com/api-rucaptcha#intro"


software_names = [SoftwareName.CHROME.value]
operating_systems = [OperatingSystem.WINDOWS.value, OperatingSystem.LINUX.value]   
    
user_agent_rotator = UserAgent(software_names=software_names, operating_systems=operating_systems, limit=100)


ACCS = [i.replace("\n", "").replace(" ", "") for i in open("secrets.txt").readlines()]
PROXIES = [i.replace("\n", "").replace(" ", "") for i in open("proxies.txt").readlines()]

class Page():
    SIGN   = "/user/sign_v2"
    LOGIN  = "/user/login_v2"
    MINT   = "/badge/mint"
    CHECK  = "/badge/user_can_mint"

w3 = Web3(Web3.HTTPProvider("https://rpc.ankr.com/eth"))
results_link = "https://clck.ru/3vyXS"
URL = "https://api.debank.com"