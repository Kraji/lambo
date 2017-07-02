import numpy as np
from numpy import dot
from math import floor
def ctw_update(countTree, betaTree, eta, index, xt, alpha):
	#POTENTIAL PROBLEM WITH 'INDEX'
	Nx = len(eta) + 1 
	pw = np.append(eta, 1)
	pw = pw / np.sum(pw)
	pe = (countTree[:, index] + 0.5) / (np.sum(countTree[:, index]) + Nx / 2.)
	temp = betaTree[index]
	if temp < 1000: 
		eta = (alpha * temp * pe[:Nx-1] + (1-alpha) * pw[:Nx-1])/(alpha*temp*pe[Nx-1] + (1-alpha)*pw[Nx-1])
	else:
		eta = (alpha * pe[:Nx-1] + (1-alpha) * pw[:Nx-1]/temp)/(alpha*pe[Nx-1] + (1-alpha)*pw[Nx-1]/temp)
	countTree[xt, index] = countTree[xt, index] + 1
	betaTree[index] = betaTree[index] * pe[xt] / pw[xt]

	return countTree, betaTree, eta

def ctw_algorithm(x, Nx, D):
	n = len(x)
	countTree = np.zeros((Nx, (Nx**(D+1))/(Nx-1)))
	betaTree = np.ones(Nx**(D+1)/(Nx-1))
	Px_record = np.zeros((Nx, n-D))
	indexweight = np.array([Nx**k for k in range(D)])
	offset = (Nx**D - 1) / (Nx-1) + 1

	for i in range(D, n): #NOT SURE ABOUT THE INDEXES
		context = x[i-D:i]
		leafindex = context.dot(indexweight) + offset
		xt = int(x[i])
		eta = (countTree[:Nx-1, leafindex-1] + 0.5) / (countTree[Nx-1, leafindex-1] + 0.5)
		countTree[xt, leafindex-1] = countTree[xt, leafindex-1] + 1
		node =floor((leafindex+Nx-2)/Nx)
		while node != 0:
			node = int(node)
			countTree, betaTree, eta = ctw_update(countTree, betaTree, eta, node, xt, 0.5)
			node =floor((node+Nx-2.)/Nx)
		eta_sum = np.sum(eta) + 1.
		Px_record[:, i-D] = np.array([float(eta), 1]) / eta_sum
	return Px_record

x = np.random.choice([0,1], size=100)
D = 5

Px = ctw_algorithm(x, 2, D)
print Px[:,-5:]




