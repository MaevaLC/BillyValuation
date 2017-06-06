# -*- coding: utf-8 -*-
"""
Created on Mon May 29 13:53:38 2017

@author: m.leclech
"""


import json
import os



url = "neptune2.estia.fr"
seance = 2



def eliminate(jsonFile):
    with open(jsonFile) as f:
        annotatedText = json.load(f)
        for word in annotatedText["tokens"]:
                if word["dependencyEdge"]["label"] == "AMOD":
                    annotatedText["tokens"].remove(word)
        return annotatedText["tokens"]
        

files = []
for element in os.listdir("res/annotatedText/"+url+"/"+str(seance)):
    if element.endswith('.json'):
        files.append(element)

for file in files:    
    with open("res/annotatedText/"+url+"/"+str(seance)+"/"+file) as f:
        annotatedText = json.load(f)
    sentence = ""
    for word in annotatedText["tokens"]:
        sentence += word["text"]["content"] + " "
    print(sentence)    
    e = eliminate("res/annotatedText/"+url+"/"+str(seance)+"/"+file)
    sentenceE =""
    for word in e:
        sentenceE += word["text"]["content"] + " "
    print (sentenceE)
    print("")
        