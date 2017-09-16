import numpy as np
import sqlite3
conn = sqlite3.connect('../../kraken.sqlite')

cursor = conn.cursor()

cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
print(cursor.fetchall())

cursor.execute("SELECT Price,Volume,Time FROM ETHEUR_Trades LIMIT 5")
result = cursor.fetchall()

res_array=np.array(result)
print type(result)
print res_array

# Available Pairs
# ETCETH ETCXBT ETHEUR ETHGBP ETHUSD ETHXBT GNOETH GNOEUR GNOUSD GNOXBT LTCEUR LTCUSD LTCXBT XBTEUR XBTGBP XBTUSD ZECEUR ZECUSD ZECXBT
pairs = ['ETCETH', 'ETCXBT', 'ETHEUR', 'ETHGBP', 'ETHUSD', 'ETHXBT', 'GNOETH', 'GNOEUR', 'GNOUSD', 'GNOXBT', 'LTCEUR', 'LTCUSD', 'LTCXBT', 'XBTEUR', 'XBTGBP', 'XBTUSD', 'ZECEUR', 'ZECUSD', 'ZECXBT']


for p in pairs:
    print p
    cursor.execute("SELECT COUNT(*) FROM %s_Trades" % p)
    print cursor.fetchall()

usedPairs = ['ETHEUR','XBTEUR','LTCEUR']

# 01/01/2017
timeOrigin=1483228800

vwap_sqlite = sqlite3.connect('../../vwap.sqlite')

vwap_cursor = vwap_sqlite.cursor()

# Create table
vwap_cursor.execute('CREATE TABLE %s (Price real, Volume real, Time integer)' % pair)

# Insert a row of data
vwap_cursor.execute("INSERT INTO %s VALUES (%f, %f, %i)" % (pair,))

for pair in usedPairs:
    cursor.execute("SELECT Price,Volume,Time FROM %s_Trades WHERE TIME >= %s" % (pair,str(timeOrigin)))
    result = np.array(cursor.fetchall())
    

