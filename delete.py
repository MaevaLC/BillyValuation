# -*- coding: utf-8 -*-
"""
Created on Tue Jun  6 17:08:14 2017

@author: m.leclech
"""

from random import *
import json


randBinList = lambda n: [randint(0,1) for b in range(1,n+1)]
url = "neptune2.estia.fr"
seance = 2
path = "res/annotatedText/"+url+"/"+str(seance)


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



testDL = randBinList(30)
testSF = createListWords(path+"/5a44e1ee157b9509529aa8a460683c4d.json")

def delete (deleteList, sentence):
    temp = ""
    for i in range(len(deleteList)):
        if str(deleteList[i]) == "1":
            if i < len(sentence) :
                temp += sentence[i].lemme + " "
    print(temp)

print(testDL)            
delete(testDL, testSF)
