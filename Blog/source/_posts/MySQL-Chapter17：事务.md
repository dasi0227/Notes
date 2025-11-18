---
title: 事务
tags:
  - MySQL
categories:
  - 笔记
cover: /image/database.png
abbrlink: 6d75022e
date: 2024-12-18 11:29:52
description: ACID特性、调度、可串行化、隔离性级别
---
<meta name="referrer" content="no-referrer"/>

## 1. ACID

|特性|解释|意义|
|-|-|-|
|原子性（Atomicity）|确保事务是数据库执行的最小单位，即事务的操作要么全部成功反映到数据库中，要么完全不执行回滚到事务开始前的状态|防止事务部分执行导致数据不一致|
|一致性（Consistency）|确保数据库在事务执行前后，数据始终符合完整性约束|保证数据库的合法性|
|隔离性（Isolation）|确保多个事务并发执行时，彼此不互相干扰|防止并发冲突|
|持久性（Durability）|确保事务提交后对数据库的修改是永久的|确保数据可靠性，不会因为故障导致数据丢失|

## 2. 事务状态

|状态|含义|下一刻状态|
|-|-|-|
|活动（Active）|事务正在执行|部分提交、失败|
|部分提交（Partially Commited）|事务完成所有操作，但尚未提交|提交|失败|
|提交（Commited）|事务成功执行并提交，更改已经永久保存|事务周期结束|
|失败（Failed）|事务被中断或事务出错无法继续执行|终止|
|终止（Aborted）|事务回滚，更改被撤销|事务周期结束|

![](https://dasi-blog.oss-cn-guangzhou.aliyuncs.com/DataBase/chapter15-19/202412251201637.png)

## 3. 调度

调度机制：保留每个事务内部的操作顺序的前提下，决定多个事务的全部指令如何顺序执行
- 串行调度：多个事务按照顺序执行，即一个事务的全部指令执行完毕后，另一个事务才开始执行
- 并发调度：可以交替执行来自多个事务的不同指令，同时保证相同事务的指令顺序

为什么要并发调度
1. 提高CPU和磁盘利用率：一个事务常常只使用很少的资源
2. 减少事务的平均响应时间，提升用户体验：防止长事务阻塞短事务的执行
3. 支持多用户环境：确保多个用户的操作可以同时进行且互不干扰

![](https://dasi-blog.oss-cn-guangzhou.aliyuncs.com/DataBase/chapter15-19/202412251201638.png)
![](https://dasi-blog.oss-cn-guangzhou.aliyuncs.com/DataBase/chapter15-19/202412251201639.png)

## 4. 一致性

### 4.1 可串行化

**并发调度的执行结果与某种串行调度的执行结果相同**
- 冲突可串行化：当前调度的冲突操作顺序与某种串行调度的冲突操作顺序一致，即通过交换非冲突操作，可以将并发调度转换为一个串行调度
- 视图可串行化：当前调度的最终结果与某个串行调度的最终结果一致（包含了冲突可串行化）

![](https://dasi-blog.oss-cn-guangzhou.aliyuncs.com/DataBase/chapter15-19/202412251201643.png)

### 4.2 冲突

冲突：来自不同事务，作用于同一数据项，且至少有一个是写操作
- 读-写冲突（Read-Write）：一个事务先读，另一个事务后写
- 写-读冲突（Write-Read）：一个事务先写，另一个事务后读
- 写-写冲突（Write-Write）：一个事务先写，另一个事务后写

{% note warning flat %}
冲突操作只是可能会破坏数据一致性，表明了一种潜在的风险，但并不一定会导致实际的数据不一致
{% endnote %}

冲突等价：两种调度方式中，所有冲突操作的执行顺序相同

优先图：每个节点代表一个事务，如果事务 T1 和事务 T2 存在冲突操作，且 T1 发生在事务 T2 之前，则画一条从 T1 到 T2 的边

![](https://dasi-blog.oss-cn-guangzhou.aliyuncs.com/DataBase/chapter15-19/202412251201641.png)
![](https://dasi-blog.oss-cn-guangzhou.aliyuncs.com/DataBase/chapter15-19/202412251201640.png)

定理：**如果优先图中没有环，则调度是冲突可串行化的**，根据优先图的拓扑排序，可以得出与调度冲突等价的所有串行调度

![](https://dasi-blog.oss-cn-guangzhou.aliyuncs.com/DataBase/chapter15-19/202412251201642.png)

## 5. 隔离性

### 5.1 隔离性级别

- 可串行化（serializable）：最严格，事务完全串行化执行
- 可重复读（repeatable read）：只允许读取已提交数据，同时不允许其他事务更新正在读的数据
- 已提交读（read committed）：只允许读取已提交数据，但可以允许其他事务修改正在读的数据
- 未提交读（read uncommitted）：最宽松，允许读取未提交数据

### 5.2 可恢复

级联回滚（cascading rollback）：一个事务的回滚导致其他依赖它的事务也必须回滚

可恢复（Recoverable）：**一个事务不能依赖于未提交的数据，并先于它提交**，否则无法通过回滚解决。也就是说，对于事务T1和T2，如果T2读取了事务T1之前所写过的数据，则事务T1必须先于T2提交

{% note warning flat %}
一个调度可以是可恢复的，但不是冲突可串行化的
{% endnote %}

![](https://dasi-blog.oss-cn-guangzhou.aliyuncs.com/DataBase/chapter15-19/202412251201645.png)