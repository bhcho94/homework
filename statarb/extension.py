import pandas as pd
import numpy as np
import os

path = os.getcwd()

data = pd.read_csv(path + '/close.csv')
data['Date'] = pd.to_datetime(data['Date'])
data.set_index('Date', inplace = True)
tickers = list(data.columns.values)
data = data/data.iloc[0]
result_dict = {}
trading_data = data.loc[data.index > '2017-09-08']
data = data.loc[data.index < '2017-09-09']
potential_pairs = pd.read_csv(path + '/potential.csv', index_col=0)

result_dict = {}

for j in range(10):
        first = potential_pairs.iloc[j]['first']
        second = potential_pairs.iloc[j]['second']
        sd = np.std(data[first] - data[second])
        count1 = 0
        count = 0
        for i in range(1, len(data)):
                d = data.iloc[i][first] - data.iloc[i][second]
                d1 = data.iloc[i-1][first] - data.iloc[i-1][second]
                e = abs(d) - 2*sd
                e1 = abs(d1) - 2*sd
                if d*d1 < 0:
                    count += 1
                if e*e1 < 0:
                    count1+=1
        result_dict[potential_pairs.index.values[j]] = [count, count1]

print(result_dict)
result_df = pd.DataFrame.from_dict(result_dict, orient = 'index', columns = ['crosses','signals'])

print(result_df)