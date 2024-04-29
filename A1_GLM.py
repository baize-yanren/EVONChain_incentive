import cvxpy as cp
import numpy as np

# 参数设置
N = 20  # 矿工数量
s = 1  # 每个矿工的计算能力上限
Z = 20  # PoW难度系数
T = 20  # PoW块生成的预期时间
b = 1  # 非挖矿收入因子

# 初始化变量
x = np.random.normal(10, 1, N)  # 服从(10,1)的正态分布
alpha = np.zeros(N)  # 初始化每个矿工的奖励

# 主循环
for i in range(N):
    # 计算除当前矿工外的其他矿工的计算资源分配之和
    j = np.sum(x[:i]) + np.sum(x[i+1:])
    
    # 构建并解决凸优化问题
    a = cp.Variable()
    obj = cp.Minimize(a)
    cons = [a >= j*b/s, a*T >= Z*(j + x[i])/s]
    prob = cp.Problem(obj, cons)
    prob.solve()
    
    alpha[i]=a.value
    # 更新当前矿工的计算资源分配
    x[i] = alpha[i]*j/(b*s)

# 输出结果
print("每个矿工的计算资源分配:", x)
print("每个矿工的奖励:", alpha)
