# -*- coding: utf-8 -*-
"""
Created on Fri May 12 13:51:00 2017

@author: m.leclech
"""

import json
from pprint import pprint
from anytree import Node, RenderTree

with open('annotatedText.json', 'r') as f:
    annotatedText = json.load(f)

listeDependency =[]
listeNode =[]

for i in range(len(annotatedText["tokens"])):
    annotatedWord= annotatedText["tokens"][i]
    Dependency = (annotatedWord["dependencyEdge"]["headTokenIndex"])
    Text = (annotatedWord["text"]["content"])
    listeDependency.append((Text,i,Dependency))
        
pprint(listeDependency)

#trouver le root
for i in range(len(listeDependency)):
    if listeDependency[i][1] == listeDependency[i][2] :
        text = listeDependency[i][0]
        indexRoot = listeDependency[i][2]
        root = Node(text)
        listeNode.append(root)
        break
        print(listeDependency)


#for i in range(len(listeDependency)):
#    if listeDependency[i][2] :
#        listeNode.append(Node(listeDependency[i][0],parent=listeNode[0]))
    


#chat = Node("chat", parent=root)

for pre, fill, node in RenderTree(root):
    print("%s%s" % (pre, node.name))



