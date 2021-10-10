
import pandas as pd
tx_data = "tx.csv"

tx_data = pd.read_csv(tx_data)
portfolio = tx_data[tx_data['usd']>0].rename(columns={"purchase_price":"avg_purchase_price"})[['ticker','avg_purchase_price']].groupby('ticker').mean().join(tx_data[['ticker','usd','shares']].groupby('ticker').sum()).to_dict(orient="index")
print(portfolio)
tickers = [t.upper() for t in tx_data['ticker'].unique()]
quit()
import datetime
# earliest_date = datetime.datetime.strptime(np_rows[:,2][0], "%m/%d/%Y").date()
# tx_data['date'] = tx_data['date'].apply(lambda d: datetime.datetime.strptime(d, "%m/%d/%Y").date().strftime("%Y%m%d"))
import numpy as np
from dateutil.parser import parse
tx_data['date'] = tx_data['date'].apply(lambda d: np.datetime64(parse(d).date()))
def edit_integer_sign_based_on_tx_type(r):
    m = -1 if r.type == "sell" else 1; 
    r.shares = r.shares * m
    r.usd = r.usd * m
    return r
tx_data = tx_data.transform(edit_integer_sign_based_on_tx_type, axis=1)
# print(tx_data['date'].describe(datetime_is_numeric=True)[['min','max']].to_dict())
# print(tx_data['date'].describe(datetime_is_numeric=True)[['min','max']].apply(lambda d: d.strftime("%Y%m%d")).to_dict())
# print(tx_data)
min_max = tx_data['date'].describe(datetime_is_numeric=True)[['min','max']]
from dateutil.relativedelta import relativedelta
# periods = [(now+relativedelta(months=-(i*3)))
min_date = min_max.loc['min']
max_date = datetime.datetime.now() + relativedelta(days=-1)  #min_max.loc['max']
def your_while_generator():
    # if (max_date.day-1): 
    #     yield max_date.date()

    # i = max_date.month
    # print(i.month % 12 or 12)
    # i = datetime.date(max_date.year, max_date.month, 1)
    i = max_date
    while i > min_date:
        yield i
        # i = i + relativedelta(months=-1) 
        i = i + relativedelta(days=-1) 
    # yield min_date.date()


tx_data['date'] = tx_data['date'].apply(lambda d: d.date().strftime("%Y%m%d"))
tx_data['ticker'] = tx_data['ticker'].apply(lambda d: d.upper())
min_max.loc['min'].strftime("%Y%m%d")
ticks = [i.strftime("%Y%m%d") for i in your_while_generator()]
ticks.sort()
foo = pd.Series([min_max.loc['min'].strftime("%Y%m%d"), max_date.strftime("%Y%m%d"),*tx_data['date'].tolist(), *ticks]).unique()
# foo.reverse()
foo.sort()
import json
cache = json.load(open('foo.json', 'r'))
import urllib.request
has_new_data = 0
from time import sleep
def find_data(data_date):
    global has_new_data
    if(cache.get(data_date)==None):
        print (f"Data not found for {data_date}. Updating cache...")
        has_new_data = 1
        contents = urllib.request.urlopen("https://coinmarketcap.com/historical/"+data_date)
        bytes_str = contents.read()
        data_str = bytes_str.decode("utf-8")
        cache[data_date] = json.loads(data_str[data_str.find('"listingHistorical":{"data":')+28:data_str.find(',"page":1,"sort":""')])
        print("Sleeping for 15 seconds...")
        sleep(15)
    else:
        print (f"Data found for {data_date}. Retrieving...")
    foobar = [my_coin['symbol'] for my_coin in cache.get(data_date) if my_coin['symbol'] in tickers]
    # if(len(foobar)!=len(tickers)):
    #     raise ValueError('Tickers not found.', set(TICKERS).difference(set(foobar)))
    if(has_new_data):
        with open('foo.json', 'w') as outfile:
            json.dump(cache, outfile)
        has_new_data = 0
    return [d for d in cache[data_date]]

    # return [[G['USD']*next(h for h in b if h[1]==G['symbol'])[3],G['symbol'],G['USD'],next(h for h in b if h[1]==G['symbol'])[3], G['id'], G['last_updated']] for G in cache[data_date]]
