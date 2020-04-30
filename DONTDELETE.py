import datetime as dt  
import matplotlib.pyplot as plt 
from matplotlib import style
from mpl_finance import candlestick_ochl
import matplotlib.dates as mdates
import pandas as pd 
import pandas_datareader as pdr 
import pandas_datareader.data as web
import numpy as np
from collections import Counter
import os
import bs4 as bs 
import pickle
import requests 
from sklearn import svm, neighbors
from sklearn.model_selection import cross_validate
from sklearn.model_selection import train_test_split
from sklearn.ensemble import VotingClassifier, RandomForestClassifier
style.use('ggplot')


# these are the companies we are interested in, so we will hard code the tickers in this array 
tickers = ['AAPL','AXP','NKE','CVX','JNJ','F','ALK']


# variables we will need
# datetime(year, month, day) 
sars = 'sars'
start_sars = dt.datetime(2002,10,1)
end_sars = dt.datetime(2004,1,1)

swine = 'swine'
start_swine = dt.datetime(2009,4,15)
end_swine = dt.datetime(2010,8,11)

ebola = 'ebola'
start_ebola = dt.datetime(2013,12,1)
end_ebola = dt.datetime(2016,1,14)

corona = 'corona'
start_corona = dt.datetime(2019,11,17)
end_corona = dt.datetime(2020,4,24)

# lina jan 22 2121


pandemics = [sars,swine,ebola,corona]
######### get the data for each time period of the corresponding pandemic 
def get_data_from_yahoo_pandemic(pandemic,start,end):
    # with open('sp500tickers.pickle','rb') as f:
    #         tickers = pickle.load(f)
    if not os.path.exists('stock_dfs_{}'.format(pandemic)):
        os.makedirs('stock_dfs_{}'.format(pandemic))

    # tickers = ['AAPL','AXP','NKE','CVX','JNJ','F','ALK']
    # start = dt.datetime(2002,10,1)
    # end = dt.datetime(2003,9,1)


    # to test use tickers[:10] so you don't have to wiat for all 500
    for ticker in tickers:
        print(ticker)
        if not os.path.exists('stock_dfs_{}/{}.csv'.format(pandemic,ticker)):
            try:
                df = web.DataReader(ticker,'yahoo',start,end)
                df.to_csv('stock_dfs_{}/{}.csv'.format(pandemic,ticker))
            except KeyError:
                pass
        else:
            print('Already have {}'.format(ticker))

# sars
get_data_from_yahoo_pandemic(sars,start_sars,end_sars)

# swine
get_data_from_yahoo_pandemic(swine,start_swine,end_swine)

# ebola
get_data_from_yahoo_pandemic(ebola,start_ebola,end_ebola)

# corona
get_data_from_yahoo_pandemic(corona,start_corona,end_corona)


########### combine each dataset into one csv
def compile_data_pandemic(pandemic):
    # with open("sp500tickers.pickle","rb") as f:
    #     tickers = pickle.load(f)

    main_df = pd.DataFrame()
    # tickers = ['AAPL','AXP','NKE','CVX','JNJ','F','ALK']
    for count,ticker in enumerate(tickers):
        try:
            df = pd.read_csv('stock_dfs_{}/{}.csv'.format(pandemic,ticker))
            df.set_index('Date',inplace=True)

            df.rename(columns = { 'Adj Close': ticker}, inplace=True)
            df.drop(['Open','High','Low','Close','Volume'],1,inplace=True)
            if main_df.empty:
                main_df = df
            else:
                main_df = main_df.join(df, how = 'outer')
            
            if count % 10 == 0:
                # print(count)
                pass
        except FileNotFoundError as e:
            print('no file')
            continue
    main_df.to_csv('stock_dfs_{}/{}.csv'.format(pandemic,pandemic))
    # return main_df

# sars 
compile_data_pandemic(sars)
# swine
compile_data_pandemic(swine)
# ebola
compile_data_pandemic(ebola)
# corona
compile_data_pandemic(corona)



############# process data for labels ... 

def process_data_for_labels(pandemic,ticker):
    # how many days 
    days = 7 
    df = pd.read_csv('stock_dfs_{}/{}.csv'.format(pandemic,pandemic), index_col=0)
    # df = pd.read_csv('sars_data.csv', index_col=0)

    tickers = df.columns.values.tolist()
    df.fillna(0,inplace=True)

    for i in range(1, days+1):
        df['{}_{}d'.format(ticker,i)] = (df[ticker].shift(-i) - df[ticker]) / df[ticker]
    df.fillna(0,inplace=True)
    return tickers,df


############# ml target function 
def buy_sell_hold(*args):
    cols = [c for c in args]
    requirement = .02
    for col in cols:
        if col > requirement:
            return 1
        if col < -requirement:
            return -1

    return 0



############ to x,y 

def extract_feature_sets(pandemic,ticker):
    tickers, df = process_data_for_labels(pandemic,ticker)
    hm_days=7

    df['{}_target'.format(ticker)] = list(map( buy_sell_hold, df['{}_1d'.format(ticker)],
        df['{}_2d'.format(ticker)],
        df['{}_3d'.format(ticker)],
        df['{}_4d'.format(ticker)],
        df['{}_5d'.format(ticker)],
        df['{}_6d'.format(ticker)],
        df['{}_7d'.format(ticker)]
        ))
    #list(map(buy_sell_hold, *[df['{}_{}d'.format(ticker, i)]for i in range(1, hm_days+1)]))

    vals = df['{}_target'.format(ticker)].values.tolist()
    str_vals = [str(i) for i in vals]
    print('Data spread: ',Counter(str_vals))
    df.fillna(0,inplace=True)

    df = df.replace([np.inf, -np.inf], np.nan)
    df.dropna(inplace=True)

    df_vals = df[[ticker for ticker in tickers ]].pct_change()
    df_vals = df_vals.replace([np.inf, -np.inf],0)
    df_vals.fillna(0, inplace=True)

    X=df_vals.values
    y=df['{}_target'.format(ticker)].values

    return X,y

########### actual ml 
def do_ml(pandemic,ticker):
    X,y=extract_feature_sets(pandemic,ticker)

    X_train, X_test, y_train, y_test = train_test_split(X,y,test_size=.25,random_state=42)


    # K nearest neighbors
    clf = neighbors.KNeighborsClassifier()
    # voting classifies
    clf = VotingClassifier([
        ('lsvc', svm.LinearSVC()),
        ('knn', neighbors.KNeighborsClassifier()),
        ('rfor', RandomForestClassifier())
    ])



    clf.fit(X_train,y_train) 
    confidence = clf.score(X_test,y_test)
    print('Accuracy:',confidence)
    predictions = clf.predict(X_test)
    print('Predicted spread:',Counter(predictions))

    return confidence

for ticker in tickers:
    print(ticker)
    for pandemic in pandemics:
        print(pandemic)
        do_ml(pandemic,ticker)
        print('\n')
    print('\n\n')



# do_ml(sars,'JNJ')