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

