import numpy as np
import matplotlib.pyplot as plt
execfile('ctw.py')

f = open('compressed_EthEur.p','rb')
A = cPickle.load(f)
f.close()

boxEth=A[:,0]

#LOG RETURNS
logEth = np.log(boxEth[1:]) - np.log(boxEth[:nb_bins-1])

bitEth = (logEth > 0.002)

alg = ctw_algorithm(bitEth,2,10)
proba = alg[0][1,:]
print proba.shape, bitEth.shape
plt.plot(bitEth[190010:192010])
plt.plot(proba[190000:192000])

plt.show(block=False)
raw_input("<Hit Enter To Close>")
plt.close()

# LL
# deltaAmp = 8
# cov = np.zeros(2*deltaAmp + 1)
# x = range(-deltaAmp,deltaAmp+1)

# for delta in x:
    # for i in range(deltaAmp,nb_bins-deltaAmp-1):
        # cov[delta]+=logEth[i]*logBtc[i+delta]

# plt.plot(x,cov)
# plt.show()
