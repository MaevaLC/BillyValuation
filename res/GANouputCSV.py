# -*- coding: utf-8 -*-
"""
Created on Mon Jul  3 07:42:29 2017

@author: m.leclech
"""

import csv
csvf = open("GANoutputV3.csv", "w")
for i in range(721):
    output = [1,0,0.3]
    out = csv.writer(csvf, delimiter=',', lineterminator = '\n')
    out.writerow(output)
csvf.close()