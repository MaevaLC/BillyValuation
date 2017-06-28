# -*- coding: utf-8 -*-
"""
Created on Tue Jun  6 17:08:14 2017

@author: m.leclech
"""

from random import *
import csv
import json
import os
import numpy as np


randBinList = lambda n: [randint(0,1) for b in range(1,n+1)]

url = "ideavaluation.estia.fr"
seance = 2
path = "annotatedText/"+url+"/"+str(seance)


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


def delete (deleteList, sentence):
    temp = ""
    for i in range(len(deleteList)):
        if str(deleteList[i]) == "0":
            if i < len(sentence):
                temp += sentence[i].lemme + " "
    return temp      
            

#files=[]
#for element in os.listdir(path):
#    if element.endswith('.json'):
#        files.append(element)
#for file in files:
#    sentence = createListWords(path+"/"+file)
#    for n in range(10):
#        randomDL = randBinList(30)
#        print(randomDL)
#        print(delete(randomDL, sentence))
#        
        
def featureDelete(deleteList, sentenceFeature):
    result = []
    c = 0
    for i in range(len(deleteList)):
        if str(deleteList[i]) == "0":
            for n in range(i*91,(i+1)*91):
                result.append(sentenceFeature[n])
        else :
            c+=1
    for j in range(c):
        for k in range(91):
            result.append(0.0)
        #result.append(1.0)
    return result


csvf = open("trainV3.csv", "a") 
csvd = open("deletionV3.csv", "a")  
csva = open("answerV3.csv", "a")  
# load data
dataset = np.loadtxt("trainV3.csv", delimiter=",")
flatX_a = dataset[:,0:2730]
for flatXelement in flatX_a:
    for n in range(10):
        out = csv.writer(csvf, delimiter=',', lineterminator = '\n')
        out.writerow(flatXelement)
        randomList = randBinList(30)
        outD = csv.writer(csvd, delimiter=',', lineterminator = '\n')
        outD.writerow(randomList)
        answer = featureDelete(randomList, flatXelement)
        outA = csv.writer(csva, delimiter=',', lineterminator = '\n')
        outA.writerow(answer)
csvf.close()
csvd.close()
csva.close()
        
    

