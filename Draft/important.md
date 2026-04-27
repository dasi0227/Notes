## Spring


Bean 的生命周期？
```text
1. 实例化: 先字段初始化，然后调用构造函数
2. 依赖注入: 注入依赖的 Bean
3. 前置处理: 遍历所有实现 BeanPostProcessor 接口的对象，执行 postProcessBeforeInitialization 方法
4. 初始化: 
		1. 调用 @PostConstruct 注解的方法 
		2. 调用 InitializingBean 接口的 afterPropertiesSet 方法 
		3. 调用 @Bean 声明的 initMethod
5. 后置处理: 遍历所有实现 BeanPostProcessor 接口的对象，执行它们的 postProcessAfterInitialization方法
6. 可用: 被放入一级缓存
7. 销毁: 
		1. 调用 @PreDestroy 注解的方法 
		2. 调用 DisposableBean 接口的 destroy 方法
    3. 调用 @Bean 声明的 destroyMethod
```


为什么推荐构造器注入？
```text
1. 支持手动 new: 字段注入必须依赖 IoC 容器，如果需要手动 new 创建对象，则字段注入会失效成为 null，而构造器注入恰好确保了手动 new 也要求传递完整参数
2. 暴露循环依赖: 字段注入通过三级缓存允许注入尚未初始化完全的 Bean，容忍循环依赖，而构造器注入发生在实例化，此时工厂还未放在三级缓存中，因此强制要求注入的 Bean 必须可用，否则启动时会报错
3. 支持 final: 字段注入底层是 Spring 利用反射实现，final 字段无法被正常反射赋值，而构造器本身就适配 final 的不可变性
支持单元测试: 字段注入必须依赖 IoC 容器或手动实现反射，而构造器可以直接传递 Mock 对象
```


为什么需要三级缓存？
```text
三级缓存是为了解决单例 Bean 的循环依赖（A->B->A）的问题：A 会等待 B 初始化完成，B 又会等待 A 初始化完成，则会卡住无法进行。
因此当创建 A 之后，不会直接将半成品 A 放入缓存，而是将 A 的工厂放入第三级缓存，当 A 被循环需要的时候，才会调用工厂的 getEarlyBeanReference() 决定是 A 应该创建为代理对象还是原始对象，然后将这个早期 Bean 放入第二级缓存提供给 B 使用，从而让 B 继续初始化，最后让 A 继续初始化。 
而之所以不在一开始就直接调用 getEarlyBeanReference()，是因为其破坏了 Bean 的正常生命周期，属于一种迫不得已的特殊暴露机制，而循环依赖的发生率又比较低，因此应该在确实发生循环依赖、必须提前注入 Bean 时，Spring 才会按需调用它，否则 Bean 应当按照正常生命周期走完。
```


JDK 代理和 CGLIB 代理的区别？
```text
JDK 代理: 通过实现与目标类相同的接口来实现代理，要求目标类必须有接口，且只能代理接口有的方法
CGLIB 代理: 通过生成目标类的子类并重写方法来实现代理，要求目标类必须不是 final，且只能代理目标类非 final/private 的方法
```


DispatcherServlet 的处理流程？
```text
1. 拿到处理链: 通过请求中的 URL，调用 HandlerMapping 的方法拿到处理链 HandlerExecutionChain
2. 拿到适配器: 先从 HandlerExecutionChain 中拿到处理器 Handler，然后遍历所有 HandlerAdapter，拿到第一个支持的适配器
3. 执行拦截器的前置逻辑: 调用 HandlerExecutionChain 中的 applyPreHandle 方法
4. 执行适配器和处理器: 利用适配器，根据 HttpServletResquest 和 HttpServletResponse，调用处理器的 Controller 方法
5. 执行拦截器的后置逻辑: 调用 HandlerExecutionChain 中的 applyPostHandle 方法
6. 视图渲染: 如果返回的是视图名称，会利用 ViewResolver 查找并渲染视图
7. 执行拦截器的结束逻辑: 调用 HandlerExecutionChain 中的 triggerAfterCompletion 方法
```


\#{} 和 \${} 的区别是什么？
```text
#{}: 利用预编译和参数绑定，先利用占位符 ? 代替参数值，然后生成执行计划，执行的时候才绑定到具体的参数值
${}: 利用字符串拼接 sql 语句，参数值直接影响执行计划，会有 SQL 注入风险
```


