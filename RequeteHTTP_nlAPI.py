# -*- coding: utf-8 -*-
"""
Created on Wed May 10 11:59:58 2017

@author: m.leclech
"""


import hashlib
import json
import os
import requests  


def hashSentence(sentenceToHash):
    """Take a string, return a string hashed (md5)"""    
    
    hash_object = hashlib.md5((sentenceToHash).encode())
    return(hash_object.hexdigest())


def requestGoogleToken(url):
    """Request a token to use with Google API Auth 
    The url arg is the server, idevaluation.estia.fr or neptune2.estia.fr"""    
    
    f = open("cred/tokenMagic.txt","r")
    tokenMagic = f.readline()
    reqJeton = requests.get("http://"+url+"/api/googleToken?token="+tokenMagic)
    tokenSeance = reqJeton.json() #type = dict
    tokenGoogle=tokenSeance['token']['access_token']
    return tokenGoogle


def annotateText(url, seance, message):
    """Take the url of the server as a string (idevaluation.estia.fr, neptune2.estia.fr), 
    an int seance which is the id of the sceance where the message come from, 
    and the message as a string which need to be annotated
    and in return create a json file with the data in annotatedText/:url/:seance"""    
    
    #create dirs if not existing yet
    if os.path.exists("annotatedText/"+url+"/"+str(seance)) == False:
        os.makedirs("annotatedText/"+url+"/"+str(seance)) 
    #check that the sentence isn't already annotated
    if os.path.isfile("annotatedText/"+url+"/"+str(seance)+"/"+hashSentence(message)+".json") == False :
        #request to annotate
        r = requests.post("https://language.googleapis.com/v1beta2/documents:annotateText",
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
                          headers = {"authorization": "Bearer "+ requestGoogleToken(url)}
                          ).json()
        #json named after the message content
        with open("annotatedText/"+url+"/"+str(seance)+"/"+hashSentence(message)+".json", 'w') as f:
            f.write(json.dumps(r, indent=4))