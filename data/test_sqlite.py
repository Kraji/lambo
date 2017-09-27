import numpy as np
import matplotlib.pyplot as plt
import sqlite3
import tensorflow as tf
from random import randint
import math

def av_group(tab,n):
    s = tab.size
    new_size = s / n
    ans = np.zeros(new_size)
    for i in range(new_size):
        ans[i] = np.mean(tab[i*n:(i+1)*n])
    return ans

conn = sqlite3.connect('../../vwap.sqlite')

cursor = conn.cursor()


cursor.execute("SELECT Price,Volume,Time FROM ETHEUR")
eth = np.array(cursor.fetchall())

cursor.execute("SELECT Price,Volume,Time FROM XBTEUR")
btc = np.array(cursor.fetchall())

(size, p) = btc.shape
# plt.plot(btc[:,2],btc[:,0])
# plt.show()
minWindowSize = 3

ethPrice= av_group(eth[:,0],minWindowSize)
btcPrice= av_group(btc[:,0],minWindowSize)
size = ethPrice.size

ethLog = np.log(ethPrice[1:]) - np.log(ethPrice[:(size-1)]) 
btcLog = np.log(btcPrice[1:]) - np.log(btcPrice[:(size-1)]) 
ethLog = 1000* ethLog

windowSizes=np.array([1,4,20])
windowQuantity=np.array([3,3,3])
nbWindow = windowSizes.size
inputSize = np.sum(windowQuantity)
buf = np.max(windowSizes*windowQuantity)

# Build train set
def build_train_set(tab):
    ans = np.zeros([tab.size-buf,inputSize+1])
    for i in range(tab.size - buf):
        nInput = 0
        inputVector = np.zeros(inputSize)
        # Loop over window sizes
        for nW in range(nbWindow):
            # Loop over the number of window of size windowSizes[nW]
            for j in range(windowQuantity[nW]):
                # Final index of the window
                indexEnd = i + buf - j*windowSizes[nW]
                windowMean = np.mean(tab[(indexEnd-windowSizes[nW]):indexEnd])
                inputVector[nInput]=windowMean
                nInput+=1
        outputValue=np.mean(tab[(i + buf) : (i + buf + 3)])
        ans[i,:-1]=inputVector
        ans[i,inputSize]=outputValue
    return ans

def random_batch(train_set, batch_size):
    (nR, nC) = train_set.shape
    ans = np.zeros([batch_size, nC])
    for i in range(batch_size):
        r= randint(0,nR-1)
        ans[i,:] = train_set[r,:]
    return ans

train_set = build_train_set(ethLog)

W = tf.Variable(tf.ones([inputSize,1])) / float(inputSize)
b = tf.Variable(tf.ones([1]))

# VARIABLES
x = tf.placeholder(tf.float32, [None,inputSize])
y = tf.placeholder(tf.float32, [None,1])

n_hidden_1=10
n_hidden_2=10
hidden1_units=10
# HIDDEN LAYER
weights1 = tf.Variable( tf.truncated_normal([inputSize, hidden1_units], stddev=1.0 / math.sqrt(float(inputSize))))
biases1 = tf.Variable(tf.zeros([hidden1_units]))
hidden1 = tf.nn.relu(tf.matmul(x, weights1) + biases1)
# OUTPUT LAYER
weights2 = tf.Variable( tf.truncated_normal([hidden1_units,1], stddev=1.0 / math.sqrt(float(hidden1_units))))
biases2 = tf.Variable(tf.zeros([1]))
model = tf.matmul(hidden1, weights2) + biases2

# Hidden fully connected layer with 256 neurons
# layer_1 = tf.layers.dense(x, n_hidden_1,activation=tf.nn.relu)
# Hidden fully connected layer with 256 neurons
# layer_2 = tf.layers.dense(layer_1, n_hidden_2,activation=tf.nn.relu)
# Output fully connected layer with a neuron for each class
# model = tf.layers.dense(layer_1, 1)

# MODEL
# model = tf.matmul(x,W) + b

# LOSS
objective_function = tf.reduce_mean(tf.square(y - model))

mean, var = tf.nn.moments(y, axes=[0])
error = tf.reduce_mean(tf.square(y - model))
dummy = var

# ALGO
optimizer = tf.train.GradientDescentOptimizer(0.05)
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

batch = random_batch(train_set,10000)
batch_x = batch[:,:-1]
batch_y = batch[:,-1].reshape(10000,1)
error, dummy, W, b , model,y = session.run([error,dummy, W, b ,model,y], feed_dict={x: batch_x, y: batch_y})
print error
print dummy
# print model[1:10]
# print y[1:10]
# print batch_x[1]
# print batch_y[1]
# print np.dot(batch_x[1],W) + b
# print W
# logSize = ethLog.size
# predi = np.zeros(logSize-buf)
# for i in range(logSize-buf):
    # predi[i]=np.dot(ethLog[i:i+buf],W) + b

# trueValue=ethLog[buf:]
# print 'resultat'
# print np.var(trueValue)
# print np.mean(np.square(trueValue-predi))
