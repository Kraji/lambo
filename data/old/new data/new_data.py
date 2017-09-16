import krakenex
import numpy as np
import matplotlib.pyplot as plt
import time
import cPickle
import progressbar
import sys, select, os
import datetime


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

# load the id of the last transaction on the market

def last_transaction_id(k, currency):
	res=k.query_public('Trades',{'pair':currency})
	last_now=res['result']['last']

	return last_now


k=krakenex.API()
currency='XETHZEUR'

# Opening of the trade register or initialization 

try:
    f = open('EthEur.p','rb')
    A = cPickle.load(f)
    print 'Shape of the transaction matrix : '+ str(A.shape)
    f.close()
except IOError:
    last_id, data= trade_data(k,currency,'0')
    f=open('EthEur.p','wb')
    cPickle.dump(data,f)
    f.close()
    f = open('EthEur.p','rb')
    A = cPickle.load(f)
    print 'Register of transaction just created and initiated'
    f.close()

# Reading of the last transaction ID of the register or initialization

try:
    f=open('LastID','rb')
    last_id=f.read().decode('utf8')	
    f.close()
except IOError:
    f=open('LastID','wb')
    f.write(last_id)
    f.close()
print 'ID of the last saved transaction : '+ last_id
print('Date of the last saved transaction : '+datetime.datetime.fromtimestamp(int(str(last_id)[:10])).strftime('%Y-%m-%d %H:%M:%S'))
print('\n')

starttime=time.time()
i=0

last_now=last_transaction_id(k, currency)
print 'ID of the last transation on the market : '+ last_now
print('Date of the last transaction on the market : '+datetime.datetime.fromtimestamp(int(str(last_now)[:10])).strftime('%Y-%m-%d %H:%M:%S'))
print('\n')

time.sleep(1. - ((time.time() - starttime) % 1.))

bar = progressbar.ProgressBar(maxval=100, widgets=[progressbar.Bar('=', '[', ']'), ' ', progressbar.Counter()])
bar.start()

while last_id<last_now and i<100:
    try:
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

        #print('Transaction at time : '+datetime.datetime.fromtimestamp(int(str(last_id)[:10])).strftime('%Y-%m-%d %H:%M:%S'))

        bar.update(i+1)
        i+=1
        #time.sleep(2. - ((time.time() - starttime) % 2.))
        time.sleep(1.)

    except ValueError as e:
        if e.message == 'No JSON object could be decoded':
            continue
    if sys.stdin in select.select([sys.stdin], [], [], 0)[0]:
        line = raw_input()
        break

bar.finish()

# f = open('LastID','wb')
# f.write(last_id)
# f.close()

# f = open('EthEur.p','rb')
# A = cPickle.load(f)
# A.shape
# f.close()