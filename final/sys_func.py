# -*- encoding: utf-8 -*-
'''
@Description    :
@Date           :2024/05/29 15:35:54
@Author         :WangYR
@version        :1.0
\n包含函数：
    \ngenerate_nodes(user_count, cloud_count, miner_count, gamma)
    \ngenerate_transactions(users, num)
    \npack_and_mine(clouds, miners, transaction_pool, alpha)
'''
import random
from sys_node import *

def miner_chooce(miners):
    '''
    权重随机选择一个矿工节点
    '''
    total_hash_power = 0
    for miner in miners:
        total_hash_power+=miner.hashing_investment
    miners_probabilities = [miner.hashing_investment / total_hash_power for miner in miners]
    selected_miner = random.choices(miners, weights=miners_probabilities, k=1)
    return selected_miner[0]

def generate_nodes(user_count, cloud_count, miner_count, gamma):
    """
    生成指定数量的用户节点、云节点和矿工节点
    生成矿工节点时即确定该节点的链外单位收入
    """
    users = [UserNode() for _ in range(user_count)]
    clouds = [CloudNode() for _ in range(cloud_count)]
    miners = [MinerNode(1, 1, gamma) for _ in range(miner_count)]
    return users, clouds, miners

def generate_transactions(users,num,transaction_pool,fee_choice):
    """
    用户节点之间随机生成交易
    输入：
        users: 用户节点列表
        num: 需要生成的交易数量
        transaction_pool: 交易池
        fee_choice: 交易费列表
    输出：
        transaction_pool: 更新后的交易池
    """
    # transaction_pool = []
    for _ in range(num):
        sender = random.choice(users)
        recipient = random.choice(users)
        while recipient == sender:
            recipient = random.choice(users)
        amount = random.randint(1, 100)
        fee = random.choice(fee_choice)
        size=random.uniform(1000,20000)#1kb-20kb
        fee=fee*size/10000
        transaction = Transaction(sender, recipient, size, amount, fee)
        # print(transaction)
        if sender.send_transaction(transaction,amount, fee):
            transaction_pool.append(transaction)
    return transaction_pool

def pack_and_mine(clouds, miners, transaction_pool, alpha):
    """
    云节点进行一次打包，矿工节点进行挖矿和验证
    输入：
        clouds: 云节点列表
        miners: 矿工节点列表
        transaction_pool: 交易池
        alpha: 挖矿奖励系数
    输出：
        block: 打包后的区块
        transaction_pool: 更新后的交易池
    """
    # 云节点选择最有利的交易进行打包
    packer = random.choice(clouds)
    # 修改矿工算力投入
    miner = miner_chooce(miners)
    sum_size = 0
    sum_fee = 0
    limit_size = 1000000
    num=random.randint(10,500)
    i=0
    blocklist = []
    while sum_size<limit_size and i!=num:
        t=packer.pack(transaction_pool)
        if t==None:
            break
        else:
            if sum_size+t.size<limit_size:
                sum_size+=t.size
                sum_fee += t.fee
                transaction_pool.remove(t)
                blocklist.append(t)
                i+=1
            else:
                break

    block=Block(i,sum_size,sum_fee,blocklist)
    # print(block)
    # 矿工节点进行挖矿和验证
    if miner.validate(packer, block):
        packer.receive_fee(block.fee)
        miner.receive_reward(alpha)
    return block, transaction_pool