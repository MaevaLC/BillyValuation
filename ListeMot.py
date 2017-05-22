# -*- coding: utf-8 -*-
"""
Created on Thu May 18 09:43:13 2017

@author: m.leclech
"""


import json
import os
import requests

from Billy import requestToken
from pprint import pprint


def listTypeWord(url, seance, typeWord):
    """Function to list the word with a certain TAG such a as ADJ, ADP, NOUN, VERB 
    url of the server (string), id of the seance (int), type of Word (string)"""    
    
    fichiers = []    #list of annotated data
    for element in os.listdir("annotatedText/"+url+"/"+str(seance)):
        if element.endswith('.json'):
            fichiers.append(element)   #the list is filled with the name of every json in the directory
    listWords = []
    for fichier in fichiers:  #load each json file
        with open("annotatedText/"+url+"/"+str(seance)+"/"+fichier, 'r') as f:
            annotatedText = json.load(f)            
            for i in range(len(annotatedText["tokens"])):    #for every word
                annotatedWord= annotatedText["tokens"][i]
                if annotatedWord["partOfSpeech"]["tag"] == typeWord:  #return it if it's the type searched
                    listWords.append(annotatedWord["lemma"])
    return listWords
   
                 
def typeNextWord(url, seance, jsonFile, indexWord):
    """ Find the type of the word next after the word you specify """

    with open("annotatedText/"+url+"/"+str(seance)+"/"+jsonFile, 'r') as f:
        annotatedText = json.load(f) 
        if len(annotatedText["tokens"]) <= indexWord :
            return "None"
        else :
            nextWord = annotatedText["tokens"][indexWord+1]
            typeNextWord = nextWord["partOfSpeech"]["tag"]
            return typeNextWord


def listLexicon(url, seance):
    """Return the list of the lexicon for the seance (int) on the server (string)"""
    
    tokenSeance = requestToken(url, seance)
    request = requests.get("http://"+url+"/api/lexique/list?token="+tokenSeance).json()  
    pprint(request)


def create(url, seance, name, description=""):
    """Create a new lexicon for this seance (int) on the server (string),
    name and description are string"""
    
    tokenSeance = requestToken(url, seance)
    request = requests.post("http://"+url+"/api/lexique/create",
                      json = {"token": tokenSeance,
                              "name": name,
                              "description": description,
                              })
    r = request.json()
    pprint(r)


def listeWord(url, seance, lexiconName):
    """Return a list with all the word in the lexicon (identified by its name, string),
    for the seance (int) on the server (string)"""

    tokenSeance = requestToken(url, seance)
    request = requests.get("http://"+url+"/api/lexique/"+lexiconName+"/all?token="+tokenSeance).json()  
    pprint(request)
    
 
def addWord(url, seance, lexiconId, lemme, text, pos):
    """Add a word to the lexicon (id, int) for this seance (int) on the server (string),
    Word is define by the word, its lemme and its pos (all string)"""
    
    tokenSeance = requestToken(url, seance)
    request = requests.post("http://"+url+"/api/lexique/"+str(lexiconId)+"/add",
                      json = {"token": tokenSeance,
                              "lemme": lemme,
                              "text": text,
                              "partOfSpeech": pos,
                              })
    r = request.json()
    pprint(r)    


#function call        
print("liste adjectif")     
print(listTypeWord("neptune2.estia.fr",2,"ADJ"))

#listLexicon("neptune2.estia.fr", 2)
#create("neptune2.estia.fr", 2, "plop", "C'est chouette les descriptions")
#listeWord("neptune2.estia.fr", 2, "toto")
#addWord("neptune2.estia.fr", 2, 1, "ta", "tatata", "pobj")
