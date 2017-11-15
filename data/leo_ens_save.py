import numpy as np
import datetime
import matplotlib.pyplot as plt
import matplotlib.dates as md
import time
import sqlite3
import tensorflow as tf
from random import randint
import math

def alpha(tab):
    s= tab.size
    ans=np.zeros(s)
    for i in range(s-1):
        if (tab[i+1] >= tab[i]):
            k=0
            while (k <= i and tab[i+1]>=tab[i-k]):
                k +=1
            ans[i+1]=k

        if (tab[i+1] < tab[i]):
            k=0
            while (k <= i and tab[i+1]<=tab[i-k]):
                k +=1
            ans[i+1]=-k

    return ans


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
# 2 min

cursor = conn.cursor()


cursor.execute("SELECT Price,Volume,Time FROM ETHEUR")
eth = np.array(cursor.fetchall())

# cursor.execute("SELECT Price,Volume,Time FROM XBTEUR")
# eth = np.array(cursor.fetchall())
minWindowSize = 1

theTime = eth[:,2]
print 'min time ', np.min(theTime) # 1er janv 2017
print 'max time ', np.max(theTime) # 26 juin 2017
print 'total timestamp: ', theTime.size

timeWindow=[0.70,0.92]
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

alEth = alpha(ethPrice)
deltas = np.array([10,20,30,50,80,100,200,500,1000,1500])
nMAX  = np.zeros(deltas.size)
nMIN  = np.zeros(deltas.size)
for i in range(deltas.size):
    for k in alEth:
        if (k >= deltas[i]):
            nMAX[i] = nMAX[i] + 1
        if (k <= -deltas[i]):
            nMIN[i] = nMIN[i] + 1
plt.hist(alEth,range=[-1500,1500],bins=80)
plt.show()
plt.plot(deltas,nMAX)
plt.plot(deltas,nMIN)
plt.show()
## STRATEGY
# windows=np.array([30,150,200,300,350])
# windows=np.array([500,700,1000,1500,2000])
windows=np.array([1500])
maxWindow = np.max(windows)
nbWindow=windows.size

nbTimes = ethPrice.size
initial_money = 1000 + 5*ethPrice[maxWindow]
print 'INITIAL TIME: ', convertTimestamp(timeStampsPeriod[0])
print 'TOTAL: ', initial_money

periodeMax =50


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

corr=autocorrelation(ethLog,7) 
thres = np.std(corr)

tSell=[]
tBuy=[]

for i in range(nbTimes):
    if (i> maxWindow):
        price = ethPrice[i]
        portfolioMoney[i,:] = money + price*ether
        portfolioCash[i,:] = money
        holdFolio[i] = initial_money*price / ethPrice[maxWindow]
        # TEMPS CARAC
        if (ethPrice[i] == np.min(ethPrice[i-tempsCarac:i+1])):
            if (tMax > 0):
                deltaMin = i - tMax
                # print 'deltaMin : ',deltaMin
            tMin = i
        if (ethPrice[i] == np.max(ethPrice[i-tempsCarac:i+1])):
            if (tMin > 0):
                deltaMax = i -tMin
                # print 'deltaMax : ',deltaMax
            tMax = i

        for k in range(nbWindow):
            periodeMax  = windows[k]
            # if (deltaMin > 0  and deltaMax >0):
                # periodeMax = int(periodeMax*(deltaMin + deltaMax)/2000)
            periodeShort = np.max([int(periodeMax/4),1])
            periodeXShort = np.max([int(periodeMax/3),1])

            # STRATS
            if (ethPrice[i] == np.min(ethPrice[i-periodeMax:i+1]) and counter[k]==0):
                # Buy
                counter[k]=1
                # moneyBuy = money[k] *0.5
                # money[k] -= moneyBuy
                # ether[k] += moneyBuy* (1.0-fees) / price
            if (ethPrice[i] == np.max(ethPrice[i-periodeMax:i+1])):
                tMaxi[k] = i
                counter[k]=0
                # # SELL
                # nbMin[k] = nbMin[k] + 1
                # ethSell = ether[k] *0.5
                # ether[k] -= ethSell
                # money[k] += ethSell * price * (1.0-fees)
                # sellTimes.append(timeStampsPeriod[i])
            if (ethPrice[i] == np.max(ethPrice[i-periodeShort:i+1])):
                # Buy
                moneyBuy = money[k] *0.99
                money[k] -= moneyBuy
                ether[k] += moneyBuy* (1.0-fees) / price
                tBuy.append(i)
                # counter[k]=0
            if (np.abs(corr[i])> 3*thres):
                tMaxi[k] = i
            if (
                    (ethPrice[i] == np.min(ethPrice[i-periodeXShort:i+1]) and counter[k]==1)
                    # or 
                    # (ethPrice[i] == np.min(ethPrice[i-periodeXShort:i+1]))
                    # or
                    # (tMaxi[k]>0 and 
                        # (i-tMaxi[k])< 100 and ethPrice[i] == np.min(ethPrice[i-periodeXShort:i+1]))
                    ):
                # SELL
                ethSell = ether[k] *0.99
                ether[k] -= ethSell
                money[k] += ethSell * price * (1.0-fees)
                tSell.append(i)
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

tBuy=np.array(tBuy)
tSell=np.array(tSell)
for k in range(nbWindow):
    plt.plot(timeStampsPeriod,np.log(portfolioMoney[:,k]), label = str(windows[k]))
    plt.scatter(tBuy,6*np.ones(tBuy.size),marker='+', c='green')
    plt.scatter(tSell,6*np.ones(tSell.size),1,marker='v', c='red')
    plt.legend()

plt.plot(timeStampsPeriod,np.log(holdFolio),label='HOLDER')
plt.legend()
plt.title('From '+ convertTimestamp(np.min(theTime)) + ' to ' + convertTimestamp(np.max(theTime)) )

plt.subplot(2,1,2)
corr=autocorrelation(ethLog,7) 
# vol=volatilite(ethLog,7) 
plt.plot(timeStampsPeriod,corr)
# plt.plot(timeStampsPeriod,vol)
# plt.plot(maxTimes)
# plt.plot(timeStampsPeriod,holdFolio,label='HOLDER')
# for k in range(nbWindow):
    # plt.plot(timeStampsPeriod,portfolioCash[:,k], label = str(windows[k]))
    # plt.legend()
# plt.plot(timeStampsPeriod,ethPrice)
# plt.plot(ethVol)
plt.show()

print 'Windows',windows
print thres
# print 'NB_MIN',nbMin
# print 'NB_MAX',nbMax
