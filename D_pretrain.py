# -*- coding: utf-8 -*-
"""
Created on Fri Jun  9 12:39:32 2017

@author: m.leclech
"""

from keras.callbacks import EarlyStopping
from keras.models import Model
from keras.layers import Input, LSTM, Dense, Flatten
from keras.optimizers import SGD, RMSprop, Adagrad, Adadelta, Adam, Adamax, Nadam
import numpy as np
import time

np.set_printoptions(threshold=np.inf)

# parameters
nb_words = 30
nb_features = 91
outputVal = 2

# *** DATA FOR TRAINING ***
# load data
datasetF = np.loadtxt("DtrainV3.csv", delimiter=",", dtype='float')
datasetA = np.loadtxt("DanswerV3.csv", delimiter=",", dtype='float')
#datasetFt = np.loadtxt("GtrainV3.csv", delimiter=",", dtype='float')
#datasetAt = np.loadtxt("GanswerV3.csv", delimiter=",", dtype='float')
print("*** Data loaded ! ***\n")
# split into input (X) and output (Y) variables and reshape to matrix
# define the shapes of the matrix
shape_S = (30,nb_features)
shape_O = (2)
# get the list of lists of vars
flatX = datasetF[:,0:(nb_words*nb_features)]
flatY = datasetA[:,0:2]
#flatX_t = datasetFt[:,0:(nb_words*nb_features)]
#flatYt = datasetAt[:,0:(nb_words*nb_features)]
# make them a matrix
X = []
for listX in flatX:
    X.append(listX.reshape(shape_S))
Y = []
for listY in flatY:
    Y.append(listY.reshape(shape_O))
#X_t = []
#for listX_t in flatX_t:
#    X_t.append(listX_t.reshape(shape_S))
print("*** Data reshaped ! ***\n")
# *** END DATA ***


# train
#listeN = [100]
#listeM = [1]
#listeN = [1,100,447,1000,2000,4477]
#listeLR = [0.0001, 0.001, 0.01, 0.1, 1]
#listeN = [SGD(), RMSprop(lr = 0.001), Adagrad(), Adadelta(), Adam(), Adamax(), Nadam()]
listeM = ['mean_squared_error',
          'hinge', 'binary_crossentropy',
          'kullback_leibler_divergence', 'poisson']
#listeM = ['mean_squared_error', 'mean_absolute_error', 'mean_absolute_percentage_error', 'mean_squared_logarithmic_error',
#          'squared_hinge', 'hinge', 'binary_crossentropy',
#          'kullback_leibler_divergence', 'poisson', 'cosine_proximity']
#listeM = ['mean_squared_error']
listeN = [RMSprop(lr = 0.001)]

for n in listeN:    
    for m in listeM:
        
        # create RNN
        inputSentence = Input(shape=(nb_words, nb_features))        
        dis = LSTM(nb_features//2, activation='relu', return_sequences=True)(inputSentence)
        dis = LSTM(nb_features//4, activation='relu', return_sequences=True)(dis)
        dis = Flatten()(dis)
        dis = Dense(nb_features*nb_words//4, activation='relu')(dis)
        D_out = Dense(outputVal, activation='sigmoid')(dis)
        D = Model(inputs=inputSentence, outputs=D_out)
    
        # compile
        D.compile(loss=m, optimizer=n, metrics=['binary_accuracy'])        
    
        # fit
        print("\n" + str(n))
        print(str(m) + "\n")
        callbacks = [EarlyStopping(monitor='loss', patience=5, 
                    min_delta=0.1, verbose=1, mode ="min")]
        D.fit(np.array(X), np.array(flatY),
              batch_size=100, epochs=250, verbose=0,
              callbacks=callbacks, shuffle=True)
        
        # print scores
        scores = D.evaluate(np.array(X), np.array(flatY), verbose = 0)
        print("\n%s: %.2f%%" % (D.metrics_names[1], scores[1]*100))
        
        # save
        D.save_weights('D_'+str(time.strftime("%y%m%d_%H%M%S"))+'.h5')

        # predict
        predictions = D.predict(np.array(X))
        print(np.round(predictions[0:7],2))
        print(np.round(predictions[-7:-  1],2))
