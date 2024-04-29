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

class A1:
  '''
  mostly solve incentive_allocation_iterative()
  '''
  def __init__(self,num,k,beta):
    # 初始化
    self.num = num
    '''矿工数量'''
    self.Thres = 0.03 
    '''方差标准'''
    self.DIF = 0 
    '''具体方差'''
    self.k = k
    self.beta = beta

    # for i in range(num):
    #   beta[i]=np.random.rand()*5
    # 常数定义
    self.r=20
    '''PoS块数和PoW块数的预期比例'''
    self.L=1000000
    '''h[i]最可能的数字\n\nh[i]: A hit of node i,hi属于u(0,M)'''
    self.N=100
    '''网络中PoS矿工的数量'''
    self.B=100
    '''期望时间修正,调整两个PoS块之间的时间的值'''

    # self.k=2
    # """PoW过程的比例修正\n\nT=k*alpha"""
    # self.beta = 2

    self.U=60
    '''所有PoS矿工的token平均'''
    self.Z=10
    '''PoW过程的难度系数'''

  def incentive_allocation_iterative(self,x):
    """
    激励分配迭代算法
    参数：
      x: 可行解集
      Thres: 最大允许差异
      round: 最大迭代次数
    返回：
      更新后的解集 x
    """
    # beta = np.ones(self.num)
    alpha = np.ones(self.num)
    j = np.zeros(self.num)
    # 迭代循环
    round=0
    while self.DIF > self.Thres or round < 100:
      # 对于集合 I 中的每个 i
      for i in range(self.num):
        # 计算 ji
        j[i] = sum(x[:i]) + sum(x[i+1:])
        
        # 求解 (9) 以获得 ai
        # alpha[i] = some_steps_through_cvxpy(r,L,N,B,j[i],beta[i],k)
        a=cp.Variable()
        constraints = [a >= 0,
                      20 <= a * self.k,
                      # cp.sqrt((a**3) * j[i] / beta[i]) >= self.Z / self.k]
                      cp.sqrt((a**3) * j[i] / self.beta) >= self.Z / self.k]

        acc_a = sum(alpha[:i]) + a + sum(alpha[i+1:])
        obj = cp.Minimize(acc_a)
        prob = cp.Problem(obj,constraints)
        prob.solve(qcp=True,solver=cp.ECOS)
        alpha[i]=a.value
        # print("status:", prob.status)

        # 计算 xi
        # x[i] = np.sqrt(alpha[i] * j[i] / beta[i] ) - j[i]
        x[i] = np.sqrt(alpha[i] * j[i] / self.beta ) - j[i]
      # 计算 DIF
      self.DIF = self.variance(alpha)
      round += 1
      if round%10==0:
        print("This is round:", round,", with a DIF of",self.DIF)
        print("alpha(5):", alpha[:5])
        print("miner(5):", x[:5])
    return x,alpha[0]
      
  def variance(self,data):
    # 计算均值。
    mean = np.mean(data)
    # 计算每个元素与均值的差的平方。
    squared_differences = np.square(data - mean)
    # 计算方差。
    variance = np.mean(squared_differences)
    return variance

def th(b,k,num,x):
  algo=A1(num,k,b)
  x1,alpha=algo.incentive_allocation_iterative(x)
  return [k,b,x1,alpha]

def main():
  #I
  num=20
  l=[2,4,6,8,10]
  k_l=[2]
  x=np.random.rand(num)
  print(x)

  path="./test code/algo1_output.csv"
  with open(path,"w",newline='') as csvfile:
    writer = csv.writer(csvfile)
    writer.writerow(['k','beta',"x_sum","alpha"])
    for k in tqdm(k_l):
      res=[]
      for beta in l:
        print("k=",k,"beta=",beta)
        algo=A1(num,k,beta)
        # x=[0.1,0.2,0.3,0.4,0.5]
        x1,alpha=algo.incentive_allocation_iterative(x)
        print("x_sum:",sum(x1),'\nalpha:',alpha)
        writer.writerow([k,beta,sum(x1),alpha])
        res.append(alpha)
      plt.plot(l,res,'o-',label=k)
    plt.grid(zorder=0, linewidth="0.5",linestyle=":")
    plt.legend()
    plt.xlabel('beta')
    plt.ylabel('alpha')
    plt.show()

def mtcompu():
  k_l=[2,4,6,8,10]
  b_l=[2,4,6,8,10]
  num=20
  x=np.random.rand(num)
  print(x)
  res=[]
  for i in tqdm(k_l):
    p=mp.Pool(processes=8)
    func = partial(th,k=i,num=num,x=x)
    res.append(p.map(func,b_l))
  print(res)

  for list_k in res:
    alpha=[]
    for l in list_k:
      alpha.append(l[3])
    plt.plot([2,4,6,8,10],alpha,'o-',label=list_k[0][0])
  plt.grid(zorder=0, linewidth="0.5",linestyle=":")
  plt.legend()
  plt.xlabel('beta')
  plt.ylabel('alpha')
  plt.show()

if __name__ == "__main__":
  main()
  # mtcompu()

'''
i involved in I   矿工ID 与 矿工集
x[i]              矿工i投入的算力
s[i]              矿工i的总算力
j[i]              链上除i的总算力
alpha             激励的硬币数
beta[i]           采矿以外的目的可以获得的单位收入
k=T/alpha         PoW过程的比例修正
Z                 PoW过程的难度系数
T                 两PoW块之间的预期时间(PoW块预期生成周期)
r                 PoS块数和PoW块数的预期比例
L                 h_i最大的可能数字
h[i]              A hit of node i, hi属于u(0,M)
N                 网络中PoS矿工的数量
B                 期望时间修正,调整两个PoS块之间的时间的值
U                 所有PoS矿工的token平均
c                 特定一轮中矿工成本
''''''
1:  M_i(alpha,x_i)=alpha*P(x_i)+beta_i*(s_i-x_i)-c
2:  max M_i(alpha,x_i)
3:  0<=x_i<=s_i
4:  min alpha
5:  sum(x_i)>=Z/T
6:  T>=r*(L/((N+1)*B*U))
7:  x_i*=sqrt(alpha*j_i/beta_i)-j_i
8:  sqrt((alpha**3) * j[i] / beta[i])>=Z/k
P(x_i)=x_i/(x_i+j_i)
''''''
max M_i(alpha,x_i)  [0<=x_i<=s_i]
min alpha           [sum(x_i)>=Z/T
                    T>=r*(L/((N+1)*B*U))]
9:  min U(alpha_i)=acc(alpha_i)
                    [T>=r*(L/((N+1)*B*U))
                    sqrt((alpha**3) * j[i] / beta[i])>=Z/k]
'''