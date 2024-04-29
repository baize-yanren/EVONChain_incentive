import numpy as np
import csv
import matplotlib.pyplot as plt
import multiprocessing as mp

import incentive_allocation as ia
from x_init import x_init

def main():
    #I
    num=20
    # l=[0.2,0.5,0.8,1.2,1.6,2,3,4,5,6,7,8,9,10]
    l=[2,4,6,8]
    x=x_init(2,num)

    print(x)
    if x is str:
      exit()
    a_res=[]
    xm_res=[]
    x_res=[]
    T=19

    for beta in l:
        x1,alpha=ia.incentive_allocation(num,beta,T,x,test_mode=True)
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
    plt.show()

    fig,al=plt.subplots()
    al.bar(l,a_res,color="peru")
    al.set_xlabel('beta')
    al.set_ylabel('alpha')

    xl=al.twinx()
    xl.plot(l,xm_res,'Db--')
    xl.set_ylabel('average x')

    plt.show()
    print('\n',xm_res,'\n',a_res)

if __name__ == "__main__":
    main()
