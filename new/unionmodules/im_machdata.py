# -*- coding: utf-8 -*-
"""
Created on Fri May 15 15:11:07 2020

@author: curry
"""
import csv 

#导入机器型号及参数
def importmach(url):
    """将地址为url的机器csv数据文件导入到模型中，
       建立以机器编号为key的字典
    """  
    d_machs = {}
    M_key = []
    files=open(url,'rt')
    Reader=csv.DictReader(files)
    for row in Reader: 
        data1 = [float(row['Bin_Width']), float(row['Bin_Length'])]
        M_key.append(row['index'])
        d_machs[row['index']] = data1       
    return d_machs,M_key








