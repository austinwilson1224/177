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
style.use('ggplot')

# start = dt.datetime(2000,1,1)
# end = dt.datetime(2020,4,25)


# df = web.DataReader('TSLA', 'yahoo', start, end)
# df.head()
# df.shape
# df.tail(10)

# df.to_csv('TSLA.csv')


tesla = pd.read_csv('TSLA.csv',parse_dates=True,index_col = 0)
tesla.head()
tesla.plot()

df['Adj Close'].plot()
plt.show()

# stands for 100 moving average
# takes todays prices and the previous 99 days and averages them,
# does this for consecutive days
df['100ma'] = df['Adj Close'].rolling(window=100, min_periods = 0).mean()
df.dropna(inplace=True)
df.tail()

df.head()


ax1 = plt.subplot2grid((6,1),(0,0),rowspan=5, colspan=1)
ax2 = plt.subplot2grid((6,1), (5,0), rowspan=1,colspan=1,sharex=ax1)

ax1.plot(df.index,df['Adj Close'])
ax1.plot(df.index,df['100ma'])
ax2.bar(df.index,df['Volume'])



# not a moving averave
# olhc stands for open low high close
# this will shrink the data set significantly because its the average for every 10 days
df_ohlc = df['Adj Close'].resample('10D').ohlc()
df_volume = df['Volume'].resample('10D').sum()


df.shape
df_olhc.shape

df_ohlc.head()

df_ohlc.reset_index(inplace=True)

df_ohlc.head()

df_ohlc['Date'] = df_ohlc['Date'].map(mdates.date2num)

ax1 = plt.subplot2grid((6,1),(0,0),rowspan=5, colspan=1)
ax2 = plt.subplot2grid((6,1), (5,0), rowspan=1,colspan=1,sharex=ax1)
ax1.xaxis_date()

candlestick_ochl(ax1,df_ohlc.values,width=2,colorup='g')
ax2.fill_between(df_volume.index.map(mdates.date2num), df_volume.values, 0)
plt.show()




########### automating getting the S&P 500 companies ################  5 

import bs4 as bs 
import pickle
import requests 

def save_sp500_tickers(): 
    response = requests.get('https://en.wikipedia.org/wiki/List_of_S%26P_500_companies')
    soup = bs.BeautifulSoup(response.text)
    table = soup.find('table',{'class':'wikitable sortable'})
    tickers = [] 
    for row in table.findAll('tr')[1:]:
        ticker = row.findAll('td')[0].text.replace('\n','')
        tickers.append(ticker)
    with open('sp500tickers.pickle','wb') as f:
        pickle.dump(tickers,f)
    # print(tickers)
    return tickers

save_sp500_tickers()


########### using list of sp500 tickers to get all data from those companies ### 6 
import os 


def get_data_from_yahoo(reload_sp500=False):
    if reload_sp500:
        tickers = save_sp500_tickers()
    else:
        with open('sp500tickers.pickle','rb') as f:
            tickers = pickle.load(f)
    if not os.path.exists('stock_dfs'):
        os.makedirs('stock_dfs')

    start = dt.datetime(2000,1,1)
    end = dt.datetime(2020,4,25)


    # to test use tickers[:10] so you don't have to wiat for all 500
    for ticker in tickers:
        print(ticker)
        if not os.path.exists('stock_dfs/{}.csv'.format(ticker)):
            try:
                df = web.DataReader(ticker,'yahoo',start,end)
                df.to_csv('stock_dfs/{}.csv'.format(ticker))
            except KeyError:
                pass
        else:
            print('Already have {}'.format(ticker))
get_data_from_yahoo()


def get_data_from_yahoo_sars():
    # with open('sp500tickers.pickle','rb') as f:
    #         tickers = pickle.load(f)
    if not os.path.exists('stock_dfs_sars'):
        os.makedirs('stock_dfs_sars')

    tickers = ['AAPL','AXP','NKE','CVX','JNJ','F','ALK']
    start = dt.datetime(2002,10,1)
    end = dt.datetime(2003,9,1)


    # to test use tickers[:10] so you don't have to wiat for all 500
    for ticker in tickers:
        print(ticker)
        if not os.path.exists('stock_dfs_sars/{}.csv'.format(ticker)):
            try:
                df = web.DataReader(ticker,'yahoo',start,end)
                df.to_csv('stock_dfs_sars/{}.csv'.format(ticker))
            except KeyError:
                pass
        else:
            print('Already have {}'.format(ticker))

get_data_from_yahoo_sars()



############# combine all those data frames into one for sp500 #############  7

