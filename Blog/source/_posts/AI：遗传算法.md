---
title: 遗传算法
tags:
  - AI
categories:
  - 笔记
description: 介绍了遗传算法的核心要素、基本操作和算法流程，其中包括选择策略，交叉重组策略和变异策略，分析了影响性能的因素和遗传算法的性质，最后用遗传算法解决八皇后问题
cover: image/ai.png
abbrlink: 9cfaa3ca
date: 2024-07-01 09:55:43
---
<meta name="referrer" content="no-referrer"/>

## 1. 核心思想

- 个体（individual）：候选解
- 种群（population）：候选解的集合，表示问题的解空间
- 染色体（chromosome）：候选解的编码方式，表示个体的特征，是一种象征着基因的数据结构
- 精英（elite）：适应度最好的个体
- 适应度（fitness）：目标函数值
- 环境容纳量（capacity）：种群的最大个体数量
- 优化准则（optimization）：指导算法何时停止搜索（迭代次数）
- 自然选择（selection）：根据个体的适应度选择优秀个体作为父代，用于产生子代形成新的个体
- 交叉重组（crossover）：提取两个父体的染色体片段进行交换组合，从而生成新的染色体来形成子代个体
- 基因变异（mutation）：对个体染色体中的某些基因进行随机改变或替换来实现
  
## 2. 基本操作

### 2.1 选择策略

- 轮盘赌选择（Roulette Wheel）：轮盘的每个扇区代表不同的个体，每个扇区的张角与个体的适应度成比例，然后产生一个随机数，落入哪个扇区就选择相应的个体
- 锦标赛选择（Tournament）：根据设定的参赛人员数量随机选取种群中若干个个体，选择其中适应度最大的个体
- 最佳个体选择（elitist）：把群体中适应度最高的个体不进行交叉而直接复制到下一代

### 2.2 交叉重组策略

- 单点交叉（Single-Point Crossover）：随机设定一个交叉点，该点前/后的部分基因结构进行互换，以此生成两个新的个体
- 均匀交叉（Uniform Crossover）：按照50%的概率对父代每一个基因位点进行交换，从而产生新的子代个体
- 部分匹配交叉（Partial-mapped Crossover,PMX）：具体操作可见七的代码

