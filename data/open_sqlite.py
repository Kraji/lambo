import numpy as np
import sqlite3
execfile('box_making.py')
conn = sqlite3.connect('../../kraken.sqlite')

cursor = conn.cursor()

# ETCETH ETCXBT ETHEUR ETHGBP ETHUSD ETHXBT GNOETH GNOEUR GNOUSD GNOXBT LTCEUR LTCUSD LTCXBT XBTEUR XBTGBP XBTUSD ZECEUR ZECUSD ZECXBT
pairs = ['ETCETH', 'ETCXBT', 'ETHEUR', 'ETHGBP', 'ETHUSD', 'ETHXBT', 'GNOETH', 'GNOEUR', 'GNOUSD', 'GNOXBT', 'LTCEUR', 'LTCUSD', 'LTCXBT', 'XBTEUR', 'XBTGBP', 'XBTUSD', 'ZECEUR', 'ZECUSD', 'ZECXBT']


usedPairs = ['ETHEUR','XBTEUR','LTCEUR']

# 01/01/2017
# timeOrigin=1483228800
timeOrigin=1483229100
# 26/06/2017
timeFinal=1498435200

vwap_sqlite = sqlite3.connect('../../vwap.sqlite')

vwap_cursor = vwap_sqlite.cursor()

for pair in usedPairs:
    print pair
    vwap_cursor.execute('CREATE TABLE %s (Price real, Volume real, Time integer)' % pair)
    cursor.execute("SELECT Price,Volume,Time FROM %s_Trades WHERE TIME >= %s and TIME <= %s" % (pair,str(timeOrigin),str(timeFinal)))
    result = np.array(cursor.fetchall())
    vwap_pair = box_making(result,60,timeOrigin,timeFinal)
    (nRows, nCols) = vwap_pair.shape
    for i in range(nRows):
        vwap_cursor.execute("INSERT INTO %s VALUES (%f, %f, %i)" % (pair,vwap_pair[i,0],vwap_pair[i,1],int(vwap_pair[i,2])))
    vwap_sqlite.commit()


