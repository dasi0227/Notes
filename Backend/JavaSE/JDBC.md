# JDBC

## 概述

JDBC 是 Java 提供的一套标准 API，用于在 Java 程序中统一地访问各种关系型数据库，使得程序员不必关心底层数据库厂商的细节，就能使用统一的接口进行增删改查，实现跨数据库的可移植性

java.sql：是 Java 标准库里定义 JDBC API 的包，主要包含了操作关系型数据库所需的核心接口和类
- Driver：定义了数据库驱动必须实现的接口，负责将 JDBC 调用转为数据库厂商的网络协议
- DriverManager：加载并管理一组 Driver，通过它的 getConnection(...) 方法为应用提供 Connection
- Connection：表示与数据库的会话。可以用它来创建 Statement、开启/提交/回滚事务、获取元数据等
- Statement：执行静态 SQL
- PreparedStatement：执行带参数的预编译 SQL
- CallableStatement：调用存储过程
- ResultSet：封装 SELECT 查询结果，以游标方式逐行读取
- SQLException：所有 JDBC 操作抛出的异常类型，包含错误码和 SQL 状态码等信息
- DatabaseMetaData：用于查询数据库的元信息
- ResultSetMetaData：用于查询结果集的元信息

JDBC 流程
1. 加载驱动
2. 建立与数据库的连接
3. 创建 SQL
4. 执行 SQL
5. 处理返回的结果
6. 关闭资源

> 从 mysql 5.1.6 开始就不需要再注册驱动，因为底层已经自动帮我们实现了

## 建立连接的方式

利用 DriverManager.getConnection
```java
Connection conn = DriverManager.getConnection(url, user, password);
```

利用 DataSource
```java
MysqlDataSource ds = new MysqlDataSource();
ds.setURL(url);
ds.setUser(user);
ds.setPassword(password);
Connection conn = ds.getConnection();
```

## Connection

- Statement createStatement()：创建一个用于执行静态 SQL 的 Statement
- PreparedStatement prepareStatement(String sql)：创建一个可绑定参数的预编译 SQL 语句对象
- CallableStatement prepareCall(String sql)：创建一个调用存储过程的 CallableStatement
- DatabaseMetaData getMetaData()：获取此连接所对应数据库的元数据
- boolean isValid(int timeout)：检查连接在给定秒数内是否仍有效
- void setReadOnly(boolean readOnly)：将连接置为只读模式
- boolean isReadOnly()：检查是否只读
- String getSchema()：设置当前连接的默认模式
- void setSchema(String schema)：获取当前连接的默认模式
- boolean isClosed()：检查连接是否已关闭
- void close()：关闭连接

## ResultSet

ResultSet 就是对查询结果的“游标”（Cursor）封装，允许你以编程方式在它返回的行集合中移动、读取甚至更新

- boolean next()：移到下一行，返回 false 表示已到末尾
- boolean previous()：移到上一行，返回 false 表示已到开头
- boolean rs.first()：移到第一行
- boolean rs.last()：移到最后一行
- boolean absolute(int row)：移动到指定行号，正数从头数，负数从尾数
- rs.beforeFirst()：移到第一行之前，用于正序遍历
- rs.afterLast()：移到最后一行之后，用于倒序便利
- int getRow()：返回当前行号
- XXX getXXX(int columnIndex)：按列索引读取指定类型的值
- XXX getXXX(String columnLabel)：按列名称读取指定类型的值
- boolean wasNull()：判断上一次读取的列值是否为 SQL NULL
- void updateXXX(...)：修改当前行的列值
- void updateRow()：提交对当前行的修改
- void insertRow()：在插入行区域提交新行
- void deleteRow()：删除当前行
- void close()：关闭游标并释放资源
- ResultSetMetaData getMetaData()：获取列的元信息 
  - int getColumnCount()：返回结果集中列的总数
  - String getColumnName(int column)：返回第 column 列的名称
  - int getColumnType(int column)：获取第 column 列的 SQL 类型
  - boolean isAutoIncrement(int column)：判断是否自动增长

## Statement

- ResultSet executeQuery(String sql)：执行 SELECT 语句，返回查询结果的 ResultSet
- int executeUpdate(String sql)：执行 INSERT、UPDATE、DELETE、CREATE、DROP，返回受影响行数
- boolean execute(String sql)：通用执行方法，返回 true 表示返回 ResultSet，返回 false 表示返回受影响函数
- ResultSet getResultSet()：获取 ResultSet
- int getUpdateCount()：获取受影响行数
- void setMaxRows(int max) / int getMaxRows()：设置／获取查询返回的最大行数
- void setQueryTimeout(int seconds) / int getQueryTimeout()：设置／获取 SQL 执行的超时时间（秒）
- void close() / boolean isClosed()：关闭此 Statement 并释放资源／检查是否已关闭  

