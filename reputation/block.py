# -*- encoding: utf-8 -*-
'''
@Description    :block management
@Date           :2024/04/29
@Author         :WangYR
@version        :1.0
'''
# block: {size:区块大小,num:打包的交易数目,fee:交易费表,safe:安全性}
def block_safe_check(block,limit):
    if block['size']<=limit:
        return True
    else:
        return False
    
def create_block(trade_list,limit,head):
    '''
    输入：
        trade_list: [(size,fee),...]
    输出：
        block: {size:区块大小,num:打包的交易数目,fee:交易费表,safe:安全性}
    '''
    total_size=0
    total_fee=0
    for t in trade_list:
        total_size+=t[0]
        total_fee+=t[1]
    block={'size':total_size,'num':len(trade_list),'fee':total_fee,'safe':None}
    block['safe']=block_safe_check(block,limit-head)
    return block
