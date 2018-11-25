

import pandas as pd
import numpy as np
import os
import matplotlib.pyplot as plt
import statsmodels as sm
from statsmodels.tsa.stattools import adfuller

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
    return (df, len(df))


def build_portfolio(trade_list, trading_data = trading_data):
    index_list = trading_data.index.tolist()
    portfolio = pd.DataFrame(index = trading_data.index.values, columns = ['Short','Long','ShortR','LongR','Trading'])
    l = trade_list[1]
    trade_list = trade_list[0]
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
            portfolio['Trading'][dt] = 1

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
    return (portfolio, l)

def analyze_portfolio(pairs):
    i = 0
    df = (build_portfolio(trading_signals(pairs[i][0], pairs[i][1]))[0])
    trade_count = build_portfolio(trading_signals(pairs[i][0], pairs[i][1]))[1]
    for i in range(1, len(pairs)):
        df = df + (build_portfolio(trading_signals(pairs[i][0], pairs[i][1])))[0]
        trade_count += build_portfolio(trading_signals(pairs[i][0], pairs[i][1]))[1]
    df_short = df['ShortR']/df['Trading']
    df_long = df['LongR']/df['Trading']
    df_final = pd.concat([df_short, df_long], axis=1)
    df_final.columns = ['Short Return','Long Return']
    df_final.index.name = 'Date'
    df_final['Total'] = df_final['Short Return'] + df_final['Long Return']
    df_final.fillna(0, inplace = True)
    arithemtic_daily_mean = np.mean(df_final['Total'])
    annualized_return = (1+arithemtic_daily_mean)**250 - 1
    annualized_std = np.std(df_final['Total'])*np.sqrt(250)
    sharpe_ratio = annualized_return/annualized_std
    return [annualized_return, annualized_std, sharpe_ratio, trade_count]

print(analyze_portfolio([['HON','NEE'], ['TXN','SYK'],['BDX','SYK'], ['HON','DHR'],['JPM','PNC']]))


