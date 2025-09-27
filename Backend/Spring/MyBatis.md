# MyBatis



   * [概述](#概述)
   * [Mapper](#mapper)
      * [定义](#定义)
      * [映射流程](#映射流程)
      * [iBatis](#ibatis)
   * [基本使用](#基本使用)
      * [mybatis-config.xml](#mybatis-configxml)
         * [environments](#environments)
         * [mappers](#mappers)
         * [settings](#settings)
      * [传递值](#传递值)
         * [方式](#方式)
         * [类型](#类型)
      * [返回值](#返回值)
         * [默认别名](#默认别名)
         * [类型别名](#类型别名)
         * [字段别名](#字段别名)
         * [集合类型](#集合类型)
         * [获取自增长主键](#获取自增长主键)
         * [selectKey 标签](#selectkey-标签)
   * [多表映射](#多表映射)
      * [定义](#定义)
      * [一对一映射](#一对一映射)
      * [一对多映射](#一对多映射)
      * [自动映射](#自动映射)
   * [动态语句](#动态语句)
      * [\<if>](#if)
      * [\<where>](#where)
      * [\<set>](#set)
      * [\<choose>](#choose)
      * [\<sql>](#sql)
   * [批量执行](#批量执行)
      * [Executor](#executor)
      * [\<foreach>](#foreach)
   * [分页机制](#分页机制)
      * [MySQL 实现](#mysql-实现)
      * [PageHelper 插件实现](#pagehelper-插件实现)



## 概述

**ORM**（Object-Relational Mapping，对象关系映射）：是一种程序设计思想，目标是**把面向对象编程中的对象和关系型数据库中表建立自动映射关系，使得程序员可以像操作对象一样操作数据库**

**MyBatis** 是  Java 中专门负责持久层的框架，是 ORM 的一种实现方式，主要作用是**把 Java 方法与数据库的 SQL 语句**进行映射

- **半自动 ORM**：程序员手写 SQL，MaBatis 负责把 SQL 的结果自动封装为 Java 对象
- **代码分离**：SQL 可以写到 XML 映射文件和注解之中，使其与 Java 代码完全分离
- **参数绑定**：MyBatis 会自动把 Java 对象的属性值绑定到 SQL 语句的占位符，无需手动操作
- **动态 SQL**：可以使用标签，根据条件在运行时拼接 SQL 语句

| 对比     | JDBC                               | MyBatis                                 | Hibernate                               |
| -------- | ---------------------------------- | --------------------------------------- | --------------------------------------- |
| 本质     | 直接利用 JDBC 的 API               | 半自动 ORM 框架                         | 全自动 ORM 框架                         |
| SQL 编写 | 手写 SQL + 手动拼接参数            | 支持动态 SQL，参数动态绑定              | 框架生成 SQL                            |
| 特征     | 灵活度最高，但开发效率低、代码量大 | 保留 SQL 灵活性，并减少了 JDBC 重复劳动 | 开发效率高，但性能低、对 SQL 极其不敏感 |



## Mapper

### 定义

Mapper 指的是 **SQL 映射器**，将 Java 方法映射为 SQL 语句

- **实体**：用来承载数据库表的数据，是 Java 中存储一行数据的对象，没有业务逻辑，主要完成 getter/setter/toString 方法

    ```java
    public class Employee {
        private int id;
        private String name;
        private Double salary;
        // getter / setter / toString
    }
    ```

- **接口**：定义针对特定实体类的数据库操作对应的方法，不能有重载，主要声明方法名 + 参数类型 + 返回类型，不需要实现类（MyBatis 会通过动态代理自动创建）

    ```java
    public interface EmployeeMapper {
        Employee queryById(int id);
    }
    ```

- **映射配置文件**：写具体的 SQL 语句，将 SQL 和 Mapper 接口的抽象方法绑定

    - namespace 指定 Mapper 接口的全限定名
    - id 指定与 SQL 对应的 Mapper 接口 中的方法名
    - resultType 指定实体类的全限定名

    ```xml
    <!-- 文件名通常为 EmployeeMapper.xml -->
    <mapper namespace="com.dasi.mapper.EmployeeMapper">
        <select id="queryById" resultType="com.dasi.pojo.Employee">
            select emp_id as id, emp_name as name, emp_salary as salary
            from employee
            where emp_id = #{id}
        </select>
    </mapper>
    ```

- **全局配置文件**：告诉 MyBatis 映射配置文件的位置，数据库的连接信息，以及一些全局配置信息

    ```xml
    <!-- 文件名通常为 mybatis-config.xml -->
    <?xml version="1.0" encoding="UTF-8" ?>
    <!DOCTYPE configuration
            PUBLIC "-//mybatis.org//DTD Config 3.0//EN"
            "http://mybatis.org/dtd/mybatis-3-config.dtd">
    
    <configuration>
    
        <!-- 全局配置 -->
        <settings>
            <!-- 开启驼峰命名自动映射（user_name -> userName） -->
            <setting name="mapUnderscoreToCamelCase" value="true"/>
            <!-- 开启二级缓存 -->
            <setting name="cacheEnabled" value="true"/>
            <!-- 打印 SQL 到控制台 -->
            <setting name="logImpl" value="STDOUT_LOGGING"/>
        </settings>
    
        <!-- 配置数据库 -->
        <environments default="development">
            <environment id="development">
                <transactionManager type="JDBC"/>
                <dataSource type="POOLED">
                    <property name="driver" value="com.mysql.cj.jdbc.Driver"/>
                    <property name="url" value="jdbc:mysql://localhost:3306/mybatis"/>
                    <property name="username" value="root"/>
                    <property name="password" value="jason2004"/>
                </dataSource>
            </environment>
        </environments>
    
        <!-- Mapper 映射文件位置 -->
        <mappers>
            <mapper resource="mappers/EmployeeMapper.xml"/>
        </mappers>
    
    </configuration>
    ```

### 映射流程

1. 首先根据全局配置文件连接到数据库并进行一些初始化设置，然后获取到映射配置文件的位置
2. 利用动态代理获取映射接口的实现类
3. 调用实现类中的接口方法，然后在映射配置文件中：
    1. 找到 namespace 与映射接口一致的映射配置
    2. 找到 id 与方法名一致的 SQL 语句
4. 执行 SQL 语句，并将结果转换为 resultType 类型的对象返回

### iBatis

iBatis 是 MyBatis 的前身，它不需要创建 Mapper 接口，也不需要在 XML 中设置 namespace 属性，而是**利用 sqlMapClient 的 API 根据字符串 id 找到对应 SQL 语句**

- 字符串 ID 无法自动补全，容易拼错，而且只有到了运行才会报错
- 返回类型是 Object，需要强制类型转换目标类型，不安全
- 方法名和 SQL ID 没有任何关系
- SQL ID 没有隔离，而是全局共享，容易冲突

```java
User user = (User) sqlMapClient.queryForObject("getUserById", 1);
```

MyBatis 最大的更新在于引入了 Mapper 接口 和 namespace，**利用 sqlSession.getMapper() 自动生成接口实现类，再通过接口的全限定名和方法名找到对应的 SQL**

- 有代码补全，错误可在编译期发现
- 返回类型就是目标类型，不需要强制类型转换
- 方法名与 XML 中 id 是完全一致的
- SQL ID 根据 namespace 进行了分组，在不同组间可以重名，更加灵活

```java
UserMapper userMapper = sqlSession.getMapper(UserMapper.class);
User user = userMapper.getUser(1);
```



## 基本使用

### mybatis-config.xml

#### environments

配置多个数据库连接环境（如开发、测试、生产等）

- `<environments default="...">`：用 default 属性指定当前使用的环境 ID

- `<environment id="...">`：用 id 属性来标识一个特定的环境
- `<transactionManager type="...">`：用 type 属性来设置事务管理方式（JDBC 自动；MANAGED 手动）
- `<dataSource type="...">`：用 type 属性来设置数据库的连接信息（POOLED 使用连接池；UNPOOLED 不使用连接池）

#### mappers

告诉 MyBatis 去哪里找 SQL 映射文件，有以下几种方式

- `<mapper resource="mappers/XXX.xml"/>`：按照资源路径，只加载指定的 XML 文件
- `<mapper class="com.dasi.mapper.XXX"/>`：按照接口注解，只加载指定的接口
- `<package name="com.dasi.mapper"/>`：按照包扫描所以接口，适合一次性加载多个 XML 文件

#### settings

通过 `<setting name="..." value="..." />` 控制 MyBatis 的缓存策略、延迟加载、执行期类型等核心特性，一次性全局生效，所有映射器都会遵循

| name                     | value | 意义                                                         |
| ------------------------ | ----- | ------------------------------------------------------------ |
| mapUnderscoreToCamelCase | false | 是否自动将数据库下划线命名映射为驼峰命名，如 emp_name → empName |
| cacheEnabled             | true  | 是否开启全局二级缓存                                         |
| lazyLoadingEnabled       | false | 是否启用延迟加载，即关联对象在真的用到时才查询               |
| logImpl                  | /     | 指定日志实现类，常见的有 STDOUT_LOGGING、LOG4J2、SLF4J       |
| defaultStatementTimeout  | /     | 设置 SQL 执行的超时时间                                      |
| defaultExecutorType      | /     | 设置 SQL 的执行方式：SIMPLE 执行一次就创建一个 PS；REUSE 复用 PS；BATCH 缓存后批量处理 |

### 传递值

#### 方式

| 对比     | #{}                    | ${}                         |
| -------- | ---------------------- | --------------------------- |
| 替换方式 | 占位符 ?               | 字符串拼接                  |
| 性质     | 安全、可以自动类型转换 | 有 SQL 注入风险、统一字符串 |
| 场景     | 传递值                 | 传递表名、列名等 SQL 结构   |

#### 类型

传入单个简单类型 / 传入单个对象：直接利用 `#{key}`

```xml
<!-- 单个简单类型，直接利用变量名 -->
<select id="queryByCondition" resultType="com.dasi.pojo.Employee">
    SELECT emp_id, emp_name, emp_salary
    FROM employee
    WHERE emp_id = #{id}
</select> 

<!-- 单个对象，直接利用属性名 -->
<select id="queryByCondition" resultType="com.dasi.pojo.Employee">
    SELECT emp_id, emp_name, emp_salary
    FROM employee
    WHERE emp_name = #{name} AND emp_salary = #{salary}
</select>
```

传入多个简单类型：利用注解声明参数变量在 SQL 的名称

```java
public interface EmployeeMapper {
    Employee queryByNameAndSalary(
        @Param("name") String name,
        @Param("salary") Double salary
    );
}
```

传入多个简单类型：根据传递顺序使用默认设置好的名称

```xml
<!-- arg 从 0 开始 -->
<select id="queryByCondition" resultType="com.dasi.pojo.Employee">
    SELECT emp_id, emp_name, emp_salary
    FROM employee
    WHERE emp_name = #{arg0} AND emp_salary = #{arg1}
</select>

<!-- param 从 1 开始 -->
<select id="queryByCondition" resultType="com.dasi.pojo.Employee">
    SELECT emp_id, emp_name, emp_salary
    FROM employee
    WHERE emp_name = #{param1} AND emp_salary = #{param2}
</select>
```

传入 Map 类型：使用在集合中设置的键值

```java
// 接口定义：Employee queryByCondition(Map<String, Object> params);
Map<String, Object> params = new HashMap<>();
params.put("name", "Alice");
params.put("salary", 5000.0);
mapper.queryByCondition(params);
```

### 返回值

#### 默认别名

MyBatis 内置了一批常用 Java 类型的简写，可以在 resultType 直接使用，不需要写出完整的全限定名

- int→\_int, double→\_double, boolean→\_boolean
- Integer→int, Double→double, Boolean→boolean
- string→String, map→Map, list→List

#### 类型别名

单个注册，自定义别名

```xml
<typeAliases>
  <typeAlias type="com.dasi.pojo.Employee" alias="Emp"/>
</typeAliases>
```

包扫描，别名为首字母小写的类名

```xml
<typeAliases>
  <package name="com.dasi.pojo"/>
</typeAliases>
```

> 设置在 mybatis-config.xml

#### 字段别名

利用 MyBatis 提供的下划线变驼峰

```xml
<settings>
  <setting name="mapUnderscoreToCamelCase" value="true"/>
</settings>
```

手动在 SQL 中设置别名

```xml
<select id="selectById" resultType="com.dasi.pojo.Employee">
  SELECT emp_id as empId, emp_name as empName, emp_salary as empSalary
  FROM employee 
  WHERE emp_id = #{id}
</select>
```

利用标签设置映射关系：id 表示主键字段，result 表示普通字段；property 指定类的属性名，column 指定数据表的列名

```xml
<!-- 用法：<select id="selectById" resultMap="empResultMap"> -->

<resultMap id="empResultMap" type="com.dasi.pojo.Employee">
	<id property="empId" column="emp_id" />
  <result property="empName" column="emp_name" />
  <result property="empSalary" column="emp_salary" />
</resultMap>
```

> 设置在 XxxMapper.xml

#### 集合类型

单行 Map：设置返回类型为 map，会把数据封装为属性名和属性值

```xml
<!--
public interface EmpMapper {
  Map<String, Object> selectAsMap();
}
-->

<select id="selectAsMap" resultType="map">
  SELECT emp_id, emp_name, emp_salary FROM employee WHERE emp_id = #{id}
</select>
```

多行 Map：需要在接口处利用注解，**声明 Map 的键为数据表主键在 Java 中的名字**，设置 resultType 为实体类的类型而不是 map，会把数据封装为 id 和对象

```xml
<!--
public interface EmpMapper {
  @MapKey("empId")
  Map<Integer, Employee> selectAllAsMap();
}
-->

<select id="selectAllAsMap" resultType="com.dasi.pojo.Employee">
  SELECT emp_id, emp_name, emp_salary FROM employee
</select>
```

多行 List：设置 resultType 为实体类的类型而不是 list，会把数据封装为对象列表

```xml
<!--
public interface EmpMapper {
  List<Employee> selectAllAsList();
}
-->

<select id="selectAllAsList" resultType="com.dasi.pojo.Employee">
  SELECT emp_id, emp_name, emp_salary FROM employee
</select>
```

#### 获取自增长主键

当把主键交给数据库利用自增机制设置时，可以利用相关属性将 id 值反向赋给 Java 对象

- useGeneratedKeys：启用 JDBC 返回主键
- keyProperty：主键在 Java 对象的名字
- keyColumn：主键在数据表的名字

```xml
<insert id="insertEmp" useGeneratedKeys="true" keyProperty="empId" keyColumn="emp_id">
    INSERT employee(emp_name, emp_salary)
    VALUES (#{empName}, #{empSalary})
</insert>
```

#### selectKey 标签

在执行 \<insert> 语句**之前**或**之后**，可以额外执行一条通过 \<selectKey> 设置的 SQL 来获取值，并把它回填到 Java 对象的属性里

- order：与 \<insert> 语句的执行先后关系
- resultType：回填值的类型
- keyProperty：回填值在 Java 对象的名字
- keyColumn：回填值在数据表的名字（用于多列主键或列名与属性名不一致时）

```xml
<insert id="insertEmp">
    <selectKey order="BEFORE" resultType="string" keyProperty="empId">
        SELECT REPLACE(UUID(), '-', '')
    </selectKey>
    INSERT INTO employee(emp_id, emp_name, emp_salary)
    VALUES (#{empId}, #{empName}, #{empSalary})
</insert>
```



## 多表映射

### 定义

在数据库中是实现多个表的连接，在 Java 中就是实现对象之间的映射关系

- 一对一：对象的属性是另一个对象

    ```java
    class Student {
        private Integer orderId;
        private String orderName;
        private Customer customer; // 一个订单一个客户
    }
    ```

- 一对多；对象的属性是另一个对象的集合

    ```java
    class Order {
        private Integer customerId;
        private String customerName;
        private List<Order> orders; // 一个客户多个订单
    }
    ```

### 一对一映射

\<association>：告诉 MyBatis 当前属性是对象，需要通过关联表查询

- property：关联对象的名字
- javaType：关联对象的类型

```xml
<resultMap id="orderMap" type="com.dasi.pojo.Order">
  	<!-- 自身属性 -->
    <id column="order_id" property="orderId" />
    <result column="order_name" property="orderName" />
  
    <!-- 关联对象 -->
    <association property="customer" javaType="customer">
        <id column="customer_id" property="customerId" />
        <result column="customer_name" property="customerName" />
    </association>
</resultMap>

<!-- 必须用 resultMap 实现映射关系 -->
<select id="queryOrderById" resultMap="orderMap">
    SELECT * FROM t_order o JOIN t_customer c
    ON o.customer_id = c.customer_id
    WHERE o.order_id = #{id}
</select>
```

### 一对多映射

\<collection>：告诉 MyBatis 当前属性是对象列表，需要通过关联表查询

- property：关联对象的名字
- ofType：关联对象的类型

```xml
<resultMap id="customerMap" type="customer">
    <!-- 自身属性 -->
  	<id column="customer_id" property="customerId" />
    <result column="customer_name" property="customerName" />

  	<!-- 关联对象 -->
    <collection property="orders" ofType="order">
        <id column="order_id" property="orderId" />
        <result column="order_name" property="orderName" />
    </collection>
</resultMap>

<!-- 必须用 resultMap 实现映射关系 -->
<select id="queryOrderListById" resultMap="customerMap">
    SELECT * FROM t_order o
    JOIN t_customer c
    ON o.customer_id = c.customer_id
    WHERE o.customer_id = #{id}
</select>
```

### 自动映射

需要在 mybatis.config.xml 的 settings 中开启 **autoMappingBehavior**，但是无论是单层还是嵌套，**都需要有 \<id> 标签**

| 值      | 含义                                       | 场景                                             |
| ------- | ------------------------------------------ | ------------------------------------------------ |
| NONE    | 禁用自动映射，必须写 \<resultMap>          | 名称不一致，或者不满足驼峰式，需要自定义         |
| PARTIAL | 只映射单层列，且没有在 \<resultMap> 中出现 | 不适用于嵌套映射，比如 association 和 collection |
| FULL    | 映射所有列，即使在 \<resultMap> 中出现     | 适用于名称完全对应的情况                         |



## 动态语句

### \<if>

根据 test 属性设置的条件决定是否拼接某段 SQL，其中 test 里写的是 Java 表达式，用的是 Java 对象中的名称，但是存在以下两种典型错误

```xml
<select id="queryEmployee" resultType="com.dasi.pojo.Employee">
		SELECT * FROM employee
  	WHERE
    <if test="empName != null">
        emp_name = #{empName}
    </if>
    <if test="empSalary != null">
        AND emp_salary = #{empSalary}
    </if>
</select>
```

- 如果两个条件都不满足，那么 WHERE 关键字是多余的，SQL 语句错误
- 如果第一个条件不满足，第二个条件满足，那么 AND 关键字是多余的，SQL 语句错误

```xml
<update id="updateEmployee">
    UPDATE employee
    SET
    <if test="empName != null">
        emp_name = #{empName},
    </if>
    <if test="empSalary != null">
        emp_salary = #{empSalary}
    </if>
    WHERE emp_id = #{empId}
</update>
```

- 如果两个条件都不满足，那么就不存在 SET 项，SQL 语句错误
- 如果第一个条件满足，第二个条件不满足，那么逗号 , 是多余的，SQL 语句错误

### \<where>

专门处理 WHERE 的条件拼接，会自动加上 WHERE 关键字，同时会自动去掉开头多余的 AND / OR

- 如果两个条件都不满足，那么会自动去掉 WHERE 关键字，变为查全表
- 如果第一个条件不满足，第二个条件满足，那么会自动去掉 AND 关键字

```xml
<select id="queryEmployee" resultType="com.dasi.pojo.Employee">
		SELECT * FROM employee
  	<where>
  			<if test="empName != null">
      			AND emp_name = #{empName}
      	</if>
      	<if test="empSalary != null">
          	AND emp_salary = #{empSalary}
      	</if>
  	</where>
</select>
```

### \<set>

专门处理 SET 的条件赋值，会自动加上 SET 关键字，同时会自动去掉结尾多余的 ,

```xml
<update id="updateEmployee">
    UPDATE employee
    <set>
        <if test="empName != null">
            emp_name = #{empName},
        </if>
        <if test="empSalary != null">
            emp_salary = #{empSalary},
        </if>
    </set>
    WHERE emp_id = #{empId}
</update>
```

### \<choose>

专门处理条件选择和分支判断，相当于 Java 里面的 switch-case 结构，优先级按照 \<when> 标签的设置顺序，同时支持使用 \<otherwise> 标签设置默认选择

```xml
<!-- 先根据名字查，查不到再根据 id 查，还查不到就查全表 -->
<select id="selectChoose" resultType="employee">
    SELECT * FROM employee
    WHERE
    <choose>
        <when test="empName != null">
            emp_name = #{empName}
        </when>
        <when test="empSalary != null">
            emp_id = #{empId}
        </when>
        <otherwise>
            1 = 1
        </otherwise>
    </choose>
</select>

<!-- 只应该选择一种模式进行更新，而不是先满足第一个条件后更新后，又满足第二个条件继续更新 -->
<update id="updateChoose">
		UPDATE employee
  	SET
    <choose>
        <when test="empSalary <= 5000">
            emp_salary = emp_salary * 1.2
        </when>
        <when test="empSalary >= 10000">
            emp_salary = emp_salary * 0.8
        </when>
        <otherwise>
            emp_salary = emp_salary * 1.1
        </otherwise>
    </choose>
</update>
```

### \<sql>

定义 SQL 片段，利用 id 属性可以给 SQL 片段赋于一个名称，后续通过名称引用它

```xml
<sql id="SelectAllFromEmployee">
    SELECT * FROM employee
</sql>

<select id="selectAll" resultType="com.dasi.pojo.Employee">
  	<include refid="SelectAllFromEmployee"/>
  	WHERE emp_id = #{empId}
</select>
```



## 批量执行

### Executor

开启 sqlSession 的批量模式，把 SQL 语句和参数缓存起来，一次性发送，减少网络交互，是在 Java 层面的批量，不适合有返回值依赖的场景，即无法获得自增主键

- 需要在创建 sqlSession 的时候开启 `ExecutorType.BATCH`
- 需要手动调用 `flushStatements()` 发送对象

```java
try (SqlSession sqlSession = sqlSessionFactory.openSession(ExecutorType.BATCH)) {
    EmployeeMapper mapper = sqlSession.getMapper(EmployeeMapper.class);

    for (int i = 0; i < 1000; i++) {
        Employee emp = new Employee(null, "User" + i, 3000.0);
        mapper.insert(emp);
    }

    sqlSession.flushStatements();
    sqlSession.commit();
}
```

### \<foreach>

直接在 SQL 里利用 foreach 标签循环拼接多行数据，是在 SQL 层面的批量

- **collection**：要遍历的集合名，需要与 Mapper 设置的参数名一致，必须
- **item**：每次迭代的变量名，相当于 for 循环设置的局部变量，必须
- **open**：循环内容之前加的字符串，可选
- **separator**：循环内容的元素之间的分隔符，可选
- **close**：循环内容之后加的字符串，可选

批量查询 / 删除：利用 IN 关键字判断字段值是否在集合之中

```xml
<select id="queryBatch" resultType="employee">
    SELECT * FROM employee
    WHERE emp_id IN
    <foreach collection="ids" open="(" separator="," close=")" item="id">
        #{id}
    </foreach>
</select>

<delete id="deleteBatch">
    DELETE FROM employee
    WHERE emp_id IN
    <foreach collection="ids" open="(" separator="," close=")" item="id">
        #{id}
    </foreach>
</delete>
```

批量插入：利用 VALUES 关键字拼接一个个元组

```xml
<insert id="insertBatch">
    INSERT INTO employee (emp_id, emp_name, emp_salary)
    VALUES
    <foreach collection="employees" separator="," item="employee">
        (#{employee.empId}, #{employee.empName}, #{employee.empSalary})
    </foreach>
</insert>
```

批量更新：直接对整个 SQL 语句进行循环拼接

```xml
<update id="updateBatch">
    <foreach collection="employees" item="employee">
        UPDATE employee
        SET emp_name = #{employee.empName},
            emp_salary = #{employee.empSalary}
        WHERE emp_id = #{employee.empId};
    </foreach>
</update>
```



## 分页机制

### MySQL 实现

```sql
SELECT * FROM [tableName] ORDER BY [colKey] LIMIT [rowOffset] [rowNum]
```

- **colKey**：必须要有排序键，否则 MySQL 返回的结果**顺序不固定**
- **rowOffset**：表示跳过多少行
- **rowNum**：表示要获取多少行

### PageHelper 插件实现

首先需要在 pom.xml 中添加依赖，然后在 mybatis-config.xml 注册并配置插件

```xml
<plugins>
    <plugin interceptor="com.github.pagehelper.PageInterceptor">
        <property name="helperDialect" value="mysql" />
    </plugin>
</plugins>
```

1. 创建 PageHelper 对象，并且指定 pageNum 和 pageSize

    - rowOffset = (pageNum - 1) * pageSize

    - rowNum = pageSize

2. 创建 PageInfo 对象，构造函数中传入结果列表对象

    - getPages() / getTotal()：获取总页数和总行数
    - getPageNum() / getPageSize() / getSize()：获取当前页码、页大小、当前页大小（末尾页通常小于预先设置的页大小，页码从 1 开始）
    - getStartRow() / getEndRow()：获取第一条 / 最后一条记录的行号（从 1 开始）
    - isHasNextPage() / isHasLastPage()：是否有下 / 上一页
    - isIsFirstPage() / isIsLastPage()：是否是第一页 / 最后一页
    - getList()：获取当前页的数据列表，需要用 ArrayList 转换才可以不带元数据

```java
// 1. 获取代理对象
EmployeeMapper employeeMapper = sqlSession.getMapper(EmployeeMapper.class);
// 2. 获取查询结果
List<Employee> employees = employeeMapper.selectEmployeeByPage();
// 3. 创建 PageHelper 对象，设置页信息
PageHelper.startPage(1, 2);
// 4. 创建 PageInfo 对象，传入查询结果
PageInfo<Employee> pageInfo = new PageInfo<>(employees);
// 5. 调用 API 获取元数据
System.out.println("pages：" + pageInfo.getPages());
System.out.println("rows：" + pageInfo.getTotal());
System.out.println("pageSize：" + pageInfo.getPageSize());
System.out.println("pageNum：" + pageInfo.getPageNum());
System.out.println("isNext：" + pageInfo.isHasNextPage());
System.out.println("isLast：" + pageInfo.isHasPreviousPage());
System.out.println("List：" + new ArrayList<>(pageInfo.getList()));
```

> 不能把两个查询结果放到一个 PageInfo