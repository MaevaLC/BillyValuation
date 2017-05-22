# -*- coding: utf-8 -*-
"""
Created on Tue May 16 09:02:22 2017

@author: m.leclech
"""


import json

from graphics import Point, Text, GraphWin


global compteur


def fillListParent(pathFile):
    """Filling the list Parent with the data from the file -> [2] in a int with the index of the Parent"""    
    
    #list where dependency is done by specifying its parents (Google way)
    listeDependencyParent =[]    
    with open(pathFile, "r") as f:
        annotatedText = json.load(f)
        for i in range(len(annotatedText["tokens"])):
            annotatedWord= annotatedText["tokens"][i]
            dependency = (annotatedWord["dependencyEdge"]["headTokenIndex"])
            text = (annotatedWord["text"]["content"])
            listeDependencyParent.append([text,i,dependency])
    return listeDependencyParent
    

def fillListChildren(listeDependencyParent):
    """Reversing the data to make the list Children -> now [2] is a list with the index of children ="""    
    
    #list where dependency is done by specifying its children (the way my Nodes work)
    listeDependencyChildren =[]
    for i in range(len(listeDependencyParent)):
        listeEnfant = []
        for j in range(len(listeDependencyParent)):
            if listeDependencyParent[i][1] == listeDependencyParent[j][2] :
                listeEnfant.append(j)
        listeDependencyChildren.append([listeDependencyParent[i][0],listeDependencyParent[i][1],listeEnfant])
    return listeDependencyChildren
    

class Node:
    """Class to define a node in the tree"""
    
    def __init__(self, text, position, lemme, pos, dependencyEdge, childPosition):
        """Constructor"""
        
        self.text = text
        self.position = position
        self.lemme = lemme
        self.pos = pos
        self.dependencyEdge = dependencyEdge
        self.childPosition = childPosition
 

def createListNode(listeDependencyChildren):
    """List of Node made with the listeDependencyChildren
    
    listeDependencyChildren does not have all the info required by the constructor yet, will be added later if needed"""    
    
    listeNode = []
    for i in range(len(listeDependencyChildren)) :
        listeNode.append(Node(listeDependencyChildren[i][0],listeDependencyChildren[i][1],"none","none","none",listeDependencyChildren[i][2]))
    return listeNode


def findRootIndex(listeDependencyChildren):
    """Find the root's index"""
    
    for i in listeDependencyChildren :
        if i[1] in i[2] :
            return i[1]


def countOfParent(listeDependencyParent, indexWord):
    """Find the number of parent a word have, given the list of all dependency"""
    
    global compteur
    motEnfant = listeDependencyParent[indexWord]
    if (motEnfant[1] != motEnfant[2]):
        compteur+=1        
        countOfParent(listeDependencyParent, motEnfant[2])    
    return compteur


def setupRoot(board, longueur, hauteur, listeDependencyChildren):
    """Find the root, draw it and add it to the listMotPlace"""   
    
    listeMotPlace=[]
    for i in listeDependencyChildren :
        if i[1] in i[2] :
            root = Text(Point(longueur,hauteur),i[0])
            root.draw(board)
            board.getMouse()  #can get annotated, it just to make a pause
            listeMotPlace.append(i)
            return listeMotPlace


def setupRestOfWords(board, longueur, hauteur, listeMotPlace, listeDependencyChildren, listeDependencyParent):
    """While every word in not in place on the board, continue to place them"""
    
    global compteur
    i = 1        
    while len(listeMotPlace)<len(listeDependencyChildren):
        mot = listeMotPlace[i-1]
        for j in mot[2]:
            if j == listeMotPlace[0][2][0] :
                pass    #since the root refer to itself as children, small trick to not make it duplicate to infinite
            else :
                compteur = 0                
                motEnfant = listeDependencyChildren[j]
                Text(Point(longueur+75*j,hauteur+countOfParent(listeDependencyParent,j)*50),motEnfant[0]).draw(board) #print the word on the board, position need to be adjusted
                listeMotPlace.append(listeDependencyChildren[j]) #add the word to the listMotPlace
                board.getMouse()    #can get annotated, it just to make a pause
        i += 1
    board.getMouse() # pause, wait for a click on the window
    board.close()  #board get closed properly
    

def drawTree(pathFile):
    """Draw the tree of the annotatedFile provided"""
    
    global longueur
    global hauteur
    listeParent = fillListParent(pathFile)
    listeChildren = fillListChildren(listeParent)    
    #definition of the Board to print the tree
    lengthBoard = 1500
    heightBoard = 700
    board = GraphWin("My Board", lengthBoard, heightBoard)
    #def of my anchor for the first point
    longueur = (findRootIndex(listeChildren)/len(listeChildren)) * lengthBoard + 100
    hauteur = (findRootIndex(listeChildren)/len(listeChildren)) * heightBoard + 100
    #place the words
    liste = setupRoot(board, longueur, hauteur, listeChildren)
    setupRestOfWords(board, longueur, hauteur, liste, listeChildren, listeParent)
    
#test
#drawTree('annotatedText.json')