# -*- coding: utf-8 -*-
"""
Created on Thu May 18 09:43:13 2017

@author: m.leclech
"""


import json
import os
import requests

from Billy import requestSeanceToken
from pprint import pprint
   
                 
def wordTag(url, seance, jsonFile, wordIndex):
    """Returns the tag of the word you specify 

    Args:
        url (string): the url of the server the jsonFile come from
        seance (int): the id of the seance the jsonFile come from
        jsonFile (string): the name of the json file (including the .json)
        wordIndex: the position of the word in the sentence
    Returns:
        a string, which is the tag attribute of the word
    
    """

    with open("annotatedText/"+url+"/"+str(seance)+"/"+jsonFile, 'r') as f:
        annotatedText = json.load(f) 
        if wordIndex >= len(annotatedText["tokens"]):
            raise ValueError("There isn't that many word in the sentence")
        word = annotatedText["tokens"][wordIndex]
        wordTag = word["partOfSpeech"]["tag"]
        return wordTag


def wordLabel(url, seance, jsonFile, wordIndex):
    """Returns the label of the word you specify 

    Args:
        url (string): the url of the server the jsonFile come from
        seance (int): the id of the seance the jsonFile come from
        jsonFile (string): the name of the json file (including the .json)
        wordIndex: the position of the word in the sentence
    Returns:
        a string, which is the label attribute of the word
    
    """

    with open("annotatedText/"+url+"/"+str(seance)+"/"+jsonFile, 'r') as f:
        annotatedText = json.load(f) 
        if wordIndex >= len(annotatedText["tokens"]):
            raise ValueError("There isn't that many word in the sentence")
        word = annotatedText["tokens"][wordIndex]
        wordTag = word["dependencyEdge"]["label"]
        return wordTag


def listWords(url, seance, wordTag):
    """Function to list all words with a certain TAG in a seance
    
    Args:
        url (string): the url of the server the jsonFile come from
        seance (int): the id of the seance the jsonFile come from
        wordTag (string): ADJ, ADP, ADV, CONJ, DET, NOUN, NUM, PRON, PRT, PUNCT, VERB
    Returns:
        the list of words corresponding (list of dict)
    
    """    
    
    files = []
    for element in os.listdir("annotatedText/"+url+"/"+str(seance)):
        if element.endswith('.json'):
            files.append(element)
    listWords = []
    for file in files:
        with open("annotatedText/"+url+"/"+str(seance)+"/"+file, 'r') as f:
            annotatedText = json.load(f)            
            for word in annotatedText["tokens"]:
                if word["partOfSpeech"]["tag"] == wordTag:
                    listWords.append(word)
    return listWords
    
    
def listLexicon(url, seance):
    """Return the list of lexicons existing
    
    Args:
        url (string): the url of the server
        seance (int): the id of the seance
    Returns:
        a dict {success: boolean, lexiques: []}
    
    """
    
    tokenSeance = requestSeanceToken(url, seance)
    request = requests.get("http://"+url
                            +"/api/lexique/list?token="+tokenSeance).json()  
    return request


def createLexicon(url, seance, name, description=""):
    """Create a new lexicon
    
    Args:
        url (string): the url of the server the lexicon will relate to
        seance (int): the id of the seance the lexicon will relate to
        name (string): the name of the new lexicon
        [description] (string): a global idea of the theme of the lexicon
    Returns:
        a dict {success: boolean, *****A COMPLETER*****}
    
    """
    
    tokenSeance = requestSeanceToken(url, seance)
    request = requests.post("http://"+url+"/api/lexique/create",
                      json = {"token": tokenSeance,
                              "name": name,
                              "description": description,
                              }).json()
    return request


def listWordsLexicon(url, seance, lexiconName):
    """Return the list with all the words of a lexicon
    
    Args:
        url (string): the url of the server the lexicon relate to
        seance (int): the id of the seance the lexicon relate to
        lexiconName (string): the name of the lexicon
    Returns:
        a dict {success: boolean, tokens: []}
        
    """

    tokenSeance = requestSeanceToken(url, seance)
    request = requests.get("http://"+url
                            +"/api/lexique/"+lexiconName
                            +"/all?token="+tokenSeance).json()  
    return request
    
 
def addWordToLexicon(url, seance, lexiconId, lemme, text, pos):
    """Add a word to the lexicon
    
    Args:
        url (string): the url of the server the word relate to
        seance (int): the id of the seance the word relate to
        lexiconId (int): the id of the lexicon in which the word will be added
        lemme (string): the lemme of the word
        text (string): the word itself
        pos (string): "part of speech" of the word
    Returns:
        a dict {success: boolean, *****A COMPLETER*****}
    
    """
    
    tokenSeance = requestSeanceToken(url, seance)
    request = requests.post("http://"+url+"/api/lexique/"+str(lexiconId)+"/add",
                      json = {"token": tokenSeance,
                              "lemme": lemme,
                              "text": text,
                              "partOfSpeech": pos,
                              }).json()
    return request
 

#function call        
#print("liste adjectif")     
#print(listTypeWord("neptune2.estia.fr",2,"ADJ"))
#print(wordTag("neptune2.estia.fr", 2, "6e5b7aa8dc9c1dc011fcb0c83d5141a5.json", 7))

pprint(listLexicon("neptune2.estia.fr", 2))
#pprint(createLexicon("neptune2.estia.fr", 2, "plop"))
#pprint(listWordsLexicon("neptune2.estia.fr", 2, "toto"))
#pprint(addWordToLexicon("neptune2.estia.fr", 2, 1, "ta", "tatata", "pobj"))
