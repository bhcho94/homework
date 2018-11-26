import pandas as pd
import numpy as np
import os
from statsmodels.tsa.stattools import adfuller

path = os.getcwd()


data = pd.read_csv(path + '/close.csv')
data['Date'] = pd.to_datetime(data['Date'])
data.set_index('Date', inplace = True)
tickers = list(data.columns.values)
data = data/data.iloc[0]
result_dict = {}
trading_data = data.loc[data.index > '2017-09-08']
data = data.loc[data.index < '2017-09-09']

for i in range(len(tickers)):
        for j in range(i, len(tickers)):
                if i != j:
                        first = tickers[i]
                        second =tickers[j]
                        ssd = sum((data[first] - data[second])**2)
                        sd = np.std(data[first] - data[second])
                        pearson = (sum(data[first]*data[second]) - len(data[first])*np.mean(data[first])*np.mean(data[second]))/((len(data[first] - 1))*np.std(data[first])*np.std(data[second]))
                        adftest = adfuller(data[first] - data[second])
                        result_dict[first + '-' + second] = [first, second, ssd, sd, pearson]

result_df = pd.DataFrame.from_dict(result_dict, orient = 'index', columns = ['first','second','SSD','SD','Pearson'])

potential_pairs = result_df.sort_values('SSD').head(500)
#potential_pairs.to_csv(path + '/potential.csv')

exit()