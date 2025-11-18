---
title: 关系模型
tags:
  - MySQL
categories:
  - 笔记
cover: /image/database.png
abbrlink: 7fda2204
date: 2024-09-18 13:30:02
description: 介绍了关系数据库，其中包括关系的模式与实例、关系查询语言和关系代数
---
<meta name="referrer" content="no-referrer"/>

## 1. 关系数据库

关系数据库：将数据组织成表格形式，为每张表赋予一个唯一名称
- **表（table）**：每个表由行和列组成
- **元祖（tuple）**：指代行，每一行代表一个数据记录
- **属性（attribute）**：指代列，每一列代表一个数据字段

{% note info flat %}根据集合的定义，元组在关系中出现的顺序是无关紧要的{% endnote %}

**域（domain）**：每个属性允许取值的集合
{% note success flat %}
性别属性的域是男和女
年龄属性的域是0-100的整数
{% endnote %}

**原子的（atomic）**：一个域中的元素被认为是不可再分的单元
{% note success flat %}
数量上：联系电话可以既填自己、父母和朋友等，是多个手机号码的集合
结构上：手机号可以拆分为国家编号、地区编号和通信公司编号等，是多个字段的组成
{% endnote %}

**关系模式（schema）**：描述了关系的**蓝图**，定义了表的**名称、属性、数据类型、域和约束**

关系实例（instance）：描述了关系的**快照**，存储了某时刻的数据集合，是具体的元组的集合
{% note success flat %}
学生关系的模式：student(name,id,age,major,cardnum)
学生关系的实例：(dasi,22336218,20,cs,5201314)
{% endnote %}

## 2. 码

{% label "数据完整性（uniqueness）" orange %}
- **实体完整性**：确保任一元组的所有属性值必须能**唯一标识**该元组，即一个关系中**不能存在两个元组在所有属性值上都相同**
- **引用完整性/参照完整性**：确保引用属性的值必须存在于其他表中
- **域完整性**：确保属性值符合域和数据结构
- **用户自定义完整性**：属性值符合特定业务的规则

**超码（superkey）**：一个或多个属性的集合，超码可以在一个关系中唯一标识出一个元组

{% note info flat %}
根据定义，超码的**任意超集**都是超码，因此可能存在很多超码
{% endnote %}

**候选码（candidate key）**：任意真子集都不是超码的**最小超码**

{% note info flat %}
候选码虽然是最小的，但是**可以有多个候选码**，如学生既可以用身份证唯一标识，也可以用学号唯一标识，还可以用“专业+毕业高中+年级+姓名”的组合来唯一标识
{% endnote %}

**主码（primary key）**：由数据库设计者**人为选中**来作为在一个关系中区分不同元组的候选码
- 主码**一定是候选码**！主码**一定是超码**！
- 主码**不是表的天然属性**，是人根据数据库的使用目的来手动选择的！
- 主码的选择必须是那些**不变化或者极少变化的属性**！

{% note info flat %}习惯上，总是将主码属性放在其他属性**之前**，并加**下划线**：student(<u>id</u>,name,age){% endnote %}

**外码（foreign key）**：外码用于引用另一个关系中的主码或唯一约束
- 用来确保数据的引用完整性，即外码值必须在被引用的主码或唯一约束中存在
- 外码可以引用本关系中的主码，形成自引用

{% note warning flat %}
外码约束不等于引用完整性约束！外码约束是引用完整性约束的子集，引用完整性不仅包括外键与主键的关系，还可能涉及更复杂的业务规则
{% endnote %}

## 3. 模式图

每个关系为一个框，关系名用灰色显示在顶部，在框内列出了各属性

{% note info flat %}
使用**双箭头**表示不是外码约束的引用完整性约束
数据库系统支持**图形化用户界面**的设计工具来创建数据库模式图
{% endnote %}

## 4. 关系查询语言

- **命令式（imperative）**：明确指定数据库操作的步骤和顺序，如存储过程、触发器
- **函数式（functional）**：通过函数或表达式来描述数据操作，如SQL 内置函数、关系代数
- **声明式（declarative）**：只需要描述“想要什么”，而不需要指定“如何做”，如SQL 查询

