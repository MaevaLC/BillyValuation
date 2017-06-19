# -*- coding: utf-8 -*-
"""
Created on Fri Jun  9 15:54:04 2017

@author: m.leclech
"""


from keras.models import Sequential
from keras.layers import Dense

model = Sequential()
model.add(Dense(32, activation='relu'))
model.compile(loss='categorical_crossentropy',
                optimizer='adam',
                metrics=['accuracy'])
model.fit()