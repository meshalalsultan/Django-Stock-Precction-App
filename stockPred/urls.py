from django.urls import path 
from . import views

urlpatterns = [
    path('', views.home, name="home"),
    path('stock_index/', views.stock_index , name='stock_index'),
    path('result/', views.result , name='result'),
    path('sentemint_index' , views.sentemint_index , name='sentemint_index'),
    path('sentemint/', views.sentemint , name='sentemint'),
    path('tweet_sentemint/', views.tweet_sentemint , name='tweet_sentemint'),
    path('tweet_sent_index/',views.tweet_sent_index , name ='tweet_sent_index'),
    path('bitcoin_index/',views.bitcoin_index , name='bitcoin_index'),
    path('bitcoin_pred/',views.bitcoin_pred, name = 'bitcoin_pred'),
    path('social_recomandation' , views.social_recomandation , name = 'social_recomandation'),
    path('social_reco' ,views.social_reco , name='social_reco'),
    path('prices/', views.prices, name="prices"),
    path('twet_sent/' , views.twet_sent , name='twet_sent'),
]
