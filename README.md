# README



## Overview

个人学习笔记仓库，主要涵盖 **Java 基础、Web 开发、Spring 框架、八股、数据、运维** 等主题。



## Contents

### ☕️ JavaSE

- [Grammar](Backend/JavaSE/Grammar.md)：初识 Java、package、main、Java 开发流程、基础语法
- [OOP](Backend/JavaSE/OOP.md)：封装、继承、多态、重载、重写、Object 类、static、codeblock、加载顺序、interface
- [Class](Backend/JavaSE/Class.md)：Math、Arrays、System、BigDecimal、LocalDateTime、Enum、Exception、Wrapper、StringBuffer、Pattern、Matcher
- [Collection&Map](Backend/JavaSE/Collection&Map.md)：数组与集合、框架体系、Collection、Map、遍历手段、接口方法
- [Core](Backend/JavaSE/Core.md)：I/O、泛型、线程、反射、网络、JDBC

### 🌐 Web

- [HTML](Backend/Web/HTML.md)：初识 Web 开发、超文本标记语言、结构、文本/列表/表格标签、多媒体标签、表单标签
- [CSS](Backend/Web/CSS.md)：样式、语法、选择器、优先级、文本属性、盒子模型、盒子排版
- [JavaScript](Backend/Web/JavaScript.md)：语法、JSON、BOM、DOM、Event、Ajax、ES6
- [Vue](Backend/Web/Vue.md)：前端工程化、Vue 框架、.vue 文件、模版语法、参数传递、路由、异步编程、CORS、Pinia 状态存储、Element-Plus
- [JavaWeb](Backend/Web/JavaWeb.md)：Web 应用、HTTP、Tomcat、路径配置、Servlet、Request、Response、Session、Listener、Filter

### 🍃 Spring

- [SpringFramework](Backend/Spring/SpringFramework.md)：全家桶介绍、Bean、IoC、AOP、JDBC、Resource、Validator、Junit、Maven
- [SpringMVC](Backend/Spring/SpringMVC.md)：架构介绍、基于 web.xml 和 springMVC.xml 配置、基于注解配置、@RequestMapping、拦截器、异常处理器、请求域共享数据、视图映射、数据读入与写出、文件下载与上传
- [MyBatis](Backend/Spring/MyBatis.md)：Mapper、mybatis-config.xml、传递值、返回值、多表映射、动态语句、批量执行、分页机制 
- [MyBatis-Plus](Backend/Spring/MyBatis-Plus.md)：BaseMapper、IService、Wrapper、实体类注解、MyBatisX
- [SSM](Backend/Spring/SSM.md)：依赖整理、全注解配置、编码流程
- [SpringBoot](Backend/Spring/SpringBoot.md)：pom.xml、application.yml、启动类、读取配置、项目打包、整合 SSM
- [SpringCloud](Backend/Spring/SpringCloud.md)：单机/集群/分布式架构、微服务定义、Nacos Discovery、Nacos Config、OpenFeign、Sentinel、Gateway、Filter、Seata
- [SpringSecurity](/Backend/SpringSecurity.md)：待学习...

### 🛠 Middleware

- [Redis](Backend/Middleware/Redis.md)：缓存、基本命令、九大数据类型、Persistence、Transaction、Pipeline、Replication、Sentinel、Cluster、SpringBoot 集成、BigKey、双写一致性、高级数据结构应用、Lua、分布式锁、三大问题与三大方案、过期策略、底层分析
- [RabbitMQ](Backend/Middleware/RabbitMQ.md)：消息中间件、体系架构、交互流程、SpringBoot 集成、消息可靠性、延迟消息、优先级队列
- [Kafka](Backend/Middleware/Kafka.md)：待学习...
- [Elasticsearch](Backend/Middleware/Elasticsearch.md)：待学习...

### 🚀 Projects

- [苍穹外卖](Backend/Project/苍穹外卖.md)：项目设计、代码设计、DTO 和 VO、业务处理、Nginx、RESTful、PageHelper、SLF4J、JWT、Swagger、OSS、@AutoFill、@ExceptionHandler、HttpClient、SpringCache、SpringTask、WebSocket、ECharts、POI
- [黑马点评](Backend/Project/黑马点评.md)：Nginx 代理、令牌拦截器、序号生成器、防穿透、防击穿、防竞争、滚动分页、位置查询、签到记录、访问统计

### 📚 八股