利用 MyBatis 需要做什么工作？
```text
1. 扫描注册: 根据 @MapperScan("...")，会找到所有被 @Mapper 注解标记的接口
2. 代理创建: 使用 MapperFactoryBean 为每个 Mapper 接口创建 JDK 动态代理对象
3. 方法解析: 先从 mapper.xml 文件或 @Select 等注解中查找对应的 sql 语句来执行，然后使用内部持有的 SqlSession 执行，并将返回结果映射为对象
```


MyBatis-Plus 比 MyBatis 做了哪些增强？
```text
1. 继承泛型接口: MyBatis-Plus 提供 BaseMapper<T> 泛型接口，内部预定义了通用的 CRUD 方法，用户自定义 Mapper 接口只需要继承并指明实体类型，MyBatis-Plus 就会通过 JDK 动态代理生成实现类，并通过 SqlInjector 自动注入对应的 SQL 语句
2. 实体类映射: 在实体类中利用 @TableName 映射表名，@TableId 映射主键（type 属性可以指定主键生成策略），@TableField 映射列名（exist 属性可以指定是否属于库表）
3. 条件构造器: Mybatis-Plus 提供 LambdaQueryWrapper/LambdaUpdateWrapper/LambdaDeleteWrapper 条件构造器，可以链式调用 eq, like 等方法构造条件，并在运行时动态解析为 SQL 语句
4. 分页增强: 在配置类通过 @Bean 注册一个 MybatisPlusInterceptor 对象，并在该对象中添加 PaginationInnerInterceptor 对象，实际上它会拦截分页方法，根据传递的 Page 对象的配置，先执行 COUNT * 查询，再给即将执行的查询方法拼接上 LIMIT offset size，最后将两个查询的结果封装回 Page 对象返回
5. Lambda 字段解析: MyBatis-Plus 并没有执行这个 Lambda 方法，而是通过序列化拿到类名和方法名，将 getter 解析为字段名，然后通过类的反射检查字段上的 @TableField 注解，从而拿到库表列名
```


maven 如何使用 pom.xml？
```text
1. 读取: 读取项目根目录下的 pom.xml 文件
2. 解析: 解析 pom.xml 中 <dependencies> 标签声明的依赖坐标 groupId + artifactId + version，只从远程仓库下载该依赖的 pom 文件进行递归解析，构建完整的依赖树
3. 查找: 根据依赖树，去本地仓库 ~/.m2/repository/groupId/artifactId/version/ 目录下，查找 jar 包是否存在，如果不存在则从远程仓库下载
```


fat jar 结构是什么？
```text
META-INF/MANIFEST.MF: jar 包的启动说明书，包含 Main-Class（jar 包从哪里运行） 和 Start-Class（应用从哪里运行）
BOOT-INF/classes/: src/main/java/ 下编译的 .class 文件 + src/main/resource/ 下的配置文件和静态文件
BOOT-INF/lib/: Maven 递归解析 pom.xml 得到的所有第三方依赖的 jar 包
org/springframework/boot/loader/: Spring Boot 的类加载器 LaunchedClassLoader，让 JVM 具备加载嵌套 jar 的能力
```


@SpringBootApplication 有哪些注解组成？
```text
@Configuration: 标记当前类是配置类，允许使用 @Bean 定义额外的 Bean
@ComponentScan: 默认扫描当前类所在包及其子包，自动注册注解了的类到 IoC 容器
@EnableAutoConfiguration: 触发自动配置机制，将需要的配置类注册到 IoC 容器
```


自动配置机制？
```text
1. 导入: 解析 @EnableAutoConfiguration 带有 @Import(AutoConfigurationImportSelector.class)，触发实例化
2. 扫描: 该对象会调用 selectImports() 方法，扫描所有 jar 包下存在的 META-INF/spring/org.springframework.boot.autoconfigure.AutoConfiguration.imports 文件
3. 读取: 读取文件每一行的配置类的全限定名得到列表
4. 过滤: 根据 @ConditionalOnClass（存在指定类） / @ConditionalOnMissingBean（不存在指定对象） / @ConditionalOnProperty（存在属性值），筛选得到满足条件的配置类
5. 排序: 根据 @AutoConfigureOrder / @AutoConfigureAfter / @AutoConfigureBefore，对配置类进行依赖排序
6. 注册: 将配置类注册为 BeanDefinition
```


