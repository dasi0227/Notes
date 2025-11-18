---
title: 中级SQL
tags:
  - MySQL
categories:
  - 笔记
cover: /image/database.png
description: 连接，视图，事务，完整性约束，数据定义，索引和授权
abbrlink: 2566557f
date: 2024-09-19 19:41:28
---
<meta name="referrer" content="no-referrer"/>

## 1. 连接

什么是连接：**将多个表中的元组经过特定方式结合在一起，以便进行特定的查询**

为什么使用连接：**笛卡尔积会生成大量无意义的元组组合**

![](https://dasi-blog.oss-cn-guangzhou.aliyuncs.com/DataBase/chapter4/202409241401382.png)

### 1.1 NATURAL JOIN

自动基于两个表中**同名的属性**来匹配元组

```sql
select student.name
from student natural join takes;
```

{% note warning flat %}
`relation1 natural join relation2,relation3`不等价于`relation1 natural join relation2 natural join relation3`，因为前者是与relation3的笛卡尔积，后者是与relation3的自然连接
{% endnote %}

### 1.2 INNER JOIN

`inner join...on <谓词>`：设置通用的谓词来明确连接条件

```sql
-- 内连接
select student.ID,takes.ID,name,course_id
from student join takes on student.ID = take.ID;
```

{% note info flat %}
`join`缺省情况下是内连接`inner join`
{% endnote %}

### 1.3 OUTER JOIN

{% note info flat %}
自然连接和内连接的局限性：**仅保留匹配的记录，而丢失其他元组，但有时候我们又希望保留部分不匹配元组**
{% endnote %}

`left/right/full outer join...on <谓词>`：不仅返回满足连接条件的行，还会返回部分未匹配的行，自动用空值填充缺失的属性
- **左外连接**：只保留出现在左边的关系中的元组
- **右外连接**：只保留出现在右边的关系中的元组
- **全外连接**：保留出现在两个关系中的元组

使用左外连接
![](https://dasi-blog.oss-cn-guangzhou.aliyuncs.com/DataBase/chapter4/202409241401384.png)

使用右外连接
![](https://dasi-blog.oss-cn-guangzhou.aliyuncs.com/DataBase/chapter4/202409241401385.png)

### 1.4 USING

`JOIN USING (<属性列表>)`：用于指定连接两个表时使用的相同列名，使得查询更加简洁

```sql
-- 列出所有被选课程的信息
select *
from takes join course using (course_id);
```

### 1.5 总结

实际上，连接可以分为**连接类型**和**连接条件**，**任意的连接类型可以和任意的连接条件进行组合**

![](https://dasi-blog.oss-cn-guangzhou.aliyuncs.com/DataBase/chapter4/202409241401386.png)

以下四种方式是等价的
```sql
-- 自然连接
select course_id
from student natural join takes;
-- 内连接
select course_id
from student inner join takes on student.ID = take.ID;
-- USING运算
select course_id
from student join takes using (ID);
-- 使用where子句
select course_id
from student,takes
where student.ID = takes.ID;
```

## 2. 视图

`create view <视图名> as <查询表达式>`：视图是**虚拟表，不存储数据，每次查询时动态生成结果**，目的是用户**可以不必重复编写**复杂的SQL语句来访问同一个表

{% note warning flat %}
普通视图可以看做成是**永久性的with语句**
{% endnote %}

```sql
-- 创造物理系在2017年秋季开设的所有课程信息视图
create view physics_fall_2017 as
  select course.course_id,sec_id,building,room_number
  from course,section
  where course.course_id = section.course_id
    and course.dept_name = 'Physics'
    and section.semester = 'Fall'
    and section.year = 2017;
-- 查看视图
select *
from physics_fall_2017;
-- 使用视图
select course_id
from physics_fall_2017;
```

![](https://dasi-blog.oss-cn-guangzhou.aliyuncs.com/DataBase/chapter4/202409241401378.png)

**物化视图（materialized view）**：是一种特殊类型的视图，它在数据库中存储实际的数据，而不是简单地存储查询定义，同时物化视图需要持续刷新来保持**数据的最新状态**

如果视图满足下列可更新条件，对视图的更新会反映到基表中
- 简单视图：**没有GROUP BY、DISTINCT、ODDERED BY和HAVING等**
- 单一表：定义视图时**不允许使用连接，嵌套子查询，集合运算**
- 没有计算列：**没有计算列、表达式和聚集函数**

## 3. 约束

### 3.1 NOT NULL

**非空约束**：某些属性的值不允许为空

```sql
-- 姓名和预算不允许为空
name varchar(20) not null
budget numeric(12,2) not null
```

{% note warning flat %}
主码始终满足非空约束
{% endnote %}

### 3.2 UNIQUE

**唯一性约束**：关系中没有两个元组在某些属性上的取值相同

```sql
-- 同一学期同一建筑同一房间同一时间不允许有两个课程
unique(semester,building,room_number,time_slot_id)
```

### 3.3 CHECK

**检查约束**：指定一个谓词，关系中的每个元组都必须满足这个谓词

```sql
-- 学期必须是四个季节之一
check(semester in ('Fall','Winter','Spring','Summer'))
```

### 3.4 REFERENCES

**引用约束**：确保在一个表中引用另一个表的行时，引用的值在被引用的表中是有效的

```sql
-- 系名必须存在于系表中
foreign key (dept_name) references department(dept_name)
```

### 3.5 CASCADE

**级联约束**：用在外码中，当主表中的记录被删除/更新时，自动删除/更新外表中相关的记录

```sql
foreign key (dept_name) references department(dept_name) 
-- 删除被引用的元组时，自动删除所有引用该元组的元组
on delete cascade,
-- 更新被引用的元组时，自动更新所有引用该元组的元组
on update cascade
```

### 3.6 CONSTRAINT

**约束命名**：给上述约束起名字，当违反约束时可以根据名称来明确错误类型

```sql
-- 给check约束命名为min_salary
salary numeric(8,2), constraint min_salary check(salary > 20000)
```

### 3.7 assertion

**断言约束**：用于定义跨多个表或行的全局条件，确保数据库中的数据满足特定的规则

```sql
-- 用于检查所有学生的总学分是否与他们实际获得的学分一致
create assertion tot_credits_constraint check(\
  not exists(
    select ID
    from student
    where tot_cred <> (
      select coalesce(sum(credits), 0)
      from takes natural join course
      where student.ID = takes.ID and grade is not null
    )
  )
)
```

{% note success flat %}
SQL不提供`for all X, P(X)`的结构，所以一般采用`not exists X that not P(X)`，即**对全部X都有P==不存在X不满足P**
{% endnote %}

## 4. 数据处理

### 4.1 日期和时间

数据类型
- `DATE`：存储年月日，**YYYY-MM-DD**
- `TIME`：存储时分秒，**HH:MM:SS**
- `DATETIME/TIMESTAMP`：存储时间戳，**YYYY-MM-DD HH:MM:SS**

内置函数
- `CURDATE()`：返回当前年月日
- `CURTIME()`：返回当前时分秒
- `NOW()`：返回当前时间戳

```sql
-- 创建一个事件表
CREATE TABLE events (
  event_id INT PRIMARY KEY,
  event_date DATE,
  event_time TIME,
  event_timestamp TIMESTAMP
);
-- 插入事件记录
INSERT INTO events (event_id, event_date, event_time, event_timestamp) VALUES
(1, CURRENT_DATE, CURRENT_TIME, NOW()),
(2, '2024-09-23', '14:30:00', '2024-09-23 14:30:00');
-- 查询事件记录的年份
SELECT YEAR(event_timestamp) AS year,
FROM events;
```

### 4.2 类型转换

#### 4.2.1 CAST

`cast(expression as type)`：将表达式e转换为类型t

```sql
-- 将字符串 '123' 转换为整数 123
SELECT CAST('123' AS SIGNED);
-- 将字符串 '2023-10-01' 转换为日期
SELECT CAST('2023-10-01' AS DATE);
-- 将浮点数 123.45 转换为小数类型
SELECT CAST(123.45 AS DECIMAL(5, 2));
```

#### 4.2.2 FORMAT

`format(number, decimal)`：格式化数字，**添加千位分隔符并指定小数位数**

```sql
-- 返回 '1,234,567.89'
SELECT FORMAT(1234567.89, 2);
-- 返回 '1,235'
SELECT FORMAT(1234.567, 0);
```

#### 4.2.3 COALESCE

`coalesce(column, value)`：用于提供默认值或处理空值

```sql
-- 显示教师的ID和工资，但是将空工资显示为-1
select ID, coalesce(salary, -1)
from instructor;
```

{% note warning flat %}
处理后的值必须符合属性数据结构
{% endnote %}

### 4.3 DEFAULT

用于插入数据时，指定某些属性的初始值/缺省值

```sql
-- 学生的初始学分为0
create table student(
  ID          varchar (5),
  name        varchar (20) not null,
  dept_name   varchar (20),
  tot_cred    numeric (3,0) default 0,
  primary key (ID)
);
```

### 4.4 LOB

- 字符大对象（CLOB）：用于存储大量的文本数据
- 二进制大对象（BLOB）：用于存储大量的二进制数据，如图像、音频、视频等

```sql
book_review clob(10KB) 
picture blob(10MB) 
movie blob(2GB)
```

### 4.5 自定义

`create type type_name as data_type`：自定义一个数据类型

```sql
-- 创建美元数据类型并使用
create type Dollars as numeric(12,2);
create table department(
  dept_name varchar(20),
  building  varchar(15),
  budget    Dollars
);
```

`create domain domain_name domain_definition`：自定义一个域类型

```sql
-- 不仅可以设置数据类型，还可以添加约束条件
create domain Dollars as numeric(12,2) unique not null;
```

### 4.6 AUTO_INCREMENT

为主码生成唯一的、递增的值，而不是人为去一个个设置

```sql
-- MySQL
create table test (
  ID number(5) AUTO_INCREMENT
);
```

{% note warning flat %}
MySQL会为AUTO_INCREMENT设置一个计数器，计数器是单调递增的，即如果删除元组不会导致计数器回退，如果数据库发现当前id已经被占用，则继续递增
{% endnote %}

## 5. 授权

### 5.1 GRANT

`grant <权限列表> (<属性列表>) on <对象列表> to <用户/角色列表>;`
- `(属性列表)`是可选的，不是所有数据库都支持
- 对象可以是表、视图、数据库
- 关键字`all previleges`表示授予全部权限
- 关键字`public`表示公开，即授权给全部人

```sql
-- 给数据库用户Amit授予了在department关系上的选择权限
grant select on department to Amit;
-- 授予关于department的全部权限给全部人
grant all previleges on department to public;
```

### 5.2 ROLE

不必给每一个用户都使用相同命令来设置权限，而是**先给角色授予权限，再给用户授予角色即可**

```sql
-- 授予用户权限
grant delete on department to dasi;
-- 创建老师和教导主任角色
create role dean;
create role teacher;
-- 授予角色权限
grant update on teaches to dean;
grant select on teaches to teacher;
-- 将老师的权限授予教导主任
grant teacher to dean;
-- 将教导主任的权限授予用户
grant dean to dasi;
```

{% note warning flat %}
角色可以授予用户，也可以授予其他角色，用户可以有多重身份
{% endnote %}

### 5.3 视图权限

- 如果当前用户希望创建一个视图，必须**在视图引用的底层表上至少有选择权限**
- 可以给其他用户授予使用视图的权限
- 用户对视图的权限不会自动继承到底层表

```sql
-- 创建视图
create view geo_instructor as(
  select * 
  from instructor 
  where dept_name = 'Geology'
);
-- 给用户授权使用视图来查询
grant select on geo_instructor to dasi;
```

### 5.4 引用权限

用户必须拥有某个表的引用权限才能**在新表中定义对该表的外键约束**

```sql
-- 允许dasi引用department关系的dept_name属性
grant references (dept_name) on department to dasi;
```

### 5.5 转移权限

用户可以不仅赋予它使用的权限，还赋予它授权别人的权利

```sql
-- 授予Amit在department上的选择权限，并且允许Amit将该权限授予其他用户
grant select on department to Amit with grant option;
```

### 5.6 收回权限

- `restrict`是禁止级联收权，如果权限已经转移，则收权失败
- `cascade`是允许级联收权，会收回其他用户的权限

```sql
-- 非级联
revoke select on department from Amit restrict;
-- 级联
revoke select on department from dasi cascade;
-- 收回授权的权利
revoke grant option for select on department from Amit;
```