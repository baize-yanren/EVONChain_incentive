# -*- encoding: utf-8 -*-
'''
@Description    :经济声誉混合模拟
@Date           :2024/05/15 14:34:33
@Author         :WangYR
@version        :1.0
'''

import random

# 补充的类和函数

class Transaction:
    def __init__(self, sender, recipient, size, amount, fee):
        self.sender = sender  # 发送者
        self.recipient = recipient  # 接收者
        self.size = size # 交易大小
        self.amount = amount  # 交易金额
        self.fee = fee  # 交易费

class CloudNode:
    def __init__(self):
        self.main_wallet = 0  # 主钱包
        self.pledge_wallet = 0  # 质押钱包
        self.reputation = 50  # 初始声誉值

    def pack(self, transaction_pool, miner_node):
        """
        从交易池中选择最有利的交易并打包
        """
        # 选择交易费最高、交易金额最小的交易
        most_beneficial_transaction = max(transaction_pool, key=lambda tx: tx.fee / tx.size)
        
        if miner_node.validate(self, [most_beneficial_transaction]):
            transaction_fee = most_beneficial_transaction.fee
            self.receive_fee(transaction_fee)

    def receive_fee(self, transaction_fee):
        """
        根据规则获得交易费和声誉值
        """
        if self.reputation < 100:
            # 声誉值未达到100时，按比例分配交易费
            self.main_wallet += transaction_fee * (self.reputation / 100)
            self.pledge_wallet += transaction_fee * (1 - self.reputation / 100)
        else:
            # 声誉值达到100后，全部交易费进入主钱包，并转移1%到主钱包
            self.main_wallet += transaction_fee + self.pledge_wallet * 0.05
            self.pledge_wallet = self.pledge_wallet * 0.95

        self.reputation = min(self.reputation + 1, 100)

    def __str__(self):
        return f"Cloud Node - Main Wallet: {self.main_wallet}, Staking Wallet: {self.pledge_wallet}, Reputation: {self.reputation}"


class MinerNode:
    def __init__(self, hashing_power, hashing_investment, beta):
        self.hashing_power = hashing_power  # 算力
        self.hashing_investment = hashing_investment  # 算力投入
        self.beta = beta  # 链外单位算力收入
        self.wallet = 0  # 钱包

    def validate(self, cloud_node, transaction_pool):
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
        return f"Miner Node - Wallet: {self.wallet}"


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

    def receive_transaction(self, amount):
        """
        接收交易
        """
        self.wallet += amount

    def __str__(self):
        return f"User Node - Wallet: {self.wallet}"

def generate_nodes(user_count, cloud_count, miner_count, beta):
    """
    生成指定数量的用户节点、云节点和矿工节点
    """
    users = [UserNode() for _ in range(user_count)]
    clouds = [CloudNode() for _ in range(cloud_count)]
    miners = [MinerNode(1, 1, beta) for _ in range(miner_count)]
    return users, clouds, miners

def generate_transactions(users):
    """
    用户节点之间随机生成交易
    """
    transaction_pool = []
    for _ in range(100):
        sender = random.choice(users)
        recipient = random.choice(users)
        while recipient == sender:
            recipient = random.choice(users)
        amount = random.randint(1, 100)
        fee = random.uniform(0, 10)
        size=random.uniform(1000,20000)#1kb-20kb
        transaction = Transaction(sender, recipient, size, amount, fee)
        sender.send_transaction(transaction,amount, fee)
        transaction_pool.append(transaction)
    return transaction_pool

def pack_and_mine(clouds, miners, transaction_pool):
    """
    云节点进行一次打包，矿工节点进行挖矿和验证
    """
    # 云节点选择最有利的交易进行打包
    packer = random.choice(clouds)
    miner = random.choice(miners)
    sum_size = 0
    limit_size = 1000000
    num=random.randint(10,1000)
    i=0
    while sum_size<limit_size or i==num:
        packer.pack(transaction_pool, random.choice(miners))
        i+=1

    # 矿工节点进行挖矿和验证
    return miner.validate(packer, transaction_pool)

# 生成节点
users, clouds, miners = generate_nodes(20, 4, 10, 2)
for user in users:
    print(user)
for cloud in clouds:
    print(cloud)
for miner in miners:
    print(miner)

# 生成交易
transaction_pool = generate_transactions(users)

# 打包和挖矿
pack_and_mine(clouds, miners, transaction_pool)

# 打印节点信息
for user in users:
    print(user)
for cloud in clouds:
    print(cloud)
for miner in miners:
    print(miner)


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