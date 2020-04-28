import pandas_datareader as pdr 

import matplotlib.pyplot as plt 

plt.style.use('seaborn-darkgrid')

import pandas as pd 
import numpy as np 


# using yahoo finance api to get stock prices
# ^GSPC is for the S&P500 in yahoo finance 
# first case of corona was reported on 17th of November in 2019 
data_sp = pdr.get_data_yahoo('^GSPC', '17-Nov-19')

data_sp.head()
data_sp.shape

data_pc = data_sp.Close.pct_change()

# Plot
data_pc.plot(figsize=(10, 7), grid=True)
plt.axvline('30-Jan-20')
plt.show()












# Read the timelines from the CSV file
timelines = pd.read_csv('pandemics_timelines.csv').dropna()
for col in timelines.columns[1:]:
    timelines[col] = pd.to_datetime(timelines[col])
    
tl = covid_timelines
data = pd.DataFrame()
data[inst] = pdr.get_data_yahoo('^GSPC', 
    tl.first_case.iloc[0]-pdr.timedelta(days=30), 
    tl.last_date.iloc[0]+pdr.timedelta(days=365))['Adj Close']    

# Read the data from yahoo fianance
def get_data(tl):    
    inst_list = ['^GSPC', 'CL=F','GC=F', 'TLT']
    data = pd.DataFrame()
    for inst in inst_list:
        try:
            data[inst] = pdr.get_data_yahoo(inst, tl.first_case.iloc[0]-pdr.timedelta(days=30), 
                                        tl.last_date.iloc[0]+pdr.timedelta(days=365))['Adj Close']    
        except Exception as e:
            print('No data available for ',inst, e)

    return data
    
# Get data during covid19 pandemic
covid_timelines = timelines.loc[timelines.pandemic_name=='covid19']
data= get_data(covid_timelines)

data.head()

# Plot daily percentage change
def plot_daily_pc(data, tl):
    data_pc = data.pct_change().dropna()
    fig = plt.figure(figsize=(12, 8))
    i = 0
    for col in data_pc.columns:
        # Add the subplot
        sub = fig.add_subplot(2, 2, i+1)
        i = i+1
        # Set title
        sub.set_title(col, fontsize=20)
        # Plot
        r = random.random()
        b = random.random()
        g = random.random()
        data_pc[col].plot(color=(r, g, b))
        sub.set_ylabel('Returns')
        sub.grid(which="major", color='k', linestyle='-.', linewidth=0.2)
        sub.axvline(x=tl.first_case.iloc[0], color='RoyalBlue',
                    linestyle='dashdot', linewidth=3)
        sub.axvline(x=tl.who_emergency.iloc[0], color='Red',
                    linestyle='dashdot', linewidth=3)

    plt.tight_layout()
    plt.show()
    
plot_daily_pc(data, covid_timelines)