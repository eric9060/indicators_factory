import base64
from random import randint
import time
import scrapy

from crawlers.utils import SpiderBase
from jinja2 import Template
from crawlers.utils.group_alarm import catch_except
from crawlers.utils.humanize import humanize_float_en
from crawlers.utils.redis_conn import rds

address_label_map = {
    "34xp4vRoCGJym3xR7yCVPFHoCNxv4Twseo": "Binance-coldwallet",
    "bc1qgdjqv0av3q56jvd82tkdjpy7gdp9ut8tlqmgrpmv24sq90ecnvqqjwvw97": "Bitfinex-coldwallet",
    "3JJmF63ifcamPLiAmLgG96RA599yNtY3EQ": "Binance-coldwallet",
    "3LYJfcfHPXYJreMsASk2jkn69LWEYKzexb": "Binance-BTCB-Reserve",
    "3LCGsSmfr24demGvriN4e3ft8wEcDuHFqh": "CoinCheck",
    "3JZq4atUahhuA9rLhXLMhhTo133J9rF97j": "Bitfinex-coldwallet",
    "38UmuUqPCrFmQo4khkomQwZ4VbY2nZMJ67": "OKEX-coldwallet",
    "3Kzh9qAqVWQhEsfQz7zEQL1EuSx5tyNLNS": "Gemini-coldwallet",
    "bc1qm34lsc65zpw79lxes69zkqmk6ee3ewf0j77s3h": "Binance-wallet",
    "385cR5DM96n1HvBDMzLHPYcw89fZAXULJP": "Bittrex-coldwallet",
    "3FupZp77ySr7jwoLYEJ9mwzJpvoNBXsBnE": "Gemini-wallet",
    "3H5JTt42K7RmZtromfTSefcMEFMMe18pMD": "Poloniex-coldwallet",
    "3BMEXqGpG4FxBA1KWhRFufXfSTRgzfDBhJ": "BITMEX-coldwallet",
    "3DwVjwVeJa9Z5Pu15WHNfKcDxY5tFUGfdx": "OKEX-coldwallet",
    "36NkTqCAApfRJBKicQaqrdKs29g6hyE4LS": "OKEX-coldwallet"
}

def encryptApiKey():
    apikey = 'a2c903cc-b31e-4547-9299-b6d07b7631ab'
    return apikey[8:]+apikey[:8]

def encryptTime():
    e = round(time.time()*1000)
    t = str(1*e + 1111111111111)
    return f'{t}{randint(0,10)}{randint(0,10)}{randint(0,10)}'

def getApiKey():
    r = encryptApiKey() + '|' + encryptTime()
    res = base64.b64encode(r.encode('utf-8'))
    return res


class BTCRich(SpiderBase):
    name = 'idx-btc-rich'

    ts_ms = round(time.time()*1000)
    url = f'https://www.oklink.com/api/explorer/v1/btc/richers?t={ts_ms}&offset=0&limit=20'
    headers = {'x-apiKey': getApiKey()}

    def start_requests(self):
        yield scrapy.Request(url=self.url, headers=self.headers)

    @catch_except
    def parse(self, response, **kwargs):
        data = response.json()
        print(data)
        #print(data['hits'][0])

# 获取到之后要存到 redis，下一次才能做减法