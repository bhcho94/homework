#this script is nearly identical to the Nelson-Siegel.py script except it uses the Svensson method
import numpy as np 
import pandas as pd
import math
import statsmodels.formula.api as sm
import matplotlib.pyplot as plt
import os

#loading data from csv format
path = os.getcwd()
data = pd.read_csv(path + '/GBOND20010731.csv')

#separating only yield rates and maturities
yields = list(data['YTM'].values)
#converting maturity to years
maturities = list((data['TAU']/365).values)

#Nelson-Siegel-Svensson discount function
def NSSvensson(B0, B1, B2, B3, tau1, tau2, m):
    return B0 + B1*(1-math.exp(-m/tau1)) + B2*((1-math.exp(-m/tau1))/(m/tau1) - math.exp(-m/tau1)) + B3*((1-math.exp(-m/tau2))/(m/tau2) - math.exp(-m/tau2))

#create two function X1 and X2 that are partof the 2nd and 3rd term of the NS equation, respectively
#we use these to create X inputs for a linear regression
def X1(tau1, m):
    return (1-math.exp(-m/tau1))

def X2(tau1, m):
    return ((1-math.exp(-m/tau1)/(m/tau1)) - math.exp(-m/tau1))

def X3(tau2, m):
    return ((1-math.exp(-m/tau2)/(m/tau2)) - math.exp(-m/tau2))

#next, we test for different values of tau1 and tau2 to find the value that minimizes the squared sum of the residuals

tau1, tau2 = 0, 0
curmin= 999
for i in range(10):
    x1 = []
    x2 = []
    x3 = []
    t1 = np.random.randint(0, 10)
    t2 = np.random.randint(0, 10)
    if t1 == 0:
        t1 = 0.1
    if t2 == 0:
        t2 = 0.1
    for j in range(len(yields)):
        x1.append(X1(t1, maturities[j]))
        x2.append(X2(t1, maturities[j]))
        x3.append(X3(t2, maturities[j]))
    df = pd.DataFrame({"A": yields, "B":x1, "C":x2, "D": x3})
    result = sm.ols(formula = 'A ~ B + C + D', data=df).fit()
    r = sum(result.resid**2)
    if r < curmin:
        curmin = r
        tau1, tau2 = t1, t2

print(tau1, tau2, curmin)
tau1, tau2 = 0.7043, 2.662906
#from this we see that tau = 4.593 gives us the most optimized residual sum of squares
#using this value of tau we can now estimate our parameters for B0, B1, and B2


x1 = []
x2 = []
x3 = []
for j in range(len(yields)):
    x1.append(X1(tau1, maturities[j]))
    x2.append(X2(tau1, maturities[j]))
    x3.append(X3(tau2, maturities[j]))
df = pd.DataFrame({"A": yields, "B":x1, "C":x2, "D":x3})
result = sm.ols(formula = 'A ~ B + C + D', data=df).fit()
B0, B1, B2, B3 = result.params[0], result.params[1], result.params[2], result.params[3]

print(B0, B1, B2, B3, tau1, tau2)

#NS_forward is the function to calculate the forward rate using the above parameters
def NSS_forward(B0, B1, B2, B3, tau1, tau2, m):
    return B0 + B1*((1-math.exp(-m/tau1))/m/tau1) + B2*((1-math.exp(-m/tau1))/(m/tau1) - math.exp(-m/tau1)) + B3*((1-math.exp(-m/tau2))/(m/tau1) - math.exp(-m/tau1))

#now construct a dataframe of the calculated spot and forward rates from maturity 0 to 10 years
forward = 0
ytm = 0
result_dict = {}
plot_maturities = np.linspace(0.1, 10, 100)
for m in plot_maturities:
    forward = (NSS_forward(B0, B1, B2, B3, tau1, tau2, m))
    ytm = (NSSvensson(B0,B1,B2,B3, tau1, tau2, m))
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