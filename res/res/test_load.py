# -*- coding: utf-8 -*-
"""
Created on Wed Jun 14 17:00:29 2017

@author: m.leclech
"""


from keras.models import load_model
import numpy as np

np.set_printoptions(threshold=np.inf)

# parameters
nb_words = 30
nb_features = 91
deletion = 1
# load data
datasetFt = np.loadtxt("trainV3.csv", delimiter=",", dtype='float')
datasetDt = np.loadtxt("deletionV3.csv", delimiter=",", dtype='float')
datasetAt = np.loadtxt("answerV3.csv", delimiter=",", dtype='float')
# split into input (X) and output (Y) variables
shape_a = (30,nb_features)
shape_b = (30,1)
flatX_at = datasetFt[:,0:(nb_words*nb_features)]
flatX_bt = datasetDt[:,0:30]
flatYt = datasetAt[:,0:(nb_words*nb_features)]
X_at = []
for listX_at in flatX_at:
    X_at.append(listX_at.reshape(shape_a))
X_bt = []
for listX_bt in flatX_bt:
    X_bt.append(listX_bt.reshape(shape_b))
Yt = []
for listYt in flatYt:
    Yt.append(listYt.reshape(shape_a))


print('ok0')
mix = load_model('F1.h5')
print('ok1')
predictions = mix.predict([np.array(X_at), np.array(X_bt)])
print('ok2')
print(predictions[0][0])