# -*- coding: utf-8 -*-
"""
Created on Thu Jun 29 09:48:06 2017

@author: m.leclech
"""


from keras.models import load_model
from AnnotateText import annotateText


url = "ideavaluation.estia.fr"
seance = 2
path = "annotatedText/"+url+"/"+str(seance)  #to change later
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


def listIndex(featuresList, string):
    for k in range(len(featuresList)):
        if string == featuresList[k]:
            return k
            

def sentenceToFeature(file):
    fileFeature = []
    listWords = createListWords(path+"/"+file)   
    if len(listWords) < 30 :
        for word in listWords:
            wordFeature = [0.0]*len(featListTag + featListLabel)
            coeff = 1.0
            tagIndex = listIndex(featListTag, word.tag)
            labelIndex = listIndex(featListLabel, word.label) + len(featListTag)
            wordFeature[tagIndex] += coeff
            wordFeature[labelIndex] += coeff
            fileFeature += wordFeature
        rest = 30 - len(listWords)
        for i in range(rest):
            fileFeature += [0.0]*(len(featListTag + featListLabel))


#generator = load_model('????.h5')
x = ''
while x != 'stop':
    x = input('Phrase originale :')
    #featX = annotateText(url, seance, x)
    featX = 