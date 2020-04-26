import datetime as dt  
import matplotlib.pyplot as plt 
from matplotlib import style
from mpl_finance import candlestick_ochl
import matplotlib.dates as mdates
import pandas as pd 
import pandas_datareader.data as web

style.use('ggplot')

start = dt.datetime(2000,1,1)
end = dt.datetime(2020,4,25)


df = web.DataReader('TSLA', 'yahoo', start, end)
df.head()
df.shape
df.tail(10)

df.to_csv('TSLA.csv')


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





############# combine all those data frames into one for sp500 #############  7

def compile_data():
    with open("sp500tickers.pickle","rb") as f:
        tickers = pickle.load(f)

    main_df = pd.DataFrame()

    for count,ticker in enumerate(tickers):
        df = pd.read_csv('stock_dfs/{}.csv'.format(ticker))
        df.set_index('Date',inplace=True)

        df.rename(columns = { 'Adj Close': ticker}, inplace=True)
        df.drop(['Open','High','Low','Close','Volume'],index=1,inplace=True)
        if main_df.empty:
            main_df = df
        else:
            main_df = main_df.join(df, how = 'outer')
        
        if count % 10 == 0:
            print(count)



main_df.head()
main_df.to_csv('sp500_joined_closes.csv')



############### correlation table ########

def visualize_data():
    df = pd.read_csv('sp500_joined_closes.csv')
    df['AAPL'].plot()
    plt.show()

visualize_data()






