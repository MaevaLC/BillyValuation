# -*- coding: utf-8 -*-
"""
Created on Fri Jun  9 12:39:32 2017

@author: m.leclech
"""


import time
from keras.models import Model, load_weights
from keras.layers import Input, LSTM, Dense, concatenate, Flatten
from keras.optimizers import RMSprop
from keras.utils import plot_model


def get_G(G_in, nb_features=91, deletion=1, lr = 0.01):
    gen = Dense(nb_features, activation='relu')(G_in)
    gen = Dense(nb_features//2, activation='relu')(gen)
    G_out = Dense(deletion, activation='sigmoid')(gen)
    G = Model(inputs=G_in, outputs=G_out)
    opt = RMSprop(lr)
    G.compile(loss='mean_squared_error', optimizer=opt, metrics=['binary_accuracy'])
    return G


def get_F(F_in, nb_features=91, deletion=1, lr = 0.001):    
    sentenceMatrix = LSTM(nb_features, return_sequences=True)(F_in[0])    
    deletionMatrix = LSTM(deletion, return_sequences=True)(F_in[1])    
    fusion = concatenate([sentenceMatrix, deletionMatrix])
    fusion = Dense(122, activation='relu')(fusion)
    fusion = Dense(102, activation='relu')(fusion)
    F_out = Dense(nb_features, activation='sigmoid')(fusion)    
    F = Model(inputs=F_in, outputs=F_out)
    opt = RMSprop(lr)
    F.compile(loss='mean_squared_error', optimizer=opt, metrics=['binary_accuracy'])    
    return F


def get_D(D_in, nb_words=30, nb_features=91, deletion=1, lr = 0.01):
    dis = Dense(nb_features//2, activation='relu')(D_in)
    dis = Dense(nb_features//4, activation='relu')(dis)
    dis = Flatten()(dis)
    dis = Dense(nb_features*nb_words//4, activation='relu')(dis)
    D_out = Dense(deletion, activation='sigmoid')(dis)
    D = Model(inputs=D_in, outputs=D_out)
    opt = RMSprop(lr)
    D.compile(loss='mean_squared_error', optimizer=opt, metrics=['binary_accuracy'])
    return D


def set_trainability(model, trainable=False):
    model.trainable = trainable
    for layer in model.layers:
        layer.trainable = trainable
        
        
def make_gan(GAN_in, G, F, D):
    G_out = G(GAN_in)
    F_out = F([GAN_in, G_out])
    GAN_out = D(F_out)
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
G.summary()
print("*** G is ok ! ***\n")
  
inputDeletion = Input(shape=(nb_words, deletion))
F = get_F([inputSentence, inputDeletion])
F.summary()
print("*** F is ok !! ***\n")

inputNewSentence = Input(shape=(nb_words, nb_features))
D = get_D(inputNewSentence)
D.summary()
print("*** D is ok !!! ***\n")

# creation of GAN model
GAN = make_gan(inputSentence, G, F, D)
GAN.summary()
print("*** GFD iz 0k !1!!1!!1! ***\n")

# training
F = load_weights('F1.h5')
G = load_weights('????.h5')
set_trainability(F, False)
set_trainability(D, False)
GAN.fit()

# recuperation of G
#G.save('G_'+str(time.strftime("%y%m%d_%H%M%S"))+'.h5')
print("*** G is saved :) ***\n")
plot_model(GAN, to_file='GAN.png')