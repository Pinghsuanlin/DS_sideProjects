import numpy as np
from statsmodels.nonparametric.smoothers_lowess import lowess
import matplotlib.pyplot as plt #provides more control over the plotting functions than `pylab`
# pip install -U scikit-learn
from sklearn.model_selection import train_test_split
from sklearn. metrics import mean_squared_error

"""Generate a sin wave with added noise"""
def generate_data(n_samples=200, noise_level=0.2):
    # generate x values from 0 to 4 pi
    x = np.linspace(0, 4 * np.pi, n_samples)
    # generate y values as since wave with added noise
    y = np.sin(x) + np.random.normal(0, noise_level, n_samples)
    return x, y

"""Perform LOWESS smoothing on the input data; 
Use boostrap resampling to estimate confidence intervals.
Returns the smoothed curve and confidence bounds"""
def lowess_with_confidence_bounds(x, y, eval_x, N=200, conf_interval=0.95, lowess_kw=None):
    if lowess_kw is None:
        lowess_kw = {}
    
    # perform LOWESS smoothing
    smoothed = lowess(endog=y, exog=x, xvals=eval_x, return_sorted=False, **lowess_kw)#[:, 1] # this caseus error as too many indices #return_sorted=False, 
    
    # Bootstrap resampling
    smoothed_values = np.empty((N, len(eval_x)))
    for i in range(N):
        # randomly sample with replacement
        sample = np.random.choice(len(x), len(x), replace=True)
        sampled_x, sampled_y = x[sample], y[sample]
        # perform LOWESS on resampled data
        smoothed_values[i] = lowess(endog=sampled_y, exog=sampled_x, xvals=eval_x, return_sorted=False, **lowess_kw)#[:, 1] #return_sorted=False, 
    
    # calculate confidence intervals
    alpha = (1 - conf_interval) / 2
    bottom = np.percentile(smoothed_values, alpha * 100, axis=0)
    top = np.percentile(smoothed_values, (1 - alpha) * 100, axis=0)
    
    return smoothed, bottom, top

"""Uses LOWESS to predice y values for the test set.
Calculate RMSE for validation."""
def forecast_and_validate(x_train, y_train, x_test, y_test, lowess_kw=None):
    if lowess_kw is None:
        lowess_kw = {}
    
    # Forecast using LOWESS
    y_pred = lowess(endog=y_train, exog=x_train, xvals=x_test, return_sorted=False, **lowess_kw)#[:, 1] 
    
    # Calculate RMSE
    rmse = np.sqrt(mean_squared_error(y_test, y_pred))
    
    return y_pred, rmse

# Generate data
np.random.seed(0)
x, y = generate_data(n_samples=200, noise_level=0.2)

# Split data into train and test sets
x_train, x_test, y_train, y_test = train_test_split(x, y, test_size=0.2, random_state=42)

# Fit LOWESS and calculate confidence intervals
eval_x = np.linspace(min(x), max(x), 300)
smoothed, bottom, top = lowess_with_confidence_bounds(x_train, y_train, eval_x, lowess_kw={'frac': 0.3})

# Forecast and validate
y_pred, rmse = forecast_and_validate(x_train, y_train, x_test, y_test, lowess_kw={'frac': 0.3})

# Create a smooth forecast line to avoid zig-zag issue with forecast line
forecast_x = np.linspace(min(x_test), max(x_test), 100)
forecast_y = lowess(y_train, x_train, xvals=forecast_x, return_sorted=False, frac=0.3)


# Plotting
plt.figure(figsize=(12, 6))
plt.scatter(x_train, y_train, alpha=0.5, label='Training Data', color='blue')
plt.scatter(x_test, y_test, alpha=0.5, label='Test Data', color='green')
plt.plot(eval_x, smoothed, c='red', label='LOWESS (Train)', linewidth=2)
plt.fill_between(eval_x, bottom, top, alpha=0.2, color='gray', label='95% CI')
plt.plot(forecast_x, forecast_y, c='orange', label='LOWESS (Forecast)', linewidth=2)
plt.scatter(x_test, y_pred, c='purple', label='Predicted Points', s=30)
plt.legend()
plt.title(f'LOWESS with Confidence Inervals and Forecast (RMSE: {rmse:.4f})')
plt.xlabel('X')
plt.ylabel('Y')
plt.grid(True, alpha=0.3)
plt.show()

print(f"Root Mean Squared Error: {rmse:.4f}")


forecast_x = np.linspace(min(x_test), max(x_test), 100)
forecast_y = lowess(y_train, x_train, xvals=forecast_x, return_sorted=False, frac=0.3)
