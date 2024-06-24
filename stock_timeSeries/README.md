<a name='back2table'></a>
## Table of Content:
* [Prophet Additive Model Prediction](#additivesModelPrediction)</br>
* [ARIMA Model Prediction](#ARIMAModelPrediction)

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
     <img width="818" alt="image" src="https://github.com/Pinghsuanlin/PythonScopedSkills/assets/96319356/c090a201-f387-46bb-b8a8-5ce9c09aad40">

  3. Validate forecast's accuracy (cf. estimated and real data:
     <img width="818" alt="image" src="https://github.com/Pinghsuanlin/PythonScopedSkills/assets/96319356/df03638c-bd37-486e-b537-baa377d21146">


[Back 2 table](#back2table)
