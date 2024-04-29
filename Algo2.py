# -*- encoding: utf-8 -*-
'''
@Description    :
@Date           :2024/03/25 15:21:10
@Author         :WangYR
@version        :1.0
'''
import numpy as np
from math import *
import csv
import matplotlib.pyplot as plt
import multiprocessing as mp
from functools import partial
from tqdm import tqdm

def incentive_allocation_heuristic_algorithm(Z,k,beta,N):
    x_sum = pow(pow(Z/(k*beta),2)*pow(N-1,3)/pow(N,6),1/4) 
    alpha = 2*sqrt(Z*beta*N/k)*pow(1/(N-1),1/4)
    return x_sum,alpha

def main():
    Z=10
    N=100
    # k=2
    # beta=2
    l=[2,4,6,8,10]

    # path="./test code/algo2_output.csv"
    path="./test code/test.csv"
    with open(path,"w",newline='') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(['k','beta',"x_sum","alpha"])
        for k in l:
            res=[]
            for beta in l:
                x_sum,alpha=incentive_allocation_heuristic_algorithm(Z,k,beta,N)
                # print("k=",k,"beta=",beta)
                # print(x_sum,alpha)
                writer.writerow([k,beta,x_sum,alpha])
                res.append(alpha)
            plt.plot(l,res,'o-',label=k)
        plt.grid(zorder=0, linewidth="0.5",linestyle=":")
        plt.legend()
        plt.xlabel('beta')
        plt.ylabel('alpha')
        plt.show()

def th(b,k):
    Z=10
    N=100
    x_sum,alpha=incentive_allocation_heuristic_algorithm(Z,k,b,N)
    return [k,b,x_sum,alpha]

if __name__ == '__main__':
    main()
    
    k_l=[2,4,6,8,10]
    b_l=[2,4,6,8,10]
    res=[]
    for i in tqdm(k_l):
        num_processes = mp.cpu_count()-2
        p=mp.Pool(processes=num_processes)
        func = partial(th,k=i)
        res.append(p.map(func,b_l))
    print(res)
