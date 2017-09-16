import numpy as np
import matplotlib.pyplot as plt
import sqlite3
execfile('box_making.py')
conn = sqlite3.connect('../../vwap.sqlite')

cursor = conn.cursor()

# ETCETH ETCXBT ETHEUR ETHGBP ETHUSD ETHXBT GNOETH GNOEUR GNOUSD GNOXBT LTCEUR LTCUSD LTCXBT XBTEUR XBTGBP XBTUSD ZECEUR ZECUSD ZECXBT
pairs = ['ETCETH', 'ETCXBT', 'ETHEUR', 'ETHGBP', 'ETHUSD', 'ETHXBT', 'GNOETH', 'GNOEUR', 'GNOUSD', 'GNOXBT', 'LTCEUR', 'LTCUSD', 'LTCXBT', 'XBTEUR', 'XBTGBP', 'XBTUSD', 'ZECEUR', 'ZECUSD', 'ZECXBT']


usedPairs = ['ETHEUR','XBTEUR','LTCEUR']

# 01/01/2017
# timeOrigin=1483228800
timeOrigin=1483229100
# 26/06/2017
timeFinal=1498435200

cursor.execute("SELECT Price,Volume,Time FROM ETH")
eth = np.array(cursor.fetchall())

cursor.execute("SELECT Price,Volume,Time FROM BTC")
btc = np.array(cursor.fetchall())

