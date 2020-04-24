import csv 
import numpy as np 
import pandas as pd 
from sklearn import linear_model 
import matplotlib.pyplot as plt 
import datetime as dt

google = pd.read_csv('GOOG.csv')

# convert dates 
google['Date'] = pd.to_datetime(google['Date'])
google['Date'] = google['Date'].map(dt.datetime.toordinal)
google.Date.head()





# storing the prices and dates in a variable 
price = np.asarray(google.Open)
date = np.asarray(google.Date)

# reshaping as numpy array 
price = price.reshape(price.shape[0],1)
date = date.reshape(date.shape[0],1)


# checking the size....should be the same 
price.shape
date.shape


# lm stands for linear model 
lm = linear_model.LinearRegression()


# traing model / get parameters 
lm.fit(date,price)

# prediction 

def predict_price(date):
    date = pd.to_datetime(date)
    date = dt.datetime.toordinal(date)
    date = np.asarray(date)
    date = date.reshape(1,-1)
    prediction = lm.predict(date)
    return prediction


prediction_date = '4/24/20'
predict_price(date)
