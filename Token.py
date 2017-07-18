# -*- coding: utf-8 -*-
"""
Created on Wed May 24 15:58:49 2017

@author: m.leclech
"""


import requests


def getMagicToken():
    """Return the magic token"""    
    
    with open("cred/tokenMagic.txt","r") as f:
        magicToken = f.readline()
    return magicToken


def requestSeanceToken(url, idSeance):
    """Request a token from the server to access a specific seance
    
    Args:
        url (string): the url of the server
        idSeance (int): the id of the seance
    Returns:
        the Token needed (string)
        
    """    
    
    seanceToken = requests.get("http://"+url+"/api/seance/"
                                        +str(idSeance)+"/token?token="
                                        +getMagicToken()).text
    return seanceToken


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