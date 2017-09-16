import numpy as np
import matplotlib.pyplot as plt
import sqlite3
import tensorflow as tf
from random import randint

def av_group(tab,n):
    s = tab.size
    new_size = s / n
    ans = np.zeros(new_size)
    for i in range(new_size):
        ans[i] = np.mean(tab[i*n:(i+1)*n])
    return ans

execfile('ctw.py')
conn = sqlite3.connect('../../vwap.sqlite')

cursor = conn.cursor()


cursor.execute("SELECT Price,Volume,Time FROM ETHEUR")
eth = np.array(cursor.fetchall())

cursor.execute("SELECT Price,Volume,Time FROM XBTEUR")
btc = np.array(cursor.fetchall())

(size, p) = btc.shape
# plt.plot(btc[:,2],btc[:,0])
# plt.show()
window=5
ethPrice= av_group(eth[:,0],window)
btcPrice= av_group(btc[:,0],window)
size = ethPrice.size

ethLog = np.log(ethPrice[1:]) - np.log(ethPrice[:(size-1)]) 
btcLog = np.log(btcPrice[1:]) - np.log(btcPrice[:(size-1)]) 
# plt.hist(ethLog,170,normed=1, range=[-0.009,0.009])
# plt.show()
ethLog = 1000* ethLog


def build_train_set(tab, buf):
    ans = np.zeros([tab.size-buf,buf+1])
    for i in range(tab.size - buf):
        ans[i,:-1]=tab[i:(i+buf)]
        ans[i,buf]=tab[i+buf]
    return ans

def random_batch(train_set, batch_size):
    (nR, nC) = train_set.shape
    ans = np.zeros([batch_size, nC])
    for i in range(batch_size):
        r= randint(0,nC-1)
        ans[i,:] = train_set[r,:]
    return ans

buf=3
train_set = build_train_set(ethLog,buf)

W = tf.Variable(tf.ones([buf,1])) / float(buf)
b = tf.Variable(tf.ones([1]))


x = tf.placeholder(tf.float32, [None,buf])
y = tf.placeholder(tf.float32, [None,1])

# MODEL
model = tf.matmul(x,W) + b

# LOSS
objective_function = tf.reduce_mean(tf.square(y - model))

mean, var = tf.nn.moments(y, axes=[0])
error = tf.reduce_mean(tf.square(y - model))
dummy = var

# ALGO
optimizer = tf.train.GradientDescentOptimizer(0.01)
train = optimizer.minimize(objective_function)

# INIT SESSION
init = tf.global_variables_initializer()
session = tf.Session()
session.run(init)

for nBatch in range(50):
    batch = random_batch(train_set,50)
    batch_x = batch[:,:-1]
    batch_y = batch[:,-1].reshape(50,1)
    session.run(train, feed_dict={x: batch_x, y: batch_y})

batch = random_batch(train_set,500)
batch_x = batch[:,:-1]
batch_y = batch[:,-1].reshape(500,1)
error, dummy, W, b , model= session.run([error,dummy, W, b ,model], feed_dict={x: batch_x, y: batch_y})
print error
print dummy
print W
print b
