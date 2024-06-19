#pip install numpy < 1.24
import numpy as np
import pandas as pd
#pip install pandas_datareader
from pandas_datareader import data
import matplotlib
import lxml
#pip install pynance
import pynance as pn
np.__version__ #1.23.5
# python -m pip install prophet
from prophet import Prophet
from functools import reduce

#=== plotting setting-----------------------
import matplotlib.pyplot as plt
import seaborn as sns

plt.style.use('fivethirtyeight') # type: ignore
matplotlib.rcParams['axes.labelsize'] = 14
matplotlib.rcParams['xtick.labelsize'] = 12
matplotlib.rcParams['ytick.labelsize'] =12
matplotlib.rcParams['text.color'] = 'k'

#=== interested tickers-----------------------
tickers = ['AAPL', 'MSFT', 'NVDA']
dt = pn.data.get(tickers, '2019-01-01', '2024-06-17')
dt.head()
dt.tail()

mi = dt.columns; mi
mi.tolist()
ind = pd.Index([e[0]+ '_'+ e[1] for e in mi.tolist()])
print(ind)
dt2 = dt.copy()
dt2.columns = ind
dt2.head()


#=== Calculate market capitalization-----------------------
# number of shares
"""source: macrotrend> revenue & profits > share outstanding
https://www.macrotrends.net/stocks/charts/AAPL/apple/shares-outstanding
or yChart for SP500 https://ycharts.com/companies/SPGI/shares_outstanding#:~:text=S%26P%20Global%20Shares%20Outstanding%3A%20312.90M%20for%20April%2019%2C%202024&text=View%20and%20export%20this%20data%20back%20to%201984
"""

# yearly avg number of shares outstanding for 'AAPL', 'MSFT', 'NVDA', '^GSPC'
aapl_shares = {2024:15.47e9, 2023:15.84e9, 2022:16.4e9, 2021:16.93e9, 2020:17.61e9, 2019:18.8e9}
nvda_shares = {2024:2.49e9, 2023:2.51e9, 2022:2.54e9, 2021:2.51e9, 2020:2.47e9, 2019:2.5e9}
msft_shares = {2024:7.47e9, 2023:7.46e9, 2022:7.53e9, 2021:7.60e9, 2020:7.68e9, 2019:7.74e9}
#e9 as in billions of dollars

#create a year column
dt2['Year'] = dt2.index.year
#take dates from index and move to Date column
dt2.reset_index(level=0, inplace=True)
dt2['Cap_AAPL']=0
dt2['Cap_NVDA']=0
dt2['Cap_MSFT']=0
# dt2[('Cap', 'AAPL')]=0
# dt2[('Cap', 'NVDA')]=0
# dt2[('Cap', 'MSFT')]=0
# dt2[('Cap', 'gspc')]=0

#calculate market cap for all years
for i, year in enumerate(dt2['Year']):
    #retrieve the shares for the year
    aapl_s = aapl_shares.get(year)
    nvda_s = nvda_shares.get(year)
    msft_s = msft_shares.get(year)
    
    #update the cap column to shares * price
    dt2['Cap_AAPL'][i] = aapl_s * dt2['Close_AAPL'][i]
    dt2['Cap_NVDA'][i] = nvda_s * dt2['Close_NVDA'][i]
    dt2['Cap_MSFT'][i] = msft_s * dt2['Close_MSFT'][i]
    
#===Visual comparison-----------------------
plt.figure(figsize=(10,8))
plt.plot(dt2['Date'], dt2['Cap_AAPL']/1e12, 'b-', label='AAPL')
plt.plot(dt2['Date'], dt2['Cap_NVDA']/1e12, 'r-', label='NVDA')
plt.plot(dt2['Date'], dt2['Cap_MSFT']/1e12, 'g-', label='MSFT')
plt.xlabel('Date')
plt.ylabel('Market Cap (Trillion $)')
plt.title('Market Cap of AAPL, NVDA, MSFT')
plt.legend()

#Find since when did MSFT surpass AAPL in market cap since 2023
filtered_23 = dt2[(dt2['Cap_MSFT'] > dt2['Cap_AAPL']) & (dt2['Date'].dt.year >= 2023)]
#get the first date that meet the requirements
first_date = filtered_23['Date'].min()
last_date = filtered_23['Date'].max()
print("MSFT's market cap exceeded AAPL's in 2023 or later s {} to {}.".format(first_date.date(), last_date.date()))

#===Prophet models-----------------------
#columns needed (ds:date, y:cap)
aapl = dt2.rename(columns={'Date': 'ds', 'Cap_AAPL': 'y'})
#put market cap in trillions
aapl['y'] = aapl['y'] / 1e9

msft = dt2.rename(columns={'Date': 'ds', 'Cap_MSFT': 'y'})
#put market cap in trillions
msft['y'] = msft['y'] / 1e9

nvda = dt2.rename(columns={'Date': 'ds', 'Cap_NVDA': 'y'})
#put market cap in trillions
nvda['y'] = nvda['y'] / 1e9

#make the prophet models and fit on the data
"""
* changepoint_prior_scale: Parameter modulating the flexibility of the
automatic changepoint selection. 
    Large values will allow many changepoints, 
    small values will allow few changepoints.
* n_changepoints: Number of potential changepoints to include.
"""
aapl_prophet= Prophet(changepoint_prior_scale=0.05)
aapl_prophet.fit(aapl)