# api_data = [[d, [ for data in find_data(d) if data['symbol'] in tickers]] for d in foo]
# foo.remove(20210618)
foo = list(foo)
foo.remove('20210618')
api_data = np.ndarray.flatten(np.array([[dict({'id':data['id'],'last_updated':data['last_updated'],'symbol': data['symbol'], 'USD': data['quote']['USD']['price']}) for data in find_data(d) if data['symbol'] in tickers] for d in foo]))
api_data = pd.DataFrame.from_records(api_data)
api_data['last_updated'] = api_data['last_updated'].apply(lambda d: parse(d).date().strftime("%Y%m%d"))
# print(tx_data.merge(api_data.rename(columns={"last_updated":"date","USD":"spot_price"})))
tx_data = tx_data.rename(columns={"usd":"tx_usd"}).merge(api_data.rename(columns={"last_updated":"date","symbol":"ticker","USD":"spot_price_usd"}))
# tx_data = pd.concat([tx_data.rename(columns={"usd":"tx_usd"}), api_data.rename(columns={"last_updated":"date","symbol":"ticker","USD":"spot_price_usd"})], axis=1).dropna(thresh=2)
# tx_data = pd.concat([tx_data.rename(columns={"usd":"tx_usd"}), api_data.rename(columns={"last_updated":"date","symbol":"ticker","USD":"spot_price_usd"})], axis=1).dropna(thresh=2)
# tx_data = tx_data[tx_data['tx_usd'].notnull()]
tx_data['purchase_price'] = tx_data.apply(lambda d: d['tx_usd'] / d['shares'], axis=1)
# tx_data['value'] = tx_data.apply(lambda d: d['shares'] * d['spot_price_usd'], axis=1)
tx_data['value'] = tx_data['shares'].values * tx_data['spot_price_usd'].values
# portfolio = tx_data[['ticker','shares','tx_usd']].groupby('ticker').sum().to_dict()
# print(tx_data.groupby('ticker', as_index=False).sum())
# print( pd.concat([tx_data.rename(columns={"usd":"tx_usd"}), api_data.rename(columns={"last_updated":"date","symbol":"ticker","USD":"spot_price_usd"})], axis=1))
# print(api_data.rename(columns={"last_updated":"date"})
# .join(tx_data,how="left",lsuffix = "_l", rsuffix = '_r' ))
quux = [tx_data[tx_data['ticker'] == t] for t in tickers]
quuz = [q['shares'].cumsum() for q in quux]
fred = list(zip(quuz, quux))

for f in fred:
    # print(f[0].array)
    f[1]['shares_cum_sum'] = f[0].array
# fred  =pd.concat([pd.DataFrame(f[0]) for f in fred],axis=0, ignore_index=True)
fred = [pd.DataFrame(f[1]) for f in fred]
fred = fred[0].append(fred[1].append(fred[2].append(fred[3], ignore_index=True), ignore_index=True))
# print(tx_data.merge(api_data.rename(columns={"last_updated":"date","USD":"spot_price"})))
api_data = api_data.rename(columns={"last_updated":"date","symbol":"ticker"}).merge(fred,how="left")
# api_data['value_cum_cum'] = tx_data.apply(lambda d: d['value'] / d['shares_cum_sum']  if d['value'] else 0, axis=1)
api_data['fee_%'] = api_data.apply(lambda d:  round(d['purchase_price'] / d['spot_price_usd'] - 1, 4)*100 if d['purchase_price'] else 0, axis=1)
api_data['value_cum_sum'] = api_data.apply(lambda d:  d['shares_cum_sum'] * d['spot_price_usd'], axis=1)

# api_data.assign(value=api_data['shares_cum_sum']*api_data['USD'])
# api_data['cum_tx_usd'] = api_data['tx_usd'].cumsum().array
api_data.insert(2, 'tx_usd_cum_sum', api_data['tx_usd'].cumsum().array)
print(api_data)
# print(api_data.groupby(['ticker','date']).max())


# print(api_data.merge(fred[['ticker','shares_cum_sum','date']],left_on=['last_updated','symbol'],right_on=['date','ticker'],how="left")[['ticker','date','shares_cum_sum', 'USD']])
# print(api_data[api_data['symbol']=="BTC"])
# print(api_data.rename(columns={"last_updated":"date","symbol":"ticker","USD":"spot_price_usd"}).merge(tx_data))
# quit()
api_data = api_data.to_dict('records')
# tx_data = tx_data.to_dict('records')
with open('bar.json', 'w') as outfile:
			json.dump({"portfolio": dict({"ticks": ticks,"totals": portfolio}), "data":api_data}, outfile)

print('Your data is ready.')
