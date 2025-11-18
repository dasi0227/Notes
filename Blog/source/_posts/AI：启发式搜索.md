---
title: 启发式搜索
tags:
  - AI
categories:
  - 笔记
description: 利用评估函数f(n) = g(n) + h(n)，主要算法有GBFS，A，A*和IDA*，可以利用松弛条件创造可接纳的启发式函数，最后用A*算法解决八数码问题
cover: image/ai.png
abbrlink: 5ef94582
date: 2024-07-01 09:51:08
---
<meta name="referrer" content="no-referrer"/>

## 1. 启发式搜索

盲目搜索的局限性：没有考虑边界上哪一个状态结点更具有前景，即扩展它更有可能得到目标状态，然而实际问题中可以根据额外的知识来衡量每个状态的前景

**评估函数：f(n) = g(n) + h(n)**
- 实际代价函数g(n)：从起始结点到当前结点的最小步数估计值，影响得到解的最优性
- 启发式函数h(n)：从当前结点到目标结点的最小步数估计值，影响发现解的速度
- 评估函数f(n)：从起始结点到目标结点且经过当前结点的最小步数估计值

![](https://i-blog.csdnimg.cn/blog_migrate/d6bd46a7d49d912f1b560446a5f6b8b9.png)

## 2. 贪婪最好优先搜索算法（GBFS）

核心思想：只令f(n)=h(n)，选择边界中h值最小的结点来扩展

步骤：
1. 从初始结点开始，将其放入优先级队列中
2. 从优先级队列中取出h(n)最小的结点
3. 如果该结点是目标结点，则搜索结束并返回过程
4. 否则，扩展该结点，将其邻居结点加入优先级队列中，并根据它们的评估函数值重新排序队列
5. 重复2-4步，直到找到目标结点或优先级队列为空

评测
- 贪婪的本质：每一步都倾向于沿着直接通往目标的路径前进，然而却忽略了先前路径的实际代价，可能会导致在搜索空间中陷入局部最优解而非全局最优解
- 不具有完备性
- 不具有最优性

## 3. A和A*算法

### 3.1 核心思想

- 令f(n)=g(n) + h(n)，选择边界中f值最小的结点来扩展，并在扩展过程中不断更新每个结点的g值
- 更新路径：若已知结点n的实际代价g(n)和从结点n到结点m的路径为c(n->m)，则g(m) = g(n) + c(c->m)
- *的含义：在数学中，一个变量加*（star）表示最优状况，当A算法中的参数设置最优时，A算法会演变为A*算法

### 3.2 数据结构

- OPEN表：存储还未被扩展且可以被扩展的结点
- CLOSED表：存储已经被扩展的结点
- 结点n的数据域：h(n)，g(n)
- 结点n的指针域：父结点指针，子结点指针

### 3.3 A算法的步骤

1. 将初始结点s放入OPEN表，将CLOSED表清空
2. 将OPEN表中的结点按照评估函数值的大小升序排列，取出评估函数值最小的结点n
3. 如果结点n不是目标结点且它有后继结点，遍历它的所有后继结点m：
  1. 如果后继结点m在OPEN表，说明后继结点m有两个父结点，即有两条从初始结点s到结点m路径，因此更新后继结点选择较小的g值，并更新后继结点m的父结点指针为结点n
  2. 如果后继结点m在CLOSED表，说明后继结点m有两个父结点，如果后继结点m相对于结点n的g值更小，则更新后继结点m的父结点指针为结点n，并将该后继结点m移除CLOSED表加入OPEN表，回到第3.1步
  3. 如果后继结点不在OPEN表也不在CLOSED表，说明找到一个全新结点，直接将后继结点m加入OPEN表
4. 将结点n放入CLOSED表中，如果OPEN表不为空，回到第2步

方框图

![](https://i-blog.csdnimg.cn/blog_migrate/5b3d6cc7aa7fd88472b5e8c633602e4d.png)

伪代码

![](https://i-blog.csdnimg.cn/blog_migrate/2051db5be1bda92d570c72648c9f8d8d.png)

### 3.4 A*算法的区别

在上述3.2步时，如果n的后继结点m在CLOSED表，我们会更新相关信息并把m移除CLOSED表加入OPEN表。
但是如果设置的启发式函数h的是最优的启发式函数h*，那么A算法会进化成A*算法，区别在于：
- 第一次遍历到后继结点m并将m加入到CLOSED表时，就已经找到了结点m的最优目标函数值f*(m)，之后如果再遍历到m，就无需判断更新，即CLOSED表只进不出
- 可以发现，A*算法会比A算法节省很多空间和时间，因此关键在于：如何实现A* --> 如何设置最优启发式函数f* --> 如何设置最优评估函数h*

![](https://i-blog.csdnimg.cn/blog_migrate/b47f0db4f56328f7a9786b20ed4746af.jpeg)

## 4. h*(n)的性质

1. 可采纳性：假设h*(n)是从结点n到目标结点的实际最优路径成本，当对于所有节点n，满足h(n) <= h*(n)

> 理解：h(n)是从结点n到目标结点的估计路径成本，如果估计比实际还低，那么对于用户来说显然是欣然接受的

2. 单调性：对任一结点n和它的后继节点m都有h(n)<=c(n->m) + h(m)

> 理解：从n到目标结点的估计，永远都比先从n到m再从m到目标结点的估计小

3. 定理
- 满足可采纳性则满足最优性（反之不一定成立）
- 满足单调性则一定满足可采纳性（反之不一定成立）
- 最优性保证我们在第一次遍历到一个结点时，就是沿着到这个结点的最优路径扩展的，因此如果h(n)满足单调性，则不需要进行环检测

## 5. 迭代加深A*算法

步骤
1. 初始化深度阈值为起始结点的评估函数值，将起始结点入栈
2. 弹出栈顶结点，如果栈顶结点等于目标结点，则退出循环并返回路径
3. 否则，对栈顶结点的全部子结点进行判断：
  1. 若该子结点的评估函数值 > 当前深度阈值，则忽略该子结点
  2. 若该子结点的评估函数值 ≤ 等于当前深度阈值，则将该子结点入栈
4. 重复执行3和4步，直到栈空则递增深度阈值，返回第2步开始

性质分析
- 优点：避免了无用结点的存储，所需内存小，空闲复杂度小
- 缺点：每次增加深度，都要从起始结点重新开始迭代，时间复杂度高

## 6. 创建可接纳的启发式函数

### 6.1 松弛问题

概念：将原始问题的制约条件删减得到松弛问题，将松弛问题解作为启发式函数

原理：因为松弛问题的解步骤一定比原始问题的解步骤少，即h(n) < h*(n)

常用方法：网格问题中的距离公式：假设两位置为(x1,y1)、(x2,y2)
- Manhattan曼哈顿距离d = |x1-x2| + |y1-y2|
- Diagonal对角线距离d = max{|x1-x2| , |y1-y2|}
- Euclidean欧式距离d = [(x1-x2)2 + (y1-y2)2]1/2

### 6.2 例子：八数码问题

1. 方法一
  - 松弛问题：只要方块A和B位置上/下/左/右相邻就可以把A移动到B
  - 启发式函数h(n) = 所有方块到达其目标位置的曼哈顿距离之和

![](https://i-blog.csdnimg.cn/blog_migrate/6be2781361833313ca4b5decd277571d.jpeg)

2. 方法二
  - 松弛问题：任意情况都可以移动
  - 启发式函数h(n) = 当前状态与目标状态位置不同的方块数

![](https://i-blog.csdnimg.cn/blog_migrate/875057d51207416bc98cd80a071f3c47.png)

### 6.3 支配

定义：假设h1和h2都是可采纳的启发式函数，如果对任意结点n都有h1(n) < h2(n)，则h2支配了h1函数

> 理解：h2支配h1，说明h2比h1含有更多的启发式信息，更具有价值

定理：若h2支配h1，那么使用h2扩展的结点包含了使用h1扩展的结点

最大式组合：若h2和h1互不包含，可以取h = max(h1,h2)
     

## 7. 实践：八数码问题

```python
import numpy as np

class Node:
  def __init__(self,matrix,cost,path):
    self.matrix = matrix                    # 状态
    self.cost = cost                        # 代价
    self.value = self.evaluate(self.matrix) # 价值
    self.path = path                        # 从起始结点到当前结点的路径

  # 评估函数：曼哈顿距离
  def evaluate(self,cur_matrix):
    end_matrix = np.array([[1, 2, 3], [8, 0, 4], [7, 6, 5]])
    Manhattan_distance = 0
    # 坐标绝对值差的总和
    for index,element in np.ndenumerate(cur_matrix):
      x1,y1 = index[0],index[1]
      x2,y2 = find_number(end_matrix,element)
      Manhattan_distance += abs(x1-x2)
      Manhattan_distance += abs(y1-y2)
    return Manhattan_distance

# 找到数字的行列坐标
def find_number(matrix,number):
  x,y = np.where(matrix == number)
  return x[0],y[0]

# 与0交换位置，获取当前状态的全部子状态
def swap_zero(matrix):
  x,y = find_number(matrix,0)
  sub_matrixs = []
  # 往上移动
  if x != 0:
    num = np.copy(matrix)
    num[x][y] = num[x-1][y]
    num[x-1][y] = 0
    sub_matrixs.append(num)
  # 往下移动
  if x != 2:
    num = np.copy(matrix)
    num[x][y] = num[x+1][y]
    num[x+1][y] = 0
    sub_matrixs.append(num)
  # 往左移动
  if y != 0:
    num = np.copy(matrix)
    num[x][y] = num[x][y-1]
    num[x][y-1] = 0
    sub_matrixs.append(num)
  # 往右移动
  if y != 2:
    num = np.copy(matrix)
    num[x][y] = num[x][y+1]
    num[x][y+1] = 0
    sub_matrixs.append(num)
  return sub_matrixs

# A*算法
def Astar(start_matrix,end_matrix):
  CLOSED = []     # 记录已扩展的结点
  OPEN = []       # 记录已得到但还未被扩展的结点
  OPEN.append(Node(start_matrix,0,[]))

  while OPEN:
    # 对OPEN表升序排序
    OPEN.sort(key=lambda x:x.value + x.cost)
    # 取出OPEN表中目标函数值最小的结点
    curnode = OPEN.pop(0)
    # 如果是目标状态，则返回目标路径
    if np.array_equal(curnode.matrix,end_matrix):
      curnode.path.append(Node(end_matrix,0,[]))
      return curnode.path
    # 扩展当前结点
    sub_matrixs = swap_zero(curnode.matrix)
    # 遍历子结点
    for sub_matrix in sub_matrixs:
      # 是否在CLOSED表
      found_in_closed = False
      for closed_matrix in CLOSED:
        if np.array_equal(sub_matrix, closed_matrix):
          found_in_closed = True
          break
      # 如果在CLOSED表，则无需操作
      if found_in_closed:
        continue

      # 是否在OPEN表
      found_in_open = False
      for item in OPEN:
        if np.array_equal(item.matrix, sub_matrix):
          found_in_open = True
          # 找到之后，需要对目标函数值进行判断更新
          if  curnode.cost + 1 < item.cost: 
            item.cost = curnode.cost + 1
            item.path = curnode.path + [curnode]
            break
      # 如果不在OPEN表，代表是新结点，则直接加入OPEN表
      if not found_in_open:
        newpath = curnode.path + [curnode]
        # 代价就是当前路径长度+1
        newnode = Node(sub_matrix,curnode.cost + 1,newpath)
        OPEN.append(newnode)
    CLOSED.append(curnode.matrix)   # 将该结点加入CLOSED表
        
def Print(matrix):
  for row in matrix:
    print(row)
  print()
    
start_matrix = np.array([[2, 8, 3], [1, 6, 4], [7, 0, 5]])
end_matrix = np.array([[1, 2, 3], [8, 0, 4], [7, 6, 5]])
path = Astar(start_matrix,end_matrix)
for node in path:
    Print(node.matrix)
```

![](https://i-blog.csdnimg.cn/blog_migrate/35a3b832a22222916a72dcc9dbfcc3d3.png)