## SQL 注入

SQL 注入（SQL Injection）是一种常见的安全漏洞，攻击者通过在应用程序的输入中注入恶意的 SQL 片段，使后台数据库执行非预期的命令，从而达到窃取、篡改甚至删除数据的目的

```java
System.out.print("用户名：");
String inputUser = sc.nextLine().trim();
System.out.print("密码：");
String inputPwd  = sc.nextLine().trim();

// ⚠️ 漏洞写法：直接拼接用户输入到 SQL
String sql = "SELECT * FROM users "
			+ "WHERE username = '" + inputUser + "' "
			+   "AND passwd   = '" + inputPwd  + "'";
System.out.println("执行 SQL: " + sql);
```

假设用户名为 dasi，密码为 666

正常情况
```text
用户名：dasi
密码：666
执行 SQL: SELECT * FROM users WHERE username = 'dasi' AND passwd   = '666'
登录成功，欢迎 dasi

用户名：dasi
密码：999
执行 SQL: SELECT * FROM users WHERE username = 'dasi' AND passwd   = '999'
用户名或密码错误
```

SQL 注入
```text
用户名：whatever
密码：whatever' OR '1' = '1
执行 SQL: SELECT * FROM users WHERE username = 'whatever' AND passwd   = 'whatever' OR '1' = '1'
登录成功，欢迎 dasi
```

## PreparedStatement

PreparedStatement 实际上是继承 Statement 的子接口，相比于 Statement 的优点
- 预编译：在数据库端对 SQL 语句做一次解析、校验和执行计划生成，后续执行只需绑定新参数即可，性能更好
- 防止 SQL 注入：所有用户输入都通过 ? 占位符绑定，不会被当作 SQL 语句的一部分拼接执行
- 可重用：同一个 PreparedStatement 对象可多次设置不同参数并执行，无需每次都重新构造 SQL 语句

构造的 sql 语句：需要输入的字段用 ? 代替，序号从 1 开始

常用 API
- void setXXX(int parameterIndex, XXX x)：绑定类型
- void clearParameters()：清除之前所有已设置的参数
- ResultSet executeQuery()：执行 SELECT，返回查询结果 
- int executeUpdate()：执行 INSERT/UPDATE/DELETE/CREATE/DROP，返回受影响行数 
- boolean execute()：通用执行
  - 返回 true 则可调用 getResultSet() 取结果
  - 返回 false 则可调用 getUpdateCount() 取更新计数
- void addBatch()：将当前已绑定参数的 SQL 加入批处理
- int[] executeBatch()：批量执行所有已添加的批处理，返回每条执行结果
- void clearBatch()：清空批处理列表
- void close() / boolean isClosed()：关闭此 PreparedStatement 或检查是否已关闭

## 事务

事务要么全部成功提交，要么全部失败回滚，以下 API 都属于 Connection

- void setAutoCommit(boolean autoCommit)：开启或关闭自动提交模式
- boolean getAutoCommit()：查看当前自动提交模式
- void commit()：提交当前事务 
- void rollback()：回滚当前事务自上次提交
- Savepoint setSavepoint()：设置事务保存点
- void rollback(Savepoint savepoint)：回滚到指定保存点
- void releaseSavepoint(Savepoint savepoint)：释放保存点
- int getTransactionIsolation()：获取事务隔离级别
- void setTransactionIsolation(int level)：设置事务隔离级别
  - TRANSACTION_READ_UNCOMMITTED：允许脏读、允许不可重复读、允许幻读
  - TRANSACTION_READ_COMMITTED：禁止脏读、允许不可重复读、允许幻读
  - TRANSACTION_REPEATABLE_READ：禁止脏读、禁止不可重复读、允许幻读
  - TRANSACTION_SERIALIZABLE：禁止脏读、禁止不可重复读、禁止幻读

```java
try {
    connection.setAutoCommit(false);
    // 数据库处理...
    connection.commit();
} catch (Exception e) {
    connection.rollback();    
}
...
```
  
## 批处理

批处理是将多条 SQL 语句合并到一次网络往返中执行的机制，能够显著减少客户端与数据库服务器之间的交互次数，从而提高大量插入／更新／删除操作的性能

以下 API 都属于 Statement/PreparedStatement

- void addBatch(String sql)：将指定的 SQL 加入批处理
- void addBatch()：将预编译的 SQL 加入批处理
- int[] executeBatch()：批量执行已加入的 SQL，返回每条语句的更新计数数组
- void clearBatch()：清空当前批处理中的所有 SQL

