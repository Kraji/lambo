import numpy as np

def box_making(data_input, delta_t, initial_transaction):

    dataShape = data_input.shape
    (nRows, nCols)= dataShape
    nb_data=nRows
    
    price=data_input[:,0]
    volume=data_input[:,1]
    time=data_input[:,2]
    
    initial_time = data_input[init_transaction,2]
    final_time =  data_input[nRows-1,2]
    
    time_interval = final_time - initial_time
    nb_bins = int(time_interval // delta_t +1)
    
    data_compressed=np.zeros((nb_bins,3))
    
    vwap = np.zeros(nb_bins)
    weights = np.zeros(nb_bins)
    time_stamp=initial_time+delta_t*np.arange(nb_bins)


    for j in range(init_ind,nb_data):
    	ind = int((time[j]-initial_time)//delta_t)
    	vwap[ind] += volume[j] * price[j]
    	weights[ind] += volume[j]
    for k in range(len(vwap)):
    	if weights[k] > 0.0001:
            vwap[k] = vwap[k] / weights[k]
    	else:
    	    vwap[k] = vwap[k-1]

    data_compressed[:,0]=vwap
    data_compressed[:,1]=weights
    data_compressed[:,2]=time_stamp
    return data_compressed
