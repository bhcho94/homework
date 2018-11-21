import numpy as np 
import pandas as pd
import math
import matplotlib.pyplot as plt
import os

#loading data from csv format
path = os.getcwd()
data = pd.read_csv(path + '/GBOND20010731.csv')

#separating only yield rates and maturities
yields = list(data['YTM'].values)
#converting maturity to years
maturities = list((data['TAU']/365).values)

#Nelson-Siegel discount function
def NS(B0, B1, B2, tau, m):
    return B0 + (B1+B2)*(1-math.exp(-m/tau))*(tau/m) - B2*math.exp(-m/tau)


#create two function X1 and X2 that are partof the 2nd and 3rd term of the NS equation, respectively
#we use these to create X inputs for a linear regression
def X1(tau, m):
    return (1-math.exp(-m/tau))*(tau/m)

def X2(tau, m):
    return math.exp(-m/tau)

#next, we test for different values of tau to find the value that minimizes the squared sum of the residuals
tau = 0
curmin = 999
for i in range(1,100):
    x1 = []
    x2 = []
    for j in range(len(yields)):
        x1.append(X1(i, maturities[j]))
        x2.append(X2(i, maturities[j]))
    df = pd.DataFrame({"A": yields, "B":x1, "C":x2})
    result = sm.ols(formula = 'A ~ B + C', data=df).fit()
    r = sum(result.resid**2)
    if r < curmin:
        curmin = r
        tau = i

#from here we see that tau = 5 gives us the smallest residual sum of squares
#we test further to find a more accurate and precise tau value around 5

for i in np.linspace(4, 6, 100):
    x1 = []
    x2 = []
    for j in range(len(yields)):
        x1.append(X1(i, maturities[j]))
        x2.append(X2(i, maturities[j]))
    df = pd.DataFrame({"A": yields, "B":x1, "C":x2})
    result = sm.ols(formula = 'A ~ B + C', data=df).fit()
    r = sum(result.resid**2)
    if r < curmin:
        curmin = r
        tau = i

#from this we see that tau = 4.593 gives us the most optimized residual sum of squares
#using this value of tau we can now estimate our parameters for B0, B1, and B2


x1 = []
x2 = []
for j in range(len(yields)):
    x1.append(X1(tau, maturities[j]))
    x2.append(X2(tau, maturities[j]))
df = pd.DataFrame({"A": yields, "B":x1, "C":x2})
result = sm.ols(formula = 'A ~ B + C', data=df).fit()
B0, B1, B2 = result.params[0], result.params[1] - result.params[2], result.params[2]

#NS_forward is the function to calculate the forward rate using the above parameters
def NS_forward(B0, B1, B2, tau, m):
    return B0 + B1*math.exp(-m/tau) + B2*(m/tau)*math.exp(-m/tau)

#now construct a dataframe of the calculated spot and forward rates from maturity 0 to 10 years
NS_forward_yields = []
NS_yield = []
forward = 0
ytm = 0
result_dict = {}
plot_maturities = np.linspace(0.1, 10, 100)
for m in plot_maturities:
    forward = (NS_forward(B0, B1, B2, tau, m))
    ytm = (NS(B0,B1,B2, tau, m))
    result_dict[m] = [forward, ytm]

#plot the results
df = pd.DataFrame.from_dict(result_dict, orient = 'index')
df.columns = ['Forward Rate','Spot Rate']
forward_rates = plt.plot(df['Forward Rate'])
spot_rates = plt.plot(df['Spot Rate'])
actual_yields = plt.scatter(maturities, yields, color = 'g')
plt.title('NS Yield Curve')
plt.xlabel('Maturities')
plt.ylabel('Yield (%)')
plt.grid()
plt.legend()
plt.axis(xmin = 0, ymin = 0, xmax = 10, ymax = 10)
plt.legend()
plt.show()