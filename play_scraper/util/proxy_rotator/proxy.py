__author__ = 'Grainier Perera'
import random
import requests


def get_available_proxies(url):
    proxies_list = requests.get(url).content
    available_proxies = [proxy.rstrip('\r') for proxy in proxies_list.split('\n')]
    good_proxies = []
    for proxy in available_proxies:
        if ':8080' in proxy:
            good_proxies.append(proxy)
            pass
        pass
    return good_proxies
    pass


def get_random_proxy(url):
    available_proxies = get_available_proxies(url)
    if len(available_proxies) > 0:
        random.seed()
        random_proxy = available_proxies[random.randint(0, len(available_proxies) - 1)]
        if random_proxy == '':
            random_proxy = get_random_proxy(url)
            pass
        return random_proxy
        pass
    else:
        return None
    pass