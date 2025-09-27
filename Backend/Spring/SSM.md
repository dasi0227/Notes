# SSM



   * [概念](#概念)
      * [整合](#整合)
      * [容器](#容器)
   * [依赖](#依赖)
      * [SpringFramework](#springframework)
      * [SpringMVC](#springmvc)
      * [MyBatis](#mybatis)
      * [开发辅助](#开发辅助)
      * [pom.xml](#pomxml)
   * [配置类](#配置类)
      * [DataSourceConfig](#datasourceconfig)
      * [MapperJavaConfig](#mapperjavaconfig)
      * [ServiceJavaConfig](#servicejavaconfig)
      * [WebJavaConfig](#webjavaconfig)
      * [SSMConfig](#ssmconfig)
   * [SSM 实践（查询为例）](#ssm-实践查询为例)
      * [1. 编写封装类](#1-编写封装类)
      * [2. 编写控制层](#2-编写控制层)
      * [3. 编写业务层](#3-编写业务层)
      * [4. 编写持久层](#4-编写持久层)



## 概念

### 整合

SSM 顾名思义指的是 Java Web 开发中的三大经典框架的整合，目的就是用 Spring 容器统一管理三层组件的 Bean

- S：SpringFramework，作为业务层，负责业务对象的管理（IoC）和控制（AOP）
- S：SpringMVC，作为控制层，负责客户端的请求与响应（Controller-Model-View）
- M：MyBatis，作为数据层，负责操作数据库，实现 Java 方法和 SQL 语句的映射（Mapper）

### 容器

两个容器：将关注点分离，实现解耦合，可以灵活配置

- Root 容器：管理 Service 和 Mapper
- Web 容器：管理 Controller

<img src="https://dasi-blog.oss-cn-guangzhou.aliyuncs.com/Java/SpringMVC202508111357083.png" alt="image-20250811135706947" style="zoom: 50%;" />

Root Ioc 容器作为父容器可以调用 Web IoC 子容器

- 父容器的 Bean 子容器可以访问，但是子容器的 Bean 父容器不能访问
- 调用方向为：Controller → Service → Mapper

<img src="https://dasi-blog.oss-cn-guangzhou.aliyuncs.com/Java/SpringMVC202508111401486.png" alt="image-20250811140115437" style="zoom:50%;" />

配置文件

| 名称              | 功能                                                         |
| ----------------- | ------------------------------------------------------------ |
| DataSourceConfig  | 读取 jdbc 属性文件、配置 Druid 数据源                        |
| MapperJavaConfig  | 注册并配置 SqlSessionFactoryBean、扫描 Mapper 接口           |
| ServiceJavaConfig | 扫描 @Service，配置事务管理器                                |
| WebJavaConfig     | 配置视图解析器、消息转换器、参数解析器、拦截器和 CORS 等；扫描 @Controller |
| SSMConfig         | 创建两个容器并关联，注册 DispatcherServlet                   |

<img src="https://dasi-blog.oss-cn-guangzhou.aliyuncs.com/Java/SpringMVC202508111418553.png" alt="image-20250811141808492" style="zoom:50%;"  />



## 依赖

### SpringFramework

- spring-context：提供 IoC 容器和 Bean 生命周期管理
- spring-aspects：提供 AOP 功能
- spring-tx：提供事务管理
- spring-jdbc：提供 JDBC 封装

### SpringMVC

- spring-webmvc：提供 MVC 框架
- spring-web：提供 Web 基础服务
- jakarta.jakartaee-web-api：提供 Web 规范 API
- jakarta.servlet-api：提供 Servlet API

### MyBatis

- mybatis：提供映射器
- mybatis-spring：将 Spring 和 Mybatis 整合
- pagehelper：提供 MyBatis 分页插件
- mysql-connector-java：提供 MySQL 的 JDBC 驱动
- druid：提供 MySQL 连接池

### 开发辅助

- lombok：提供样板代码注解
- logback-classic：提供日志
- jackson-databind：提供 JSON 转换

### pom.xml

```xml
<project xmlns="http://maven.apache.org/POM/4.0.0"
         xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"
         xsi:schemaLocation="http://maven.apache.org/POM/4.0.0 http://maven.apache.org/xsd/maven-4.0.0.xsd">
    <modelVersion>4.0.0</modelVersion>

    <groupId>dasi</groupId>
    <artifactId>SSM</artifactId>
    <version>1.0-SNAPSHOT</version>
    <packaging>pom</packaging>
    <modules>
        <module>Demo1</module>
    </modules>

    <!-- 版本统一管理 -->
    <properties>
        <maven.compiler.source>17</maven.compiler.source>
        <maven.compiler.target>17</maven.compiler.target>
        <project.build.sourceEncoding>UTF-8</project.build.sourceEncoding>
        <spring.version>6.2.9</spring.version>
        <spring.tx.version>6.0.6</spring.tx.version>
        <jakarta.ee.version>9.1.0</jakarta.ee.version>
        <jakarta.servlet.version>5.0.0</jakarta.servlet.version>
        <jackson.version>2.15.0</jackson.version>
        <mybatis.version>3.5.11</mybatis.version>
        <mybatis.spring.version>3.0.3</mybatis.spring.version>
        <pagehelper.version>5.3.1</pagehelper.version>
        <mysql.version>8.0.33</mysql.version>
        <druid.version>1.2.16</druid.version>
        <lombok.version>1.18.26</lombok.version>
        <logback.version>1.5.18</logback.version>
    </properties>

    <dependencies>
        <!-- SpringFramework -->
        <dependency>
            <groupId>org.springframework</groupId>
            <artifactId>spring-context</artifactId>
            <version>${spring.version}</version>
        </dependency>
        <dependency>
            <groupId>org.springframework</groupId>
            <artifactId>spring-aspects</artifactId>
            <version>${spring.tx.version}</version>
        </dependency>
        <dependency>
            <groupId>org.springframework</groupId>
            <artifactId>spring-tx</artifactId>
            <version>${spring.tx.version}</version>
        </dependency>
        <dependency>
            <groupId>org.springframework</groupId>
            <artifactId>spring-jdbc</artifactId>
            <version>${spring.tx.version}</version>
        </dependency>

        <!-- SpringMVC -->
        <dependency>
            <groupId>org.springframework</groupId>
            <artifactId>spring-webmvc</artifactId>
            <version>${spring.version}</version>
        </dependency>
        <dependency>
            <groupId>org.springframework</groupId>
            <artifactId>spring-web</artifactId>
            <version>${spring.version}</version>
        </dependency>
        <dependency>
            <groupId>jakarta.platform</groupId>
            <artifactId>jakarta.jakartaee-web-api</artifactId>
            <version>${jakarta.ee.version}</version>
        </dependency>
        <dependency>
            <groupId>jakarta.servlet</groupId>
            <artifactId>jakarta.servlet-api</artifactId>
            <version>${jakarta.servlet.version}</version>
        </dependency>

        <!-- MyBatis -->
        <dependency>
            <groupId>org.mybatis</groupId>
            <artifactId>mybatis</artifactId>
            <version>${mybatis.version}</version>
        </dependency>
        <dependency>
            <groupId>org.mybatis</groupId>
            <artifactId>mybatis-spring</artifactId>
            <version>${mybatis.spring.version}</version>
        </dependency>
        <dependency>
            <groupId>com.github.pagehelper</groupId>
            <artifactId>pagehelper</artifactId>
            <version>${pagehelper.version}</version>
        </dependency>
        <dependency>
            <groupId>mysql</groupId>
            <artifactId>mysql-connector-java</artifactId>
            <version>${mysql.version}</version>
        </dependency>
        <dependency>
            <groupId>com.alibaba</groupId>
            <artifactId>druid</artifactId>
            <version>${druid.version}</version>
        </dependency>

        <!-- 开发辅助 -->
        <dependency>
            <groupId>org.projectlombok</groupId>
            <artifactId>lombok</artifactId>
            <version>${lombok.version}</version>
            <scope>provided</scope>
        </dependency>
        <dependency>
            <groupId>ch.qos.logback</groupId>
            <artifactId>logback-classic</artifactId>
            <version>${logback.version}</version>
        </dependency>
        <dependency>
            <groupId>com.fasterxml.jackson.core</groupId>
            <artifactId>jackson-databind</artifactId>
            <version>${jackson.version}</version>
        </dependency>
    </dependencies>
</project>
```



## 配置类

### DataSourceConfig

```java
// 声明 DataSource 的配置类
@Configuration
// 告诉 Spring 去类路径加载 jdbc.properties 资源文件来提供给 @Value 注解
@PropertySource("classpath:jdbc.properties")
public class DataSourceJavaConfig {
  	// 利用 @Value 注解通过占位符把对应的值注入成员变量
    @Value("${jdbc.user}")
    private String user;
    @Value("${jdbc.password}")
    private String password;
    @Value("${jdbc.url}")
    private String url;
    @Value("${jdbc.driver}")
    private String driver;

 		// 创建一个 DruidDataSource 对象，设置元信息，作为 Bean 提供给容器
    @Bean
    public DataSource getDataSource() {
        DruidDataSource dataSource = new DruidDataSource();
        dataSource.setUsername(user);
        dataSource.setPassword(password);
        dataSource.setUrl(url);
        dataSource.setDriverClassName(driver);
        return dataSource;
    }
}
```

### MapperJavaConfig

```java
// 声明 MyBatis 的配置类，充当 mybatis-config.xml
@Configuration
// 扫描指定包下所有 Mapper 接口，提供给 SqlSessionFactoryBean
@MapperScan("com.dasi.mapper")
public class MapperJavaConfig {
  	// 创建 SqlSessionFactoryBean 对象，作为 Bean 提供给容器
    // 启动时：
  	// 	1. SqlSessionFactoryBean 根据配置创建出 SqlSessionFactory 实例作为 Bean
    // 	2. 根据 @MapperScan 为每个接口创建出对应的 MapperFactoryBean 作为 Bean（内部持有 SqlSessionTemplate 的引用）
  	// 运行时：
    // 	1. SqlSessionTemplate 会从 SqlSessionFactory 获取一个 SqlSession
  	//	2. SqlSessionTemplate 会调用 getMapper 方法获取接口的动态代理
    @Bean
    public SqlSessionFactoryBean getSqlSessionFactoryBean(DataSource dataSource) {
      	// 创建一个 SqlSessionFactoryBean 对象
        SqlSessionFactoryBean sqlSessionFactoryBean = new SqlSessionFactoryBean();
      	// 参数注入数据源，用于设置 sqlSessionFactoryBean
        sqlSessionFactoryBean.setDataSource(dataSource);
				
      	// MyBatis 自己的 Configuration 类
        org.apache.ibatis.session.Configuration configuration = new org.apache.ibatis.session.Configuration();
      	// 配置开启下划线-驼峰转换
        configuration.setMapUnderscoreToCamelCase(true);
      	// 配置日志为 Slf4j
        configuration.setLogImpl(Slf4jImpl.class );
      	// 配置开启自动映射
        configuration.setAutoMappingBehavior(AutoMappingBehavior.FULL);
      	// 将配置应用到 sqlSessionFactoryBean
        sqlSessionFactoryBean.setConfiguration(configuration);
				
      	// 设置别名，自动取实体类名的首字母小写名作为别名
        sqlSessionFactoryBean.setTypeAliasesPackage("com.dasi.pojo");

      	// 配置 MyBatis 的插件
        PageInterceptor pageInterceptor = new PageInterceptor();
        Properties properties = new Properties();
        properties.setProperty("helperDialect", "mysql");
        pageInterceptor.setProperties(properties);
        sqlSessionFactoryBean.setPlugins(new Interceptor[]{pageInterceptor});

        return sqlSessionFactoryBean;
    }
}
```

### ServiceJavaConfig

```java
// 声明 SpringFramework 的配置类，充当 spring-config.xml
@Configuration
// 开启 AOP 的代理功能，启用 @Aspect 注解
@EnableAspectJAutoProxy
// 开启声明式事务，启用 @Transactional 注解
@EnableTransactionManagement
// 扫描指定包下所有用 @Component/@Service 标注的类，注册为 Bean
@ComponentScan("com.dasi.service")
public class ServiceJavaConfig {
  	// 注册一个事务管理器，作为 Bean 提供给容器
    @Bean
    public TransactionManager transactionManager(DataSource dataSource) {
      	// 参数注入数据源，用于设置 dataSourceTransactionManager
        DataSourceTransactionManager dataSourceTransactionManager = new DataSourceTransactionManager();
        dataSourceTransactionManager.setDataSource(dataSource);
        return dataSourceTransactionManager;
    }
}
```

### WebJavaConfig

```java
// 声明 SpringMVC 的配置类，充当 springMVC.xml
@Configuration
// 扫描指定包下所有用 @RestController/@Controller 标注的类，注册为 Bean
@ComponentScan("com.dasi.controller")
// 启用 SpringMVC 的默认配置，底层会注册很多核心 Bean
// - 路由映射：RequestMappingHandlerMapping
// - 路由适配：RequestMappingHandlerAdapter
// - 消息转换：HttpMessageConverter
// - 异常处理：ExceptionHandlerExceptionResolver
// - 参数校验：Validator
@EnableWebMvc
// 实现 WebMvcConfigurer 接口，可以按需进行配置和扩展
public class WebJavaConfig implements WebMvcConfigurer {
    // 开启静态资源处理，将静态资源交给默认的 Servlet 处理
    @Override
    public void configureDefaultServletHandling(DefaultServletHandlerConfigurer configurer) {
        configurer.enable();
    }

    // 配置视图解析器为 JSP，并配置视图文件的前缀和后缀
    @Override
    public void configureViewResolvers(ViewResolverRegistry registry) {
        registry.jsp("/WEB-INF/views/", ".jsp");
    }

    // 注册拦截器，可以实现登陆校验、权限控制、日志记录等
    @Override
    public void addInterceptors(InterceptorRegistry registry) {
        registry.addInterceptor(new LoginInterceptor())
                .addPathPatterns("/**")
                .excludePathPatterns("/login");
    }
}

```

### SSMConfig

```java
// SSM 项目的入口配置类，用来代替 web.xml
public class SSMConfig extends AbstractAnnotationConfigDispatcherServletInitializer {
  	// 设置 root 容器，使用 DataSource 配置类、MyBatis 配置类、SpringFramework 配置类
    @Override
    protected Class<?>[] getRootConfigClasses() {
        return new Class[]{DataSourceJavaConfig.class, MapperJavaConfig.class, ServiceJavaConfig.class};
    }
		
  	// 设置 web 容器，使用 SpringMVC 配置类
    @Override
    protected Class<?>[] getServletConfigClasses() {
        return new Class[]{WebJavaConfig.class};
    }

  	// 注册 DispatcherServlet 并设置拦截的 URL 模式
    @Override
    protected String[] getServletMappings() {
        return new String[]{"/"};
    }
}
```



## SSM 实践（查询为例）

> 假设已经完成 SSM 的配置

### 1. 编写封装类

Page 类：**统一分页数据格式**，包含当前页码、每页条数、数据总条数和当前页数据

```java
@Data
@NoArgsConstructor
@AllArgsConstructor
public class Page<T> {
    private Integer currentPage;
    private Integer pageSize;
    private Integer total;
    private List<T> data;
}
```

Result 类：**统一响应结果格式**，包含业务状态码、提示信息和数据内容

```java
@Data
@AllArgsConstructor
@ToString
public class Result {
    private int code;
    private String msg;
    private Object data;
	
  	// 成功结果
    public static Result success(Object data) {
        return new Result(200, "成功", data);
    }
	
  	// 失败结果
    public static Result fail(Object data) {
        return new Result(500, "错误", data);
    }
}
```

### 2. 编写控制层

```java
// 允许跨域
@CrossOrigin
// 标识该类为 REST 风格的控制器，返回 JSON 而不是视图
@RestController
// 为该控制器统一指定请求路径前缀 /schedule
@RequestMapping("schedule")
// 启用 Slf4j 日志功能，可直接使用 log.info 等方法
@Slf4j
public class ScheduleController {
		// 注入业务层接口，Spring 会自动找到其实现类实例
    @Autowired
    private ScheduleService scheduleService;
		
  	// 处理 GET 请求，并匹配路径格式
    @GetMapping("/{currentPage}/{pageSize}")
  	// 从 URL 路径中获取参数，并绑定到方法参数
    public Result page(@PathVariable("currentPage") int currentPage,
                       @PathVariable("pageSize")    int pageSize) {
      	
      	// 调用业务层方法获取分页结果
        Result result = scheduleService.page(currentPage, pageSize);
	      
      	// 打印查询结果到日志
        log.info("查询结果为：{}", result);
        return result;
    }
}
```

### 3. 编写业务层

```java
/* 接口定义为
public interface ScheduleService {
    Result queryPage(int currentPage, int pageSize);
}
*/

// 将此类注册为 Bean
@Service
public class ScheduleServiceImpl implements ScheduleService {

  	// 注入 ScheduleMapper， Spring 会自动生成其实现类实例
    @Autowired
    private ScheduleMapper scheduleMapper;
  
  	// 分页查询日程数据的方法实现
    @Override
    public Result queryPage(int currentPage, int pageSize) {

        // 使用 PageHelper 插件启动分页功能
        PageHelper.startPage(currentPage, pageSize);

        // 调用持久层方法获取日程结果
        List<Schedule> scheduleList = scheduleMapper.querySchedule();
      	
      	// 将查询结果传入 PageInfo 对象，自动得到分页结果
        PageInfo<Schedule> pageInfo = new PageInfo<>(scheduleList);

        // 装配 PageInfo 对象到自定义的 Page 对象
        Page<Schedule> schedulePage = new Page<>(currentPage, pageSize, (int) pageInfo.getTotal(), pageInfo.getList());
      
      	// 装配 Page 对象到自定义的 Result 对象
        return Result.success(schedulePage);
    }
}
```

### 4. 编写持久层

```xml
<!-- 接口定义为
public interface ScheduleMapper {
    List<Schedule> querySchedule();

    int deleteSchedule(Integer id);

    int addSchedule(Schedule schedule);

    int updateSchedule(Schedule schedule);
}
-->

<!-- 指定 XML 文件和 Mapper 接口的映射 -->
<mapper namespace="com.dasi.mapper.ScheduleMapper">
  	<!-- 指定 SQL 语句和 Mapper 方法的映射 -->
    <select id="querySchedule" resultType="com.dasi.pojo.Schedule">
        select * from schedule
    </select>
</mapper>
```