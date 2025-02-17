* Models:
  * Classification: Decision Tree, Random Fores
  * Regression

* Techniques: Backtesting optimization
* Trading Strategies: Percent Change, 50-day Moving Average (medium-term trend indicator), Pairs Trading, Bollinger Bands, Loss-Decreasing Strategies 
* Source: [yahoo finance](https://finance.yahoo.com) -> `yfinance`

---
# Project 1. Percent Change Backtesting with Classification & Regression Models
* Appraoches: `pct_change(-1) * 100 * -1` to calculate the difference from the next day, `backtesting` to evaluate the model performance, `pickle` to save the model objects and `scikit-learn`'s `DecisionTreeRegressor`, `DecisionTreeClassifier` for modeling
* backtesting output:
![image](https://github.com/user-attachments/assets/a6268db5-11d3-4258-b387-37c3e8eb94ef)
Zomming in:
<img width="1440" alt="image" src="https://github.com/user-attachments/assets/81b7ef90-bbe4-419d-849b-7c2eb1ae9f14" />


---
### Performance Metrics
| Metric | Meaning | How to interpret? |
|:-------| :-------|:------------------|
| Start & End Date| The first and last date of the backtest| The time period tested|
| Duration| The total number of days covered in the test| Longer tests are more reliable|
| Equity Final [$]| The final portfolio value at the end| Higher is better|
| Return [%]| Total percentage return of the strategy| If negative, the strategy lost money|
| Buy & Hold Return [%]| How much you'd make if you just bought and held the asset| If it beats your strategy, the strategy might not be good|
| Exposure Time [%]| The percentage of time the strategy in an active position (invested)| Low exposure means the strategy was mostly in cash|
| Max. Drawdown [%]| The worst percetnage loss from a peak before recovering| A high drawdown means the strategy has large temporary losses|
| Max. Drawdown [$]| The largest dollar loss before recovering| A high dollar drawdown might indicate high risk|


eg.
* If **_Buy & Hold Return [%]_**=15%, the strategy outperformed buy&hold by 15%.; if `30%` meaning buy&hold may be better than the strategy.
* If **_Max.Drawdown_[%]_**=-5%, the worst loss was only 5%, meaning low risk; if `-40%` means very risky.



### Trade-Specific Metrics
| Metric | Meaning | How to interpret? |
|:-------| :-------|:------------------|
| Trades| The total number of trades executed| Too few means the strategy is inactive; too many means it's overtrading.|
| Win Rate [%]| Percentage of profitable trades| **_Above 50%_** is good, but win rate alone isn't enough|
| Best Trade [%]| The highest return from a single trade| Shows the potential upside of the strategy|
| Worst Trade [%]| The largest percentage loss from a single loss| Shows the worst-case scenario for a single trade|
| Avg. Trade [%]| The average return per trade| If negative, the strategy is losing over time|
| Profit Factor| `(Total Profit / Total Loss)` Measure risk vs reward| If **_> 1.5_**, the strategy is profitable. **_Below 1_** is losing money|
| Commissions [$]| The total fees paid for trading| High commissions reduce net profits|



eg.
* **_Profit Factor_**=2.0, meaning the profits are twice as large as losses.
* **_Win Rate_**=60%, meaning more than half the trades were profitable.
