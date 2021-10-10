HAS_NEW_DATA = 0 
PERIODS = 5
TICKERS = ['MATIC', 'ETH', 'BTC', 'VET']
# TICKERS = ['REN', 'ZIL', 'ETH', 'BTC', 'VET']
# TICKERS = ['DENT']
# TICKERS = ['SAND','ENJ','MANA']
# TICKERS = ['UNI', 'AAVE', 'ZRX', 'MKR', 'COMP', 'YFI', 'SNX', 'SUSHI', 'UMA']
URL = "https://coinmarketcap.com/historical/"
# WEIGHTS = [0.013149107,0.021471593,0.021276873,0.034428597,0.055709704,0.090145152,0.145865942,0.236029032,0.381924]
# WEIGHTS = [100]
WEIGHTS = [38, 24, 29, 9]
# WEIGHTS = [38, 23.5, 14.5, 26]
# TICKERS = ['ADA', 'BTC', 'ETH']
# WEIGHTS = [62, 23.5, 14.5]

from itertools import permutations
PERMUTATIONS = [*map(lambda x : [*map(lambda y: list(y), x)], [list(zip(each_permutation, TICKERS)) for each_permutation in permutations(WEIGHTS, len(TICKERS))])]
waldo = set()
def check_for_duplicate(p):
	print(len(p))
    # plugh = ''.join(list(map(lambda x: ''.join([str(y) for y in x]), p))
	plugh = ''.join(list(map(lambda x: ''.join([str(y) for y in x]), p)))
	if(plugh in waldo):
		return False
	waldo.add(plugh)
	return True
#                 return this.res.filter(f => {
#                     let bar = f[0][1].map(e => e[0] + e[1]).join('');
#                     if (foo.has(bar)) return 0;
#                     return foo.add(bar);
# print (PERMUTATIONS)
PERMUTATIONS = list(filter(check_for_duplicate, PERMUTATIONS))

import json
cache = json.load(open('foo.json', 'r'))

from datetime import timedelta
import calendar
import datetime
import urllib.request

def add_months(sourcedate, months):
    month = sourcedate.month - 1 - months
    year = sourcedate.year + month // 12
    month = (month % 12 - 1) or 12
    day = min(sourcedate.day, calendar.monthrange(year,month)[1])
    return datetime.date(year, month, day)

my_list = {}
def get_data(start_date = None, no_of_periods = PERIODS):
	global my_list
	global HAS_NEW_DATA
	x = datetime.strptime(start_date, "%m/%d/%y") if start_date else datetime.datetime.now() - timedelta(days=1)
	y = x
	for n in range(no_of_periods):
		my_date = y.strftime("%Y%m%d")
		if(cache.get(my_date)==None):
			print ('updating cache...', my_date)
			HAS_NEW_DATA = 1
			contents = urllib.request.urlopen(URL+my_date)
			bytes_str = contents.read()
			data_str = bytes_str.decode("utf-8")
			cache[my_date] = json.loads(data_str[data_str.find('"listingHistorical":{"data":')+28:data_str.find(',"page":1,"sort":""')])
		else:
			print ('found in cache...', my_date)
		foobar = [my_coin['symbol'] for my_coin in cache.get(my_date) if my_coin['symbol'] in set(TICKERS)]
		if(len(foobar)!=len(set(TICKERS))):
				print()
				raise ValueError('Tickers not found.', set(TICKERS).difference(set(foobar)))
		my_list[my_date]=cache.get(my_date)
		y = add_months(x, 3*n)
	if(HAS_NEW_DATA):
		with open('foo.json', 'w') as outfile:
			json.dump(cache, outfile)
		HAS_NEW_DATA = 0
	
get_data()
coinlists = my_list.items()
foo = list(zip([coinlist[0] for coinlist in coinlists], list(map(lambda x: (list(map(lambda y: dict({"id": y['id'],"last_updated": y['last_updated'], "symbol": y['symbol'], "USD": y['quote']['USD']['price']}), x))), [[my_coin for my_coin in coinlist[1] if my_coin['symbol'] in set(TICKERS)] for coinlist in coinlists]))))
foo.reverse()
bar = [[[a[0], a[1], *a[2]] for a in b] for b in [[[*p, *[[fred['USD'], p[0]/fred['USD']] for fred in [next(period_1_usd_value for period_1_usd_value in [f[1] for f in foo][0] if period_1_usd_value['symbol']==p[1])]]] for p in P] for P in PERMUTATIONS]]
garply = [f[1] for f in foo]
plugh = [f[0] for f in foo]
quux = []
for b in bar:
	# print(b)
	quuz = []
	# quuz.append(b)
	for g in garply:
		quuz.append([[G['USD']*next(h for h in b if h[1]==G['symbol'])[3],G['symbol'],G['USD'],next(h for h in b if h[1]==G['symbol'])[3], G['id'], G['last_updated']] for G in g])
	quux.append(quuz)
		# print(g)
# print(json.dumps([list(zip(plugh, q)) for q in quux]))
with open('bar.json', 'w') as outfile:
			json.dump([list(zip(plugh, q)) for q in quux], outfile)

print('Your data is ready.')