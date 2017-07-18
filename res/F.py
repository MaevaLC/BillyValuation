# -*- coding: utf-8 -*-
"""
Created on Fri Jun  9 12:39:32 2017

@author: m.leclech
"""

from keras.models import Sequential
from keras.layers import Merge, Dense


def F(generatorModel):
    
    mix = Sequential()
    mix.add(Merge([generatorModel.inputs, generatorModel(generatorModel.inputs)], mode='concat'))
    mix.add(Dense(32, activation='relu'))
    mix.add(Dense(91, activation='softmax'))
    
    mix.compile(loss='categorical_crossentropy',
                    optimizer='rmsprop',
                    metrics=['accuracy'])
    
    return mix
    
