# Projects:
## 1. Harris vs Trump 2024 Election Prediction: 
The project aimed to simulate the 2024 U.S. Presidential Election using Bayesian methodology while incorporating polling data, past 2020 election results and uncertainty modeling. The goal was to forecast electoral vote (EV) distributions and visualize state-by-state probabilities.

### Approach & Methodology
1. Data Collection & Processing
  * Polling Data Scraping:
    * Used `BeautifulSoup`, `requests` to scrape the latest state-level polling from [FiveThirtyEight](https://projects.fivethirtyeight.com/polls/president-general/).
    * Addressed HTML structural variations (eg. those having "More" dropdown toggle) and standardize Democratic candidate (Biden or other candidates as Harris).
  * 2020 Historical Election data: include electoral vote and total votes per state.
  * Dynamic Weighting between polls and past votes:
    * Defined `weight_poll` and `weight_vote` to control how much weight we place on recent polls and past election results. The two of which must sum up to 1. 
    * Iterate over multiple weight combinations to simulate different forecast scenarios.

2. Bayesian Simulation with Beta Distribution
  * Modeled state-level uncertainty using beta distribution: model the **probability** of a candidate winning a majority in each state
    * `alpha= weighted Harris votes + 1`
    * `beta= weighted Trump votes + 1`
  * Vectorized Monte Carlo Simulation (`NumPy, SciPy`):
    * winner-takes-all 
  
3. Aggregate Results & Probability Mapping
 * State-levle probability calculation
   * Aggregate expected electoral votes for each state (`np.mean`)
   * Use `GeoPandas`, `Matplotlib` to plot probabilities of each candidate winning each state

### Key Findings & Conclusion
* Trump is clear winning across multiple states
<img width="1264" alt="image" src="https://github.com/user-attachments/assets/be61996c-c92b-4dbf-bae2-54a19da78d97" />

