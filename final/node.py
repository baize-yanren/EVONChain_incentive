class dealer:
    '''交易节点\n
    基础参数
    \n\n\twallet\n\n
    函数
    \n\n\tmake_transaction(self,amount,tran_fee)\n\n\tget_transaction(self,amount)'''
    def __init__(self,wallet):
        self.wallet = wallet
    def make_transaction(self,amount,tran_fee):
        '''提出交易请求，钱包扣除交易内容与交易费'''
        self.wallet -= amount + tran_fee
    def get_transaction(self,amount):
        '''完成交易，钱包获得交易内容'''
        self.wallet += amount

class miner:
    '''挖矿节点\n
    基础参数
    \n\n\tcpt_pw:节点总算力\n\n\tcpoc:节点投入链上算力\n\n\tbeta:链外单位算力收入\n\n\twallet:钱包\n\n
    函数
    \n\n\tmake_transaction(self,amount,tran_fee)\n\n\tget_transaction(self,amount)'''
    def __init__(self,cpt_pw,cpoc,beta,wallet):
        self.cpt_pw=cpt_pw
        self.cpt_pw_onchain=cpoc
        self.beta=beta
        self.wallet=wallet
    def make_transaction(self,amount,tran_fee):
        '''提出交易请求，钱包扣除交易内容与交易费'''
        self.wallet -= amount + tran_fee
    def get_transaction(self,amount):
        '''完成交易，钱包获得交易内容'''
        self.wallet += amount
    def mining(self,head):
        return head['check']
    
class cloud:
    '''云节点\n
    基础参数
    \n\n\twallet：钱包\n\n\twallet2：质押钱包\n\n\treputation：声誉
    函数
    \n\n\t'''
    def __init__(self):
        self.wlt = 0
        self.wlt2 = 0
        self.rep = 50
    def pack_in(self,trans):
        total_fee=sum(trans.fee)
        total_size=sum(trans.size)
        head={'check':True}
        return total_size,total_fee,head
    def pack_end(self, transaction_fee):
        """
        打包过程，根据声誉值分配交易费到两个钱包
        """
        if self.reputation < 100:
            # 声誉值未达到100时，按比例分配交易费
            self.wlt += transaction_fee * (self.reputation / 100)
            self.wlt2 += transaction_fee * (1 - self.reputation / 100)
        else:
            # 声誉值达到100后，全部交易费进入主钱包，并转移1%到主钱包
            self.wlt += transaction_fee + self.wlt2 * 0.05
            self.wlt2 = self.wlt2 * 0.95

        # 每次打包增加声誉值
        self.reputation = min(self.reputation + 1, 100)