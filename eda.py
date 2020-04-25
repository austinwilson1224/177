import csv 
import numpy as np 
import pandas as pd 
from sklearn import linear_model 
import sklearn
import matplotlib.pyplot as plt 
import datetime as dt

google = pd.read_csv('GOOG.csv')
apple = pd.read_csv('AAPL.csv')

apple.head(20)

# convert dates 
google['Date'] = pd.to_datetime(google['Date'])
apple.Date = pd.to_datetime(apple.Date)

google['Date'] = google['Date'].map(dt.datetime.toordinal)
apple.Date = apple.Date.map(dt.datetime.toordinal)
# google.Date.head()





# storing the prices and dates in a variable 
price_google = np.asarray(google.Close)
date_google = np.asarray(google.Date)

price_apple = np.asarray(apple.Close)
date_apple = np.asarray(apple.Date)


price_apple.shape
date_apple.shape



# reshaping as numpy array 
price_google = price_google.reshape(price_google.shape[0],1)
date_google = date_google.reshape(date_google.shape[0],1)

price_apple = price_apple.reshape(price_apple.shape[0],1)
date_apple = date_apple.reshape(date_apple.shape[0],1)


# checking the size....should be the same 
price_apple.shape
date_apple.shape


# lm stands for linear model 
# y = mx + b 
lm = linear_model.LinearRegression()


lm.fit(date_apple,price_apple)

lm.coef_
# traing model / get parameters 
# passing in (x,y) 
# lm.fit(date,price)

# prediction 

def predict_price(date):
    date = pd.to_datetime(date)
    date = dt.datetime.toordinal(date)
    date = np.asarray(date)
    date = date.reshape(1,-1)
    prediction = lm.predict(date)
    return prediction


prediction_date = '4/24/20'
pred = predict_price(prediction_date)
pred
pred = pred[0][0]
print("google stock price on {} will be {}".format(prediction_date,pred))
