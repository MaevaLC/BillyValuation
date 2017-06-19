# -*- coding: utf-8 -*-
"""
Created on Wed May 10 11:59:58 2017

@author: m.leclech
"""


import hashlib
import json
import os
import requests  

from src.Token import requestGoogleToken


def hashSentence(stringToHash):
    """Return a string hashed (md5)"""    
    
    hashString = hashlib.md5((stringToHash).encode()).hexdigest()
    return hashString


def annotateText(url, seance, message):
    """Annotate a message
    
    Args:
        url (string): the server the message come from
        seance (string): the seance the message come from
        message (string): the sentence you want to annotate
    Returns:
        None
        Create json files with the data in ./annotatedText/:url/:seance
    
    """    
    
    path = "annotatedText/"+url+"/"+str(seance)
    #create dirs if not existing yet
    if os.path.exists(path) == False:
        os.makedirs(path) 
    #check that the sentence isn't already annotated
    if os.path.isfile(path+"/"+hashSentence(message)+".json") == False :
        #request to annotate
        r = requests.post("https://language.googleapis.com"
                         +"/v1beta2/documents:annotateText",
                          json = {"document":{
                                      "type":"PLAIN_TEXT",
                                      "content": message
                                      },
                                  "features":{
                                      "extractSyntax": True,
                                      "extractEntities": True,
                                      "extractDocumentSentiment": True
                                      },
                                  "encodingType": "UTF8",
                                  },
                          headers = {"authorization": "Bearer "
                                     + requestGoogleToken(url)}
                          ).json()
        #json named after the message content
        with open(path+"/"+hashSentence(message)+".json", 'w') as f:
            f.write(json.dumps(r, indent=4))

annotateText("ideavaluation.estia.fr", 2, "coucou")