from django.shortcuts import render
from datetime import datetime
import investpy
from . import profile
from . import keras
from . import Sammary
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer
import nltk
from nltk.corpus import stopwords

nltk.download('stopwords')
stop_words = stopwords.words('english')

set(stopwords.words('english'))

# Create your views here.
def home(request):
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
    return render(request, 'result.html',{'stock' : stock , 'country' : country , 'startDate' : start_date , 'endDate' : end_date , 'co_profile': co_profile , 'pred':pred})

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

    '''
    if raw_text  = request.GET['url1'] > 0:

        docx = Sammary.analyze_text(raw_text)
        ht = Sammary.displacy.render(docx,style="ent")
        ht = ht.replace("\n\n","\n")
    else:
        pass
    '''

    

    return render(request, 'sentemint.html' , {'final':compound , 'text1':text1 , 'summary_result':summary_result})
