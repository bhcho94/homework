

import pandas as pd
import numpy as np
import os
import matplotlib.pyplot as plt
import statsmodels as sm
from statsmodels.tsa.stattools import adfuller
from statsmodels.regression.linear_model import OLS
path = os.getcwd()

prices = pd.read_csv(path + '/close.csv')
data = pd.DataFrame()
prices['Date'] = pd.to_datetime(prices['Date'])
prices.set_index('Date',inplace = True)
tickers = list(data.columns.values)
data = prices/prices.iloc[0]
trading_data = data.loc[data.index > '2017-09-08']
data = data.loc[data.index < '2017-09-09']
prices = prices.loc[prices.index > '2017-09-09']

def trading_signals(first, second, trading_data = trading_data, formation_data = data):
    signal = 2*np.std(formation_data[first] - formation_data[second])
    result_dict = {}
    trading = False
    differences = trading_data[first] - trading_data[second]
    for i in range(len(differences)):
        if trading == False:
            if abs(differences.iloc[i]) > signal and abs(differences.iloc[i] < 2*signal):
                trading = True
                start_date = differences.index.values[i]
        else:
            if (differences.iloc[i-1] * differences.iloc[i] < 0) or (i == len(differences)-1) or abs(differences.iloc[i] > 2*signal):
                trading = False
                end_date = differences.index.values[i]
                if differences[i-1] > 0:
                    s_ret = (trading_data[first][start_date] - trading_data[first][end_date])/trading_data[first][start_date]
                    l_ret = (trading_data[second][end_date] - trading_data[second][start_date])/trading_data[second][start_date]
                    result_dict[start_date] = [first, second, start_date, end_date, s_ret,l_ret]
                else:
                    s_ret = (trading_data[second][start_date] - trading_data[second][end_date])/trading_data[second][start_date]
                    l_ret = (trading_data[first][end_date] - trading_data[first][start_date])/trading_data[first][start_date]
                    result_dict[start_date] = [second, first, start_date, end_date, s_ret,l_ret]
    df = pd.DataFrame.from_dict(result_dict, orient = 'index', columns = ['Short','Long','Start','End', 'SReturn','LReturn'])
    df.index = list(range(len(df)))
    df['Total'] = df['SReturn'] + df['LReturn']
    df['Length'] = (df['End'] - df['Start']).dt.days

    return df


def build_portfolio(trade_list, trading_data = trading_data):
    index_list = trading_data.index.tolist()
    portfolio = pd.DataFrame(index = trading_data.index.values, columns = ['Short','Long','ShortR','LongR','ShortTD','LongTD'])
    for i in range(len(trade_list)):
        start = trade_list['Start'][i]
        end = trade_list['End'][i]
        short = trade_list['Short'][i]
        lon = trade_list['Long'][i]
        di = index_list.index(start)
        di2 = index_list.index(end)
        for j in range(di2 - di + 1):
            date_index = di + j
            dt = index_list[date_index]
            portfolio['Short'][dt] = trading_data[short][dt]/trading_data[short][index_list[di]]
            portfolio['Long'][dt] = trading_data[lon][dt]/trading_data[lon][index_list[di]]
            portfolio['Short'][dt] = trading_data[short][dt]/trading_data[short][index_list[di]]
            portfolio['Long'][dt] = trading_data[lon][dt]/trading_data[lon][index_list[di]]

    portfolio.fillna(value = 0, axis = 0)
    for j in range(1, len(portfolio)):
        if portfolio.iloc[j-1]['Short'] > 0:
            portfolio.iloc[j]['ShortR'] = -(portfolio.iloc[j]['Short'] - portfolio.iloc[j-1]['Short'])/portfolio.iloc[j-1]['Long']
            portfolio.iloc[j]['LongR'] = (portfolio.iloc[j]['Long'] - portfolio.iloc[j-1]['Long'])/portfolio.iloc[j-1]['Long']
        else:
            portfolio.iloc[j]['ShortR'] = 0
            portfolio.iloc[j]['LongR']= 0
    portfolio['Total'] = portfolio['ShortR'] + portfolio['LongR']
    portfolio.fillna(0, inplace = True)
    return portfolio


df1 = (build_portfolio(trading_signals('HON','NEE')))
df2 = (build_portfolio(trading_signals('TXN','SYK')))
df3 = (build_portfolio(trading_signals('BDX','SYK')))
df4 = (build_portfolio(trading_signals('HON','DHR')))
df5 = (build_portfolio(trading_signals('JPM','PNC')))
df = (df1 + df2 + df3 + df4 + df5)[['Short','Long']]
df['Short Return'] = -df.pct_change()['Short']
df['Long Return'] = df.pct_change()['Long']
print(df)