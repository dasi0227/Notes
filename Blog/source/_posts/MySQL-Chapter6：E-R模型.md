---
title: E-R模型
tags:
  - MySQL
categories:
  - 笔记
cover: /image/database.png
abbrlink: 3f15d095
date: 2024-10-09 22:17:45
description: 如何画E-R图，如何将E-R图转换为关系模式，E-R图的性质
---
<meta name="referrer" content="no-referrer"/>

## 1. 数据库设计

数据库设计流程
1. **需求分析**：与业务人员沟通，了解业务流程和数据需求
2. **概念设计**：将需求转化为高层次的实体-关系模型
3. **逻辑设计**：将实体-联系模型转换为关系模式，并规范化关系模式
4. **物理设计**：选择数据库管理系统，定义存储结构，优化查询性能
5. 实现与部署
6. 测试与优化
7. 维护与迭代

数据库设计目标：数据完整、冗余少、性能好、安全性高、可维护性高、可扩展性高

## 2. 实体-联系模型

### 2.1 实体（Entity）

**实体**：现实世界中可区别于所有其他对象的一个“事物”或“对象”

**实体集**：共享相同性质或属性的、具有相同类型的实体的集合

E-R图表示实体集：一个**矩形**，头部是实体集的名称，剩下是实体集所有属性的名称，其中作为主码的属性被加了下划线

