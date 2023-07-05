import numpy as np
import pandas_datareader.data as web
from datetime import datetime, timedelta
import yfinance as yfin

yfin.pdr_override()

# PARAMETERS TO SET
discount_rate = 0.0525
arithmic_div_yield = 0.005
stock = "AAPL"
days_to_expiration = 365
trading_days_to_expiration = round(days_to_expiration * 252/365)
strike_price = 200
trials = 10000

start = datetime.today() - timedelta(days = 365*7.5)
end = datetime.today()

# calculate true yield
cash_price = 1 - discount_rate * 30/360
true_yield = 365/30*np.log(1+0.004375/cash_price)

# calculate continuous dividend yield
cont_div_yield = np.log(1 + arithmic_div_yield)

# calculate risk neutral drift
drift = true_yield - cont_div_yield

# read stock data
df = web.DataReader(stock, start, end)["Adj Close"]

# calculate standard deviation
std_dev = df.pct_change().std() * np.sqrt(365/252)

# MONTE CARLO SIMULATION
# assume normal distribution of returns
counter1 = 0
counter2 = 0
cur_price = df.iloc[-1]
for i in range(trials):
    price = cur_price
    daily_return = np.random.normal(drift / 365, std_dev, days_to_expiration) + 1
    strike_met = False
    for r in daily_return:
        price *= r
        if price >= strike_price and strike_met == False:
            counter1 += 1
            strike_met = True
    if price >= strike_price:
        counter2 += 1

print(f"probability of meeting strike before expiration date is {counter1/trials}")
print(f"probability of meeting strike on expiration date {counter2/trials}")
