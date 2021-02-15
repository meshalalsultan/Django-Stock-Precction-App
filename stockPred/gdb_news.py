from fredapi import Fred

fred = Fred(api_key='db6f8fecf821dd7d93c03618e0ccd6f9')

data = fred.get_series_first_release('GDP')

print(data)

#Get latest data

last_gdb_data = fred.get_series_latest_release('GDP')#
print(last_gdb_data)

#search for data series

fred = fred.search('potential gdp')
fred.to_csv('fred.csv')
print(fred)