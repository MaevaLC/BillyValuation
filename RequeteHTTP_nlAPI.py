# -*- coding: utf-8 -*-
"""
Created on Wed May 10 11:59:58 2017

@author: m.leclech
"""

import requests   
import json
from pprint import pprint

#requete du jeton google
f = open("cred/tokenMagic.txt","r")
tokenMagic = f.readline()
reqJeton = requests.get("http://neptune2.estia.fr/api/googleToken?token="+tokenMagic)
tokenSeance = reqJeton.json() #type = dict
tokenGoogle=tokenSeance['token']['access_token']

#requete pour annotate
r = requests.post("https://language.googleapis.com/v1beta2/documents:annotateText",
                  json = {"document":{
                              "type":"PLAIN_TEXT",
                              "content":"Le chat est grand."
                              },
                          "features":{
                              "extractSyntax": True,
                              "extractEntities": True,
                              "extractDocumentSentiment": True
                              },
                          "encodingType": "UTF8",
                          },
                  headers = {"authorization": "Bearer "+ tokenGoogle}
                  ).json()
                  

#sauvegarde du json
with open('annotatedText.json', 'w') as f:
    f.write(json.dumps(r, indent=4))
pprint(r)
    
