# -*- encoding: utf-8 -*-
'''
@Description    :incentive_allocation
@Date           :2024/04/02
@Author         :WangYR
@version        :2.0
'''
import numpy as np
import cvxpy as cp
import matplotlib.pyplot as plt
import multiprocessing as mp

      
def variance(data):
    # 计算均值。
    mean = np.mean(data)
    # 计算每个元素与均值的差的平方。
    squared_differences = np.square(data - mean)
    # 计算方差。
    variance = np.mean(squared_differences)
    return variance

def a_solver(beta,k,j):
  # 参数
  Z=1000
  T=20
  # 计算区
  # 1
  # a = np.sqrt(beta/j)*Z/T

  # 2(有问题)
  # a=min(20/k,pow(pow(Z/k,2)*j/beta,1/3))

  # 3  
  al=cp.Variable()
  constraints = [al >= 20 / k
                ,cp.sqrt((al**3) * j / beta) >= Z / k]
                # ,al >= cp.power(cp.power(Z/k,2)*j/beta,1/3)]

  obj = cp.Minimize(al)
  prob = cp.Problem(obj,constraints)
  prob.solve(qcp=True,solver=cp.ECOS)
  a=al.value

  return a
  
def incentive_allocation(num,beta,k,x,test_mode=False):
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

    # beta = np.ones(self.num)
    alpha = np.ones(num)
    j = [1]*num
    # 迭代循环

    while DIF > Thres or round < 100:
      # 对于集合 I 中的每个 i
      for i in range(num):
        # 计算 ji
        j[i] = np.sum(x[:i]) + np.sum(x[i+1:])
        # print(j[i],x)
        # k=input("check")
        # 求解 (9) 以获得 ai
        alpha[i]=a_solver(beta,k,j[i])
        
        # a=cp.Variable()
        # constraints = [20 <= a * k,
        #               cp.sqrt((a**3) * j[i] / beta) >= Z / k]
        # acc_a = sum(alpha[:i]) + a + sum(alpha[i+1:])
        # obj = cp.Minimize(acc_a)
        # prob = cp.Problem(obj,constraints)
        # prob.solve(qcp=True,solver=cp.ECOS)
        # alpha[i]=a.value

        # 计算 xi
        # x[i] = np.sqrt(alpha[i] * j[i] / beta[i] ) - j[i]
        x[i] = np.sqrt(alpha[i] * j[i] / beta ) - j[i]
        if(x[i]<=0):
           x[i] = 0
      # 计算 DIF
      DIF = variance(alpha)
      round += 1

      # test code
      if test_mode == True:
        if round%20==1 or round == 100:
          print("This is round:", round,", with a DIF of",DIF)
          print("alpha:", np.mean(alpha))
          print("sum_x:", sum(x),'\n',x,'\n')

    return x,np.mean(alpha)

# test code
# num=20
# t=[10.0]*num
# x=np.array(t)
# beta=2
# k=2
# x1,alpha=incentive_allocation(num,beta,k,x,True)
# print(x1,alpha)