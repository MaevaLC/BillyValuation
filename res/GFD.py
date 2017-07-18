# -*- coding: utf-8 -*-
"""
Created on Fri Jun  9 12:39:32 2017

@author: m.leclech
"""


import time
from keras.callbacks import EarlyStopping
from keras.models import Model
from keras.layers import Input, LSTM, Dense, concatenate, Flatten, Lambda
from keras.optimizers import RMSprop
import keras.backend as K
import numpy as np

def lambdaMean(x):
    return K.mean(K.round(x), axis=1)


def get_G(G_in, nb_features=91, deletion=1, lr = 0.01):
    gen = LSTM(nb_features, activation='relu', return_sequences=True)(G_in)
    gen = LSTM(nb_features//2, activation='relu', return_sequences=True)(gen)
    G_out = LSTM(deletion, activation='sigmoid', return_sequences=True)(gen)
    G = Model(inputs=G_in, outputs=G_out)
    opt = RMSprop(lr)
    G.compile(loss='mean_squared_error', optimizer=opt, metrics=['binary_accuracy'])
    return G


def get_F(F_in, nb_features=91, deletion=1, lr = 0.001):    
    sentenceMatrix = LSTM(nb_features, return_sequences=True, activation='relu')(F_in[0])    
    deletionMatrix = LSTM(deletion, return_sequences=True, activation='relu')(F_in[1])    
    fusion = concatenate([sentenceMatrix, deletionMatrix])
    fusion = Dense(122, activation='relu')(fusion)
    fusion = Dense(102, activation='relu')(fusion)
    F_out = Dense(nb_features, activation='sigmoid')(fusion)    
    F = Model(inputs=F_in, outputs=F_out)
    opt = RMSprop(lr)
    F.compile(loss='mean_squared_error', optimizer=opt, metrics=['binary_accuracy'])    
    return F


def get_D(D_in, nb_words=30, nb_features=91, deletion=1, lr = 0.01):
    dis = LSTM(nb_features//2, activation='relu', return_sequences=True)(D_in)
    dis = LSTM(nb_features//4, activation='relu', return_sequences=True)(dis)
    dis = Flatten()(dis)
    dis = Dense(nb_features*nb_words//4, activation='relu')(dis)
    D_out = Dense(2, activation='sigmoid')(dis)
    D = Model(inputs=D_in, outputs=D_out)
    opt = RMSprop(lr)
    D.compile(loss='binary_crossentropy', optimizer=opt, metrics=['binary_accuracy'])
    return D


def set_trainability(model, trainable=False):
    model.trainable = trainable
    for layer in model.layers:
        layer.trainable = trainable
        
        
def make_gan(GAN_in, G, F, D):
    G_out = G(GAN_in)    
    F_out = F([GAN_in, G_out])
    GAN_out = D(F_out)
    lambdaLayer=Lambda(lambdaMean)(G_out)
    GAN_out = concatenate([GAN_out, lambdaLayer])
    GAN = Model(GAN_in, GAN_out)
    GAN.compile(loss='mean_squared_error', optimizer=G.optimizer, metrics=['binary_accuracy'])
    return GAN


# parameters
nb_words = 30
nb_features = 91
deletion = 1

# creation of sub models G, F, D
inputSentence = Input(shape=(nb_words, nb_features))
G = get_G(inputSentence)
#G.summary()
print("*** G is ok ! ***\n")
inputDeletion = Input(shape=(nb_words, deletion))
F = get_F([inputSentence, inputDeletion])
#F.summary()
print("*** F is ok !! ***\n")

inputNewSentence = Input(shape=(nb_words, nb_features))
D = get_D(inputNewSentence)
#D.summary()
print("*** D is ok !!! ***\n")

# creation of GAN model
GAN = make_gan(inputSentence, G, F, D)
GAN.summary()
print("*** GFD iz 0k 1! ***\n")

# *** DATA FOR TRAINING ***
shape_S = (30,nb_features)
shape_O = (3)
# load data
datasetGANin = np.loadtxt("GANtrainV3.csv", delimiter=",", dtype='float')
datasetGANout = np.loadtxt("GANoutputV3.csv", delimiter=",", dtype='float')
flat_GANin = datasetGANin[:,0:(nb_words*nb_features)]
flat_GANout = datasetGANout[:,0:3]
# make them a matrix
GAN_in = []
for listGANin in flat_GANin:
    GAN_in.append(listGANin.reshape(shape_S))
GAN_out = []
for listGANout in flat_GANout:
    GAN_out.append(listGANout.reshape(shape_O))

# training
F.load_weights('F_170703_191548.h5')
print("*** F is loaded ! ***\n")
D.load_weights('D_170713_145643.h5')
print("*** D is loaded ! ***\n")
set_trainability(F, False)
set_trainability(D, False)
callbacks = [EarlyStopping(monitor='loss', patience=12, 
            min_delta=0.01, verbose=1, mode ="min")]
GAN.fit(np.array(GAN_in), np.array(flat_GANout),
                batch_size=100, epochs=250, verbose=2,
                callbacks=callbacks, shuffle=True)

# recuperation of G
G.save('G_'+str(time.strftime("%y%m%d_%H%M%S"))+'.h5')
print("*** G is saved :) ***\n")