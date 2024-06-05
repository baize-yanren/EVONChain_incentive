# -*- encoding: utf-8 -*-
'''
@Description    :系统节点
@Date           :2024/05/15 14:34:33
@Author         :WangYR
@version        :1.1
\n包含类：
    Transaction:交易类
    Block:区块类
    CloudNode:云节点类
    MinerNode:矿工节点类
    UserNode:用户节点类
'''

import random
import matplotlib.pyplot as plt

# 补充的类和函数
class Transaction:
    current_id=1
    def __init__(self, sender, recipient, size, amount, fee):
        self.id = Transaction.current_id
        self.sender = sender  # 发送者
        self.recipient = recipient  # 接收者
        self.size = size # 交易大小
        self.amount = amount  # 交易金额
        self.fee = fee  # 交易费
        Transaction.current_id+=1
    def reset_id(self):
        Transaction.current_id = 1
    def __str__(self):
        return f"Transaction ID:{self.id}, size:{self.size}, amount:{self.amount}, fee:{self.fee}"

class Block:
    def __init__(self,num,sum_size,sum_fee,transactions):
        self.num=num
        self.size=sum_size
        self.fee=sum_fee
        self.transactions = transactions
    def __str__(self):
        return f"Block - Num:{self.num},size:{self.size},fee:{self.fee}"

class CloudNode:
    def __init__(self):
        self.main_wallet = 0  # 主钱包
        self.pledge_wallet = 0  # 质押钱包
        self.reputation = 50  # 初始声誉值

    def pack(self, transaction_pool):
        """
        从交易池中选择最有利的交易并打包
        """
        # 选择交易费最高、交易大小最小的交易
        if transaction_pool:
            most_beneficial_transaction = max(transaction_pool, key=lambda tx: tx.fee / tx.size)
            return most_beneficial_transaction
        else:
            return None

    def receive_fee(self, transaction_fee,tau):
        """
        根据规则获得交易费和声誉值
        """
        if self.reputation < 100:
            # 声誉值未达到100时，按比例分配交易费
            self.main_wallet += transaction_fee * (self.reputation / 100)
            self.pledge_wallet += transaction_fee * (1 - self.reputation / 100)
        else:
            # 声誉值达到100后，全部交易费进入主钱包，并转移1%到主钱包
            self.main_wallet += transaction_fee + self.pledge_wallet * tau
            self.pledge_wallet = self.pledge_wallet * (1-tau)

        self.reputation = min(self.reputation + 1, 100)

    def __str__(self):
        return f"Cloud Node - Main Wallet: {self.main_wallet}, Staking Wallet: {self.pledge_wallet}, Reputation: {self.reputation}"

class MinerNode:
    current_id=1
    def __init__(self, hashing_power, hashing_investment, gamma):
        self.hashing_power = hashing_power  # 算力
        self.hashing_investment = hashing_investment  # 算力投入
        self.gamma = gamma  # 链外单位算力收入
        self.wallet = 0  # 钱包
        self.id = MinerNode.current_id
        MinerNode.current_id+=1

    def validate(self, cloud_node, block):
        """
        验证云节点的打包合法性
        """
        # 简化模拟，假设每次验证都成功
        return True

    def receive_reward(self, alpha):
        """
        接收交易费作为奖励
        """
        self.wallet += alpha

    def __str__(self):
        return f"Miner Node - Miner Id: {self.id}, Wallet: {self.wallet}"

class UserNode:
    def __init__(self):
        self.wallet = 1000  # 初始钱包金额

    def send_transaction(self, transaction, amount, fee):
        """
        发起交易
        """
        if self.wallet >= amount + fee:
            self.wallet -= amount + fee
            transaction.recipient.receive_transaction(amount)
        return True

    def receive_transaction(self, amount):
        """
        接收交易
        """
        self.wallet += amount

    def __str__(self):
        return f"User Node - Wallet: {self.wallet}"



