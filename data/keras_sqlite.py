import numpy as np
import matplotlib.pyplot as plt
import sqlite3
import tensorflow as tf
from random import randint
import math
import keras
from keras.layers import Dense, Activation, Dropout
from keras.models import Sequential


model = Sequential()

model.add(Dense(units=10,activation='relu', input_dim=inputSize))
model.add(Dropout(0.5))
# model.add(Dense(units=10,activation='relu'))
# model.add(Dropout(0.5))
model.add(Dense(units=1, activation = 'linear'))

adam = keras.optimizers.Adam(lr=0.001, beta_1=0.9, beta_2=0.999, epsilon=1e-08, decay=0.0)
model.compile(loss=keras.losses.mean_squared_error, optimizer=adam) 

batch_size = size
# 40000
# batch = random_batch(train_set,batch_size)
trainIndex = int(size*0.85)
trainStart = int(size*0.2)
batch=train_set
X_train = batch[trainStart:trainIndex,:-1]
Y_train = batch[trainStart:trainIndex,-1]#.reshape(batch_size,1)

# batch = random_batch(train_set,40000)
batch = train_set
X_test = batch[trainIndex:,:-1]
Y_test = batch[trainIndex:,-1]#.reshape(size,1)

model.fit(X_train, Y_train, batch_size=128, nb_epoch=40, verbose=1, validation_data=(X_test,Y_test) )
# model.fit(x_train, y_train, epochs=5, batch_size=32)

# for nBatch in range(50):
    # batch = random_batch(train_set,batch_size)
    # x_batch = batch[:,:-1]
    # y_batch = batch[:,-1].reshape(batch_size,1)
    # model.train_on_batch(x_batch, y_batch)


loss= model.evaluate(X_test, Y_test, batch_size=128)

print 'loss: ', loss
print 'variance: ', np.var(Y_test)
