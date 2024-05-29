# -*- encoding: utf-8 -*-
'''
@Description    :纳什均衡计算
@Date           :2024/05/29 13:45:12
@Author         :WangYR
@version        :1.0
'''
import numpy as np
import cvxpy as cp

def variance(data):
    # 计算均值。
    mean = np.mean(data)
    # 计算每个元素与均值的差的平方。
    squared_differences = np.square(data - mean)
    # 计算方差。
    variance = np.mean(squared_differences)
    return variance

def incentive_allocation(num,gamma,x,test_mode=False):
    """
    激励分配迭代算法
    外部参数：
        num: 参与矿工数量
        gamma: 矿工链外投入算力的预期单位收益
        x: 可行解集
    内部参数：
        Thres: 最大允许差异
        round: 最大迭代次数
        Dp: 主块难度系数
        T: 主块和副块的比例
    返回：
        更新后的解集 x,对应的p
    """
    round=0
    Thres=0.03
    DIF=0
    Dp=1000
    M=np.ones(num)
    q=0
    T=20
    while DIF>Thres or round<100:
        #对集合I中的每个i
        for i in range(num):
            q=np.sum(x[:i])+np.sum(x[i+1:])
            M[i]=np.sqrt(gamma/q)*Dp/T
            x[i]=np.sqrt(M[i]*q/gamma)-q
            if(x[i]<=0):
                x[i]=0
        DIF=variance(M)
        round+=1

        if test_mode==True:
            if round%20==0:
                print("This is round:", round,", with a DIF of",DIF)
                print("M:", np.mean(M))
                print("sum_x:", sum(x),'\n',x,'\n')
    return x,np.mean(M)