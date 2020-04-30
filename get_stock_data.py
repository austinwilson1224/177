import datetime as dt  
import matplotlib.pyplot as plt 
from matplotlib import style
from mpl_finance import candlestick_ochl
import matplotlib.dates as mdates
import pandas as pd 
import pandas_datareader as pdr 
import pandas_datareader.data as web
import bs4 as bs 
import pickle
import requests 
import os 


# this function will get all the tickers from wikipedia 

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



# this will get the data from yahoo api and store each one in folder stock_dfs
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

# this function will put all of these into one file you can save it to csv
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
df = compile_data()

df.to_csv('sp500.csv')
