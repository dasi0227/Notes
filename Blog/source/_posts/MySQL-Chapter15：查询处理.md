---
title: 查询处理
tags:
  - MySQL
categories:
  - 笔记
cover: /image/database.png
description: 查询处理的流程，选择、连接和排序的查询原语分析，物化和流水线两种执行模式
abbrlink: 2e9d5c8b
date: 2024-12-08 14:56:03
---
<meta name="referrer" content="no-referrer"/>

## 1. 查询处理

处理流程
1. 查询分析：检查查询语句的拼写、语法、权限、安全性等
2. 查询翻译：将查询语句转换为内部的表示形式，通常是**关系代数表达式**
3. 查询优化：构造具有最小查询执行代价的查询执行计划（原语操作序列）
4. 查询执行：代码生成器接受优化器的查询执行计划并生成内部执行代码，然后由执行引擎执行代码并返回结果

![](https://dasi-blog.oss-cn-guangzhou.aliyuncs.com/DataBase/chapter14/202412091542494.png)

查询原语：数据库引擎用来执行查询操作的基本运算步骤
- **选择（selection）**：根据选择条件筛选元组
- **连接（join）**：根据连接条件合并两个元组
- **排序（sort）**：根据排序键排序元组
- **投影（projection）**：根据投影条件筛选属性

![](https://dasi-blog.oss-cn-guangzhou.aliyuncs.com/DataBase/chapter14/202412091542488.png)

## 2. 查询代价

影响因素
- **磁盘访问**：读取或写入数据时进行磁盘 I/O 操作
- **CPU资源**：查询进程是否需要排队来等待调度
- **网络通信**：对于分布式数据库系统，数据分布在不同的网络节点上，需要考虑网络延迟

代价度量
- **响应时间**：查询从发起到返回结果所经历的时间
- **资源消耗总量**：执行查询时消耗的资源总量

{% note warning flat %}
优化器通常努力去将查询计划的资源消耗总量降到最低，而不是努力将响应时间降到最低，这是因为**准确的响应时间依赖于缓存和磁盘的物理布局，而数据库无法预先知道这些信息，也就无法预估响应时间**
{% endnote %}

**查询代价 = 传输次数 x 平均传输时间 + 寻道次数 x 平均寻道时间**
- 假设平均传输时间和平均寻道时间**固定不变**，因此只需要计算传输次数和寻道次数
- **如果两个块是相邻的，可以认为寻道时间为0**
- 基于**最坏打算**：初始缓冲区为空，且不利用缓冲区

## 3. 选择运算

假设数据库的总块数为b，索引树的高度为h，满足等值条件的块数为n

|算法|传输次数|寻道次数|分析|
|-|-|-|-|
|线性搜索，码上等值|最好1，最坏b，平均b/2|1|只需要寻道初始块，然后顺序读取全部块，只要发现等值即可停止扫描|
|线性搜索，非码上等值|b|1|只需要寻道初始块，然后顺序读取接下来的全部块|
|B+树聚集索引，码上等值|h+1|h+1|每一层索引块和最后的等值数据块需要一次寻道和一次传输|
|B+树聚集索引，非码上等值|h+n|h+1|聚集索引确保数据块之间的连续性，因此在索引的基础上，寻道1次，传输n次|
|B+树辅助索引，码上等值|h+1|h+1|每一层索引块和最后的等值数据块需要一次寻道和一次传输|
|B+树辅助索引，非码上等值|h+n|h+n|辅助索引需要对每个数据块都进行一次寻道|

合取/析取：假设数据库的总块数为b，码x和码y的索引树的高度为h1和h2，满足等值条件的块数为n1和n2（假设都是聚集索引）
|算法|传输次数|寻道次数|
|-|-|-|
|x索引，y线性|h1+1+b|h+2|
|分别索引|h1+h2+n1+n2|h1+h2+2|
|组合索引|h+1|h+1|

{% note warning flat %}
索引搜索相较于线性搜索，**虽然可以减少了传输次数，但是增加了寻道次数**，所以索引搜索更适合大规模数据（传输作为瓶颈），线性搜索更适合小规模数据（寻道作为瓶颈）
{% endnote %}

## 4. 排序运算

假设一共有 B 个数据块，可用 M 个内存块
1. 内排序
   1. 从磁盘中读取 M 个数据块到内存中
   2. 在内存中对这 M 个数据块进行内排序
   3. 将排序后的 M 个数据块作为 1 个归并段写回磁盘
   4. 重复上述过程，直到所有数据块被处理完毕，一共生成生成$\lceil B/M \rceil$个归并段
2. 外排序
   1. 为每个归并段分配 n 个内存块作为输入缓冲，同时必须保留 1 个内存块作为输出缓冲
   2. 对输入缓冲中的内存块进行外排序，将结果放入输出缓冲的内存块中
   3. 当输出缓冲的内存块满时，将该内存块写入磁盘作为新归并段的一部分
   4. 当输入缓冲的某个内存块空时，从对应的归并段中读取下一个数据块到输入缓冲
   5. 重复上述过程，直到所有小的归并段都处理完成，一次外排序可以处理$\lfloor M/n \rfloor - 1$个归并段
3. 重复第 2 步，直到得到最后唯一的全局有序的归并段，一共进行了$log_{\lfloor M/n \rfloor - 1}(\lceil B/M \rceil)$趟归并

![](https://dasi-blog.oss-cn-guangzhou.aliyuncs.com/DataBase/chapter14/202412091542489.png)

传输次数：$2B + 2B * log_{\lfloor M/n \rfloor - 1}(\lceil B/M \rceil)$
- $2B$：内排序需要读取和写回全部数据块
- $2B * log_{\lfloor M/n \rfloor - 1}(\lceil B/M \rceil)$：外排序每趟都需要读取和写回全部数据块

寻道次数：$2\lceil B / M \rceil + 2\lceil B / M \rceil * log_{\lfloor M/n \rfloor - 1}(\lceil B/M \rceil) - \lceil B / M \rceil$
- $2\lceil B / M \rceil$：每次创造一个归并段，都需要寻道起始块的位置和寻道归并段的位置
- $2\lceil B / M \rceil * log_{\lfloor M/n \rfloor - 1}(\lceil B/M \rceil)$：每次创造一个更大的归并段，都需要寻道起始归并段的位置和寻道更大归并段的位置
- $-\lceil B / M \rceil$：注意最后一次外排序不需要写回，所以寻道次数变少了

## 5. 连接运算

{% note info flat %}
以下讨论的连接都是$r \bowtie_\theta s$，其中$b_x$表示关系x的块数，$n_x$表示关系x的元组数
{% endnote %}

### 5.1 元组嵌套循环连接

**对于外关系中的每一元组，遍历内关系中的所有元组，检查是否满足连接条件**
- 传输次数 = $b_r + n_r * b_s$：外关系的每一行都需要传输内关系的全部块
- 寻道次数 = $b_r + n_r$：外关系的每一行都需要寻道内关系的起始块，从内关系回到外关系也需要寻道一次

```
for each tuple_r in r:
  for each tuple_s in s:
    if join_condition(tuple_r, tuple_s):
      add (tuple_r, tuple_s) to result
```

### 5.2 块嵌套循环连接

**对于外关系中的每一块，遍历内关系中的所有块，检查是否满足连接条件**
- 传输次数 = $b_r + b_r * b_s$：外关系的每一块都需要传输内关系的全部块
- 寻道次数 = $2 * b_r$：从外关系进入内关系寻道一次，从内关系返回外关系寻道一次

```
for each block_r of r:
  for each block_s of s:
    for each tuple_r in block_r:
      for each tuple_s in block_s:
        if join_condition(tuple_r, tuple_s):
          add (tuple_r, tuple_s) to result
```

{% note warning flat %}
如果分配了M个数据块作为输出缓冲区，那么只有输出缓冲区满了才需要寻道写回
- 传输次数 = $b_r + \lceil b_r/(M) \rceil * b_s$
- 寻道次数 = $2 * \lceil b_r/(M) \rceil$

{% endnote %}

### 5.3 索引嵌套循环连接

**对于外关系的每个元组，利用索引直接选择内关系满足条件的行**
- 传输次数 = $b_r + n_r * cost_{index}$
- 寻道次数 = $n_r * cost_{index}$

```
for each tuple_r in r:
  use index_s on tuple_s where join_condition:
    add (tuple_r, tuple_s) to result
```

### 5.4 归并排序连接

**先对两个表进行内排序，然后在外排序的时候，只需要找到匹配的行，不需要进行实际的归并操作**

- 传输次数 = $3(b_r+b_s)$
  - 内排序阶段 = $2(b_r+b_s)$：读入和写回各需一次
  - 外排序阶段 = $b_r+b_s$：只需要读入
- 寻道次数 = $2(\lceil b_r/M \rceil + \lceil b_s / M \rceil) + \lceil b_r / b_b \rceil + \lceil b_s / b_b \rceil$
  - 内排序阶段 = $2(\lceil b_r/M \rceil + \lceil b_s / M \rceil)$
  - 外排序阶段 = $\lceil b_r / b_b \rceil + \lceil b_s / b_b \rceil$

```
runs_r = internel_sort(r)
runs_s = internel_sort(s)
for tuple_r, tuple_s in runs_r, runs_s:
  if join_condition(tuple_r, tuple_s):
    add (tuple_r, tuple_s) to result
```

{% note warning flat %}
$M$是内存中可以容纳的块数，$b_b$是每个归并段分配的输入缓冲块数
{% endnote %}


### 5.5 哈希连接

**构建阶段利用第一个哈希函数，将两个关系按照连接键的值划分到多个分区中；探测阶段利用第二个哈希函数，对相同分区的元组进行精确匹配**
- 传输次数 = $3(b_r+b_s)$
  - 构建阶段 = $2(b_r+b_s)$：每次读取或写入一个块需要一次传输
  - 探测阶段 = $b_r+b_s$：只有读取需要一次传输，不需要写入
- 寻道次数 = $2(\lceil b_r / M \rceil + \lceil b_s / M \rceil) + \lceil b_r / b_b \rceil + \lceil b_s / b_b \rceil$
  - 构建阶段 = $2(\lceil b_r / M \rceil + \lceil b_s / M \rceil)$：每次读取或写入一个块需要一次寻道
  - 构建阶段 = $\lceil b_r / b_b \rceil + \lceil b_s / b_b \rceil$：每次读取一个分区需要一次寻道

```
R = hash1(r)
S = hash1(s)
for area_r, area_s in R, S:
    for tuple_r in area_r:
      key_r = hash2(tuple_r)
      for tuple_s in area_s:
        key_s = hash2(tuple_s)
          if key_r == key_s:
            add (tuple_r, tuple_s) to result
```

{% note warning flat %}
$M$是内存中可以容纳的块数，$b_b$是每个分区分配的输入缓冲块数
{% endnote %}


![](https://dasi-blog.oss-cn-guangzhou.aliyuncs.com/DataBase/chapter14/202412091542492.png)

## 6. 执行模式

执行模式：如何处理包含多个运算的表达式

|特性|物化|流水线|
|-|-|-|
|定义|得到整个中间结果集后，存储磁盘中，后续的查询步骤从磁盘中获取数据|指每一步的计算结果直接传递给下一步进行处理|
|局限性|必须等待前一个操作完全执行完毕并物化结果；引入了将中间结果写回磁盘和从磁盘读取中间结果的时延|如果某个操作依赖于前一个操作的完整结果（聚合、排序），则流水线失效|
|适用场景|中间结果较小，且需要反复利用|操作可以并行处理，且中间结果是一次性使用的|

![](https://dasi-blog.oss-cn-guangzhou.aliyuncs.com/DataBase/chapter14/202412091542493.png)

驱动方式
- 需求驱动模式 (Demand-Driven) / 拉模式（Pull）/ 按需模式（Lazy）：每当上游操作需要数据时，下游操作才生成数据
- 生产驱动模式 (Producer-Driven) / 推模式（Push） / 驱动模式（Eager）：下游操作不断执行，主动将数据传递给上游