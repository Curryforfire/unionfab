import csv
from PickUnchosen import *

#零件类
class Product(object):
    def __init__(self, j):
        self.index = j
    def get_index(self):
        return self.index  
    def get_width(self):
        return dict_parts[self.index][3]     
    def get_height(self):
        return dict_parts[self.index][4] 
    def __str__(self):
        return 'index:' + str(self.index) +' <' + str(self.get_width())\
            +',' + str(self.get_height())+ '>' 


Prod = [] 
MACH = []
I_m = []
Unpacking = []   #分配了但期数靠后所以暂不考虑装箱的   
def bridge_packing(x,I,N_key,dict_parts,dict_machs,Mach_key,display_I):  
    """将第一阶段模型分配结果传递到第二阶段装箱中
    """
    if display_I > I:
        display_I = I
    Prod_KI=[]    
    for k in range(len(Mach_key)):  
        Prod_KI.append([])              
        for i in range(display_I):
            Prod_KI[k].append([])
            for j in N_key:
                if x[i,j,k].x == 1:
                    Prod_KI[k][i].append(Product(j))
    
    for i in range(display_I,I):
        for k in range(len(Mach_key)):
            for j in N_key:
                if x[i,j,k].x == 1:
                    Unpacking.append(j)    
                    
    for k in range(len(Mach_key)):
        for i in range(display_I):
            if Prod_KI[k][i] != []:
#                MACH.append(k+1)
                I_m.append(i+1)
                Prod.append(Prod_KI[k][i])
#                a = str("{:.0f}_{:.0f}".format(k+1,i+1))   # a记录的是有排版的机器编号和对应期数 不便于后期处理，换种方式表达 
                print('\n machine',Mach_key[k],'at period {:.0f} :'.format(i+1))
                MACH.append(Mach_key[k])   
                Bin_Width = dict_machs[Mach_key[k]][0]
                Bin_Length = dict_machs[Mach_key[k]][1]
                S = Bin_Width * Bin_Length
                rec_packing(Prod_KI[k][i],Bin_Width,Bin_Length,dict_parts,S)                 
    return None


collect_unchosen=[]
coordinate_bottleft = [] 
coordinate_toright = []
item_botleft = []
item_toright = [] 
S_ratio = []
def rec_packing(Prod_KI, Bin_Width, Bin_Length,dict_parts,S):
    """装箱主函数，调用nextlayer和topright两个
    函数分别解决左下方开始和阶梯型右上角基于高度
    递减的装箱。width即水平延伸为宽度，height是
    二维平面的纵向延伸为高度。并通过分别累加s1，
    s2并对两阶段求和计算总的底面利用率。
    """ 
    cur_width=[]
    cur_width.append(0)                  
    cmax_height=[]
    cmax_height.append(0) 
    max_height = 0 
    item_existed,item_selected = [[]],[[]]  
    cur_layer=1
    width_topright,height_topright,item_topright,index_topright=[[]],[[]],[[]],[[]]
    rec_dict,rec_unchosen=[],[]
    t,i,layer_index,s1,s2=0,0,0,0,0
    coord_botleft,coord_toright = [],[]
    
    mydict = pick(Prod_KI,dict_parts,m=0,dictionary={}) 
    rec_dict = sorted(mydict.items(),key=lambda s: (s[1][1],s[1][0]), reverse=True)  
    """对零件集合组成的字典重新排序（height递减）
    但不改变对应key的值,排序后是list中套元组，元
    组中是key和对应的value
    """      
#两种装箱方式的函数                                         
    nextlayer(Bin_Width,Bin_Length,cmax_height,item_existed,rec_dict,cur_layer,cur_width,item_selected,max_height,coord_botleft,layer_index,i=0)    
    topright(index_topright,item_topright,t,height_topright,width_topright,rec_dict,item_selected,item_existed,cur_layer,cmax_height,coord_toright,layer_index,i=0,width=0,height=0)
#计算两种方式的零件装配左下角坐标   
    
    item_botleft.append(item_selected)
    item_toright.append(index_topright)

    
    coordinate_toright = coordinate_tp(index_topright,cmax_height,dict_parts,coord_toright,Bin_Width)
    coordinate_bottleft.append(coord_botleft)        

#计算两种方式和的总利用率     
    for i in range(len(item_existed)):
        for j in range(len(item_existed[i])):
            s1 += item_existed[i][j][0]*item_existed[i][j][1]
    for i in range(len(item_topright)):
        for j in range(len(item_topright[i])):
            s2 += item_topright[i][j][0]*item_topright[i][j][1]   
    S_ss = (s1+s2)/S
    S_ratio.append(S_ss)

#输出未被打印的零件集合  
    un_collect = unchosen(collect_unchosen,rec_unchosen,rec_dict)
    return un_collect

