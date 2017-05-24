# -*- coding: utf-8 -*-
"""
Created on Thu May 18 09:43:13 2017

@author: m.leclech
"""


import json
import os
import requests

from Token import requestSeanceToken


def listLabelWords(url, seance, wordLabel):
    """Function to list all words with a certain LABEL in a seance
    
    Args:
        url (string): the url of the server the jsonFile come from
        seance (int): the id of the seance the jsonFile come from
        wordLabel (string): https://goo.gl/5htKX0
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
                if word["dependencyEdge"]["label"] == wordLabel:
                    listWords.append(word)
    return listWords


def listTagWords(url, seance, wordTag):
    """Function to list all words with a certain TAG in a seance
    
    Args:
        url (string): the url of the server the jsonFile come from
        seance (int): the id of the seance the jsonFile come from
        wordTag (string): https://goo.gl/yX4gPH
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
        a dict {success: boolean}
    
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
        a dict {success: boolean, tokenId: int}
    
    """
    
    tokenSeance = requestSeanceToken(url, seance)
    request = requests.post("http://"+url+"/api/lexique/"+str(lexiconId)+"/add",
                      json = {"token": tokenSeance,
                              "lemme": lemme,
                              "text": text,
                              "partOfSpeech": pos,
                              }).json()
    return request
