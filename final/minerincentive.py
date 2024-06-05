# -*- encoding: utf-8 -*-
'''
@Description    :挖矿奖励模拟
@Date           :2024/05/29 13:43:58
@Author         :WangYR
@version        :1.0
'''
import numpy as np
import csv
import matplotlib.pyplot as plt
import multiprocessing as mp

import incentive_allocation as ia
from sys_node import *
import sys_func as f



def x_init(distr:int,num:int):
    '''controls the distribution of the x.
    distr can be 1-4:
    ### 1:Uniform distributions
    Set the capabilities of computational power at 10 units of each device.\n
    所有矿工都是1个单位算力
    ### 2:Normal distribution
    We set the average at 10 units and sigma = 1.\n
    正态分布，均值10
    ### 3:Cluster distribution
    集群分布，x将随机被赋值为[4,8,12,16]
    ### 3:zipf分布：其均值浮动过大，不做考虑
    '''
    if distr==1:
        t=[10.0]*num
        x=np.array(t)
    elif distr==2:
        x=np.random.normal(10,1,num)
    elif distr==3:
        t=np.random.randint(1,5,num)
        t2=[]
        for i in t:
            t2.append(float(i*4))
        x=np.array(t2)
    elif distr==4:
        x=np.random.zipf(2,num)
    else:
        x='distr error'
    return x

def main01():
    #I
    num=20
    # l=[0.2,0.5,0.8,1.2,1.6,2,3,4,5,6,7,8,9,10]
    l=[1,2,3,4,5,6,7,8]
    x=x_init(1,num)

    print(x)
    if x is str:
      exit()
    a_res=[]
    xm_res=[]
    x_res=[]

    for gamma in l:
        x1,alpha=ia.incentive_allocation(num,gamma,x,test_mode=True)
        a_res.append(alpha)
        xm_res.append(np.mean(x1))

        sorted_x=np.sort(x1)
        y = np.arange(1, len(sorted_x)+1) / len(sorted_x)
        plt.plot(sorted_x,y)

        # x=np.array(sorted_x)
        # y=np.array(y)
        # xs=np.linspace(x.min(),x.max(),300)
        # ys=make_interp_spline(x,y)(xs)
        # plt.plot(xs,ys)
        

    plt.ylabel("CDF")
    plt.xlabel("x")
    plt.legend(l, loc='lower right')
    plt.ylim(0,1)
    # plt.xlim(-1,1)
    plt.show()

    # fig,xl=plt.subplots()
    # xl.bar(l,xm_res,width=0.5)
    # xl.set_xlabel('gamma')
    # xl.set_ylabel('average x')
    # plt.ylim(0.2,0.8)
    # al=xl.twinx()
    # al.plot(l,a_res,color="peru",marker='.',markersize=15,markerfacecolor='w')
    # al.set_ylabel('M0')
    plt.bar(l,xm_res,width=0.5)
    plt.xlabel('gamma')
    plt.ylabel('average x')
    plt.ylim(0.2,0.8)
    plt.grid(axis='y',alpha=0.5,ls='--')
    plt.show()

    plt.plot(l,a_res,color="peru",marker='.',markersize=15,markerfacecolor='w')
    plt.xlabel('gamma')
    plt.ylabel('M0')
    plt.grid(axis='y',alpha=0.5,ls='--')
    plt.show()

    print('\n',xm_res,'\n',a_res)

def sim(gamma):
    blockchain=[]
    # 生成节点
    n_miner=2000
    users, clouds, miners = f.generate_nodes(5000, 100, n_miner, gamma)
    transaction_pool = []
    fee=[1,2,3,4,5,6,7,8,9,10]

    for i in range(5):
        # 生成交易
        transaction_pool = f.generate_transactions(users,100,transaction_pool,fee)

        # 选择打包交易
        block, transaction_pool=f.pack_and_mine(clouds, miners, transaction_pool, 1)
        blockchain.append(block)
        print(len(transaction_pool),block)

'''
    a_res=[]
    xm_res=[]
    x_res=[]


        x1,alpha=ia.incentive_allocation(n_miner,gamma,x,test_mode=True)
        a_res.append(alpha)
        xm_res.append(np.mean(x1))

        sorted_x=np.sort(x1)
        y = np.arange(1, len(sorted_x)+1) / len(sorted_x)'''

if __name__ == "__main__":
    main01()
    # l=[1,2,3,4,5,6,7,8]
    # for gamma in l:    
    #     sim(gamma)