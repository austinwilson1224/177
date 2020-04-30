'''

This is our first basic linear model 
the stocks we are interested in are listed in tickers list



'''


import csv 
import numpy as np 
import pandas as pd 
from sklearn import linear_model 
import sklearn
import matplotlib.pyplot as plt 
import datetime as dt

tickers = ['AAPL','AXP','NKE','CVX','JNJ','F','ALK']
drop_columns = ['High','Low','Open','Close','Volume']
# some others are crude oil, gold and treasury bonds 
# crude oil ticker = 'CL=F'
# gold ticker = 'GC=F'
# treasury bond = 'TFT'

%cd '/Users/austinwilson/Desktop/CSUS/177/final project/final solution'
%ls
aapl = pd.read_csv('stock_dfs/AAPL.csv')
axp = pd.read_csv('stock_dfs/AXP.csv')
nke = pd.read_csv('stock_dfs/NKE.csv')
cvx = pd.read_csv('stock_dfs/CVX.csv')
jnj = pd.read_csv('stock_dfs/JNJ.csv')
f = pd.read_csv('stock_dfs/F.csv')
alk = pd.read_csv('stock_dfs/ALK.csv')


# google = pd.read_csv('GOOG.csv')
# apple = pd.read_csv('AAPL.csv')

# apple.head(20)

# convert dates and drop the columns we dont care about 
def convert_dates(df):
    df['Date'] = pd.to_datetime(df['Date'])
    df['Date'] = df['Date'].map(dt.datetime.toordinal)
    df.drop(columns=['High','Low','Open','Close','Volume'],inplace=True)



# aapl['Date'] = pd.to_datetime(aapl['Date'])
# axp['Date'] = pd.to_datetime(axp['Date'])
# nke['Date'] = pd.to_datetime(nke['Date'])
# google['Date'] = pd.to_datetime(google['Date'])
# google['Date'] = pd.to_datetime(google['Date'])
# google['Date'] = pd.to_datetime(google['Date'])

convert_dates(aapl)
convert_dates(axp)
convert_dates(nke)
convert_dates(cvx)
convert_dates(jnj)
convert_dates(f)
convert_dates(alk)

nke.head()

# apple.Date = pd.to_datetime(apple.Date)

# google['Date'] = google['Date'].map(dt.datetime.toordinal)
# apple.Date = apple.Date.map(dt.datetime.toordinal)
# google.Date.head()


aapl.tail()


# storing the prices and dates in a variable 
def to_xy(df):
    x = np.asarray(df['Date'])
    y = np.asarray(df['Adj Close'])

    # reshaping
    x = x.reshape(x.shape[0],1)
    y = y.reshape(y.shape[0],1) 
    print(x.shape)
    print(y.shape)
    return x,y

aapl_x,aapl_y = to_xy(aapl)
axp_x,axp_y = to_xy(axp)
nke_x,nke_y = to_xy(nke)
cvx_x,cvx_y = to_xy(cvx)
jnj_x,jnj_y = to_xy(jnj)
f_x,f_y = to_xy(f)
alk_x,alk_y = to_xy(alk)


f_x.shape




# price_google = np.asarray(google.Close)
# date_google = np.asarray(google.Date)

# price_apple = np.asarray(apple.Close)
# date_apple = np.asarray(apple.Date)


# price_apple.shape
# date_apple.shape



# reshaping as numpy array 


# price_google = price_google.reshape(price_google.shape[0],1)
# date_google = date_google.reshape(date_google.shape[0],1)

# price_apple = price_apple.reshape(price_apple.shape[0],1)
# date_apple = date_apple.reshape(date_apple.shape[0],1)


# checking the size....should be the same 



# lm stands for linear model 
# y = mx + b 
lm = linear_model.LinearRegression()


lm.fit(aapl_x,aapl_y)

lm.

lm.coef_
# traing model / get parameters 
# passing in (x,y) 
# lm.fit(date,price)

# prediction 

def predict_price(date,x,y):
    date = pd.to_datetime(date)
    date = dt.datetime.toordinal(date)
    date = np.asarray(date)
    date = date.reshape(1,-1)
    lm = linear_model.LinearRegression()
    lm.fit(x,y)
    print(lm.coef_)
    prediction = lm.predict(date)
    return prediction


prediction_date = '4/29/20'
pred = predict_price(prediction_date,f_x,f_y)
pred
pred = pred[0][0]
pred
print("google stock price on {} will be {}".format(prediction_date,pred))
