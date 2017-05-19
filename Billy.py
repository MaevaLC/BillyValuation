# -*- coding: utf-8 -*-
"""
Created on Fri May  5 09:22:02 2017

@author: m.leclech
"""


import json
import requests

from RequeteHTTP_nlAPI import annotateText


global tokenSeance
global tokenMagic


def seance(url):
    """Take the url of the server (ideavaluation.estia.fr or neptune2.estia.fr,
    print the list of seances with their id"""    
    
    global tokenMagic
    seance = requests.get("http://"+url+"/api/seance/list?token="+tokenMagic)
    listeSeanceJ = seance.json() #type = list of dict
    print (listeSeanceJ)


def requestToken(url, idSeance):
    """Request a token from the server to be able to fetch data for a sceance
    url is the one of the server (str), idSeance is the id of the seance (int)"""    
    
    global tokenSeance
    global tokenMagic
    r = requests.get("http://"+url+"/api/seance/"+str(idSeance)+"/token?token="+tokenMagic)
    tokenSeance = r.text #type = str
    return tokenSeance
 
   
def getData(url):
    """Fetch the data from the server (url as an string),
    return a list with the sentence in it (list of str)
    you don't need to specify the seance's id since its link to the tokenSeance""" 
    
    message=[]
    #fetch the data and save it as a json (not useful for now, might be for future update)
    data_json = requests.get("http://"+url+"/api/message/all?token="+tokenSeance).json()    
    with open('data_messages.json', 'w') as f:
        f.write(json.dumps(data_json, indent=4))
    #data_json is a dict of 2 element (success : boolean & result : list of dict)
    for i in range(len(data_json['result'])):  #data_json['result'] is a list of dict
        dictionnaire = data_json['result'][i]  #we work on the i-th dict of the list
        message.append(dictionnaire['text'])  #the text of this element is add to the list of message
    return message


def annotateData(url, seance, listMessage):
    """Use RequeteHTTP_nlAPI to annotate each message one after another in the list
    url (str) and seance (int) are needed to classify the result in the corret path"""    
    
    for message in listMessage:
        annotateText("neptune2.estia.fr", 2, message)
    

#WILL NEED TO MAKE A MAIN HERE TO MAKE IT EASIER
f = open("cred/tokenMagic.txt","r")  #recuperation du token Magic
tokenMagic = f.readline()
f.close()

#Seance("ideavaluation.estia.fr")  #Connaitre les sceances
requestToken("neptune2.estia.fr", 2)  #Preciser la sceance pour obtenir le jeton approprié
listeMessage = getData("neptune2.estia.fr")  #Recuperer les messages
annotateData("neptune2.estia.fr", 2, listeMessage)  #Les annote via Google NL API


