# -*- encoding: utf-8 -*-
'''
@Description    :经济声誉混合激励模拟
@Date           :2024/05/29 13:39:03
@Author         :WangYR
@version        :1.0
'''

import matplotlib.pyplot as plt
import random
# import sys_node as node
from sys_node import *
import sys_func as f

def main():
    blockchain=[]
    num_pack=100
    alpha=1
    gamma=2
    # 生成节点
    users, clouds, miners = f.generate_nodes(20, 1, 10, gamma)

    mw=[]
    pw=[]
    rep=[]
    x=[]
    tau=0.01
    transaction_pool=[]
    fee=[0.0004,0.0006,0.0008,0.001,0.0012]

    for i in range(num_pack):
        # 生成交易
        transaction_pool = f.generate_transactions(users,500,transaction_pool,fee)
        # 打包和挖矿
        blockchain.append(f.pack_and_mine(clouds, miners, transaction_pool, alpha, tau))
        for cloud in clouds:
            mw.append(cloud.main_wallet)
            pw.append(cloud.pledge_wallet)
            rep.append(cloud.reputation)
        x.append(i+1)

    # 打印节点信息
    # for user in users:
    #     print(user)
    # for cloud in clouds:
    #     print(cloud)
    # for miner in miners:
    #     print(miner)
    # print(len(blockchain),len(transaction_pool))
    
    
    # 作图
    # 比例
    mwd=[mw[0]]
    pwd=[pw[0]]
    for i in range(1,num_pack):
        mwd.append(mw[i]-mw[i-1])
        pwd.append(pw[i]-pw[i-1])
    print(mwd,pwd)
    plt.bar(x,mwd,width=-1,label='main wallet',edgecolor='grey',zorder=5,align='edge')
    plt.bar(x,pwd,width=-1,bottom=mwd,label='pledge wallet',edgecolor='grey',zorder=5,align='edge')
    plt.tick_params(axis='x',length=0)
    plt.grid(axis='y',alpha=0.5,ls='--')
    # plt.ylim(0,1600)
    # plt.xlim(0,50)
    plt.legend(loc='upper left')
    # plt.tight_layout()
    # plt.savefig('bar1.png', dpi=600)
    plt.show()

    # 折线
    fig,ax1=plt.subplots()

    ax1.plot(x,rep,'c',label="reputation")
    plt.ylim(50,105)

    ax2=ax1.twinx()
    ax2.plot(x,pw,label='pledge wallet')
    ax2.plot(x,mw,label='main wallet')
    fig.legend(loc='upper left')
    plt.show()
    
    return clouds[0].main_wallet,clouds[0].pledge_wallet,clouds[0].reputation

for i in range(1):
    mw,pw,rep=main()
    print(mw,pw,mw/pw,rep)



def main1():
    # 模拟交易池
    transaction_pool = []

    # 创建节点
    cloud_node = CloudNode()
    miner_node = MinerNode(100, 500, 0.1)
    sender = UserNode()
    recipient = UserNode()

    # 发起交易
    sender.send_transaction(recipient, 100, 10)
    transaction_pool.append(Transaction(100, 2000, 10))

    # 云节点打包
    cloud_node.pack(transaction_pool, miner_node)

    # 打印节点信息
    print(cloud_node)
    print(miner_node)
    print(sender)
    print(recipient)