SpringBoot 比原生 Spirng 做了哪些增强？
```text
1. 自动配置: 提供了自动配置机制，只需在 application.yml 中填写少量配置项，框架就能基于约定自动完成大部分配置 ➡️ 不再需要手动编写 XML 文件或大量配置类
2. 依赖管理: 提供了各类 starter，每个 starter 通过自己的 pom.xml 预先组织好一组经过兼容性验证的相关依赖及其版本，依靠 Maven 的递归解析添加到 classpath ➡️ 不再需要检查版本冲突
3. Web 支持: SpringBoot 提供了 Tomcat 容器，Web 应用在打包后可直接以 java -jar 方式独立运行 ➡️ 不再需要手动部署到外置 Tomcat
4. 配置多样: SpringBoot 提供了外部化配置机制，支持命令行参数（--xxx=） > 系统属性（-Dxxx=） > 环境变量（export Xxx=） > 多环境配置文件（application.yml）等多种方式
5. 增强支持: SpringBoot 提供了 Actuator 组件，可让应用自动暴露多种运维端点，方便监控和管理；还提供 devtools 工具，可让应用自动重启和热更新，方便开发
```


SpringApplication.run() 流程？
```text
1. 创建启动类对象: 创建 SpringApplication 实例，并推断应用类型是 Servlet（webmvc）/ Reactive（webflux），加载初始化器 ApplicationContextInitializer 和监听器 ApplicationListener
2. 创建环境对象: 按照命令行参数 > 环境变量 > 配置文件读取配置参数，统一放到 Environment 对象之中
3. 创建 IoC 容器对象: 根据第 1 步推断出来的应用类型，创建对应的 ApplicationContext 实例
4. 初始化 IoC 容器: 先将第 2 步创建的 Environment 对象设置到容器，然后执行第 1 步中加载的 ApplicationContextInitializer，最后注册容器的启动类为 @SpringBootApplication 注解的类
5. 刷新 IoC 容器和 Web 容器: 扫描所有 @Component / @Configuration / @Bean，生成 BeanDefinition 放在 BeanFactory 中，然后提前实例化 BeanPostProcessor，最后依次遍历进行创建、注入和初始化: 创建内嵌的 Tomcat 容器，设置端口和环境，然后注册 DispatcherServlet 到 IoC 容器中，最后启动 Tomcat
6. 发布事件: 发布 ContextRefreshedEvent 和 ApplicationStartedEvent 事件
7. 执行 Runner: 执行 ApplicationRunner 和 CommandLineRunner，拿到命令行参数，完成启动后的自定义逻辑
8. 发布事件: 发布 ApplicationReadyEvent 事件
```


## JVM


栈帧内存布局是什么？
```text
局部变量表: 方法参数和局部变量
操作数栈: 计算过程中的中间结果
动态链接: 指向方法所属类的运行时常量池
方法返回地址: 记录当前方法被调用的指令位置，即方法执行完后的返回地址
```


类元信息的内存布局是什么？
```text
类信息: 类名、父类、接口、修饰符
字段信息: 字段名、类型、修饰符
方法信息: 方法名、参数列表、返回值、修饰符、字节码
_java_mirror: 堆中的 Class 对象引用
_class_loader: 堆中的类加载器对象引用
```


运行时常量池的内存布局是什么？
```text
引用：类引用、方法引用、字段引用
字面量：字符串和基本类型
```


对象的内存布局是什么？
```text
对象头-标记字段: 运行时的动态信息，如哈希码、GC 分代年龄和锁状态
对象头-类型指针: 指向元空间里面的类元信息
实例数据: 对象字段值，即基本类型值和引用
```


字符串字面量在整个过程中是如何被解析的？
```text
编译: String s = "hello" 会被编译成 ldc #2
解析: JVM 首次执行 ldc #2 时发现 #2 没有被解析过，因此去字符串常量池查找是否存在对象引用，如果不存在则创建一个 String 对象，最后将该对象引用缓存到 #2 对应的条目中
运行: JVM 之后执行到 ldc #2 会直接取缓存好的对象引用，不再去查字符串常量池
```


如何利用动态链接实现多态的？
```text
1. 找方法: 根据运行时常量池中的符号引用，解析得到类中方法表的槽位
2. 找对象: 从操作数栈中拿到对象引用
3. 找类型: 根据对象头的类型指针，拿到对象所属类的类元信息地址
4. 找实现: 根据类元信息地址和方法在类中的槽位，在虚方法表中定位最终方法的地址
```


为什么需要双亲委派机制？
```text
唯一性: 不同的类加载器加载同一个类文件，JVM 会认为是两个不同的类，双亲委派确保了类文件对应的类全局唯一
安全性: 确保核心类库只能由 BootstrapClassLoader 加载，防止用户破坏核心类的加载机制
```


