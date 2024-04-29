import numpy as np

def x_init(distr:int,num:int):
    '''controls the distribution of the x.
    distr can be 1-4:
    ### 1:Uniform distributions
    Set the capabilities of computational power at 10 units of each device.\n
    所有矿工都是10个单位算力
    ### 2:Normal distribution
    We set the average at 10 units and sigma = 1.\n
    正态分布，均值10
    ### 3:Zipf distribution
    alpha=2,均值在10左右
    ### 4:Cluster distribution
    集群分布，x将随机被赋值为[4,8,12,16]
    '''
    if distr==1:
        t=[10.0]*num
        x=np.array(t)
    elif distr==2:
        x=np.random.normal(10,1,num)
    elif distr==3:
        x=np.random.zipf(2,num)
    elif distr==4:
        t=np.random.randint(1,5,num)
        t2=[]
        for i in t:
            t2.append(float(i*4))
        x=np.array(t2)
    else:
        x='distr error'
    return x

# print(x_init(0,10))