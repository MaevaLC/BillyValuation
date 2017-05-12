# -*- coding: utf-8 -*-
"""
Created on Fri May 12 13:51:00 2017

@author: m.leclech
"""

import json
from pprint import pprint

with open('annotatedText.json', 'r') as f:
    annotatedText = json.load(f)

listeDependency =[]
listeText = []

for i in range(len(annotatedText["tokens"])):
    annotatedWord= annotatedText["tokens"][i]
    listeDependency.append(annotatedWord["dependencyEdge"]["headTokenIndex"])
    listeText.append(annotatedWord["text"]["content"])
        
    
    
    
    pprint(annotatedWord)
    pprint(listeDependency)
    pprint(listeText)