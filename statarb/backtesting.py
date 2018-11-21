import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

#importing data
tickers = pd.read_csv('C:/Users/USER-PC/Documents/School/tickers.csv')
data = pd.read_csv('C:/Users/USER-PC/Documents/School/close.csv')
data['Date'] = pd.to_datetime(data['Date'])
data.set_index('Date', inplace = True)
data = data/data.iloc[0]
trading_data = data.loc[data.index > '2017-11-08']
data = data.loc[data.index < '2017-11-09']

def backtest(first, second):
    differences = trading_data[first] - trading_data[second]
    historical_differences = data[first] - data[second]
    sd = np.std(historical_differences)
    c = 0
    dates = []
    for i in range(len(differences)):
        if abs(differences.iloc[i]) > 2*sd:
            c += 1
            dates.append(differences.index.values[i])
    plt.plot(differences)
    plt.title(first + '-' + second)
    plt.xlabel('Date')
    plt.ylabel('Differneces')
    plt.axhline(2*sd, color = 'r')
    plt.axhline(-2*sd, color = 'r')
    plt.savefig('C:/Users/USER-PC/Documents/School/' + first + '-' + second)
    #plt.plot([differences.index.values[0], 2*sd], [differences.index.values[len(differences)-1], 2*sd], linestyle='-')
    #plt.plot([differences.index.values[0], -2*sd], [differences.index.values[len(differences)-1], -2*sd], linestyle='-')
    return c, dates

print(backtest('DWDP', 'ECL'))