# -*- encoding: utf-8 -*-
'''
@Description    :incentive_allocation
@Date           :2024/04/29
@Author         :WangYR
@version        :3.0
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

def a_solver(beta,j,T,Dp=1000):
    '''
    alpha迭代算法
    输入：
        beta:矿工链外投入算力的预期单位收益
        j:链上除x[i]外的总算力
        T:主块和副块的比例
        Dp:主块难度系数
    输出：
        更新后的a
    '''
    # 1:直接计算
    a = np.sqrt(beta/j)*Dp/T
    # 2:凸优化

    return a

def incentive_allocation(num,beta,T,x,test_mode=False):
    """
    激励分配迭代算法
    外部参数：
        num: 参与矿工数量
        beta: 矿工链外投入算力的预期单位收益
        T: 主块和副块的比例
        x: 可行解集
    内部参数：
        Thres: 最大允许差异
        round: 最大迭代次数
        Dp: 主块难度系数
    返回：
        更新后的解集 x,对应的alpha
    """
    round=0
    Thres=0.03
    DIF=0
    Dp=1000
    alpha=np.ones(num)
    j=1
    while DIF>Thres or round<100:
        #对集合I中的每个i
        for i in range(num):
            j=np.sum(x[:i])+np.sum(x[i+1:])
            alpha[i]=a_solver(beta,j,T,Dp)
            x[i]=np.sqrt(alpha[i]*j/beta)-j
            if(x[i]<=0):
                x[i]=0
        DIF=variance(alpha)
        round+=1

        if test_mode==True:
            if round%20==0:
                print("This is round:", round,", with a DIF of",DIF)
                print("alpha:", np.mean(alpha))
                print("sum_x:", sum(x),'\n',x,'\n')
    return x,np.mean(alpha)