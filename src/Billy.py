# -*- coding: utf-8 -*-
"""
Created on Fri May  5 09:22:02 2017

@author: m.leclech
"""


import json
import requests

from AnnotateText import annotateText
from Token import getMagicToken, requestSeanceToken


def getSeanceList(url):
    """Return the list of seance for this server
    
    Args:
        url (string): the url of the server
    Returns:
        a list of seances (list of dict)
        
    """    
    
    seanceList = requests.get("http://"+url+"/api/seance/list?token="
                                   +getMagicToken()).json()
    return seanceList
 
   
def getMessageList(url, idSeance):
    """Get a list of the "text" attribute of all messages
    
    Args:
        url (string): the url of the server
        idSeance (int): the id of the seance
    Returns:
        a list of messages (list of string)
    """ 
    
    messageList=[]
    data_json = requests.get("http://"+url+"/api/message/all?token="
                                      +requestSeanceToken(url, idSeance)).json()    
    with open('data_messages.json', 'w') as f:
        f.write(json.dumps(data_json, indent=4)) # save the data as json.
    for message in data_json['result']:  
        messageList.append(message['text'])  
    return messageList


def annotateData(url, seance, listMessage):
    """Annotate a list of text message with Googe Natural Language API
    
    Args:
        url (string): the url of the server
        idSeance (int): the id of the seance
        listMessage (list of string): the messages to annotate
    Returns:
        None 
        Create files with the data in ./annotatedText/:url/:seance
        
    """    
    
    for message in listMessage:
        annotateText(url, seance, message)  #import from RequeteHTTP_nlAPI


if __name__ == '__main__':  
    url = "neptune1.estia.fr"
    idSeance = 2
    print(getSeanceList(url))  #Connaitre les sceances
    #listeMessage = getMessageList(url, idSeance)  #Recuperer les messages
    #annotateData(url, idSeance, listeMessage)  #Les annote via Google NL API


