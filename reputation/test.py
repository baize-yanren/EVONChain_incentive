import random
def sim_trade(limit):
    # 生成交易
    size_acc=0
    fee_acc=0
    tradelist=[]
    while True:
        size=random.uniform(1000,20000)#1kb-20kb
        fee=random.uniform(0,10)
        if size_acc+size>=limit:
            break
        size_acc+=size
        fee_acc+=fee
        tradelist.append((size,fee))
    return tradelist,size_acc,fee_acc

while True:
    tradelist,size_acc,fee_acc=sim_trade(1e6)
    if size_acc>=1e6:
        print(size_acc,fee_acc,tradelist)