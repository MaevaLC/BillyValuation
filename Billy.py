# -*- coding: utf-8 -*-
"""
Created on Fri May  5 09:22:02 2017

@author: m.leclech
"""

import requests
from pprint import pprint
import json

global tokenSeance
global tokenMagic

f = open("cred/tokenMagic.txt","r")
tokenMagic = f.readline()

def Seance():
    global tokenMagic
    seance = requests.get("http://ideavaluation.estia.fr/api/seance/list?token="+tokenMagic)
    listeSeanceJ = seance.json() #type = list of dict
    print (listeSeanceJ)

def RequestToken(idSeance):
    global tokenSeance
    global tokenMagic
    r = requests.get("http://ideavaluation.estia.fr/api/seance/"+str(idSeance)+"/token?token="+tokenMagic)
    tokenSeance = r.text #type = str
    return tokenSeance
    
def GetData():
    message=[]
    data_json = requests.get("http://ideavaluation.estia.fr/api/message/all?token="+tokenSeance).json()
    
    with open('data_messages.json', 'w') as f:
        f.write(json.dumps(data_json, indent=4))    
    
    #dict de 2 elments (success : boolean et result : list de dict)
    for i in range(len(data_json['result'])) :  #data_json['result'] est une list de dict
        dictionnaire = data_json['result'][i]   #on recup le ieme dict de la list
        message.append(dictionnaire['text'])    #on recup le texte du dict
    pprint (message)
    return message

def DecodeJson():
    print ('')



#Seance()                           #Connaitre les sceances
RequestToken(2)                    #Preciser la sceance pour obtenir le jeton approprié
GetData()                          #Recuperer les messages
#convertir
#traiter
#reconvertir
#envoyer

# a ajouter : url en argument
