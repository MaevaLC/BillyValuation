# -*- coding: utf-8 -*-
"""
Created on Wed May 10 11:59:58 2017

@author: m.leclech
"""

import requests   
import json
import hashlib

#function to hash the phrase to name the file
def hash (phraseToHash) :
    hash_object = hashlib.md5((phraseToHash).encode())
    return(hash_object.hexdigest())

#request for a Google Token via IdeaValuation's server
def requestGoogleToken(url) :
    f = open("cred/tokenMagic.txt","r")
    tokenMagic = f.readline()
    reqJeton = requests.get("http://"+url+"/api/googleToken?token="+tokenMagic)
    tokenSeance = reqJeton.json() #type = dict
    tokenGoogle=tokenSeance['token']['access_token']
    return tokenGoogle

#create an json with the annotated file in it
def annotateText(message,url) :
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
    #json named after the message name
    with open("annotatedText/"+hash(r["sentences"][0]["text"]["content"])+".json", 'w') as f:
        f.write(json.dumps(r, indent=4))
 
#call of the function   
annotateText("Bonus financier ou bons d'achats pour les bons élèves si apport en déchèterie par exemple.", "ideavaluation.estia.fr")  #or neptune2