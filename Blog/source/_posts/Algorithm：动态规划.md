---
title: 动态规划
tags:
  - Algorithm
categories:
  - 算法
cover: /image/algorithm.png
abbrlink: 7bb01bb2
swiper_index: 6
date: 2024-10-22 15:09:35
description: 介绍了动态规划的原理，并用4个典例进行了详细分析，总结过后完成经典DP问题
---
<meta name="referrer" content="no-referrer"/>

## 1. 原理

**动态规划（Dynamic Programming,DP）**：通过把复杂的问题分解成更小的子问题，并记录这些子问题的解来避免计算重复子问题，从而达到降低计算复杂度的目的

两种分解的区别
|区别|分治策略|动态规划|
|-|-|-|
|划分点|通常只有一个划分点|可以有多个划分点|
|子问题性质|子问题之间都是相互独立的|子问题是重叠的：一是存在重复的子问题，而是子问题的解依赖于其他子问题|
|如何处理子问题|将子问题的解合并返回到上一级|低级子问题的解被全局存储，以供更高级的子问题使用|

动态规划的三要素
- **最优子结构**：一个问题的最优解可以通过其子问题的最优解来构建
- **重叠子问题**：一个问题的子问题在解决过程中会被多次计算，并且不会生成新的子问题
- **状态转移方程**：构建**动态规划表（DP TABLE）**

{% note warning flat %}
考虑寻找一个图中从起点到终点的最长简单路径，假设图为$A \leftrightarrows B \leftrightarrows C \leftrightarrows D \leftrightarrows A$，从A到D的最长简单路径是$A \leftarrow B \leftarrow C \leftarrow D$，如果拆成两个子问题，A到B的最长简单路径是$A \leftarrow D \leftarrow C \leftarrow B$，B到D的最长简单路径是$B \leftarrow A \leftarrow D$，合并在一起就是$A \leftarrow D \leftarrow C \leftarrow B \leftarrow A \leftarrow D$，显然这不是简单路径，不符合最优子结构！
{% endnote %}

动态规划的核心步骤
1. **刻画一个最优子结构**
2. **递归地定义重叠子问题 / 设计状态转移方程**
3. **采用自底向上的方法计算最优解的值**
4. **利用结果构造得到最优解的过程**

{% note warning flat %}
第4步是可选的，因为有时候题目不需要知道过程只需要知道结果
{% endnote %}

刻画最优子结构的方式
1. **证明求最优解的第一步总是做出一个选择，然后假定该选择就是最优的**
2. **基于上述选择，确定划分为多少个子问题，以及每个子问题空间是什么**
3. **利用“剪切-粘贴”法，证明子问题的最优解与原问题的最优解是一致的**

自底向上的方式
- **只求解一次子问题：精心安排求解顺序，保证第一次求解某个子问题时就可以得到其最优解**
- **问题只依赖于其子问题：精心设计求解方程，保证所有依赖的子问题都已经求解完毕**

## 2. 典例

### 2.1 钢条切割

##### 问题介绍

问题描述：有一根长度为n的钢条和一张价格表，目标是切割这根钢条使得销售这些片段可以获得最高收益（也可以不切割，一整根卖出去）

案例分析：假设有一根长度为4的钢条和如下的价格表，则有8种切割方案：$<(4),(1,3),(2,2),(3,1),(1,1,2),(1,2,1),(2,1,1),(1,1,1,1)>$，其中$(2,2)$的方案可以获得最高收益10
|长度|1|2|3|4|5|6|7|8|9|10|
|-|-|-|-|-|-|-|-|-|-|-|
|价格|1|5|8|9|10|17|17|20|24|30|

##### 第1步：刻画一个最优子结构

对于当前钢条，考虑全部最佳切割点中最左边的切割点，该切割点将钢条分为左段和右段，**可知左段不需要继续切割，右段需要继续切割（也可以不切割）**，因此**当前钢条的最优收益 = 左段价格 + 右段的最佳收益**

##### 第2步：递归地定义重叠子问题

假设钢条总长为n，左段长度为i，最佳收益为r，钢条价格为p，则有
$$
r_n = \begin{cases}
0 & \text{if }n = 0 \\
\max(p_i + r_{n-i}) & \text{if }0 < i \leq n
\end{cases}
$$

##### 第3步：采用自底向上的方法计算最优解的值

考虑每个长度l的钢条及其最大收益
- 对于长为0的钢条，最大收益就是0
- 对于长为1的钢条，最大收益就是价格
- 对于长为2的钢条，最大收益可以分为左1加右1，左2加右0，其中长为0、1的最大收益由前面步骤可得
- 对于长为3的钢条，最大收益可以分为左1加右2，左2加右1，左3加右0，其中长为0、1、2的最大收益由前面步骤可得
- 对于长为4的钢条，最大收益可以分为左1加右3，左2加右2，左3加右1，左4加右0，其中长为0、1、2、3的最大收益由前面步骤可得
- 以此类推，直到长为n，其中长为0、1、2、3、...、n-1的最大收益由前面步骤可得

##### 第4步：利用结果构造得到最优解的过程

记录长为l的钢条对应的最佳切割点，相当于记录最佳切割点对应的左段长度，那么**最优解 = 左段长度 + 右段钢条的左段长度 + 右段钢条的右段钢条的左段长度，以此类推，直到某次右段钢条的长度为0**

##### 代码实现

```python
# 从左到右输出每段长度
def optimal(left_len, n):
  left = 0
  right = n
  while right != 0:
    left = left_len[right]
    print(left)
    right = right - left

def cut_rod(p, n):
  # 最大收益
  reward = [0] * (n + 1)
  # 最佳切割点对应的左段长度
  left_len = [0] * (n + 1)
  # 每次循环得到长度为curlen的钢条的最大收益
  for cur_len in range(1, n + 1):
    # 初始化最大收益为负数，用于比较
    max_price = -1
    # 遍历所有切割点，i是左段长度，cur_len - i是右段长度
    for left in range(1, cur_len + 1):
      right = cur_len - left
      cur_price = p[left] + reward[right]
      # 更新最大收益和对应的切割点
      if cur_price > max_price:
        max_price = cur_price
        left_len[cur_len] = left
    # 记录cur_len的最大收益
    reward[cur_len] = max_price
  # 长度为n的最大收益
  max_price = reward[n]
  # 获取最优解的过程
  optimal(left_len, n)
  return max_price
```

