# -*- coding: utf-8 -*-
"""
Created on Tue May 16 09:02:22 2017

@author: m.leclech
"""

#import
import json
from graphics import Point, Text, GraphWin

#open the file with the annotated text
with open('annotatedText.json', 'r') as f:
    annotatedText = json.load(f)

#list where dependency is done by specifying its parents (Google way)
listeDependencyParent =[]
#list where dependency is done by specifying its children (the way my Nodes work)
listeDependencyChildren =[]

#filling the list Parent with the data from the file -> [2] in a int with the index of the Parent
for i in range(len(annotatedText["tokens"])):
    annotatedWord= annotatedText["tokens"][i]
    dependency = (annotatedWord["dependencyEdge"]["headTokenIndex"])
    text = (annotatedWord["text"]["content"])
    listeDependencyParent.append([text,i,dependency])
    
#reversing the data to make the list Children -> now [2] is a list with the index of children
for i in range(len(listeDependencyParent)):
    listeEnfant = []
    for j in range(len(listeDependencyParent)):
        if listeDependencyParent[i][1] == listeDependencyParent[j][2] :
            listeEnfant.append(j)
    listeDependencyChildren.append([listeDependencyParent[i][0],listeDependencyParent[i][1],listeEnfant])
    
#creation of a class for my Node
class Node:
    """ Classe definissant un noeud d'un arbre """
    
    #constructor
    def __init__(self, text, position, lemme, pos, dependencyEdge, childPosition):
        self.text = text
        self.position = position
        self.lemme = lemme
        self.pos = pos
        self.dependencyEdge = dependencyEdge
        self.childPosition = childPosition
        
#liste of Node made with the listeDependencyChildren
#listeDependencyChildren does not have all the info required by the constructor yet, will be added later if needed
listeNode = []
for i in range(len(listeDependencyChildren)) :
    listeNode.append(Node(listeDependencyChildren[i][0],listeDependencyChildren[i][1],"none","none","none",listeDependencyChildren[i][2]))

#definition of the Board to print the tree
board = GraphWin("My Board", 1500, 700)
#def of my anchor for the first point, will try to make it dynamic later
longueur = 100
hauteur = 100

#list of the words put on the Board
listeMotPlace=[]

#i plan to make everything a function to make it cleaner, but for now i made it only for the root
#so yup this function found for the root, draw it and add it to the listMotPlace
def setupRoot():
    for i in listeDependencyChildren :
        if i[1] in i[2] :
            root = Text(Point(longueur,hauteur),i[0])
            root.draw(board)
            board.getMouse()  #can get annotated, it just to make a pause
            listeMotPlace.append(i)
            return root            
setupRoot()

#while every word in not in place on the board, continue to place them
i=1        
while len(listeMotPlace)<len(listeDependencyChildren):
    mot = listeMotPlace[i-1]
    for j in mot[2]:
        if j == listeMotPlace[0][2][0] :
            pass    #since the root refer to itself as children, small trick to not make it duplicate to infinite
        else :
            motEnfant = listeDependencyChildren[j]
            Text(Point(longueur+50*j,hauteur +30*i),motEnfant[0]).draw(board) #print the word on the board, position need to be adjusted
            listeMotPlace.append(listeDependencyChildren[j]) #add the word to the listMotPlace
            board.getMouse()    #can get annotated, it just to make a pause
    i+=1


board.getMouse() # pause, wait for a click on the window
board.close()  #board get closed properly


