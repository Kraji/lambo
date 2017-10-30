import numpy as np
import datetime
import matplotlib.pyplot as plt
import sqlite3
import tensorflow as tf
from random import randint
import math

def av_group_vol(tab,n,delta):
    s = tab.size
    new_size = (s - 2*delta) / n
    ans = np.zeros(new_size)
    vol = np.zeros(new_size)
    deltaSquare = np.square(tab[1:] - tab[:(s-1)]) 
    for i in range(new_size):
        ans[i] = np.mean(tab[i*n+delta:(i+1)*n+delta])
        vol[i] = np.mean(deltaSquare[i*n:(i+1)*n + 2*delta])
    return ans,vol
def av_group(tab,n):
    s = tab.size
    new_size = s / n
    ans = np.zeros(new_size)
    for i in range(new_size):
        ans[i] = np.mean(tab[i*n:(i+1)*n])
    return ans

def convertTimestamp(stamp):
    return datetime.datetime.fromtimestamp(stamp).strftime('%Y-%m-%d')

# conn = sqlite3.connect('../../vwap.sqlite')
conn = sqlite3.connect('../../krajbox.sqlite')

cursor = conn.cursor()


cursor.execute("SELECT Price,Volume,Time FROM ETHEUR")
eth = np.array(cursor.fetchall())

# cursor.execute("SELECT Price,Volume,Time FROM XBTEUR")
# btc = np.array(cursor.fetchall())




# (size, p) = btc.shape
# plt.plot(btc[:,2],btc[:,0])
# plt.show()

minWindowSize = 2
theTime = eth[:,2]
print 'min time ', np.min(theTime) # 1er janv 2017
print 'max time ', np.max(theTime) # 26 juin 2017
print 'total timestamp: ', theTime.size

timeWindow=[0.53,0.6]
indexStart = int(timeWindow[0]*theTime.size)
indexStop = int(timeWindow[1]*theTime.size)
# nbPoints = int(np.floor(theTime.size / 3))


# theTime = theTime[-nbPoints:]
theTime = theTime[indexStart:indexStop]
print 'min time ', convertTimestamp(np.min(theTime)) # 1er janv 2017
print 'max time ', convertTimestamp(np.max(theTime)) # 26 juin 2017

# ethPrice= av_group(eth[-nbPoints:,0],minWindowSize)
ethPrice, ethVol= av_group_vol(eth[indexStart:indexStop,0],minWindowSize,1)
# btcPrice,btcVol= av_group_vol(btc[-nbPoints:,0],minWindowSize,1)
size = ethPrice.size
print size

timeStampsPeriod = np.min(theTime) + minWindowSize*120*np.array(range(size))

ethLog = np.log(ethPrice[1:]) - np.log(ethPrice[:(size-1)]) 
# btcLog = np.log(btcPrice[1:]) - np.log(btcPrice[:(size-1)]) 
ethLog = 1000* ethLog



ethVolSd = np.std(ethVol)
ethVolMean = np.mean(ethVol)
ethSd = np.std(ethLog)
ethMean = np.mean(ethLog)

# size = ethLog.size
# extremVolEth = []
# extremLogEth = []
# extremVolEthY = []
# extremLogEthY = []
# ethRecord = []
# ethBad = []
# periodeMax = 500
# nbRecords=0
# nbBad=0
# for i in range(size):
    # if (i> periodeMax):
        # if (ethPrice[i] == np.min(ethPrice[i-periodeMax:i+1])):
            # ethBad.append(i)
            # nbBad+=1
        # if (ethPrice[i] == np.max(ethPrice[i-periodeMax:i+1])):
            # ethRecord.append(i)
            # nbRecords+=1
    # if (np.abs(ethVol[i]-ethVolMean) > 2*ethVolSd):
        # extremVolEth.append(i)
        # extremVolEthY.append(ethVol[i])
    # if (np.abs(ethLog[i]-ethMean) > 2*ethSd):
        # extremLogEth.append(i)
        # extremLogEthY.append(ethLog[i])

# ethRecordY = np.zeros(nbRecords)
# ethBadY = np.zeros(nbBad)
# plt.figure(1)
# plt.subplot(2,1,1)
# plt.scatter(extremLogEth,extremLogEthY,marker='*', c='red')
# plt.scatter(ethRecord,ethRecordY,marker='+', c='green')
# plt.scatter(ethBad,ethBadY,marker='v', c='purple')
# plt.scatter(extremVolEth,extremVolEthY,marker='o',c='black')
# plt.subplot(2,1,2)
# plt.plot(ethPrice)
# plt.plot(ethLog)
# plt.plot(ethVol)
# plt.show()


## STRATEGY

money = 1000
ether = 5

nbTimes = ethPrice.size
initial_money = money + ether*ethPrice[0]
print 'TOTAL: ', initial_money

periodeMax = 200

buyTimes = []
sellTimes = []
portfolioMoney = np.zeros(nbTimes)
holdFolio = np.zeros(nbTimes)

fees = 0.26 / 100

for i in range(nbTimes):
    if (i> periodeMax):
        price = ethPrice[i]
        portfolioMoney[i] = money + price*ether
        holdFolio[i] = initial_money*price / ethPrice[0]
        pMax = np.min([800,int(7*ethVolSd*periodeMax / (ethVol[i]+ 0.000000001))])
        startPeriod= np.max([0,i-pMax])
        if (ethPrice[i] == np.min(ethPrice[startPeriod:i+1])):
            ethSell = ether *0.9
            ether -= ethSell
            money += ethSell * price*(1.0-fees)
            sellTimes.append(i)
        if (ethPrice[i] == np.max(ethPrice[startPeriod:i+1])):
            moneyBuy = money *0.9
            money -= moneyBuy
            ether += moneyBuy *(1.0-fees)/ price
            buyTimes.append(i)

print 'money: ', money
print 'ether: ', ether
print 'TOTAL: ', money + ether*ethPrice[nbTimes-1]
sellY = np.zeros(len(sellTimes))
buyY = np.zeros(len(buyTimes))
plt.figure(1)
plt.subplot(2,1,1)
plt.scatter(buyTimes,buyY,marker='+', c='green')
plt.scatter(sellTimes,sellY,marker='v', c='red')
plt.plot(portfolioMoney)
plt.plot(holdFolio)
plt.subplot(2,1,2)
plt.plot(ethPrice)
# plt.plot(ethVol)
plt.show()
