# -*- coding: utf-8 -*-
"""
Created on Thu May 21 14:32:42 2020

@author: curry
"""
import csv

def getmach(Result_URL):
    files=open(Result_URL,'rt')
    Reader=csv.reader(files)
    machset = []
    with open('Parts_un.csv', 'w', newline='') as file:
        head = next(Reader)
        for row in Reader:
            if row[0] not in machset:
                machset.append(row[0])
        print('the used machs are',machset)
        print('the num of used machs are',len(machset))
    return machset