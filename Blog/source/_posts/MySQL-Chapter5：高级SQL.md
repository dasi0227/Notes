---
title: 高级SQL
tags:
  - MySQL
categories:
  - 笔记
cover: /image/database.png
abbrlink: 68260beb
date: 2024-10-09 14:28:11
description: 动态SQL，嵌入式SQL，存储过程，函数，触发器，程序结构
---
<meta name="referrer" content="no-referrer"/>

## 1. 程序设计语言访问SQL

必要性
- SQL并**没有提供通用语言的全部表达能力**，需要通过高级语言C、Java或Python来编写实现
- **非声明式动作不能通过SQL实现**，如打印一份报告、与用户实时交互、图形化展示等

方式
- 动态SQL：在程序运行时动态生成和执行SQL语句的技术，通过字符串拼接的方式生成SQL语句，然后通过数据库接口执行
- 嵌入SQL：通过预处理器将SQL语句转换为宿主语言的可执行代码

SQL注入：用户输入可能被直接拼接到SQL语句中，应使用参数化查询或对用户输入进行严格的验证和转义

## 2. FUNCTION

接受输入参数，**返回一个结果**

```sql
-- 输入系名，返回该系的老师总数
create function dept_count(dept_name varchar(20)) 
returns int
begin
  declare d_count int;
    select count(*) into d_count
    from instructor
    where instructor.dept_name = dept_count.dept_name
  return d_count;
end;

-- 返回计算结果
create function add_numbers(a int, b int)
returns int
begin
    return a + b;
end;

-- 直接使用
select dept_count('computer science');
select add_numbers(1, 2);
```

## 3. PROCEDURE

接受输入参数，**执行一系列操作或逻辑**

```sql
create procedure add_employee (
    in emp_id int,
    in emp_name varchar(50),
    in emp_salary decimal(10, 2)
)
begin
    insert into employees (id, name, salary)
    values (emp_id, emp_name, emp_salary);
end;

-- call使用
call add_employee(101, 'John Doe', 50000.00);
```

## 4. TRIGGER

在特定的事件发生时，**自动执行预定义的语句**
- 触发事件：触发器在什么事件发生时被激活（INSERT、UPDATE 或 DELETE）
- 触发时间：触发器在事件之前还是事件之后执行（BEFORE、AFTER）
- 触发动作：触发器执行的具体操作

```sql
-- 在插入新员工记录之前，自动生成员工 ID
create trigger before_employee_insert
before insert on employees
for each row
begin
  set new.employee_id = (select max(employee_id) + 1 from employees);
end;
```

## 5. 程序结构

### 5.1 WHILE

```sql
WHILE 布尔表达式 DO
  语句序列;
END WHILE;
```

### 5.2 REPEAT

```sql
REPEAT 
  语句序列;
UNTIL 布尔表达式
END REPEAT;
```

### 5.3 IF

```sql
IF 布尔表达式 THEN
    语句序列;
ELSEIF 布尔表达式 THEN
    语句序列;
ELSE
    语句序列;
END IF;
```

### 5.4 CASE

```sql
CASE
  WHEN 布尔表达式 THEN 语句序列;
  WHEN 布尔表达式 THEN 语句序列;
  ELSE 语句序列;
END CASE;
```