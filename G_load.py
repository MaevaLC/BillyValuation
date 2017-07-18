# -*- coding: utf-8 -*-
"""
Created on Thu Jun 29 09:48:06 2017

@author: m.leclech
"""

import json
import hashlib
import random as rd
import numpy as np
from keras.models import Model
from keras.layers import Input, LSTM
from keras.optimizers import RMSprop
from AnnotateText import annotateText

np.set_printoptions(threshold=np.inf)


url = "ideavaluation.estia.fr"
seance = 2
path = "annotatedText/"+url+"/"+str(seance)
featListTag = ["ADJ", "ADP", "ADV", "AFFIX", "CONJ", "DET", "NOUN", "NUM", "PRON",
"PRT", "PUNCT", "UNKNOWN", "VERB", "X"]
featListLabel = ["ABBREV", "ACOMP", "ADVCL", "ADVMOD",
"ADVPHMOD", "AMOD", "APPOS", "ATTR", "AUX", "AUXCAUS", "AUXPASS", "AUXVV", "CC",
"CCOMP", "CONJ", "COP", "CSUBJ", "CSUBJPASS", "DEP", "DET", "DISCOURSE", "DISLOCATED",
"DOBJ", "DTMOD", "EXPL", "FOREIGN", "GOESWITH", "IOBJ", "KW", "LIST", "MARK", "MWE",
"MWV", "NEG", "NN", "NOMC", "NOMCSUBJ", "NOMCSUBJPASS", "NPADVMOD", "NSUBJ",
"NSUBJPASS", "NUM", "NUMBER", "NUMC", "P", "PARATAXIS", "PARTMOD", "PCOMP",
"POBJ", "POSS", "POSTNEG", "PRECOMP", "PRECONJ", "PREDET", "PREF", "PREP", "PRONL",
"PRT", "PS", "QUANTMOD", "RCMOD", "RCMODREL", "RDROP", "REF", "REMNANT",
"REPARANDUM", "ROOT", "SNUM", "SUFF", "SUFFIX", "TITLE", "TMOD", "TOPIC", "UNKNOWN",
"VMOD", "VOCATIVE", "XCOMP"]


class Word:
    """Class to define a word, by its lemme, position, parent, children"""
    
    def __init__(self, lemme, position, parent, tag, label):
        """Constructor"""
    
        self.lemme = lemme
        self.position = position
        self.parent = parent
        self.children = []
        self.tag = tag
        self.label = label
        

def createListWords(pathFile):
    """Create a list of objects (Word)
    
    Args: 
        the path of the annotated data file (string)
    Returns: 
        a list containing Word objects (list)
    
    """
    
    listWords = []
    with open(pathFile, "r") as f:
        annotatedText = json.load(f)
        for i in range(len(annotatedText["tokens"])):
            annotatedWord = annotatedText["tokens"][i]
            dependency = annotatedWord["dependencyEdge"]["headTokenIndex"]
            text = annotatedWord["text"]["content"]
            tag = annotatedWord["partOfSpeech"]["tag"]
            label = annotatedWord["dependencyEdge"]["label"]
            listWords.append(Word(text, i, dependency, tag, label))
    for word in listWords:
        listWords[word.parent].children.append(word.position)
    return listWords


def hashSentence(stringToHash):
    """Return a string hashed (md5)"""    
    
    hashString = hashlib.md5((stringToHash).encode()).hexdigest()
    return hashString


def listIndex(featuresList, string):
    for k in range(len(featuresList)):
        if string == featuresList[k]:
            return k


def normalise(L):
    minimum = min(L)[0]
    maximum = max(L)[0]
    ecart = maximum-minimum
    for i in range(len(L)):
        intermediaire = (L[i][0]-minimum)
        L[i] = intermediaire/ecart
    return L
        
        
def sentenceToFeature(file):
    fileFeature = []
    listWords = createListWords(path+"/"+file)   
    if len(listWords) < 30 :
        for word in listWords:
            wordFeature = [0.0]*len(featListTag + featListLabel)
            coeff = 1
            tagIndex = listIndex(featListTag, word.tag)
            labelIndex = listIndex(featListLabel, word.label) + len(featListTag)
            wordFeature[tagIndex] += coeff
            wordFeature[labelIndex] += coeff
            #wordFeature[-2] = float(word.position/29)
            fileFeature += wordFeature
        rest = 30 - len(listWords)
        for i in range(rest):
            fileFeature += [0.0]*(len(featListTag + featListLabel))
    return fileFeature


def delete(deleteList, sentence):
    temp = ""
    for i in range(len(deleteList)):
#        rounded = np.round(DL[i])
        if deleteList[i] < 0.96: #0.865
            if i < len(sentence):
                temp += sentence[i].lemme + " "
    return temp


# parameters
nb_words = 30
nb_features = 91
deletion = 1

# rnn
G_in = Input(shape=(nb_words, nb_features))
gen = LSTM(nb_features, activation='relu', return_sequences=True)(G_in)
gen = LSTM(nb_features//2, activation='relu', return_sequences=True)(gen)
G_out = LSTM(deletion, activation='sigmoid', return_sequences=True)(gen)
G = Model(inputs=G_in, outputs=G_out)
opt = RMSprop(0.01)
G.compile(loss='mean_squared_error', optimizer=opt, metrics=['binary_accuracy'])


G.load_weights('G_170717_134615.h5')
shape_S = (30,91)
x = input('You : ')
while x != 'stop':
    annotateText(url, seance, x)
    fileName = hashSentence(x)+'.json'
#    fileName = '42e11e68afd808dc29476f1e0524c0b9.json'
    features = sentenceToFeature(fileName)
    featuresArray = np.array(features) 
    featuresMatrix = [np.array([featuresArray.reshape(shape_S)])]
    predictions = G.predict(featuresMatrix)
    # redemander à D !!!!!!!!!!!!!
    print(normalise(predictions[0]))
    print('Billy : '+delete(normalise(predictions[0]), createListWords(path+'/'+fileName)))
    x = input('You : ')    