cache = {}

from itertools import permutations
# list1 = [61.8, 23.484, 14.516]
list1 = [61.8, 23.48, 14.52]
list2 = ['ADA', 'BTC', 'ETH']
all_combinations = [list(zip(each_permutation, list2)) for each_permutation in permutations(list1, len(list2))]
from datetime import timedelta
import urllib.request
url = "https://coinmarketcap.com/historical/"
import json
from datetime import timedelta
import datetime
import calendar
from decimal import *
getcontext().prec = 18

periods = []
def add_months(sourcedate, months):
    month = sourcedate.month - 1 - months
    year = sourcedate.year + month // 12
    month = (month % 12 - 1) or 12
    day = min(sourcedate.day, calendar.monthrange(year,month)[1])
    return datetime.date(year, month, day)

def get_data(start_date = None, no_of_periods = 5):
	my_list = []
	x = datetime.strptime(start_date, "%m/%d/%y") if start_date else datetime.datetime.now() - timedelta(days=1)
	y = x
	#x = datetime.strptime(start_date, "%m/%d/%y") if start_date else datetime.now()
	for n in range(no_of_periods):
		#y = x - timedelta(month=(3*n))
		periods.append(y.strftime("%Y%m%d"))
		contents = urllib.request.urlopen(url+y.strftime("%Y%m%d"))
		y = add_months(x,3*n)
		# add_months(x,1)
		bytes_str = contents.read()
		data_str = bytes_str.decode("utf-8")
		start_str = '"listingHistorical":{"data":'
		start = data_str.find(start_str)+len(start_str)
		end = data_str.find(',"page":1,"sort":""')
		cropped_str = data_str[start:end]
		# file1 = open("MyFile.txt","a")
		# file1.write(cropped_str)
		# file1.close()
		data_list = json.loads(cropped_str)
		# cache[y.strftime("%Y%m%d")] = data_list
		# print(data_list) 

		my_data = (list(map(lambda x:dict({"symbol":x['symbol'],"last_updated":x['last_updated'], "USD":x['quote']['USD']['price']}), [coin for coin in data_list if coin['symbol'] in set(list2)])))
		my_list.append(my_data)
	return my_list
print("Getting pricing data...")
# print(get_data())
starting_amt = 100
starting_amts = list(map(lambda x:x*(starting_amt/100), list1))
# historical_data = get_data().reverse()
# = [[{'symbol': 'BTC', 'USD': 51206.69295307718}, {'symbol': 'ETH', 'USD': 1723.1537960718588}, {'symbol': 'ADA', 'USD': 1.13336663749198}], [{'symbol': 'BTC', 'USD': 48561.16615390074}, {'symbol': 'ETH', 'USD': 1541.9142855099035}, {'symbol': 'ADA', 'USD': 1.11486800364865}], [{'symbol': 'BTC', 'USD': 49631.24137077495}, {'symbol': 'ETH', 'USD': 1564.7076468627545}, {'symbol': 'ADA', 'USD': 1.2923878693104}], [{'symbol': 'BTC', 'USD': 7909.72939346}, {'symbol': 'ETH', 'USD': 200.767247427}, {'symbol': 'ADA', 'USD': 0.0414952067859}], [{'symbol': 'BTC', 'USD': 8909.9536515}, {'symbol': 'ETH', 'USD': 237.853095033}, {'symbol': 'ADA', 'USD': 0.0489445066712}]]

historical_data = get_data()
historical_data.reverse()
periods.reverse()
for m in range(len(list2)):
	foo = next(x for x in historical_data[0] if x['symbol']==list2[m])
	foo['purchased'] = starting_amts[m]/foo['USD']

for n in historical_data[1:]:
	for m in range(len(list2)):
		foo = next(x for x in n if x['symbol']==list2[m])
		bar = next(x for x in historical_data[0] if x['symbol']==list2[m])
		foo['value_as_USD'] = foo['USD'] * bar['purchased']
# print({"weights": list1, "tickers":list2, "historical_data":historical_data})




total = 0
for n in historical_data[-1]:
	# print (n)
	total += n['value_as_USD']
	# for m in range(len(list2)):
		# foo = next(x for x in n if x['symbol']==list2[m])
		# total += foo['value_in_USD']

# print({"total": total, "weights": list1, "tickers":list2, "historical_data":historical_data})
# print (all_combinations)

def calc_return(permutation):
	calculated_returns = []
	for m in range(len(permutation)):
		bar = [*permutation[m]]
		foo = next(x for x in historical_data[0] if x['symbol']==bar[1])
		bar.append(starting_amts[m]/foo['USD'])
		bar.append(foo['USD'])
		calculated_returns.append(bar)
		# foo['purchased'] = starting_amts[m]/foo['USD']
	return [calculated_returns]

all_returns = []
for p in all_combinations:
	all_returns.append(calc_return(p))


for z in all_returns:
	for n in historical_data[1:]:
		bar = []
		for m in range(len(z[0])):
			foo = next(x for x in n if x['symbol']==z[0][m][1])
			bar.append([foo['USD'] * z[0][m][2],z[0][m][1],z[0][m][2],foo['USD']])
		z.append(bar)



print(all_returns)
print(periods)