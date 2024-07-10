# pip install beautifulsoup4 #to pull data out of html files
# pip install requests #to grab the source code from wiki page
# pip install yfinance #to get stock data
# pip install datetime #to deal with datetime object
import bs4 as bs
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

#every symbol was imported and stored with the new line character (\n) which is what we need to remove
#with list comprehension
tickers = [s.replace('\n', '') for s in tickers]
print(tickers)


#---Download each stock from Yahoo Finance
start = datetime.datetime(2019, 1, 1)
end = datetime.datetime(2024, 7, 10)
data = yf.download(tickers, start=start, end=end)
# data.head()

#format the data
df = data.stack().reset_index().rename(index=str, columns={'level_1': 'Ticker'}).sort_values(['Ticker','Date'])
df.set_index('Date', inplace=True)
# df.head()
#save to csv file (for future use)
df.to_csv('sp500.csv')
