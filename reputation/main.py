# -*- encoding: utf-8 -*-
'''
@Description    :reputation sim
@Date           :2024/04/29
@Author         :WangYR
@version        :1.0
'''
import numpy as np
import random
import block
import node

def sim_trade(limit):
    # 生成交易
    size_acc=0
    fee_acc=0
    tradelist=[]
    i=0
    while True:
        i+=1
        size=random.uniform(1000,20000)#1kb-20kb
        fee=random.uniform(0,10)
        if size_acc+size>=limit:
            break
        size_acc+=size
        fee_acc+=fee
        tradelist.append((size,fee))
    return tradelist,size_acc,fee_acc,i

def sim_illegal_trade(limit):
    # 生成可能的非法交易
    size_acc=0
    fee_acc=0
    tradelist=[]
    i=0
    while True:
        i+=1
        size=random.uniform(1000,20000)#1kb-20kb
        fee=random.uniform(0,10)
        size_acc+=size
        fee_acc+=fee
        tradelist.append((size,fee))
        if size_acc+size>limit:
            break
    return tradelist,size_acc,fee_acc,i
        
def main():
    # 暂以原始BTC为准，区块头80字节，区块最大1MB
    limit=1e6
    head=80
    num=10
    block_num=400
    nodelist = None
    total_fee=0
    total_wallet=0
    total_trade=0
    # create nodelist
    for i in range(num):
        nodelist = node.create_node(nodelist)
        print(nodelist)

    # while True:
    for i in range(block_num):
        nx=random.randint(1,num)
        trade_list,size_acc,fee_acc,trade_num = sim_trade(limit-head)
        total_fee+=fee_acc
        total_trade+=trade_num
        b=block.create_block(trade_list,limit,head)
        acceptence,nodelist=node.rep_manage(nodelist,nx-1,b,limit)
        if i%20==0:
            print('--------------------')
            print('trade no. %d',i)
            print(size_acc,fee_acc,nx)
            print(acceptence,'\n',nodelist)

    reputation=[]
    for n in nodelist:
        total_wallet+=n['wallet']
        reputation.append(n['rep'])
    print('--------------------')
    print('总结：')
    print(total_fee,total_wallet)
    print('system earned:',total_fee-total_wallet)
    print(total_trade,'trade has been successfully traded.')
    print('with',block_num,'block generated.')
    print('reputation:',np.min(reputation),np.mean(reputation),np.max(reputation))
    print('variance reputation:',np.var(reputation))
    print(nodelist)

if __name__ == '__main__':
    main()