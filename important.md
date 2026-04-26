
* [Spring](#spring)
* [JVM](#jvm)
* [Redis](#redis)

## Spring

Bean 的生命周期？

为什么推荐构造器注入？

为什么需要三级缓存？

JDK 代理和 CGLIB 代理的区别？

DispatcherServlet 的处理流程？

\#{} 和 \${} 的区别是什么？

利用 MyBatis 需要做什么工作？

MyBatis-Plus 比 MyBatis 做了哪些增强？

maven 如何使用 pom.xml？

fat jar 结构是什么？

@SpringBootApplication 有哪些注解组成？

自动配置机制？

SpringBoot 比原生 Spirng 做了哪些增强？

SpringApplication.run() 流程？

## JVM

栈帧内存布局是什么？

类元信息的内存布局是什么？

运行时常量池的内存布局是什么？

对象的内存布局是什么？

字符串字面量在整个过程中是如何被解析的？

如何利用动态链接实现多态的？

为什么需要双亲委派机制？

类的加载过程？

对象的创建过程？

能作为 GC Roots 的对象有哪些？

三种 GC 算法？

哪些情况会进入老年代？

有哪些垃圾回收器？

## Redis

String = SDS 的结构和意义？

List = ziplist / listpack 的结构和意义？

Hash / Set = ziplist + hashtable 的结构和意义？

ZSet = hashtable + skiplist 的结构和意义？

Redis 的事务机制有什么特性？

RDB 和 AOF 的机制？

AOF 写回、重写和重放分别是什么意思？

主从复制的流程？

哨兵如何解决单点故障？

集群的意义是什么？

双写并发如何破坏一致性？

双写一致性的策略是什么？

Cache 穿透是什么？如何解决？

Cache 击穿是什么？如何解决？

Cache 雪崩是什么？如何解决？

限流是什么？

熔断是什么？

降级是什么？

为什么 Redis 这么快？

