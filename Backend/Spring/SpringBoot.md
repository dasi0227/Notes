# SpringBoot



## 使用

### 概念

SpringBoot 是 SpringFramework 的升级版和扩展，目的是**用最少的配置、最快的速度启动一个 Spring 项目**，帮助开发员**省掉了传统的 xml 配置、依赖整合和 Servlet 配置工作**

- **自动配置**：根据引入的依赖，SpringBoot 会自动生成常用的 Bean 和相关配置类
- **内嵌 Web 服务器**：自带 Tomcat，不需要部署到外部容器
- **零 XML 配置**：通过注解可以完成一切 xml 配置
- **统一依赖管理**：只需要使用 **starter** 依赖，就可以一次性引入所需依赖及版本，不用手动对齐版本号
- **一键启动**：入口是一个 main() 函数，启动项目就像运行程序一样简单
- **多环境配置**：可以有多个配置文件，手动使用 `spring.profiles.active` 属性手动指定使用哪个配置文件

### 依赖

在 `pom.xml` 中指定 SpringBoot 父项目，则会激动继承一系列默认配置和依赖管理

```xml
<parent>
    <groupId>org.springframework.boot</groupId>
    <artifactId>spring-boot-starter-parent</artifactId>
    <version>3.5.3</version>
</parent>
```

### 启动

声明一个 **Main** 类，放到**最外层包**，并添加上 **@SpringBootApplication** 注解，运行 Main 就相当于启动项目

```java
@SpringBootApplication
public class Main {
    public static void main(String[] args) {
        SpringApplication.run(Main.class, args);
    }
}
```

### 配置

SpringBoot 的配置文件主要是设置应用程序的关键参数，主要用于配制项目端口、应用名、日志级别、数据库连接信息以及第三方服务参数，**SpringBoot 已经提供了一些固定的键值来修改一些关键参数，同时也支持自定义键值，但是不能重名，**同时主配置文件名必须为以下两种格式

-  `application.properties` ：key 和 value之间只有一个等号

    ```properties
    # 服务器基础信息
    server.port=8080
    server.servlet.context-path=/app
    
    # 自定义字段
    dasi.name=wyw
    dasi.age=22
    dasi.scores=100,89,91
    ```
    
- `application.yaml`：key 和 value之间必须有空格

    ```yaml
    # 服务器基础信息
    server:
      port: 8080
      servlet:
        context-path: /app
    
    # 自定义字段
    dasi:
    	name: wyw
    	age: 22
    	score:
    		- 100
    		- 89
    		- 91
    ```

### 读取

> 使用预先设置好的字段，SpringBoot 会自动读取，这里主要是指自定义字段的读取

**@Value**：直接将配置文件中的某个值注入到字段里

- 每个字段都需要写注解
- 无法给集合类型赋值，除非手动使用 SpEL 分隔字符串

```java
public class User {

    @Value("${user.dasi.name}")
    private String name;

    @Value("${user.dasi.age}")
    private Integer age;

    @Value("#{'${user.dasi.salary}'.split(',')}")
    private List<Integer> salary;
}
```

**@ConfigurationProperties**：将配置文件中的一组属性批量绑定到 Java Bean 中

- 只要在注解指定前缀，对应的值会自动注入到同名属性中
- 可以直接给集合类型赋值，但是需要加上 Lombok 的 @Data 注解

```java
@Data
@ConfigurationProperties(prefix = "user.dasi")
public class User {
    private String name;
    private Integer age;
    private List<Integer> scores;
}
```

### 打包

**传统项目**：将生成的 .war 容器放到 Tomcat 容器的 `webapps/` 目录，然后使用 `startup.sh`，容器会自动解压 .war 并运行项目

**SpringBoot 项目**：使用 Maven 的 `package` 的脚本，自动打包生成可执行的 `.jar` 文件，在终端直接使用 `java -jar [-配置=值] xxx.jar` 即可运行项目

- `--server.port`：修改启动端口
- `--server.servlet.context-path`：修改项目的上下文路径
- `--spring.profiles.active`：指定运行环境 xxx，会使用对应的的 `application-xxx.yaml` 配置文件

```xml
<build>
  <plugins>
      <plugin>
          <groupId>org.springframework.boot</groupId>
          <artifactId>spring-boot-maven-plugin</artifactId>
      </plugin>
  </plugins>
</build>
```



## 整合

### 整合 SpringMVC

添加依赖