### 2.2 矩阵乘法链

#### 问题介绍

问题描述：给定n个矩阵的乘法链，目标是找到一种结合顺序，使得计算矩阵乘法链所需要的标量乘法次数最小，其中$p \times q$和$q \times r$的矩阵相乘所需要的标量乘法次数为$p \cdot q \cdot r$，得到的结果矩阵为$p \times r$

案例分析：假设有三个矩阵A、B、C，它们的维度分别为10x100、100x5和5x50，有以下两种结合顺序，显然选择第1种的顺序所需的标量乘法次数更少
1. (AB)C：需要10x100x5 + 10x5x50 = 7500次标量乘法
2. A(BC)：需要10x100x50 + 100x5x50 = 75000次标量乘法

#### 第1步：刻画一个最优子结构

对于当前矩阵乘法链，找到一个最佳切割点分成左链和右链，相当于给左链和右链都加上一个括号，则**当前链的最小次数 = 左链的最小次数 + 右链的最小次数 + 两链结果相乘的次数**

#### 第2步：递归地定义重叠子问题

假设第i个矩阵的行值是$p[i]$，列值是$p[i+1]$，假设某条链的链首是第i个矩阵，链尾是第j个矩阵，该链的最小标量乘法次数表示为二维数组$m[i][j]$，对于切割点k，则有
$$
m[i][j] = \min_{i \leq k < j} (m[i][k] + m[k+1][j] + p[i] \cdot p[k+1] \cdot p[j+1])
$$

#### 第3步：采用自底向上的方法计算最优解的值

考虑每个链长l以及对应的链首i和链尾j，有$l = j - i + 1$
- l=2，最小标量乘法次数就是$p[i] \cdot p[i+1] \cdot p[i+2]$
- l=3，那么可以分解为左1乘右2，左2乘右1，其中长为2的由前面步骤可得
- l=4，那么可以分解为左1乘右3，左2乘右2，左3乘右1，其中长为2、3的由前面步骤可得
- l=5，那么可以分解为左1乘右4，左2乘右3，左3乘右2，左4乘右1，其中长为2、3、4的由前面步骤可得
- 以此类推，直到l=n，其中长为1、2、3、...、n-1的由前面步骤可得

#### 第4步：利用结果构造得到最优解的过程

需要额外的一个数组s[i][j]来保存该链对应的最佳切割点，那么**最优解 = （最佳切割点） 和 （左链的最佳切割点）和 （右链的最佳切割点） 和 （左链-左链的最佳切割点和左链-右链的最佳切割点） 和 （右链-左链的最佳切割点和右链-右链的最佳切割点）和 ...，以此类推，直到所有子链长度都是2即无法再分**

#### 代码实现

```python
# 递归求最优解
def optimal(s,i,j):
  if i == j:
    return 'A' + str(i)
  else:
    return '(' + optimal(s,i,s[i][j]) + 'x' + optimal(s,s[i][j]+1,j) + ')'

# 自底向上求最优解
def matrix_chain_order(p):
  # 矩阵个数即链的长度，-1是因为p多存了一个元素表示最后一个矩阵的列值
  n = len(p) - 1
  # 最小标量乘法次数
  m = [[0] * n for _ in range(n)]
  # 最佳切割点
  s = [[0] * n for _ in range(n)]
  # 每次循环得到长度为l的每个矩阵乘法链的最小标量乘法次数
  for l in range(2,n+1):
    # 遍历链首上标，根据公式l=j-i+1，且j最大为n-1，可知i最大为n-l
    for i in range(0,n-l+1):
      # 定义最小标量乘法次数为正无穷，用于比较
      min_mult = float('inf')
      # 计算链尾下标
      j = i + l - 1
      # 遍历每个切割点
      for k in range(i,j):
        # 左链
        left = m[i][k]
        # 右链
        right = m[k+1][j]
        # 当前最小标量乘法次数
        cur_mult = left + right + p[i]*p[k+1]*p[j+1]
        # 比较最小标量乘法次数
        if cur_mult < min_mult:
          min_mult = cur_mult
          s[i][j] = k
      # 得到长度为l的每个矩阵乘法链的最小标量乘法次数
      m[i][j] = min_mult
  # 最优解
  min_mult = m[0][n-1]
  res = optimal(s,0,n-1)
  return min_mult,res
```

{% note warning flat %}
m必须初始化为0，由于j=i+l-1，因此始终有j>i，所以要保证j<=i的矩阵值一直是0才能计算子问题的解
{% endnote %}

### 2.3 最长公共子序列

#### 问题介绍

问题描述：给定两个序列X和Y，目标是找到它们的最长公共子序列，其中子序列是指下标递增（不一定连续）的元素组成的序列，该问题又称为LCS问题（Longest Common Subsequence）

案例分析：假设X = ABDAB，Y = BCCDAACAB，它们的公共子序列有AB，BD，BDA，BDB，DAB，BDAB，其中最长的是BDAB，长度为4

#### 第1步：刻画一个最优子结构

