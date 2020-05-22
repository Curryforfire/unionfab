# -*- coding: utf-8 -*-
"""
Created on Wed May 20 20:48:08 2020

@author: curry
"""

import os
import glob
import pandas as pd
import csv
import numpy as np


"""merge文件夹内的所有csv文件
"""
#def combine():
#    cwd = os.getcwd()
#    
#    #Change “url” to your desired working directory.
#    os.chdir(cwd)
#    
#    extension = 'csv'
#    all_filenames = [i for i in glob.glob('*.{}'.format(extension))]
#    #combine all files in the list
#    combined_csv = pd.concat([pd.read_csv(f) for f in all_filenames ])
#    #export to csv
#    combined_csv.to_csv( "combined_csv.csv", index=False, encoding='utf-8-sig')



def combine(Parts_new,Parts_un): 
    outputfile= Parts_new 
    csv_1=pd.read_csv(Parts_new)
    csv_2=pd.read_csv(Parts_un)
    out_csv=pd.concat([csv_2,csv_1],axis=0)
    out_csv.to_csv(outputfile,index=False)

    





