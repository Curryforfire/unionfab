# -*- coding: utf-8 -*-
"""
Created on Fri May 15 23:14:57 2020

@author: curry
"""
import csv
import time 
import datetime 

#零件端数据导入
def importdata(url):
    """将地址为url的零件csv数据文件导入到模型中，
       建立以零件编号为key的字典
    """  
    d_parts = {}
    N_key = []
    files=open(url,'rt')
    Reader=csv.DictReader(files)
    for row in Reader:
        timeArray = time.strptime(row['duetime'], "%Y/%m/%d %H:%M:%S")
        timestamp = time.mktime(timeArray)
        now_time = datetime.datetime.now()
        mkt_now = time.mktime(now_time.timetuple())
        delt_time = (timestamp-mkt_now)/3600
        data1 = [row['sigma'], row['height'], delt_time, 
                 float(row['width']), float(row['length']), row['area']]
        N_key.append(row['index'])
        d_parts[row['index']] = data1       
    return d_parts,N_key



