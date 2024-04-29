# -*- encoding: utf-8 -*-
'''
@Description    :node management
@Date           :2024/04/29
@Author         :WangYR
@version        :1.0
'''
def create_node(node_list):
    if node_list==None:
        node_list=[]
        node={'num':1,'rep':50,'wallet':0}
        node_list.append(node)
    else:
        node={'num':len(node_list)+1,'rep':50,'wallet':0}
        node_list.append(node)
    return node_list

def rep_manage(node_list,i,block,limit):
    """Manage node reputation\n
    参数：
        node_list: [{num: 节点编号,rep: 节点声誉,wallet: 钱包},...]
        block: {size:区块大小,num:打包的交易数目,fee:块内总交易费,safe:安全性}
        limit: 区块大小极限   
    输出：
        acceptence,node_list
    """
    if node_list[i]['rep']==0:
        # 若声誉为0，不承认其打包
        return False,node_list
    else:
        if block['safe']==True:
            # 打包数据安全可靠，接受打包，节点获取对应代币，声誉提高
            node_list[i]['wallet']+=block['fee']*node_list[i]['rep']/100
            node_list[i]['rep']+=block['size']/limit
            if node_list[i]['rep']>100:
                node_list[i]['rep']=100
            acce=True
        else:
            # 打包数据异常，声誉清零，不接受打包数据
            node_list[i]['rep']=0
            acce=False
        return acce,node_list