def coordinate_tp(index_topright,cmax_height,dict_parts,coord_toright,Bin_Width):
    """计算TP方式摆放的零件坐标
    """
    for layer in range(len(index_topright)-2):
            coord_toright.append([])
            cmax_height.append([])
            cmax_height[layer+1] += cmax_height[layer]  
    for layer in range(len(index_topright)-1):
        if index_topright[layer] != []:    
            cmax_height.append([])
            coord_toright.append([])
            a = Bin_Width
            for r in index_topright[layer]:
                a -= dict_parts[r][3]
                coord_toright[layer].append((a,cmax_height[layer]-dict_parts[r][4]))     
                
    coordinate_toright.append(coord_toright)    
    return coordinate_toright  

def pick(Prod_KI,dict_parts,m,dictionary={}):
    """对每一版零件单独定义字典，以本身编号作为key，
    （width和height）作为value
    """    
    for i in range(len(Prod_KI)): 
        m = Prod_KI[i].get_index()
        dictionary[m] = (dict_parts[m][3],dict_parts[m][4])
    return dictionary



unc = [] 
def unchosen(collect_unchosen,rec_unchosen,rec_dict):
    """每一版剩下（未被选择）的零件集合，在每一次计算完后
    代入下一阶段继续运算
    """   
    for i in range(len(rec_dict)):
        rec_unchosen.append(rec_dict[i][0]) 
    unc.append(rec_unchosen)
    if rec_unchosen != []:
        print("\nUnchosen items' index : ",rec_unchosen)   
    collect_unchosen += rec_unchosen
    return collect_unchosen  
    

#以下四个函数给出二维摆放方案  
def nextlayer(Bin_Width,Bin_Length,cmax_height,item_existed,rec_dict,cur_layer,cur_width,item_selected,max_height,coord_botleft,layer_index,i=0):       #cur_layer是最高层数 而layer_index是需要遍历的每一层    
    """从第一层开始，如果第i层横向有空间可装,
    则调用firsrfit进行装箱，否则判断i+1层
    """ 
    if rec_dict != []: 
        if max_height + rec_dict[-1][1][1] <= Bin_Length:   #这种情况满足的条件就是rec_dict非空
            for r in rec_dict[:]:              #[:]
                if max_height + r[1][1] <= Bin_Length:
                    firstfit(Bin_Width,item_existed,item_selected,cur_width,rec_dict,r,max_height,cmax_height,coord_botleft,layer_index=i)
            
            cmax_height.append(0)
            
            cmax_height[i]=item_existed[i][0][1]
            
            max_height += cmax_height[i]
            
            print("\n{:.0f} layer packed items :".format(i+1),item_selected[i])
            if r not in item_selected:  
                i += 1
                nextlayer(Bin_Width,Bin_Length,cmax_height,item_existed,rec_dict,cur_layer,cur_width,item_selected,max_height,coord_botleft,layer_index,i)  
        
def firstfit(Bin_Width,item_existed,item_selected,cur_width,rec_dict,r,max_height,cmax_height,coord_botleft,layer_index): 
    cur_width.append(0)
    if cur_width[layer_index] + r[1][0] <= Bin_Width:    
        
        coord_botleft.append([])
        coord_botleft[layer_index].append((cur_width[layer_index] ,max_height))
        cur_width[layer_index] += r[1][0]  
        item_selected.append([])                 #添加的是零件序号信息
        item_selected[layer_index].append(r[0])
        item_existed.append([])                  #添加的是零件长宽信息
        item_existed[layer_index].append(r[1])   
        rec_dict.remove(r)
        return rec_dict 
        
def topright(index_topright,item_topright,t,height_topright,width_topright,rec_dict,item_selected,item_existed,cur_layer,cmax_height,coord_toright,layer_index=0,i=0,width=0,height=0):
    """在第一阶段装箱结束后，会生成多层版面，每一层均为阶梯型，
    记录这些阶梯型的参数，供第二阶段倒阶梯型利用
    """
    while item_existed[i] != []:
        item_existed[i].reverse()
        for r in item_existed[i]:     
            width += r[0]
            width_topright[i].append(width)
            height_topright[i].append(r[1])
        width_topright[i].pop()
        height_topright[i].pop()
        width_topright.append([])   
        height_topright.append([])
        width = 0
        i += 1
    width_topright.pop()
    height_topright.pop()
    cmax_height.pop()
    toprightlayer(index_topright,item_topright,height_topright,width_topright,rec_dict,cur_layer,cmax_height,i,t,layer_index)
    return rec_dict
    
def toprightlayer(index_topright,item_topright,height_topright,width_topright,rec_dict,cur_layer,cmax_height,i,t,layer_index):  
    i=0
    if rec_dict != []:
        while layer_index < len(cmax_height):
            for i in range(len(width_topright[layer_index])):
                for r in rec_dict: 
                    if i + 1 <= len(width_topright[layer_index]): 
                        if t + r[1][0] <= width_topright[layer_index][i] and r[1][1] + height_topright[layer_index][i] <= cmax_height[layer_index]:                              
                            item_topright[layer_index].append(r[1])
                            index_topright[layer_index].append(r[0])
                            t += r[1][0]
                            rec_dict.remove(r)                           
            item_topright.append([])
            index_topright.append([])
            if index_topright[layer_index] != []:
                print("\n{:.0f} layer corner packed items :".format(layer_index+1),index_topright[layer_index])
            i=0
            t=0
            layer_index += 1

