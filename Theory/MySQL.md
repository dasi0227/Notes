# MySQL



## 基本概念

**RDB（Relational Database, 关系系数据库）**是一种建立在关系模型基础上的数据库，数据以**表格（Table）**的形式组织，每张表由**行（Row）和列（Column）**组成，利用**主键和外键**实现数据间的**一对多、一对一和多对多**关系

**SQL（Structured Query Language, 结构化查询语言）**是用来与数据库交互的**通用声明式语言**，又可以细分为

- **DDL（Data Definition Language）**：定义数据库结构，如 CREATE、ALTER、DROP、TRUNCATE
- **DML（Data Manipulation Language）**：对表中数据进行操作，如 SELECT、INSERT、UPDATE、DELETE
- **DCL （Data Control Language）**：用来控制数据库的权限和访问，如 GRANT、REVOKE
- **TCL（Transaction Control Language）**：用来管理数据库事务，如 COMMIT、ROLLBACK、SAVEPOINT

**MySQL** 是一种实现了 RDB 并支持 SQL 语法的数据库系统，MySQL 由于其**开源免费、成熟稳定、功能完善、文档丰富、兼容性好、高可用、高性能**等优点，广泛使用在各类系统之中



## 字段类型

### 数值类型

整数

- **TINYINT**：1 字节，范围 ±128～127
- **SMALLINT**：2 字节，范围约 ±3万
- **MEDIUMINT**：3 字节，范围约 ±800万
- **INT**：4 字节，范围约 ±21亿
- **BIGINT**：8 字节，范围约 ±900万兆

> 整型具有一个 **UNSIGNED 属性，可以令最高位不用作正负符号位，统一为正数**，因此最高位也用作数值位，即**把正整数的上限提高一倍，下限为 0**

浮点数

- **FLOAT**：4 字节，单精度浮点数，大约能保证 6～7 位有效数字
- **DOUBLE**：8 字节，双精度浮点数，大约能保证 15~16 位有效数字
- **DECIMAL(M, D) / NUMERIC(M, D)**：动态大小，精确精度，M 指定总位数，D 指定小数位数

### 字符串类型

- **CHAR(M)**：定长字符串，最长 255 字符，如果不足长度会用空格符号补齐
- **VARCHAR(M)**：变长字符串，最大 65535 字节，如果不足长度不会补齐，但是底层会额外用 1～2 字节存实际长度
- **TEXT**：文本，分为 TINYTEXT、TEXT、MEDIUMTEXT、LONGTEXT
- **BLOB**：二进制数据，分为 TINYBLOB、BLOB、MEDIUMBLOB、LONGBLOB

> 内存分别占据：255B - 64KB - 16MB - 4GB

### 日期时间类型

- **YEAR**：YYYY，占 1 字节
- **TIME**：HH:MM:SS，占 3 字节
- **DATE**：YYYY-MM-DD，占 3 字节
- **DATETIME**：YYYY-MM-DD HH:MM:SS，占 8 字节，存储字面量，存啥取啥
- **TIMESTAMP**：YYYY-MM-DD HH:MM:SS，占 4 字节，存储时会自动转为 UTC，读取时再根据当前时区转为本地时间



## NULL

### 含义

NULL 在 MySQL 中表示”**未知**“，它既不表示”零“，也不表示“错”，甚至不能完全表示为”空“

- NULL 的语义**既可以是不存在值，也可以是不知道值**
- NULL 与任何值（包括 NULL）比较运算的结果都是 UNKNOWN
- NULL 与任何值（包括 NULL）算术运算的结果都是 NULL
- NULL 与任何值（包括 NULL）逻辑运算的结果，除非是短路，否则都是 NULL
- 除了 `COUNT(*)` 的所有聚合函数都会忽略 NULL
- 在 `ORDER BY` 中，NULL 会被当作最小值
- 只能通过 `IS NULL` 和 `IS NOT NULL` 来判断，而不能通过 `= NULL`

### 不推荐原因

在实际业务中，通常会给每一列加上 `NOT NULL DEFAULT x` 来约束非空，并且设置当插入未指定值时填充的默认值

1. 存储层面：如果表的任何一列可以为 NULL，那么 MySQL 会为这个表中的每一行维护一个 bitmap，来标志这些列是否为 NULL，造成额外存储开销
2. 运算层面：在运算之前可能都需要先判断 `IS NULL` 和 `IS NOT NULL` 
3. 索引层面：B+Tree/Hash 都要特殊处理 NULL，会降低索引效率
4. 兼容层面：在 ORM 框架中需要额外判断 NULL，否则会出现 NullPointerException 异常



## 存储引擎

### 定义

存储引擎是**表级别的底层实现机制**，决定了一张表的**数据、索引、事务、锁**是如何存储和管理的，负责表的物理存储和数据操作，通过解析上层 SQL 来处理下层存储

### InnoDB





## 基础架构

## 日志

## 索引

## 事务

## 锁

## SQL 优化

## 性能优化

