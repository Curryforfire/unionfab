import random
import numpy as np
import csv  
import datetime
import time

"""随机生成零件端数据写入csv文件
"""
  
#零件总数 
J = 60
#可以对超期风险进行等级排序，增加重要产品的超期罚项值  
#    sigma = np.round(np.random.uniform(1, 3, size = J), 2)
sigma = np.ones(J)
#每个零件打印耗时服从1h~7h的均匀分布 
h = np.round(np.random.uniform(1, 7, size = J), 2)

#当前计算机时间
start_time=datetime.datetime.now() + datetime.timedelta(hours=+50) 
#100h内要交货的时间
end_time=datetime.datetime.now() + datetime.timedelta(hours=+150) # 当前时间加上120小时

a1=tuple(start_time.timetuple()[0:9])    #设置开始日期时间元组
a2=tuple(end_time.timetuple()[0:9])   #设置结束日期时间元组 
 
start=time.mktime(a1)    #生成开始时间戳
end=time.mktime(a2)      #生成结束时间戳

tt=[]
for i in range(J):
    t=random.randint(start,end)    #在开始和结束时间戳中随机取出一个
    date_touple=time.localtime(t)          #将时间戳生成时间元组
    date=time.strftime("%Y/%m/%d %H:%M:%S",date_touple) 
    tt.append(date)


#每个零件零件长宽均为5cm~25cm的随机数  
a = np.round(np.random.uniform(3, 30, size = J), 2)
b = np.round(np.random.uniform(3, 30, size = J), 2)
s = np.round(a * b, 2)

with open('testdata.csv', 'w', newline='') as file:
    writer = csv.writer(file)
    writer.writerow(["index", "sigma", "height", "duetime", "width", "length", "area"])
    for i in range(J):
        writer.writerow([i+1, sigma[i], h[i], tt[i], a[i], b[i], s[i]]) 
        
        
"""随机生成机器端数据写入csv文件
"""

#机器总数
K = 50
Bin_Width = 60
Bin_Length = 60 

with open('machdata.csv', 'w', newline='') as file:
    writer = csv.writer(file)
    writer.writerow(["index", "Bin_Width", "Bin_Length"])
    for i in range(K):
        writer.writerow([str(i+1).zfill(3), Bin_Width, Bin_Length])
    
    
    
    
    
    
    