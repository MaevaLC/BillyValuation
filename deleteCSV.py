# -*- coding: utf-8 -*-
"""
Created on Fri Jun  9 16:27:20 2017

@author: m.leclech
"""

#import csv
#from src.AnnotateText import annotateText
#with open("phrasesV3.csv", "r") as f:
#    reader = csv.reader(f)
#
#    for row in reader:
#        print(row[0])
#        annotateText("ideavaluation.estia.fr", 2, row[0])


# creation of deletion table for the annotated text
import csv
csvf = open("deletionV3.csv", "w")
for i in range(721):
    output = [0.0]*30
    out = csv.writer(csvf, delimiter=',', lineterminator = '\n')
    out.writerow(output)
csvf.close()






