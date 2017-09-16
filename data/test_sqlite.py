import numpy as np
import matplotlib.pyplot as plt
import sqlite3

execfile('../ctw\ algorithm/python/ctw.py')
conn = sqlite3.connect('../../vwap.sqlite')

cursor = conn.cursor()


cursor.execute("SELECT Price,Volume,Time FROM ETHEUR")
eth = np.array(cursor.fetchall())

cursor.execute("SELECT Price,Volume,Time FROM XBTEUR")
btc = np.array(cursor.fetchall())

(size, p) = btc.shape
# plt.plot(btc[:,2],btc[:,0])
# plt.show()

ethLog = np.log(eth[1:,0]) - np.log(eth[:(size-1),0]) 
btcLog = np.log(btc[1:,0]) - np.log(btc[:(size-1),0]) 
plt.plot(btcLog)
# plt.plot(ethLog)
plt.show()
