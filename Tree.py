# -*- coding: utf-8 -*-
"""
Created on Mon May 22 16:43:57 2017

@author: m.leclech
"""


import json

from graphics import Point, Text, GraphWin

width = 800 
height = 600
nodeWidth = 45
nodeHeight = 60   

class Word:
    """Class to define a word, by its lemme, position, parent, children"""
    
    def __init__(self, lemme, position, parent):
        """Constructor"""
    
        self.lemme = lemme
        self.position = position
        self.parent = parent
        self.children = []
        

def createListWords(pathFile):
    """Create a list of objects (Word)
    
    Args: 
        the path of the annotated data file (string)
    Returns: 
        a list containing Word objects (list)
    
    """
    
    listWords = []
    with open(pathFile, "r") as f:
        annotatedText = json.load(f)
        for i in range(len(annotatedText["tokens"])):
            annotatedWord= annotatedText["tokens"][i]
            dependency = (annotatedWord["dependencyEdge"]["headTokenIndex"])
            text = (annotatedWord["text"]["content"])
            listWords.append(Word(text, i, dependency))
    for word in listWords:
        listWords[word.parent].children.append(word.position)
    return listWords
    

def getRootIndex(listWords):
    """Find the root's index
    
    Args:
        a list of words (list of Word objects)
    Returns:
        the position of the root in the sentence (int)
    
    """
    
    for word in listWords :
        if word.position in word.children :
            return word.position


def getParentsCount(listWords, wordIndex):
    """Find the number of parent a word have
    
    Args:
        the list of words (list of Word objects)
        the position of the word (int)
    Returns:
        the number of parents (int)
     
    """

    count = 0
    word = listWords[wordIndex]
    while (word.position != word.parent):
        count += 1        
        word = listWords[word.parent]
    return count


def setupRoot(board, x, y, listWords):
    """Draw the root and add it to the listWordOnBoard
    
    Args:
        the board which will be use to draw on (board, from graphics)
        x : the x offset of the anchor for the root (int)
        y : the y offset of the anchor for the root (int)
        listWords : the list of Words to be printed (list of Word objects)
    Returns: 
        the list of the words on the board (list of Word objects)
         
    """   
    
    listWordOnBoard = []
    root = listWords[getRootIndex(listWords)]
    rootDrawing = Text(Point(x,y),root.lemme)
    rootDrawing.draw(board)
    board.getMouse()  #can get annotated, it just to make a pause
    listWordOnBoard.append(root)
    return listWordOnBoard
            

def setupRestOfWords(board, rootX, rootY, listWordOnBoard, listWords):
    """While every word in not in place on the board, continue to place them
    
    Args:
        board : the board which will be use to draw on (board, from graphics)
        rootX : the x offset of the anchor for the root (int)
        rootY : the y offset of the anchor for the root (int)
        listWordOnBoard : the list of the words on the board (list of Word objects)
        listWords : the list of Words to be printed (list of Word objects)
    Returns: 
        none
        
    """

    wordOnBoardCheckedCount = 0        
    while len(listWordOnBoard)<len(listWords):
        word = listWordOnBoard[wordOnBoardCheckedCount]
        for childIndex in word.children:
            #since the root refer to itself as his own child
            #check to not make it duplicate to infinite
            if childIndex != word.parent:
                childWord = listWords[childIndex]
                anchorX = rootX + nodeWidth*childIndex
                anchorY = rootY + nodeHeight*getParentsCount(listWords, childIndex)
                anchor =  Point(anchorX, anchorY)
                Text(anchor, childWord.lemme).draw(board) #print the word on the board
                listWordOnBoard.append(childWord) #add the word to the listWordOnBoard
                board.getMouse()  #can get annotated, it just to make a pause    
        wordOnBoardCheckedCount += 1
    board.getMouse()  # pause, wait for a click on the window


def drawTree(pathFile):
    """Draw the tree of the annotatedFile provided
    
    Args:
        the path of the annotated data file (string)
    Returns:
        a board with the words printed on it (board, from graphics)
        
    """
    
    listWords = createListWords(pathFile)
    #definition of the Board to print the tree
    boardLength = width
    boardHeight = height
    board = GraphWin("Billy's Tree Board", boardLength, boardHeight)
    #def of my anchor for the first point
    offset = (getRootIndex(listWords)/len(listWords))
    rootPositionX = offset * boardLength + 100
    rootPositionY = offset * boardHeight + 100
    #place the words on the board
    listWordOnBoard = setupRoot(board, rootPositionX, rootPositionY, listWords)
    setupRestOfWords(board, rootPositionX, rootPositionY, listWordOnBoard, listWords)
    #pause, wait for a click on the window, then close properly
    board.getMouse() 
    board.close()
   
 
#test  
#drawTree('annotatedText.json')