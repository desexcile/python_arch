from sys import version_info
from datetime import date
import requests


# front controller
def secret_front(request):
    request['date'] = date.today()


def other_front(request):
    request['key'] = 'key'


def version_front(request):
    request['python_ver'] = f'{version_info.major}.{version_info.minor}'


def btc_to_usd(request):
    try:
        current = requests.get('https://blockchain.info/ru/ticker')
        btc = current.json().get('USD')['last']
        currency = current.json().get('USD')['symbol']
        request['btc_to_usd'] = f'{currency}{btc}'
    except Exception:
        request['btc_to_usd'] = 'Даже и не знаю какой курс..'


fronts = [secret_front, other_front, version_front, btc_to_usd]


