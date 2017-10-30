import numpy as np
import sqlite3
import cPickle
conn = sqlite3.connect('../../krajbox.sqlite')

cursor = conn.cursor()

#open cpickle
f = open('compressed_EthEur3.p','rb')
A = cPickle.load(f)
f.close()
print A.shape
rows, cols = A.shape
print A[0,:]
timeOrigin=1483229100 
# premier janvier 2017

cursor.execute('CREATE TABLE ETHEUR (Price real, Volume real, Time integer)')
nbRow=0
for i in range(rows):
    if (A[i,2]>= timeOrigin):
        # print 'insert'
        nbRow +=1
        cursor.execute("INSERT INTO ETHEUR VALUES (%f, %f, %i)" % (A[i,0],A[i,1],int(A[i,2])))

conn.commit()

print 'done: ', nbRow

