# -*- encoding: utf-8 -*-
'''
@Description    :
@Date           :2024/03/01 15:18:50
@Author         :WangYR
@version        :1.2
'''
import numpy as np
import cvxpy as cp
import csv
import matplotlib.pyplot as plt
import multiprocessing as mp
from functools import partial
from tqdm import tqdm
import random
from scipy.interpolate import make_interp_spline

      
def variance(data):
    # 计算均值。
    mean = np.mean(data)
    # 计算每个元素与均值的差的平方。
    squared_differences = np.square(data - mean)
    # 计算方差。
    variance = np.mean(squared_differences)
    return variance
  
def incentive_allocation_iterative(num,beta,x):
    """
    激励分配迭代算法
    参数：
      x: 可行解集
      Thres: 最大允许差异
      round: 最大迭代次数
    返回：
      更新后的解集 x
    """
    round=0
    DIF=0
    Thres=0.03
    Z=1000
    T=20
    # beta = np.ones(self.num)
    alpha = np.ones(num)
    j = [1]*num
    # 迭代循环

    while DIF > Thres or round < 100:
      # 对于集合 I 中的每个 i
      for i in range(num):
        # 计算 ji
        j[i] = sum(x[:i]) + sum(x[i+1:])
        # print(j[i],x)
        # k=input("check")
        # 求解 (9) 以获得 ai

        # print(j)
        alpha[i] = np.sqrt(beta/j[i])*Z/T

        # 计算 xi
        # x[i] = np.sqrt(alpha[i] * j[i] / beta[i] ) - j[i]
        x[i] = np.sqrt(alpha[i] * j[i] / beta ) - j[i]
        if(x[i]<=0):
           x[i] = 0
      # 计算 DIF
      DIF = variance(alpha)
      round += 1
    #   if round%20==1 or round == 100:
    #     print("This is round:", round,", with a DIF of",DIF)
    #     print("alpha:", np.mean(alpha))
    #     print("sum_x:", sum(x),'\n',"min_x and max_x:",min(x),max(x),'\n')
    return x,np.mean(alpha)

def main():
  #I
    num=20
    l=[0.5,2,4,6,8,10]
    # l=[10]
    x=np.random.rand(num)
    # for i in range(num):
    #    x.append(random.uniform(1,10))
    print(x)
    a_res=[]
    xm_res=[]
    x_res=[]

    for beta in l:
        x1,alpha=incentive_allocation_iterative(num,beta,x)
        a_res.append(alpha)
        xm_res.append(np.mean(x1))

        sorted_x=np.sort(x1)
        y = np.arange(1, len(sorted_x)+1) / len(sorted_x)
        
        # xs=np.linspace(sorted_x.min(),sorted_x.max(),800)
        # ys=make_interp_spline(sorted_x,y)(xs)
        # plt.step(xs,ys)
        plt.step(sorted_x,y)

    plt.ylabel("CDF")
    plt.xlabel("x")
    plt.legend(l, loc='lower right')
    plt.show()

    # fig,al=plt.subplots()
    # al.plot(l,a_res,'or-')
    # al.set_xlabel('beta')
    # al.set_ylabel('alpha')

    # xl=al.twinx()
    # xl.plot(l,xm_res,'Db--')
    # xl.set_ylabel('average x')

    # plt.show()

if __name__ == "__main__":
  main()
