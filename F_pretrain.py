# -*- coding: utf-8 -*-
"""
Created on Fri Jun  9 12:39:32 2017

@author: m.leclech
"""

from keras.callbacks import EarlyStopping
from keras.models import Model
from keras.layers import Input, LSTM, Dense, concatenate
from keras.optimizers import SGD, RMSprop, Adagrad, Adadelta, Adam, Adamax, Nadam
import numpy as np
import time

np.set_printoptions(threshold=np.inf)

# parameters
nb_words = 30
nb_features = 91
deletion = 1

# *** DATA FOR TRAINING ***
# load data
datasetF = np.loadtxt("trainV3.csv", delimiter=",", dtype='float')
datasetD = np.loadtxt("deletionV3.csv", delimiter=",", dtype='float')
datasetA = np.loadtxt("answerV3.csv", delimiter=",", dtype='float')
datasetFt = np.loadtxt("trainV3.csv", delimiter=",", dtype='float')
datasetDt = np.loadtxt("deletionV3.csv", delimiter=",", dtype='float')
datasetAt = np.loadtxt("answerV3.csv", delimiter=",", dtype='float')
print("*** Data loaded ! ***\n")
# split into input (X) and output (Y) variables and reshape to matrix
# define the shapes of the matrix
shape_S = (30,nb_features)
shape_D = (30,1)
# get the list of lists of vars
flatX_a = datasetF[:,0:(nb_words*nb_features)]
flatX_b = datasetD[:,0:30]
flatY = datasetA[:,0:(nb_words*nb_features)]
flatX_at = datasetFt[:,0:(nb_words*nb_features)]
flatX_bt = datasetDt[:,0:30]
flatYt = datasetAt[:,0:(nb_words*nb_features)]
# make them a matrix
X_a = []
for listX_a in flatX_a:
    X_a.append(listX_a.reshape(shape_S))
X_b = []
for listX_b in flatX_b:
    X_b.append(listX_b.reshape(shape_D))
Y = []
for listY in flatY:
    Y.append(listY.reshape(shape_S))
X_at = []
for listX_at in flatX_at:
    X_at.append(listX_at.reshape(shape_S))
X_bt = []
for listX_bt in flatX_bt:
    X_bt.append(listX_bt.reshape(shape_D))
Yt = []
for listYt in flatYt:
    Yt.append(listYt.reshape(shape_S))
print("*** Data reshaped ! ***\n")
# *** END DATA ***


# train
#listeN = [100]
#listeM = [1]
#listeN = [1,100,447,1000,2000,4477]
#listeLR = [0.0001, 0.001, 0.01, 0.1, 1]
listeN = [RMSprop(lr = 0.001)]
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
        inputSentence = Input(shape=(nb_words, nb_features))        
        inputDeletion = Input(shape=(nb_words, deletion))        
        fusion = concatenate([inputSentence, inputDeletion])
        fusion = Dense(122, activation='relu')(fusion)
        fusion = Dense(102, activation='relu')(fusion)
        fusion = Dense(nb_features, activation='sigmoid')(fusion)
        
        F = Model(inputs=[inputSentence, inputDeletion], outputs=fusion)
    
        # compile
        F.compile(loss=m, optimizer=n, metrics=['binary_accuracy'])        
    
        # fit
        print("\n" + str(n))
        print(str(m) + "\n")
        callbacks = [EarlyStopping(monitor='loss', patience=10, 
                    min_delta=0.1, verbose=1, mode ="min")]
        F.fit([np.array(X_a), np.array(X_b)], np.array(Y),
                    batch_size=100, epochs=250, verbose=2,
                    callbacks=callbacks, shuffle=True)
        
        # print scores
        scores = F.evaluate([np.array(X_at), np.array(X_bt)], np.array(Yt), verbose = 0)
        print("\n%s: %.2f%%" % (F.metrics_names[1], scores[1]*100))
        
        # save
        F.save_weights('F_'+str(time.strftime("%y%m%d_%H%M%S"))+'.h5')

        # predict
        predictions = F.predict([np.array(X_at), np.array(X_bt)])
        print(np.round(predictions[0][0], 2))
