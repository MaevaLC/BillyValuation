# -*- coding: utf-8 -*-
"""
Created on Tue May 30 17:48:47 2017

@author: m.leclech
"""

from keras.models import Sequential
from keras.layers import Dense, Flatten
import numpy
# fix random seed for reproducibility
numpy.random.seed(7)
# load dataset
dataset = numpy.loadtxt("testV3.csv", delimiter=",")
# split into input (X) and output (Y) variables
shape=(30,91)
flatX = dataset[:,0:2730]
X = []
for listX in flatX:
    X.append(listX.reshape(shape))
Y = dataset[:,2729]
print (Y)
# create model
model = Sequential()
model.add(Dense(91, input_shape=(30, 91), activation='relu'))
model.add(Dense(40, activation='relu'))
model.add(Flatten())
model.add(Dense(1, activation='sigmoid'))
# Compile model
model.compile(loss='binary_crossentropy', optimizer='adam', metrics=['accuracy'])

print (model.summary())
print(numpy.array(X).shape)
print(Y.shape)

# Fit the model
model.fit(numpy.array(X), Y, epochs=10, batch_size=1, verbose=0)
model.save('my_modelA2.h5')

# evaluate the model
scores = model.evaluate(numpy.array(X), Y)
print("\n%s: %.2f%%" % (model.metrics_names[1], scores[1]*100))

## calculate predictions
#predictions = model.predict(X)
## round predictions
#rounded = [round(x[0]) for x in predictions]
#print(rounded)