定理：对于$X = <x_1,x_2,\ldots,x_m>$和$Y = <y_1,y_2,\ldots,y_n>$，它们之间任意一个LCS，记为$Z = <z_1,z_2,\ldots,z_k>$，则有以下三种情况
- 如果$x_m = y_n$，则$z_k = x_m = y_n$，且$Z_{k-1}$是$X_{m-1}$和$Y{n-1}$的LCS：只有$z_k = x_m = y_n$才能保证公共子序列是最大的，因此三个序列都减去这个元素同样满足LCS性质
- 如果$x_m \neq y_n$，且$z_k \neq x_m$，则$Z$是$X_{m-1}$和$Y$的LCS：$X$减去一个与LCS毫不相干的元素，$Z$依旧保持LCS性质
- 如果$x_m \neq y_n$，且$z_k \neq y_n$，则$Z$是$X$和$Y_{n-1}$的LCS：$Y$减去一个与LCS毫不相干的元素，$Z$依旧保持LCS性质

因此，问题可以分解为
- 如果$x_m = y_n$，则相当于求$X_{m-1}$和$Y{n-1}$的LCS
- 如果$x_m \neq y_n$，则相当于求$X_{m-1}$和$Y$的LCS和$X$和$Y_{n-1}$的LCS中的较长者

#### 第2步：递归地定义重叠子问题

假设$X = <x_1,x_2,\ldots,x_m>$和$Y = <y_1,y_2,\ldots,y_n>$，令$c[i,j]$表示$X_i$和$Y_j$的LCS的长度，则有
$$
c[i,j] = \begin{cases}
0 & \text{if } i = 0 \text{ or } j = 0 \\
c[i-1,j-1] + 1 & \text{if } i,j > 0 \text{ and } x_i = y_j \\
\max(c[i,j-1],c[i-1,j]) & \text{if } i,j > 0 \text{ and } x_i \neq y_j
\end{cases}
$$

#### 第3步：采用自底向上的方法计算最优解的值

考虑每个长度下的X和每个长度下的Y对应的c[i][j]
- 如果X或Y当前长为0，则对应的LCS都是0
- X最长为1
  - Y最长为1：LCS(1,1)的长度取决于LCS(0,1)，LCS(1,0)，LCS(0,0)，而这三个都在之前得到
  - Y最长为2：LCS(1,2)的长度取决于LCS(0,2)，LCS(1,1)，LCS(0,1)，而LCS(1,1)在之前已经得到
  - 以此类推，直到Y最长为n
- X最长为2
  - Y最长为1：LCS(2,1)的长度取决于LCS(1,1)，LCS(2,0)，LCS(1,0)，而LCS(1,1)在之前已经得到
  - Y最长为2：LCS(2,2)的长度取决于LCS(1,2)，LCS(2,1)，LCS(1,1)，而LCS(2,1)在之前已经得到
  - 以此类推，直到Y最长为n
- 以此类推，直到X最长为m

#### 第4步：利用结果构造得到最优解的过程

由定理可知，只有同时改变X和Y，即当$x_m = y_n$时，才会在LCS中加入元素$x_m$，其他情况下都是单独改变X或单独改变Y去寻找$x_m = y_n$的情况，所以一个二维数组记录每次情况

