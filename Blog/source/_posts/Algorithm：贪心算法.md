---
title: 贪心算法
tags:
  - Algorithm
categories:
  - 算法
cover: /image/algorithm.png
abbrlink: a4ce31d2
date: 2024-11-02 21:59:17
description:
---
<meta name="referrer" content="no-referrer"/>

## 1. 基本原理

贪心（Greedy）：在每一步选择中，都选择当前状态下最优的选择，以希望通过一系列的局部最优的选择达到全局最优的结果

基本步骤：
1. 建立数学模型来描述问题，然后将问题分成若干个子问题
2. 对每一个子问题求局部最优解
3. 将子问题的局部最优解合并为原问题的最优解

三种方法的比较
|特性|分治策略|动态规划|贪心算法|
|-|-|-|-|
|子问题处理|独立解决|保存结果|求局部最优解|
|时间复杂度|通常较高，依赖于分解的层数|通常是O(n^2)或O(n log n)|通常是O(n)或O(log n)|
|空间复杂度|不存储中间结果，递归合并子问题的解|需要存储dp数组|不存储中间结果，直接使用局部最优解|
|方向|自顶向下|自底向上|自顶向下|

{% note success flat %}
可以发现，无论是分治策略还是动态规划还是贪心算法，他们都是将原问题分成多个子问题，再利用子问题的解求解原问题
差别在于，**分治策略不会修剪子问题递归树，而贪心算法和动态规划都会根据问题的性质和结构对子问题递归树进行修剪**
其实，**动态规划可以看作是分治策略的一种特殊情况，而贪心算法是动态规划的一种特殊情况**
{% endnote %}

贪心算法的必要条件：
- **无后效性：已经做出的决策或选择不会影响未来决策的有效性和可行性**，也就是说，一旦做出选择，就不能改变，并且该选择对后续决策不会造成负面影响
- **最优子结构：当前问题的最优解包含其子问题的最优解**

## 2. 经典问题

> 贪心算法的核心就是理解为什么局部最优解是全局最优解！

### 2.1 活动选择问题

问题描述：有n个需要在同一天使用同一个教室的活动，教室同一时刻只能由一个活动使用，给定每个活动的名字、起始时间start和结束时间end，问怎样安排活动能够使当天举行的活动的数量最多

贪心：总是选择最早结束的活动，因为这样就能够使得剩下的时间最多，剩下的时间越多，理论上能举行的活动自然就越多

{% note warning flat %}
如果我们总是选择最早开始的，那么很有可能持续很长时间
如果我们总是选择最短持续的，那么可能会有很多时间碎片无法利用
{% endnote %}

代码
```python
def select_activities(activities, n):
    activities = sorted(activities, key=lambda x: x[2])
    result = []
    end = -1
    i = 0
    while i != n:
        begin = activities[i][1]
        if begin >= end:
            result.append(activities[i][0])
            end = activities[i][2]
            print(f"choose activity {activities[i][0]} which begins at {activities[i][1]} and ends at {activities[i][2]}")
        i += 1
    return result
```

### 2.2 分数背包问题

问题描述：有n个物品，每个物品对应的价值为v，每个物品对应的重量为w，背包容量是c，可以选择任意部分物品放入背包，即不需要将整个物品装入背包，求不超过背包容量的前提下能拿的物品的最大总价值

贪心：总是选择拿均重价值最高的物品，相当于每单位背包容量都要放当前最大价值的物品

{% note warning flat %}
0/1背包不能用贪心算法，因为每选取一个物品，都会影响背包的剩余容量，而当前最大价值的物品很有可能重量很大
{% endnote %}

代码
```python
def partial_knapsack(items, capacity, n):
    # items(名称，价值，重量)，计算得到性价比(名称，性价比，重量)
    v_per_w = [[0, 0, 0] for _ in range(n)]
    for i in range(n):
        v_per_w[i][0] = items[i][0]
        v_per_w[i][1] = float(items[i][1] / items[i][2])
        v_per_w[i][2] = items[i][2]
    # 按照性价比降序排序
    v_per_w.sort(key=lambda x: x[1], reverse=True)
    total = 0
    # 一直拿整份性价比最高的，直到背包容量不够只能拿部分
    for i in range(n):
        if v_per_w[i][2] <= capacity:
            value = v_per_w[i][1] * v_per_w[i][2]
            total += value
            capacity -= v_per_w[i][2]
            print(f"Take full {v_per_w[i][0]}: weight = {v_per_w[i][2]}, value per weight = {v_per_w[i][1]:.2f}, value = {value}")
        else:
            value = v_per_w[i][1] * capacity
            total += value
            print(f"Take partial {v_per_w[i][0]}: weight = {capacity}, value per weight = {v_per_w[i][1]:.2f}, value = {value}")
            break
    print(f"Total value in knapsack: {total:.2f}")
	return total
```

