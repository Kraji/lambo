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
# plt.plot(btc[:,2],btc[:,0])
# plt.show()
minWindowSize = 3

ethPrice= av_group(eth[:,0],minWindowSize)
btcPrice= av_group(btc[:,0],minWindowSize)
size = ethPrice.size

ethPrice = ethPrice[-20000:]

ethLog = np.log(ethPrice[1:]) - np.log(ethPrice[:(size-1)]) 
btcLog = np.log(btcPrice[1:]) - np.log(btcPrice[:(size-1)]) 
# ethLog = 1000* ethLog
 # print np.mean(np.square(trueValue-predi))

money = 1000
eth = 10

step=3
for i in range(ethLog.size - step):
    if (money > 0) and (ethLog[i] > 0) and (ethLog[i+1] > 0) and (ethLog[i+2] > 0):
        useMoney = math.min(money, 20.)
        eth += useMoney/ ethPrice[]
