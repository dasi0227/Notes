---
title: 查询优化
tags:
  - MySQL
categories:
  - 笔记
cover: /image/database.png
description: 查询计划，等价转换规则、目录统计信息
abbrlink: 7e1296ef
date: 2024-12-18 11:29:40
---
<meta name="referrer" content="no-referrer"/>

## 1. 查询计划

考虑以下两个表达式树，他们代表的表达式等价，即结果一样，但右边的代价是更小，这是因为$\sigma_{dept\_name=Music}$的位置不同
- 左边：先连接，再选择，这会造成大量的无用连接
- 右边：先选择，再连接，提前过滤掉全部不满足$\sigma_{dept_name=Music}$的元组

![](https://dasi-blog.oss-cn-guangzhou.aliyuncs.com/DataBase/chapter15-19/202412251201665.png)

查询计划功能
- 决定了查询表达式中每个操作**应该使用什么算法**
- 指定这些操作**应该以什么顺序执行**

查询计划评估因素
- 统计信息：元组数量，属性值数量，分布情况
- 中间结果：中间结果对后续操作成本的影响
- 算法成本：连接、排序、选择等操作所使用算法的代价

查询计划优化器：产生一个能计算出与给定初始表达式相同的结果的查询计划，并且能以最小或接近最小的代价来执行
1. 产生逻辑上与给定表达式等价的表达式
2. 以可替代的方式对所产生的表达式做注释，以产生备选的查询计划
3. 估计每个执行计划的代价，选择估计代价最小的一个

MySQL查看查询计划：`explain <query>`
- id：查询的标识符，区分不同子查询和主查询
- select_type：查询类型
  - SIMPLE：普通查询（没有子查询）
  - PRIMARY：主查询
  - SUBQUERY：子查询
- table：查询的表
- type：连接类型
  - ALL：全表扫描
  - index：索引扫描
  - range：范围扫描
  - ref：非唯一索引扫描
  - const：常量匹配
  - NULL：不需要访问表
- possible_keys：可能使用到的索引
- key：实际使用到的索引
- key_len：用于查询的索引长度
- rows：预估扫描的行数
- Extra：额外信息
  - Using where：查询是否包含 WHERE 过滤
  - Using filesort：查询是否需要排序
  - Using index：查询是否使用了索引

## 2. 逻辑优化

### 2.1 等价转换规则

1. **合取选择运算可分解为单个选择运算的级联**：$\sigma_{\theta 1 \land \theta 2}(E) = \sigma_{\theta 1}(\sigma_{\theta 2}(E))$

2. **选择运算满足交换律**：$\sigma_{\theta 1}(\sigma_{\theta 2}(E)) = \sigma_{\theta 2}(\sigma_{\theta 1}(E))$

3. **投影运算的级联等于最外层的投影运算**：$\Pi_{L1}(\Pi_{L2}(...(\Pi_{Ln}(E))...)) = \Pi_{L1}(E)$

4. **选择运算+笛卡尔积 = 连接运算**：$\sigma_{\theta}(E1 \times E2) = E1 \bowtie_{\theta} E2$

5. **连接运算满足交换律**：$E1 \bowtie_{\theta} E2 = E2 \bowtie_{\theta} E1$

6. **当$\theta2$不涉及E1属性时，选择运算对$\theta$连接运算满足结合律**：$（E1 \bowtie_{\theta_1} E2） \bowtie_{\theta_2} E3 = E1 \bowtie_{\theta_1} (E2 \bowtie_{\theta_2} E3)$

7. **当$\theta1$只涉及E1的属性时，选择运算对$\theta$连接运算满足分配律**：$\sigma_{\theta_1}(E1 \bowtie_{\theta} E2) = (\sigma_{\theta_1}(E1)) \bowtie_{\theta} E2$

8. **当$\theta$只涉及投影属性时，投影运算对$\theta$连接运算满足分配律**：$\Pi_L(E1 \bowtie_{\theta} E2) = \Pi_L(\Pi_{L1}(E1) \bowtie_{\theta} \Pi_{L2}(E2))$

9. **选择运算对集合的并、交、差满足分配律**：
$$
\sigma_{\theta}(E1 \cup E2) = \sigma_{\theta}(E1) \cup \sigma_{\theta}(E2)\\
\sigma_{\theta}(E1 \cap E2) = \sigma_{\theta}(E1) \cap \sigma_{\theta}(E2)\\
\sigma_{\theta}(E1 - E2) = \sigma_{\theta}(E1) - \sigma_{\theta}(E2)
$$

10. **投影运算对并运算满足分配律**：$\Pi_L(E1 \cup E2) = \Pi_L(E1) \cup \Pi_L(E2)$

### 2.2 示例

对于以下表达式
$$
\Pi_{name, title}(\sigma_{deptname='Music' \land year=2017}(instructor \bowtie (teaches \bowtie \Pi_{courseid, title}(course))))
$$

根据自然连接的交换律得到
$$
\Pi_{name, title}(\sigma_{deptname='Music' \land year=2017}((instructor \bowtie teaches) \bowtie \Pi_{courseid, title}(course)))
$$

根据选择运算对连接运算的分配律得到
$$
\Pi_{name, title}((\sigma_{deptname='Music' \land year=2017}(instructor \bowtie teaches)) \bowtie \Pi_{courseid, title}(course))
$$

根据选择运算对连接运算的分配律得到
$$
\Pi_{name, title}((\sigma_{deptname='Music'}(instructor) \bowtie \sigma_{\land year=2017}(teaches)) \bowtie \Pi_{courseid, title}(course))
$$

![](https://dasi-blog.oss-cn-guangzhou.aliyuncs.com/DataBase/chapter15-19/202412251201633.png)

### 2.3 枚举

生成所有可能的等价表达式需要重复地对每个子表达式应用等价转换规则，计算量呈指数级增长，同时需要存储所有生成的等价表达式，可能导致内存使用量过大
- 只根据代价模型选择最有潜力的等价转换规则来应用
- 检测和消除重复的子表达式，利用指针指向相同的子表达式实现共享
- 利用动态规划算法来确定最优连接次序

![](https://dasi-blog.oss-cn-guangzhou.aliyuncs.com/DataBase/chapter15-19/202412251201635.png)

### 2.4 常见技术

1. 选择操作下推：将选择操作尽可能下推到查询计划的底层，减少中间结果的大小
2. 投影操作下推：尽早过滤掉不需要的列，减少数据传输量
3. 连接顺序优化：调整连接操作的顺序，减少中间结果的大小。
4. 消除冗余操作：删除查询计划中不必要或者冗余的操作

## 3. 统计信息

统计信息存储在系统目录中，是代价估算的基础
- 关系r的元组总数：$n_r$
- 关系r的块总数：$b_r$
- 关系r的一个元组的字节数：$l_r$
- 关系r的元组存储密度：$f_r = \lfloor \frac{n_r}{b_r} \rfloor$
- 关系r的属性A的非重复值数量：$V(A, r)$
- 属性值的分布情况：直方图

![](https://dasi-blog.oss-cn-guangzhou.aliyuncs.com/DataBase/chapter15-19/202412251201636.png)