### 2.3 钱币支付问题

问题描述：假设有1，2，5，10，20，50，100元的纸币，要支付价格为price元的物品，至少要用到什么纸币？

贪心：总是选择小于等于price的最大纸币

代码
```python
def cash(value, price):
    result = {}
    index = len(value) - 1
    while price != 0:
        if value[index] <= price:
            if value[index] not in result:
                result[value[index]]  = 1
            else:
                result[value[index]] += 1
            price -= value[index]
        else:
            index -= 1
    for denomination, count in result.items():
        print(f"需要{count}张面值为{denomination}的纸币")

value = [1, 2, 5, 10, 20, 50, 100]
price = 3564
cash(value, price)
```

### 2.4 小船过河问题

问题描述：有n个人，只有一艘船，船只能坐两人，每个人都有一个对应的划船速度，船的速度取决于船中两人较慢的人的划船速度，一开始n个人和船都在岸a，问将这n个人运到岸b，最少需要多久？（注意船划过去还要划回来，一来一回可以是不同的人）

贪心：实际上一个来回只能送一个人到对岸，假设一轮为两个来回，以下两个选择之一是最优选择，它们都在一轮中将当前的最慢和次慢送到岸b，并且保证剩下所有人都在岸a，因此具有最优子结构（假设按照划船时间从大到小排序）
- 选择一：次快-最快-最慢-次快，即t[-1]+2*t[-2]+t[0]
  - 第一个来回：过去选择最快的两个人，回来选择最快的人
  - 第二个来回：过去选择最慢的两个人，回来选择次快的人
- 选择二：最慢-最快-次慢-最快，即2*t[-1]+t[0]+t[1]
  - 第一个来回：过去选择最快和最慢的人，回来选择最快的人
  - 第二个来回：过去选择最快和次慢的人，回来选择最快的人

{% note warning flat %}
重点在于如何节省回来的时间，要尽可能让快的人驾船回来，也就对应着两种方法：一是让快的人即负责过去也负责回来，二是提前送一个快的人到对岸为下一次回来做准备
注意如果岸a只有三个人属于特殊情况需要单独处理！同时如果岸a只有两个人过去就不需要再回来了！
{% endnote %}

代码
```python
def cross_river(speed, n):
    # 倒序排列，因为时间越短的代表速度越快
    speed.sort(reverse=True)
    # 输出排序后的信息
    for i in range(n):
        print(f"{i}'s speed is {speed[i]}")
    # 记录总时间
    time = 0
    # 记录位于岸a的最慢的人的索引
    index = 0
    while index != n:
        if index == n - 2:
            time += speed[index]
            print(f"GO: {n-1} and {n-2}, COST: {speed[-2]}")
            print(f"END! TOTAL COST: {time}")
            index += 2
        elif index == n - 3:
            time += speed[index] + speed[index+1] + speed[-1]
            print(f"GO: {n-1} and {index}, COST: {speed[index]}")
            print(f"BACK: {n-1}, COST: {speed[-1]}")
            print(f"GO: {n-1} and {index+1}, COST:{speed[index+1]}")
            print(f"END! TOTAL COST: {time}")
            index += 3
        else:
            time1 = 2 * speed[-2] + speed[-1] + speed[index]
            time2 = 2 * speed[-1] + speed[index] + speed[index+1]
            if time1 > time2:
                time += time2
                print(f"GO: {n-1} and {index}, COST: {speed[index]}")
                print(f"BACK: {n-1}, COST: {speed[-1]}")
                print(f"GO: {n-1} and {index+1}, COST: {speed[index+1]}")
                print(f"BACK: {n-1}, COST: {speed[-1]}")
            else:
                time += time1
                print(f"GO: {n-1} and {n-2}, COST: {speed[-2]}")
                print(f"BACK: {n-1}, COST: {speed[-1]}")
                print(f"GO: {index} and {index+1}, COST: {speed[index]}")
                print(f"BACK: {n-2}, COST: {speed[-2]}")
            index += 2
    return time

speed = [1,2,2,10]
cross_river(speed, len(speed))
```

### 2.5 区间覆盖问题

问题描述

贪心：

代码：

### 2.6 赫夫曼编码

问题描述

贪心：

代码：