类的加载过程？
```text
1. 加载: 先根据类加载器 + 类的全限定名检查该加载器是否已经加载过这个类，如果加载过就直接返回，否则会读取 .class 到内存，组织成元空间中的类元信息和运行时常量池，同时在堆中生成对应的 Class 对象
2. 验证: 确保字节码符合 JVM 规范
3. 准备: 为类的 static 字段分配内存并赋零值，而 static final 字段会直接赋常量值
4. 解析: 将运行时常量池中的符号引用解析为直接引用
5. 初始化: 在首次使用该类的时候触发 <clinit> 方法，对静态变量进行赋值并执行静态代码块
```


对象的创建过程？
```text
1. 类加载检查: 检查运行时常量池中该类的符号引用是否被解析，如果没有则先触发类加载
2. 内存分配: 在堆中为对象分配内存
3. 内存初始化零值: 将内存空间清零，即 int=0，boolean=fasle，引用=null，避免对象在使用前出现随机垃圾值
4. 设置对象头: 设置对象的标记字段和类型指针
5. 执行构造方法: 先给成员变量赋值，再执行代码块，最后执行当前类的构造方法（先一路向上处理父类，然后才从上往下处理子类）
```


能作为 GC Roots 的对象有哪些？
```text
栈帧中的对象: 因为栈帧标识当前正在执行的方法，不能被破坏，所以局部变量表中的对象和操作数栈中的对象不会被回收
线程对象: 当前存在的线程对应的 Java 对象肯定不会被回收
属于类的对象: 类静态字段引用的对象、Class 对象、ClassLoader 对象，只要类没有被卸载，这些对象一定存在
JVM 内部引用的对象: 这些对象是 JVM 运行所需要的，不会被回收
```


三种 GC 算法？
```text
标记清除: 先标记所有存活对象，再回收所有没有被标记的对象内存 → 需要扫描两次，而且会留下内存碎片
标记压缩: 先标记所有存活对象，然后将它们向一端移动，最后回收末端之后的所有内存 → 需要扫描两次，而且会进行大量的内存拷贝工作
复制: 预先将内存划分为两个大小相等的区域，每次只使用一块，顺序扫描，标记到存活对象则直接复制到另一块 → 只需要扫描一次，但需要两倍内存大小
```


哪些情况会进入老年代？
```text
老龄晋升: 对象刚创建的时候年龄为 0，以后每经过一次 Minor GC 存活，年龄都会 +1，等到年龄达到预设的阈值，就会晋升到老年代 → 这是最常规的方式
动态晋升: 如果 Survivor 区中某一年龄及以上对象的总大小已经超过 Survivor 一半，即使还没达到年龄阈值，也会提前晋升到老年代 → 这批对象很可能是长期存活的，避免无意义的 Young GC
被迫晋升: Minor GC 后 Survivor 区无法放下所有对象，则会提前把年龄较大的对象晋升为老年代 → 确保 Young GC 能够正常执行
大内存晋升: 如果对象的大小超过了配置的阈值，在创建的时候会直接进入老年代 → 防止 Young GC 停顿时间过久
```


有哪些垃圾回收器？
```text
Serial: 复制 + 标记压缩，执行的时候会暂停所有用户线程，只运行单个 GC 线程
Parallel Scavenge: 复制 + 标记压缩，支持多个 GC 线程并行回收，强调减少总停顿次数，从而提高系统吞吐量（高效率）
ParNew + CMS: 复制 + 标记清除，不仅支持多个 GC 线程并行回收，还支持用户线程和 GC 线程并发执行，强调降低单次停顿时间，从而提升系统响应速度（低延迟）
G1: 复制，不再分为新生代和老年代，而是将堆划分为多个 Region，动态地决定哪些 Region 作为 Eden / Survivor / Old，会统计每个 Region 的垃圾比例和回收成本，每次只回收较高价值的 Region，支持可控停顿时间
```


## Redis


String = SDS 的结构和意义？
```text
长度获取: Redis 通过维护的 len，获取长度只需要 O(1)，用空间换时间
动态扩容判断: Redis 通过维护的 alloc 判断是否需要动态扩容：扩容时申请的新内存大小会比实际所需要的多一点，而缩短字符串时不会立马回收内存，保证留出充足的冗余空间，从而减少动态扩容次数，同样是用空间换时间
二进制安全: Redis 通过维护的 len 来判断 char[] 的结束位置，而不是依靠 '\0'，因此可以存储任意字节数据
```


