# -*- coding: utf-8 -*-
"""
Created on Mon May 22 16:43:57 2017

@author: m.leclech
"""


import json

from graphics import Point, Text, GraphWin


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
    

def findRootIndex(listWords):
    """Find the root's index
    
    Args:
        a list of words (list of Word objects)
    Returns:
        the position of the root in the sentence (int)
    
    """
    
    for word in listWords :
        if word.position in word.children :
            return word.position


def countOfParents(count, listWords, wordIndex):
    """Find the number of parent a word have
    
    Args:
        the list of words (list of Word objects)
        the position of the word (int)
    Returns:
        the numer of parents (int)
     
    """
    
    word = listWords[wordIndex]
    while (word.position != word.parent):
        count += 1        
        word = listWords[word.parent]
    return count


def setupRoot(board, length, height, listWords):
    """Draw the root and add it to the listWordOnBoard
    
    Args:
        the board which will be use to draw on (board, from graphics)
        length : the length parameter of the anchor for the root (int)
        heigth : the height parameter of the anchor for the root (int)
        listWords : the list of Words to be printed (list of Word objects)
    Returns: 
        the list of the words on the board (list of Word objects)
         
    """   
    
    listWordOnBoard = []
    root = listWords[findRootIndex(listWords)]
    rootDrawing = Text(Point(length,height),root.lemme)
    rootDrawing.draw(board)
    board.getMouse()  #can get annotated, it just to make a pause
    listWordOnBoard.append(root)
    return listWordOnBoard
            

def setupRestOfWords(board, length, height, listWordOnBoard, listWords):
    """While every word in not in place on the board, continue to place them
    
    Args:
        the board which will be use to draw on (board, from graphics)
        length : the length parameter of the anchor for the root (int)
        heigth : the height parameter of the anchor for the root (int)
        listWordOnBoard : the list of the words on the board (list of Word objects)
        listWords : the list of Words to be printed (list of Word objects)
    Returns: 
        none
        
    """

    wordOnBoardCheckedCount = 1        
    while len(listWordOnBoard)<len(listWords):
        word = listWordOnBoard[wordOnBoardCheckedCount-1]
        for childIndex in word.children:
            #since the root refer to itself as his own child
            #check to not make it duplicate to infinite
            if childIndex != word.parent:
                childWord = listWords[childIndex]
                lengthAnchor = length + 75*childIndex
                count = 0  
                heightAnchor = height + countOfParents(count, listWords, childIndex)*50
                anchor =  Point(lengthAnchor, heightAnchor)
                Text(anchor, childWord.lemme).draw(board) #print the word on the board
                listWordOnBoard.append(childWord) #add the word to the listWordOnBoard
                board.getMouse()  #can get annotated, it just to make a pause    
            else :                              
                pass
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
    lengthBoard = 1500
    heightBoard = 700
    board = GraphWin("My Board", lengthBoard, heightBoard)
    #def of my anchor for the first point
    length = (findRootIndex(listWords)/len(listWords)) * lengthBoard + 100
    height = (findRootIndex(listWords)/len(listWords)) * heightBoard + 100
    #place the words on the board
    listWordOnBoard = setupRoot(board, length, height, listWords)
    setupRestOfWords(board, length, height, listWordOnBoard, listWords)
    #pause, wait for a click on the window, then close properly
    board.getMouse() 
    board.close()
   
 
#test  
#drawTree('annotatedText.json')