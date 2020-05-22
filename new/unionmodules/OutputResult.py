# -*- coding: utf-8 -*-
"""
Created on Thu May 14 09:52:07 2020

@author: curry
"""
import PackingAlgm as pa
import csv


def output(Threshold):
    with open('testing_result.csv', 'w', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(["MACH", "display_I", "Threshold", "index_chosen", "index_unchosen", "Ocupancy Rate", "item_bottleft", "coordinate_bottleft", "item_topright", "coordinate_topright"])
                   #         编号        阈值        分配零件编号     未pack零件编号     版面利用率            BF零件编号     BF零件坐标             TP零件编号         TP零件坐标                                                                       
        for i in range(len(pa.item_botleft)):
            pa.item_botleft[i] = [ elem for elem in pa.item_botleft[i] if elem != [] ]
            pa.item_toright[i].pop()
        
        coordinate_tpcopy = pa.coordinate_toright[:]
        for i in range(len(coordinate_tpcopy)):
            while(pa.coordinate_bottleft[i][-1]) == []:
                pa.coordinate_bottleft[i].pop()
            if pa.coordinate_toright[i] != []:    
                while((pa.coordinate_toright[i][-1]) == []) & (pa.coordinate_toright[i] != [[]]):
                    pa.coordinate_toright[i].pop() 

        for i in range(len(pa.Prod)):
            m = []                    
            for j in range(len(pa.Prod[i])):
                m.append(pa.Prod[i][j].get_index()) 
            if pa.unc[i] != []:  
                for un in pa.unc[i]:   
                    m.remove(un)           
            writer.writerow([pa.MACH[i], pa.I_m[i], Threshold, m, pa.unc[i], pa.S_ratio[i], pa.item_botleft[i], pa.coordinate_bottleft[i], pa.item_toright[i], pa.coordinate_toright[i]])
        
    