List = ziplist / listpack 的结构和意义？
```text
节省内存: ziplist / listpack 作为节点可以存储多个元素，但只需要一对前后指针，避免为每个元素都维护一对前后指针
缓存加速: 虽然不同节点是离散存储，但是 ziplist / listpack 内的多个元素是连续存储的，更容易命中 CPU 缓存，从而加速访问
支持变长: ziplist / listpack 的每个元素都是一个变长结构，记录了长度信息和实际数据，利用长度信息可以实现遍历
```


Hash / Set = ziplist + hashtable 的结构和意义？
```text
ziplist / listpack: 当元素数量小的时候使用，将所有 key-value 拼凑在一起压缩一个数组里面，时间复杂度为 O(n) 是可以接受的，同时还可以连续存储的缓存性质，并且更节省内存，缺点就是如果要修改某个 value 值，可能需要进行内存移动
hashtable: 当元素数量大的时候使用，每个 key-value 对应一个节点，哈希表存储槽位链表的第一个节点，时间复杂度为 O(1)，但是会有大量的指针内存开销 【为什么 Set 底层同时用了 intset 和 hashtable？】
intset: 只在元素是整数且数量较小的时候使用，值放进数组中有序存储，利用二分法控制平均时间复杂度在 O(log n)，同时整数的大小是固定的，可以很方便的进行内存移动
hashtable: 当元素不是整数或数量较大的时候使用，此时用 key 存储数据值，而 value 统一设置为 null
```


ZSet = hashtable + skiplist 的结构和意义？
```text
dict: 用 hashtable 的 key 存储 member，value 存储 score，专门用于 ZSet 获取成员分数以及判断成员是否存在
skiplist: skiplist 是按照 score 排序的多层链表，每个节点都存储了每一层的 next 指针，同时会根据随机算法决定自己的层高，然后将自己插入到对应层的链表之中，本质上是一种空间换时间的策略，让查找没必要一个一个扫描，而是先在较高层快速跳跃，找到区间后再下沉较低层逼近目标，控制平均时间复杂度在 O(log n)
```


Redis 的事务机制有什么特性？
```text
打包执行，支持隔离性: Redis 先通过 MULTI 开启事务，会将后面所有的命令按顺序缓存到队列，然后通过 EXEC 一次性提交执行，利用 Redis 的单线程可以确保这批命令不会被打断
不能回滚，不支持原子性和一致性: 提交的命令会按顺序执行，但是如果某条命令出现了运行时错误，此前执行的命令不会撤回，此后的命令仍然会执行
内存存储，不支持持久性: Redis 的数据是直接存储在内存的，需要通过额外的 RDB 和 AOF 机制才能实现持久化
```


RDB 和 AOF 的机制？
```text
RDB: 将某一时刻的内存数据快照存储在 dump.rdb 二进制文件中，支持定时备份，缺点是空窗期大，存在数据丢失风险
AOF: 把所有写命令存储在 apppendonly.aof 文本文件中，支持自动重写，缺点是文件体积大，恢复需要逐条执行较慢
```


AOF 写回、重写和重放分别是什么意思？
```text
写回: Redis 会先将写命令写到 AOF 缓冲区，然后通过配置 always / everysec / no 来控制何时刷入磁盘（no 不是不刷盘，而是交给操作系统决定）
重写: 当 AOF 体积较大时，Redis 会启动一个子进程，生成一套数据不变的最小化写命令集合，并替换旧的 AOF 文件
重放: Redis 重启时会加载 AOF 文件，并按顺序执行其中的写命令来恢复数据。
```


主从复制的流程？
```text
1. Slave 首先执行 REPLICAOF <ip> <port> 发送请求到 Master
2. Master 收到请求后，会立刻执行 BGSAVE，异步生成一份 RDB 快照发给 Slave
3. Master 会将这期间的写命令全部填入 replication backlog（Master 全局） 和 replication buffer（逐 Slave）
4. Slave 加载完 RDB 之后，再执行 REPLCONF ACK <offset> 发送请求到 Master
5. Master 收到请求后，会从 backlog 的 offset 位置，将之后的所有写命令补发给 Slave
```


哨兵如何解决单点故障？
```text
当 Master 挂掉之后，Sentinel 会从 Slave 中选举一个新的 Master，更新整个主从复制结构，并通知客户端新的 Master 地址
```