- [JVM](Theory/JVM.md)：JDK、JRE、JVM、内存布局、栈、堆、元空间、新生代、老年代、直接内存、对象内存、对象创建过程、垃圾回收、存活判定、GC 算法、垃圾收集器、类文件、类加载过程、类加载器、JVM 参数
- [JUC](Theory/JUC.md)：进程与线程、Thread API、Monitor、生命周期、多线程、JMM、线程安全、deadlock、consistency、volatile、synchronized、CAS、JUC、ReentrantLock、Atomic、Future、CompletableFuture、ThreadPoolExecutor、ThreadLocal、AQS
- [JCF](Theory/JCF.md)：比较器、Collection、stream、iterator、List、ArrayList、LinkedList、Set、Queue、BlockingQueue、Map、HashMap、ConcurrentHashMap、集合使用规范
- [MySQL](Theory/MySQL.md)：基本概念、层级架构、字段类型、日志、事务、锁、MVCC、索引、存储结构、性能优化、SQL 优化
- [设计模式](Theory/DesignMode.md)：SOLID 原则、设计模式、工厂、单例、代理、观察者、适配器、装饰器、责任链、策略、状态
- [计算机网络](Theory/Network.md)：OSI 七层模型、HTTP、DNS、TCP、IP、NAT、ARP、网关、访问 URL 全流程
- [操作系统](Theory/OS.md)：内核、用户态和内核态、系统调用、进程、PCB、IPC、进程调度算法、特殊进程、死锁处理、内存分配、虚拟内存、缺页错误、页面置换算法、inode、链接、磁盘调度算法
- [Linux](Theory/Linux.md)：Linux 内核、Linux 发行版、命令、命令执行过程、环境变量、文件系统、目录结构、文件管理、文本管理、权限管理、用户管理、用户组管理、进程管理、软件包管理、系统信息查询
- [Shell](Theory/Shell.md)：命令行解释器和脚本、执行方式、内建命令、输入输出机制、变量、数组、运算符、流程控制、函数
- [分布式](Theory/Distributed.md)：待学习...
- [高性能](Theory/Performance.md)：待学习...
- [高可用](Theory/Availability.md)：待学习...

### 🧠 算法

- [树](Algorithm/Tree.md)：

### ⚙️ DevOps

- [Docker](DevOps/Docker.md)：待学习...
- [Kubernetes](DevOps/Kubernetes.md)：待学习...
- [Prometheus](DevOps/Prometheus.md)：待学习...

### 📊 Data Analysis

- [NumPy](Data/NumPy.md)：属性、数据类型、切片、索引、广播、迭代、修改形状、翻转、连接、分割、添加删除、字符串运算、数学运算、统计运算、线性代数运算、条件筛选运算
- [Pandas](Data/Pandas.md)：Series、DataFrame、CSV 操作、JSON 操作、数据清洗、缺失值处理、重复值处理、异常值处理、替换值处理、数据预处理、格式转换、数值处理、类别处理、数据抽样、排序、聚合、透视、时间序列分析、性能优化
- [Matplotlib](Data/Matplotlib.md)：plot、subplot、scatter、bar、barh、pie、hist、im



## Learning Path

1. JavaSE

- [x] 04.14：Core、OOP
- [x] 04.15：异常、接口、包装类、枚举类
- [x] 04.16：工具类、集合、泛型
- [x] 04.17：线程、坦克 Demo1.0
- [x] 04.18：I/O、流、坦克 Demo2.0
- [x] 04.19：网络
- [x] 04.20：多用户消息 Demo1.0
- [x] 04.21：多用户消息 Demo2.0
- [x] 04.22：反射、MySQL、JDBC、Druid
- [x] 04.23：DAO、正则表达式、满汉楼 Demo

2. JavaWeb

- [x] 04.24：HTML、CSS、JS
- [x] 04.25：BOM、登陆页面 Demo
- [x] 04.26：Tomcat、HTTP、Servlet
- [x] 04.28：XML、日程管理 Demo1.0
- [x] 05.07：Session、Cookie、域、日程管理 Demo2.0
- [x] 05.08：Filter、Listener、ajax、日程管理 Demo4.0
- [x] 05.09：ES6、npm、Vite
- [x] 05.11：Vue、pinia
- [x] 05.12：route、SPA、axios、日程管理 Demo5.0
- [x] 05.13：日程管理 Demo7.0

3. SpringFramework

- [x] 05.14：Bean
- [x] 05.15：IoC-XML
- [x] 06.04：IoC-Annotation
- [x] 06.06：IoC 底层
- [x] 06.07：AOP
- [x] 06.08：Junit、JDBCTemplate
- [x] 06.09：Transactional、Resource
- [x] 06.11：i18n、Validator
- [x] 06.12：Maven、Log4j、Junit

4. SpringMVC

