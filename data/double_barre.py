import numpy as np
import matplotlib.pyplot as plt
import sqlite3
import tensorflow as tf
from random import randint
import math

def av_group(tab,n):
    s = tab.size
    new_size = s / n
    ans = np.zeros(new_size)
    for i in range(new_size):
        ans[i] = np.mean(tab[i*n:(i+1)*n])
    return ans

conn = sqlite3.connect('../../vwap.sqlite')

cursor = conn.cursor()


cursor.execute("SELECT Price,Volume,Time FROM ETHEUR")
eth = np.array(cursor.fetchall())

cursor.execute("SELECT Price,Volume,Time FROM XBTEUR")
btc = np.array(cursor.fetchall())

(size, p) = btc.shape
minWindowSize = 3

ethPrice= av_group(eth[:,0],minWindowSize)
btcPrice= av_group(btc[:,0],minWindowSize)
size = ethPrice.size

ethLog = np.log(ethPrice[1:]) - np.log(ethPrice[:(size-1)]) 
btcLog = np.log(btcPrice[1:]) - np.log(btcPrice[:(size-1)]) 

plt.plot(ethPrice[1:10000])
plt.show()

money = 1000.0
eth = 5.0
deltaSell = 0.5 /100.0
deltaBuy= 0.01 /100.0
currentPrice = ethPrice[0]
sellLimit = (1.0 + deltaSell) *currentPrice
buyLimit = (1.0 - deltaBuy) *currentPrice

# ethStock= np.array([5])
# ethSellPrice = np.array([sellLimit])

t=100
for i in range(t):
    currentPrice = ethPrice[i]
    if currentPrice <=buyLimit:
        print 'buy'
        moneyBuy = money *0.5
        money -= moneyBuy
        eth += moneyBuy / buyLimit
        # sellLimit = (1 + delta) *currentPrice
        buyLimit = (1 - deltaBuy) *currentPrice
    if currentPrice >=sellLimit:
        print 'sell'
        ethSell = eth * 0.2
        eth -= ethSell
        money += ethSell*sellLimit
        sellLimit = (1 + deltaSell) *currentPrice
        # buyLimit = (1 - delta) *currentPrice

print money
print eth
print eth*ethPrice[t]
print ethPrice[t]
