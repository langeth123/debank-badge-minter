from config import *
from Modules.Account import Account


def handler(secret_key: str, headers: dict, proxies: str):
    account = Account(secret_key, headers, proxies)
    account.login()

    eligible_list = []
    for i in TO_MINT_BADGES:
        if account.check_eligible(i):
            eligible_list.append(i)
    
    logger.info(f'[{account.address}] Got elig badges: {"".join(f"{i} " for i in eligible_list)}')
    
    for k in eligible_list:
        account.mint(k)

def thread_runner():
    threads = []

    for i in ACCS:
        headers = {
            'authority': 'api.debank.com',
            'accept': '*/*',
            'accept-language': 'ru-RU,ru;q=0.9,en-US;q=0.8,en;q=0.7,uk;q=0.6,pl;q=0.5,cy;q=0.4,fr;q=0.3',
            'content-type': 'application/json',
            'origin': URL,
            'referer': URL,
            'sec-ch-ua': '"Not.A/Brand";v="8", "Chromium";v="114", "Google Chrome";v="114"',
            'sec-ch-ua-mobile': '?0',
            'sec-ch-ua-platform': '"Windows"',
            'sec-fetch-dest': 'empty',
            'sec-fetch-mode': 'cors',
            'sec-fetch-site': 'same-site',
            'source': 'web',
            'user-agent': user_agent_rotator.get_random_user_agent(),
            'x-api-ver': 'v2'
        }
        
        if len(PROXIES) != 0:
            proxies = choice(PROXIES)
        else:
            proxies = None

        threads.append(Thread(target=handler, args=(i, headers, proxies,)))
    
    for i in threads:
        i.start()
        timing = uniform(RUN_THREAD_TIMEOUT[0], RUN_THREAD_TIMEOUT[1])
        logger.info(f'[THREAD RUNNER] Will run next thread in: {timing} sec')

        time.sleep(timing)
    
    for k in threads:
        k.join()

    logger.success(f"Soft successfully end work. Check results here --> {results_link} <--")



if __name__ == "__main__":
    logger.info(f"Found: {len(ACCS)} accs")

    thread_runner()
