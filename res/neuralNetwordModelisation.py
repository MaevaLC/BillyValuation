# -*- coding: utf-8 -*-
"""
Created on Wed May 31 10:20:22 2017

@author: m.leclech
"""

import json
import os
import csv 

tf = open("test.csv", "w")
csvf = open("myfile.csv","w")

url = "ideavaluation.estia.fr"
seance = 2

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

def listIndex(featuresList, string):
    for k in range(len(featuresList)):
        if string == featuresList[k]:
            return k

files = []
for element in os.listdir("res/annotatedText/"+url+"/"+str(seance)):
    if element.endswith('.json'):
        files.append(element)

for file in files:    
    with open("res/annotatedText/"+url+"/"+str(seance)+"/"+file) as f:
        annotatedText = json.load(f)
        for i in range(len(annotatedText["tokens"])):
            sentenceWithoutWordI = ""
            wordFeature = [0]*len(featuresList)            
            tagIndex = listIndex(featuresList, annotatedText["tokens"][i]["partOfSpeech"]["tag"])
            labelIndex = listIndex(featuresList, annotatedText["tokens"][i]["dependencyEdge"]["label"])
            wordFeature[tagIndex] = 1
            wordFeature[labelIndex] = 1
            for j in range(len(annotatedText["tokens"])):
                if i != j:
                    sentenceWithoutWordI += annotatedText["tokens"][j]["text"]["content"] + " "
            print(sentenceWithoutWordI)
            answer = input("legit ? y/N :")
            if answer == "y":
                wordFeature.append(1)
            elif answer == "break":
                break
            else:
                wordFeature.append(0)
            print(wordFeature) #!!!!!!!!!!!!!!!!!!!!

            out = csv.writer(csvf, delimiter=',', lineterminator = '\n')
            out.writerow(wordFeature)

            for number in wordFeature :
                tf.write(str(number)+",")
            tf.write("\n")

    
tf.close()
csvf.close()