from django.shortcuts import render
from datetime import datetime
import investpy
import requests
import json
from . import profile
from . import keras
from . import Sammary
from . import bit_pred
from . import social_reco

from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer
import nltk
from nltk.corpus import stopwords
from . import tweetSentemint
import datetime as dt


nltk.download('stopwords')
stop_words = stopwords.words('english')

set(stopwords.words('english'))

# Create your views here.
def home(request):
    import requests
    import json
	
    # Grab Crypto Price Data
    price_request = requests.get("https://min-api.cryptocompare.com/data/pricemultifull?fsyms=BTC,ETH,XRP,BCH,EOS,LTC,XLM,ADA,USDT,MIOTA,TRX&tsyms=USD")
    price = json.loads(price_request.content)

    api_request = requests.get("https://min-api.cryptocompare.com/data/v2/news/?lang=EN")
    req = json.loads(api_request.content)
    t = req['Data'][0]['body']
    return render(request, 'home.html', {'req': req, 'price': price , 't':t})


def prices(request):
	if request.method == 'POST':
		import requests
		import json
		quote = request.POST['quote']
		quote = quote.upper()
		crypto_request = requests.get("https://min-api.cryptocompare.com/data/pricemultifull?fsyms=" + quote + "&tsyms=USD")
		crypto = json.loads(crypto_request.content)
		return render(request, 'prices.html', {'quote':quote, 'crypto': crypto})
		
		
	else:
		notfound = "Enter a crypto currency symbol into the form above..."
		return render(request, 'prices.html', {'notfound': notfound})




def stock_index(request):
    return render(request, 'index.html')

def result(request ):

    stock = request.GET["stockName"].upper()
    country = request.GET['country'].upper()
    start = request.GET['startDate']
    end = request.GET['endDate']
    start_date = datetime.strptime(start, "%Y-%m-%d").strftime("%d/%m/%Y")
    end_date = datetime.strptime(end, "%Y-%m-%d").strftime("%d/%m/%Y")



    co_profile = profile.get_profile(stock , country)

    pred = keras.predict(stock,country,start_date,end_date)

    signal = keras.get_signal(stock , country)
    json_records = signal.reset_index().to_json(orient ='records') 
    signal = [] 
    signal = json.loads(json_records)

    news = keras.get_news(country)
    last_event = news['event']
    last_news = news['importance']
    time = news['time']

    last_close , last_open = keras.last_close(stock,country,start_date,end_date)



    return render(request, 'result.html',{'stock' : stock ,
    'country' : country , 'startDate' : start_date ,
    'endDate' : end_date , 'co_profile': co_profile ,
    'pred':pred, 'signal' : signal , 'last_event':last_event,'last_news':last_news,'time':time,
    'last_close' : last_close , 'last_open' :last_open 
        
        })

def sentemint_index(request):
    return render(request , 'sentemint_index.html')

def sentemint(request):
    stop_words = stopwords.words('english')
    text1 = request.GET['text1'].lower()

    processed_doc1 = ' '.join([word for word in text1.split() if word not in stop_words])
    sa = SentimentIntensityAnalyzer()
    dd = sa.polarity_scores(text=processed_doc1)
    compound = round((1 + dd['compound'])/2, 2)
    summary_result = Sammary.sumy_summarizer(text1) 

    return render(request, 'sentemint.html' , {'final':compound , 'text1':text1 , 'summary_result':summary_result})
def tweet_sent_index(request):
    return render(request , 'tweet_sent_index.html')


def tweet_sentemint(request):
    #stock= request.GET["t_stock"].upper()
    query = '$'+stock
    tweets = tweetSentemint.get_tweets(query = query, count = 200)
    ptweets = [tweet for tweet in tweets if tweet['sentiment'] == 'positive']
    #st.text("Positive tweets percentage: {} %".format(100*len(ptweets)/len(tweets))) 
    Positive_tweets = 100*len(ptweets)/len(tweets)
    ntweets = [tweet for tweet in tweets if tweet['sentiment'] == 'negative']
    neg_tweet = 100*len(ntweets)/len(tweets)
    nat_tweet = 100*(len(tweets) -(len( ntweets )+len( ptweets)))/len(tweets)
    # printing first 5 positive tweets 
    #st.text("\n\nPositive tweets:")
    t = [] 
    for tweet in ptweets[:10]: 
        #tweet_p1 = tweet
        t.append(tweet)

    tweet_t1 = t[0]['text']
    tweet_t2 = t[1]['text']
    tweet_t3 = t[2]['text']
    tweet_t4 = t[3]['text']
    tweet_t5 = t[4]['text']
    tweet_s1 = t[0]['sentiment']
    tweet_s2 = t[1]['sentiment']
    tweet_s3 = t[2]['sentiment']
    tweet_s4 = t[3]['sentiment']
    tweet_s5 = t[4]['sentiment']



    return render(request,'tweet_sentemint.html' , {'stock' : stock, 'tweets':tweets , 'Positive_tweets':Positive_tweets ,
    'neg_tweet' : neg_tweet , 'nat_tweet' : nat_tweet ,
    'tweet_t1':tweet_t1,'tweet_t2':tweet_t2,'tweet_t3':tweet_t3,'tweet_t4':tweet_t4,'tweet_t5':tweet_t5,
    'tweet_s1':tweet_s1,'tweet_s2':tweet_s2 , 'tweet_s3':tweet_s3,'tweet_s4':tweet_s4,'tweet_s5':tweet_s5})


def twet_sent(request):
    stock= request.GET["t_stock"].upper()
    tiker = '$'+stock

    positive , negative , neutral = tweetSentemint.get_tweet(tiker)

    return render(request,'test_sentemint.html', {'positive' : positive,'negative' : negative,'neutral': neutral})

def bitcoin_index(request):
    return render(request , 'bitcoin_index.html')


def bitcoin_pred(request):
    crypto = request.GET["cryptoName"].upper()
    start = request.GET['start_Date']
    end = request.GET['end_Date']

    start_Date = datetime.strptime(start, "%Y-%m-%d").strftime("%d/%m/%Y")
    end_Date = datetime.strptime(end, "%Y-%m-%d").strftime("%d/%m/%Y")

    pred = bit_pred.predict(crypto,start_Date,end_Date)


    return render(request , 'bitcoin_pred.html' , {'crypto' : crypto , 'pred' : pred})


def social_recomandation(request):
    return render(request , 'social_recomandation.html')

def social_reco(request):
    symbol = request.GET['symbol']
    actual_date = dt.date.today()
    past_date = actual_date - dt.timedelta(days=365 * 3)

    actual_date = actual_date.strftime("%Y-%m-%d")
    past_date = past_date.strftime("%d/%m/%Y")

    #start_Date = datetime.strptime(start, "%Y-%m-%d").strftime("%d/%m/%Y")
    #end_Date = datetime.strptime(end, "%Y-%m-%d").strftime("%d/%m/%Y")

    dataframe = social_reco.get_stock_data(symbol, past_date, actual_date)

    (dataframe, forecast_out) = social_reco.stock_forecasting(dataframe)
    print ("Retrieving %s related tweets polarity..." % symbol)
    polarity = social_reco.retrieving_tweets_polarity(symbol)
    print ("Generating recommendation based on prediction & polarity..." ,)
    recommending=recommending(dataframe, forecast_out, polarity)

    return render (request , 'social_repo.html' , {'symbol':symbol , 'polarity' : polarity , 'recommending' : recommending } )

