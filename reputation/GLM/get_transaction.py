# -*- encoding: utf-8 -*-
'''
@Description    :单节点打包模拟
@Date           :2024/04/30 09:45:03
@Author         :WangYR
@version        :1.1
'''

import random
class Transaction:
    '''交易类'''
    def __init__(self, size, fee):
        self.size = size
        self.fee = fee

class Node:
    '''节点类'''
    def __init__(self, num, rep, wallet):
        self.num = num
        self.rep = rep
        self.wallet = wallet

def pack_block(transactions, maxBlockSize, node):
    blockSize = 0
    totalFee = 0

    selectedTransactions = []

    # Sort transactions by fee
    sortedTransactions = sorted(transactions, key=lambda t: t.fee, reverse=True)
    print(sortedTransactions[0].size,sortedTransactions[1].size,sortedTransactions[2].size,sortedTransactions[3].size)

    for t in sortedTransactions:
        if blockSize + t.size <= maxBlockSize:
            selectedTransactions.append(t)
            blockSize += t.size
            totalFee += t.fee

    # Update node's wallet
    node.wallet += totalFee*node.rep/100
    node.rep += blockSize/maxBlockSize
    if node.rep>100:
        node.rep=100

    return selectedTransactions


# Create some transactions
transactions = []

for i in range(1000):
    transactions.append(Transaction(random.uniform(1000,20000),random.uniform(0,10)))

# Create a node
node = Node(1, 50, 0)

# Pack a block
maxBlockSize = 1e6
selectedTransactions = pack_block(transactions, maxBlockSize, node)

print("Selected transactions:")
allfee=0
for t in selectedTransactions:
    print(f"Size: {t.size}, Fee: {t.fee}")
    allfee+=t.fee
print(f"Total fee: {allfee}")
print(f"Total transaction: {len(selectedTransactions)}")
print(f"Node {node.num} earned {node.wallet} coins, the reputation become {node.rep}")
