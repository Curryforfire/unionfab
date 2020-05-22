# -*- coding: utf-8 -*-
"""
Spyder Editor

This is a temporary script file.
"""

#配置环境变量
import sys
sys.path.append(r"C:\Users\curry\Desktop\new\unionmodules")

#导入模块  
from SelectModel import *
import PackingAlgm as pa
import SelectModel as sm 
from combinecsv import *
from getmach import *

#零件数据csv文件
Parts_URL = r'C:\Users\curry\Desktop\new\testdata.csv'

#机器数据csv文件
Machs_URL = r'C:\Users\curry\Desktop\new\machdata.csv'


#期数 
I = 4

#初始机器数检索范围
MACH_lower = 3
MACH_upper = 3

#分配版面阈值
Threshold = 0.9

#选择最终排版的最大期数 
display_I = 2



#运算精度默认为0.1
#计算分配及摆放方案 
startfuncion(I,display_I,MACH_lower,MACH_upper,Machs_URL,Parts_URL,Threshold,Opt_Gap=0.1) 
#
#
#
#
#Parts_new = r'C:\Users\curry\Desktop\new\testdata1.csv'
#Parts_un = r'C:\Users\curry\Desktop\new\Parts_un.csv'  
#    
#combine(Parts_new,Parts_un)



#Result_URL = r'C:\Users\curry\Desktop\new\testing_result.csv'
#
#getmach(Result_URL)





 