msft_prophet= Prophet(changepoint_prior_scale=0.05)
msft_prophet.fit(msft)

nvda_prophet= Prophet(changepoint_prior_scale=0.05)
nvda_prophet.fit(nvda)

#prediction for 2 years
dt_aapl = aapl_prophet.make_future_dataframe(periods=365 * 2, freq='D')
aapl_forecast = aapl_prophet.predict(dt_aapl)

dt_msft = msft_prophet.make_future_dataframe(periods=365 * 2, freq='D')
msft_forecast = msft_prophet.predict(dt_msft)

dt_nvda = nvda_prophet.make_future_dataframe(periods=365 * 2, freq='D')
nvda_forecast = nvda_prophet.predict(dt_nvda)

#viz
aapl_prophet.plot(aapl_forecast, xlabel='Date', ylabel='Market Cap (Billion $)')
plt.title('Market Cap of AAPL')

msft_prophet.plot(msft_forecast, xlabel='Date', ylabel='Market Cap (Billion $)')
plt.title('Market Cap of MSFT')

nvda_prophet.plot(nvda_forecast, xlabel='Date', ylabel='Market Cap (Brillion $)')
plt.title('Market Cap of NVDA')


#=== When NVDA will overtake MSFT and AAPL----------------------
aapl_names = ['aapl_%s' % column for column in aapl_forecast.columns]
msft_names = ['msft_%s' % column for column in msft_forecast.columns]
nvda_names = ['nvda_%s' % column for column in nvda_forecast.columns]
# aapl_names

#=== df to merge
aapl_forecast_1 = aapl_forecast.copy()
msft_forecast_1 = msft_forecast.copy()
nvda_forecast_1 = nvda_forecast.copy()

#rename the columns
aapl_forecast_1.columns = aapl_names
msft_forecast_1.columns = msft_names
nvda_forecast_1.columns = nvda_names

#rename as date
# aapl_forecast_1.columns.values[0:1] = ['date']
# msft_forecast_1.columns.values[0:1] = ['date']
# nvda_forecast_1.columns.values[0:1] = ['date']
aapl_forecast_1.rename(columns={aapl_names[0]: 'date'}, inplace=True)
msft_forecast_1.rename(columns={msft_names[0]: 'date'}, inplace=True)
nvda_forecast_1.rename(columns={nvda_names[0]: 'date'}, inplace=True)


#merge multiple datasets
#list of df you want to merge
df = [aapl_forecast_1, msft_forecast_1, nvda_forecast_1]
df_merged = reduce(lambda left, right: pd.merge(left, right,on='date', how='outer'), df)
df_merged.head()

#visualize trend only and the forecast
plt.figure(figsize=(10,8))
plt.plot(df_merged['date'], df_merged['aapl_trend'], 'b-')
plt.plot(df_merged['date'], df_merged['msft_trend'], 'g-')
plt.plot(df_merged['date'], df_merged['nvda_trend'], 'r-')
plt.xlabel('Date')
plt.ylabel('Market Cap ($)')
plt.title('AAPL cf MSFT cf NVDA Trend')
plt.legend()

#visualize estimate only and the forecast
plt.figure(figsize=(10,8))
plt.plot(df_merged['date'], df_merged['aapl_yhat'], 'b-')
plt.plot(df_merged['date'], df_merged['msft_yhat'], 'g-')
plt.plot(df_merged['date'], df_merged['nvda_yhat'], 'r-')
plt.xlabel('Date')
plt.ylabel('Market Cap ($)')
plt.title('AAPL cf MSFT cf NVDA Estimate')
plt.legend()


#===Forecast with uncertainty bounds
#create subplots to set figure size
fig, ax = plt.subplots(1,1, figsize=(10,8))

#plot estimate
ax.plot(df_merged['date'], df_merged['aapl_yhat'], label='aapl_prediction')

#plot uncertainty values
ax.fill_between(df_merged['date'].dt.to_pydatetime(), \
    df_merged['aapl_yhat_upper'], df_merged['aapl_yhat_lower'],
    alpha=0.6, edgecolor='k')

#plot estimate and uncertainty for msft
ax.plot(df_merged['date'], df_merged['msft_yhat'], 'g', label='msft_prediction')
ax.fill_between(df_merged['date'].dt.to_pydatetime(), \
    df_merged['msft_yhat_upper'], df_merged['msft_yhat_lower'],
    alpha=0.6, edgecolor='k')
#for nvda
ax.plot(df_merged['date'], df_merged['nvda_yhat'], 'r', label='nvda_prediction')
ax.fill_between(df_merged['date'].dt.to_pydatetime(), \
    df_merged['nvda_yhat_upper'], df_merged['nvda_yhat_lower'],
    alpha=0.6, edgecolor='k')

plt.legend()
plt.xlabel('Date')
plt.ylabel('Billion($)')
plt.title('Market Cap Prediction for AAPL, MSFT and NVDA')

#===Trend and patterns---------------
aapl_prophet.plot_components(aapl_forecast)
msft_prophet.plot_components(msft_forecast)
nvda_prophet.plot_components(nvda_forecast)
