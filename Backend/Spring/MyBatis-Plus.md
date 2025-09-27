# MyBatis-Plus



* [MyBatis-Plus](#mybatis-plus)
   * [介绍](#介绍)
      * [增强](#增强)
      * [依赖](#依赖)
      * [分页机制](#分页机制)
   * [基于 Mapper 的 API](#基于-mapper-的-api)
      * [BaseMapper](#basemapper)
      * [查](#查)
      * [增](#增)
      * [删](#删)
      * [改](#改)
      * [分页查](#分页查)
   * [基于 Service 的 API](#基于-service-的-api)
      * [IService](#iservice)
      * [查](#查)
      * [增](#增)
      * [删](#删)
      * [改](#改)
      * [分页查](#分页查)
   * [条件构造器 Wrapper](#条件构造器-wrapper)
      * [实现类](#实现类)
      * [条件方法](#条件方法)
      * [使用](#使用)
   * [实体类注解](#实体类注解)
      * [@TableName](#tablename)
      * [@TableId](#tableid)
      * [@TableField](#tablefield)
      * [@TableLogic](#tablelogic)
      * [@Version](#version)
   * [MyBatisX](#mybatisx)



## 介绍

### 增强

MyBatisPlus 简称 MP 是基于 MyBatis 的增强工具，在 MyBatis 的基础上只做增强不做改变，旨在简化开发、提高效率

- 无需大量写 XML，可以自动生成单表的 CRUD 方法
- 支持 Lambda 形式调用，提供丰富的条件拼接方式
- 内置代码生成器，是全自动 ORM 框架，可以快速生成各层代码
- 自带分页插件，开发者无需关注具体操作
- 可以输出执行的 SQL 以及其耗时，方便调试优化

### 依赖

```xml
<dependency>
    <groupId>com.baomidou</groupId>
    <artifactId>mybatis-plus-spring-boot3-starter</artifactId>
    <version>3.5.12</version>
</dependency>
<dependency>
    <groupId>com.baomidou</groupId>
    <artifactId>mybatis-plus-extension</artifactId>
    <version>3.5.12</version>
</dependency>
<dependency>
    <groupId>com.baomidou</groupId>
    <artifactId>mybatis-plus-jsqlparser</artifactId>
    <version>3.5.12</version>
</dependency>
```

### 分页机制

MyBatis-Plus 的分页机制本质上就是基于 MyBatis-Plus 的**拦截器**实现的，所以在使用之前需要在 Main 函数中往 IoC 容器添加 MyBatis 的插件容器 `MybatisPlusInterceptor`，然后往这个容器里面注册分页的拦截器 `PaginationInnerInterceptor`，它会拦截 SQL 执行过程并自动根据分页要求加上 LIMIT 子句

```java
@MapperScan("com.dasi.mapper")
@SpringBootApplication
public class Main {
    public static void main(String[] args) {
        SpringApplication.run(Main.class, args);
    }

  	// 需要注册为 Bean 提供给 IoC 容器自动使用
    @Bean
    public MybatisPlusInterceptor mybatisPlusInterceptor() {
        // 配置 MyBatis-Plus 的插件容器，其中可以添加多个内部拦截器
        MybatisPlusInterceptor mybatisPlusInterceptor = new MybatisPlusInterceptor();
      	// 添加分页插件，指定数据库类型为 MySQL
        mybatisPlusInterceptor.addInnerInterceptor(new PaginationInnerInterceptor(DbType.MYSQL));
        return mybatisPlusInterceptor;
    }
}
```



## 基于 Mapper 的 API

### BaseMapper

一般场景下需要写好 Mapper 接口中的抽象方法，然后完成 XML 文件中的 SQL 语句映射，现在只需要**将 Mapper 接口类继承自 MyBatis-Plus 提供的通用 Mapper 接口 BaseMapper\<T> （泛型传递数据库表对应的实体类）**，就可以省略基本 CRUD 方法的编写和 SQL 语句的映射，直接注入 Mapper 对象调用内置的方法即可

```java
public interface EmployeeMapper extends BaseMapper<Employee> {}
```

### 查

```java
// 根据主键查询单条记录
T selectById(Serializable id);

// 根据主键集合批量查询记录
List<T> selectBatchIds(@Param(Constants.COLLECTION) Collection<? extends Serializable> idList);

// 传递 Map 进行等值查询，其中 key 是数据库字段名，value 是匹配值
List<T> selectByMap(@Param(Constants.COLUMN_MAP) Map<String, Object> columnMap);

// 根据条件构造器查询单条记录
T selectOne(@Param(Constants.WRAPPER) Wrapper<T> queryWrapper);

// 根据条件构造器查询记录列表
List<T> selectList(@Param(Constants.WRAPPER) Wrapper<T> queryWrapper);
```

### 增

```java
// 传入对象插入一条记录
int insert(T entity);
```

### 删

```java
// 传递主键删除一条记录
int deleteById(Serializable id);

// 传递 Map 进行等值删除，其中 key 是数据库字段名，value 是匹配值
int deleteByMap(@Param(Constants.COLUMN_MAP) Map<String, Object> columnMap);

// 根据条件构造器删除
int delete(@Param(Constants.WRAPPER) Wrapper<T> wrapper);

// 根据主键集合批量删除
int deleteBatchIds(@Param(Constants.COLLECTION) Collection<? extends Serializable> idList);
```

### 改

```java
// 根据主键修改一条记录，只有不为 null 的字段会被更新
int updateById(@Param(Constants.ENTITY) T entity);

// 根据条件构造器修改
int update(@Param(Constants.ENTITY) T entity,
           @Param(Constants.WRAPPER) Wrapper<T> updateWrapper);
```

### 分页查

```java
// 条件分页查询
IPage<T> selectPage(IPage<T> page, @Param(Constants.WRAPPER) Wrapper<T> queryWrapper);
```



## 基于 Service 的 API

### IService

一般场景下，后端逻辑是控制层方法调用业务层方法调用持久层方法，而在业务层方法中如果前后没有增强逻辑，只是返回调用持久层方法的结果时，可以直接**让 Service 接口继承 MyBatis-Plus 提供的通用接口 IService\<T> ，并在实现类中继承 MyBatis 写好的 ServiceImpl<M, T>（其中 M 是实体类对应的 Mapper 接口，T 是数据库表对应的实体类）**，就可以直接在业务层注入 Service 对象调用内置方法

```java
// 业务层的接口
public interface EmployeeService extends IService<Employee> {}

// 业务层的实现类
@Service
public class EmployeeServiceImpl extends ServiceImpl<EmployeeMapper, Employee> implements EmployeeService {}
```

### 查

```java
// 根据主键查询
T getById(Serializable id);

// 根据主键集合查询
List<T> listByIds(Collection<? extends Serializable> idList);

// 根据条件构造器查询单条记录
T getOne(Wrapper<T> queryWrapper);

// 查询所有记录
List<T> list();

// 根据条件构造器查询列表
List<T> list(Wrapper<T> queryWrapper);
```

### 增

```java
// 插入一条记录
boolean save(T entity);

// 批量插入记录
boolean saveBatch(Collection<T> entityList);

// 批量插入或更新（主键判断存在则更新，不存在则插入）
boolean saveOrUpdateBatch(Collection<T> entityList);
```

### 删

```java
// 根据主键删除
boolean removeById(Serializable id);

// 根据条件构造器删除
boolean remove(Wrapper<T> queryWrapper);

// 根据主键集合批量删除
boolean removeByIds(Collection<? extends Serializable> idList);

// 根据 Map 条件删除，其中 key 是数据库字段名，value 是匹配值
boolean removeByMap(Map<String, Object> columnMap);
```

### 改

```java
// 根据主键更新
boolean updateById(T entity);

// 根据条件构造器和传入实例更新
boolean update(T entity, Wrapper<T> updateWrapper);

// 根据实例集合批量更新
boolean updateBatchById(Collection<T> entityList);
```

### 分页查

```java
// 条件分页查询
IPage<T> page(IPage<T> page, Wrapper<T> queryWrapper);
```



## 条件构造器 Wrapper

### 实现类

Wrapper 就是用来封装 SQL 语句的工具类，本质上就是**提供了一种面向对象的方式去拼接 SQL 的条件语句和更新语句**，而省略了在 XML 文件编写的过程

| **构造器类**            | **特点**                              |
| ----------------------- | ------------------------------------- |
| QueryWrapper\<T>        | 构建查询条件，支持链式调用            |
| UpdateWrapper\<T>       | 构建更新条件，支持链式调用和 set 更新 |
| LambdaUpdateWrapper\<T> | 更新条件构造器，字段使用**方法引用**  |
| LambdaQueryWrapper\<T>  | 查询条件构造器，字段使用**方法引用**  |
| AbstractWrapper         | 基础类，一般不直接使用                |

### 条件方法

| **方法**                    | **作用**             |
| --------------------------- | -------------------- |
| eq                          | 等于（=）            |
| ne                          | 不等于（<>）         |
| gt                          | 大于（>）            |
| ge                          | 大于等于（>=）       |
| lt                          | 小于（<）            |
| le                          | 小于等于（<=）       |
| between                     | BETWEEN 范围查询     |
| like / likeLeft / likeRight | 模糊查询             |
| in / notIn                  | IN 查询              |
| isNull / isNotNull          | 判断 NULL            |
| orderByAsc / orderByDesc    | 排序                 |
| set                         | 设置某个字段为固定值 |
| setSql                      | 设置某个字段为计算值 |

### 使用

筛选条件：名字里有字符 a，薪水在 5000 和 10000 之间的全部员工

```java
QueryWrapper<Employee> queryWrapper = new QueryWrapper<>();
queryWrapper.like("emp_name", "a")
  					.between("emp_salary", 3000.0, 9999.0);
List<Employee> employees = employeeMapper.selectList(queryWrapper);
```

条件筛选：区别在于是根据逻辑条件来判断是否应该把筛选条件拼接到 SQL 中

```java
// 假设传入 name 和 flag 变量
QueryWrapper<Employee> queryWrapper = new QueryWrapper<>();
queryWrapper
  // 只有 name 不为空时才会拼接 emp_name like 'a'
  .like(name != null, "emp_name", "a")
	// 只有 flag 为 true 时才会拼接 emp_salary between 3000.0 and 9999.0
	.between(flag, "emp_salary", 3000.0, 9999.0);
List<Employee> employees = employeeMapper.selectList(queryWrapper);
```

更新：名字不为空，薪水小于等于 5000 的全部员工，将名字变为 poor 并将薪水提升 20%，最后按照主键降序输出

```java
UpdateWrapper<Employee> updateWrapper = new UpdateWrapper<>();
updateWrapper.isNotNull("emp_name")
             .le("emp_salary", 5000.0)
             .set("emp_name", "poor")
             .setSql("emp_salary = emp_salary * 1.2")
             .orderByDesc("emp_id");
int rows = employeeMapper.update(null, updateWrapper);
```

> 上述使用有一个很明显的弊端，那就是需要填写数据库表中的列名，没有代码提示，而且需要反复对照数据库来进行确认

Lambda 的方式**传递的是 Java 实体类的 Getter 方法引用，MyBatis-Plus 会通过反射先解析成实体字段名，再结合实体类上的注解映射到实际的数据库列名**

- 不需要手写 SQL 列名，有代码自动补全，降低出错率
- 如果后续数据库列名或 Java 属性名发生变化，只需要在实体类上修改注解，其他地方不需要任何改动
- 写法错误会在编译期直接报错，而不是运行时才发现

```java
LambdaQueryWrapper<Employee> lambdaQueryWrapper = new LambdaQueryWrapper<>();
lambdaQueryWrapper.like(Employee::getEmpName, "d")
      						.between(Employee::getEmpSalary, 3000.0, 9999.0);
List<Employee> employees = employeeMapper.selectList(lambdaQueryWrapper);
```



## 实体类注解

### @TableName

指定实体类对应的数据库表名

### @TableId

指定主键字段对应的数据库列名，其中 type 属性指示主键生成策略

- IdType.AUTO：自增主键
- IdType.ASSIGN_ID：雪花算法，生成的主键是 LONG/BIGINT 类型
- IdType.ASSIGN_UUID：UUID 算法，生成的主键是字符串类型

### @TableField

指定普通字段对应的数据库列名，其中 exist 属性指示当前字段是否参与 SQL 操作，即是否参与数据库表列名的映射

### @TableLogic

指定当前字段是否作为**逻辑删除**的标志，即不真正从数据库删除记录，而是通过更新一个标志位字段表示已删除，其中 value 设置未删除时的值（默认0），delvalue 设置删除时的值（默认1）

- 在执行查询和删除操作时自动加上 `WHERE is_deleted = 0`

- 在执行删除操作时会自动加上 `SET is_deleted = 1`

### @Version

自动开启当前行的版本号记录，用于实现 MySQL 的乐观锁，防止并发更新时数据被覆盖，如果在更新时检查到版本不一致会更新失败

- 不适用于 wrapper.set 单独传值的方式，因为乐观锁依赖于实体对象的 version 字段来自动生成

- 在执行更新操作时会自动加上 `SET version = version + 1 WHERE version = ?`

- 需要在 Main 中的 MyBatis 插件容器中注册乐观锁插件

    ```java
    MybatisPlusInterceptor interceptor = new MybatisPlusInterceptor();
    interceptor.addInnerInterceptor(new OptimisticLockerInnerInterceptor());
    ```



## MyBatisX

1. 在 IDEA 的 Plugins 下载安装 MyBatisX
2. 打开右侧 `Database` 工具窗口 → 点击 `+` → 选择 `MySQL`
    - **Host**: `localhost`
    - **Port**: `3306`
    - **User/Password**: 数据库账号密码
3. 选择数据库 → 展开表 → 右键表名 → 选择 `MyBatisX-Generator`
4. 基础配置
    - basename：包的根路径 `com.dasi`
    - basepath：包的存储路径 `src/main/java`
    - relative package：实体类的包相对路径 `pojo`
    - encoding：字符编码方式 `UTF-8`
    - ignore xxx prefix/suffix：忽略表和字段的前缀/后缀 `t_, sys_`
5. 模版配置
    - annotation：选择 MyBatis-Plus 3（生成 `@TableName` 注解）
    - options：选择 Lombok 和 Model（生成 `@Data` 注解）
    - template：选择 MyBatis-Plus 3（生成继承 `BaseMapper` 的接口）
6. 进入自动生成的 mapper 接口 → 编写 MyBatisX 提供的方法 → 点击 `Option +。Enter` → 选择 `Generate MyBatis Sql` → 会自动在对应的 Mapper XML 文件中生成 SQL 映射标签