import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import os

path = (os.getcwd())

data = pd.read_csv(path + '/close.csv')
data['Date'] = pd.to_datetime(data['Date'])
data.set_index('Date', inplace = True)
tickers = list(data.columns.values)
data = data/data.iloc[0]
result_dict = {}
trading_data = data.loc[data.index > '2017-09-08']
data = data.loc[data.index < '2017-09-09']

def charts(first, second, data = data, trading_data = trading_data):
    hist_diff = data[first] - data[second]
    sd = np.std(hist_diff)
    title = first + '-' + second
    plt.plot(data[first])
    plt.plot(data[second])
    plt.title('%s Historical Prices' % title)
    plt.xlabel('Date')
    plt.ylabel('Normalized Prices')
    plt.legend()
    plt.savefig(path + '/%s Historical Prices' % title)
    plt.clf()

    plt.plot(hist_diff)
    plt.axhline(0, color = 'b', linewidth = 0.5)
    plt.axhline(2*sd, color = 'g', linewidth = 0.5)
    plt.axhline(-2*sd, color = 'g',linewidth = 0.5)
    plt.axhline(3*sd, color = 'r',linewidth = 0.5)
    plt.axhline(-3*sd, color = 'r',linewidth = 0.5)
    plt.title('%s Historical Differences' % title)
    plt.xlabel('Date')
    plt.ylabel('Difference')
    plt.savefig(path + '/%s Historical Differences' % title)
    plt.clf()

    plt.plot(trading_data[first])
    plt.plot(trading_data[second])
    plt.title('%s Past Year Prices' % title)
    plt.xlabel('Date')
    plt.ylabel('Normalized Prices')
    plt.legend()
    plt.savefig(path + '/%s Past Year Prices' % title)
    plt.clf() 

    plt.plot(trading_data[first] - trading_data[second])
    plt.axhline(0, color = 'b', linewidth = 0.5)
    plt.axhline(2*sd, color = 'g', linewidth = 0.5)
    plt.axhline(-2*sd, color = 'g',linewidth = 0.5)
    plt.axhline(3*sd, color = 'r',linewidth = 0.5)
    plt.axhline(-3*sd, color = 'r',linewidth = 0.5)
    plt.title('%s Historical Differences' % title)
    plt.xlabel('Date')
    plt.ylabel('Difference')
    plt.savefig(path + '/%s Past Year Differences' % title)

    #plt.axhline(2*sd, color = 'r')
    #plt.axhline(-2*sd, color = 'r')


charts('HON','NEE')