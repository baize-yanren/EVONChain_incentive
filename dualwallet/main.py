import random

class PackingNode:
    def __init__(self):
        self.main_wallet = 0  # 主钱包
        self.staking_wallet = 0  # 质押钱包
        self.reputation = 50  # 初始声誉值

    def pack(self, transaction_fee):
        """
        打包过程，根据声誉值分配交易费到两个钱包
        """
        if self.reputation < 100:
            # 声誉值未达到100时，按比例分配交易费
            self.main_wallet += transaction_fee * (self.reputation / 100)
            self.staking_wallet += transaction_fee * (1 - self.reputation / 100)
        else:
            # 声誉值达到100后，全部交易费进入质押钱包，并转移1%到主钱包
            self.staking_wallet = self.staking_wallet * 0.99
            self.main_wallet += transaction_fee + self.staking_wallet * 0.01

        # 每次打包增加声誉值
        self.reputation = min(self.reputation + 1, 100)

    def __str__(self):
        return f"Main Wallet: {self.main_wallet}, Staking Wallet: {self.staking_wallet}, Reputation: {self.reputation}"

def generate_transactions(expected_fee):
    """
    生成随机交易笔数和计算交易费
    """
    transaction_count = random.randint(1000, 3999)
    total_fee = transaction_count * expected_fee
    return transaction_count, total_fee

def packing_simulation(node_count,expected_fee):
    """
    打包模拟
    """
    transaction_count, total_fee = generate_transactions(expected_fee)

    # 随机选择节点进行打包
    selected_node = random.choice(nodes)
    selected_node.pack(total_fee)

    return nodes, transaction_count, total_fee

# 模拟打包过程
node_count = 10
expected_fee = 10
r=500
nodes = [PackingNode() for _ in range(node_count)]
for i in range(r): 
    nodes,transaction_count,total_fee = packing_simulation(node_count,expected_fee)
    print('round',r)
    for node in nodes:
        print(node)
