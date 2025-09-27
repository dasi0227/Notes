# SpringCloud



   * [架构](#架构)
      * [单机架构（Standalone）](#单机架构standalone)
      * [集群架构（Cluster)](#集群架构cluster)
      * [分布式架构（Distributed）](#分布式架构distributed)
   * [概述](#概述)
      * [定义](#定义)
      * [目录结构](#目录结构)
      * [POM 结构](#pom-结构)
   * [Nacos](#nacos)
      * [服务管理](#服务管理)
         * [服务注册](#服务注册)
         * [服务发现](#服务发现)
         * [服务调用与负载均衡](#服务调用与负载均衡)
      * [配置管理](#配置管理)
         * [配置加载](#配置加载)
         * [配置隔离](#配置隔离)
         * [配置监听](#配置监听)
   * [OpenFeign](#openfeign)
      * [调用方式](#调用方式)
      * [FeignClient](#feignclient)
      * [Fallback](#fallback)
      * [调用拦截](#调用拦截)
   * [Sentinel](#sentinel)
      * [核心概念](#核心概念)
         * [资源](#资源)
         * [规则](#规则)
         * [使用方式](#使用方式)
      * [流量](#流量)
         * [阈值类型](#阈值类型)
         * [流控模式](#流控模式)
         * [流控效果](#流控效果)
      * [熔断降级](#熔断降级)
         * [熔断效果](#熔断效果)
         * [熔断策略](#熔断策略)
      * [热点](#热点)
      * [授权](#授权)
      * [系统](#系统)
      * [异常处理](#异常处理)
         * [定义](#定义)
         * [blockHandler](#blockhandler)
         * [fallback](#fallback)
         * [@BlockExceptionHandler](#blockexceptionhandler)
         * [SphU 的 try-catch](#sphu-的-try-catch)
   * [Gateway](#gateway)
      * [核心概念](#核心概念)
      * [使用方式](#使用方式)
      * [Predicate](#predicate)
         * [定义](#定义)
         * [内置断言工厂](#内置断言工厂)
         * [自定义断言工厂](#自定义断言工厂)
         * [底层流程](#底层流程)
      * [Filter](#filter)
         * [定义](#定义)
         * [内置过滤器工厂](#内置过滤器工厂)
         * [自定义过滤器工厂](#自定义过滤器工厂)
         * [底层流程](#底层流程)
   * [Seata](#seata)
      * [分布式事务](#分布式事务)
      * [二阶段提交协议 2PC](#二阶段提交协议-2pc)
      * [事务模式](#事务模式)
      * [使用方式](#使用方式)



## 架构

### 单机架构（Standalone）

**应用程序（Tomcat）、数据库（MySQL）、缓存（Redis）等都集中部署在单个节点上**

- 部署简单：往往只需要 1-2 台服务器即可，成本低
- 轻量级：适合并发量低、用户量小的应用，如个人博客和团队管理系统
- **垂直扩展（scale up）**：只能通过升级硬件来提升性能，效果是有上限的

![image-20250910170951117](https://dasi-blog.oss-cn-guangzhou.aliyuncs.com/Java/202509101709253.png)

> MySQL 和 Redis 也可以分布在不同的服务器上，但本质上都是只有一台

### 集群架构（Cluster)

**应用程序（Tomcat）、数据库（MySQL）、缓存（Redis）等分布在多个不同节点上，整体对外提供统一服务**

- 负载均衡：可以将请求分发到不同节点执行
- 高可用性：单台宕机不会影响整体，其他节点可继续工作
- 实现复杂：需要确保节点间的数据一致性
- **水平扩展（scale out）**：可以通过增加节点来提升性能

![image-20250910173918261](https://dasi-blog.oss-cn-guangzhou.aliyuncs.com/Java/202509101739320.png)

### 分布式架构（Distributed）

**应用程序（订单、支付、商品、用户等服务）按功能拆分，分别部署在不同节点上，通过远程调用协作完成整体业务**

- **微服务解耦：各个服务可以按照业务边界独立开发、升级和部署，不会影响到其他服务，服务之间通过 RPC 进行交互**
- 高可用性：可通过**容错/降级**机制保证单个服务异常不会影响其他服务，从而使系统整体可用
- 多语言支持：不同模块和服务可以选择最合适的语言来实现，如算法和大模型通过 Python，控制和硬件通过 C++，Web 和业务通过 Java，它们之间通过 RPC 进行交互
- 实现复杂：需要解决**集中配置、服务通信、数据一致、分布式事务、链路追踪**等问题

![image-20250910222537110](https://dasi-blog.oss-cn-guangzhou.aliyuncs.com/Java/202509102225172.png)



## 概述

### 定义

SpringCloud 是一个基于 Spring 的微服务治理框架，帮助开发者快速搭建和治理分布式系统

- **SpringBoot 负责开发单个微服务**
- **SpringCloud 负责协调多个微服务**

| 核心功能       | 意义                                     | 工具                               |
| -------------- | ---------------------------------------- | ---------------------------------- |
| 服务注册与发现 | 动态管理服务实例，实现服务自动注册与发现 | Nacos、Eureka、Consul、Zookeeper   |
| 配置中心       | 集中化配置管理，支持动态刷新             | Spring Cloud Config、Nacos、Apollo |
| 服务调用       | 多实例间的服务请求，简化 HTTP 调用       | OpenFeign、RestTemplate            |
| 负载均衡       | 多实例请求分流，提高可用性和吞吐量       | Spring Cloud LoadBalancer、Nginx   |
| 熔断降级与限流 | 防止服务雪崩，提升系统容错性             | Resilience4j、Sentinel             |
| 网关           | 提供统一入口，负责路由、认证、限流等     | Spring Cloud Gateway、Kong         |
| 消息驱动       | 解耦服务、支持异步通信和削峰填谷         | Spring Cloud Stream                |
| 链路追踪       | 追踪请求链路，辅助监控与故障排查         | Spring Cloud Sleuth                |
| 监控           | 监控微服务运行，进行健康检查和指标采集   | Spring Boot Actuator、Prometheus   |

> 除了用 Spring Cloud 内建的能力，还可以使用外部扩充工具

### 目录结构

由于只有一台电脑，所以将不同微服务作为一个模块统一放在 services 父模块下

```bash
SpringCloudDemo
├── models								# 实体模块
│		├── src
│		└── pom.xml
├── services							# 微服务模块
│   ├── service-order			# 订单微服务
│		│		├── src
│		│		└── pom.xml
│   ├── service-product		# 商品微服务
│		│		├── src
│		│		└── pom.xml
│   └── pom.xml
└── pom.xml
```

### POM 结构

- 顶层：作为 **BOM（Bill Of Material，物料清单）**来集中管理依赖版本号，在 `<dependencyManagement>` 下引入或继承各种 BOM，可以**实现依赖版本的统一和对齐，避免不同模块间发生版本冲突，在子模块中无需重复声明版本号**

    ```xml
    <!-- Spring Boot -->
    <parent>
        <groupId>org.springframework.boot</groupId>
        <artifactId>spring-boot-starter-parent</artifactId>
        <version>3.3.4</version>
    </parent>
    
    <!-- 依赖管理 -->
    <dependencyManagement>
        <dependencies>
            <!-- Spring Cloud -->
            <dependency>
                <groupId>org.springframework.cloud</groupId>
                <artifactId>spring-cloud-dependencies</artifactId>
                <version>2023.0.3</version>
                <type>pom</type>
                <scope>import</scope>
            </dependency>
    
            <!-- Spring Cloud Alibaba -->
            <dependency>
                <groupId>com.alibaba.cloud</groupId>
                <artifactId>spring-cloud-alibaba-dependencies</artifactId>
                <version>2023.0.3.2</version>
                <type>pom</type>
                <scope>import</scope>
            </dependency>
        </dependencies>
    </dependencyManagement>
    ```

- 中间层：**作为模块容器，把多个微服务子项目聚合到一起，实现统一编译和构建，并引入公共依赖**，如 web、test、mysql、lombok、hutool 以及自研模块等，需要注意的是不在 BOM 中的依赖需要写对应版本

    ```xml
    <dependencies>  
       	<!-- 测试 -->
        <dependency>
            <groupId>org.springframework.boot</groupId>
            <artifactId>spring-boot-starter-test</artifactId>
            <scope>test</scope>
        </dependency>
    
        <!-- 网络 -->
        <dependency>
            <groupId>org.springframework.boot</groupId>
            <artifactId>spring-boot-starter-web</artifactId>
        </dependency>
    
        <!-- 数据库 -->
        <dependency>
            <groupId>com.mysql</groupId>
            <artifactId>mysql-connector-j</artifactId>
        </dependency>
    
        <!-- 连接池 -->
        <dependency>
            <groupId>org.springframework.boot</groupId>
            <artifactId>spring-boot-starter-jdbc</artifactId>
        </dependency>
    
        <!-- MyBatis-Plus -->
        <dependency>
            <groupId>com.baomidou</groupId>
            <artifactId>mybatis-plus-spring-boot3-starter</artifactId>
            <version>3.5.12</version>
        </dependency>
    
      	<!-- Lombok -->
        <dependency>
            <groupId>org.projectlombok</groupId>
            <artifactId>lombok</artifactId>
    	      <version>1.18.34</version>
        </dependency>
    
      	<!-- 通用工具 -->
        <dependency>
            <groupId>cn.hutool</groupId>
            <artifactId>hutool-all</artifactId>
            <version>5.8.26</version>
        </dependency>
      
        <!-- 自研模块 -->
        <dependency>
            <groupId>com.dasi</groupId>
            <artifactId>models</artifactId>
            <version>1.0.0</version>
        </dependency>
    </dependencies>
    ```

- 服务层：**引入只有在当前服务中才需要的特有依赖**，比如需要使用阿里云对象存储才引入 aliyun-sdk-oss，需要使用消息队列才引入 RabbitMQ，如果放入中间层会导致**每个服务体积增大和服务启动速度下降**

    ```xml
    <dependencies>
        <dependency>
            <groupId>org.springframework.boot</groupId>
            <artifactId>spring-boot-starter-amqp</artifactId>
        </dependency>
      
        <dependency>
            <groupId>com.aliyun.oss</groupId>
            <artifactId>aliyun-sdk-oss</artifactId>
            <version>3.17.0</version>
        </dependency>
    </dependencies>
    ```



## Nacos

### 服务管理

#### 服务注册

1. 引入依赖

    ```xml
    <dependency>
        <groupId>com.alibaba.cloud</groupId>
        <artifactId>spring-cloud-starter-alibaba-nacos-discovery</artifactId>
    </dependency>
    ```

2. 配置 application.yml

    ```yaml
    spring:
      application:
        name: service-order
    cloud:
      nacos:
        discovery:
          server-addr: 127.0.0.1:8848
    ```

3. 启动 Server 和 Dashboard

    - 8848：Nacos 的 Web 控制台
    - 9848：gRPC，用于服务注册/心跳
    - 9849：gRPC，用于服务间的通信

    ```bash
    docker run -d \
      --name nacos \
      -e MODE=standalone \
      -p 8848:8848 \
      -p 9848:9848 \
      -p 9849:9849 \
      nacos/nacos-server:2.4.3
    ```

4. 在服务台查看服务列表：这里开启了两个服务，其中每个服务有两个实例

![image-20250914153009864](https://dasi-blog.oss-cn-guangzhou.aliyuncs.com/Java/202509141530984.png)

#### 服务发现

Spring Cloud Alibaba 会自动注册一个 **DiscoveryClient** 对象到容器中，注入该对象可以获取已经注册的所有服务名称和所有对应的服务实例

```java
@Autowired
private DiscoveryClient discoveryClient;

public void discover() {
  	// 发现所有服务
    List<String> services = discoveryClient.getServices();
    for (String service : services) {
        System.out.println(service);
        
      	// 发现服务的所有实例，调用方法获取其信息
        List<ServiceInstance> instances = discoveryClient.getInstances(service);
        for (ServiceInstance instance : instances) {
            System.out.println(
                "  \t instanceId = " + instance.getInstanceId() +
                "\n\t scheme = " + instance.getScheme() +
                "\n\t host = " + instance.getHost() +
                "\n\t port = " + instance.getPort() +
                "\n\t uri = " + instance.getUri() +
                "\n\t metadata = " + instance.getMetadata()
            );
        }
    }
}
```

#### 服务调用与负载均衡

1. 引入依赖

    ```xml
    <dependency>
        <groupId>org.springframework.cloud</groupId>
        <artifactId>spring-cloud-starter-loadbalancer</artifactId>
    </dependency>
    ```

2. 注册 Bean：使用注解 @LoadBalanced 可以自动从 Nacos 获取服务实例进行负载均衡

    ```java
    @Bean
    @LoadBalanced
    public RestTemplate restTemplate() {
        return new RestTemplate();
    }
    ```

3. 服务调用：不需要写死主机名和端口，只需要写服务名，交给 LoadBalancer 来自动映射到不同服务实例

    ```java
    @Autowired
    private RestTemplate restTemplate;
    
    private Product getProductFromRemote(Long productId) {
        // 1. 构造 URL
        String url = "http://service-product/product/" + productId;
        // 2. 发起 HTTP 请求
        return restTemplate.getForObject(url, Product.class);
    }
    ```

### 配置管理

#### 配置加载

1. 引入依赖

    ```xml
    <dependency>
        <groupId>com.alibaba.cloud</groupId>
        <artifactId>spring-cloud-starter-alibaba-nacos-config</artifactId>
    </dependency>
    ```

2. 在 nacos 创建配置，首先选定命名空间，然后点击创建配置，最后指定 data id、group、type 以及具体内容

    ![image-20250914172625277](https://dasi-blog.oss-cn-guangzhou.aliyuncs.com/Java/202509141726425.png)

3. 配置 application.yml

    - `spring.config.import`：指定加载的配置文件，使用 `nacos:` 前缀表示从 Nacos 获取，文件位置格式为 `<Data ID>?group=<Group Name>`
    - `spring.cloud.nacos.config`：指定如何连接到 Nacos 配置中心，`server-addr` 指定服务器位置，`namespace` 指定命名空间，`group` 指定默认分组，`refresh-enabled` 指定是否动态刷新

    ```yaml
    spring:
      application:
        name: service-product
      config:
        import:
          - nacos:database.properties
          - nacos:product.properties
          - nacos:service-product.yaml?group=product
      cloud:
        nacos:
          discovery:
            server-addr: 127.0.0.1:8848
          config:
            server-addr: 127.0.0.1:8848
            namespace: public
            group: DEFAULT_GROUP
            refresh-enabled: true
    ```

4. 获取配置：可以通过 **@Value("${xxx.yyy}")** 获取单个值，也可以通过 **@ConfigurationProperties(prefix="xxx")** 映射所有值到对象并且通过 @Component 注册到容器中

    ```java
    @Data
    @Component
    @ConfigurationProperties(prefix = "product")
    public class ProductProperties {
        private String id;
        private Integer price;
        private Integer amount;
        private List<String> tags;
    }
    ```

#### 配置隔离

| 对比     | 命名空间 Namespace           | 分组 Group                         |
| -------- | ---------------------------- | ---------------------------------- |
| 定位     | 最大维度的隔离               | 命名空间内部的逻辑分类             |
| 默认值   | public                       | DEFAULT_GROUP                      |
| 限制     | 一个应用只能关联一个命名空间 | 一个应用可以同时加载多个分组的配置 |
| 主要用途 | 区分环境：生产、开发、测试   | 区分模块：商品、用户、订单         |

#### 配置监听

Spring Cloud Alibaba 会自动注册一个 **NacosConfigManager** 对象到容器中，就能通过 getConfigService() 拿到 Nacos 的核心配置服务 **ConfigService**，其中 **addListener** 方法可以给某个配置文件添加一个监听器，一旦这个配置在 Nacos 控制台被修改，客户端就会实时收到通知

创建 Nacos 的监听器需要实现两个方法

- **getExecutor()**：指定监听回调的线程池，可以通过 `Executors.newFixedThreadPool(n)` 创建
- **receiveConfigInfo(String configInfo)**：指定通知的回调方法，Nacos 会把最新的配置内容推送过来，常用于记录日志，更新 Bean 属性，通知其他微服务

```java
// 在容器启动完成之后自动执行
@Bean
public ApplicationRunner applicationRunner(NacosConfigManager nacosConfigManager) {
    return args -> {
        ConfigService configService = nacosConfigManager.getConfigService();

        String dataId = "product.properties";
        String group = "DEFAULT_GROUP";

        // 获取旧配置
        AtomicReference<String> oldConfig = new AtomicReference<>(
                configService.getConfig(dataId, group, 5000)
        );

      	// 添加监听器
        configService.addListener("product.properties", "DEFAULT_GROUP", new Listener() {
            @Override
            public Executor getExecutor() {
                return Executors.newFixedThreadPool(1);
            }

            @Override
            public void receiveConfigInfo(String newConfigInfo) {
                // 获取新配置
              	String oldConfigInfo = oldConfig.get();
                
              	if (!oldConfigInfo.equals(newConfigInfo)) {
                    System.out.println("旧配置：\n" + oldConfigInfo);
                    System.out.println("--------");
                    System.out.println("新配置：\n" + newConfigInfo);
                }
              
                // 更新旧配置
                oldConfig.set(newConfigInfo);
            }
        });
    };
}
```



## OpenFeign

### 调用方式

- **编程式 Rest 客户端**：需要**手动拼接 URL 来发请求**，如 RestTemplate 和 WebClient
- **声明式 Rest 客户端**：只需要**声明一个接口并注解**，底层框架会自动生成代理对象来发起请求，如 OpenFeign

### FeignClient

1. 引入依赖

    ```xml
    <dependency>
        <groupId>org.springframework.cloud</groupId>
        <artifactId>spring-cloud-starter-openfeign</artifactId>
    </dependency>
    ```

2. 配置 application.yml：指定调用微服务的情况，可以指定连接超时和业务超时，其中日志级别有

    - NONE：默认值，不打印任何日志
    - BASIC：只记录请求方法、URL、响应状态码和执行时间
    - HEADERS：在 BASIC 的基础上，记录请求和响应头信息
    - FULL：记录所有内容

    ```yaml
    spring:
    	cloud:
        openfeign:
          client:
            config:
              default:
                logger-level: basic
                connect-timeout: 10000
                read-timeout: 10000
              service-product:
                logger-level: basic
                connect-timeout: 10000
                read-timeout: 10000
    ```

3. 启用注解

    ```java
    @EnableFeignClients
    @SpringBootApplication
    public class OrderApp {
        public static void main(String[] args) {
            SpringApplication.run(OrderApp.class, args);
        }
    }
    ```

4. 定义接口：value 指定微服务名称，内容和远程服务的 Controller 对象中的方法保持一致

    ```java
    @FeignClient(value = "service-product", fallback = ProductFeignClientFallback.class)
    public interface ProductFeignClient {
        @GetMapping("product/{id}")
        Product getProduct(@PathVariable("id") Long productId);
    }
    ```

5. 注入 Bean：**发起请求像调用方法一样**

    ```java
    @Autowired
    private ProductFeignClient productFeignClient;
    
    @Override
    public Order createOrder(Long userId, Long productId) {
      	// 调用 FeignClient 对象的方法
        Product product = getProductFromRemote(productId);
        BigDecimal totalAmount = product.getPrice().multiply(new BigDecimal(product.getNum()));
      
      	// 创建 Order 对象
        Order order = new Order();
        order.setId(1L);
        order.setUserId(userId);
        order.setTotalAmount(totalAmount);
        order.setProductList(List.of(product));
        return order;
    }
    ```

### Fallback

可以给每一个 FeignClient 接口指定一个 fallback 类，该类需要实现  FeignClient 接口，是 Feign 在调用远程服务失败时的降级处理逻辑，即兜底操作

```java
@Component
public class ProductFeignClientFallback implements ProductFeignClient {
    @Override
    public Product getProduct(Long productId) {
        Product product = new Product();
        product.setId(productId);
        product.setName("商铺信息错误");
        product.setPrice(new BigDecimal("0"));
        product.setNum(0);
        return product;
    }
}
```

### 调用拦截

默认情况下，微服务间调用只会传输方法参数里的内容，而**前端请求头中的用户信息、Token、TraceId 等上下文信息不会自动透传**，因此 OpenFeign 提供了专用的拦截器接口 RequestInterceptor，只需要重写 apply 方法，就可以对请求进行拦截，并通过注入的 RequestTemplate 对象进行增强

```java
@Component
public class TokenOpenFeignInterceptor implements RequestInterceptor {
    @Override
    public void apply(RequestTemplate requestTemplate) {
        String token = UUID.randomUUID().toString();
        requestTemplate.header("token", token);
    }
}
```

虽然 OpenFeign 没有提供对响应的直接拦截，但是它提供了 Decoder 和 ErrorDecoder 接口来实现对成功响应和失败响应的统一处理

```java
@Configuration
@Slf4j
public class FeignConfig {
    @Bean
    public Decoder feignDecoder(ObjectMapper objectMapper) {
        return (response, type) -> {
            String body = Util.toString(response.body().asReader(StandardCharsets.UTF_8));
            log.info("调用成功: {}", body);
            return objectMapper.readValue(body, objectMapper.constructType(type));
        };
    }

    @Bean
    public ErrorDecoder errorDecoder() {
        return (methodKey, response) -> {
            String body;
            try {
                body = Util.toString(response.body().asReader(StandardCharsets.UTF_8));
            } catch (IOException e) {
                throw new RuntimeException(e);
            }
            log.error("调用失败: {}", body);
            return new RuntimeException(methodKey + "远程调用异常！");
        };
    }
}
```



## Sentinel

### 核心概念

#### 资源

资源是 Sentinel 需要监控的业务

- 系统级别：Sentinel 会把整个应用 JVM 当作一个资源

- 方法级别：手动利用注解将整个方法标记为资源

    ```java
    @SentinelResource("getUser")
    public User getUser(Long id) { ... }
    ```

- 接口级别：自动把请求方法标记为资源，名称默认为请求路径

    ```java
    @GetMapping("read")
    public String read() { ... }
    ```

- 代码级别：可以通过 try 和 SphU 来给将一个代码块标记为资源

    ```java
    try (Entry entry = SphU.entry("customBlock"))  { ... }
    ```

#### 规则

- 流量（Flow）：限制资源的 QPS、并发线程数
- 热点（ParamFlow）：限制参数值的 QPS
- 熔断降级（Degrade）：限制错误率、慢响应比例、错误数
- 系统（System）：限制系统负载、CPU 使用率
- 授权（Authority）：限制黑名单、白名单

#### 使用方式

1. 引入依赖

    ```xml
    <dependency>
        <groupId>com.alibaba.cloud</groupId>
        <artifactId>spring-cloud-starter-alibaba-sentinel</artifactId>
    </dependency>
    ```

2. 配置 application.yml

    ```yaml
    spring:
      cloud:
        sentinel:
          transport:
            dashboard: localhost:8858
          eager: true
    
    # 实际上只有开启 Sentinel，先前 OpenFeign 的 fallback 才会生效
    feign:
      sentinel:
        enabled: true
    ```

3. 启动 Dashboard（Server 在服务的 JVM 内部跑，跟 Nacos 不一样）

    ```bash
    java -Dserver.port=8858 -jar sentinel-dashboard-1.8.8.jar
    ```

### 流量

#### 阈值类型

- **QPS**：**每秒最多处理的请求数量**

- **线程数**：同时存在的并发线程上限，即**同一时间最多处理的请求数量**

#### 流控模式

- **直接**：限制当前资源本身

- **关联**：限制关联资源，当下游资源拥挤时，限制上游资源，防止级联雪崩

- **链路**：限制特定调用链路下的资源，比如同一个下游方法被多个上游方法调用，但只对部分上游方法的调用进行限流

#### 流控效果

- **快速失败**：直接拒绝请求，抛出 FlowException
- **预热**：从一个较低阈值直接升高到较高阈值
- **排队等待**：强制保证请求按照阈值匀速通过，超过速率的请求会排队等待，如果排队时间超过了最大等待时间会返回失败

![afdf72691ecc30aff79b1fdcc01d75f1](https://dasi-blog.oss-cn-guangzhou.aliyuncs.com/Java/202509151609016.png)

### 熔断降级

#### 熔断效果

- **统计时长**：用于统计异常和慢调用的时间窗口
- **最小请求数**：在统计时长内，至少达到多少请求数才触发统计判断，防止样本太少导致误判
- **熔断时长**：进入熔断状态后，直接阻断请求的持续时间

#### 熔断策略

- **慢调用比例**：高于最大 RT 的请求数 / 总请求数 > 比例阈值
- **异常比例**：异常请求数 / 总请求数 > 比例阈值
- **异常数**：异常请求数 > 数量阈值

### 热点

本质上也是流量控制，只不过颗粒度从方法本身到方法的参数值，而且只能使用 QPS

- **统计窗口**：用于统计的时间窗口，计算平均 QPS
- **参数索引**：指定方法入参的位置（从 0 开始计数）
- **单机阈值：**默认的限流阈值，即对参数的所有值统一生效
- **例外参数阈值**：指定参数值的限流阈值

> 单机多 + 例外少 → 针对热点参数更严格 → 秒杀商品
>
> 单机少 + 限流多 → 针对特殊参数更宽松 → 充值用户

![2aeb0d271b3ec250e692ad9e433f7252](https://dasi-blog.oss-cn-guangzhou.aliyuncs.com/Java/202509151609521.png)

### 授权

通过自定义 **RequestOriginParser** 来决定调用方标识，从而对调用方进行白名单和黑名单处理，优先级是先检查白名单，存在则直接放行，再检查黑名单，存在则拒绝，如果都不存在默认放行

需要注意的是，**不能使用 origin 作为请求头字段**，因为 origin 是浏览器在跨域请求时自动附带的请求头，值通常是前端页面的域名，所以为了保证正确性，在进行 Feign、RestTemplate 等服务间调用时，默认不会传递 origin

```java
// 配置在 service-order
@Component
@Slf4j
public class TokenOpenFeignInterceptor implements RequestInterceptor {
    @Override
    public void apply(RequestTemplate requestTemplate) {
        String caller = "dasi";
        requestTemplate.header("caller", caller);
        log.info("添加了来源 caller：{}", caller);
    }
}

// 配置在 service-product
@Configuration
@Slf4j
public class SentinelConfig {
    @Bean
    public RequestOriginParser requestOriginParser() {
        return request -> {
            String caller = request.getHeader("caller");
            log.info("获取到来源 caller：{}", caller);
            return (caller == null || caller.isEmpty()) ? "blank" : caller;
        };
    }
}
```

### 系统

- 应用健康：
    - RT：所有请求的平均响应时间
    - 线程数：系统当前正在处理请求的线程总数
    - 入口 QPS：应用每秒接收到的请求总数
- 机器健康：
    - CPU 使用率：CPU 繁忙时间占总时间的百分比
    - LOAD：一段时间内 CPU 正在处理和等待处理的进程数

### 异常处理

#### 定义

**异常处理指的是针对不同规则触发时的兜底机制**，上述讲的五个规则都对应一个异常类 FlowException、ParamFlowException，DegradeException，AuthorityException，SystemBlockException，而它们都继承于 **BlockException**

![image-20250911175920296](https://dasi-blog.oss-cn-guangzhou.aliyuncs.com/Java/202509111759002.png)

![image-20250912101507678](https://dasi-blog.oss-cn-guangzhou.aliyuncs.com/Java/202509121015382.png)

#### blockHandler

作为 @SentinelResource 注解中的属性，指定处理 BlockException 异常的方法，并且方法的参数个数和类型需要和资源定义的方法一致，但是在最后可以多注入一个 BlockException 参数

> 可以通过 **blockHandlerClass** 属性指明 blockHandler 方法所在的类，不写的话默认在本类中查找

```java
@SentinelResource(value = "read", blockHandler = "readBlockHandler")
public String read(Long id) {
    return "正常返回：" + id;
}

public String readBlockHandler(Long id, BlockException e) {
    System.out.println("Sentinel 异常原因：" + e.getMessage());
    return "blockHandler 限制：" + id;
}
```

#### fallback

**blockHandler 只能处理 BlockException 异常**，但如果请求的服务出现了其他异常，比如空指针异常（NullPointerException）、调用失败异常（FeignException）、非法参数异常（IllegalArgumentException）等，这时候就只能通过 fallback 来处理

实际上 fallback 也可以处理 BlockException 异常，**如果同时配置了 blockHandler 和 fallback，BlockException 只会走 blockHandler，其他异常只会走 fallback**

fallback 与 blockHandler 一样，指定的是一个方法，并要求方法的参数个数和类型需要和资源定义的方法一致，但是在最后可以多注入一个 Throwable 参数

> 可以通过 **fallbackClass** 属性指明 fallback 方法所在的类，不写的话默认在本类中查找

```java
@SentinelResource(value = "read", fallback = "readFallback")
public String read(Long id) {
    return "正常返回：" + id;
}

public String readFallback(Long id, Throwable t) {
  	System.out.println("请求异常原因：" + t.getMessage());
    return "fallback 限制：" + id;
}
```

#### @BlockExceptionHandler

blockHandler / fallback 只能作用在某个资源方法上，而实际业务中不会给所有资源都设置异常回调逻辑，这时候就需要**实现 Sentinel 提供的 BlockExceptionHandler 接口，在整个应用层面捕获 BlockException 异常来进行全局统一处理**

这个拦截发生在 Sentinel 层，还没有进入 Controller 和资源，**手里只有 HttpServletResponse 对象，必须通过 PrintWriter 手动写回响应**

需要注意的是，Sentinel 已经有一个 **DefaultBlockExceptionHandler** 类实现了该接口，所以为了保证自定义的异常处理类优先注入，需要加上 **@Primary** 注解

> 429 状态码含义是 Too Many Requests，符合熔断降级的 HTTP 语义

```java
@Component
@Primary
@Slf4j
public class MyBlockExceptionHandler implements BlockExceptionHandler {
    @Override
    public void handle(HttpServletRequest request, HttpServletResponse response, String resource, BlockException e) throws Exception {
      	// 设置响应头
        response.setCharacterEncoding("utf-8");
        response.setStatus(429);
        response.setContentType("application/json;charset=utf-8");
        
      	// 设置响应体
        Result result = Result.fail(500, resource + "被 Sentinel 限制，类型为 " + e.getClass().getSimpleName());

      	String json = JSONUtil.toJsonStr(result);

      	// 写响应
        PrintWriter writer = response.getWriter();
      	writer.write(json);
        writer.flush();
        writer.close();
      
        log.error("处理 {} 中的异常 {}，返回 {}", resource, e.getMessage(), json);
    }
}
```

#### SphU 的 try-catch

SphU 提供了一种方式将代码片段定义为资源，从而可以直接利用 try-catch 结构来捕获异常

```java
try (Entry entry = SphU.entry("read")) {
    read();
} catch (BlockException e) {
    log.error("read" + " 被 Sentinel 限制，类型为 {}", e.getClass().getSimpleName());
} 
```



## Gateway

### 核心概念

- **id：每个路由规则的唯一标识**
- **uri：路由的目标地址，即请求的转发地址**，可以通过 `lb:<微服务名>` 交给注册中心自动负载均衡，也可以直接写固定具体地址
- **predicate：断言条件，即请求是否允许进入该路由**
- **filter：过滤器，即对请求进行加工处理**

### 使用方式

1. 引入依赖

    ```java
    <dependency>
        <groupId>org.springframework.cloud</groupId>
        <artifactId>spring-cloud-starter-gateway</artifactId>
    </dependency>
    ```

2. 配置 application.yml

    ```yaml
    spring:
      application:
        name: service-gateway
    
      cloud:
        gateway:
        	# 全局跨域配置
          globalcors:
            cors-configurations:
            	# 匹配所有路径：允许所有来源、请求头和请求方法
              '[/**]':
                allowed-origin-patterns: "*"
                allowed-headers: "*"
                allowed-methods: "*"
    
    			# 路由配置
          routes:
            # 商品服务路由
            - id: service-product
              uri: lb://service-product
              predicates:
                - Path=/product/**
              filters:
                - StripPrefix=1
    
            # 订单服务路由
            - id: service-order
              uri: lb://service-order
              predicates:
                - Path=/order/**
              filters:
                - StripPrefix=1
    ```

### Predicate

#### 定义

每一个路由都需要至少一个断言来判断请求是否可以进行当前的路由规则，在底层**每一个断言都是一个函数式接口 Predicate，其中只有一个方法 test，传入请求上下文 ServerWebExchange，返回是否属于当前路由 true / false**

```java
@FunctionalInterface
public interface Predicate<ServerWebExchange> {
    boolean test(ServerWebExchange exchange);
}
```

#### 内置断言工厂

| 断言项目    | 断言名称               | 断言值类型                      | 举例                                             |
| ----------- | ---------------------- | ------------------------------- | ------------------------------------------------ |
| 请求路径    | Path                   | List\<String> 或 String         | - Path=/product/**                               |
| 请求域名    | Host                   | List\<String> 或 String         | - Host=**.dasi.com                               |
| 请求方法    | Method                 | List\<HttpMethod> 或 HttpMethod | - Method=GET,POST                                |
| 请求参数    | Query                  | Tuple<String,String>            | - Query=version,v1                               |
| 请求头      | Header                 | Tuple<String,String>            | - Header=number,\d+                              |
| 请求 cookie | Cookie                 | Tuple<String,String>            | - Cookie=sessionId, abc123                       |
| 请求时间    | After、Between、Before | ZonedDateTime                   | - After=2025-09-15T10:00:00+08:00[Asia/Shanghai] |

#### 自定义断言工厂

**断言工厂是根据 application.yaml 中的配置项来批量生产断言的工厂类**，实际上只需要继承 **AbstractRoutePredicateFactory** 类并实现：

- **工厂类名前缀**：Gateway 强制要求工厂类的名字必须以 RoutePredicateFactory 结尾，而断言名称就是工厂类名去掉 RoutePredicateFactory 后的前缀
- **内部 Config 类**：存放断言工厂的配置参数，一般定义为静态内部类，避免持有外部类引用
- **无参构造方法**：把自己的 Config 类传给父类，父类会负责把 application.yml 中的配置自动绑定到 Config 对象
- **shortcutFieldOrder 方法**：定义了短格式配置参数到 Config 类的绑定顺序，返回的字符串必须与 Config 类字段名完全一致
- **apply 方法**：返回 Predicate\<ServerWebExchange> 对象，只需要实现 test 方法用来设置断言规则，其 Boolean 返回值表示是否命中路由

```java
@Component
public class VipRoutePredicateFactory extends AbstractRoutePredicateFactory<VipRoutePredicateFactory.Config> {
    // 设置配置参数
    @Data
    public static class Config {
        private String param;
        private String value;
    }

    // 绑定内部配置类
    public VipRoutePredicateFactory() {
        super(Config.class);
    }

    // 设置短写法的绑定顺序
    @Override
    public List<String> shortcutFieldOrder() {
        return List.of("param", "value");
    }

    // 设置断言规则
    @Override
    public Predicate<ServerWebExchange> apply(Config config) {
        return exchange -> {
            ServerHttpRequest request = exchange.getRequest();
            String value = request.getQueryParams().getFirst(config.param);
            return value != null && value.equals(config.value);
        };
    }
}
```

#### 底层流程

1. 启动时扫描 Spring 容器里所有实现了 RoutePredicateFactory 接口的 Bean
2. 调用父类 AbstractRoutePredicateFactory 中的绑定方法，根据自定义的类名，将前缀作为断言名称缓存起来
3. 调用父类 AbstractRoutePredicateFactory 中的绑定方法，根据自定义的 shortcutFieldOrder，解析 application.yaml 中的断言项，给自定义的 Config 赋值
4. 执行自定义的 apply 方法，生成一个断言 Predicate\<ServerWebExchange>，并与先前的断言名称绑定
5. 请求到来时，根据断言名称执行断言的 test 方法，其返回的布尔值决定是否命中

### Filter

#### 定义

每一个路由可以配置多个过滤器，过滤器会在请求转发之前和响应返回之后执行相应逻辑，在底层**每一个过滤器都是一个函数式接口 GatewayFilter，其中只有一个方法 filter，传入请求上下文 ServerWebExchange 和过滤器链 GatewayFilterChain，返回包含了过滤逻辑的 Mono 对象**

```java
public interface GatewayFilter extends ShortcutConfigurable {
    Mono<Void> filter(ServerWebExchange exchange, GatewayFilterChain chain);
}
```

#### 内置过滤器工厂

| 过滤器作用            | 过滤器名称        | 配置参数           | 举例                                                 |
| --------------------- | ----------------- | ------------------ | ---------------------------------------------------- |
| 给请求头添加参数      | AddRequestHeader  | name, value        | - AddRequestHeader=X-Request-Id,123                  |
| 给响应头添加参数      | AddResponseHeader | name, value        | - AddResponseHeader=token,abc                        |
| 去掉请求路径的前 N 段 | StripPrefix       | num                | - StripPrefix=1                                      |
| 使用正则重写路径      | RewritePath       | regex, replacement | \- RewritePath=/old/(?\<segment>.*), /new/${segment} |

#### 自定义过滤器工厂

过滤器工厂和断言工厂类似，都是通过配置自动批量生成对应的过滤器，只需要继承 **AbstractGatewayFilterFactory** 类并实现几个部分，不再赘述

```java
@Component
public class TokenGatewayFilterFactory extends AbstractGatewayFilterFactory<TokenGatewayFilterFactory.Config> {
    // 内部配置类
    @Data
    public static class Config {
        private String name;
        private String type;
    }

    // 绑定配置类
    public TokenGatewayFilterFactory() {
        super(Config.class);
    }

    // 定义短格式配置项的绑定顺序
    @Override
    public List<String> shortcutFieldOrder() {
        return List.of("name", "type");
    }

    // 过滤器逻辑
    @Override
    public GatewayFilter apply(Config config) {
        return (exchange, chain) -> {
            // 根据 type 生成不同 token
            String token = switch (config.getType()) {
                case "uuid" -> UUID.randomUUID().toString();
                case "timestamp" -> String.valueOf(System.currentTimeMillis());
                default -> "default-token";
            };

            // 构造带新请求头的 request
            ServerHttpRequest mutatedRequest = exchange.getRequest()
                    .mutate()
                    .header(config.getName(), token)
                    .build();

            // 把新 request 放回 exchange 里
            ServerWebExchange mutatedExchange = exchange.mutate()
                    .request(mutatedRequest)
                    .build();

            // 继续传给下游
            return chain.filter(mutatedExchange);
        };
    }
}
```

#### 底层流程

1. Spring 容器启动时，会扫描所有实现了 GatewayFilterFactory 接口的 Bean

2. Gateway 会调用父类 AbstractGatewayFilterFactory 中的绑定方法，把类名前缀作为过滤器名称缓存起来

3. Gateway 会调用父类 AbstractGatewayFilterFactory 中的绑定方法，根据自定义的 shortcutFieldOrder，把 application.yml 中的过滤器参数映射到 Config 类

4. Gateway 执行自定义工厂的 apply 方法，生成一个 GatewayFilter 对象，并与先前的过滤器名称绑定

5. 当请求经过断言命中路由后，Gateway 会顺序执行当前路由绑定的所有过滤器的 filter 方法



## Seata

### 分布式事务

分布式事务指的是**在分布式系统中，跨多个机器的事务能够表现得像单机事务一样，保证要么全部成功，要么全部失败**

- **全局事务**：跨多个微服务 / 数据源的整体事务，具有全局唯一的 XID
- **分支事务**：每个微服务 / 数据库执行的本地事务
- **事务管理器（Transaction Manager, TM）**：管理全局事务的生命周期，向 TC 申请 XID
- **事务协调者（Transaction Coordinator, TC）**：维护全局事务的状态，协调所有分支事务的提交和回滚
- **资源管理器（Resource Manager, RM）**：向 TC 注册分支事务，执行分支事务，汇报分支事务的执行状态，并根据 TC 指令执行提交和回滚

![img](https://seata.apache.org/zh-cn/assets/images/solution-1bdadb80e54074aa3088372c17f0244b.png)

### 二阶段提交协议 2PC

1. 第一阶段：准备阶段

    - 协调者向所有参与者发送 Prepare 请求，询问事务状态

    - 参与者执行本地事务操作但不会提交，同时对行进行上锁，并写 redo 日志和 undo 日志，如果一切正常就返回 YES，否则返回 NO

2. 第二阶段：提交/回滚阶段
    - 如果所有参与者都返回 YES，那么协调者会向所有参与者发送 Commit 请求，所有参与者提交本地事务，最后清理 undo 日志并释放锁
    - 如果有一个参与者返回 NO 或超时，那么协调者会向所有参与者发送 Rollback 请求，所有参与者根据 undo 日志进行回滚，最后清理 undo 日志并释放锁

### 事务模式

| 模式     | AT                             | XA                             |
| -------- | ------------------------------ | ------------------------------ |
| 提交时机 | 第一阶段立马提交               | 第一阶段不提交                 |
| 一致性   | 最终一致性                     | 强一致性                       |
| 回滚实现 | 依赖业务数据库中的 undo_log 表 | 依赖数据库系统自身的 undo 日志 |
| 2PC 实现 | 由 Seata 在应用层模拟实现      | 数据库内置的 XA 协议实现       |

### 使用方式

1. 引入依赖

    ```xml
    <dependency>
        <groupId>com.alibaba.cloud</groupId>
        <artifactId>spring-cloud-starter-alibaba-seata</artifactId>
    </dependency>
    ```

2. 开启 seata：我这里使用的是 apache-seata-2.1.0，在 bin 目录下直接运行即可

    ```bash
    sh seata-server.sh
    ```

3. 在业务库建 undo_log 表

    ```mysql
    create table undo_log (
        branch_id     bigint       not null, -- 分支事务 id
        xid           varchar(100) not null, -- 全局事务 id
        context       varchar(128) not null, -- 上下文信息
        rollback_info longblob     not null, -- 回滚数据
        log_status    int          not null, -- 日志状态
        log_created   datetime(6)  not null, -- 创建时间戳
        log_modified  datetime(6)  not null, -- 修改时间戳
        constraint ux_undo_log unique (xid, branch_id)
    ) charset = utf8mb4;
    ```

4. 配置 application.yml

    ```yaml
    seata:
      enabled: true
      application-id: seata-business
      tx-service-group: default_tx_group
      service:
        vgroup-mapping:
          default_tx_group: default
        grouplist:
          default: 127.0.0.1:8091
    ```

5. 开启全局事务

    ```java
    @GlobalTransactional
    @Override
    public Result purchase(Long userId, Long storageId, Integer count) {
        // 1. 扣减库存
        Result storageResult = storageFeignClient.deduct(storageId, count);
        if (storageResult.getCode() != 200) {
            log.error("扣减库存失败：userId={}, storageId={}, msg={}", userId, storageId, storageResult.getMsg());
            return storageResult;
        }
    
        // 2. 创建订单
        Result orderResult = orderFeignClient.create(userId, storageId, count);
        if (orderResult.getCode() != 200) {
            log.error("创建订单失败：userId={}, storageId={}, msg={}", userId, storageId, storageResult.getMsg());
            return storageResult;
        }
    
        log.info("添加订单成功：：userId={}, storageId={}, msg={}", userId, storageId, storageResult.getMsg());
        return Result.success();
    }
    ```

6. 开启分支事务

    ```java
    @Transactional
    @Override
    public Result createOrder(Long userId, Long storageId, Integer count) {
        // 1. 获取产品价格
        Result priceResult = storageFeignClient.getPrice(storageId);
        if (priceResult.getCode() != 200) {
            log.error("获取价格失败：userId={}, storageId={}, msg={}", userId, storageId, priceResult.getMsg());
            return priceResult;
        }
        BigDecimal price = new BigDecimal(priceResult.getData().toString());
    
        // 2. 扣减余额
        BigDecimal money = price.multiply(BigDecimal.valueOf(count));
        Result accountResult = accountFeignClient.deduct(userId, money);
        if (accountResult.getCode() != 200) {
            log.error("扣减余额失败：userId={}, storageId={}, msg={}", userId, storageId, accountResult.getMsg());
            return accountResult;
        }
    
        // 3. 保存订单
        Order order = new Order();
        order.setUserId(userId);
        order.setStorageId(storageId);
        order.setCount(count);
        order.setMoney(money);
        order.setCreateTime(LocalDateTime.now());
        save(order);
    
        log.info("添加订单成功：{}", order);
        return Result.success(order);
    }
    //---------------------------------------------------
    @Transactional
    @Override
    public Result deduct(Long storageId, Integer count) {
        // 1. 获取库存
        Storage storage = getById(storageId);
    
        // 2. 检验库存
        if (storage == null) {
            return Result.fail("商品不存在！");
        }
        Integer old_residue = storage.getResidue();
        if (old_residue < count) {
            return Result.fail("商品库存不足！");
        }
    
        // 3. 扣减库存
        Integer new_residue = old_residue - count;
        storage.setResidue(new_residue);
        updateById(storage);
    
        log.info("商品 {} 的库存从 {} 扣减到了 {}", storageId, old_residue, new_residue);
        return Result.success();
    }
    //---------------------------------------------------
    @Transactional
    @Override
    public Result deduct(Long userId, BigDecimal money) {
        // 1. 获取账户
        Account account = getById(userId);
    
        // 2. 检验账户
        if (account == null) {
            return Result.fail("用户不存在！");
        }
        BigDecimal old_balance = account.getBalance();
        if (old_balance.compareTo(money) < 0) {
            return Result.fail("用户余额不足！");
        }
    
        // 3. 扣减余额
        BigDecimal new_balance = old_balance.subtract(money);
        account.setBalance(new_balance);
        updateById(account);
    
        log.info("用户 {} 的余额从 {} 扣减到了 {}", userId, old_balance, new_balance);
        return Result.success();
    }
    ```