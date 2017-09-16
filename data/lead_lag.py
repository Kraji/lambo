import numpy as np

import tensorflow as tf
import matplotlib.pyplot as plt

import json
# execfile('api.py')

# myApi = API()

# READ DATA
datasetName = 'night_collect'
with open(datasetName + '_ETH.json') as data_file:
    ethData = json.load(data_file)
with open(datasetName + '_BTC.json') as data_file:
    btcData = json.load(data_file)

nbPoints = len(ethData)
print nbPoints

btcData = np.array(btcData)
ethData = np.array(ethData)
# 0: timestamp
# 6: price

timeBtc = btcData[:,0]
timeEth = ethData[:,0]
priceBtc = btcData[:,6]
priceEth = ethData[:,6]

nb_data=nbPoints
init_ind=0
initial_time = timeBtc[0]
final_time =  timeBtc[nbPoints-1]

volume=np.zeros(nbPoints) + 1
time=timeBtc

#vwap over time interval t
delta_t = 180
# init_ind = 999 * (nb_data / 1000)
# initial_time, final_time = time[init_ind], time[nb_data-1]
time_interval = final_time - initial_time
nb_bins = int(time_interval // delta_t +1)
boxBtc = np.zeros(nb_bins)
boxEth = np.zeros(nb_bins)
weights = np.zeros(nb_bins)
for j in range(init_ind,nb_data):
    ind = int((time[j]-initial_time)//delta_t)
    boxBtc[ind] += volume[j] * priceBtc[j]
    boxEth[ind] += volume[j] * priceEth[j]
    weights[ind] += volume[j]
for k in range(len(boxBtc)):
    if weights[k] > 0.0001:
        boxBtc[k] = boxBtc[k] / weights[k]
        boxEth[k] = boxEth[k] / weights[k]
    else:
        boxBtc[k] = boxBtc[k-1]

print(nb_bins)

# plt.plot(weights)
# plt.show()
#LOG RETURNS
logEth = np.log(boxEth[1:]) - np.log(boxEth[:nb_bins-1])
logBtc = np.log(boxBtc[1:]) - np.log(boxBtc[:nb_bins-1])

# plt.plot(logBtc)
# plt.show()
# plt.plot(logEth)
# plt.show()

bitEth = (logEth > 0.002)
# plt.plot(bitEth)
# plt.show()

execfile('ctw.py')
alg = ctw_algorithm(bitEth,2,10)
proba = alg[0][1,:]
print proba.shape, bitEth.shape
plt.plot(bitEth[10:192])
plt.plot(proba)
plt.show()

# LL
# deltaAmp = 8
# cov = np.zeros(2*deltaAmp + 1)
# x = range(-deltaAmp,deltaAmp+1)

# for delta in x:
    # for i in range(deltaAmp,nb_bins-deltaAmp-1):
        # cov[delta]+=logEth[i]*logBtc[i+delta]

# plt.plot(x,cov)
# plt.show()
