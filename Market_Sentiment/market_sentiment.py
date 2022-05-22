import pandas as pd
import numpy as np
import yfinance as yf
from datetime import datetime,timedelta
from pandas_datareader import data as pdr
from tabulate import tabulate
from bs4 import BeautifulSoup
import requests

# Tickers and each name
tickers_sector = ('XLE', 'XLF', 'XLK', 'XLV', 'XLU', 'XLI', 'XLB', 'XLY',
 'XLP', 'XLRE')
names_sector = ('Energy', 'Financial', 'Technology', 'Health', 'Utilities', 
'Industrial', 'Materials', 'Consumer Discret.', 'Consumer Staples', 'Real Estate')

tickers_indx = ('^IXIC', '^GSPC', '^RUT', 'IWO', 'IPO', 'ARKK', 'MCHI', 'BCT-USD')
names_indx = ('Nasdaq', 'SP500', 'Russell 2000', 'Russell Growth', 'IPO ETF', 'ARKK Innovation',
'China ETF', 'Bitcoin')

# Empty lists
latest_indx = []
percentage_indx = []
week_ago_indx = []
month_ago_indx = []
ytd_indx = []

latest_sect = []
ytd_sect = []
percentage_sect = []
week_ago_sect = []
month_ago_sect = []

# Dates references
today = datetime.today().date()
yesterday = today - timedelta(days=1)
month = today - timedelta(days=30)
year = today - timedelta(days=365)

# ---------------- DataFrame current stock market ---------------

print('''
1. CURRENT STOCK MARKET:
''')

for ticker in tickers_indx:
    try:
        data_indx = yf.download(ticker, period='5d', interval='1d', progress=False)
        latest_price_indx = round(data_indx['Adj Close'][-1], 2)
        yesterday_price_indx = round(data_indx['Adj Close'][-2], 2)
        percentage = round(((latest_price_indx-yesterday_price_indx)/yesterday_price_indx)*100, 2)
        latest_indx.append(latest_price_indx)
        percentage_indx.append(percentage)

    except Exception as e:
        print('ERROR', e)

df = pd.DataFrame(list(zip(names_indx, latest_indx, percentage_indx)), 
columns=['INDEX', 'VALUE', '% CHANGE'], index=None).sort_values(by=['% CHANGE'], ascending=False)
print(tabulate(df, headers='keys', tablefmt='pretty', showindex=False, colalign=("right",)))

# ---------------- DataFrame % SO FAR ---------------

print('''
2. STOCK MARKET PERFORMANCE SO FAR:
''')

for ticker in tickers_indx:
    try:
        data_indx = yf.download(ticker, period='30d', interval='1d', progress=False)
        data_indx_ytd = yf.download(ticker, start='2022-01-02', end='2022-01-04', progress=False)
        latest_price_indx = round(data_indx['Adj Close'][-1], 2)
        ytd_price_indx = round(data_indx_ytd['Adj Close'][-1], 2)
        weekago_price_indx = round(data_indx['Adj Close'][-6], 2)
        monthago_price_indx = round(data_indx['Adj Close'][-24], 2)
        percentage_week = round(((latest_price_indx-weekago_price_indx)/weekago_price_indx)*100, 2)
        percentage_month = round(((latest_price_indx-monthago_price_indx)/monthago_price_indx)*100, 2)
        percentage_ytd = round(((latest_price_indx-ytd_price_indx)/ytd_price_indx)*100, 2)
        week_ago_indx.append(percentage_week)
        month_ago_indx.append(percentage_month)
        ytd_indx.append(percentage_ytd)

    except Exception as e:
        print('ERROR', e)

df2 = pd.DataFrame(list(zip(names_indx, percentage_indx, week_ago_indx, month_ago_indx, ytd_indx)), 
columns=['INDEX', '% INTRADAY', '% LAST 7 DAYS', '% LAST 30 DAYS', '% YTD'], index=None).sort_values(by=['% YTD'], ascending=False)
print(tabulate(df2, headers='keys', tablefmt='pretty', showindex=False, colalign=("right",)))

for ticker in tickers_sector:
    try:
        data_sector = yf.download(ticker, period='30d', interval='1d', progress=False)
        data_sector_ytd = yf.download(ticker, start='2022-01-02', end='2022-01-04', progress=False)
        latest_price_sector = round(data_sector['Adj Close'][-1], 2)
        yesterday_price_sector = round(data_sector['Adj Close'][-2], 2)
        percentage_sector = round(((latest_price_sector-yesterday_price_sector)/yesterday_price_sector)*100, 2)
        ytd_price_sector = round(data_sector_ytd['Adj Close'][-1], 2)
        weekago_price_sector = round(data_sector['Adj Close'][-6], 2)
        monthago_price_sector = round(data_sector['Adj Close'][-24], 2)
        percentage_week = round(((latest_price_sector-weekago_price_sector)/weekago_price_sector)*100, 2)
        percentage_month = round(((latest_price_sector-monthago_price_sector)/monthago_price_sector)*100, 2)
        percentage_ytd = round(((latest_price_sector-ytd_price_sector)/ytd_price_sector)*100, 2)
        percentage_sect.append(percentage_sector)
        week_ago_sect.append(percentage_week)
        month_ago_sect.append(percentage_month)
        ytd_sect.append(percentage_ytd)

    except Exception as e:
        print('ERROR', e)

df3 = pd.DataFrame(list(zip(names_sector, percentage_sect, week_ago_sect, month_ago_sect, ytd_sect)), 
columns=['SECTOR', '% INTRADAY', '% LAST 7 DAYS', '% LAST 30 DAYS', '% YTD'], index=None).sort_values(by=['% YTD'], ascending=False)
print(tabulate(df3, headers='keys', tablefmt='pretty', showindex=False, colalign=("right",)))

# ---------------- DataFrame Market Sentiment ---------------

print('''
3. NASDAQ-100 NEW HIGHS - NEW LOWS:
''')

headers = {'user-agent': 'Mozilla/5.0'}
url2 = 'https://en.wikipedia.org/wiki/Nasdaq-100#Components'
response = requests. get(url2, headers=headers)
soup2 = BeautifulSoup(response.text, 'html.parser')

# Nasdaq tickers
tickers2 = soup2.find("table", attrs={'id': 'constituents'})
table2 = pd.read_html(str(tickers2))
df = pd.DataFrame(table2[0])
nasdaq_tickers = df['Ticker'].tolist()

nasdaq_highs = []
nasdaq_lows = []

# NEW HIGHS NEW LOWS
for ticker in nasdaq_tickers:
    data = yf.download(ticker, period='5d', interval='1d', progress=False)
    today = round(data['Adj Close'][-1], 2)
    yesterday = round(data['Adj Close'][-2], 2)
    if today > yesterday:
        nasdaq_highs.append(1)
    else:
        nasdaq_lows.append(1)

print('Number of new highs:', len(nasdaq_highs))
print('Number of new lows:', len(nasdaq_lows))