- [x] 08.06：RequestMapping、web.xml、Thymeleaf
- [x] 08.07：ModelAndView、RESTful、消息转换器
- [x] 08.08：Interceptor、异常处理器

5. Mybatis

- [x] 08.10：Mapper、多表映射、动态 SQL
- [x] 08.11：批量执行、分页机制、SSM、任务列表 Demo
- [x] 08.12：BaseMapper、IService、Wrapper、实体类注解

6. SpringBoot

- [x] 08.13：Main、application.yaml、整合 SSM、MyBatisX

7. 苍穹外卖

- [x] 08.15：环境搭建、接口测试搭建、项目结构搭建
- [x] 08.16：B 端（员工/分类/菜品/套餐/上传/店铺）、Redis
- [x] 08.17：C 端（微信/分类/菜品/套餐/店铺/购物车/地址）
- [x] 08.18：C 端（订单/支付）、B 端（订单）、WebSocket
- [x] 08.19：B 端（数据/工作台/导出）、完善、测试
- [x] 08.20：项目总结

8. Redis

- [x] 08.24：概念、数据结构
- [x] 08.25：持久化、事务、管道
- [x] 08.26：复制、哨兵、集群
- [x] 08.27：Spring 集成、BigKey、双写一致性、Canal
- [x] 08.28：Geo/BitMap/HyperLogLog 原理、三大问题、三大兜底
- [x] 08.29：BloomFilter、分布式锁、Redlock、Redisson
- [x] 08.30：过期策略、I/O 多路复用

9. RabbitMQ

- [x] 08.31：Docker、消息中间件、体系结构、Spring 集成
- [x] 09.01：消息可靠性、延迟消息、优先级队列

10. 黑马点评

- [x] 09.02：环境搭建、项目结构搭建、用户登录登出、安全查缓存
- [x] 09.03：秒杀库存、分布式锁、消息队列
- [x] 09.04：点赞、排行榜、共同关注、推送、滚动分页
- [x] 09.05：附近商户、用户签到、UV、PV
- [x] 09.06：笔记总结
- [x] 09.09：笔记总结

11. SpringCloud

- [x] 09.10：概念、分布式架构、Nacos Discovery
- [x] 09.11：Nacos Config、OpenFeign
- [x] 09.12：Sentinel、Gateway
- [x] 09.13：Seata
- [x] 09.14：笔记总结
- [x] 09.15：笔记总结、搬迁到 Github

12. 八股

- [x] 09.16：【JVM】内存布局
- [x] 09.17：【JVM】垃圾回收
- [x] 09.18：【JVM】类加载
- [x] 09.19：【并发编程】Thread、多线程、synchronized、volatile
- [x] 09.21：【并发编程】JUC、ThreadLocal、AQC
- [x] 09.22：【集合框架】Collection、List、Set、Queue
- [x] 09.23：【集合框架】Map、HashMap、ConcurrentHashMap
- [x] 09.24：【MySQL】基本概念与基本命令
- [x] 09.25：【MySQL】层级架构、字段类型、日志、锁
- [x] 09.26：【MySQL】MVCC、索引、存储结构、性能优化、SQL 优化
- [x] 09.28：【设计模式】工厂、单例、代理、观察者、适配器、装饰器、责任链、策略、状态
- [x] 09.29：【计算机网络】网络分层模型、HTTP、DNS
- [x] 09.30：【计算机网络】TCP
- [x] 10.01：【计算机网络】IP、NAT、ARP、网关
- [x] 10.04：【操作系统】内核、进程、死锁
- [x] 10.08：【操作系统】内存管理、文件系统
- [x] 10.09：【Linux】内核与发行版、命令、文件系统、环境变量、基本命令、包管理、系统信息查询
- [x] 10.10：【Shell】命令行解释器和脚本、脚本执行、变量、数组、运算符、流程控制、函数
- [ ] 10.11：



## ToDo

1. 待学习：八股、SpringSecurity、Linux、Docker、K8s、Kafka、Prometheus、Elasticsearch
2. 将博客笔记转移到 Github
3. 学成在线项目
4. 独立研发消息中台项目
5. 笔记交易平台项目作为毕设



## About me

💻 Major: [Computer Science](https://cse.sysu.edu.cn/)  

📦 Repo：[Github](https://github.com/dasi0227/Notes) ｜ [Gitee](https://gitee.com/dasi0227/Notes)

📮 Email: [dasi0227@qq.com](mailto:dasi0227@qq.com)

🌐 Blog: [dasi.plus](https://dasi.plus)

🧑‍💻 CSDN：[dasi0227](https://blog.csdn.net/m0_74766888)