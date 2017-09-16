import numpy as np

# data_input: price, volume, time
def box_making(data_input, delta_t, initial_time,final_time):

    dataShape = data_input.shape
    (nRows, nCols)= dataShape
    nb_data=nRows
    
    price=data_input[:,0]
    volume=data_input[:,1]
    time=data_input[:,2]
    
    # initial_time = data_input[0,2]
    # final_time =  data_input[nRows-1,2]
    
    time_interval = final_time - initial_time
    nb_bins = int(time_interval // delta_t +1)
    
    data_compressed=np.zeros((nb_bins,4))
    
    vwap = np.zeros(nb_bins)
    weights = np.zeros(nb_bins)
    time_stamp=initial_time+delta_t*np.arange(nb_bins)
    variance=np.zeros(nb_bins)

    for j in range(nb_data):
    	ind = int((time[j]-initial_time)//delta_t)
        if ind=>0:
    	   vwap[ind] += volume[j] * price[j]
    	   weights[ind] += volume[j]
    for k in range(len(vwap)):
    	if weights[k] > 0.00001:
            vwap[k] = vwap[k] / weights[k]
    	else:
    	    vwap[k] = vwap[k-1]
    
    for j in range(nb_data):
        ind = int((time[j]-initial_time)//delta_t)
        if ind=>0:
           variance[ind] += volume[j] * (price[j]-vwap[ind])**2
    for k in range(len(vwap)):
        if weights[k] > 0.00001:
            variance[k] = variance[k] / weights[k]
        else:
            variance[k] = variance[k-1]

    data_compressed[:,0]=vwap
    data_compressed[:,1]=weights
    data_compressed[:,2]=time_stamp
    data_compressed[:,3]=variance
    return data_compressed
