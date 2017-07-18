# -*- coding: utf-8 -*-
"""
Created on Fri May 12 13:51:00 2017

@author: m.leclech
"""

#import
import json
from pprint import pprint
from anytree import Node, RenderTree

#open the file with the annotated text
with open('annotatedText.json', 'r') as f:
    annotatedText = json.load(f)

#these node need to be declared as var, so i tried to stack them in the list to not have to name them
listeNode =[]
#create a list and filling it witht he data needed for Nodes (word, position, position of its parent)
listeDependency =[]
for i in range(len(annotatedText["tokens"])):
    annotatedWord= annotatedText["tokens"][i]
    Dependency = (annotatedWord["dependencyEdge"]["headTokenIndex"])
    Text = (annotatedWord["text"]["content"])
    listeDependency.append((Text,i,Dependency))
        

#trouver le root
for i in range(len(listeDependency)):
    if listeDependency[i][1] == listeDependency[i][2] :   #if a word is its own parent, it's the root
        text = listeDependency[i][0]
        indexRoot = listeDependency[i][2]
        root = Node(text)    #Node of the root (one arg only, no parent)
        listeNode.append(root)   
        break
        print(listeDependency)

# WiP : i should do each node, just some scratch right now
#for i in range(len(listeDependency)):
#    if listeDependency[i][2] :
#        listeNode.append(Node(listeDependency[i][0],parent=listeNode[0]))
#how you're suppoed to create a Node : chat = Node("chat", parent=root)

#you print the Tree
for pre, fill, node in RenderTree(root):
    print("%s%s" % (pre, node.name))



