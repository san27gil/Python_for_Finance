import pandas as pd
from tabulate import tabulate
import yfinance as yf
import matplotlib.pyplot as plt

tickers = []
prices = []
prices_today = []
shares = []
 
print('''
> Tell me one by one your porfolio. To do so, write:
    1. Ticker.
    2. Average stock price of your bought. 
    3. The number of shares owned.

> When you've finished, write "end" within the ticker section. 

> Finally, write you cash position and press enter. 
''' )

# Ask for the portfolio components
while True:
    x = input('Ticker: ')
    if len(x) == 4 or len(x) == 5:
        x = x.upper()
        tickers.append(x)
        y = float(input('Average stock price:'))
        prices.append(y)
        z = int(input('Number of shares: '))
        shares.append(z)
    elif x == 'end':
        break
    elif len(x) != 4:
        print('> Ticker must contain 4 letter words')

# Ask for the amount held in cash
cash = input('Cash in $: ')

# Get the current price of every stock in the portfolio
for ticker in tickers:
    try:
        data = yf.download(ticker, period='5d',progress=False)
        price_today = round(data['Adj Close'][-1],2)
        price_today = float(price_today)
        prices_today.append(price_today)
    except Exception as e:
        print('ERROR', e)

# Create the data frame
df = pd.DataFrame(list(zip(tickers,prices,prices_today,shares)), columns=['Ticker', 'Avg. Price', 'Current price', 'Number of shares'])
df['Bought'] = round((df['Avg. Price'] * df['Number of shares']),2).astype(str) + '$'
df['Rentabilidad'] = round((((df['Current price'] - df['Avg. Price']) / df['Avg. Price'])*100), 2).astype(str) + '%'
df['Total'] = round((df['Current price'] * df['Number of shares']),2).astype(str) + '$'

print(tabulate(df, headers='keys', tablefmt='pretty', showindex=False, colalign=("right",)))

total = df['Total'].to_list()
total.append(cash)
total = list(map(lambda x: x.replace('$', ''), total))
tickers.append('CASH')

# Graph
plt.figure(figsize=(8,4))

plt.title('Portfolio', fontsize=16, bbox={'facecolor':'0.9' , 'pad': 5})

plt.pie(total, labels=tickers, autopct='%.1f%%',
        textprops={'fontsize': 8}, wedgeprops = {'edgecolor': 'black'},
        pctdistance=0.7)

plt.show()
