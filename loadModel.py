# -*- coding: utf-8 -*-
"""
Created on Fri Jun  2 10:56:33 2017

@author: m.leclech
"""

from keras.models import load_model
import numpy

model = load_model('my_model.h5')

# load pima indians dataset
dataset = numpy.loadtxt("pima.csv", delimiter=",")
# split into input (X) and output (Y) variables
X = dataset[:,0:8]
Y = dataset[:,8]

# evaluate the model
scores = model.evaluate(X, Y)
print("\n%s: %.2f%%" % (model.metrics_names[1], scores[1]*100))