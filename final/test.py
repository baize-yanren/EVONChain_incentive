# -*- encoding: utf-8 -*-
'''
@Description    :测试文件
@Date           :2024/05/29 16:10:57
@Author         :WangYR
@version        :1.0
'''
import sys_func as f
from sys_node import *

def test_tstp():
    '''
    交易池测试
    测试完成
    '''
    # 创建节点
    users, clouds, miners = f.generate_nodes(20, 1, 10, 1)
    transaction_pool = []
    fee=[4,5,6,7,8,9]
    for i in range(5):
        # 生成交易
        transaction_pool = f.generate_transactions(users,100,transaction_pool,fee)
        print('after gene:',len(transaction_pool))
        # 选择打包交易
        block, transaction_pool=f.pack_and_mine(clouds, miners, transaction_pool, 1)
        print('after pack:',len(transaction_pool))
        print(block)
    
def miner_chooce():
    '''
    矿工选择
    测试完成
    '''
    users, clouds, miners = f.generate_nodes(20, 1, 10, 1)
    total_hash_power = 0
    for miner in miners:
        total_hash_power+=miner.hashing_investment
    miners_probabilities = [miner.hashing_investment / total_hash_power for miner in miners]
    selected_miner = random.choices(miners, weights=miners_probabilities, k=1)
    return selected_miner[0]

if __name__ == '__main__':
    print(miner_chooce())