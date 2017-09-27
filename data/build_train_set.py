import numpy as np
import matplotlib.pyplot as plt
import sqlite3
import tensorflow as tf
from random import randint
import math
import keras
from keras.layers import Dense, Activation
from keras.models import Sequential


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
eth = eth[:-100000,:]

cursor.execute("SELECT Price,Volume,Time FROM XBTEUR")
btc = np.array(cursor.fetchall())
btc = btc[:-100000,:]

(size, p) = btc.shape
# plt.plot(btc[:,2],btc[:,0])
# plt.show()
minWindowSize = 5

ethPrice= av_group(eth[:,0],minWindowSize)
btcPrice= av_group(btc[:,0],minWindowSize)
size = ethPrice.size

ethLog = np.log(ethPrice[1:]) - np.log(ethPrice[:(size-1)]) 
btcLog = np.log(btcPrice[1:]) - np.log(btcPrice[:(size-1)]) 
ethLog = 1000* ethLog
btcLog = 1000* btcLog

windowSizes=np.array([1,4,20])
windowQuantity=np.array([3,3,1])
nbWindow = windowSizes.size
inputSize = np.sum(windowQuantity)
buf = np.max(windowSizes*windowQuantity)

# Build train set
def build_train_set(tab):
    ans = np.zeros([tab.size-buf,inputSize+1])
    for i in range(tab.size - buf):
        nInput = 0
        inputVector = np.zeros(inputSize)
        # Loop over window sizes
        for nW in range(nbWindow):
            # Loop over the number of window of size windowSizes[nW]
            for j in range(windowQuantity[nW]):
                # Final index of the window
                indexEnd = i + buf - j*windowSizes[nW]
                windowMean = np.mean(tab[(indexEnd-windowSizes[nW]):indexEnd])
                inputVector[nInput]=windowMean
                nInput+=1
        outputValue=np.mean(tab[(i + buf) : (i + buf + 3)])
        ans[i,:-1]=inputVector
        ans[i,inputSize]=outputValue
    return ans

def random_batch(train_set, batch_size):
    (nR, nC) = train_set.shape
    ans = np.zeros([batch_size, nC])
    for i in range(batch_size):
        r= randint(0,nR-1)
        ans[i,:] = train_set[r,:]
    return ans


eth_train_set = build_train_set(ethLog)
btc_train_set = build_train_set(btcLog)

inputSize = 2*inputSize
train_set = np.concatenate((btc_train_set[:,:-1],eth_train_set), axis=1)

