import warnings
import itertools #to use iterators
import numpy as np
import matplotlib
import matplotlib.pyplot as plt
warnings.filterwarnings('ignore')
plt.style.use('fivethirtyeight')
import pandas as pd
#pip install statsmodels
import statsmodels.api as sm
from pylab import rcParams

matplotlib.rcParams['axes.labelsize'] = 14
matplotlib.rcParams['xtick.labelsize'] = 12
matplotlib.rcParams['ytick.labelsize'] = 12
matplotlib.rcParams['text.color'] = 'k'

#pip install xlrd
df = pd.read_excel("Superstore.xls")
df.head()

#forecast furniture sales
furniture = df.loc[df['Category'] == 'Furniture']
furniture['Order Date'].min() #Timestamp('2014-01-06 00:00:00')
furniture['Order Date'].max() #Timestamp('2017-12-30 00:00:00')

#===1. Data Preprocessing
#remove columns we don't need
cols = ['Row ID', 'Order ID', 'Ship Date', 'Ship Mode', 'Customer ID', \
    'Customer Name', 'Segment', 'Country', 'City', 'State', 'Postal Code', \
        'Region', 'Product ID', 'Category', 'Sub-Category', 'Product Name', \
            'Quantity', 'Discount', 'Profit']
furniture.drop(cols, axis=1, inplace=True)
furniture = furniture.sort_values('Order Date')

furniture.isnull().sum()

furniture = furniture.groupby('Order Date')['Sales'].sum().reset_index()

#===2. Index with time series
furniture= furniture.set_index('Order Date')
# furniture.index

#use avg daily sales for the month and start of each month as timestamp
y = furniture['Sales'].resample('MS').mean() 

#quck peak of year 2017
y['2017':]

#===3. Visualize time series
y.plot(figsize=(15, 6))
plt.show()


rcParams['figure.figsize'] = 18, 8

decomposition = sm.tsa.seasonal_decompose(y, model='multiplicative')
fig = decomposition.plot()
plt.show()

#===4. ARIMA model
#(1) Define the p,d,q parameters to take any value between 0 and 2
p = d = q = range(0,2) #seasonality, trend, noise
#(2) Generate all different combinations of p, d, q triplets
pdq = list(itertools.product(p, d, q))
#(3) Set seasonal frequency (eg. 12 for monthly data)
seasonal_pdq = [(x[0], x[1], x[2], 12) for x in list(itertools.product(p, d, q))]

#(4) Initialize a df to store the results
# results_df = pd.DataFrame(columns=['param', 'param_seasonal', 'AIC'])
results_list = [] # initialize a list instead as df doesn't work with append()

#(5) grid search: parameter selection to find the best yield performance of the model
for param in pdq:
    for param_seasonal in seasonal_pdq:
        try:
            mod = sm.tsa.statespace.SARIMAX(y, 
                                            order=param,
                                            seasonal_order=param_seasonal,
                                            enforce_stationarity=False,
                                            enforce_invertibility=False)
            results = mod.fit()
            results_list.append({'param': param,
                                 'param_seasonal': param_seasonal,
                                'AIC': results.aic})
            print('ARIMA{}x{}12 - AIC:{}'.format(param, param_seasonal, results.aic))
        except Exception as e:
            print('f"Error fitting ARIMA {param}x{param_seasonal}12:{e}')
            continue

# convert the result list to df
results_df = pd.DataFrame(results_list)

#(6) Find the parameters with the min AIC
if not results_df.empty:
    best_params = results_df.loc[results_df['AIC'].idxmin()]
    print("\nBest ARIMA parameters:")
    print("Order:", best_params['param'])
    print('Seasonal Order:', best_params['param_seasonal'])
    print("AIC:", best_params['AIC'])
else:
    print('No valid models were fitted. Please check your data and aparameter ranges')

# Output:
#     Best ARIMA parameters:
# Order: (0, 1, 1)
# Seasonal Order: (0, 1, 1, 12)
# AIC: 279.5806233386812

#===5. Fit ARIMA model
mod = sm.tsa.statespace.SARIMAX(y, 
                                order=(0,1,1),
                                seasonal_order=(0,1,1,12),
                                # enforce_stationarity=False, #so that plot_diagnostics() could work
                                enforce_invertibility=False)
results = mod.fit()
print(results.summary().tables[1])

#===6. model diagnostics
results.plot_diagnostics(figsize=(20,10))
plt.show()

#---additional diagnostic code
from statsmodels.graphics.tsaplots import plot_acf, plot_pacf
from statsmodels.stats.diagnostic import acorr_ljungbox

# ACF and PACF plots of the residuals
residuals = results.resid

plt.figure(figsize=(12,6))
plt.subplot(121)
plot_acf(residuals, lags=30, ax=plt.gca())
plt.subplot(122)
plot_pacf(residuals, lags=30, ax=plt.gca())
plt.show()

# Ljung-Box test
lb_results= acorr_ljungbox(residuals, lags=[10], return_df=True)
print("Ljung-Box test results:\n", lb_results)

#===7. Validate forecasts
pred = results.get_prediction(start=pd.to_datetime('2017-01-01'), dynamic=False)
pred_ci = pred.conf_int()

ax = y['2014':].plot(label='observed')
pred.predicted_mean.plot(ax=ax, label='One-step ahead Forecast',
                         alpha=.7, figsize=(14,7))
ax.fill_between(pred_ci.index, pred_ci.iloc[:, 0],
                pred_ci.iloc[:, 1],
                color='k',
                alpha=.2)
ax.set_xlabel('Date')
ax.set_ylabel('Furniture Sales')
plt.legend()
plt.show()

#mse of forecast
y_forecasted = pred.predicted_mean
y_truth = y['2017-01-01':]

mse = ((y_forecasted - y_truth)** 2).mean()
print('The Mean Squared Error of our forecasts is {}'.format(round(mse,2))) # 34370.12
print('The Root Mean Squared Error of our forecasts is {}'.format(round(np.sqrt(mse),2))) #185.39

#===8. Visualize forecasts
pred_uc = results.get_forecast(steps=100)#or `=500` which is the number of steps to forecast from the end of the sample
pred_ci = pred_uc.conf_int()

ax = y.plot(label='observed', figsize=(14,7))
pred_uc.predicted_mean.plot(ax=ax, label='Forecast')
ax.fill_between(pred_ci.index,
                pred_ci.iloc[:,0],
                pred_ci.iloc[:,1],
                color='k', alpha=.25)
ax.set_xlabel('Date')
ax.set_ylabel('Furniture Sales')
plt.legend()
plt.show()

