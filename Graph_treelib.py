# -*- coding: utf-8 -*-
"""
Created on Mon May 15 11:14:09 2017

@author: m.leclech
"""

#imports
from treelib import Tree
import json


#open the file with the annotated text
with open('annotatedText.json', 'r') as f:
    annotatedText = json.load(f)

#create a list and filling it witht he data needed for Nodes (word, position, position of its parent)
listeDependency =[]
for i in range(len(annotatedText["tokens"])):
    annotatedWord= annotatedText["tokens"][i]
    Dependency = (annotatedWord["dependencyEdge"]["headTokenIndex"])
    Text = (annotatedWord["text"]["content"])
    listeDependency.append([Text,i,Dependency])
        
#creation of the tree
tree=Tree()

#List of the position of words put in the Tree
indexMotPlace=[]
#finding the root and putting it in the list
for i in range(len(listeDependency)):
    if listeDependency[i][1] == listeDependency[i][2] :
        text = listeDependency[i][0]
        position = listeDependency[i][1]
        indexRoot = listeDependency[i][2]
        tree.create_node(text,position)  #creation of the node
        indexMotPlace.append(indexRoot)  #root added in the list
        print(listeDependency)
        break
 
# var needed for the next algo       
j=0
c=1  
#while everyword hasn't been placed in the tree, continue to place them
while len(indexMotPlace)<len(listeDependency):
    for i in range(len(listeDependency)) :
        if i in indexMotPlace :
            pass   #if the word is already in the tree, skip it
        elif indexRoot == listeDependency[i][2] :
            listeDependency[i][0] = str(c)+" "+listeDependency[i][0]  #add a number in front of the word to keep them in order
            tree.create_node(listeDependency[i][0],listeDependency[i][1],parent=indexRoot)  #creation of the Node in the Tree
            indexMotPlace.append(i)   #add the word in the list of word placed in the tree
            c+=1
    j=j+1
    c=1
    indexRoot=indexMotPlace[j]
 
#affichage de l'arbre     
tree.show()
        
    

