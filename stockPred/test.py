import investpy
import json
import json.tool

stock = 'tsla'
country = 'United states'
'''
report = investpy.get_stock_financial_summary(stock=stock, country=country, summary_type='income_statement', period='quarterly')
print (report)
#print (type(report))

balance_sheet = investpy.get_stock_financial_summary(stock=stock, country=country, summary_type='balance_sheet', period='quarterly')
print(balance_sheet)
i = balance_sheet.index[0]
print(i)
print(balance_sheet['Total Liabilities'][0])
print(balance_sheet['Total Liabilities'][1])

cash_flow_statement = investpy.get_stock_financial_summary(stock=stock, country=country, summary_type='cash_flow_statement', period='quarterly')
print(cash_flow_statement.columns)

def get_report(stock , country):
    report = investpy.get_stock_financial_summary(stock=stock, country=country, summary_type='income_statement', period='annual')
    cash_flow_statement = investpy.get_stock_financial_summary(stock=stock, country=country, summary_type='cash_flow_statement', period='quarterly')
    balance_sheet = investpy.get_stock_financial_summary(stock=stock, country=country, summary_type='balance_sheet', period='quarterly')

    return report , cash_flow_statement , balance_sheet


countr = [country]
important = ['high','medium' , 'low']
news = investpy.news.economic_calendar(time_filter='time_remaining',importances=important , countries=countr)

print (news['importance'][0])
if news['importance'][0] == 'high':
    print('high')
elif news['importance'][0] == 'medium':
        print('medium')
else :
    print('low ')

import pandas as pd 
import numpy as np 
import investpy



from_date='01/01/2010'
to_date='01/01/2019'
pre = keras.predict(stock , country , from_date , to_date)
print(pre)
'''
from_date='01/01/2010'
to_date='01/01/2019'

def last(stock,country,from_date,to_date):
    df = investpy.get_stock_historical_data(stock=stock, country=country, from_date=from_date, to_date=to_date)
    last = df['Close'].tail(1)[0]
    last_open = df['Open'].tail(1)[0]
    return last , last_open

last_close , last_open =last(stock,country,from_date,to_date)
print (last_close)
print (last_open)

