import krakenex
import numpy as np
import matplotlib.pyplot as plt
import time
import cPickle
import progressbar
import sys, select, os
import datetime

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

limit=1000

bar = progressbar.ProgressBar(maxval=limit, widgets=[progressbar.Bar('=', '[', ']'), ' ', progressbar.Counter()])
bar.start()

f = open('EthEur.p','rb')
A = cPickle.load(f)
f.close()

while last_id<last_now and i<limit:
    try:
        last_id, data= trade_data(k,currency,last_id)

        A=np.concatenate((A,data),axis=0)
        #print('Transaction at time : '+datetime.datetime.fromtimestamp(int(str(last_id)[:10])).strftime('%Y-%m-%d %H:%M:%S'))

        bar.update(i+1)
        i+=1
        #time.sleep(2. - ((time.time() - starttime) % 2.))
        time.sleep(0.5)

    except KeyError as e:
        if e.message == 'result':
            continue

    except ValueError as e:
        if e.message == 'No JSON object could be decoded':
            continue

    if sys.stdin in select.select([sys.stdin], [], [], 0)[0]:
        line = raw_input()
        break

bar.finish()
f = open('EthEur.p','wb')
cPickle.dump(A,f)
f.close()

f = open('LastID','wb')
f.write(last_id)
f.close()

print 'ID of the last saved transaction : '+ last_id
print('Date of the last saved transaction : '+datetime.datetime.fromtimestamp(int(str(last_id)[:10])).strftime('%Y-%m-%d %H:%M:%S'))
print('\n')

# f = open('LastID','wb')
# f.write(last_id)
# f.close()

# f = open('EthEur.p','rb')
# A = cPickle.load(f)
# A.shape
# f.close()