## 5. 关系代数

### 5.1 选择运算（select）

功能：选出满足给定谓词的元组，使用$\sigma$来表示，谓词写在$\sigma$的下标，关系写在$\sigma$后的括号内，并支持比较运算和逻辑连接词

{% note success flat %}
查询月薪高于10000的老师：$\sigma_{salary>10000}(teacher)$
查询月薪高于10000且年龄大于40的老师：$\sigma_{age>40 \land salary>10000}(teacher)$
{% endnote %}

### 5.2 投影运算（project）

功能：用于过滤掉属性从而只给出特定属性的关系，使用$\Pi$表示，希望显示的属性列表作为$\Pi$的下标，关系写在$\Pi$后的括号内，并支持在属性列表中使用算术运算

{% note success flat %}
查询老师的名字、年龄和编号：$\Pi_{name,age,id}(teacher)$
查询老师的名字和减去税收100的月薪：$\Pi_{name,salary-100}(teacher)$
{% endnote %}

### 5.3 笛卡尔积运算（cartesian-product）

功能：将两个关系的元组拼接成单个元组，使用$\times$表示，对于仅出现在一个关系的属性，通常删除关系名前缀

{% note success flat %}
学生：$student(id,name,major)$
老师：$teacher(name,course,salary)$
学生和老师的笛卡尔积：$(id,student.name,major,teacher.name,course,salary)$
{% endnote %}

### 5.4 连接运算（join）

功能：用于选择笛卡尔积中满足谓词的元组，用符号$\bowtie$表示，谓词作为$\bowtie$的下标，笛卡尔积放在$\bowtie$后的括号内

实际上连接运算等价于：$r\bowtie_{\theta}s = \sigma_{\theta}(r \times s)$

{% note success flat %}
学生是2022级且老师名字是dasi的连接：$student\bowtie_{student.year=2022 \land teacher.name=dasi}teacher$
{% endnote %}

### 5.5 并运算（union）

功能：用于给出两个关系的并集，使用$\cup$表示。要求两个关系必须有**相同数量的属性**，且关系对应**属性类型必须相同**

{% note success flat %}
查询2017年或2018年开设课程的id：$\Pi_{coureid}(\sigma_{year=2017}(section))\cup\Pi_{coureid}(\sigma_{year=2018}(section))$
{% endnote %}

### 5.6 交运算（intersection）

功能：用于给出两个关系的交集，使用$\cap$表示

{% note success flat %}
查询2017年且2018年都开设课程的id：$\Pi_{coureid}(\sigma_{year=2017}(section))\cap\Pi_{coureid}(\sigma_{year=2018}(section))$
{% endnote %}

### 5.7 差运算（set-difference）

功能：用于给出两个关系的差集，使用$-$表示

{% note success flat %}
查询2017年开设但2018年没有开设的课程id：$\Pi_{coureid}(\sigma_{year=2017}(section))-\Pi_{coureid}(\sigma_{year=2018}(section))$
{% endnote %}

### 5.8 赋值运算（assignment）

功能：将关系代数表达式的结果赋值给临时的关系变量，使用$\leftarrow$表示，左边是关系变量，右边是关系代数表达式

{% note success flat %}
查询2017年且2018年都开设课程的id
$course_2017 \leftarrow \Pi_{coureid}(\sigma_{year=2017}(section))$
$course_2018 \leftarrow \Pi_{coureid}(\sigma_{year=2018}(section))$
$course_2017 \cap $course_2018$
{% endnote %}

### 5.9 更名运算（rename）

功能：给关系代数表达式的结果赋予一个名称，使用$\rho$表示，下标是名称，后跟括号内是关系代数表达式

- 给表达式E的结果命名为x：$\rho_x(E)$
- 给表达式E的结果命名为x，并且将其属性重命名为$A_1,···,A_n$：$\rho_{x(A_1,···,A_n)}(E)$

{% note success flat %}
查询比ID为123的老师工资多的老师的姓名：$\Pi_{i.name}((\sigma_{i.salary>w.salary}(\rho_{i}(teacher)\times\sigma_{w.id=123}(\rho_{w}(teacher)))))$
{% endnote %}