```xml
<dependency>
    <groupId>org.springframework.boot</groupId>
    <artifactId>spring-boot-starter-web</artifactId>
</dependency>
```

进行配置

```yaml
spring:
  mvc:
    view:
      prefix: /WEB-INF/views/               # 设置视图文件的前缀
      suffix: .html                         # 设置视图文件的后缀
    static-path-pattern: /static/**         # 设置哪些 URL 会走静态资源处理机制
    servlet:
      path: /	                            	# 设置 DispatcherServlet 的映射路径
  web:
    resources:
      static-locations: classpath:/static/  # 设置静态资源在项目中的位置
      
# localhost:8080/app/static/login.html 会映射到 resources/static/login.html
# http://localhost:8080/app/enter 会映射到 resources/WEB-INF/views/login.html
```

### 整合 Druid

添加依赖

```xml
<dependency>
    <groupId>com.alibaba</groupId>
    <artifactId>druid-spring-boot-3-starter</artifactId>
    <version>1.2.25</version>
</dependency>
<dependency>
    <groupId>org.springframework.boot</groupId>
    <artifactId>spring-boot-starter-jdbc</artifactId>
</dependency>
<dependency>
    <groupId>com.mysql</groupId>
    <artifactId>mysql-connector-j</artifactId>
    <version>8.2.0</version>
</dependency>
```

进行配置

```yaml
spring:
  datasource:
    type: com.alibaba.druid.pool.DruidDataSource
    druid:
      # 基础配置
      url: jdbc:mysql://localhost:3306/mybatis
      username: root
      password: jason2004
      driver-class-name: com.mysql.cj.jdbc.Driver
      # 初始化连接数量
      initial-size: 5
      # 最小空闲连接数量
      min-idle: 5
      # 最大连接数量
      max-active: 20
      # 最长等待时间
      max-wait: 60000
      # 空闲时检测连接是否有效
      test-while-idle: true
      # 空闲连接检测的间隔
      time-between-eviction-runs-millis: 60000
      # 一个连接在连接池中保持空闲而不被驱逐的最小时间
      min-evictable-idle-time-millis: 30000
      # 检测连接是否有效的 SQL 语句
      validation-query: select 1
      # 借出连接时是否检测有效性
      test-on-borrow: false
      # 归还连接时是否检测有效性
      test-on-return: false
      # 是否缓存 PreparedStatement
      pool-prepared-statements: false
      # 每个连接最多缓存多少个 PreparedStatement（-1 表示无限制）
      max-pool-prepared-statement-per-connection-size: -1
      # 是否开启全局统计
      use-global-data-source-stat: true
```

### 整合 AOP

添加依赖

```xml
<dependency>
    <groupId>org.springframework.boot</groupId>
    <artifactId>spring-boot-starter-aop</artifactId>
</dependency>
```

直接使用

```java
@Component
@Aspect
@Order(5)
public class LogAdvice {

    @Before("execution(* com.dasi.service.*.*(..))")
    public void beforeMethod(JoinPoint joinPoint) {
        String className = joinPoint.getTarget().getClass().getSimpleName();
        String methodName = joinPoint.getSignature().getName();
        System.out.println("【Before】Class: " + className + ", method: " + methodName);
    }

    @After("execution(* com..service.*.*(..))")
    public void afterMethod(JoinPoint joinPoint) {
        String className = joinPoint.getTarget().getClass().getSimpleName();
        String methodName = joinPoint.getSignature().getName();
        System.out.println("【After】Class: " + className + ", method: " + methodName);
    }
}
```

### 整合 MyBatis

添加依赖

```xml
<dependency>
    <groupId>org.mybatis.spring.boot</groupId>
    <artifactId>mybatis-spring-boot-starter</artifactId>
    <version>3.0.3</version>
</dependency>
```

进行配置

```yaml
mybatis:
	# 指定映射配置文件路径
  mapper-locations: classpath:/mappers/*.xml
  # 指定实体类所在包名，自动生成别名
  type-aliases-package: com.dasi.pojo
  configuration:
  	# 开启下划线转驼峰命名
    map-underscore-to-camel-case: true
    # 对所有列进行自动映射
    auto-mapping-behavior: full
    # 使用 SLF4J 记录 SQL 日志
    log-impl: org.apache.ibatis.logging.slf4j.Slf4jImpl
```

指定 mapper 接口

```java
@MapperScan("com.dasi.mapper")
@SpringBootApplication
public class Main {
    public static void main(String[] args) {
        SpringApplication.run(Main.class, args);
    }
}
```

