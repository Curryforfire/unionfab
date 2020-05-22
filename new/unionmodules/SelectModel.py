# -*- coding: utf-8 -*-

import random
import numpy as np
from gurobipy import *
import math
import csv
import PackingAlgm
import im_partdata
import im_machdata
import OutputResult as outr
import PickUnchosen as pu




#主函数              
def startfuncion(I,display_I,MACH_lower,MACH_upper,Machs_URL,Parts_URL,threshold,Opt_Gap): 
    
    dict_parts,N_key = im_partdata.importdata(Parts_URL)
    dict_machs,Mach_key = im_machdata.importmach(Machs_URL)
    if MACH_lower > len(Mach_key):
        MACH_lower = 1
    if MACH_upper > len(Mach_key):
        MACH_upper = len(Mach_key)
    obj_Y = 0
    K = random.choice(range(MACH_lower,MACH_upper+1))      
    select_numk(I,N_key,K,MACH_lower,MACH_upper,obj_Y,dict_parts,dict_machs,Mach_key,threshold,display_I,Opt_Gap)
    outr.output(threshold)
    pu.Pickparts(Parts_URL)
        
#二分法确定合适机器数 
def select_numk(I,N_key,K,MACH_lower,MACH_upper,obj_Y,dict_parts,dict_machs,Mach_key,threshold,display_I,Opt_Gap): 
    """给定机器数可行范围，二分法缩减机器数，直到upper-lower<=1为止，
    令机器数为上界upper,缩减同时对期数作相应调整
    """
    K = math.ceil((MACH_lower+MACH_upper)/2) 
    I = math.ceil(2*MACH_upper*I/(MACH_upper+MACH_lower))  
    obj_Y = SelectedOrder(I,N_key,K,MACH_lower,MACH_upper,obj_Y,dict_parts,dict_machs,Mach_key,threshold,display_I,Opt_Gap)
    if obj_Y == None:
        return None
    else:
        if obj_Y <= 0:  
            MACH_upper = K
            return select_numk(I,N_key,K,MACH_lower,MACH_upper,obj_Y,dict_parts,dict_machs,Mach_key,threshold,display_I,Opt_Gap)
        else:
            MACH_lower = K
            return select_numk(I,N_key,K,MACH_lower,MACH_upper,obj_Y,dict_parts,dict_machs,Mach_key,threshold,display_I,Opt_Gap)


#最优化分配模型       
def SelectedOrder(I,N_key,K,MACH_lower,MACH_upper,obj_Y,dict_parts,dict_machs,Mach_key,threshold,display_I,Opt_Gap):
    
    m = Model('UnionFab_Model')    
    #变量 
    h_bar = m.addVars(I, K, lb = 0, vtype = GRB.CONTINUOUS, name = "h_bar")
    Y_a = m.addVars(I, N_key, K, lb = 0, vtype = GRB.CONTINUOUS, name = "Y_a")
    Y_b = m.addVars(I, N_key, K, lb = 0, vtype = GRB.CONTINUOUS, name = "Y_b")
    Y_bar = m.addVars(I, N_key, K, lb = 0, vtype = GRB.CONTINUOUS, name = "Y_bar")
    x = m.addVars(I, N_key, K, vtype = GRB.BINARY, name = "x")
    delta = m.addVars(I, K, vtype = GRB.BINARY, name = "delta")
    
    #目标   
    obj = quicksum((quicksum(dict_parts[j][0] * Y_bar[i, j, k] for j in N_key)\
                    + (delta[i, k] * i)) for i in range (I) for k in range(K))
    m.setObjective(obj, GRB.MINIMIZE)
    
    #约束
    m.addConstrs(h_bar[i, k] >= dict_parts[j][1] * x[i, j, k]\
                 for i in range (I) for j in N_key for k in range(K))
    m.addConstrs((((i + 1) * 0.25 + quicksum(h_bar[t, k] for t in range (i + 1))) * x[i, j, k]) == Y_a[i, j, k]\
                 for i in range (I) for j in N_key for k in range(K))
    m.addConstrs(dict_parts[j][2] * x[i, j, k] >= Y_b[i, j, k]\
                 for i in range (I) for j in N_key for k in range(K))   
    m.addConstrs(Y_bar[i, j, k] >= Y_a[i, j, k] - Y_b[i, j, k]\
                 for i in range (I) for j in N_key for k in range(K)) 
    m_key = Mach_key[:K]
    m.addConstrs(quicksum(dict_parts[j][5] * x[i, j, k] for j in N_key) <= threshold*dict_machs[m_key[k]][0]*dict_machs[m_key[k]][1] \
                 for i in range(I) for k in range(K))
    m.addConstrs(quicksum(x[i, j, k] for i in range (I) for k in range(K)) == 1 for j in N_key)  
    m.addConstrs(quicksum(x[i, j, k] for j in N_key) <= 10000000000000 * delta[i, k]\
                 for i in range (I) for k in range(K))
#    m.addConstrs(x[i,j,k] >= delta[i,k] for i in range (I) for j in N_key for k in range (K))
    #求解
#    m.Params.timeLimit = 15.0
    
    m.Params.MIPGap = Opt_Gap
    m.optimize()
    m.printAttr("x")   
    
    if MACH_upper - MACH_lower <= 1: 
        print("optimal machine number : ",K)
        Mach_key = Mach_key[:K]
        return PackingAlgm.bridge_packing(x,I,N_key,dict_parts,dict_machs,Mach_key,display_I)   
    else:
        for i in range(I):                          
            for j in N_key:
                for k in range(K):
                    obj_Y +=  Y_bar[i, j, k].x   #对Y_bar求和，大于0则说明有零件超期   
        return obj_Y 










