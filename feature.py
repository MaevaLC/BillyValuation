# -*- coding: utf-8 -*-
"""
Created on Fri Jun  2 16:03:05 2017

@author: m.leclech
"""

import csv
import json
import os


url = "neptune2.estia.fr"
seance = 2
path = "res/annotatedText/"+url+"/"+str(seance)

featuresList = ["ADJ", "ADP", "ADV", "AFFIX", "CONJ", "DET", "NOUN", "NUM", "PRON",
"PRT", "PUNCT", "UNKNOWN", "VERB", "X", "ABBREV", "ACOMP", "ADVCL", "ADVMOD",
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


def listIndex(featuresList, string):
    for k in range(len(featuresList)):
        if string == featuresList[k]:
            return k

            
csvf = open("testV3.csv", "w") 
files = []
for element in os.listdir(path):
    if element.endswith('.json'):
        files.append(element)
for file in files:
    fileFeature = []
    listWords = createListWords(path+"/"+file)   
    if len(listWords) < 30 :
        for word in listWords:
            wordFeature = [0]*len(featuresList)
            coeff = 1
            while word.position != word.parent:
                tagIndex = listIndex(featuresList, word.tag)
                labelIndex = listIndex(featuresList, word.label)
                wordFeature[tagIndex] += coeff
                wordFeature[labelIndex] += coeff
                coeff = coeff/2
                parent = listWords[word.parent]
                word = parent
            tagIndex = listIndex(featuresList, word.tag)
            labelIndex = listIndex(featuresList, word.label)
            wordFeature[tagIndex] += coeff
            wordFeature[labelIndex] += coeff
            fileFeature += wordFeature
        rest = 30 - len(listWords)
        for i in range(rest):
            fileFeature += [0]*len(featuresList)
        out = csv.writer(csvf, delimiter=',', lineterminator = '\n')
        out.writerow(fileFeature)
csvf.close()
