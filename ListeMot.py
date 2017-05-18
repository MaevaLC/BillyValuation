# -*- coding: utf-8 -*-
"""
Created on Thu May 18 09:43:13 2017

@author: m.leclech
"""

#liste à mettre sur Neptune2

#import
import json
import os

#function to list the word with a certain TAG such a as ADJ, ADP, NOUN, VERB
def listTypeWord(typeWord) :
    fichiers = []    #list of annotated data
    for element in os.listdir('annotatedText'):
        if element.endswith('.json'):
            fichiers.append(element)   #the list is filled with the name of every json in the directory
    
    for fichier in fichiers :                       #load each json file
        with open("annotatedText/"+fichier, 'r') as f:
            annotatedText = json.load(f)            
            for i in range(len(annotatedText["tokens"])):    #for every word
                annotatedWord= annotatedText["tokens"][i]
                if annotatedWord["partOfSpeech"]["tag"] == typeWord :      #return it if it's the type searched
                    print(annotatedWord["lemma"])


#function call        
print("liste adjectif")     
listTypeWord("ADJ") 

print("liste préposition")     
listTypeWord("ADP") 

print("liste verbe")     
listTypeWord("VERB") 
