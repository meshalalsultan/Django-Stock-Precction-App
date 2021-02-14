import pandas as pd 
import numpy as np 
import investpy
import datetime
from datetime import datetime
import tensorflow as tf
from tensorflow.keras.models import Sequential
from tensorflow.keras .layers import Dense , LSTM ,Conv2D, Flatten

import re
import time
import math
from sklearn.preprocessing import MinMaxScaler

from tensorflow.keras.models import load_model

model = load_model('./model.h5' , compile=False)

def predict(stock,start_Date,end_Date):
    df= investpy.get_crypto_historical_data(crypto='bitcoin', from_date=start_Date, to_date=end_Date)

    df.drop('Currency',axis=1,inplace=True)
    data = df.filter(['Close'])
    dataset = data.values
    scaler = MinMaxScaler(feature_range =(0,1))
    scaled_data = scaler.fit_transform(dataset)
    df= investpy.get_crypto_historical_data(crypto='bitcoin', from_date=start_Date, to_date=end_Date)
    df.drop('Currency' ,axis=1,inplace=True)
    pred_data = df.filter(['Close'])
    last_60_days = pred_data[-60:].values
    last_60_days_scaled = scaler.fit_transform(last_60_days)
    X_test = []
    X_test.append(last_60_days_scaled)
    X_test = np.array(X_test)
    X_test = np.reshape(X_test , (X_test.shape[0] , X_test.shape[1] , 1))
    pred_price = model.predict(X_test)
    pred_price = scaler.inverse_transform(pred_price)
    pred = []
    pred.append(pred_price)

    return pred[0]