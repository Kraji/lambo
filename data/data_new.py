import numpy as np
import cPickle
import matplotlib.pyplot as plt

# Open data
f = open('EthEur.p','rb')
A = cPickle.load(f)
dataShape = A.shape
f.close()

(nRows, nCols)= dataShape
print A[nRows-1,:]

nb_data=nRows
init_ind=100
initial_time = A[init_ind,2]#1438945790
final_time =  A[nRows-1,2]

price=A[:,0]
volume=A[:,1]
time=A[:,2]

#vwap over time interval t
delta_t = 60
# init_ind = 999 * (nb_data / 1000)
# initial_time, final_time = time[init_ind], time[nb_data-1]
time_interval = final_time - initial_time
nb_bins = int(time_interval // delta_t +1)
vwap = np.zeros(nb_bins)
weights = np.zeros(nb_bins)
for j in range(init_ind,nb_data):
    ind = int((time[j]-initial_time)//delta_t)
    vwap[ind] += volume[j] * price[j]
    weights[ind] += volume[j]
for k in range(len(vwap)):
    if weights[k] > 0.0001:
        vwap[k] = vwap[k] / weights[k]
    else:
        vwap[k] = vwap[k-1]

# plt.plot(range(nb_bins), vwap)
# plt.show()
plt.plot(volume[10000:11000])
plt.show()
plt.plot(vwap[10000:11000])
plt.show()

#log returns
y = np.log(vwap[1:]) - np.log(vwap[:nb_bins-1])
plt.plot(y[10000:11000])
plt.show()
#log returns squared
y2 = np.square(y)
