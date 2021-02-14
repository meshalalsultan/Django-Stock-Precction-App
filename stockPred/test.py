import investpy
import json
import json.tool
import re
import pandas as pd 
from textblob import TextBlob 

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
'''


import requests
import json
'''
def getAnalysis(score):
            if score < 0:
                return 'Negative'
            elif score == 0:
                return 'Neutral'
            else:
                return 'Positive'
'''	
    # Grab Crypto Price Data
price_request = requests.get("https://min-api.cryptocompare.com/data/pricemultifull?fsyms=BTC,ETH,XRP,BCH,EOS,LTC,XLM,ADA,USDT,MIOTA,TRX&tsyms=USD")
price = json.loads(price_request.content)

api_request = requests.get("https://min-api.cryptocompare.com/data/v2/news/?lang=EN")
res = json.loads(api_request.content)

print (type(res['Data']))
'''
for d in res['Data']:
    txt =  (d['body'])
    txt =  ' '.join(re.sub("(@[A-Za-z0-9]+)|([^0-9A-Za-z \t]) |(\w+:\/\/\S+)", " ", txt).split())
    #twitter = pd.DataFrame([tweet.full_text for tweet in post], columns=['Tweets'])
    df = pd.DataFrame([d['body'] for d in res['Data']], columns=['Text'])
    df['Subjectivity'] = TextBlob(txt).sentiment.subjectivity
    df['Polarity'] = TextBlob(txt).sentiment.polarity
    df['Analysis'] = df['Polarity'].apply(getAnalysis)
'''
for d in res['Data']:
    txt =  (d['body'])
    txt =  ' '.join(re.sub("(@[A-Za-z0-9]+)|([^0-9A-Za-z \t]) |(\w+:\/\/\S+)", " ", txt).split())
    txt_p = TextBlob(txt).sentiment.polarity

    if txt_p < 0:
        return 'neg'
    elif txt_p == 0:
        return 'Neutral'
    else:
        return 'Positive'



    print (df)
    #print (positive_per)

    