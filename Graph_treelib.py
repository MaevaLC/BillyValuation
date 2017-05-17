# -*- coding: utf-8 -*-
"""
Created on Mon May 15 11:14:09 2017

@author: m.leclech
"""

from treelib import Tree
import json

with open('annotatedText.json', 'r') as f:
    annotatedText = json.load(f)

listeDependency =[]

for i in range(len(annotatedText["tokens"])):
    annotatedWord= annotatedText["tokens"][i]
    Dependency = (annotatedWord["dependencyEdge"]["headTokenIndex"])
    Text = (annotatedWord["text"]["content"])
    listeDependency.append([Text,i,Dependency])
        



tree=Tree()
indexRoot=0
indexMotPlace=[]
j=0
c=1

#trouver le root
for i in range(len(listeDependency)):
    if listeDependency[i][1] == listeDependency[i][2] :
        text = listeDependency[i][0]
        position = listeDependency[i][1]
        indexRoot = listeDependency[i][2]
        tree.create_node(text,position)
        indexMotPlace.append(indexRoot)
        tree.show()
        print(listeDependency)
        break
        

#relier ce qui depend de root
while len(indexMotPlace)<len(listeDependency):
    for i in range(len(listeDependency)) :
        if i in indexMotPlace :
            pass
        elif indexRoot == listeDependency[i][2] :
            listeDependency[i][0] = str(c)+" "+listeDependency[i][0]
            tree.create_node(listeDependency[i][0],listeDependency[i][1],parent=indexRoot)
            indexMotPlace.append(i)
            c+=1
            tree.show()
    j=j+1
    c=1
    indexRoot=indexMotPlace[j]
      
tree.show()
        
    

