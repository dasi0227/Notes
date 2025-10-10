# SQL 特殊操作



   * [1. 行列转换](#1-行列转换)
      * [1.1 长格式和宽格式](#11-长格式和宽格式)
      * [1.2 长转宽/行转列（Pivot）](#12-长转宽行转列pivot)
      * [1.3 宽转长/列转行（Unpivot）](#13-宽转长列转行unpivot)
   * [2. 多行/一行转换](#2-多行一行转换)
      * [2.1 多行变一行](#21-多行变一行)
      * [2.2 一行变多行](#22-一行变多行)
   * [3. 计算连续](#3-计算连续)
      * [3.1 连续日期](#31-连续日期)
      * [3.2 连续行为](#32-连续行为)
   * [4. 窗口函数使用](#4-窗口函数使用)
      * [4.1 计算累计指标](#41-计算累计指标)
      * [4.2 计算去除最值后的平均](#42-计算去除最值后的平均)
      * [4.3 计算 Top-N](#43-计算-top-n)
      * [4.4 计算事件相邻](#44-计算事件相邻)
   * [5. 留存率](#5-留存率)



## 1. 行列转换

### 1.1 长格式和宽格式

行列转换是 SQL 中最重要的操作之一，但是开始讲行列转换的 SQL 语句之前，先要好好理解什么是行列转换，行列转换的根本目的是实现数据的“长格式/行”和“宽格式/列”之间的相互转换，作用的表通常具有三种属性，分别是**标识、类别和特征**

长格式：每一行代表一个**观测值**，属性是**标识、类别和特征**，常用于分组、聚合和统计建模

| **person** | **month** | **sales** | **profit** |
| -------- | ------- | ------- | -------- |
| **Alice** | Jan | 1000 | 100 |
| **Alice** | Feb | 1200 | 120 |
| **Alice** | Mar | 1100 | 110 |
| **Bob** | Jan | 900 | 90 |
| **Bob** | Feb | 1000 | 100 |
| **Bob** | Mar | 1100 | 110 |
| **Cally** | Jan | 1200 | 120 |
| **Cally** | Feb | 800 | 80 |
| **Cally** | Mar | 700 | 70 |

> 长格式之所以长是因为将只每一种属性都单独作为一列，而每个观测值都作为一行，即行多

宽格式：每一行代表一个**观测对象**，属性是**标识和类别值**，常用于对比和生成报表

| **person** | **Jan_sales** | **Jan_profit** | **Feb_sales** | **Feb_profit** | **Mar_sales** | **Mar_profit** |
| -------- | ----------- | ------------ | ----------- | ------------ | ----------- | ------------ |
| **Alice** | 1000 | 100 | 1200 | 120 | 1100 | 110 |
| **Bob** | 900 | 90 | 1000 | 100 | 1100 | 110 |
| **Cally** | 1200 | 120 | 800 | 80 | 700 | 70 |

> 宽格式之所以宽是因为将类别值✖️特征都单独作为一列，而每个标识对象有且只有一行，即列多

### 1.2 长转宽/行转列（Pivot）

明确我们要做的事有两件：
- 对于每个类别值✖️特征都需要创建一列 ➡️ `CASE...WHEN...THEN...ELSE...END` + `AS`
- 对于每个标识对象只需要一行 ➡️ `GROUP BY` + `MAX()`

> 注意这里的 MAX 本质不是为了聚合取最大值，因为实际上对应的行只有一个，这里只是为了配合 GROUP BY 的使用，也可以使用 MIN 或 SUM，但是不使用会报错

```sql
SELECT
    -- 每个标识对象对应一行
    person,
    -- 每个类别值✖️特征创建一列
    MAX(CASE WHEN month = 'Jan' THEN sales ELSE 0 END)  AS Jan_sales,
    MAX(CASE WHEN month = 'Jan' THEN profit ELSE 0 END) AS Jan_profit,
    MAX(CASE WHEN month = 'Feb' THEN sales ELSE 0 END)  AS Feb_sales,
    MAX(CASE WHEN month = 'Feb' THEN profit ELSE 0 END) AS Feb_profit,
    MAX(CASE WHEN month = 'Mar' THEN sales ELSE 0 END)  AS Mar_sales,
    MAX(CASE WHEN month = 'Mar' THEN profit ELSE 0 END) AS Mar_profit
FROM data_table
GROUP BY person;
```

### 1.3 宽转长/列转行（Unpivot）

明确我们要做的事有两件：
- 对于每个类别值对应的若干列分解为多行组成的表 ➡️ `AS`
- 将上述得到的表垂直拼接 ➡️ `UNION ALL`

> `UNION ALL` 会保留重复行，而 Unpivot 场景每一行本来就是唯一的，不需要去重，比使用 `UNION` 的性能要好一点

```sql
SELECT person, 'Jan' AS month, Jan_sales AS sales, Jan_profit AS profit FROM data_table
UNION ALL
SELECT person, 'Feb', Feb_sales, Feb_profit FROM data_table
UNION ALL
SELECT person, 'Mar', Mar_sales, Mar_profit FROM data_table;
```



## 2. 多行/一行转换

| **product** | **supplier** |
| - | - |
| **A** | A1 |
| **A** | A2 |
| **B** | A1 |
| **B** | A3 |

| **product** | **suppliers** |
| - | - |
| **A** | A1\ | A2 |
| **B** | A1\ | A3 |

### 2.1 多行变一行

多行到一行的转换不是为了实现聚合得到一个综合的值，而是为了将相同标识的若干个属性值拼接后放在一起，简化表格

我们要做的工作有
- 获取同一标识对象的所有属性值 ➡️ `GROUP BY`
- 将属性值进行拼接而非聚合 ➡️ `GROUP_CONCAT`
- 确定拼接的分割符 ➡️ `SEPARATOR`（默认逗号）

```sql
SELECT
  product,
  GROUP_CONCAT(DISTINCT supplier ORDER BY supplier SEPARATOR '|') AS suppliers
FROM data_table
GROUP BY product;
```

### 2.2 一行变多行

一行到多行到转换不经常使用，而且由于不同标识的 suppliers 的个数不一样且无法确定，常常需要事先明确拆分次数，假定这里每个标识对象都有且只有 3 个不同的属性值

```sql
SELECT product, SUBSTRING_INDEX(SUBSTRING_INDEX(suppliers, ',', 1), ',', -1) AS supplier FROM wide_table
UNION ALL
SELECT product, SUBSTRING_INDEX(SUBSTRING_INDEX(suppliers, ',', 2), ',', -1) FROM wide_table
UNION ALL
SELECT product, SUBSTRING_INDEX(SUBSTRING_INDEX(suppliers, ',', 3), ',', -1) FROM wide_table;
```

> 内层 `SUBSTRING_INDEX(..., ',', n)` 根据分割符获取前 n 个元素，外层 `SUBSTRING_INDEX(..., ',', -1)` 根据分割符获取最后一个元素，综合起来就是获取第 n 个元素



## 3. 计算连续

### 3.1 连续日期

计算日期连续是数据分析业务中很重要的一个操作，常用于分析用户行为与特征

| **user_id** | **active_time** |
| --------- | --------------------- |
| **1** | 2025-03-20 07:12:00 |
| **1** | 2025-03-20 14:45:23 |
| **1** | 2025-03-21 09:30:10 |
| **1** | 2025-03-21 18:05:47 |
| **1** | 2025-03-22 11:22:35 |
| **1** | 2025-03-24 08:15:59 |
| **1** | 2025-03-25 16:40:02 |
| **1** | 2025-03-26 22:00:00 |
| **2** | 2025-03-21 10:05:12 |
| **2** | 2025-03-22 12:47:33 |
| **2** | 2025-03-22 19:20:05 |
| **2** | 2025-03-23 07:55:44 |
| **2** | 2025-03-24 21:33:18 |

仔细想想，计算一共连续的天数，就是计数问题，自然会想到用 `COUNT()` 和 `GROUP BY` 进行聚合，但是 `GROUP BY` 无法处理不同的日期值，`GROUP BY` 无法处理，所以我们需要想一个办法将连续日期变为相同的值。假设有序号和日期：1.02-02，2.02-03，3.02-04，4.02-07 5.02-08
- 日期从 02-02 到 02-02 是 +0，序号从 1 到 1 是 +0，则 02-02 - 1day = 02-01
- 日期从 02-02 到 02-03 是 +1，序号从 1 到 2 是 +1，则 02-03 - 2day = 02-01
- 日期从 02-02 到 02-04 是 +2，序号从 1 到 3 是 +2，则 02-04 - 3day = 02-01
- 日期从 02-02 到 02-07 是 +5，序号从 1 到 4 是 +3，则 02-07 - 4day = 02-03
- 日期从 02-02 到 02-08 是 +6，序号从 1 到 5 是 +4，则 02-08 - 5day = 02-03

可以发现，**连续日期的日期差值和序号差值是一样的，而不连续日期的日期差值和序号差值不一样**，这说明我们只需要用连续日期的**日期 - 序号**得到连续日期的基准，**基准的个数就代表连续日期的天数**

接下来，我们看看处理这类问题的流程是什么
1. 去重得到 active_date，不需要考虑同一天不同时间多次出现，只用关注日期
2. 按照 user_id 进行分组，再根据 active_date 进行从小到大排序
3. 对排序后的结果从 1 开始标上序号
4. 如果若干行的日期连续，那么它们的日期 - 序号的结果是相同的
5. 对相同基准的行进行聚合，计算 count 值
6. 连续天数的终止日期是相同基准的行中的最大日期，而连续天数的起始日期是相同基准的行中的最小日期
7. 如果需要给连续天数设置下限，则使用 `HAVING`；如果需要根据连续天数排序，则使用 `ORDER BY`

现在我们需要了解一下上述流程需要用到的 MySQL 函数/语句
- `ROW_NUMBER()`：窗口函数，用于给结果集标上从 1 开始的连续序号（通常需要配合 ORDER BY 使用）
- `OVER()`：指定聚合/窗口函数的作用范围
- `PARTITION BY`：将数据分组，每个分组内数据独立运行窗口函数
- `DATE_SUB()`：从给定的日期减去指定的时间间隔，返回新的日期
- `INTERVAL`：指定数值的时间单位，用于 `DATE_SUB()` 中

```sql
-- 1. 去重
WITH
active_dates AS (
  SELECT
    user_id,
    DATE(active_time) AS active_date
  FROM data_table
  GROUP BY user_id, DATE(active_time)
),

-- 2. 排序后标号
numbered AS (
  SELECT
    user_id,
    active_date,
    ROW_NUMBER() OVER (PARTITION BY user_id ORDER BY active_date) AS rn
  FROM active_dates
),

-- 3. 计算基准
bASe AS (
  SELECT
    user_id,
    active_date,
    DATE_SUB(active_date, INTERVAL rn DAY) AS bASe_date
  FROM numbered
),

-- 4. 根据基准进行聚合得到计数和始末日期
SELECT
  user_id,
  MIN(active_date) AS begin_date,
  MAX(active_date) AS end_date,
  COUNT(bASe_date) AS continuous_days
FROM bASe
GROUP BY user_id, bASe_date
HAVING continuous_days >= 3
ORDER BY continuous_days;
```

最后的结果应该是这样的表格

| **user_id** | **begin_date** | **end_date** | **continuous_days** |
| --------- | ------------- | ------------- | ----------------- |
| **1** | 2025-03-20 | 2025-03-22 | 3 |
| **1** | 2025-03-24 | 2025-03-26 | 3 |
| **2** | 2025-03-21 | 2025-03-24 | 4 |

### 3.2 连续行为

有了上面的基础，对于连续行为的处理就很清晰明了了。连续行为问题是类似这样的问题：在一场比赛中，每一时间都有某个球员得分，计算至少连续三个时间点都是某个用球员得分的球员编号，以及连续得分期间的总得分。

| **user_id** | **score_time** | **score** | **rn_all** | **rn_user** | **rn_diff** |
| --------- | --------------------- | ------- | -------- | --------- | --------- |
| **A001** | 2025-03-25 09:00:00 | 2 | 1 | 1 | 0 |
| **A001** | 2025-03-25 09:05:00 | 2 | 2 | 2 | 0 |
| **A001** | 2025-03-25 09:10:00 | 2 | 3 | 3 | 0 |
| **A002** | 2025-03-25 09:15:00 | 3 | 4 | 1 | 3 |
| **A002** | 2025-03-25 09:20:00 | 2 | 5 | 2 | 3 |
| **A001** | 2025-03-25 09:25:00 | 2 | 6 | 4 | 2 |
| **A002** | 2025-03-25 09:30:00 | 2 | 7 | 3 | 4 |
| **A002** | 2025-03-25 09:35:00 | 2 | 8 | 4 | 4 |
| **A002** | 2025-03-25 09:40:00 | 3 | 9 | 5 | 4 |
| **A002** | 2025-03-25 09:42:00 | 1 | 10 | 6 | 4 |
| **A003** | 2025-03-25 09:45:00 | 2 | 11 | 1 | 10 |
| **A003** | 2025-03-25 09:50:00 | 2 | 12 | 2 | 10 |

操作流程为：
```sql
WITH
-- 1. 得到全部球员得分的序号 rn_all，得到单个球员得分的序号 rn_user
ranked AS (
  SELECT
    user_id,
    score,
    ROW_NUMBER() OVER (ORDER BY score_time) AS rn_all,
    ROW_NUMBER() OVER (PARTITION BY user_id ORDER BY score_time) AS rn_user
  FROM player_scores
),
-- 2. 对于每行，得到序号差值 rn_diff = rn_all - rn_user
diff AS (
  SELECT
    user_id,
    score,
    rn_all - rn_user AS rn_diff
  FROM ranked
),
-- 3. 根据 rn_diff 聚合得到连续次数和总得分
aim AS (
  SELECT
    user_id,
    rn_diff,
    COUNT(rn_diff) AS continuous_length,
    SUM(score) AS total_score
  FROM diff
  GROUP BY user_id, rn_diff
)
-- 4. 过滤得到连续次数大于目标次数的球员
SELECT 
  user_id,
  continuous_length,
  total_score
FROM aim
WHERE continuous_length >= 3;
```

最后的结果应该是这样的表格

| **user_id** | **continuous_length** | **total_score** |
| --------- | ------------------ | ------------- |
| **A001** | 3 | 6 |
| **A002** | 4 | 8 |



## 4. 窗口函数使用

### 4.1 计算累计指标

累计指标的含义就是**截止到 xxx 时期满足 xxx 条件的关于 xxx 的数量**，在数据分析中通常用于计算某个商品截止某年某月的销售额（KPI）。传统的方法就是对于每一个时期，找到所有小于他的时期，然后计算累计值，但是这样在日期数很多的时候，需要输入大量重复代码和 `UNION` 操作，这很明显不合适。

MySQL 提供了一个 `SUM()` 窗口函数，它可以自动实现**在指定范围（窗口）内对数值列进行累加，但不会将多行合并为一行，而是保留原有行数，输出每行对应的累加结果**，而且窗口函数支持分区、排序和指定范围，很适用于计算自定义的累计指标。

| **product_id** | **sale_date** | **sale_quantity** |
| ------------ | ------------- | --------------- |
| **1** | 2021-01-18 | 11 |
| **1** | 2021-01-25 | 14 |
| **1** | 2021-02-01 | 10 |
| **1** | 2021-02-10 | 10 |
| **1** | 2021-03-27 | 19 |
| **2** | 2021-01-24 | 5 |
| **2** | 2021-02-20 | 6 |
| **2** | 2021-02-28 | 7 |
| **3** | 2022-01-01 | 20 |

来看看我们需要干什么
- 按照日期提取月份 ➡️ `SUBSTRING(string, begin, end)`
- 每个产品对应一个分组 ➡️ `PARTITION BY product_id`
- 按照月份累计 ➡️ `ORDER BY sale_month`

```sql
WITH 
sale_monthly (
  SELECT
    product_id,
    SUBSTRING(sale_date, 1, 7) AS sale_month,
    SUM(sale_quantity) AS month_quantity
  FROM data_table
  GROUP BY product_id, substring(sale_date, 1, 7)
)

SELECT 
  product_id,
  sale_month,
  month_quantity,
  SUM(month_quantity) OVER(PARTITION BY product_id ORDER BY sale_month) AS month_kpi
FROM sale_monthly
ORDER BY product_id, sale_month;
```

最后的结果应该是这样的表格

| **product_id** | **sale_month** | **month_quantity** | **month_kpi** |
| ------------ | ------------ | ---------------- | ----------- |
| **1** | 2021-01 | 25 | 25 |
| **1** | 2021-02 | 20 | 45 |
| **1** | 2021-03 | 19 | 64 |
| **2** | 2021-01 | 5 | 5 |
| **2** | 2021-02 | 13 | 18 |
| **3** | 2022-01 | 20 | 20 |

### 4.2 计算去除最值后的平均

MySQL 提供了一个 `RANK()` 窗口函数，它可以实现对给定属性进行升序或降序排列，这样就能获得最小值和最大值，然后再利用 `AVG()` 进行聚合即可。

| **id** | **department** | **salary** |
| ---- | ------- | -------- |
| **1** | sale | 8000 |
| **2** | sale | 9000 |
| **3** | sale | 7500 |
| **4** | sale | 9000 |
| **5** | sale | 8300 |
| **6** | sale | 8000 |
| **7** | sale | 8600 |
| **8** | sale | 6800 |
| **9** | tech | 10000 |
| **10** | tech | 12000 |
| **11** | tech | 12500 |
| **12** | tech | 12300 |
| **13** | tech | 12500 |
| **14** | tech | 13000 |

```sql
WITH
ranked AS (
  SELECT
    department,
    salary,
    RANK() OVER (PARTITION BY department ORDER BY salary ASC) AS rank_ASc,
    RANK() OVER (PARTITION BY department ORDER BY salary DESC) AS rank_desc
  FROM data_table
)

SELECT 
  department,
  MIN(CASE WHEN rank_ASc = 1 THEN salary END) AS min_salary,
  MIN(CASE WHEN rank_desc = 1 THEN salary END) AS max_salary,
  ROUND(AVG(CASE WHEN rank_ASc > 1 AND rank_desc > 1 THEN salary END), 2) AS avg_salary
FROM ranked
GROUP BY department;
```

最后的结果应该是这样的表格

| **department** | **min_salary** | **max_salary** | **avg_salary** |
| ------------ | ------------ | ------------ | ------------ |
| **sale** | 6800 | 9000 | 8300 |
| **tech** | 10000 | 13000 | 12266.67 |

### 4.3 计算 Top-N

Top-N 是计算某个指标排名前 N 的对象，通常用于获取头部信息和进行广告推送。而用于排名的窗口函数有三个，但是它们处理并列的区别如下
- `ROW_NUMBER()`：即使值相同，编号也会递增
- `RANK()`：相同值会共享一个排名，但是会跳过并列的排名
- `DENSE_RANK()`：相同值会共享一个排名，但是不会跳过并列的排名

| **id** | **score** | **ROW_NUMBER** | **RANK** | **DENSE_RANK** |
| ---- | ------- | ------------ | ------ | ------------ |
| **A** | 100 | 1 | 1 | 1 |
| **B** | 90 | 2 | 2 | 2 |
| **C** | 90 | 3 | 2 | 2 |
| **D** | 80 | 4 | 4 | 3 |

因此，实际应用中我们通常需要相同值共享同一个排名，与此同时还希望不会跳过并列的排名，那么就使用 `DENSE_RANK()`。假设我们的需求是：对于每个商品，列出浏览该商品次数最多的两个客户，并向他们发送广告。

| **user_id** | **product_id** |
| - | - |
| **A1** | a |
| **A1** | a |
| **A1** | a |
| **A1** | b |
| **A1** | a |
| **A1** | a |
| **A1** | a |
| **A2** | a |
| **A2** | a |
| **A2** | a |
| **A2** | b |
| **A2** | b |
| **A3** | a |
| **A3** | a |
| **A3** | a |
| **A3** | b |
| **A3** | b |
| **A3** | a |
| **A3** | a |
| **A3** | a |
| **A4** | a |
| **A4** | b |
| **A4** | b |
| **A4** | b |
| **A4** | b |

操作流程如下：
1. 计算每个商品每个用户的浏览量
2. 按照商品进行分组，给浏览量进行排序
3. 选出每个商品浏览量前 2 的用户

```sql
WITH view AS (
  SELECT
    product_id,
    user_id,
    COUNT(*) AS view_count
  FROM data_table
  GROUP BY product_id, user_id
),
ranked AS (
  SELECT
    product_id,
    user_id,
    view_count,
    DENSE_RANK() OVER (PARTITION BY product_id ORDER BY view_count DESC) AS rn
  FROM view
)
SELECT
  product_id,
  user_id,
  view_count,
  rn
FROM ranked
WHERE rn <= 2
ORDER BY product_id, rn;
```

最后的结果应该是这样的表格

| **product_id** | **user_id** | **view_count** | **rn** |
| ------------ | --------- | ------------ | ---- |
| **a** | A1 | 6 | 1 |
| **a** | A3 | 6 | 1 |
| **a** | A2 | 3 | 2 |
| **b** | A4 | 4 | 1 |
| **b** | A2 | 2 | 2 |
| **b** | A3 | 2 | 2 |

### 4.4 计算事件相邻

有一张这样的日志表，每个时间点都有且只有一个客户执行某个操作，我们需要找出同一天执行完“签到”后立马执行“抽奖”的用户，**这里不要求时间上的相邻，而是要求对单个用户而言当天行为上的相邻**。

| **user_id** | **event_time** | **event_id** |
| - | - | - |
| **1001** | 2021-01-01 | login |
| **1001** | 2021-01-01 | register |
| **1001** | 2021-01-01 | logout |
| **1002** | 2021-01-02 | login |
| **1002** | 2021-01-02 | register |
| **1002** | 2021-01-02 | gift |
| **1002** | 2021-01-02 | logout |
| **1003** | 2021-01-01 | login |
| **1003** | 2021-01-01 | view |
| **1003** | 2021-01-01 | logout |
| **1004** | 2021-01-03 | login |
| **1002** | 2021-01-03 | register |
| **1004** | 2021-01-04 | gift |
| **1004** | 2021-01-04 | logout |

MySQL 提供了一个 `LEAD(<column>, <offset>, <default>)` 表示访问同一分区内的下一行，参数分别表示要获取的目标列，相对于当前行的偏移（默认 1 表示下一行），以及不存在偏移行的默认返回值。

```sql
WITH 
neighbor AS (
  SELECT
    user_id,
    event_id,
    event_time,
    LEAD(event_id) OVER (PARTITION BY user_id, event_time ORDER BY event_time) AS next_event_id
  FROM data_table
)

SELECT 
  DISTINCT user_id,
  event_time
FROM neighbor
WHERE event_id = 'register' AND next_event_id = 'gift';
```

最后的结果应该是这样的表格

| **user_id** | **event_time** |
| --------- | ------------- |
| **1002** | 2021-01-02 |



## 5. 留存率

留存率是衡量用户群在首次使用某服务/活跃后，在某个时间段后先前用户群继续使用/活跃的比例的指标，用于评估用户粘性和产品生命周期，其中使用产品/活跃指的是**用户在某个周期内至少有一次活动**

| **user_id** | **active_date** |
| --------- | ------------- |
| **1** | 2025-02-01 |
| **1** | 2025-02-02 |
| **1** | 2025-02-03 |
| **2** | 2025-02-01 |
| **2** | 2025-02-02 |
| **2** | 2025-02-03 |
| **2** | 2025-02-04 |
| **3** | 2025-02-01 |
| **3** | 2025-02-02 |
| **3** | 2025-02-06 |
| **4** | 2025-02-01 |
| **4** | 2025-02-02 |
| **4** | 2025-02-10 |

为了计算周期内是否活跃，实际上我们只需要**计算某个日期到起始日期的间隔是多少，如果这个间隔小于等于周期，则可以认为这个用户留存**，所以流程如下：

1. 计算每一日期对应的首次活跃的用户数量，临时表为 *(cohort_day, cohort_count)*
```sql
WITH 
cohort AS (
  SELECT 
    DATE(active_day) AS cohort_day,
    COUNT(DISTINCT user_id) AS cohort_count
  FROM data_table
  GROUP BY DATE(active_day)
),
```

2. 将 active_date 自联结 active_date，得到每一日期的不同用户的活跃日期差值，临时表为 *(cohort_day, end_day, user_id, day_diff)*
```sql
diff AS (
  SELECT 
    DATE(a.active_day) AS cohort_day,
    DATE(b.active_day) AS end_day,
    a.user_id,
    DATEDIFF(DATE(b.active_day), DATE(a.active_day)) AS day_diff
  FROM data_table a JOIN data_table b ON a.user_id = b.user_id
  WHERE DATEDIFF(DATE(b.active_day), DATE(a.active_day)) >= 1
)
```

3. 将上述两张临时表连接按照日期连接，对于每一日期，计算 day_diff 在周期内的 user_id 数量除以总数量 cohort_count，输出表为 *(cohort_day, next_day_retention, seven_day_retention)*
```sql
SELECT
  c.cohort_day,
  c.cohort_count,
  COUNT(DISTINCT CASE WHEN day_diff = 1 THEN d.user_id ELSE NULL END) AS next_day_count,
  ROUND(COUNT(DISTINCT CASE WHEN day_diff = 1 THEN d.user_id ELSE NULL END) / c.cohort_count, 4) AS next_day_retention,
  COUNT(DISTINCT CASE WHEN day_diff BETWEEN 1 AND 7 THEN d.user_id ELSE NULL END) AS seven_day_count,
  ROUND(COUNT(DISTINCT CASE WHEN day_diff BETWEEN 1 AND 7 THEN d.user_id ELSE NULL END) / c.cohort_count, 4) AS seven_day_retention
FROM diff d JOIN cohort c USING(cohort_day)
GROUP BY c.cohort_day
ORDER BY c.cohort_day;
```

最后的结果应该是这样的表格

| **cohort_day** | **cohort_count** | **next_day_count** | **next_day_retention** | **seven_day_count** | **seven_day_retention** |
| ------------ | -------------- | ---------------- | -------------------- | ----------------- | --------------------- |
| **2025-02-01** | 4 | 4 | 1.0000 | 4 | 1.0000 |
| **2025-02-02** | 4 | 2 | 0.5000 | 3 | 0.7500 |
| **2025-02-03** | 2 | 1 | 0.5000 | 1 | 0.5000 |