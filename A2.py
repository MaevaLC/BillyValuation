# -*- coding: utf-8 -*-
"""
Created on Tue May 30 17:48:47 2017

@author: m.leclech
"""

from keras.models import Sequential
from keras.layers import Dense, Flatten
import numpy as np
import random as rd
from keras import backend as K
# fix random seed for reproducibility
np.random.seed(7)
# load dataset
dataset = np.loadtxt("testV3.csv", delimiter=",")
# split into input (X) and output (Y) variables
shape=(30,91)
flatX = dataset[:,0:2730]
X = []
for listX in flatX:
    X.append(listX.reshape(shape))
randBinList = lambda n: [rd.randint(0,1) for b in range(1,n+1)]
Y = randBinList(26)  #random binary value for test
# create model
model = Sequential()
model.add(Dense(91, input_shape=(30, 91), activation='relu'))
model.add(Dense(40, activation='relu'))
model.add(Flatten())
model.add(Dense(1, activation='sigmoid'))


def validation(y_true, y_pred):
    print("#####")
    print(y_true)
    print(y_pred)
    return K.mean(K.binary_crossentropy(y_pred, y_true), axis=-1)



# Compile model
model.compile(loss=validation, optimizer='adam', metrics=['accuracy'])

#useful data to check everything is right
print (model.summary())
print(np.array(X).shape)
print(np.array(Y).shape)

# Fit the model
model.fit(np.array(X), np.array(Y), epochs=10, batch_size=1, verbose=0)  #verbose = 1 or 2 for more data

#save to load it later (include structure and weights)
model.save('my_modelA2.h5')

# evaluate the model
scores = model.evaluate(np.array(X), Y)
print("\n%s: %.2f%%" % (model.metrics_names[1], scores[1]*100))

# calculate predictions
predictions = model.predict(np.array(X))
# round predictions
rounded = [round(x[0]) for x in predictions]
print("\n Predictions")
print(rounded)

