from django.shortcuts import render
from datetime import datetime
import investpy
from . import profile
from . import keras

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