```java
for (int i = 1; i <= 5000; i++) {
    ps.setString(...);
    ps.addBatch();
    if (i % 1000 == 0) {
        ps.executeBatch();
        ps.clearBatch();
    }
}
```

## 连接池

什么是连接池：预先创建多个数据库连接并缓存起来的组件，当应用需要数据库连接时，从池里“借用”一个而不是重新建立，使用完毕后再归还给池而不是关闭
- 建立一个 JDBC 连接通常需要数十到数百毫秒，批量请求时如果每次都新建连接，开销巨大
- 池可以限制最大连接数，防止因过多并发连接而耗尽数据库资源
- 应用代码不用关心连接的创建、销毁和异常回收，只需借用/归还即可

常用方法
- 初始化
  - void setInitialPoolSize(int size)：在连接池启动时预先创建并缓存的连接数
  - void setMinPoolSize(int size)：连接池中始终保持的最小空闲连接数
  - void setMaxPoolSize(int size)：连接池允许分配的最大连接数，超过此数量时，借用连接会阻塞或超时
  - void setMaxIdleTime(int seconds)：空闲连接在池中保留的最长时间（秒），超过时会被回收并关闭
  - void setCheckoutTimeout(int ms)：从池中借用连接时的最大等待时长（毫秒），超出会抛出超时异常
- 状态监控
  - int getNumBusyConnectionsDefaultUser()：当前已借出的活动连接数
  - int getNumIdleConnectionsDefaultUser()：当前未借出的连接数
  - int getNumConnectionsDefaultUser()：当前池中总连接数
- 连接监测
  - boolean isValid(int timeout)：检测一个物理连接在指定超时时间内是否还能正常工作
  - void setValidationQuery(String sql)：指定一个简单的 SQL 用来检测连接有效性
  - void setTestConnectionOnCheckout(boolean flag)：在借出连接前执行验证查询，保证返回给应用的连接都是可用的
  - void setTestConnectionOnCheckin(boolean flag)：在归还连接时执行验证查询，确保池中的连接长期健康
  - void setIdleConnectionTestPeriod(int seconds)：设定一个周期（秒），让连接池在后台定时对所有空闲连接执行验证查询
- 销毁资源
  - void close()：释放所有空闲与活动连接，并清理内部资源

> 惰性初始化：系统不知道你是否真的要使用资源，因此池子并不会在 ComboPooledDataSource 构造时就马上建好 3 个连接，而是在第一次真正向它请求连接的时候，才一次性按初始化的数量创建那么多连接

## DBUtils

QueryRunner 是 Apache Commons DBUtils 中的核心类，用来简化 JDBC 操作
- 自动获取并关闭 Connection、PreparedStatement 和 ResultSet，避免大量手写 try-catch
- 更方便地设置 SQL 参数，并且直接返回 Java 对象
- 支持将同一条带参数的 SQL 与多组参数打包，批量执行

ResultSetHandler<T> 是用来将 ResultSet 转换成任意 Java 对象的核心接口
- BeanHandler<T>：把 ResultSet 的第一行映射为一个 JavaBean
- BeanListHandler<T>：把整个结果集的每一行都映射成一个 Bean，返回 Bean 组成的 List<T>
- MapHandler：取结果集的第一行，返回 Map<String,Object>，Key = 列标签，Value = 列值
- MapListHandler：把所有行都做 MapHandler，返回 List<Map<String,Object>>
- ScalarHandler<T>：返回第一行的第一列值。常用于 COUNT(*)、聚合或获取单个标量值
- ColumnListHandler<T>：返回某一列的所有值为一个 List<T>

Bean：用来承载一行查询结果的类，通常与表对应，要求
- 必须有一个 public 的无参构造函数
- 属性名与列名必须一一对应
- 所有要映射的字段都必须声明为 private
- 对应每个属性有标准的 public setter/getter
- 如果 Bean 中有额外的属性，而 SQL 并不返回对应列，DBUtils 会自动跳过，不会报错
- 映射时大小写不敏感，ID、id、Id 都能对应 setId()

常用方法：
- QueryRunner(DataSource)：自动绑定连接池中的一个连接
- int update(String sql, Object... params)：执行一条带占位符的 DML/DDL，params 按顺序填充占位符，返回受影响行数
- int[] batch(String sql, Object[][] params)：批量执行同一条带参 SQL，同时传递一个二维数组提供多组参数
- <T> T query(String sql, ResultSetHandler<T> rsh, Object... params)：执行 SELECT 查询，并将结果交给 ResultSetHandler 去处理
- void fillStatement(PreparedStatement ps, Object... params)：将可变参数 params 按顺序绑定到给定的 PreparedStatement 上，然后就可以手动调用 ps 执行，实际上用于重写来实现额外功能

