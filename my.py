from itertools import permutations
list1 = [61.8, 23.484, 14.516]
list2 = ['ADA', 'BTC', 'ETH']
all_combinations = [list(zip(each_permutation, list2)) for each_permutation in permutations(list1, len(list2))]
# https://stackoverflow.com/questions/65780978/accessing-all-historical-crypto-data-with-specified-time-interval-using-financia
import urllib.request
# use urllib to get HTML data
url = "https://coinmarketcap.com/historical/20201206/"
contents = urllib.request.urlopen(url)
bytes_str = contents.read()

# decode bytes string
data_str = bytes_str.decode("utf-8")

# crop the raw JSON string out of the website HTML
start_str = '"listingHistorical":{"data":'
start = data_str.find(start_str)+len(start_str)
end = data_str.find(',"page":1,"sort":""')
cropped_str = data_str[start:end]

# create a Python list from JSON string
data_list = json.loads(cropped_str)
print ("total cryptos:", len(data_list))
print (list(map(lambda x:dict({"symbol":x['symbol'], "USD":x['quote']['USD']['price']}), [coin for coin in data_list if coin['symbol'] in {"ETH","BTC","ADA"}])))

from datetime import datetime, timedelta

x = datetime(2020, 5, 17)

print(x + timedelta(days=10))
print(x.strftime("%Y%d%m"))

for n in range(5):
	y = x+timedelta(days=n)
	print(y.strftime("%Y%d%m"))

#https://www.geeksforgeeks.org/how-to-add-days-to-a-date-in-python/

from datetime import datetime
from datetime import timedelta
  
# taking input as the date
Begindatestring = "2020-10-11"
  
# carry out conversion between string 
# to datetime object
Begindate = datetime.strptime(Begindatestring, "%Y-%m-%d")
  
# print begin date
print("Beginning date")
print(Begindate)
  
# calculating end date by adding 10 days
Enddate = Begindate + timedelta(days=10)
  
# printing end date
print("Ending date")
print(Enddate)


from itertools import permutations
list1 = [61.8, 23.484, 14.516]
list2 = ['ADA', 'BTC', 'ETH']
all_combinations = [list(zip(each_permutation, list2)) for each_permutation in permutations(list1, len(list2))]
from datetime import timedelta
import urllib.request
url = "https://coinmarketcap.com/historical"
from datetime import datetime, timedelta
def get_data(start_date = null, no_of_periods = 4):
	x = datetime.strptime(start_date, "%m/%d/%y") if start_date else datetime.now()
	for n in range(no_of_periods):
		y = x - timedelta(months=(3*n))
		contents = urllib.request.urlopen(url+y.strftime("%Y%d%m"))
		bytes_str = contents.read()
		data_str = bytes_str.decode("utf-8")
		start_str = '"listingHistorical":{"data":'
		start = data_str.find(start_str)+len(start_str)
		end = data_str.find(',"page":1,"sort":""')
		cropped_str = data_str[start:end]
		data_list = json.loads(cropped_str)
		print (list(map(lambda x:dict({"symbol":x['symbol'], "USD":x['quote']['USD']['price']}), [coin for coin in data_list if coin['symbol'] in set(list2)])))
get_data()

