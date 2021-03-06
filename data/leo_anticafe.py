import numpy as np
import datetime
import matplotlib.pyplot as plt
import matplotlib.dates as md
import time
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

def autocorrelation(tab,window):
    ans = np.zeros(tab.size)
    delta = tab[1:] - tab[:-1]
    corr = np.append([0,0],delta[1:]*delta[:-1])
    for i in range(tab.size - window):
        ans[i+window]= np.mean(corr[i:(i+window+1)])
    return ans
def volatilite(tab,window):
    ans = np.zeros(tab.size)
    delta = tab[1:] - tab[:-1]
    corr = np.append([0],np.square(delta))
    for i in range(tab.size - window):
        ans[i+window]= np.mean(corr[i:(i+window+1)])
    return ans

def convertTimestamp(stamp):
    return datetime.datetime.fromtimestamp(stamp).strftime('%Y-%m-%d')

def miniMaxPeriods(tab):
    ans = np.zeros(tab.size)
    for i in range(tab.size):
        kMax=0
        while (tab[i-kMax] <= tab[i] and (i-kMax) > 0):
            kMax += 1
        kMin=0
        while (tab[i-kMin] >= tab[i] and (i-kMin) > 0):
            kMin += 1

        if (kMin >= kMax):
            ans[i]=-kMin
        else:
            ans[i]=kMax
    return ans

        
        

# conn = sqlite3.connect('../../vwap.sqlite')
conn = sqlite3.connect('../../krajbox.sqlite')

cursor = conn.cursor()


cursor.execute("SELECT Price,Volume,Time FROM ETHEUR")
eth = np.array(cursor.fetchall())

# cursor.execute("SELECT Price,Volume,Time FROM XBTEUR")
# btc = np.array(cursor.fetchall())
minWindowSize = 1

theTime = eth[:,2]
print 'min time ', np.min(theTime) # 1er janv 2017
print 'max time ', np.max(theTime) # 26 juin 2017
print 'total timestamp: ', theTime.size

timeWindow=[0.69,0.995]
indexStart = int(timeWindow[0]*theTime.size)
indexStop = int(timeWindow[1]*theTime.size)
# nbPoints = int(np.floor(theTime.size / 3))


# theTime = theTime[-nbPoints:]
theTime = theTime[indexStart:indexStop]
print 'min time ', convertTimestamp(np.min(theTime)) # 1er janv 2017
print 'max time ', convertTimestamp(np.max(theTime)) # 26 juin 2017

# ethPrice= av_group(eth[-nbPoints:,0],minWindowSize)
ethPrice= av_group(eth[indexStart:indexStop,0],minWindowSize)
# btcPrice,btcVol= av_group_vol(btc[-nbPoints:,0],minWindowSize,1)
size = ethPrice.size
print size
timeStampsPeriod = np.min(theTime) + minWindowSize*120*np.array(range(size))

ethLog = np.log(ethPrice)
## STRATEGY

nbTimes = ethPrice.size
initial_money = 1000 + 5*ethPrice[maxWindow]
print 'INITIAL TIME: ', convertTimestamp(timeStampsPeriod[0])
print 'TOTAL: ', initial_money

periodeMax =50

# windows=np.array([30,150,200,300,350])
windows=np.array([500,700,1000,1500,2000])
maxWindow = np.max(windows)
nbWindow=windows.size

portfolioMoney = initial_money*np.ones(shape=(nbTimes,nbWindow))
portfolioCash = initial_money*np.ones(shape=(nbTimes,nbWindow))
holdFolio = initial_money*np.ones(nbTimes)

money = 1000 * np.ones(nbWindow)
ether = 5* np.ones(nbWindow)

fees = 0.16 / 100
# fees = 0.0
counter = np.zeros(nbWindow)

tempsCarac = 1200
tMax = 0
tMin = 0
deltaMin=0
deltaMax=0
tMaxi = np.zeros(nbWindow)
tMini = np.zeros(nbWindow)

for i in range(nbTimes):
    if (i> maxWindow):
        price = ethPrice[i]
        portfolioMoney[i,:] = money + price*ether
        portfolioCash[i,:] = money
        holdFolio[i] = initial_money*price / ethPrice[maxWindow]
        for k in range(nbWindow):
            periodeLong  = windows[k]
            # if (deltaMin > 0  and deltaMax >0):
                # periodeMax = int(periodeMax*(deltaMin + deltaMax)/2000)
            periodeMiddle = np.max([int(periodeMax/3),1])
            periodeShort = np.max([int(periodeMax/10),1])

            # STRATS
            if (ethPrice[i] == np.min(ethPrice[i-periodeLong:i+1])):
                # Buy
                tMini[k]=i
            if (ethPrice[i] == np.max(ethPrice[i-periodeLong:i+1])):
                tMaxi[k] = i
            
            if (ethPrice[i] == np.max(ethPrice[i-periodeShort:i+1]) and (i-tMini[k])< periodeMiddle):
                # Buy
                moneyBuy = money[k] *0.5
                money[k] -= moneyBuy
                ether[k] += moneyBuy* (1.0-fees) / price
                # counter[k]=0
            elif (ethPrice[i] == np.min(ethPrice[i-periodeShort:i+1]) and (i-tMaxi[k])< periodeMiddle):
                # SELL
                ethSell = ether[k] *0.9
                ether[k] -= ethSell
                money[k] += ethSell * price * (1.0-fees)
                # sellTimes.append(timeStampsPeriod[i])
            # else:
                # counter[k]=0

                # buyTimes.append(timeStampsPeriod[i])

print 'FINAL TIME: ', convertTimestamp(timeStampsPeriod[nbTimes-1])
for k in range(nbWindow):
    print 'STRATEGY PERIOD: ', windows[k]
    # print 'money: ', money
    # print 'ether: ', ether
    print 'TOTAL: ', money[k] + ether[k]*ethPrice[nbTimes-1]
    print ''

print 'HOLDER'
print 'TOTAL : ', holdFolio[-1]

# maxTimes = miniMaxPeriods(ethPrice)
# plt.plot(maxTimes)
# plt.show()
timeStampsPeriod = timeStampsPeriod - timeStampsPeriod[0]
timeStampsPeriod=range(timeStampsPeriod.size)
# sellY = np.zeros(len(sellTimes))
# buyY = np.zeros(len(buyTimes))
plt.figure(1)
plt.subplot(2,1,1)
# plt.scatter(buyTimes,buyY,marker='+', c='green')
# plt.scatter(sellTimes,sellY,marker='v', c='red')

for k in range(nbWindow):
    plt.plot(timeStampsPeriod,np.log(portfolioMoney[:,k]), label = str(windows[k]))
    plt.legend()

plt.plot(timeStampsPeriod,np.log(holdFolio),label='HOLDER')
plt.legend()
plt.title('From '+ convertTimestamp(np.min(theTime)) + ' to ' + convertTimestamp(np.max(theTime)) )

plt.subplot(2,1,2)
corr=autocorrelation(ethLog,7) 
vol=volatilite(ethLog,7) 
plt.plot(timeStampsPeriod,corr)
plt.plot(timeStampsPeriod,vol)
# plt.plot(maxTimes)
# plt.plot(timeStampsPeriod,holdFolio,label='HOLDER')
# for k in range(nbWindow):
    # plt.plot(timeStampsPeriod,portfolioCash[:,k], label = str(windows[k]))
    # plt.legend()
# plt.plot(timeStampsPeriod,ethPrice)
# plt.plot(ethVol)
plt.show()

print 'Windows',windows
# print 'NB_MIN',nbMin
# print 'NB_MAX',nbMax
