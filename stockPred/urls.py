from django.urls import path 
from . import views

urlpatterns = [
    path('', views.home , name='home'),
    path('result/', views.result , name='result'),
    path('sentemint_index' , views.sentemint_index , name='sentemint_index'),
    path('sentemint/', views.sentemint , name='sentemint'),
]
