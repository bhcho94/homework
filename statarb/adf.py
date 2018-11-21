import pandas as pd
import numpy as np
import os
import matplotlib.pyplot as plt
import statsmodels as sm
from statsmodels.tsa.stattools import adfuller
from statsmodels.regression.linear_model import OLS
path = os.getcwd()

data = pd.read_csv(path + '/close.csv')
data['Date'] = pd.to_datetime(data['Date'])
data.set_index('Date', inplace = True)
tickers = list(data.columns.values)
data = data/data.iloc[0]
result_dict = {}
trading_data = data.loc[data.index > '2017-09-08']
data = data.loc[data.index < '2017-09-09']
potential_pairs = pd.read_csv(path + '/potential.csv', index_col = 0)
adf = {}

def half_life(ts):
    ts = np.asarray(ts)
    delta_ts = np.diff(ts)
    lag_ts = np.vstack([ts[1:], np.ones(len(ts[1:]))]).T
    beta = np.linalg.lstsq(lag_ts, delta_ts, rcond = -1)
    return (np.log(2) / beta[0])[0]

for j in range(len(potential_pairs)):
        first = potential_pairs.iloc[j]['first']
        second = potential_pairs.iloc[j]['second']
        pearson = potential_pairs.iloc[j]['Pearson']
        t = adfuller(data[first] - data[second])
        hl = half_life(data[first] - data[second])
        nt = adfuller(trading_data[first] - trading_data[second])
        nhl = half_life(trading_data[first] - trading_data[second])
        adf[potential_pairs.index.values[j]] = [t[0], t[1], hl, pearson, nt[0], nt[1], nhl]

adf_result = pd.DataFrame.from_dict(adf, orient = 'index', 
columns = ['Test Statistic', 'p-value', 'half-life', 'pearson', 'n1', 'n2','n3'])

adf_result = adf_result[adf_result['p-value'] < 0.02]

print(adf_result.sort_values('p-value').sort_values('half-life'))