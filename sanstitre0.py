# -*- coding: utf-8 -*-
"""
Created on Tue Jun  6 10:58:39 2017

@author: m.leclech
"""

## load pima indians dataset
#dataset = numpy.loadtxt("testV3.csv", delimiter=",")
## split into input (X) and output (Y) variables
#listX=dataset[:,0:2730]
#shape = (30,91)
#X = listX.reshape(shape)
#print(X)

# Create your first MLP in Keras
from keras.models import Sequential
from keras.layers import Dense
import numpy
# fix random seed for reproducibility
numpy.random.seed(7)
# load pima indians dataset
dataset = numpy.loadtxt("pima.csv", delimiter=",")
# split into input (X) and output (Y) variables
X = dataset[:,0:8]
Y = dataset[:,8]
# create model
model = Sequential()
model.add(Dense(12, input_dim=8, activation='relu'))
model.add(Dense(8, activation='relu'))
model.add(Dense(1, activation='sigmoid'))
# Compile model
model.compile(loss='binary_crossentropy', optimizer='adam', metrics=['accuracy'])
# Fit the model
model.fit(X, Y, epochs=150, batch_size=10, verbose=0)
# evaluate the model
scores = model.evaluate(X, Y)
print("\n%s: %.2f%%" % (model.metrics_names[1], scores[1]*100))

print(model.summary())
print(X.shape)
print(Y.shape)