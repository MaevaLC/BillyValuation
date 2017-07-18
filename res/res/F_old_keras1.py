# -*- coding: utf-8 -*-
"""
Created on Fri Jun  9 12:39:32 2017

@author: m.leclech
"""

from keras.callbacks import EarlyStopping
from keras.models import Sequential, load_model
from keras.layers import Merge, LSTM, Dense, Concatenate
from keras.optimizers import SGD, RMSprop, Adagrad, Adadelta, Adam, Adamax, Nadam
import numpy as np

np.set_printoptions(threshold=np.inf)

# parameters
nb_words = 30
nb_features = 91
deletion = 1

# load data
datasetF = np.loadtxt("trainV3.csv", delimiter=",", dtype='float')
datasetD = np.loadtxt("deletionV3.csv", delimiter=",", dtype='float')
datasetA = np.loadtxt("answerV3.csv", delimiter=",", dtype='float')
datasetFt = np.loadtxt("trainV3.csv", delimiter=",", dtype='float')
datasetDt = np.loadtxt("deletionV3.csv", delimiter=",", dtype='float')
datasetAt = np.loadtxt("answerV3.csv", delimiter=",", dtype='float')
# split into input (X) and output (Y) variables
shape_a = (30,nb_features)
shape_b = (30,1)
flatX_a = datasetF[:,0:(nb_words*nb_features)]
flatX_b = datasetD[:,0:30]
flatY = datasetA[:,0:(nb_words*nb_features)]
X_a = []
for listX_a in flatX_a:
    X_a.append(listX_a.reshape(shape_a))
X_b = []
for listX_b in flatX_b:
    X_b.append(listX_b.reshape(shape_b))
Y = []
for listY in flatY:
    Y.append(listY.reshape(shape_a))
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


# train
#listeN = [100]
#listeM = [1]
#listeN = [1,100,447,1000,2000,4477]
#listeLR = [0.0001, 0.001, 0.01, 0.1, 1]
listeN = [SGD(), RMSprop(lr = 0.001), Adagrad(), Adadelta(), Adam(), Adamax(), Nadam()]
#listeN = [SGD(), RMSprop(lr = 0.001), Adagrad(), Adadelta(), Adam(), Adamax(), Nadam()]
#listeM = ['mean_squared_error', 'mean_absolute_error', 'mean_absolute_percentage_error', 'mean_squared_logarithmic_error',
#          'squared_hinge', 'hinge', 'binary_crossentropy',
#          'kullback_leibler_divergence', 'poisson', 'cosine_proximity']
#listeM = ['mean_squared_error', 'mean_absolute_error', 'mean_absolute_percentage_error', 'mean_squared_logarithmic_error',
#          'squared_hinge', 'hinge', 'binary_crossentropy',
#          'kullback_leibler_divergence', 'poisson', 'cosine_proximity']
listeM = ['mean_squared_error']
for n in listeN:    
    for m in listeM:
        # create RNN
        sentenceMatrix = Sequential()
        sentenceMatrix.add(LSTM(nb_features, return_sequences=True, input_shape=(nb_words, nb_features)))
        
        deletionMatrix = Sequential()
        deletionMatrix.add(LSTM(deletion, return_sequences=True, input_shape=(nb_words, deletion)))
        
        mix = Sequential()
        mix.add(Merge([sentenceMatrix, deletionMatrix], mode='concat'))
        mix.add(Dense(122, activation='relu'))
        mix.add(Dense(102, activation='relu'))
        mix.add(Dense(nb_features, activation='sigmoid'))        
        
        # compile
        callbacks = [EarlyStopping(monitor='loss', patience=50, min_delta=0.01, verbose=1, mode ="min")]       
        mix.compile(loss=m,
                    optimizer=n,
                    metrics=['binary_accuracy'])        
    
        # fit
        print("\n" + str(n))
        print(str(m) + "\n")
        mix.fit([np.array(X_a), np.array(X_b)], np.array(Y),
                    batch_size=100, epochs=250, verbose=0,
                    callbacks=callbacks, shuffle=True)
        
        #print scores
        scores = mix.evaluate([np.array(X_at), np.array(X_bt)], np.array(Yt), verbose = 0)
        print("\n%s: %.2f%%" % (mix.metrics_names[1], scores[1]*100))
        
        #save
        #mix.save('modelF'+str(scores[1]*100)+'.h5')

        #reload model and predict
        #mixt = load_model("modelF97.8159347083.h5")
        predictions = mix.predict([np.array(X_at), np.array(X_bt)])
        print(np.round(predictions[0][0], 2))
