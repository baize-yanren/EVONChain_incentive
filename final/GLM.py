class Transaction:
    def __init__(self, amount, size, fee):
        self.amount = amount  # 交易金额
        self.size = size  # 交易大小
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

    def send_transaction(self, recipient, amount, fee):
        """
        发起交易
        """
        if self.wallet >= amount + fee:
            self.wallet -= amount + fee
            recipient.receive_transaction(amount, fee)

    def receive_transaction(self, amount, fee):
        """
        接收交易
        """
        self.wallet += amount

    def __str__(self):
        return f"User Node - Wallet: {self.wallet}"




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
