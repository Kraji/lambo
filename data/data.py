import krakenex
import numpy as np
import matplotlib.pyplot as plt
import time
import cPickle
import progressbar

# load OHLC data from Kraken for ETHEUR

def ohlc(k, currency):
	res = k.query_public('OHLC', {'pair': 'currency', 'interval': 1})
	data = res['result']['currency']
	nb_data = len(data)
	open_values = np.array([data[i][1] for i in range(nb_data)], dtype=float)
	closing_values = np.array([data[i][4] for i in range(nb_data)], dtype=float)
	lowest_values = np.array([data[i][3] for i in range(nb_data)], dtype=float)
	highest_values = np.array([data[i][2] for i in range(nb_data)], dtype=float)
	av_values = np.array([data[i][5] for i in range(nb_data)], dtype=float)
	data_bin = np.array([(closing_values[i] - open_values[i] > 0.) for i in range(nb_data)], dtype=int)

	return data,nb_data, open_values, closing_values, closing_values, lowest_values, highest_values, av_values, data_bin

# load all trade data from Kraken for ETHEUR

def trade_data(k, currency, lastid):
	res=k.query_public('Trades',{'pair':currency,'since':lastid})
	#last= np.array(res['result']['last']).astype(float)
	last= res['result']['last']
	#np.savetxt('LastID.txt',[last])
	data = np.array(res['result'][currency])[:,:3].astype(float)

	return last, data

# load the id of the last transaction

def last_transaction_id(k, currency):
	res=k.query_public('Trades',{'pair':currency})
	last_now=res['result']['last']

	return last_now


k=krakenex.API()
currency='XETHZEUR'

f = open('EthEur.p','rb')
A = cPickle.load(f)
print 'Shape of the transaction matrix : '+ str(A.shape)
f.close()

f=open('LastID','rb')
last_id=f.read().decode('utf8')
f.close()
print 'ID of the last saved transaction : '+ last_id
#print type(last_id)

starttime=time.time()
i=0

last_now=last_transaction_id(k, currency)
print 'ID of the last transation on the market : '+ last_now

time.sleep(1. - ((time.time() - starttime) % 1.))

bar = progressbar.ProgressBar(maxval=200, \
    widgets=[progressbar.Bar('=', '[', ']'), ' ', progressbar.Percentage()])
bar.start()

while last_id<last_now or i<200:
    last_id, data= trade_data(k,currency,last_id)

    f = open('EthEur.p','rb')
    A = cPickle.load(f)
    f.close()
    
    f = open('EthEur.p','wb')
    A=np.concatenate((A,data),axis=0)
    cPickle.dump(A,f)
    f.close()

    f = open('LastID','wb')
    f.write(last_id)
    f.close()

    bar.update(i+1)
    i+=1
    time.sleep(3. - ((time.time() - starttime) % 3.))

bar.finish()

f = open('LastID','wb')
f.write(last_id)
f.close()

f = open('EthEur.p','rb')
A = cPickle.load(f)
A.shape
f.close()