# Notes

## Overview

个人学习笔记仓库，主要涵盖 **Java 基础、Web 开发、Spring 框架、前端、数据库、数据分析**等主题。

## Contents

- ☕️ JavaSE
  - to be updated

- 🌐 Web
  - to be updated

- 🍃 Spring
  - [SpringFramework：全家桶介绍、Bean、IoC、AOP、JDBC、Resource、Validator、Junit、Maven](Backend/Spring/SpringFramework.md)  
  - [SpringMVC：架构介绍、基于 web.xml 和 springMVC.xml 配置、基于注解配置、@RequestMapping、拦截器、异常处理器、请求域共享数据、视图映射、数据读入与写出、文件下载与上传](Backend/Spring/SpringMVC.md)  
  - [MyBatis：Mapper、mybatis-config.xml、传递值、返回值、多表映射、动态语句、批量执行、分页机制](Backend/Spring/MyBatis.md)  
  - [MyBatis-Plus：BaseMapper、IService、Wrapper、实体类注解、MyBatisX](Backend/Spring/MyBatis-Plus.md)  
  - [SSM：依赖整理、全注解配置、编码流程](Backend/Spring/SSM.md)  
  - [SpringBoot：pom.xml、application.yml、启动类、读取配置、项目打包、整合 SSM](Backend/Spring/SpringBoot.md)  
  - [SpringCloud：单机/集群/分布式架构、微服务定义、Nacos Discovery、Nacos Config、OpenFeign、Sentinel、Gateway、Filter、Seata](Backend/Spring/SpringCloud.md)  

- 🛠 Middleware
  - [Redis：缓存、基本命令、九大数据类型、Persistence、Transaction、Pipeline、Replication、Sentinel、Cluster、SpringBoot 集成、BigKey、双写一致性、高级数据结构应用、Lua、分布式锁、三大问题与三大方案、过期策略、底层分析](Backend/Middleware/Redis.md)
  - [RabbitMQ：消息中间件、体系架构、交互流程、SpringBoot 集成、消息可靠性、延迟消息、优先级队列](Backend/Middleware/RabbitMQ.md)  

- ⚙️ DevOps

  - Linux
  - Docker

- 🚀 Projects  

  - [Sky-Take-Out](Backend/苍穹外卖.md)  
  - [黑马点评](Backend/黑马点评.md)  

- 📊 Data Analysis

    - [NumPy](Data/DataAnalysis/NumPy Note.md)  

    - [Pandas](Data/DataAnalysis/Pandas Note.md)  

    - [Hadoop](Data/hadoop/hadoop.md)  


## Learning Path

1. JavaSE

    - 04.14：Core、OOP

    - 04.15：异常、接口、包装类、枚举类

    - 04.16：工具类、集合、泛型

    - 04.17：线程、坦克Demo1.0

    - 04.18：I/O、流、坦克Demo2.0

    - 04.19：网络

    - 04.20：多用户消息Demo1.0

    - 04.21：多用户消息Demo2.0

    - 04.22：反射、MySQL、JDBC、Druid

    - 04.23：DAO、正则表达式、满汉楼Demo

2. JavaWeb

    - 04.24：HTML、CSS、JS

    - 04.25：BOM、登陆页面Demo

    - 04.26：Tomcat、HTTP、Servlet

    - 04.28：XML、日程管理Demo1.0

    - 05.07：Session、Cookie、域、日程管理Demo2.0

    - 05.08：Filter、Listener、ajax、日程管理Demo4.0

    - 05.09：ES6、npm、Vite

    - 05.11：Vue、pinia

    - 05.12：route、SPA、axios、日程管理Demo5.0

    - 05.13：日程管理Demo7.0

3. SpringFramework

    - 05.14：Bean

    - 05.15：IoC-XML

    - 06.04：IoC-Annotation

    - 06.06：IoC 底层

    - 06.07：AOP

    - 06.08：Junit、JDBCTemplate

    - 06.09：Transactional、Resource

    - 06.11：i18n、Validator

    - 06.12：Maven、Log4j、Junit

3. SpringMVC

    - 08.06：RequestMapping、web.xml、Thymeleaf

    - 08.07：ModelAndView、RESTful、消息转换器

    - 08.08：Interceptor、异常处理器

4. Mybatis

    - 08.10：Mapper、多表映射、动态 SQL

    - 08.11：批量执行、分页机制、SSM、任务列表Demo
    - 08.12：BaseMapper、IService、Wrapper、实体类注解

5. SpringBoot
    - 08.13：Main、application.yaml、整合 SSM、MyBatisX

6. 苍穹外卖

    - 08.15：环境搭建、接口测试搭建、项目结构搭建

    - 08.16：B端（员工/分类/菜品/套餐/上传/店铺）、Redis

    - 08.17：C端（微信/分类/菜品/套餐/店铺/购物车/地址）

    - 08.18：C端（订单/支付）、B端（订单）、WebSocket

    - 08.19：B端（数据/工作台/导出）、完善、测试

    - 08.20：项目总结

7. Redis

    - 08.24：概念、数据结构

    - 08.25：持久化、事务、管道

    - 08.26：复制、哨兵、集群

    - 08.27：Spring 集成、BigKey、双写一致性、Canal

    - 08.28：Geo/BitMap/HyperLogLog 原理、三大问题、三大兜底

    - 08.29：BloomFilter、分布式锁、Redlock、Redisson

    - 08.30：过期策略、I/O 多路复用

8. RabbitMQ

    - 08.31：Docker、消息中间件、体系结构、Spring 集成

    - 09.01：消息可靠性、延迟消息、优先级队列

9. 黑马点评

    - 09.02：环境搭建、项目结构搭建、用户登录登出、安全查缓存

    - 09.03：秒杀库存、分布式锁、消息队列

    - 09.04：点赞、排行榜、共同关注、推送、滚动分页

    - 09.05：附近商户、用户签到、UV、PV

    - 09.06：笔记总结

    - 09.09：笔记总结

10. SpringCloud

    - 09.10：概念、分布式架构、Nacos Discovery

    - 09.11：Nacos Config、OpenFeign

    - 09.12：Sentinel、Gateway

    - 09.13：Seata

    - 09.14：笔记总结

    - 09.15：笔记总结

To Be Continued...

## TODO

1. 将博客笔记转移到 github 保存
2. 学成在线项目
3. 独立研发消息中台
4. 笔记交易平台作为毕设

## About me

🎓 School: SYSU

💻 Major: Computer Science  

💬 WeChat: WanDasi24  

📧 Email: [dasi0227@qq.com](mailto:dasi0227@qq.com) | [wanyw0227@gmail.com](mailto:wanyw0227@gmail.com)  

🌐 Blog: [https://dasi.plus](https://dasi.plus)  