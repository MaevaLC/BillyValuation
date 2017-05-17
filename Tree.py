# -*- coding: utf-8 -*-
"""
Created on Tue May 16 09:02:22 2017

@author: m.leclech
"""

import json
from pprint import pprint
from graphics import Point, Text, GraphWin

with open('annotatedText.json', 'r') as f:
    annotatedText = json.load(f)

listeDependencyParent =[]
listeDependencyChildren =[]

for i in range(len(annotatedText["tokens"])):
    annotatedWord= annotatedText["tokens"][i]
    dependency = (annotatedWord["dependencyEdge"]["headTokenIndex"])
    text = (annotatedWord["text"]["content"])
    listeDependencyParent.append([text,i,dependency])
    
#pprint(listeDependencyParent)

for i in range(len(listeDependencyParent)):
    listeEnfant = []
    for j in range(len(listeDependencyParent)):
        if listeDependencyParent[i][1] == listeDependencyParent[j][2] :
            listeEnfant.append(j)
    listeDependencyChildren.append([listeDependencyParent[i][0],listeDependencyParent[i][1],listeEnfant])
    
#pprint(listeDependencyChildren)
    
    

class Node:
    """ Classe definissant un noeud d'un arbre """
    
    def __init__(self, text, position, lemme, pos, dependencyEdge, childPosition):
        self.text = text
        self.position = position
        self.lemme = lemme
        self.pos = pos
        self.dependencyEdge = dependencyEdge
        self.childPosition = childPosition
        

        
listeNode = []
for i in range(len(listeDependencyChildren)) :
    listeNode.append(Node(listeDependencyChildren[i][0],listeDependencyChildren[i][1],"none","none","none",listeDependencyChildren[i][2]))

board = GraphWin("My Board", 1500, 700)
longueur = 100
hauteur = 100

listeMotPlace=[]

print(listeDependencyChildren)

def setupRoot():
    for i in listeDependencyChildren :
        if i[1] in i[2] :
            root = Text(Point(longueur,hauteur),i[0])
            listeMotPlace.append(i)
            return root
            
root = setupRoot()
root.draw(board)
board.getMouse()

i=1        
while len(listeMotPlace)<len(listeDependencyChildren):
    mot = listeMotPlace[i-1]
    for j in mot[2]:
        if j == listeMotPlace[0][2][0] :
            pass
        else :
            motEnfant = listeDependencyChildren[j]
            #ecrire le mot position j
            Text(Point(longueur+50*j,hauteur +30*i),motEnfant[0]).draw(board)
            #l'ajouter à la liste des mots place
            listeMotPlace.append(listeDependencyChildren[j])
            board.getMouse()
    i+=1


board.getMouse() # pause for click in window
board.close()


