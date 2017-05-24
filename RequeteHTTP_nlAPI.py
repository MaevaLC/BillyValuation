# -*- coding: utf-8 -*-
"""
Created on Wed May 10 11:59:58 2017

@author: m.leclech
"""


import hashlib
import json
import os
import requests  

from Billy import getMagicToken


def hashSentence(stringToHash):
    """Return a string hashed (md5)"""    
    
    hashString = hashlib.md5((stringToHash).encode()).hexdigest()
    return hashString


def requestGoogleToken(url):
    """Request a token to use with Google API Auth
    
    Args:
        url (string): the server you'll ask from
                      idevaluation.estia.fr or neptune2.estia.fr
    Returns:
        a token to use Natural Language API
                      
    """    
    
    magicToken = getMagicToken()
    tokenRequest = requests.get("http://"+url+"/api/googleToken?token="
                                         +magicToken).json()
    googleToken = tokenRequest['token']['access_token']
    return googleToken


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
                          headers = {"authorization": "Bearer"
                                     + requestGoogleToken(url)}
                          ).json()
        #json named after the message content
        with open(path+"/"+hashSentence(message)+".json", 'w') as f:
            f.write(json.dumps(r, indent=4))