![](https://dasi-blog.oss-cn-guangzhou.aliyuncs.com/DataBase/chapter6/202410101532296.png)

### 2.2 联系（Relationship）

**联系**：实体之间的关联

**联系集**：是相同类型联系的集合

![](https://dasi-blog.oss-cn-guangzhou.aliyuncs.com/DataBase/chapter6/202410101532295.png)

E-R图表示联系集：一个**菱形**，通过**线条**连接到多个不同的实体集

![](https://dasi-blog.oss-cn-guangzhou.aliyuncs.com/DataBase/chapter6/202410101532294.png)

### 2.3 概念

术语
- **参与**：实体集参与联系集R表示实体集之间存在联系R
- **度**：参与联系集的实体集数目
- **角色表示**：实体在联系中扮演的功能，在E-R图中的**线条上方**标识
- **描述性属性**：用于解释/描述联系的特定属性，提供了联系的更多相关信息，通过**虚线**连接一个**矩形**标识

![](https://dasi-blog.oss-cn-guangzhou.aliyuncs.com/DataBase/chapter6/202410101532293.png)

属性类型
- **简单**：不能被划分为子部分，例如性别
- **复合**：可以被划分为子部分，称为成员属性，例如住址可以被分为市、区、街道、房号
- **单值**：只有一个单独的值，例如身份证号
- **多值**：可以有多个不同的值，例如手机号
- **基**：直接存储在数据库中的原始数据，例如姓名、住址、出生日期
- **派生**：值可以从基属性的值派生出来，并不存储，例如年龄可以从出生日期和当前日期推算出来

![](https://dasi-blog.oss-cn-guangzhou.aliyuncs.com/DataBase/chapter6/202410101532292.png)

### 2.4 映射基数

映射基数（mapping cardinality）：表示**一个实体能通过一个联系集关联的其他实体的数量**
- **一对一（one-to-one）**：A中的一个实体至多与B中的一个实体相关联，B中的一个实体至多与A中的一个实体相关联
- **一对多（one-to-many）**：A中的一个实体可以与B中任意数量的实体相关联，B中的一个实体至多与A中的一个实体相关联
- **多对一（many-to-one）**：A中的一个实体至多与B中的一个实体相关联，B中的一个实体可以与A中任意数量的实体相关联
- **多对多（many-to-many）**：A中的一个实体可以与B中任意数量的实体相关联，同时B中的一个实体可以与A中任意数量的实体相关联

![](https://dasi-blog.oss-cn-guangzhou.aliyuncs.com/DataBase/chapter6/202410101532291.png)

E-R图：**箭头指向的实体表示只能有一个或最多一个**
- 一对一：一个学生最多只有一个导师，一位导师最多只有一位学生
- 一对多：一个学生最多最多有一个导师，但是一个导师可以有多个学生
- 多对一：一个学生可以有多个导师，但是一个导师最多有一位学生
- 多对多：一个学生可以有多个导师，一个导师也可以有多个学生

![](https://dasi-blog.oss-cn-guangzhou.aliyuncs.com/DataBase/chapter6/202410101532290.png)

自定义基数约束：用`l..h`的形式表示，其中l表示最小基数，h表示最大基数，可以用`*`表示没有限制，E-R图中在线段上方标识

{% note success flat %}
一对一可以表示为：`1..1`
一对多可以表示为：`1..*`
{% endnote %}

![](https://dasi-blog.oss-cn-guangzhou.aliyuncs.com/DataBase/chapter6/202410101532288.png)

### 2.5 参与约束

**全部（total）**：实体集E中的每个实体都**必须参与**到联系集R中的至少一个联系

**部分（partial）**：实体集E中的每个实体可以**选择性地参与**到联系集R中的一个联系

E-R图：**哪边是必须参与的，哪边就用双线标识**，例如学生必须有一个导师，但不是所有导师都需要有一个学生，因此联系到学生是双线

![](https://dasi-blog.oss-cn-guangzhou.aliyuncs.com/DataBase/chapter6/202410101532289.png)

## 3. 主码

### 3.1 联系集的主码

E-R图：**联系集R的主码是那些没有被有向线段指向的实体集的主码的并集**
- 一对一：老师id和学生id任选一个作为联系集的主码
- 一对多：学生只能选一个老师，因此学生id可以作为联系集的主码
- 多对一：老师只能有一个学生，因此老师id可以作为联系集的主码
- 多对多：老师id和学生id的组合作为联系集的主码


### 3.2 实体集类型

|类型|定义|E-R图|
|-|-|-|
|强实体集|可以独立存在的实体集，它有自己的主键，不需要依赖其他实体集来唯一标识|单边框矩形|
|弱实体集|不能独立存在的实体集，它依赖于标识性实体集和自己的分辨符属性来唯一标识|双边框矩形，属性用下划虚线|

标识性实体集：是一个概念，指代弱实体集所依赖的实体集

标识性联系：弱实体集与标识性实体集之间的关系，用**双边框菱形**表示

{% note warning flat %}
弱实体集必须参与标识性联系，因此弱实体集到标识性联系是双线标识的
{% endnote %}

![](https://dasi-blog.oss-cn-guangzhou.aliyuncs.com/DataBase/chapter6/202410101532287.png)

### 3.3 消除冗余

如果存在两个关系X,Y都有相同属性A，但是A是Y的主码，那么**A在X中就是冗余属性**，应该**设立联系集通过A将X和Y相关联**

![](https://dasi-blog.oss-cn-guangzhou.aliyuncs.com/DataBase/chapter6/202410101532286.png)

## 4. 将E-R图转换为关系模式

### 4.1 流程

1. 转换强实体集
   1. 为每个强实体集创建一个关系模式
   2. 实体集的属性转换为关系的属性
   3. 实体集的主键转换为关系的主键

![](https://dasi-blog.oss-cn-guangzhou.aliyuncs.com/DataBase/chapter6/202410101532285.png)

2. 转换弱实体集
   1. 为每个弱实体集创建一个关系模式
   2. 弱实体集的属性转换为关系的属性
   3. 弱实体集的部分键和标识性实体集的主键共同组成关系的主键
   4. 标识性实体集的主键作为外键引入弱实体集的关系中

![](https://dasi-blog.oss-cn-guangzhou.aliyuncs.com/DataBase/chapter6/202410101532284.png)

3. 转换联系集
   1. 一对一：不需要创建独立的关系模式，将外键添加到查询频率较高的一方
   2. 一对多：不需要创建独立的关系模式，而是将“一”方的实体集的主键作为外键嵌入到“多”方的实体集中
   3. 多对多：建立一个独立的关系模式，包含参与联系的实体集的主键作为外键，同时外键的组合作为新关系的主键

![](https://dasi-blog.oss-cn-guangzhou.aliyuncs.com/DataBase/chapter6/202410101532283.png)

4. 转换复杂属性
   1. 为复合属性的每个成员属性创建一个单独的属性
   2. 为每个多值属性创建一个新的关系模式，其中包含一个外键引用原实体的主码，以及单独一个多值属性的值

{% note success flat %}
例如主码为`id=2233`的学生有两个手机号110和119，那么就应该在多值属性的`student_phone`关系中插入两个元组`(2233,110)`和`(2233,119)`
{% endnote %}

### 4.2 冗余处理

**连接弱实体集与其对应的强实体集的联系集的模式是冗余的**

![](https://dasi-blog.oss-cn-guangzhou.aliyuncs.com/DataBase/chapter6/202410101532282.png)

**如果实体集a在联系集ab中的参与是全部的，那么转换的关系模式a和ab可以合并成单个模式**

![](https://dasi-blog.oss-cn-guangzhou.aliyuncs.com/DataBase/chapter6/202410101532281.png)

{% note success flat %}
即使是部分参与，我们也可以通过补空值的方式合并
{% endnote %}

## 5. E-R图高级特性

### 5.1 特化和概化

**特化（Specialization）**：将一个较为通用的实体集细分为多个更具体的实体集，子实体集继承父实体集全部属性，同时也可以拥有自己的属性

**概化（Generalization）**：将一组具有共同特征的实体集归纳为一个更一般的实体集，父实体集包含子实体集所有共同属性

约束
1. 不相交约束（disjoint）：子实体集之间是互斥的
2. 重叠约束（overlappig）：子实体集允许有交集
3. 完全性约束（total）：父实体集中的每个实体必须属于某个子实体集
4. 部分性约束（partial）：父实体集中的每个实体可以不属于某个子实体集

转换关系模式
1. 为每个高层实体集和底层实体集都创建一个关系模式
2. 对于每个低层实体集，引用高层实体集的主码作为外码约束，同时也作为主码属性

E-R图：用一个**空心箭头**从子实体集指向父实体集，又称为`ISA`联系

![](https://dasi-blog.oss-cn-guangzhou.aliyuncs.com/DataBase/chapter6/202410101532280.png)

### 5.2 聚集

**聚集（aggregation）**：将联系集本身作为一个整体参与其他联系集

E-R图：使用一个**矩形**包裹住一个联系和它的参与实体

![](https://dasi-blog.oss-cn-guangzhou.aliyuncs.com/DataBase/chapter6/202410101532279.png)

## 6. 注意事项

1. 当一个实体集的主码需要作为另一个实体集的属性时，应该通过 联系集 来表示这种关系，而不是直接将主码作为属性

2. 联系集本身已经隐含了参与实体集的主码属性，因此在设计联系集时，不需要显式声明这些主码属性

![](https://dasi-blog.oss-cn-guangzhou.aliyuncs.com/DataBase/chapter6/202410101532278.png)

3. 如果一个对象可以独立存在，并且有独特的标识和其他附加信息，就应该使用实体集（地址可以定义为实体集，性别年龄应该被定义为属性）

![](https://dasi-blog.oss-cn-guangzhou.aliyuncs.com/DataBase/chapter6/202410101532276.png)

4. 如果是描述发生在实体间的行为且不关联过多的信息，采用联系集

![](https://dasi-blog.oss-cn-guangzhou.aliyuncs.com/DataBase/chapter6/202410101532274.png)

5. 如果参与联系的对象总是或大部分只有两个，那么使用二元联系

![](https://dasi-blog.oss-cn-guangzhou.aliyuncs.com/DataBase/chapter6/202410101532299.png)

## 7. E-R图汇总

![](https://dasi-blog.oss-cn-guangzhou.aliyuncs.com/DataBase/chapter6/202410101532297.png)