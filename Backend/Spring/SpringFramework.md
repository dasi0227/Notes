# SpringFramework



   * [概念](#概念)
      * [Spring 全家桶](#spring-全家桶)
      * [SpringFramework](#springframework)
   * [IoC](#ioc)
      * [定义](#定义)
      * [Bean](#bean)
      * [XML 配置 Bean](#xml-配置-bean)
         * [手动装配](#手动装配)
         * [自动装配](#自动装配)
      * [注解配置 Bean](#注解配置-bean)
         * [组件扫描](#组件扫描)
         * [@Component](#component)
         * [@Autowired](#autowired)
         * [@Configuration](#configuration)
      * [Bean 的生命周期](#bean-的生命周期)
         * [获取 Bean](#获取-bean)
         * [完整流程](#完整流程)
      * [底层实现](#底层实现)
         * [BeanFactory](#beanfactory)
         * [IoC 的流程](#ioc-的流程)
         * [字段注入的流程](#字段注入的流程)
   * [AOP](#aop)
      * [定义](#定义)
      * [代理模式](#代理模式)
         * [概念](#概念)
         * [JDK 动态代理](#jdk-动态代理)
         * [CGLIB 动态代理](#cglib-动态代理)
      * [注解实现 AOP](#注解实现-aop)
         * [切入点表达式语法](#切入点表达式语法)
         * [@Before](#before)
         * [@AfterReturning](#afterreturning)
         * [@AfterThrowing](#afterthrowing)
         * [@After](#after)
         * [@Around](#around)
         * [@Pointcut](#pointcut)
         * [@Order](#order)
         * [执行顺序](#执行顺序)
   * [JDBC](#jdbc)
      * [JdbcTemplate](#jdbctemplate)
         * [意义](#意义)
         * [XML 配置 DataSource](#xml-配置-datasource)
         * [SQL 流程](#sql-流程)
      * [@Transactional](#transactional)
         * [意义](#意义)
         * [propagation](#propagation)
         * [isolation](#isolation)
         * [timeout](#timeout)
         * [readOnly](#readonly)
         * [rollbackFor / noRollbackFor](#rollbackfor-norollbackfor)
   * [Resource](#resource)
      * [意义](#意义)
      * [实现类](#实现类)
      * [ResourceLoader](#resourceloader)
      * [注册 Resource 对象的 Bean](#注册-resource-对象的-bean)
   * [Validator](#validator)
      * [意义](#意义)
      * [绑定校验对象](#绑定校验对象)
      * [校验注解](#校验注解)
   * [i18n](#i18n)
      * [含义](#含义)
      * [Spring 国际化](#spring-国际化)
   * [Junit](#junit)
      * [意义](#意义)
      * [使用](#使用)
   * [Maven](#maven)
      * [概念](#概念)
      * [pom.xml](#pomxml)
   * [Log4j](#log4j)
      * [概述](#概述)
      * [XML 配置](#xml-配置)



## 概念

### Spring 全家桶

Spring 是一个开源的 Java 应用框架，旨在简化企业级 Java 开发，其核心在于通过**松耦合设计和面向切面编程**，使得应用更加可测试、可维护、可扩展

- **SpringFramework**：基础容器与通用服务 
- **SpringMVC**：基于 Servlet 的 MVC Web 框架，用于处理 HTTP 请求并渲染视图或输出 JSON
- **SpringBoot**：约定优于配置的快速启动框架，通过自动配置和 Starter 依赖实现“零”或“极少”配置
- **SpringCloud**：构建分布式系统和微服务生态，整合配置管理、服务发现、客户端负载均衡、熔断、消息总线等模式
- **SpringData**：统一的数据访问抽象，为多种存储如关系型数据库、NoSQL、搜索引擎等提供一致的仓库 API
- **SpringSecurity**：基于过滤器链的应用安全框架，提供认证（Authentication）和授权（Authorization）功能

> 广义的 Spring 指的是整个生态，而狭义的 Spring 指的就是 Spring Framework

辨析

- **框架（Framework）**：是解决特定类型问题的可复用设计方案，具有一系列的约定和规范，程序员只需要填空式地写业务逻辑，由框架调用业务代码
- **容器（Container）**：是对象生命周期和依赖关系的管理器，负责创建（实例化）、配置（属性注入）、组装（依赖注入）、交互（域内共享）和销毁（资源释放）

### SpringFramework

两个核心模块

- **IoC（Inverse of Control，控制反转）**：由容器负责对象的创建、配置和管理，应用代码不再自行 new 对象，而是声明依赖，让容器通过依赖注入对象
- **AOP（Aspect-Oriented Programming，面向切面编程）**：将横切关注点（日志、事务、校验、监控）从业务逻辑中抽离，以切面的方式在运行时动态织入，而不改变业务代码结构

特点

- **非侵入式**：业务类无需继承特定父类或实现特定接口，只需要加上注解或在配置文件中声明
- **容器化**：Spring IoC 容器负责对象的实例化、装配、生命周期管理和依赖解析
- **组件化**：按照功能模块拆分为多个子组件（Core、Beans、Context、AOP、JDBC、ORM、Web、Security）
- **一站式**：覆盖从核心容器到 Web MVC、数据访问、事务管理、安全、批处理、集成消息、云原生等全套企业级功能



## IoC

### 定义

**Ioc（Inversion of Control，控制反转）**：是面向对象编程中的一种设计原则，由容器负责**管理所有 Java 对象的实例化和初始化**

**DI（Dependency Injection，依赖注入）**：是 IoC 的一种具体实现方式，由容器动态地**将依赖对象注入到目标对象中**，而不是由目标对象自己创建或查找依赖

IoC 的可实现性

- Java 规范**要求【类名】和【文件名】严格对应**，也就是类 Foo 必须放在 Foo.java（编译后是 Foo.class）
- Java 规范**要求【包路径】与【文件存储路径】严格对应**，也就是包 com.dasi.service 必须对应目录 …/com/dasi/service/

### Bean

Bean 就是由 Spring IoC 容器直接管理的对象

- Bean 是容器的最基本单位，只要一个对象交给了 Spring 管理，它就可以称作为 Bean
- 本质上就是一个普通的 Java 对象，只不过完全由容器负责它的生命周期

### XML 配置 Bean

#### 手动装配

\<bean> 用于在 XML 中**声明一个需要被 Spring IoC 容器管理的 Java 对象**，属性有

- id/name：Bean 的唯一标识名称
- class：Bean 对应的全限定类名
- lazy-init：是否延迟初始化
    - true 表示首次调用 getBean 时才实例化
    - false 表示容器初始化时就实例化，默认值
- scope：Bean 的作用域
    - singleton 表示只创建一个实例，全局共享，默认值
    - prototype 表示每次调用 getBean() 就创建一个实例
    - session 表示每个 HTTP 会话创建一个实例
    - request 表示每个 HTTP 请求创建一个实例
- init-method：指定初始化回调方法
- destroy-method：指定销毁回调方法

\<bean> 下的子标签用于注入属性

- \<constructor-arg name="...">：通过**构造器注入**指定名称属性的值（很少使用）
- \<property name="...">：通过 **Setter 方法注入**指定名称属性的值

\<property> 下的子标签用于声明注入的值

- \<value>：注入普通的值，如字符串、数字等
- \<ref bean="..." />：注入指定 id 的 Bean
- \<bean class="..." />：注入指定类路径的 Bean
- \<list> / \<set> / \<map>：注入 List / Set / Map 集合，可以嵌套子标签声明值

> 当 Spring 同时通过构造器注入和 Setter 注入给同一个字段赋值时，会执行有参构造器，再调用 Setter 方法

```xml
<!-- User Bean -->
<bean id="user" class="com.dasi.bean.User">
    <!-- 构造器注入 -->
    <constructor-arg name="age">
        <value>21</value>
    </constructor-arg>

    <!-- setter 注入 -->
    <property name="name">
        <value>wyw</value>
    </property>

    <!-- 注入外部 bean -->
    <property name="address" >
        <ref bean="addressBean"/>
    </property>

    <!-- 注入匿名内部 bean -->
    <property name="pet">
        <bean class="com.dasi.bean.Pet" />
    </property>

    <!-- 注入 List 类型 -->
    <property name="hobbies">
        <list>
            <value>basketball</value>
            <value>hiphop</value>
        </list>
    </property>

    <!-- 注入 Set 类型 -->
    <property name="skills">
        <set>
            <value>Java</value>
            <value>Spring</value>
        </set>
    </property>

    <!-- 注入 Map 类型 -->
    <property name="meta">
        <map>
            <entry key="github" value="https://github.com/dasi0227"/>
            <entry key="blog" value="https://dasi.plus/"/>
        </map>
    </property>
</bean>
```

#### 自动装配

可以利用 \<bean> 标签的 autowire 属性值实现自动装配，这样就不再需要 \<property> 标签注入

- byType：**根据属性类型去容器中查找唯一的同类型 Bean**，如果存在多个同类型 Bean（如 PaymentService 有 AlipayServiceImpl 和 WechatPayServiceImpl），Spring 会抛出异常
- byName：**根据属性名去容器中查找同名的 Bean**，如果找到同名但是类型不兼容会抛出异常

> 如果同时配置了 `autowire` 和显式的 `<property>`，显式配置会覆盖自动装配
>
> 如果找不到对应的 Bean，不会抛出异常，只是注入被跳过，属性值为 null

### 注解配置 Bean

#### 组件扫描

默认情况下，Spring 容器不会主动扫描并装配带注解的类，**必须在 XML 配置中显式开启组件扫描**，才能让 Spring 识别并注册这些注解 Bean

```xml
<beans xmlns="http://www.springframework.org/schema/beans"
       xmlns:context="http://www.springframework.org/schema/context"
       xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"
       xsi:schemaLocation="
         http://www.springframework.org/schema/beans
         http://www.springframework.org/schema/beans/spring-beans.xsd
         http://www.springframework.org/schema/context
         http://www.springframework.org/schema/context/spring-context.xsd">

    <!-- 开启组件扫描，自动注册带注解的 Bean -->
    <context:component-scan base-package="com.dasi.com"/>
</beans>
```

#### @Component

标记一个类为 Spring 容器管理的 Bean，属于通用型注解

- 默认的 Bean 名称为该**类名首字母小写的驼峰形式**
- 可以在声明时手动指定 Bean 名称
- Spring 对常见层次场景提供了其他三种主要注解 **@Service、@Repository、@Controller**，本质上都是 @Component，只是增强代码可读性

```java
@Component("UserService") // 默认是 userService
public class UserService {
    // 业务逻辑...
}
```

#### @Autowired

按照 byType 的方式自动将匹配的 Bean 装配到目标对象中，有以下三种方式注入，只是时机不同

- **字段注入**：最简洁，但是无法用 final 修饰字段

    ```java
    @Component
    public class UserController {
        @Autowired
        private UserService userService;
    }
    ```

- **Setter 注入**：适合可选依赖，但是无法用 final 修饰字段

    ```java
    @Component
    public class UserController {
    	  private UserService userService;
        @Autowired
      	public void setUserService(UserService userService){
          	this.userService = userService;
        }
    }
    ```

- **构造器注入**：适合强制依赖，支持 final 字段，最推荐

    ```java
    @Component
    public class UserController {
        private final UserService userService;
        @Autowired
        public UserController(UserService userService) {
          	this.userService = userService;
        }
    }
    ```

- **方法注入**：适合注入多个依赖，支持 final 字段

    ```java
    @Component
    public class UserController {
        @Autowired
        public void init(UserService userService, UserRepository userRepository) {
            System.out.println("init() 被调用");
        }
    }
    ```

- **@Qualifier**：由于 @Autowired 是依靠类型装配，所以当容器中存在多个同类型的 Bean 时，需要使用 @Qualifier 指定要注入的 Bean 名称或自定义标识

    ```java
    @Component
    public class UserController {
        @Autowired
        @Qualifier("vipUserService")
        private UserService userService;
    }
    ```

- **@Resource**：先按照 byName 的方式，再按照 byType 的方式自动将匹配的 Bean 装配到目标对象中，位置和 @Autowired 相同

    ```java
    @Component
    public class UserController {
    
        // 按属性名 "userService" 找 Bean，如果没找到，再按类型找
        @Resource
        private UserService userService;
    
        // 显式指定 Bean 名
        @Resource(name = "adminUserServiceImpl")
        private UserService adminService;
    }
    ```

#### @Configuration

@Configuration 将类标记为 Spring 容器的配置类，告诉容器可以把它当成 XML 文件来解析

@ComponentScan 告诉 Spring 要去哪里扫描带有组件注解的类，从而把它们注册为 Bean，并加载到容器之中

```java
@Configuration
@ComponentScan("com.dasi")
public class SpringConfig {
		// 声明一个 Bean，id 默认为 "userService"
    @Bean
    public UserService userService() {
        return new UserService();
    }
		// 自定义 Bean 名称
    @Bean(name = "orderService")
    public OrderService orderService() {
        return new OrderService();
    }
}
```

### Bean 的生命周期

#### 获取 Bean

XML

```java
ApplicationContext context = new ClassPathXmlApplicationContext("bean.xml");
UserService userService = context.getBean("userService", UserService.class);
```

注解

```java
AnnotationConfigApplicationContext context = new AnnotationConfigApplicationContext(SpringConfig.class);
UserService userService = context.getBean(UserService.class);
```

#### 完整流程

1. **实例化**：通过反射调用构造器创建 Bean 实例
2. **依赖注入**：通过 Setter、字段、构造方法等方式，把容器中的依赖 Bean 注入到该 Bean 的属性中
3. **初始化前置处理**：遍历所有已注册的 BeanPostProcessor，调用 postProcessBeforeInitialization(Object bean, String beanName)
4. **初始化接口回调**：调用实现了 InitializingBean 接口的 afterPropertiesSet() 方法
5. **初始化方法回调**：调用配置的初始化方法 init-method()
6. **初始化后置处理**：遍历所有注册的 BeanPostProcessor，调用 postProcessAfterInitialization(Object bean, String beanName)
7. **销毁前置处理**：遍历所有注册的 DestructionAwareBeanPostProcessor，调用 postProcessBeforeDestruction(Object bean, String beanName)
8. **销毁接口回调**：调用实现了 DisposableBean 接口的 destroy() 方法
9. **销毁方法回调**：调用配置的销毁方法 destroy-method

### 底层实现

#### BeanFactory

BeanFactory 是 Spring 最核心的 IoC 容器接口，实践中常用他的继承类 **ApplicationContext**

| **方法**                                                     | **作用**                                                   |
| ------------------------------------------------------------ | ---------------------------------------------------------- |
| \<T> T getBean(Class\<T> requiredType)                       | 按类型获取 Bean                                            |
| \<T> T getBean(String name, Class\<T> requiredType)          | 按名称 + 类型获取 Bean                                     |
| Object getBean(String name)                                  | 按名称获取 Bean，会执行类型转换                            |
| Object getBean(String name, Object... args)                  | 按名称获取 Bean，并传入创建时需要的参数                    |
| boolean containsBean(String name)                            | 判断容器中是否存在指定名称的 Bean                          |
| boolean isSingleton(String name)                             | 判断指定 Bean 是否为单例                                   |
| boolean isPrototype(String name)                             | 判断指定 Bean 是否为原型（每次获取都创建新实例）           |
| boolean isTypeMatch(String name, ResolvableType typeToMatch) | 判断 Bean 类型是否匹配给定类型，用于按名称获取 Bean 的场景 |
| Class<?> getType(String name)                                | 获取指定 Bean 的类型                                       |

#### IoC 的流程

1. **包名→路径**：根据传递的包名，转化为对应的文件存储路径，交给 ClassLoader 查资源
2. **递归目录扫描**：将获取到的每个目录构造成 File 对象，调用 isDirectory() 判断是否是目录，是目录则调用 listFiles() 方法获得其下所有文件，递归调用 loadBean()
3. **处理类文件**：如果是文件则调用 getAbsolutePath() 得到类的完整文件系统路径，再截取掉根路径前缀和后缀，只得到相对路径 classPath
4. **拼全限定名**：将 classPath 转化为全限定名 className，调用 Class.forName(className) 获取类的类型 clazz
5. **过滤非 Bean**：对类调用 clazz.getAnnotation(XXX.class) 判断是否存在指定的注解
6. **实例化**：如果存在，则调用 clazz.getConstructor().newInstance() 调用类的无参构造器创建实例
7. **注册 Bean**：最后按接口或按类本身作为键，存入 beanFactory

#### 字段注入的流程

1. **遍历所有 Bean 实例**：遍历已经放入 beanFactory 的所有实例 beanInstance
2. **遍历字段**：遍历每个实例的所有字段 field
3. **过滤非注入字段**：对字段调用 field.getAnnotation(XXX.class) 判断是否存在指定的注解
4. **确定依赖类型**：如果确实存在注解，则调用 field.getType() 获取对应的依赖类型 fieldClass
5. **查找依赖实例**：调用 beanFactory.get(fieldClass) 获取已经存在 beanFactory 中的依赖对象
6. **注入字段**：最后调用 field.set(beanInstance, dependency) 将依赖对象注入到当前对象



## AOP

### 定义

AOP（Aspect-Oriented Programming，面向切面编程）是一种将横切关注点从业务逻辑中分离出来，并在运行时动态织入到目标对象的编程范式

- **切面（Aspect）**：负责横切逻辑的类，本质上一个横切逻辑对应一个方法
- **连接点（JoinPoint）**：执行过程中被插入横切逻辑的程序位置，本质上所有 Bean 的方法调用都被当作为连接点
- **切入点（Pointcut）**：切面匹配连接点的规则或表达式，本质上是一组过滤规则，限定只有某些连接点才能执行对应切面
- **通知（Advice）**：在切面“前后”的执行代码，常用于说明切面的情况
- **织入（Weaving）**：把切面逻辑应用到目标对象的过程

典型应用

- **事务管理**：在业务方法前后开启和提交/回滚事务
- **安全校验**：在敏感方法前检查用户权限
- **性能监控**：在方法前后记录执行时间
- **日志审计**：自动记录方法入参、出参、异常等

### 代理模式

#### 概念

Spring AOP 是通过代理模式来实现的，也就是代理对象的增强逻辑是由 AOP 的切面定义的

代理模式是一种设计模式，为目标对象提供一个代理对象，可以在客户端和目标对象之间添加附加行为，也可以延迟目标对象的创建或进行权限校验等

- **SubjectInterface**：定义了真实对象和代理对象的共同接口，客户端通过该接口调用，不关心具体是代理还是实现类
- **RealSubject**：实现接口，完成核心业务逻辑
- **Proxy**：实现接口，并持有 RealSubject 的引用，可以在调用方法前后加上**附加逻辑**

![image-20250809123457855](https://dasi-blog.oss-cn-guangzhou.aliyuncs.com/Java/SpringMVC202508091234948.png)

#### JDK 动态代理

代理流程

1. 运行时自动生成目标类的代理类
2. 调用代理类方法时，会统一转发到 InvocationHandler.invoke()
3. 在 invoke() 里设置前置/后置增强逻辑
4. 在 invoke() 里利用反射调用目标类方法

代理创建：利用 java.lang.reflect.Proxy 对象的 newProxyInstance() 方法，要求目标类必须已经实现所有接口

- **ClassLoader loader**：用来加载生成的代理类到 JVM
- **Class<?>[] interfaces**：代理需要实现的接口列表
- **InvocationHandler h**：实现了 InvocationHandler 接口中 invoke 方法的回调对象

```java
// 原始目标对象
UserService target = new UserServiceImpl();

// 获取目标对象的类加载器
ClassLoader classLoader = target.getClass().getClassLoader();

// 获取目标对象的接口列表
Class<?>[] interfaces = target.getClass().getInterfaces();

// 创建实现 invoke 的回调对象
InvocationHandler invocationHandler = new InvocationHandler() {
    @Override
    public Object invoke(Object proxy, Method method, Object[] args) throws Throwable {
				System.out.println("前置增强");
        Object result = method.invoke(target, args);
        System.out.println("后置增强");
        return result;
    }
};

// 创建代理对象
UserService proxy = (UserService) Proxy.newProxyInstance(classLoader, interfaces, invocationHandler);
```

#### CGLIB 动态代理

代理流程

1. 运行时自动生成目标类的子类代理类
2. 调用代理类方法时，会统一转发到 MethodInterceptor.intercept()
3. 在 intercept() 里设置前置/后置增强逻辑
4. 在 intercept() 里反射调用目标类方法

代理创建：利用 net.sf.cglib.proxy.Enhancer 对象的 create() 方法，要求目标类不能是 final，被代理的方法不能是 final

- **setSuperclass(Class<?>)**：指定目标类
- **setCallback(Callback)**：指定实现了 MethodInterceptor 接口中 intercept 方法的回调对象

```java
// 原始目标对象
UserService target = new UserServiceImpl();

// 创建增强对象
Enhancer enhancer = new Enhancer();

// 指定目标类
enhancer.setSuperclass(target.getClass());

// 创建回调对象
MethodInterceptor methodInterceptor = new MethodInterceptor() {
	  @Override
    public Object intercept(Object obj, Method method, Object[] args, MethodProxy proxy) throws Throwable {
        System.out.println("前置增强");
        Object result = proxy.invokeSuper(obj, args);
        System.out.println("后置增强");
        return result;
		}
};

// 设置回调对象
enhancer.setCallback(methodInterceptor);

// 创建代理对象
UserService proxy = (UserService) enhancer.create();
```

> 有接口用 JDK，没接口用 CGLIB

### 注解实现 AOP

#### 切入点表达式语法

```text
execution(修饰符? 返回类型 方法全限定名(参数模式) 异常模式?)
```

- 修饰符：可选的，如 public、protected
- 返回类型：void、String、*（任意类型）
- 方法全限定名：包名.类名.方法名（* 和 .. 可做通配）
- 参数模式：() 表示无参，(*) 表示一个任意类型参数，(..) 表示任意数量参数
- 异常模式：可选的，如 throws IOException

```java
// 匹配任意方法
execution(* *(..))

// 匹配 com.dasi.service 包下所有类的所有方法
execution(* com.dasi.service.*.*(..))

// 匹配 com.dasi 包及子包下所有类的所有方法
execution(* com.dasi..*.*(..))

// 匹配 UserService 接口中所有方法
execution(* com.dasi.service.UserService.*(..))

// 匹配 UserServiceImpl 类中所有方法
execution(* com.dasi.service.impl.UserServiceImpl.*(..))

// 匹配返回值为 String 的所有方法
execution(String com.dasi..*.*(..))

// 匹配第一个参数是 String 的方法
execution(* com.dasi..*.*(String, ..))

// 匹配 public 方法
execution(public * com.dasi..*.*(..))
```

> 支持使用逻辑运算符 &&、||、! 来复合多个切入点表达式

#### @Before

在目标方法执行之前调用，通过 value 属性设置切入点表达式，不改变返回值，JoinPoint 参数是当前连接点信息

```java
@Before(value="切入点表达式")
public void beforeAdvice(JoinPoint joinPoint) {
  	String methodName = joinPoint.getSignature().getName();
    System.out.println("方法名：" + methodName);
}
```

#### @AfterReturning

在目标方法正常完成并已经完成返回后调用，通过 value 属性设置切入点表达式，其中 returning 属性的值必须和方法中的参数变量名保持一致，revVal 参数保存了返回值

```java
@AfterReturning(value="切入点表达式", returning="retVal")
public void afterReturningAdvice(JoinPoint joinPoint, Object retVal) {
		System.out.println("返回值：" + retVal);
}
```

#### @AfterThrowing

在目标方法抛出异常后调用，通过 value 属性设置切入点表达式，其中 throwing 属性的值必须和方法中的参数变量名保持一致，ex 参数保存了异常对象

```java
@AfterThrowing(value="切入点表达式", throwing="ex")
public void afterThrowingAdvice(JoinPoint joinPoint, Throwable ex) {
	  System.out.println("异常信息：" + ex.getMessage());
}
```

#### @After

在目标方法执行结束后调用，无论是正常返回还是抛出异常都会执行，通过 value 属性设置切入点表达式

```java
@After(value="切入点表达式")
public void afterAdvice(JoinPoint joinPoint) {
    String methodName = joinPoint.getSignature().getName();
    System.out.println("方法名：" + methodName);
}
```

#### @Around

包裹目标方法执行，通过 value 属性设置切入点表达式

- 既可以在方法前后插入逻辑，也可以通过 try-catch 捕获异常
- 既可以决定是否执行目标方法，也可以修改方法的返回值
- 参数 ProceedingJoinPoint 是 JoinPoint 的继承类，通过调用 proceed() 执行目标方法
- 需要返回一个值作为被调用方法的返回值

```java
@Around(value="切入点表达式")
public Object aroundAdvice(ProceedingJoinPoint pjp) {
	  Object result = null;
  	try {
      	System.out.println("前置");
      	Object result = pjp.proceed();
	      System.out.println("后置");
    } catch (Throwable e) {
      	System.out.println("异常");
    } finally {
      	System.out.println("结束");
    }
    return result;
}
```

#### @Pointcut

**定义一个命名的切入点**，从而可以在其他通知注解中直接使用方法名

- 切入点名称就是函数方法名，不需要有函数题，只是起到标记作用
- 在通知注解中直接使用方法即可

```java
@Pointcut("execution(* com.dasi.service.*.*(..))")
public void serviceMethods() {}

@Before("serviceMethods()")
public void beforeService() {
    System.out.println("前置通知");
}

@After("serviceMethods()")
public void afterService() {
    System.out.println("后置通知");
}
```

#### @Order

用来指定切面的执行顺序，当多个切面同时匹配同一个连接点时，会按 @Order 的值来排序

- 数字越小的优先级越高
- 如果没有 @Order，默认优先级最低

```java
@Aspect
@Order(1)
@Component
public class LogAspect {
    @Before("execution(* com.dasi.service.*.*(..))")
    public void log() {
        System.out.println("日志记录");
    }
}

@Aspect
@Order(2)
@Component
public class SecurityAspect {
    @Before("execution(* com.dasi.service.*.*(..))")
    public void checkSecurity() {
        System.out.println("安全检查");
    }
}
```

#### 执行顺序

1. @Around（环绕前置）
2. @Before（前置）
3. @AfterReturning（返回）/ @AfterThrowing（异常）
4. @After（后置）
5. @Around（环绕后置）



## JDBC

### JdbcTemplate

#### 意义

JdbcTemplate 是 **Spring 提供的一个用来简化 JDBC 操作的类**，不再手动写数据库连接、资源释放、异常处理这些重复样板代码

1. 会自动获取并释放 Connection、PreparedStatement、ResultSet，避免忘记关闭而导致数据库连接泄漏
2. 会将 SQLException 的 checked 异常转成 Spring 的 DataAccessException 的 runtime 异常，无需大量 try–catch
3. 内置 queryForObject()、query()、update()、batchUpdate() 等方法，几乎覆盖了所有增删改查场景

#### XML 配置 DataSource

首先可以引入 `.properties` 属性文件，然后通过 `${}` 占位符表达式实现值的注入，最后注册 JdbcTemplate

```xml
<!-- 引入外部属性文件 -->
<context:property-placeholder location="classpath:jdbc.properties" />

<!-- 配置数据源 -->
<bean id="druidDataSource" class="com.alibaba.druid.pool.DruidDataSource">
    <property name="url" value="${jdbc.url}" />
    <property name="driverClassName" value="${jdbc.driver}" />
    <property name="username" value="${jdbc.username}" />
    <property name="password" value="${jdbc.password}" />
</bean>

<!-- 注册 JdbcTemplate 的 Bean -->
<bean id="jdbcTemplate" class="org.springframework.jdbc.core.JdbcTemplate">
    <property name="dataSource" ref="druidDataSource" />
</bean>
```

注解配置 DataSource

```java
// 声明这是一个 Spring 配置类
@Configuration
// 扫描 com.dasi 包及其子包
@ComponentScan(basePackages = "com.dasi")
// 开启基于注解的事务管理
@EnableTransactionManagement
// 指定属性文件 jdbc.properties 的位置
@PropertySource("classpath:jdbc.properties")
public class SpringConfig {

    // 注入 Spring 的 Environment 对象，用来读取属性文件中的配置信息
    private final Environment env;

    // 构造方法注入 Environment
    public SpringConfig(Environment env) {
        this.env = env;
    }

    // 配置 Druid 数据源并注册到容器
    @Bean
    public DataSource dataSource() {
        DruidDataSource druidDataSource = new DruidDataSource();
        druidDataSource.setUrl(env.getProperty("jdbc.url"));
        druidDataSource.setDriverClassName(env.getProperty("jdbc.driver"));
        druidDataSource.setUsername(env.getProperty("jdbc.username"));
        druidDataSource.setPassword(env.getProperty("jdbc.password"));
        return druidDataSource;
    }

    // 配置 JdbcTemplate 并注册到容器
    @Bean
    public JdbcTemplate getJdbcTemplate(DataSource druidDataSource) {
        return new JdbcTemplate(druidDataSource);
    }

    // 配置事务管理器并注册到容器
    @Bean
    public DataSourceTransactionManager getDataSourceTransactionManager(DataSource druidDataSource) {
        return new DataSourceTransactionManager(druidDataSource);
    }
}
```

#### SQL 流程

```java
@Repository
public class UserDao {
  	// 注入 JdbcTemplate 对象
    @Autowired
    private JdbcTemplate jdbcTemplate;

    // 新增用户
    public int addUser(String username, String password) {
        String sql = "INSERT INTO user(username, password) VALUES (?, ?)";
        return jdbcTemplate.update(sql, username, password);
    }

    // 删除用户
    public int deleteUser(int id) {
        String sql = "DELETE FROM user WHERE id = ?";
        return jdbcTemplate.update(sql, id);
    }

    // 更新用户
    public int updatePassword(int id, String newPassword) {
        String sql = "UPDATE user SET password = ? WHERE id = ?";
        return jdbcTemplate.update(sql, newPassword, id);
    }

    // 查询单行单列
    public String getUsernameById(int id) {
        String sql = "SELECT username FROM user WHERE id = ?";
        return jdbcTemplate.queryForObject(sql, String.class, id);
    }

    // 查询单行多列：自定义 RowMapper
    public User getUserById(int id) {
        String sql = "SELECT id, username, password FROM user WHERE id = ?";
        return jdbcTemplate.queryForObject(
                sql,
                (rs, rowNum) -> {
                    User user = new User();
                    user.setId(rs.getInt("id"));
                    user.setUsername(rs.getString("username"));
                    user.setPassword(rs.getString("password"));
                    return user;
                },
                id
        );
    }

    // 查询单行多列：直接利用 BeanPropertyRowMapper
    public User getUserByIdAutoMap(int id) {
        String sql = "SELECT id, username, password FROM user WHERE id = ?";
        return jdbcTemplate.queryForObject(sql, new BeanPropertyRowMapper<>(User.class), id);
    }

    // 查询多行：返回 List 集合
    public List<User> getAllUsers() {
        String sql = "SELECT id, username, password FROM user";
        return jdbcTemplate.query(
                sql,
                (rs, rowNum) -> {
                    User user = new User();
                    user.setId(rs.getInt("id"));
                    user.setUsername(rs.getString("username"));
                    user.setPassword(rs.getString("password"));
                    return user;
                }
        );
    }
}
```

### @Transactional

#### 意义

@Transactional 是 **Spring 提供的声明式事务管理注解**，只需标注在类或方法上，就可以对 Bean 的方法调用进行拦截并在调用前后开启/提交或回滚事务

- **声明式事务**：把事务控制逻辑（开启、提交、回滚）交给 Spring 的事务管理器，由 AOP 代理织入到方法调用前后，业务代码只关注核心逻辑
- **集中化配置**：通过注解参数（传播行为、隔离级别、超时、只读、回滚规则等）统一管理事务特性，避免重复写模板代码和 JDBC 事务控制

```java
@Transactional(
    propagation  = Propagation.REQUIRES_NEW,
    isolation    = Isolation.SERIALIZABLE,
    timeout      = 10,
    readOnly     = true,
    rollbackFor  = {IOException.class, SQLException.class},
    noRollbackFor= {CustomBusinessException.class}
)
@Service
public class BookServiceImpl implements BookService {}
```

#### propagation

定义事务的**传播行为**，决定当前方法如何加入或开启一个新事务

- **REQUIRED**：如果存在当前事务，则加入，否则新建一个事务（默认值）
- **SUPPORTS**：如果存在事务，则加入；否则以非事务方式运行
- **MANDATORY**：必须在事务中运行，否则抛异常
- **REQUIRES_NEW**：暂停当前事务，新建一个
- **NOT_SUPPORTED**：以非事务方式运行，如果存在事务则挂起
- **NEVER**：以非事务方式运行，如果存在事务则抛异常

#### isolation

定义事务**隔离级别**，控制并发时不同事务之间可见的数据状态

- **DEFAULT**：使用底层数据库默认隔离级别（默认值）
- **READ_UNCOMMITTED**：允许脏读、不可重复读、幻读
- **READ_COMMITTED**：禁止脏读，允许不可重复读、幻读
- **REPEATABLE_READ**：禁止脏读、不可重复读，允许幻读
- **SERIALIZABLE**：串行化，禁止脏读、不可重复读、幻读

> **脏读**：事务 A 读到了事务 B **已修改但还没提交**的数据
>
> **可重复读**：事务 A 在同一个事务内先后两次读取**同一行记录**，却因事务 B 在**两次读取之间提交了更新**，而读到不同的值
>
> **幻读**：事务 A 在同一事务内，对**满足某个条件的行集合**先后执行两次查询，因事务 B 在**两次之间插入或删除了若干行**，导致第二次查询“多”或“少”了“幻影”行

#### timeout

定义事务**超时时间**，超过该时间 Spring 强制回滚事务

- -1：表示永不超时（默认值）
- 单位秒，如果到期前方法仍未返回，则抛出 TransactionTimedOutException

#### readOnly

定义事务**是否只读**，只读不允许修改操作，只允许查询操作

#### rollbackFor / noRollbackFor

定义事务触发回滚的异常类型，可以指定哪些异常**必须回滚**，也可以指定哪些异常**不需要回滚**



## Resource

### 意义

Resource 接口是 **Spring 对外部资源访问的统一抽象**，无论资源是文件、类路径、网络流还是内存数据，都能用相同方法操作

- **定位**：getFile()、getURL()、getURI() 
- **读取**：getInputStream()
- **检查**：exists() 、isReadable() 
- **获取**：getFilename() 、lastModified() 、contentLength() 、getDescription()

### 实现类

| 实现类                 | **应用场景**                                      |
| ---------------------- | ------------------------------------------------- |
| ClassPathResource      | 读取类路径资源（JAR 包或编译目录中的文件）        |
| FileSystemResource     | 直接访问磁盘文件或目录                            |
| UrlResource            | 访问 HTTP、FTP、本地 file: 协议等 URL             |
| ServletContextResource | Web 应用中通过 ServletContext 读取 WEB-INF 等资源 |
| InputStreamResource    | 把已有的 InputStream 包装成 Resource              |
| ByteArrayResource      | 把内存数据包装成 Resource                         |

### ResourceLoader

ResourceLoader 是 **Spring 提供的一个顶层接口**， 只有一个方法 **getResource(String location)**，根据给定的资源路径字符串，自动返回一个对应的 Resource 对象，不用你自己去判断是文件、类路径、还是 URL

- 类路径资源：`classpath:config/app.properties`
- 绝对路径文件：`file:/data/config/app.properties`
- 网络资源：`http://example.com/file.txt`
- 相对路径：`app.properties`

 ApplicationContext 继承了 ResourceLoader，可以直接利用它来获取

```java
ApplicationContext ctx = new ClassPathXmlApplicationContext("bean.xml");
Resource resource = ctx.getResource("classpath:test.txt");
```

### 注册 Resource 对象的 Bean

在 Spring 中，可以把资源（文件、URL、类路径等）封装成 Resource 对象，作为 Bean 放到到容器中，注入到自定义的业务 Bean 中

- 扩展：在 Bean 里可以写一个或多个方法，专门用来操作资源
- 复用：所有读取、解析、异常处理都集中在一个地方，调用方只管调用你的封装方法
- 灵活：不用在业务代码中自己去判断路径类型、创建 FileInputStream 等

基于注解的流程

1. 注册 Resource Bean

    ```java
    @Configuration
    public class ResourceConfig {
        @Bean
        public Resource emailResource() {
            return new DefaultResourceLoader().getResource("classpath:email.txt");
        }
    }
    ```

2. 注册 Service Bean

    ```java
    @Component
    public class EmailResource {
        private final Resource emailResource;
    
        // 构造器注入 Resource
        public EmailResource(Resource emailResource) {
            this.emailResource = emailResource;
        }
    
      	// 自定义获取方法
        public String getEmail() {
            try (InputStream in = emailResource.getInputStream()) {
                return StreamUtils.copyToString(in, StandardCharsets.UTF_8);
            } catch (Exception e) {
                e.printStackTrace();
                return null;
            }
        }
    }
    ```

3. 使用 Bean

    ```java
    mailResource emailResource = context.getBean(EmailResource.class);
    System.out.println(emailResource.getEmail());
    ```



## Validator

### 意义

Validator 是 **Spring 提供的校验机制接口**，可以解耦校验逻辑与业务逻辑

- `boolean supports(Class<?> clazz)`：设置是否需要校验
- `validate(Object target, Errors errors)`：设置校验逻辑，errors 用来记录错误

rejectValue

- `String field`：需要校验的字段名
- `String errorCode`：自定义的错误代码
- `String defaultMessage`：自定义的错误消息

ValidationUtils 工具类：静态类，封装了常见的校验逻辑，不需要自己写 rejectValue 方法

- `rejectIfEmpty(Errors errors, String field, String errorCode, String defaultMessage)`：检查字段是否为 null 或 ""
- `rejectIfEmptyOrWhitespace(Errors errors, String field, String errorCode, String defaultMessage)`：检查字段是否为 null 或 "" 或只包含空白符

```java
// 自定义校验器对象
public class PersonValidator implements Validator {
  	// 是否执行校验
    @Override
    public boolean supports(Class<?> clazz) {
        return Person.class.equals(clazz);
    }
  
  	// 设置校验逻辑
    @Override
    public void validate(Object target, Errors errors) {
      	// 利用 ValidationUtils
        ValidationUtils.rejectIfEmpty(errors, "name", "name.empty", "name is empty");
      
      	// 自定义校验方法
        Person p = (Person) target;
        if (p.getAge() < 0) {
            errors.rejectValue("age", "age.value.invalid", "age must > 0");
        }
    }
}
```

### 绑定校验对象

```java
// 1. 获取需要校验的类对象 person
Person person = new Person("", -20);
// 2. 获取校验器对象 validator
PersonValidator validator = new PersonValidator();
// 3. 获取绑定器对象 binder，传递校验类对象
DataBinder binder = new DataBinder(person);
// 4. 利用 binder 绑定 person 和 validator
binder.setValidator(validator);
// 5. 调用 validate 执行校验
binder.validate();
// 6. 获取校验结果 result 
BindingResult result = binder.getBindingResult();
// 7. 获取某个字段上存在的错误信息
System.out.println(result.getFieldError("name").getDefaultMessage());
System.out.println(result.getFieldError("age").getDefaultMessage());
```

### 校验注解

Spring 提供了一些常见的校验注解，用在实体类字段、方法参数上，配合校验器自动检查数据是否合法

| **注解**                           | **含义**                                              |
| ---------------------------------- | ----------------------------------------------------- |
| @Null                              | 必须为 null                                           |
| @NotNull                           | 不能为 null，但可以是空字符串                         |
| @NotEmpty                          | 字符串/集合/数组/Map 非 null 且长度 > 0               |
| @NotBlank                          | 字符串非 null，trim() 后长度 > 0                      |
| @AssertTrue                        | 必须为 true                                           |
| @AssertFalse                       | 必须为 false                                          |
| @Min(value)                        | 数值 ≥ value                                          |
| @Max(value)                        | 数值 ≤ value                                          |
| @Range(min, max)                   | 数值在 [min, max] 范围内                              |
| @Positive                          | 数值 > 0                                              |
| @PositiveOrZero                    | 数值 ≥ 0                                              |
| @Negative                          | 数值 < 0                                              |
| @NegativeOrZero                    | 数值 ≤ 0                                              |
| @Size(min, max)                    | 字符串/集合/数组/Map 长度或元素个数在 [min, max] 范围 |
| @Length(min, max)                  | 字符串长度在 [min, max] 范围                          |
| @Pattern(regexp)                   | 字符串匹配指定正则                                    |
| @Email                             | 字符串须符合邮箱格式                                  |
| @URL(protocol, host, port, regexp) | 字符串符合 URL 格式，可指定协议等                     |
| @Past                              | 必须在当前时间之前                                    |
| @PastOrPresent                     | 必须在当前或之前                                      |
| @Future                            | 必须在当前时间之后                                    |
| @FutureOrPresent                   | 必须在当前或之后                                      |



## i18n

### 含义

i18n 表示 **internationalization**（首字母 i + 18 个字母 + 尾字母 n），目的是为应用在不同地区、语言环境下提供**本地化文本**和**格式支持**（如日期、数字、货币等），让多语言管理与动态切换更方便

资源文件命名：`基础名称_语言代码_国家代码.properties`

- 语言代码：小写（如 zh、en、fr）
- 国家代码：大写（如 CN、US、FR）

> 默认名称回退查找：messages_en_US ➡ messages_en ➡ messages

### Spring 国际化

配置资源文件，通常放在 `src/main/resources/i18n/`

- messages_zh_CN.properties

    ```properties
    greet=你好 {0}，欢迎来到 {1}！
    bye=欢迎再次访问！
    ```

- messages_en_US.properties

    ```properties
    greet=Hello {0}, welcome to {1}!
    bye=Hope to see you again!
    ```

XML 配置消息源

```xml
<bean id="messageSource" class="org.springframework.context.support.ResourceBundleMessageSource">
  	<!-- 配置要加载的资源文件的基础路径，不需要带语言、国家和 .properties 后缀，由容器自己解析  -->	
    <property name="basenames">
        <list>
            <value>i18n/messages</value>
        </list>
    </property>
  
  	<!-- 指定加载文件时的字符编码 -->
    <property name="defaultEncoding" value="UTF-8"/>
</bean>
```

Java 注解配置

```java
@Configuration
public class I18nConfig {
    @Bean
    public MessageSource messageSource() {
        ResourceBundleMessageSource ms = new ResourceBundleMessageSource();
      	// 配置路径
        ms.setBasenames("i18n/messages");
      	// 配置字符编码
        ms.setDefaultEncoding("UTF-8");
        return ms;
    }
}
```

利用 getMessage() 方法从消息源中提取消息

- greet：是资源文件中的键
- params：是资源文件中占位符的替换数组
- Locale：一个内置很多常量的 Java 类（CHINA 对应 _zh_CN，Locale.US 对应 _en_US）

```java
@Autowired
private MessageSource messageSource;

public void testI18n() {
    Object[] params = {"Dasi", "Spring i18n"};
    // 中文
    String zh = messageSource.getMessage("greet", params, Locale.CHINA);
    // 英文
    String en = messageSource.getMessage("greet", params, Locale.US);

    System.out.println(zh);
    System.out.println(en);
}
```



## Junit

### 意义

- 以前要手动 new ClassPathXmlApplicationContext() 再 getBean() 来获取对象，集成 Junit 后只需要直接在类上加 Spring 测试注解，容器会自动启动，@Autowired 字段直接注入
- 加上注解 @Transactional，测试执行后数据库操作会自动回滚，保证数据干净、互不污染
- Spring TestContext 会在测试启动时织入 AOP 代理，可以检测是否如预期地拦截了目标方法
- TestContext Framework 会缓存 ApplicationContext，避免为每个测试重复启动容器，提升效率

### 使用

Junit5

```java
@SpringJUnitConfig(locations = "classpath:bean.xml")
public class TestJunit {
    @Autowired
    private User user;

    @Test
    public void testUser() {
        user.run();
    }
}
```

Junit4

```java
@RunWith(SpringJUnit4ClassRunner.class)
@ContextConfiguration("classpath:bean.xml")
public class TestJunit {
    @Autowired
    private User user;

    @Test
    public void testUser(){
        user.run();
    }
}
```



## Maven

### 概念

Maven 是创建  Java 项目的工具，负责两大功能

- **构建项目**：自动完成编译、测试、打包、上传等过程
- **依赖管理**：自动下载、更新、管理各种第三方库，再也不需要手动去网站上找 Jar 包

Maven 常见指令有：

- mvn compile：编译源代码
- mvn test：执行测试代码
- mvn package：打包为 .jar 或 .war 文件
- mvn intall：安装构建好的包到本地仓库
- mvn clean：删除构建输出目录
- mvn dependency:tree：查看项目依赖树

### pom.xml

pom 全程 Project Object Model（项目对象模型），在这里面负责规定 Java 应用的基本信息和属性、需要哪些依赖和插件，如何进行构建，**是 Maven 项目的说明书、购物清单和施工计划书**

【核心标签】

| 标签         | 作用                                 |
| ------------ | ------------------------------------ |
| project      | 最外层标签，必须存在                 |
| modelVersion | 固定写 4.0.0                         |
| groupId      | 项目所属的组织或公司标识             |
| artifactId   | 项目唯一标识符                       |
| version      | 项目的版本号                         |
| packaging    | 打包类型                             |
| properties   | 定义全局变量，统一管理版本号、编码等 |
| dependencies | 声明项目依赖的库列表                 |
| build        | 构建配置区，包含插件、资源目录等     |
| plugins      | 声明构建过程中使用的插件             |

【依赖库的基本子标签】

| 标签       | 作用                                                         |
| :--------- | ------------------------------------------------------------ |
| groupId    | 组织/公司/项目的域名                                         |
| artifactId | 具体的库或插件名称                                           |
| version    | 使用的版本号                                                 |
| scope      | 依赖项的生命周期和使用范围（compile、provided、runtime、test） |

```xml
<project>
  <modelVersion>4.0.0</modelVersion>

  <groupId>com.example</groupId>
  <artifactId>my-app</artifactId>
  <version>1.0</version>
  <packaging>jar</packaging>

  <!-- 这里写 Java 信息 -->
  <properties>
    <maven.compiler.source>17</maven.compiler.source>
    <maven.compiler.target>17</maven.compiler.target>
    <project.build.sourceEncoding>UTF-8</project.build.sourceEncoding>
  </properties>

  <!-- 导入依赖库 -->
  <dependencies>
    <dependency>
      <groupId>com.google.code.gson</groupId>
      <artifactId>gson</artifactId>
      <version>2.10.1</version>
      <scope>compile</scope>
    </dependency>
  </dependencies>

  <!-- 导入插件 -->
  <build>
    <plugins>
      <plugin>
        <groupId>org.apache.maven.plugins</groupId>
        <artifactId>maven-compiler-plugin</artifactId>
        <version>3.11.0</version>
        <configuration>
          <source>17</source>
          <target>17</target>
        </configuration>
      </plugin>
    </plugins>
  </build>
</project>
```



## Log4j

### 概述

Log4j（Log for Java）是 Java 项目里用来记录日志的框架，有以下几个部分构成

- 优先级：低级别默认会输出更高级别的信息，但不会输出更低级别的的信息
    - FATAL：严重错误才输出
    - ERROR：输出错误信息
    - WARN：输出警告信息
    - INFO：普通运行信息
    - DEBUG：调试信息
    - TRACE：最详细的跟踪信息
- 输出方式
    - Console：控制台
    - File：本地文件
    - RollingFile：输出到文件并按时间/大小滚动
    - Socket：远程套接字
    - JDBC：数据库
- 输出格式：通过占位符可以自动填充信息
    - %d{\<format>}：日期时间，可以自定义格式
    - %level / %p：日志级别
    - %msg / %m：日志内容
    - %C：类名
    - %logger / %c：logger 名
    - %F：源文件名
    - %M：方法名
    - %t：线程名
    - %T：线程 ID
    - %n：换行符

### XML 配置

```xml
<?xml version="1.0" encoding="UTF-8"?>
<Configuration status="WARN" monitorInterval="30">
    <!-- 定义输出方式 -->
    <Appenders>
        <!-- 控制台 -->
        <Console name="console" target="SYSTEM_OUT">
            <PatternLayout pattern="[%d{HH:mm:ss.SSS}] [%t] %-5level %logger{36} - %msg%n"/>
        </Console>

        <!-- 文件输出 -->
        <File name="file" fileName="logs/test1.log" append="true">
            <PatternLayout pattern="[%d{HH:mm:ss.SSS}] [%t] %-5level %logger{36} - %msg%n"/>
        </File>

        <!-- 滚动文件输出 -->
        <RollingFile name="rollingFile"
                     fileName="logs/test2.log"
                     filePattern="logs/test2-%d{yyyy-MM-dd}-%i.log.gz">
            <PatternLayout pattern="[%d{HH:mm:ss.SSS}] [%t] %-5level %logger{36} - %msg%n"/>
            <Policies>
                <TimeBasedTriggeringPolicy interval="1" modulate="true"/>
                <SizeBasedTriggeringPolicy size="10MB"/>
            </Policies>
            <DefaultRolloverStrategy max="30"/>
        </RollingFile>
    </Appenders>

    <!-- 定义日志规则 -->
    <Loggers>
        <!-- 单独为包设置级别 -->
        <Logger name="com.example" level="debug" additivity="false">
            <AppenderRef ref="console"/>
            <AppenderRef ref="file"/>
        </Logger>

        <!-- 单独为第三方库设置级别 -->
        <Logger name="org.springframework.web" level="warn" additivity="false"/>

        <!-- 全局设置 -->
        <Root level="debug">
            <AppenderRef ref="console"/>
            <AppenderRef ref="file"/>
            <AppenderRef ref="rollingFile"/>
        </Root>
    </Loggers>
</Configuration>
```