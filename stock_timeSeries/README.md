<a name='back2table'></a>
## Table of Content:
* [Prophet Additive Model Prediction](#additivesModelPrediction)</br>
* [ARIMA Model Prediction](#ARIMAModelPrediction)</br>
* [Scrape S&P500 with bs4 and requests](#scrapeSP500)</br>
* [Locally Weighted Scatterplot Smoothing (LOWESS) Fitting](#lowessFit)</br>

<a name='additivesModelPrediction'></a>
# In _additivesModelPrediction.py_, I used `Pynance` to retrieve stock data and `Prophet` for future 2 years prediction.
* Key Insights include:
  1. Predicting interested ticker potential market cap:
     
     <img width="400" alt="image" src="https://github.com/Pinghsuanlin/PythonScopedSkills/assets/96319356/8b110982-2222-43f3-8cb3-79ec37638a16">

  2. Predicting trend and component in weekly and yearly timestamp as such:
     
     <img width="393" alt="image" src="https://github.com/Pinghsuanlin/PythonScopedSkills/assets/96319356/c288a35d-3bb7-4097-b5a5-ba0981950624">

[Back 2 table](#back2table)


<a name='ARIMAModelPrediction'></a>
# The project is forecasting sale using Autoregressive Integrated Moving Average (ARIMA) model
`ARIMA(p, d, q)` encompass seasonality, trend, and noise respectively.

* Key Insights include:
  1. Grid-search to get the optimal parameters of the model:
     
    ```{python}
    results_list = [] 
    
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
                                             'AIC': results.aic}, ignore_index=True)
                print('ARIMA{}x{}12 - AIC:{}'.format(param, param_seasonal, results.aic))
            except Exception as e:
                print('f"Error fitting ARIMA {param} * {param_seasonal}12:{e}')
                continue
    
    # convert the result list to df
    results_df = pd.DataFrame(results_list)

    #find the best combo with the least AIC
    if not results_df.empty:
      best_params = results_df.loc[results_df['AIC'].idxmin()]
      print("\nBest ARIMA parameters:")
      print("Order:", best_params['param'])
      print('Seasonal Order:', best_params['param_seasonal'])
      print("AIC:", best_params['AIC'])
    else:
      print('No valid models were fitted. Please check your data and aparameter ranges')

    ```

  2. Diagnose ARIMA models' fit and residual:
     
     <img width="700" alt="image" src="https://github.com/Pinghsuanlin/PythonScopedSkills/assets/96319356/c090a201-f387-46bb-b8a8-5ce9c09aad40">


  4. Validate forecast's accuracy (cf. estimated and real data:
     
     <img width="400" alt="image" src="https://github.com/Pinghsuanlin/PythonScopedSkills/assets/96319356/df03638c-bd37-486e-b537-baa377d21146">


[Back 2 table](#back2table)


<a name='ARIMAModelPrediction'></a>
# Scrape S&P500 with bs4 and requests
Key syntax: 
  ```{Python}
  import requests
  import yfinance as yf
  import datetime
  
  #----Read all tickers’ stocks belonging to the S&P500 
  #visit the interested page for list of 500 companies
  resp = requests.get('https://en.wikipedia.org/wiki/List_of_S%26P_500_companies')
  #create a BeautifulSoup object that parse HTML the way a web browser
  soup = bs.BeautifulSoup(resp.text, 'lxml')
  #inspect element and look for the table
  table = soup.find('table', {'class': 'wikitable sortable'})
  
  
  #---Store them in a list
  #create an empty list 
  tickers = []
  #populate it using for loop by which we iterate through the table
  for row in table.findAll('tr')[1:]:
      ticker = row.findAll('td')[0].text
      tickers.append(ticker)
  print(tickers)
  ```

[Back 2 table](#back2table)

<a name='lowessFit'></a>
# Locally Weighted Scatterplot Smoothing Fitting
Unlike linear, stepwise or other regression model, LOWESS is a **_non-parametric_** regression that fits a smooth curve to a set of points without assuming any particular functional form for the relationship between variables. It's suitable for data with *periodicity* and *volatility*.</br>

Key syntax:
```{Python}
from statsmodels.nonparametric.smoothers_lowess import lowess

# compute a lowesss smoothing estimate of the data (using `statsmodels`)
smoothed = sm.nonparametric.lowess(exog=x, endog=y, frac=0.2)

# plot the fit line
fig, ax = pylab.subplots()
ax.scatter(x, y)
ax.plot(smoothed[:, 0], smoothed[:, 1], c='k')
pylab.autoscale(enable=True, axis='x', tight=True)
```

Output:</br>
<img width="528" alt="image" src="https://github.com/user-attachments/assets/aa4ba2fb-af8e-4573-8679-11291ee9d116">


[Back 2 table](#back2table)