![](https://i-blog.csdnimg.cn/blog_migrate/c9cae2c69c116ef9b3fd22b239efb8bf.png)

> PMX具体操作：https://blog.csdn.net/qq_32182397/article/details/106031512

### 2.3 变异策略（随机，随机，还是随机）

- 位点变异（Bit-flip）：随机选择一个或多个基因位点，并以一定的变异概率改变这些基因位点上的基因值
- 逆转变异（Inversion）：随机选择两个基因位点，然后将这两个基因位点之间的基因逆序排列
- 插入变异（Insertion）：随机选择一个基因位点插入到另一个随机选择的位置中
- 互换变异（Swap）：随机选取两个基因位点进行互换
- 移动变异（Shift）：随机选取一个基因位点向左或向右移动一个随机位数

## 3. 算法流程

1. 初始化：初始种群和最大迭代次数
2. 迭代：是否到达最大迭代次数，当前种群中是否有个体是最优解
  1. 根据选择策略，选出两个具有优秀基因的个体
  2. 将上一步选择的两个个体交叉重组，获得两个新个体加入种群
  3. 如果达到环境容纳量，则淘汰原种群中两个具有劣质基因的个体
  4. 按照变异概率随机对种群中每个个体基因突变
3. 输出最优解

![](https://i-blog.csdnimg.cn/blog_migrate/47dd2ccb8b901beccaef8ce2f97cd1c0.png)

## 4. 影响性能的因素

### 4.1 最大迭代次数

其他因素不变的情况下，最大迭代次数越多，结果的适应度越好，平均GA时间越长。

### 4.2 最大种群数量

其他因素不变的情况下，最大种群数量越多，结果的适应度先上升后下降。这是因为我们此时在锦标赛选择策略种设置的“参赛人员数量”相对于最大种群数量偏小，所以最后选择出来的优秀亲本的实际上可能不优秀，因此每次遗传得到的子代也不够好
因此我们我们应该根据最大种群数量来确定竞标赛选择的参赛人员数量，可以设置参赛人员数量是最大种群数量的80%

### 4.3 初始变异概率

其他因素不变的情况下，初始变异概率从小到大，结果的适应度先是很低，然后上升，最后下降。这是因为如果变异概率太大，可能会导致种群里的精英也发生了变异，而精英是最接近最优解的，不应该发生变异；如果变异概率太低，会导致缺乏多样性、解空间覆盖不足、演化速度变慢等问题

### 5. 评测

### 5.1 特点

- 没有太多的数学要求：直接对数据结构对象（数串）操作
- 利用大量随机技术进行搜索：提升找到全局最优解的概率
- 并行化：对种群中每一个个体的操作是相同的，可以同时进行
- 评估简单： 仅用适应度函数值来评估个体

### 5.2 性质

- 良好的鲁棒性：遗传算法对问题的参数设置和初始种群的选择相对不敏感
- 良好的收敛性：随着算法的迭代，种群的平均适应度也逐渐增加，直至达到一定的稳定状态
- 完备性：理论上遗传算法是完备的，然而在实践中，由于搜索空间的复杂性和计算资源的限制，不一定能够找到全局最优解，但遗传算法通常能够找到接近全局最优解的局部最优解

## 6. 八皇后问题

问题描述：在一个 8x8 的国际象棋棋盘上，摆放八个皇后，使得任意两个皇后都不能在同一行、同一列或同一斜线上共存

```python
import random

# 获取两个随机点
def random2point(size):
  point1 = random.randint(1, size - 1)
  point2 = random.randint(1, size - 1)
  while point1 == point2:
    point2 = random.randint(1, size - 1)
  return min(point1, point2), max(point1, point2)     # 小的在前，大的在后

# 初始种群生成函数
def initial(amount,size):
  population = []
  while len(population) != amount:        # 一共生成amount个体
      individual = random.sample(range(size),size)
      individual = ''.join([str(item) for item in individual])
      if individual not in population:    # 确保个体不同
          population.append(individual)
  return population

# 适应度函数：计算冲突数
def fitness(individual):
  conflicts = 0
  size = len(individual)
  for i in range(0,size-1):
    for j in range(i+1,size):
      diag1 = (int(individual[i]) - i) == (int(individual[j]) - j)
      diag2 = (int(individual[i]) + i) == (int(individual[j]) + j)
      if individual[i] == individual[j] or diag1 or diag2:
        conflicts += 1
  return conflicts   

# 选择策略：锦标赛，随机选10个个体“竞赛”，选出冲突数最小的个体
def tournament_select(population):
  tournament1 = random.sample(population,10)  
  parent1 = min(tournament1, key=fitness)
  tournament2 = random.sample(population,10)
  if parent1 in tournament2:
    tournament2.remove(parent1)
  parent2 = min(tournament2, key=fitness)
  return parent1,parent2

# 交叉重组策略：PMX
def crossover(parent1,parent2):
  size = len(parent1)
  child1,child2= [None] * size,[None] * size
  mapping1,mapping2= {},{}
  # 选择交叉点
  point1, point2 = random2point(size)
  # 复制交叉段
  child1[point1:point2 + 1] = parent2[point1:point2 + 1]
  child2[point1:point2 + 1] = parent1[point1:point2 + 1]
  # 创建映射字典
  mapping1 = {parent2[i]: parent1[i] for i in range(point1, point2 + 1)}
  mapping2 = {parent1[i]: parent2[i] for i in range(point1, point2 + 1)}
  # 填充子代
  for i in range(size):
    if i < point1 or i > point2:
      element1 = parent1[i]
      while element1 in mapping1:
        element1 = mapping1[element1]
      child1[i] = element1

      element2 = parent2[i]
      while element2 in mapping2:
        element2 = mapping2[element2]
      child2[i] = element2
  return ''.join(child1), ''.join(child2)

# 基因突变策略：逆转变异
def mutation(individual):
  size = len(individual)
  point1, point2 = random2point(size)
  mutate_individual = individual[:point1] + individual[point1:point2+1][::-1] + individual[point2+1:]
  return mutate_individual

#遗传算法
def genetic(population):
  size = len(population)
  max_iteration = 1000
  iteration = 0
  mutation_rate = 0.05    # 变异概率

  while iteration != max_iteration:
    # 按照适应度排序种群
    population = sorted(population,key=fitness)
    # 算法终止：找到最优解
    for item in population:
      if fitness(item) == 0:
        return item
    # 挑选出两个具有优秀基因的个体去交配
    parent1,parent2 = tournament_select(population)
    # 得到两个孩子
    child1,child2 = crossover(parent1,parent2)
    # 替换原有种群具有劣势基因的个体
    population[size-1],population[size-2] = child1,child2
    # 种群每个个体都有可能基因突变
    for i in range(len(population)):
      if random.random() < mutation_rate:
        population[i] = mutation(population[i])
    # 迭代次数+1
    iteration += 1
    return None

population = initial(20,8)
result = genetic(population)
if result != None:
  print('succss:',result)
else:
  print('fail')
```

## 7.TSP旅行商问题

问题描述：假设有一个旅行商需要访问n个城市，并且每对城市之间都有距离或者成本，旅行商需要找到一条最短路径，使得他只访问每个城市一次，并且最终回到出发城市，使得总的访问成本最小。

```python
import os
import random
import math
import time
import matplotlib.pyplot as plt
class GeneticAlgTSP():
  # 初始化种群函数：amount是种群中个体个数，length是个体的染色体长度，且保留精英
  def initial_population(self, amount, length, elite):
    population = []
    # 要求对精英进行一次变异，防止精英占据绝对优势陷入局部最优解
    if elite != []:
      elite = self.mutate(elite)
      population.append(elite)
    while len(population) != amount:
      individual = random.sample(range(length), length)
      # 每个个体的染色体要求不同
      if individual not in population:
        population.append(individual)
    return population

  # 初始化城市坐标函数：filename是读取的tsp格式文件名称
  def initial_cities(self, filename):
    cities = []
    # 得到文件路径
    diskpath = os.path.dirname(__file__)
    filepath = diskpath + '//TSP数据库//'+ filename
    # 读取文件
    with open(filepath, 'r') as file:
      lines = file.readlines()                      # 读取全部行
      for line in lines:
        if line.startswith("EOF"):                  # 如果是END OF FILE则退出循环
          break
        data = line.split()                         # 每行按照空格分开数据
        if len(data) == 3 and data[0].isdigit():    # 需要的只是坐标数据，其他忽略
          x = float(data[1])
          y = float(data[2])
          cities.append((x, y))                     # 将坐标(x, y)加入城市坐标列表
    return cities

  # 初始化类函数：种群列表和城市坐标列表
  def __init__(self, filename, elite):
    self.cities = self.initial_cities(filename)
    self.population = self.initial_population(10, len(self.cities), elite)

  # 随机生成两点函数：限定在size范围内
  def random2point(self, size):
    point1 = random.randint(1, size - 1)
    point2 = random.randint(1, size - 1)
    while point1 == point2:
      point2 = random.randint(1, size - 1)
    return min(point1, point2), max(point1, point2)     # 小的在前大的在后

  # 欧几里得距离函数：根据坐标计算两个城市之间的欧几里得距离
  def euclidean_distance(self, city1, city2):
    x1, y1 = city1
    x2, y2 = city2
    distance = math.sqrt((x2 - x1)**2 + (y2 - y1)**2)
    return distance

  # 适应度函数：计算闭合旅行路径的总长度
  def fitness(self, individual):
    amount = len(individual)
    distance = 0
    for i in range(amount):
      city1 = self.cities[individual[i]]
      city2 = self.cities[individual[(i + 1) % amount]]       # 取模可以确保得到闭合环路
      distance += self.euclidean_distance(city1, city2)
    return int(distance)                                        # 取整

  # 选择策略：锦标赛->随机选8个个体竞赛，选出适应度最好的个体
  def tournament_select(self, population):
    group1 = random.sample(population, 8)
    parent1 = min(group1, key=self.fitness)
    group2 = random.sample(population, 8)
    if parent1 in group2:
      group2.remove(parent1)                 # 确保选择的两个个体不重复
    parent2 = min(group2, key=self.fitness)
    return parent1, parent2

  # 交叉重组策略：部分映射交叉PMX
  def crossover(self, parent1, parent2):
    size = len(parent1)
    child1, child2 = [None] * size, [None] * size
    # 选择交叉点
    point1, point2 = self.random2point(size)
    # 复制交叉段
    child1[point1:point2 + 1] = parent2[point1:point2 + 1]
    child2[point1:point2 + 1] = parent1[point1:point2 + 1]
    # 创建映射字典
    mapping1 = {parent2[i]: parent1[i] for i in range(point1, point2 + 1)}
    mapping2 = {parent1[i]: parent2[i] for i in range(point1, point2 + 1)}
    # 填充非交叉段
    for i in range(size):
      if i < point1 or i > point2:
        element1 = parent1[i]
        while element1 in mapping1:
          element1 = mapping1[element1]
        child1[i] = element1

        element2 = parent2[i]
        while element2 in mapping2:
          element2 = mapping2[element2]
        child2[i] = element2
    return child1, child2

  # 基因突变策略：逆转变异
  def mutate(self, individual):
    size = len(individual)
    point1, point2 = self.random2point(size)
    mutate_individual = individual[:point1] + individual[point1:point2 + 1][::-1] + individual[point2 + 1:]
    return mutate_individual

  # 遗传算法
  def GA(self, max_iterations, max_populations, mutate_rate):
    iteration = 0
    while iteration != max_iterations:
      size = len(self.population)
      # 挑选出两个具有优秀基因的个体去交配
      parent1, parent2 = self.tournament_select(self.population)
      # 得到两个孩子
      child1, child2 = self.crossover(parent1, parent2)
      # 如果数量已经到达环境容纳量，则替换原有种群具有劣势基因的个体，否则直接加入种群
      self.population = sorted(self.population, key=self.fitness)  
      if size == max_populations:
        self.population[size - 1], self.population[size - 2] = child1, child2
      elif size <= 18:
        self.population.append(child1)
        self.population.append(child2)
      # 种群每个个体都有可能基因突变
      self.population = sorted(self.population, key=self.fitness)  
      rate = mutate_rate      # 初始变异概率相同                                         
      for i in range(len(self.population)):
        if random.random() < mutate_rate:
          self.population[i] = self.mutate(self.population[i])
        rate += 0.01        # 适应度值越高，基因越劣质，变异概率越高
      iteration += 1
    self.population = sorted(self.population, key=self.fitness)
    return self.fitness(self.population[0]), self.population[0]

# 可视化路径函数
def plot_path(points, path):
  # 擦除掉原先的图
  plt.cla()
  # 提取点的坐标
  x_values = [point[0] for point in points]
  y_values = [point[1] for point in points]
  # 绘制点
  plt.scatter(x_values, y_values, color='blue', s=15)
  # 绘制路径
  for i in range(len(path) - 1):
    point1 = points[path[i]]
    point2 = points[path[i + 1]]
    plt.plot([point1[0], point2[0]], [point1[1], point2[1]], color='red', linewidth=0.1)
  # 连接最后一个点和第一个点，形成闭合路径
  point1 = points[path[-1]]
  point2 = points[path[0]]
  plt.plot([point1[0], point2[0]], [point1[1], point2[1]], color='red', linewidth=0.1)
  # 设置标题和标签
  plt.title('Visualization of Path')
  plt.xlabel('X')
  plt.ylabel('Y')
  plt.legend(['points', 'path'], loc='upper right')
  # 重新画图
  plt.draw()
  # 控制更新频率
  plt.pause(0.2)

# 进化算法
def EA(filename):
  max_iterations = 10000          # 最大迭代次数
  max_generations = 100           # 最大进化次数
  max_populations = 20            # 最大种群数量
  max_blocktime = 15              # 最大阻塞次数
  mutate_rate = 0.08              # 初始变异概率

  generation = 0
  best_distance = float('inf')
  best_path = []

  blocktime = 0
  while generation != max_generations:
    solve = GeneticAlgTSP(filename, best_path)
    distance, path = solve.GA(max_iterations, max_populations, mutate_rate)
    # 进化的本质:找到比上一代精英还要好的个体
    if distance < best_distance or blocktime == max_blocktime:
      if distance < best_distance:
        best_distance = distance
        best_path = path
      print("第", generation + 1, "次路径长度:", best_distance)
      plot_path(solve.cities, best_path)
      blocktime = 0
      generation += 1
      continue
    blocktime += 1
  return best_distance, best_path


filename = '//' + 'rw1621'+ '.tsp'
best_distance,best_path = EA(filename)
print("最佳路线:",best_path)
print("最短距离",best_distance)
```