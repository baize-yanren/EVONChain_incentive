# EVONChain_incentive

针对EVONChain的激励机制的代码实现

<!-- PROJECT SHIELDS -->

[![Contributors][contributors-shield]][contributors-url]
[![Forks][forks-shield]][forks-url]
[![Stargazers][stars-shield]][stars-url]
[![Issues][issues-shield]][issues-url]
 
## 目录

- [文件目录说明](#文件目录说明)
- [区块链的经济激励](#区块链的经济激励)
- [区块链的声誉激励](#区块链的声誉激励)
  - [本质逻辑](#本质逻辑)
  - [算法逻辑](#算法逻辑)
- [作者](#作者)


### 文件目录说明

```
filetree 
├── README.md
├── Algo1.py
├── Algo2.py
├── A1_GLM.py
├── test.py
├── test.csv
├── /project0402/
│  ├── incentive_allocation.py
│  ├── x_init.py
│  └── main.py
├── /project0429/
│  ├── incentive_allocation.py
│  ├── x_init.py
│  └── main.py
└── /reputation/
   ├── block.py
   ├── node.py
   └── main.py
```

### 区块链的经济激励

通过两阶段斯塔克博格博弈完成对矿工算力投入和挖矿奖励的博弈。

1.0/2.0版本：使用凸优化算法。

3.0版本：在单个不等式中取等式值。

### 区块链的声誉激励

#### 本质逻辑
1. 打包节点从交易池中取一定量交易进行打包，要求总大小小于1MB。打包节点结合其声誉值收取交易费。
$$NodeEarn=sum(fee)*\dfrac{NodeRep}{100}$$

<center>pls.在实际情况中节点会优先打包交易费高的交易，且块大小尽可能接近临界值</center>

2. 打包后交由挖矿节点进行挖矿并上链，过程中若发现区块非法，则将打包节点的声誉罚为0。原则上声誉为0的打包节点无法打包，打的包也不会被挖矿节点挖掘。
#### 算法逻辑
##### 1.0
1. 随机生成交易，累加至size_sum略小于limit时设定为即将被打包的一组。
$$(size,fee) \in ([1kb-20kb],[0,10])$$
$$limit=1MB-80B$$
<center>参照[比特币交易](https://bitcoin.org/en/developer-reference#tx)的格式。</center>

2. 在打包节点列表中随机一个节点进行打包，根据交易费与打包前声誉奖励打包费，根据其区块大小奖励声誉值。
$$NodeRep += \dfrac{BlockSize}{limit}$$
$$NodeEarn=sum(fee)*\dfrac{NodeRep}{100}$$

### 作者

白泽炎刃