# from requests import Request, Session
# from requests.exceptions import ConnectionError, Timeout, TooManyRedirects
# import json
# data = {}
# url = 'https://pro-api.coinmarketcap.com/v1/cryptocurrency/listings/latest'
# parameters = {
#   'start':'1',
#   'limit':'500',
#   'convert':'USD'
# }
# headers = {
#   'Accepts': 'application/json',
#   'X-CMC_PRO_API_KEY': 'd524261c-b415-4a78-a341-ceba5a2dc64a',
# }

# session = Session()
# session.headers.update(headers)

# try:
#   response = session.get(url, params=parameters)
#   data = json.loads(response.text)
#   print(data)
# except (ConnectionError, Timeout, TooManyRedirects) as e:
#   print(e)

# with open('cmc_coin_list.json', 'w') as outfile:
#   json.dump(data, outfile)
import json
import pandas as pd


# Python3 code to demonstrate working of
# Standard deviation of list
# Using sum() + list comprehension
  
# initializing list
test_list = pd.Series([1,1])
  
# printing list
# print("The original list : " + str(test_list))
  
# Standard deviation of list
# Using sum() + list comprehension
# mean = sum(test_list) / len(test_list)
# variance = sum([((x - mean) ** 2) for x in test_list]) / len(test_list)
# res = variance ** 0.5
  
# Printing result
# print("Standard deviation of sample is : " + str(res))
print("1st Quintile of sample is : " + str(test_list.quantile(.25)))
Top5 = test_list.quantile(.25) 

async def handle(request):
    name = request.match_info.get('name', "Anonymous")
    text = "Hello, " + name
    return web.Response(text=text)

from aiohttp import web
app = web.Application()
import socketio
sio = socketio.AsyncServer(async_mode='aiohttp',  cors_allowed_origins='*')
sio.attach(app)
import aiohttp_cors
cors = aiohttp_cors.setup(app)
routes = [web.get('/', handle), web.get('/{name}', handle)]
app.router.add_routes(routes)
# app.router.add_static("/", rootdir) if you want to serve static, and this has to be absolutely the last route since it's the root. Adding any route after this becomes ignored as '/' matches everthing.
for resource in app.router._resources:
  # Because socket.io already adds cors, if you don't skip socket.io, you get error saying, you've done this already.
  if resource.raw_match("/socket.io/"):
    continue
  cors.add(resource, { '*': aiohttp_cors.ResourceOptions(allow_credentials=True, expose_headers="*", allow_headers="*") })


@sio.on('connect')
async def connect(sid, environ): 
    print('connect ', sid)
    await sio.emit('details', {'data': 'foobar'}) # works as expected

@sio.event
def disconnect(sid):
    print('disconnect ', sid)

print('REST services running on port 8080...')

import urllib.request
def fetch(url):
    contents = urllib.request.urlopen(url)
    bytes_str = contents.read()
    data_str = bytes_str.decode("utf-8")
    return data_str
import pandas as pd
import json
# fetch CoinGecko coin list from URL or cache
# CoinGecko_coinlist = fetch("https://api.coingecko.com/api/v3/coins/list")
# with open('CoinGecko_coinlist.json', 'w') as outfile:
#     json.dump(CoinGecko_coinlist, outfile)
CoinGecko_coinlist = json.load(open('CoinGecko_coinlist.json', 'r'))
CoinGecko_coinlist = pd.DataFrame(json.loads(CoinGecko_coinlist))#.set_index('id')
# Coinmarketcap_coinlist = pd.DataFrame(list(json.load(open('foo.json', 'r')).values())[2])
Coinmarketcap_coinlist = pd.DataFrame(list(json.load(open("cmc_coin_list.json",'r'))['data']))[['name','symbol','id']]
Coinmarketcap_coinlist['name_coinmarketcap'] = Coinmarketcap_coinlist['name']
Coinmarketcap_coinlist['name'] = Coinmarketcap_coinlist['name'].apply(lambda x: x.lower())
CoinGecko_coinlist['symbol'] = CoinGecko_coinlist['symbol'].apply(lambda x: x.upper())
CoinGecko_coinlist['name_coingecko'] = CoinGecko_coinlist['name']
CoinGecko_coinlist['name'] = CoinGecko_coinlist['name'].apply(lambda x: x.lower())
foobar = Coinmarketcap_coinlist.merge(CoinGecko_coinlist, on=['symbol','name']).rename(columns={"id_y":"id_coingecko","id_x":"id_coinmarketcap"}).values.tolist()
print(foobar)

#.set_index('id')
# if __name__ == '__main__':
#     web.run_app(app)