集群的意义是什么？
```text
提升系统吞吐量，支持多个 Master 节点，而每个 Master 节点又可以配置各自的 Slave 节点，并通过 CRC16(key) mod slots 将 key 分片到多个槽位，每个 Master 只负责各自的 slots，从而防止 key 的写入冲突
```


双写并发如何破坏一致性？
```text
读写并发: 原先数据库和缓存都是 1，线程 A 进行写 2，线程 B 进行读：线程 A 删缓存 1 → 线程 B 读数据库 1 → 线程 A 写数据库 2 → 线程 A 写缓存 2 → 线程 B 写缓存 1
写写并发: 原先数据库和缓存都是 1，线程 A 进行写 2，线程 B 进行写 3：线程 A 写数据库 2 → 线程 B 写数据库 3 → 线程 B 写缓存 3 → 线程 A 写缓存 2
```


双写一致性的策略是什么？
```text
Cache Aside: 解决读写并发：先更新数据库，再删除缓存，等到下一次读取时才触发写回缓存 → 避免脏缓存
延迟双删: 解决读写并发：先删除缓存，再更新数据库，等待一段时间再删除缓存 → 消除脏缓存
加锁: 解决读写并发和写写并发：对数据加锁 → 避免并发
```


Cache 穿透是什么？如何解决？
```text
查询一个不在缓存也不在数据库的数据，永远也不会写回缓存，导致请求一直打到数据库上
解决-布隆过滤器: 写数据时都放入布隆过滤器，查数据时先判断 key 是否存在 → 仍有一定概率穿透，而且无法从布隆过滤器中撤销某个 key
解决-缓存空值: 将不在数据库的数据也写回缓存，值为 null → 可能导致内存充斥大量存空值的 key
```


Cache 击穿是什么？如何解决？
```text
某一个 HotKey 过期，导致一瞬间大量请求打到数据库上
解决-过期时间处理: 设置定时器，定期刷新 HotKey 的 TTL，或者干脆设置为永不过期 → 必须事先知道哪个是 HotKey
解决-加锁: 只让一个线程去查询数据库并重建缓存，其他线程原地等待 → 吞吐下降，大部分请求的响应延迟增加
```


Cache 雪崩是什么？如何解决？
```text
同一时间内大量 key 过期，导致一瞬间大量请求打到数据库上
解决-随机过期: 设置 TTL 时在固定值上增加一个随机值 → 仍有一定概率雪崩
解决-分批预热: 相隔一段时间写入一批 key → 预热阶段可能发生击穿
```


限流是什么？
```text
限制单位时间内进入数据库的请求数量，多余请求排队等候，防止瞬时流量打垮数据库 → 系统卡顿
```


熔断是什么？
```text
当数据库持续异常或响应持续过慢时，临时切断接口，返回错误响应，防止故障扩散和加剧 → 破坏业务连续性
```


降级是什么？
```text
当数据库正在维护或出现异常时，调用接口直接返回旧响应 / 默认响应 / 兜底响应，防止系统不可用 → 影响用户决策
```


为什么 Redis 这么快？
```text
1. 基于内存: 所有的数据都直接存储在内存之中，而内存读写是纳秒级别，远快于磁盘读写的毫秒级别
单线程执行: 核心操作都是由一个线程完成，避免了锁竞争和线程上下文切换，不用担心并发带来的额外开销
2. 数据结构高效: Redis 的数据结构都不是直接利用 C 的数据结构，而是采取空间换时间的策略，维护额外的字段来降低操作的时间复杂度
3. IO 多路复用: 通过 epoll 事件驱动机制，将连接监听交给内核，自己只处理就绪连接，从主动轮询变为被动唤醒，从而实现一个线程处理多个 socket 连接
	1. Redis 启动时调用 epoll_create 在内核里创建一个 epoll 事件管理器实例 
	2. Redis 首先调用 epoll_ctl 将 server socket 注册到 epoll 中，然后调用 epoll_wait，让内核负责监听 server socket 的状态变化 
	3. 每当有客户端发起连接请求时，内核会把 server socket 加入就绪队列，唤醒 Redis 线程处理 
	4. Redis 会从 server socket 调用 accept 拿到 client socket ，然后调用 epoll_ctl 将 client socket 注册到 epoll，然后调用 epoll_wait，让内核负责监听所有 client socket 变化 
	5. 当有客户端发送数据时，内核会把 client socket 加入就绪队列，唤醒 Redis 线程处理 
	6. Redis 会从 client socket 调用 read 读取命令执行，然后调用 write 将结果写回 client socket
```