![](https://dasi-blog.oss-cn-guangzhou.aliyuncs.com/Algorithm/202410171523548.png)

#### 代码实现

```python
# 递归找最大公共子序列
def optimal(road, X, len_X, len_Y):
  if len_X == 0 or len_Y == 0:
    return ''
  # 从右下往左上遍历，因此新找到的元素要放在最后面
  if road[len_X][len_Y] == 'bingo':
    return optimal(road, X, len_X - 1, len_Y - 1) + X[len_X]
  elif road[len_X][len_Y] == 'left':
    return optimal(road, X, len_X, len_Y - 1)
  elif road[len_X][len_Y] == 'up':
    return optimal(road, X, len_X - 1, len_Y)

def LCS(X, Y):
  # 在X和Y的开头插入'$'，以匹配下标和序号
  X = '$' + X
  Y = '$' + Y
  len_X = len(X)
  len_Y = len(Y)
  common = [[0 for _ in range(len_Y)] for _ in range(len_X)]
  road = [['' for _ in range(len_Y)] for _ in range(len_X)]
  for i in range(1, len_X):
    for j in range(1, len_Y):
      if X[i] == Y[j]:
        common[i][j] = common[i - 1][j - 1] + 1
        road[i][j] = 'bingo'
      else:
        # 去掉当前X的最后一个元素得到的LCS
        X_left = common[i][j - 1]
        # 去掉当前Y的最后一个元素得到的LCS
        Y_up = common[i - 1][j]
        if X_left > Y_up:
          common[i][j] = X_left
          road[i][j] = 'left'
        else:
          common[i][j] = Y_up
          road[i][j] = 'up'
  res = optimal(road, X, len_X - 1, len_Y - 1)
  return common, res
```

### 2.4 最优二叉搜索树

#### 问题介绍

问题描述：给定n个关键字$<k_1,k_2,k_3,\ldots,k_n>$，其中还存在n+1个伪关键字$<d_0,d_1,d_2,\ldots,d_n>$，满足$d_n>k_n,\,k_i<d_i<k_{i+1}$，关键字没找到就会找到伪关键字，每个关键字有一个访问概率p，每个伪关键字也有一个访问概率q，假定搜索代价是找到关键字所访问的结点个数，即$depth(i)+1$，要求构造出一个二叉搜索树，使得在该树中的搜索各种关键字的代价最小，即：$1 + \sum_{i=1}^{n}{depth(k_i) \times p_i} + \sum_{i=0}^{n}{depth(d_i) \times q_i}$最小，也称为OBST问题（Optimal Binary Search Tree）

案例分析：对一个n=5的关键字集合及如下搜索概率，有以下两种树结构，其中第二种代价最小为2.75

|i|0|1|2|3|4|5|
|-|-|-|-|-|-|-|
|p_i|0.00|0.15|0.10|0.05|0.10|0.20|
|q_i|0.05|0.10|0.05|0.05|0.05|0.10|

![](https://dasi-blog.oss-cn-guangzhou.aliyuncs.com/Algorithm/202410171523550.png)
![](https://dasi-blog.oss-cn-guangzhou.aliyuncs.com/Algorithm/202410171523549.png)

{% note warning flat %}
最优二叉搜索树不一定是高度最矮的，搜索频率越大的也不一定出现在越上面
{% endnote %}

#### 第1步：刻画一个最优子结构

如果一颗树是最优二叉搜索树，则它的根节点的左子树和右子树也都是最优二叉搜索树

#### 第2步：递归地定义重叠子问题

假设当前树存在按序关键字$<k_i,k_{i+1},\ldots,k_j>$，其中选取$k_r,i\leq r \leq j$作为根结点，那么它的左子树就只有关键字$<k_i,\ldots,k_{r-1}>$和伪关键字$<d_{i-1},\ldots,d_{r-1}>$，右子树就只有关键字$<k_{r+1},\ldots,k_j>$和伪关键字$<d_r,\ldots,d_j>$

但子树的搜索代价是以其高度计算的，将子树插到原树的根节点的位置会导致高度增加1，因此需要计算子树插入原树导致的搜索代价增量，即$w[i][j]= 1 \times (\sum_{l=i}^{j}{p_l} + \sum_{l=i-1}^{j}{q_l})$，它也满足递归式$w[i][j] = w[i][r-1] + w[r+1,j] + 1 \times p_r$

令e[i][j]表示以关键字$<k_i,\ldots,k_j>$和伪关键字$<d_{i-1},\ldots,d_j>$组成的最优二叉搜索树的搜索代价则有：
$$
e[i][j] = 
\begin {cases}
q_i & \text{if } i > j \\
\min_{i\leq r \leq j} \{e[i][r-1] + e[r+1][j] + w[i][j]\} & \text{if } i \leq j
\end{cases}
$$

#### 第3步：采用自底向上的方法计算最优解的值

考虑每个子树的关键字的起始下标是i，终止下标是j，则结点总数为l = j - i + 1
- l=0，就是伪关键字，搜索代价为q[i-1]
- l=1，r只能是i（左0右0）
- l=2，r可以是i（左0右1），i+1（左1右0），其中结点总数为0、1的在之前已经算出
- l=3，r可以是i（左0右2），i+1（左1右1），i+2（左2右0），其中结点总数为0、1、2的在之前已经算出
- 以此类推，直到l=n，其中长为0、1、2、3、...、n-1的在之前已经算出

#### 第4步：利用结果构造得到最优解的过程

用一个二维数组root[i][j]记录划分子树选取的最佳根节点，那么**从root[1][n]选取的划分根节点开始划分成左子树和右子树，然后再选取左子树的划分根节点和右子树的划分根节点，以此类推，直到无法划分**

#### 代码实现

```python
# 先序遍历最优搜索二叉树
def optimal(root, i, j):
  if i == j + 1:
    print('d_' + str(j))
    return
  r = root[i][j]
  print('k_' + str(r))
  optimal(root, i, r-1)
  optimal(root, r+1, j)

def OBST(p,q):
  # p的下标从1开始，q的下标从0开始，但是他们最后一个下标都是n，因此在p的最前面加一个元素
  p = [0.0] + p
  length = len(q)
  w = [[0.0 for _ in range(length)] for _ in range(length)]
  e = [[0.0 for _ in range(length)] for _ in range(length)]
  root = [[0 for _ in range(length)] for _ in range(length)]
  # 由于l = j - i + 1，l = 0时，j = i - 1
  for i in range(1, length):
    e[i][i-1] = q[i-1]
    w[i][i-1] = q[i-1]
  for l in range(1, length):
    # j最大为length-1，根据公式l=j-i+1，因此i最大为length-l
    for i in range(1, length - l + 1):
      # 根据公式l=j-i+1,因此j=i+l-1
      j = i + l - 1
      e[i][j] = float('inf')
      w[i][j] = w[i][j-1] + p[j] + q[j]
      for r in range(i, j+1):
        if r + 1 > j:
          min_e = e[i][r-1] + q[j] + w[i][j]
        else:
          min_e = e[i][r-1] + e[r+1][j] + w[i][j]
        if min_e < e[i][j]:
          e[i][j] = min_e
          root[i][j] = r
  # 最优解
  optimal(root, 1, 5)
  min_e = e[1][length-1]
  return min_e
```

## 3. 总结

计算机没有人类的思维，但是他有人类无可比拟的计算能力，也就是说，任何基础问题计算机理论上都可以穷举出结果，然而**很多时候穷举是愚蠢的，计算机会花大量时间甚至90%的时间去穷举错误/不合理/不存在的情况，导致穷举的代价（时间和空间）变得巨大**

因此**算法实际上就是思考“如何聪明高效地穷举”，上述列出状态转移方程的本质就是找到一种合理的穷举方式**

总的来说，我认为，解决动态规划问题，就是要构建出一张DP TABLE
- DP TABLE的**第0行和第0列代表着平凡情况，也就是可以直接判断，不需要递归分解的情况**
- DP TABLE通常是**从左到右（一维），从左上到右下（二维）填充数据的**
- DP TABLE中任一元素的值通常**取决于其左上部分元素的值**

{% link 动态规划解题套路框架,labuladong 的算法笔记,https://labuladong.online/algo/essential-technique/dynamic-programming-framework-2/ %}

## 4. 经典DP

{% note warning flat %}
接下来的题目不会像之前那么详细地分析，只会给出**题目描述，算法思路和具体代码**
{% endnote %}

### 4.1 斐波那契数列

构建一张一维DP表，**dp[i]的值取决于前几个元素即dp[i-1], dp[i-2]等**

#### 4.1.1 爬楼梯

问题描述：给定一个整数n表示楼梯级数，一个人每次能上1、2或3级，问走到n级有多少种走法

算法描述：令dp[i]表示走i级一共有的走法，则dp[i]=dp[i-3]+dp[i-2]+dp[i-1]，且dp[1]=1，dp[2]=2，dp[3]=4

具体代码
```python
def climb_stairs(n):
  dp = [0 for _ in range(n + 1)]
  dp[1] = 1
  dp[2] = 2
  dp[3] = 4
  for i in range(4, n + 1):
    dp[i] = dp[i-3] + dp[i-2] + dp[i-1]
  print(dp[n])

n = 5
climb_stairs(n)
```

#### 4.1.2 解码数字串

问题描述：给定一个只包含数字的表示已编码的非空字符串s（长度大于等于2），使用如下映射进行解码："1" -> 'A'，"2" -> 'B'，...，"26" -> 'Z'，你需要计算并返回解码该字符串的所有可能方法的总数，并给出全部解码方案。（编码不包含前导0，即"06"不存在映射，但是"10"会映射到"J"）

算法思路：令dp[i]表示从第1个字符到第i个字符的解码方案数量，对于当前字符str[i]，分为三种情况：
1. str[i+1]是0，因此必须和这个0结合：dp[i]=dp[i-1],dp[i+1]=dp[i-1]；
2. str[i-1]和str[i]组成的数字位于1~26：dp[i]=dp[i-1]+dp[i-2]；
3. str[i]只能独自编码：dp[i]=dp[i-1]。

具体代码：
```python
def decode(string,mapping):
  n = len(string)
  string = '#' + string
  # dp用于存储方案数量，codes用于存储解码
  dp = [0 for _ in range(n+1)]
  dp[0] = 1
  codes = [[] for _ in range(n + 1)]
  codes[0] = [""]
  # 从1遍历到n
  i = 1
  while i != (n + 1):
    # 代码设计会跳过全部后导0，如果还能遍历到0，说明存在两个连续的零或者第一个就是0，肯定无法解码！
    if string[i] == '0':
      print("can't decode!")
      return 0
    # 当前字符是否必须和后面的0结合？
    if i != n and string[i+1] == '0':
      dp[i] = dp[i-1]
      dp[i+1] = dp[i-1]
      for code in codes[i - 1]:
        codes[i].append(code + mapping[string[i:i+2]])  
        codes[i+1].append(code + mapping[string[i:i+2]])
      i += 2
    # 当前字符是否可以和前一个字符结合解码？
    elif string[i-1] != '0' and string[i-1] != '#' and 1 <= int(string[i-1:i+1]) <= 26:
      dp[i] = dp[i-1] + dp[i-2]
      for code in codes[i - 1]:
        codes[i].append(code + mapping[string[i]])
      for code in codes[i - 2]:
        codes[i].append(code + mapping[string[i-1:i+1]])    
      i += 1
    # 当前字符只能单独解码
    else:
      dp[i] = dp[i-1]
      for code in codes[i - 1]:
        codes[i].append(code + mapping[string[i]])  
      i += 1
  print(f"{string[1:n]} decode: {codes[n]}")
  return dp[n]

string = '01101016'
mapping = {}
for i in range(1, 27):
  mapping[str(i)] = chr(i + 64)
print(f"there are {decode(string,mapping)} ways to decode {string}")
```

### 4.2 回合制博弈

构建一张二维DP表，假定**博弈双方都采取DP表的最优方案，当前回合的获胜情况取决于当前回合过后，对方回合的获胜情况**

#### 4.2.1 拿硬币

问题描述：假设有n个硬币，两个玩家 A 和 B 轮流从中拿硬币。每个玩家在自己的回合中可以选择从 1 到 k 个硬币（k 是一个固定的数且k<=n）进行拿取，拿完最后一个硬币的玩家获胜。如果A先拿，判断A是否必赢，如果必赢给出A必胜的方案

算法思路：令dp[i][j]表示己方还剩下i个硬币，最多可以拿j个硬币的情况下，赢1还是输0，如果至少存在一个k使得dp[i-k][j]=0，也就是存在一定击败对方的方法，那么己方就必赢，如果对全部k都有dp[i-k][j]=1，也就是无论怎么样对方都必赢，那么己方就必输

具体代码
```python
def take_coin(n,k):
  dp = [[-1 for _ in range(k+1)] for _ in range(n+1)]
  take = [[-1 for _ in range(k+1)] for _ in range(n+1)]
  for i in range(1, n+1):
    for j in range(1, k+1):
      if j >= i:
        dp[i][j] = 1
        take[i][j] = i
      else:
        if all(dp[i-t][j] == 1 for t in range(1, j+1)):
          dp[i][j] = 0
        else:
          for t in range(1, j+1):
            if dp[i-t][j] == 0:
              dp[i][j] = 1
              take[i][j] = t
              break
  # 游戏开始
  if dp[n][k] == 1:
    print(f"There are {n} coins and people can only take 1-{k} coins at a time!")
    rest = n
    while 1:
      # A回合
      a_take = take[rest][k]
      rest -= a_take
      print(f"A takes {a_take} and left {rest}")
      if rest == 0:
        print("A wins!")
        break
      # B回合
      b_take = int(input("please enter amount that B takes: "))
      rest -= b_take
      print(f"B takes {b_take} and left {rest}")
      if rest == 0:
        print("B wins!")
        break
  else:
    print("A must lose!")

# A先拿2，然后B拿1则A拿3，B拿2则A拿2，B拿3则A拿1，即A拿一个能使剩余为4的数量，最后B拿1则A拿3，B拿2则A拿2，B拿3则A拿1，即A拿一个能使剩余为0的数量，所以A百分之百胜利
take_coin(10, 3)
```

#### 4.2.2 拿石子

问题描述：有n堆石头放在一行（n为偶数），第i堆石头一共有array[i]个石头，每次只能拿最左边石堆或最右边的石堆，最后谁拿的石头总数最多谁获胜。如果A先拿，给出A能拿到最多石头的方案，并判断最后是否能获胜

算法思路：令dp[i][j]只剩下从第i堆到第j堆石头时可以获取的最多石头数量，令sum表示从第i堆到第j堆石头的石头总数，如果拿最左边大则dp[i][j] = sum - dp[i+1][j]，如果拿最右边大则dp[i][j] = sum - dp[i][j-1]

具体代码：
```python
def take_stone(array):
  n = len(array)
  array = [0] + array
  dp = [[0 for _ in range(n + 1)] for _ in range(n + 1)]
  stone = [[-1 for _ in range(n + 1)] for _ in range(n + 1)]
  # l = j - i + 1，j = i + l - 1，i = j - l + 1
  # l最大为n，j最大为n，i最大为n - l + 1
  for l in range(1, n + 1):
    for i in range(1, n - l + 2):
      j = i + l - 1
      if i == j:
        dp[i][j] = array[i]
      else:
        total = sum(array[i:j+1])
        left = total - dp[i+1][j]
        right = total - dp[i][j-1]
        if left > right:
          dp[i][j] = left
          stone[i][j] = 0
        else:
          dp[i][j] = right
          stone[i][j] = 1
  # 游戏开始
  left = 1
  right = n
  while left <= right:
    # A回合
    print(f"there are {array[left:right+1]}")
    direct_A = stone[left][right]
    if direct_A == 1:
      print(f"A takes {array[right]}")
      right -= 1
    else:
      print(f"A takes {array[left]}")
      left += 1
    # B回合
    print(f"there are {array[left:right+1]}")
    direct_B = int(input("enter your choice (0--left and 1--right): "))
    if direct_B == 1:
      print(f"you take {array[right]}")
      right -= 1
    else:
      print(f"you take {array[left]}")
      left += 1
  print(f"A got {dp[1][n]} and you got {sum(array) - dp[1][n]}")
  print("A wins" if dp[1][n] > (sum(array) - dp[1][n]) else "you win")

array = [28, 15, 1, 33, 24, 9, 17, 10]
take_stone(array)
```

### 4.3 背包问题

这类问题通常给定一个限制，然后每个元素都可以选择执行或不执行，构建一张二维DP表，其中**行遍历元素个数，列遍历限制数**

#### 4.3.1 0/1背包

问题描述：给定n个物品，每个物品都有体积volume和价值value，目标是找到能够装入固定容量为c的背包中的最大价值，其中每个物品只能选择放入背包或不放入

算法思路
- 按顺序排好物体，dp[i][j]表示容量为i时将前j个物品放入背包的最大价值，其中i的取值为[1,c]，j的取值为[1,n]，那么结果就是dp[n][c]
- 先遍历容量，再遍历物品，假设此时已经遍历到dp[i][j]，对于第j个物体
  - 如果它的体积已经大于背包容量，那么肯定无法放下，则dp[i][j]=dp[i][j-1]
  - 如果它的体积小于等于背包容量，那么可以选择放和不放，放的话就是剩下体积放前j-1个物品的最大价值加上第j个物品的价值，因此dp[i][j]=max(dp[i][j-1]，dp[i-volume(j)][j-1]+value(j))

具体代码
```python
def Knapsack(volume, value, n, c):
  dp = [[0 for _ in range(n+1)] for _ in range(c+1)]
  index = [[[] for _ in range(n+1)] for _ in range(c+1)]
  for i in range(1, c+1):
    for j in range(1, n+1):
      if volume[j] > i:
        dp[i][j] = dp[i][j-1]
        index[i][j] = index[i][j-1]
      else:
        not_put = dp[i][j-1]
        put = dp[i-volume[j]][j-1] + value[j]
        if not_put > put:
          index[i][j] = index[i][j-1]
          dp[i][j] = not_put
        else:
          index[i][j] = index[i-volume[j]][j-1]
          index[i][j].append(j)
          dp[i][j] = put
  print(dp[c][n])     # 14
  print(index[c][n])  # [2, 3, 4, 5]

n = 5
c = 10
volume = [0,5,4,3,2,1]
value = [0,1,2,3,4,5]
Knapsack(volume, value, n, c)
```

#### 4.3.2 最小划分数组

问题描述：给出一个正整数数组，把它分成S1、S2两部分，使S1的数字和与S2的数字和的差的绝对值最小

算法思路
- 已知SUM=S1+S2是不变的，令|S1-S2|最小，即令|S1-(SUM-S1)|最小，即令|2S1-SUM|最小，即令|S1-SUM/2|最小，且S1和S2中肯定有一个小于等于SUM/2，不妨令S1小于等于SUM/2，即在S中找到一个子集S1，使得S1尽可能接近SUM/2，因此对于每个元素，他要么放进S1，要么不放进S1，可以看成类背包问题
- 令dp[i][j]表示前j个元素最接近i的和，则结果就是dp[sum/2][n]

具体代码
```python
def minimum_partition(array,n):
  sumnum = sum(array)
  total = sumnum // 2
  s1 = [[[] for _ in range(n+1)] for _ in range(total+1)]
  dp = [[0 for _ in range(n+1)] for _ in range(total+1)]
  for i in range(1,total+1):
    for j in range(1,n+1):
      if array[j] > i:
        dp[i][j] = dp[i][j-1]
        s1[i][j] = s1[i][j-1][:]
      else:
        not_put = dp[i][j-1]
        put =  dp[i-array[j]][j-1] + array[j]
        if not_put > put:
          dp[i][j] = not_put
          s1[i][j] = s1[i][j-1][:]
        else:
          dp[i][j] = put
          s1[i][j] = s1[i-array[j]][j-1][:]
          s1[i][j].append(array[j])
  print(abs(2 * dp[total][n] - sumnum))
  print(s1[total][n])

array = [0, 1, 6, 11, 5]
minimum_partition(array,4)
```

#### 4.3.3 子集和

问题描述：给定一个非负整数的集合S，一个值M，问S中是否有一个子集，使得子集和等于M（注意集合里不存在相同的元素）

算法思路：令dp[i][j]表示前j个数是否可以刚好凑成i
- 对于i=0，平凡凑成
- 如果array[j]>i，则dp[i][j]=dp[i][j-1]
- 如果array[j]<=i且dp[i-array[j]][j-1]==1，即用前j-1个数正好也可以凑成i-array[j]，则dp[i][j]=1，且往后可以不用计算了，即使可能存在不同方案
- 如果array[j]<=i且dp[i-array[j]][j-1]==0，即用前j-1个数不能凑成i-array[j]，则dp[i][j]=0

具体代码：
```python
def subsetsum(array,key):
  n = len(array)
  array = [0] + array
  dp = [[0 for _ in range(n+1)] for _ in range(key+1)]
  num = [[[] for _ in range(n+1)] for _ in range(key+1)]
  # 构成0是始终可行的
  for j in range(n+1):
    dp[0][j] = 1
  for i in range(1,key+1):
    for j in range(1,n+1):
      if array[j] > i:
        dp[i][j] = dp[i][j-1]
      elif dp[i-array[j]][j-1] == 1:
        # 往后都不用判断了，都是百分之百可行的，虽然可能有别的方法
        for k in range(j,n+1):
          dp[i][k] = 1
          num[i][k] = num[i-array[j]][j-1][:]
          num[i][k].append(array[j])
        break
  if dp[key][n] == 1:
    print(f"there is a subset {num[key][n]} whose sum is {key}!")
  else:
    print(f"there is no subset whose sum is {key}!")

array = [6, 2, 9, 8, 3, 7]
print(f"set is {array}")
subsetsum(array,17) # [6, 2, 9]
subsetsum(array,26) # [6, 9, 8, 3]
subsetsum(array,31) # no
subsetsum(array,33) # [6, 9, 8, 3, 7]
```

### 4.4 最优选择策略

这类问题通常每种情况下有几个选项可供选择，**dp[i]的值往往与其相邻元素有关**

#### 4.4.1 最小路径和

问题描述：给定一个包含非负整数的二维网格grid，每个格子中的数值表示从该位置到其相邻格子的移动成本，只允许向下或向右移动，找到从左上角到右下角的最小路径和

算法思路：令dp[i][j]表示从左上角到(i,j)的最小路径和，因为只允许向下或向右移动，也就是说dp[i][j] = max(dp[i-1][j] + cost[i-1][j], dp[i][j-1] + cost[i][j-1])，同时，最上面一行和最左边一列的dp是可以直接确定的

具体代码
```python
def MinimumPath(array,row,col):
  dp = [[0 for _ in range(col)] for _ in range(row)]
  direct = [['' for _ in range(col)] for _ in range(row)]
  direct[0][0] = 'begin->'
  for j in range(1, col):
    dp[0][j] = dp[0][j-1] + array[0][j-1]
    direct[0][j] = direct[0][j-1] + 'right->'
  for i in range(1, row):
    dp[i][0] = dp[i-1][0] + array[i-1][0]
    direct[i][0] = direct[i-1][0] + 'down->'
  for i in range(1, row):
    for j in range(1, col):
      down = dp[i-1][j] + array[i-1][j]
      right = dp[i][j-1] + array[i][j-1]
      if down < right:
        dp[i][j] = down
        direct[i][j] = direct[i-1][j] + 'down->'
      else:
        dp[i][j] = right
        direct[i][j] = direct[i][j-1] + 'right->'
  direct[-1][-1] = direct[-1][-1] + 'end'
  # begin->down->right->down->right->end
  print(direct[-1][-1])
  # 14
  print(dp[-1][-1])

array = [
  [1, 3, 4],
  [2, 5, 9],
  [7, 6, 0]
]
MinimumPath(array,3,3)
```

#### 4.4.2 股票买卖

问题描述：给定一个数组price，其中price[i]表示第i天的股票价格，可以进行多次交易，但是每次交易必须先买入然后卖出，通过选择合适的买入和卖出时机，计算在第n天可以获得的最大利润，注意不可以在同一天进行买入和卖出，同时认为每次买入和卖出的量都是1

算法思路：dp[i]表示第i天获得的最大收益，假设已经遍历到第i天，那么可以两种选择，选择其中的较大值
- 不进行任何操作，那么dp[i]=dp[i-1]
- 卖股票，那么就要在之前选择一天j买股票，那么dp[i]=dp[j-1]+price[i]-price[j]

具体代码
```python
def stock_jobbing(price,n):
  dp = [0 for _ in range(n + 1)]
  deal = [[] for _ in range(n + 1)]
  for i in range(1,n+1):
    not_sold = dp[i-1]
    sold = -float('inf')
    buy_day = -1
    for j in range(1,i):
      temp = dp[j-1] + price[i] - price[j]
      if temp > sold:
        sold = temp
        buy_day = j
    if sold > not_sold:
      dp[i] = sold
      deal[i] = deal[buy_day-1]
      deal[i].append((buy_day,i))
    else:
      dp[i] = not_sold
      deal[i] = deal[i-1]
  print(dp[n])    # 7
  print(deal[n])  # [(1, 2), (3, 4)]

price = [0, 7, 1, 5, 3, 6, 4]
n = 6
stock_jobbing(price, n)
```

#### 4.4.3 编辑距离

问题描述：给定两个字符串 word1 和 word2，计算将 word1 转换为 word2 所需的最小编辑操作次数，允许的操作有插入一个字符、删除一个字符或替换一个字符。示例：intention->替换i为e->entention->删除t->enention->替换n为c->enection->替换n为x->exection->插入u->execution，一共5次（其中一种）

算法思路：
- 令dp[i][j]表示将word1（长度为n）的前i个字符变为word2（长度为m）的前j个字符所需要的最小编辑次数，则最终结果就是dp[n][m]
- 假设遍历到dp[i][j]，我们保证知道dp[0~i][0~j]的值，也就是说我们可以认为我们知道：
  - 如何最简单地将word1[1:i]转换为word2[1:j-1]，那么只需要在word1的最后添加一个word2[j]就行了：dp[i][j] = dp[i][j-1] + 1
  - 如何最简单地将word1[1:i-1]转换为word2[1:j]，那么只需要在word1的最后删除一个word2[j]就行了：dp[i][j] = dp[i-1][j] + 1
  - 如何最简单地将word1[1:i-1]转换为word2[1:j-1]，那么只需要在word1的最后把word[i]变为word[j]就行了：dp[i][j] = dp[i-1][j-1] + 1
- 考虑平凡情况
  - dp[i][0] = i：删除word1的全部前i个字符
  - dp[0][j] = j：插入word2的全部前j个字符
  - dp[i][j] = dp[i-1][j-1]：字符一样，不需要更改，word[i] = word[j]

具体代码
```python
def edit_distance(word1, word2):
  n = len(word1)
  m = len(word2)
  word1 = '0' + word1
  word2 = '0' + word2
  dp = [[0 for _ in range(m + 1)] for _ in range(n + 1)]
  operations = [[[] for _ in range(m + 1)] for _ in range(n + 1)]

  for i in range(1, n + 1):
    dp[i][0] = i  # 删除操作
    operations[i][0].append("Delete " + word1[i])
  for j in range(1, m + 1):
    dp[0][j] = j  # 插入操作
    operations[0][j].append("Insert " + word2[j])

  for i in range(1, n + 1):
    for j in range(1, m + 1):
      if word1[i] == word2[j]:
        dp[i][j] = dp[i - 1][j - 1]
        operations[i][j] = operations[i - 1][j - 1]  # 无操作
      else:
        insert = dp[i][j - 1] + 1
        delete = dp[i - 1][j] + 1
        replace = dp[i - 1][j - 1] + 1

        # 找到最小操作并记录
        if insert <= delete and insert <= replace:
          dp[i][j] = insert
          operations[i][j] = operations[i][j - 1][:]
          operations[i][j].append("Insert " + word2[j])
        elif delete <= insert and delete <= replace:
          dp[i][j] = delete
          operations[i][j] = operations[i - 1][j][:]
          operations[i][j].append("Delete " + word1[i])
        else:
          dp[i][j] = replace
          operations[i][j] = operations[i - 1][j - 1][:]
          operations[i][j].append("Replace " + word1[i] + " with " + word2[j])

  print("edit distance:", dp[n][m])
  print(f"from {word1[1:]} to {word2[1:]} opearations:")
  for op in operations[n][m]:
    print(op)

# 示例使用
word1 = "intention"
word2 = "execution"
edit_distance(word1, word2)
```

### 4.5 子序列

这类问题的做法比较统一，就是**先从小到大遍历长度l，然后dp[i][j]表示不同的起点i和终点j，根据长度l填充表**

#### 4.5.1 最长回文子序列（Longest Palindrome Subsequence,LPS）

问题描述：回文子序列是指正着读和反着读都相同的子序列，给定一个字符串，求该字符串的最长回文子序列的长度

算法思路：令dp[i][j]表示从i到j子串的最长回文子序列，对于长度为l且从i到j的子串，如果i和j相同，则dp[i][j] = dp[i+1][j-1] + 2，否则dp[i][j] = max(dp[i+1][j],dp[i][j-1])

具体代码
```python
def LPS(str):
  n = len(str)
  str = '0' + str
  char = [[str[k] for k in range(n+1)] for _ in range(n+1)]
  dp = [[1 for _ in range(n+1)] for _ in range(n+1)]
  # l = j - i + 1，因此j = i + l - 1，i最大为n - l + 1
  for l in range(2, n + 1):
    for i in range(1, n - l + 2):
      j = i + l - 1
      if str[i] == str[j]:
        dp[i][j] = dp[i+1][j-1] + 2
        char[i][j] = str[i] + char[i+1][j-1] + str[j]
      else:
        if dp[i+1][j] > dp[i][j-1]:
          dp[i][j] = dp[i+1][j]
          char[i][j] = char[i+1][j]
        else:
          dp[i][j] = dp[i][j-1]
          char[i][j] = char[i][j-1]
  print(char[1][n])
  print(dp[1][n])

str = 'zabxcdyefxghaz'
LPS(str)
```

#### 4.5.2 最长上升子序列（Longest Increasing Subsequence，LIS）

问题描述：给定一个长度为n的数组，找出一个最长的单调递增子序列

算法思路：令dp[i][j]表示从i到j的子串的最长单调递增子序列，有两种情况，选择两者中的最大值
- array[j]作为最后的数字，找到所有小于array[j]的索引k，则dp[i][j] = max(dp[i][k] + 1)对于i<=k<j
- array[j]不作为最后的数字，则dp[i][j]=dp[i][j-1]

```python
def LIS(array):
  n = len(array)
  array = [-1] + array
  dp = [[0 for _ in range(n+1)] for _ in range(n+1)]
  sequence = [[[] for _ in range(n+1)] for _ in range(n+1)]
  # l = j - i + 1, i = j - l + 1, j = i + l - 1
  # j最大为n，所以i最大为n - l + 1
  for l in range(1,n+1):
    for i in range(1,n - l + 2):
      j = i + l - 1
      if i == j:
        dp[i][j] = 1
        sequence[i][j].append(array[i])
      else:
        islast = -float('inf')
        index = -1
        for k in range(i,j):
          if array[k] < array[j] and islast < (dp[i][k] + 1):
            islast = dp[i][k] + 1
            index = k
        notlast = dp[i][j-1]
        if islast > notlast:
          dp[i][j] = islast
          sequence[i][j] = sequence[i][k][:]
          sequence[i][j].append(array[j])
        else:
          dp[i][j] = notlast
          sequence[i][j] = sequence[i][j-1][:]
  print(f"LIS is {sequence[i][j]} whose length is {dp[1][n]}")


array = [4,5,1,7,3,8,9]
print(array)
LIS(array)
array = [3,2,7,1,5,4,6,9,8,0,10]
print(array)
LIS(array)
```
