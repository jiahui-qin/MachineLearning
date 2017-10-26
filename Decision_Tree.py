"""
决策树
应该用一系列if...else...结构来实现
"""
##首先需要计算熵
from collections import Counter
from math import log
class play(object):
    def __init__(self, outlook, temputure, hun, wind, play):
        self.outlook = outlook
        self.temputure = temputure
        self.hun = hun
        self.wind = wind
        self.play = play


def cal_entroy(cal_list):
    ##这里传入了一个list，下面的程序要传入一个list
    ent = 0
    leng=len(cal_list)
    cou_list = Counter(cal_list)
    for cal_ele in cou_list.keys():
        cal_prob = cou_list[cal_ele] / leng
        ent = ent - cal_prob * log(cal_prob, 2)
    return ent

def cal_gain(s_list, depend_var):
    ##传入两个自变量和应变量序列计算信息增益
    ##depend_var 因变量， s_list：当前要考虑的自变量
    p_ent = cal_entroy(depend_var)
    ord_list = []
    s_set = set(s_list)
    s_set=list(s_set)
    for i in range(len(s_set)):
        ord_list.append([])
    for i in range(len(s_list)):
        loc = s_set.index(s_list[i])
        ord_list[loc].append(i) ##打印出不同元素对应的位置
    
    sum_ent = 0
    for ords_list in ord_list:
        ords_ent = cal_entroy([depend_var[i] for i in ords_list])
        sum_ent = sum_ent + len(ords_list)/len(s_list)*ords_ent
    ent = p_ent - sum_ent
    return ent, ord_list, s_set

##print(cal_gain([1,1,2,3,3,3,2,1,1,3,1,2,2,3],[1,1,2,2,2,1,2,1,2,2,2,2,2,1]))
class decision_tree(object):
    ##决策树类
    
def cho_next(cur_property, ord_list, s_set, dec_matrix, depend_var):
    #为当前节点选择一个下一步信息增益最大的点
    loc = s_set.index(cur_property)
    cal_list = ord_list(loc)
    gain_l = []
    for y_var in dec_matrix:
        ##对每一个depend_var计算当前的增益
        gain_l.append(cal_gain([y_var[i] for i in cal_list], [depend_var[i] for i in cal_list]))
    return dec_matrix.index(max(gain_l))


##大致意思是这个没有错啦，以后慢慢来