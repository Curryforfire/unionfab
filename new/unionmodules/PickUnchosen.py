# -*- coding: utf-8 -*-
"""
Created on Thu May 14 10:51:41 2020

@author: curry
"""
import csv
import SelectModel as sm 
import PackingAlgm as pa
import pandas as pd



def Pickparts(Parts_URL):
    total_unselected = pa.collect_unchosen + pa.Unpacking
    files=open(Parts_URL,'rt')
    Reader=csv.reader(files)
    with open('Parts_un.csv', 'w', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(["index", "sigma", "height", "duetime", "width", "length", "area"])
        for row in Reader:
            if row[0] in total_unselected:
                writer.writerow([row[0],row[1], row[2],
                        row[3], row[4], row[5],row[6]]) 

 


    