def compile_data():
    with open("sp500tickers.pickle","rb") as f:
        tickers = pickle.load(f)

    main_df = pd.DataFrame()

    for count,ticker in enumerate(tickers):
        try:
            df = pd.read_csv('stock_dfs/{}.csv'.format(ticker))
            df.set_index('Date',inplace=True)

            df.rename(columns = { 'Adj Close': ticker}, inplace=True)
            df.drop(['Open','High','Low','Close','Volume'],1,inplace=True)
            if main_df.empty:
                main_df = df
            else:
                main_df = main_df.join(df, how = 'outer')
            
            if count % 10 == 0:
                print(count)
        except FileNotFoundError as e:
            print('no file')
            continue
    return main_df

def compile_data_sars():
    # with open("sp500tickers.pickle","rb") as f:
    #     tickers = pickle.load(f)

    main_df = pd.DataFrame()
    tickers = ['AAPL','AXP','NKE','CVX','JNJ','F','ALK']
    for count,ticker in enumerate(tickers):
        try:
            df = pd.read_csv('stock_dfs_sars/{}.csv'.format(ticker))
            df.set_index('Date',inplace=True)

            df.rename(columns = { 'Adj Close': ticker}, inplace=True)
            df.drop(['Open','High','Low','Close','Volume'],1,inplace=True)
            if main_df.empty:
                main_df = df
            else:
                main_df = main_df.join(df, how = 'outer')
            
            if count % 10 == 0:
                print(count)
        except FileNotFoundError as e:
            print('no file')
            continue
    return main_df
    
df_sars = compile_data_sars()

df_sars.shape
df_sars.head()


# df.head()
df_sars.to_csv('sars_data.csv')



############### correlation table ########  8 

def visualize_data():
    df = pd.read_csv('sp500_joined_closes.csv',parse_dates=True)
    # df['AAPL'].plot()
    # plt.show()
    df_corr = df.corr()

    # print(df_corr.head())

    data = df_corr.values
    fig = plt.figure()
    ax = fig.add_subplot(1,1,1)

    heatmap = ax.pcolor(data, cmap = plt.cm.RdYlGn)
    fig.colorbar(heatmap)
    ax.set_xticks(np.arange(data.shape[0]) + .5, minor=False)
    ax.set_yticks(np.arange(data.shape[1]) + .5, minor=False)
    ax.invert_yaxis()
    ax.xaxis.tick_top()

    column_labels = df_corr.columns
    row_labels = df_corr.index

    ax.set_xticklabels(column_labels)
    ax.set_yticklabels(row_labels)
    plt.xticks(rotation=90)
    heatmap.set_clim(-1,1)
    plt.tight_layout()
    plt.show()


visualize_data()



################## preprocessing data for machine learning ########## 9 

def process_data_for_labels(ticker):
    # how many days 
    hm_days = 7 
    df = pd.read_csv('sp500_joined_closes.csv', index_col=0)
    # df = pd.read_csv('sars_data.csv', index_col=0)

    tickers = df.columns.values.tolist()
    df.fillna(0,inplace=True)

    for i in range(1, hm_days+1):
        df['{}_{}d'.format(ticker,i)] = (df[ticker].shift(-i) - df[ticker]) / df[ticker]
    df.fillna(0,inplace=True)
    return tickers,df

# a,b=process_data_for_labels('XOM')

# a
# b





################## machine learning target function ##### 10
# 1 is for buy
# -1 is for sell
# 0 is hold
def buy_sell_hold(*args):
    cols = [c for c in args]
    requirement = .02
    for col in cols:
        if col > requirement:
            return 1
        if col < -requirement:
            return -1

    return 0


############### creating labels for machine learning ###### 11 

def extract_feature_sets(ticker):
    tickers, df = process_data_for_labels(ticker)
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

    return X,y,df

# x,y,df = extract_feature_sets('AMZN')
# x.shape
# y.shape
# df


############ machine learning ###### 12

from sklearn import svm, neighbors
from sklearn.model_selection import cross_validate
from sklearn.model_selection import train_test_split
from sklearn.ensemble import VotingClassifier, RandomForestClassifier

def do_ml(ticker):
    X,y,df=extract_feature_sets(ticker)

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

# sars 
do_ml('AAPL')
do_ml('ALK')
do_ml('AXP')
do_ml('CVX')
do_ml('F')
do_ml('JNJ')
do_ml('NKE')






do_ml('AMZN')
do_ml('GOOG')
do_ml('JNJ')
do_ml('KR')
do_ml('AXP')
do_ml('NIKE')
do_ml('INTC')
do_ml('AMD')
do_ml('ALK')
do_ml('AMAT')
do_ml('ADSK')
do_ml('BBY')
do_ml('CAH')
do_ml('GM')
do_ml('KHC')
do_ml('LVS')
do_ml('NDAQ')
do_ml('NFLX')
do_ml('PFE')











