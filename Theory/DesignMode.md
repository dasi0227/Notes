# 设计模式



   * [SOLID 原则](#solid-原则)
      * [S 单一指责原则](#s-单一指责原则)
      * [O 开闭原则](#o-开闭原则)
      * [L 里氏替换原则](#l-里氏替换原则)
      * [I 接口隔离原则](#i-接口隔离原则)
      * [D 依赖倒置原则](#d-依赖倒置原则)
   * [设计模式](#设计模式)
      * [定义](#定义)
      * [Spring 用到的](#spring-用到的)
   * [工厂模式 Factory](#工厂模式-factory)
      * [定义](#定义)
      * [简单工厂](#简单工厂)
      * [工厂方法](#工厂方法)
      * [抽象工厂](#抽象工厂)
   * [单例模式 Singleton](#单例模式-singleton)
      * [定义](#定义)
      * [饿汉式](#饿汉式)
      * [懒汉式](#懒汉式)
      * [静态内部类](#静态内部类)
      * [枚举单例](#枚举单例)
   * [适配器模式 Adapter](#适配器模式-adapter)
      * [定义](#定义)
      * [类适配器](#类适配器)
      * [对象适配器](#对象适配器)
   * [代理模式 Proxy](#代理模式-proxy)
      * [定义](#定义)
      * [静态代理](#静态代理)
      * [JDK](#jdk)
      * [CGLIB](#cglib)
   * [观察者模式 Observer](#观察者模式-observer)
   * [装饰器模式 Decorator](#装饰器模式-decorator)
   * [责任链模式 Chain of Responsibilit](#责任链模式-chain-of-responsibilit)
   * [策略模式 Strategy](#策略模式-strategy)
   * [状态模式 State](#状态模式-state)



## SOLID 原则

### S 单一指责原则

**单一职责原则（Single Responsibility Principle）**：一个类或一个模块应该只负责一类功能，从而降低代码的耦合度

```java
// ❌：UserService 还需要负责邮件相关的功能
public class UserService {
    void register(User user) { /* 注册用户 */ }
		void sendEmail(User user) { /* 发送邮件 */ }
}
// ✅：拆分为两个类
public class UserService {
    void register(User user) { /* 注册用户 */ }
}
public class EmailService {
		void sendEmail(User user) { /* 发送邮件 */ }
}
```

### O 开闭原则

**开闭原则（Open-Closed Principle）**：对扩展开放，对修改关闭，也就是当需要增加新功能时，应该创建新的 API 而不是修改原有的 API

```java
// ❌：每新增一个形状都需要修改方法
public double calcArea(Object shape) {
    if (shape instanceof Circle) return ...;
    if (shape instanceof Rectangle) return ...;
    return 0;
}

// ✅：每新增一个形状只需要多写一个类
interface Shape {
    double area();
}
class Circle implements Shape { double area() { return ...; } }
class Rectangle implements Shape { double area() { return ...; } }
```

### L 里氏替换原则

**里氏替换原则（Liskov Substitution Principle）**：子类必须能替换父类，并且不会影响父类预期的行为

```java
// ❌：鸵鸟 Ostrich 继承了鸟但是不能执行 fly 方法
class Bird { void fly() {} }
class Sparrow extends Bird { void fly() { ... } }
class Ostrich extends Bird { void fly() { throw new UnsupportedOperationException(); }}

// ✅：将非通用方法单独抽离出来
interface Bird { }
interface Flyable { void fly(); }
class Sparrow implements Bird, Flyable { void fly() { ... } }
class Ostrich implements Bird { }
```

### I 接口隔离原则

**接口隔离原则（Interface Segregation Principle）**：接口要尽可能地小而专/垂直/细粒度，避免“胖接口”

```java
// ❌：Dog 不会飞但被迫重写 fly
interface Animal {
    void fly();
    void run();
}
class Dog implements Animal { 
  void fly() { ... }
  void run() { ... }
}

// ✅：细分为两个接口
interface Runnable { void run(); }
interface Flyable { void fly(); }
class Dog implements Runnable { ... }
```

### D 依赖倒置原则

**依赖倒置原则（Dependency Inversion Principle）**：高层模块不应该依赖于底层模块，代码的依赖关系应该通过抽象来建立

```java
// ❌：UserRepository 实体直接依赖于 MySQLConnection 实体，无法切换数据库
class MySQLConnection { void connect() {} }
class UserRepository { private MySQLConnection conn = new MySQLConnection(); }

// ✅：通过抽象 DBConnection 类建立依赖关系
interface DBConnection { void connect(); }
class MySQLConnection implements DBConnection { public void connect() {} }
class UserRepository {
    private DBConnection conn;
    public UserRepository(DBConnection conn) { this.conn = conn; }
}
```



## 设计模式

### 定义

设计模式不是代码实现，而**是代码抽象/蓝图/模版，是在特定场景下被长期验证的、可复用的代码设计经验**，描述了**如何组织类和对象来完成某个设计目标**，核心目标是确保代码的**可读、可复用、可扩展、可维护**

| **类别** | **关注点** | **理解** | **例子** |
| ---------------------------- | -------- | ------------------------------------------------------------ | ---------------------------------------------------- |
| **创建型模式（Creational）** | 对象创建 | 隐藏实例的实现类和创建过程 | 单例、工厂 |
| **结构型模式（Structural）** | 对象组合 | 在不改变原有类的情况下，通过组合为系统增加新功能 | 适配器、装饰器、代理、桥接 |
| **行为型模式（Behavioral）** | 对象协作 | 定义对象的通信模式来降低代码耦合度和交互复杂度，使得对象之间互不干扰 | 责任链、观察者、迭代器、策略、状态、模板方法、解释器 |

### Spring 用到的

- 工厂模式：ApplicationContext 工厂通过传递 Bean 的名称和类型生产 Bean
- 单例模式：Spring IoC 保证所有 Bean 都是单例
- 代理模式：Spring AOP 通过 JDK/CGLIB 生成动态代理来织入切面
- 适配器模式：RequestMappingHandlerAdapter 让不同 Controller 方法都能被统一调用
- 观察者模式：ApplicationListener 和 ApplicationEvent 实现了事务的定义和事务监听者
- 装饰器模式：BeanWrapper 在调用 setPropertyValue 方法时会把字符串类型转换为对应类型
- 责任链模式：HandlerInterceptor 定义了拦截器，请求可逐层处理或中断
- 策略模式：Resource 接口有 ClassPathResource、FileSystemResource、UrlResource 等实现
- 模版方法模式：JdbcTemplate 和 RestTemplate 实现了固定流程，用户只需要传 SQL 和 URL



## 工厂模式 Factory

### 定义

**将对象的创建逻辑封装，对外提供统一的获取接口**

- **类数量膨胀**：每增加一种产品就需要增加对应工厂类，代码量上升
- **简单工厂不符合开闭原则**：新增产品必须修改工厂代码

<img src="https://dasi-blog.oss-cn-guangzhou.aliyuncs.com/Java/202509282353467.png" alt="image-20250928235339380" style="zoom:50%;" />

### 简单工厂

方式 1：直接传递类名字符串，然后用 if-else 来判断，这样做的坏处是违背了开闭原则

```java
public class ShapeFactory {
    public static Shape newShape(String type) {
        if ("circle".equals(type)) return new Circle();
        if ("rect".equals(type)) return new Rectangle();
        throw new IllegalArgumentException("未知类型");
    }
}
```

方式 2：由静态方法名来指定创建类，遵循开闭原则

```java
public class ShapeFactory {
    public static Circle newCircle() {
      	return new Circle();
    }
    public static Rectangle newRectangle() {
      	return new Rectangle();
    }
}
```

### 工厂方法

不需要单独创建一个工厂类，而是作为类的静态方法来创建当前类的对象

```java
public class Circle {
  	private Circle() {}
  	public static Circle newCircle() {
      	return new Circle();
    }
}
```

### 抽象工厂

在不修改底层工厂类的情况下，提供一个顶层抽象工厂类，从而可以灵活扩展产品类。实际上还可以创建多个抽象子工厂类，然后再由一个顶级抽象工厂类实现耦合

```java
public interface ShapeFactory {
  	Shape newShape();
}

public class CircleFactory implenments ShapeFactory {
	  private Circle() {}
  
  	@Override
  	public Shape newShape() {
      	return new Circle();
    }
}

public class RectangleFactory implenments ShapeFactory {
	  private Rectangle() {}
  
  	@Override
  	public Shape newShape() {
      	return new Rectangle();
    }
}
```



## 单例模式 Singleton

### 定义

**保证一个类只有一个实例，并提供全局访问点**

- **扩展性差**：需要将类的构造方法声明为私有，限制了继承与多态使用，不利于功能拓展
- **隐藏全局状态**：模块间可能通过单例产生隐性耦合，违背单一职责
- **线程不安全**：并发场景下，多线程可能会创建多个实例

### 饿汉式

在类加载的时候创建实例，即定义一个静态常态类对象并初始化，可以保证线程安全，但实例对象不一定会用到，可能会浪费内存

```java
public class Singleton {
    // 私有化构造
    private Singleton() {}
    // 类加载时就创建实例，静态常量保证了线程安全
    private static final Singleton instance = new Singleton();
    // 提供公共访问⽅法
    public static Singleton getInstance() {
        return instance;
    }
}
```

### 懒汉式

在类对象被使用的时候才创建实例，虽然可以节省内存，但是在多线程高并发下可能会创建多个实例

```java
public class Singleton {
    // 私有化构造
    private Singleton() {}
    // 类加载时不初始化
    private static Singleton instance;
    // 提供公共访问⽅法
    public static Singleton getInstance() {
      	// 当且仅当为空才创建，线程不安全
      	if (instance == null) {
          	instance = new Singleton();
        }
        return instance;
    }
}
```

为了保证线程安全，可以通过给方法加 synchronized 关键字来保证线程安全，但是这样做会很影响并发性能

```java
public class Singleton {
    // 私有化构造
    private Singleton() {}
    // 类加载时不初始化
    private static Singleton instance;
    // 提供上锁的公共访问⽅法
    public synchronized static Singleton getInstance() {
      	// 当且仅当为空才创建
      	if (instance == null) {
          	instance = new Singleton();
        }
        return instance;
    }
}
```

实际上，可以利用类的监控器锁来锁住创建对象的代码而不是一整个方法，但是需要把 instance 声明为 volatile，防止代码重排序导致锁失效

```java
public class Singleton {
    // 私有化构造
    private Singleton() {}
    // 类加载时不初始化，并加上 volatile
    private static volatile Singleton instance;
    // 提供公共访问⽅法
    public static Singleton getInstance() {
      	// 当且仅当为空才创建，这里可能会放入多个线程
      	if (instance == null) {
          	// 锁住创建过程
          	synchronized (Singleton.class) {
              	// 再次判断，双重检查
              	if (instance == null) {
                    instance = new Singleton();     
                }
            }
        }
        return instance;
    }
}
```

### 静态内部类

外部类在加载的时候，不会立刻加载内部类，只有用到的时候才会加载，JVM 保证 final 字段在多线程高并发环境下也只会执行一次，所以也不需要 synchronized 或 volatile

```java
public class Singleton {
		// 私有化构造
  	private Singleton() {}
  	// 内部静态类：延迟加载
  	private static class SingletonHolder {
      	// 静态常量：线程安全
      	private static final Singleton instance = new Singleton();
    }
		// 提供公共访问⽅法
  	public static Singleton getInstance() {
      	return SingletonHolder.instance;
    }
}
```

### 枚举单例

Java 的枚举类型在底层是一个特殊的类，枚举类的实例会在类加载的时候就创建完成，JVM 会保证它的唯一性和线程安全，甚至连构造器都不需要写，而且可以防反射来破坏单例，但是这样做的缺陷就在于 enum 从语义上不如 class 直观，而且无法实现懒加载

```java
public enum Singleton {
    INSTANCE;
}
```



## 适配器模式 Adapter

### 定义

**将一个类的接口转换为客户端期望的另一种接口来实现兼容**

- **系统的复杂性增加**：引入额外适配层，阅读和维护难度变高
- **滥用风险**：过度使用可能掩盖系统真正的设计问题

![image-20250929084401500](https://dasi-blog.oss-cn-guangzhou.aliyuncs.com/Java/202509290844625.png)

### 类适配器

Adapter 类继承了 Adpatee 并实现了 Target，由于 Java 是单继承制，因此一个 Adapter 只能适配一个 Adaptee，耦合度很高

```java
public interface MediaPlayer {
    void play(String fileName);
}

public class OldPlayer {
    public void playFile(String fileName) {
        System.out.println("Playing with OldPlayer: " + fileName);
    }
}

public class PlayerAdapter extends OldPlayer implements MediaPlayer {
    @Override
    public void play(String fileName) {
        playFile(fileName);
    }
}
```

### 对象适配器

Adapter 只需要实现了 Target，在内部持有 Adpatee 实例，这样一个 Adapter 就可以同时适配多个不同的 Adpatee

```java
public interface MediaPlayer {
    void play(String fileName);
}

public class OldPlayer {
    public void oldPlay(String fileName) {
        System.out.println("Playing with OldPlayer: " + fileName);
    }
}

public class NewPlayer {
    public void newPlay(String fileName) {
        System.out.println("Playing with NewPlayer: " + fileName);
    }
}

class PlayerAdapter implements MediaPlayer {
    private Object adaptee;
  
  	// 构造时需要传递适配者对象
    public PlayerAdapter(Object adaptee) {
        this.adaptee = adaptee;
    }
  
  	// 根据适配者类型执行
    @Override
    public void play(String fileName) {
        if (adaptee instanceof OldPlayer) {
            ((OldPlayer) adaptee).oldPlay(fileName);
        } else if (adaptee instanceof NewPlayer) {
            ((NewPlayer) adaptee).newPlay(fileName);
        }
    }
}
```



## 代理模式 Proxy

### 定义

**通过代理对象控制对真实对象的访问，并可在调用前后增加额外逻辑**

- **性能开销**：增加一层代理调用，可能影响性能
- **类数量增多**：需要额外代理类，结构变复杂
- **调试困难**：排查问题时容易混淆真实对象和代理对象

![image-20250929084428510](https://dasi-blog.oss-cn-guangzhou.aliyuncs.com/Java/202509290844682.png)

### 静态代理

静态代理指的是开发者手动编写代理类，在编译器就能确定代理，但这样每多一个接口就要写一个代理类，如果增强逻辑一致，会造成大量代码冗余，同时不利于大规模扩展。相反动态代理就是指在代码运行过程中，由专门的对象根据接口定义自动生成代理类，不需要手动编写代理类代码

```java
interface Service {
    void doSomething();
}

class RealService implements Service {
    public void doSomething() {
        System.out.println("执行真实业务逻辑");
    }
}

class ServiceProxy implements Service {
    private RealService realService = new RealService();
    public void doSomething() {
        System.out.println("代理前：日志");
        realService.doSomething();
        System.out.println("代理后：收尾");
    }
}
```

### JDK

JDK 动态代理在运行时通过 Proxy.newProxyInstance() 方法生成一个实现指定接口的代理类实例，这个方法需要传入类加载器、接口数组以及 InvocationHandler 的实现。代理类的方法调用会被转发到 InvocationHandler.invoke()，底层依赖反射来增强和织入代理逻辑

> 必须基于同一接口，如果不存在该接口则无法使用，而且反射的开销比较大

```java
interface Service {
    void doSomething();
}

class RealService implements Service {
    public void doSomething() {
        System.out.println("执行业务逻辑");
    }
}

class ProxyHandler implements InvocationHandler {
    private Object realSubject;
  
    public ProxyHandler(Object realSubject) { 
      	this.realSubject = realSubject;
    }
  
  	@Override
    public Object invoke(Object proxy, Method method, Object[] args) throws Throwable {
        System.out.println("代理前：日志");
        Object result = method.invoke(realSubject, args); // 调用实际类方法
        System.out.println("代理后：收尾");
        return result;
    }
}

public class Client {
    public static void main(String[] args) {
        Service real = new RealService();
        Service proxy = (Service) Proxy.newProxyInstance(
            real.getClass().getClassLoader(),
            real.getClass().getInterfaces(),
            new ProxyHandler(real));
        proxy.doSomething();
    }
}
```

### CGLIB

CGLIB 动态代理基于字节码生成技术，在运行时为目标类创建一个子类，这个子类会重写目标类的非 final 方法，并在方法中调用 MethodInterceptor.intercept()，会调用 MethodProxy.invokeSuper() 来调用父类方法，这样就能在方法执行前后织入增强逻辑

> 不需要接口，对任何类都可以，虽然字节码生成的成本比 JDK 高很多，但是一劳永逸，即调用开销会比 JDK 低很多

```java
class RealService {
    public void doSomething() {
        System.out.println("执行业务逻辑");
    }
}

class ProxyInterceptor implements MethodInterceptor {
    @Override
    public Object intercept(Object obj, Method method, Object[] args, MethodProxy proxy) throws Throwable {
        System.out.println("代理前：日志");
        Object result = proxy.invokeSuper(obj, args); // 调用父类方法
        System.out.println("代理后：收尾");
        return result;
    }
}

public class Client {
    public static void main(String[] args) {
        Enhancer enhancer = new Enhancer();
        enhancer.setSuperclass(RealService.class);
        enhancer.setCallback(new ProxyInterceptor());
        RealService proxy = (RealService) enhancer.create();
        proxy.doSomething();
    }
}
```



## 观察者模式 Observer

**定义一对多依赖关系，当主题状态改变时，所有观察者都会自动收到通知**

- **性能问题**：观察者数量过多时，通知链可能影响系统响应速度
- **循环依赖风险**：观察者之间可能形成通知环路

![image-20250929084453081](https://dasi-blog.oss-cn-guangzhou.aliyuncs.com/Java/202509290844181.png)

```java
// 主题接口
interface Subject {
    void attach(Observer o); // 添加观察者
    void detach(Observer o); // 移除观察者
    void notifyObservers(String message); // 通知观察者
}

// 观察者接口
interface Observer {
    void update(String message); // 处理通知
}

class ConcreteSubject implements Subject {
    private List<Observer> observers = new ArrayList<>();

    @Override
    public void attach(Observer o) {
        observers.add(o);
    }

    @Override
    public void detach(Observer o) {
        observers.remove(o);
    }

    @Override
    public void notifyObservers(String message) {
        for (Observer o : observers) {
            o.update(message);
        }
    }
}

class ConcreteObserver implements Observer {
    private String name;

    public ConcreteObserver(String name) {
        this.name = name;
    }

    @Override
    public void update(String message) {
        System.out.println(name + " 收到通知: " + message);
    }
}
```



## 装饰器模式 Decorator

**在不修改原始类的情况下，动态为对象添加新功能**

- **类数量增多**：每种增强都要实现一个装饰类
- **顺序敏感**：装饰器的叠加顺序可能影响最终结果

![image-20250929084528301](https://dasi-blog.oss-cn-guangzhou.aliyuncs.com/Java/202509290845379.png)

```java
// 接口，需要被实现/装饰
interface Coffee {
    public String getDetail();
    public double getCost();
}

// 最基础的实现
class Americano implements Coffee {
    @Override
    public String getDetail() {
        return "美式";
    }

    @Override
    public double getCost() {
        return 9.9;
    }
}

// 拿到基础实现类的引用，不需要实现接口方法，因此声明为抽象类
abstract class CoffeeDecorator implements Coffee {
    protected Coffee decoratedCoffee;
    public CoffeeDecorator(Coffee coffee) {
        this.decoratedCoffee = coffee;
    }
}

// 冰块修饰
class IceDecorator extends CoffeeDecorator {
    // 拿到基础实现类的引用
    public IceDecorator(Coffee coffee) {
        super(coffee);
    }

    // 装饰 Ice
    @Override
    public String getDetail() {
        return decoratedCoffee.getDetail() + " + 一份牛奶";
    }

    // 装饰 Ice
    @Override
    public double getCost() {
        return decoratedCoffee.getCost() + 2.0;
    }
}

// 糖度修饰
class SugarDecorator extends CoffeeDecorator {
    // 拿到基础实现类的引用
    public SugarDecorator(Coffee coffee) {
        super(coffee);
    }

    // 装饰 Sugar
    public String getDetail() {
        return decoratedCoffee.getDetail() + " + 一份焦糖";
    }

    // 装饰 Sugar
    public double getCost() {
        return decoratedCoffee.getCost() + 2.0;
    }
}

// 客户端
public class Client {
    public static void main(String[] args) {
        // 基础实现类
        Coffee coffee = new Americano() {};
        System.out.println(coffee.getDetail() + " -> " + coffee.getCost());

        // 加了两层装饰器
        coffee = new IceDecorator(coffee);
        coffee = new SugarDecorator(coffee);
        System.out.println(coffee.getDetail() + " -> " + coffee.getCost());
    }
}

/* 输出：
美式 -> 9.9
美式 + 一份牛奶 + 一份焦糖 -> 13.9
*/
```



## 责任链模式 Chain of Responsibilit

**将多个处理器串成一条链，请求沿链传递，直到某个处理器处理为止**

- **无处理者风险**：如果没有合适的处理者，请求可能被丢弃
- **调试不便**：链条过长时，很难追踪到底哪个节点处理了请求

![image-20250929084954406](https://dasi-blog.oss-cn-guangzhou.aliyuncs.com/Java/202509290849597.png)

```java
// 抽象处理器
abstract class Handler {
    protected Handler next;

    public void setNext(Handler next) {
        this.next = next;
    }

    public abstract void handleRequest(int level);
}

// 具体处理器 1
class LevelOneHandler extends Handler {
    @Override
    public void handleRequest(int level) {
        if (level == 1) {
            System.out.println("一级处理者处理请求");
        } else if (next != null) {
            next.handleRequest(level);
        }
    }
}

// 具体处理器 2
class LevelTwoHandler extends Handler {
    @Override
    public void handleRequest(int level) {
        if (level == 2) {
            System.out.println("二级处理者处理请求");
        } else if (next != null) {
            next.handleRequest(level);
        }
    }
}

// 客户端
public class Client {
    public static void main(String[] args) {
        Handler h1 = new LevelOneHandler();
        Handler h2 = new LevelTwoHandler();

      	// 组装责任链
        h1.setNext(h2);
      
      	int level = 2;
        h1.handleRequest(level);
    }
}

/* 输出：
一级处理者处理请求
二级处理者处理请求
*/
```



## 策略模式 Strategy

**定义一系列算法，并使它们可以互换，客户端可在运行时自由选择**

- **客户端知晓性强**：调用方必须知道有哪些策略，并选择合适的策略
- **类数量增多**：每种策略都是独立类，系统膨胀

![image-20250929085509093](https://dasi-blog.oss-cn-guangzhou.aliyuncs.com/Java/202509290855270.png)

```java
interface PaymentStrategy. {
  	void pay(int amount);
}

class WeChatPay implements PaymentStrategy {
    public void pay(int amount) {
        System.out.println("使用微信支付 " + amount + " 元");
    }
}

class AliPay implements PaymentStrategy {
    public void pay(int amount) {
        System.out.println("使用支付宝支付 " + amount + " 元");
    }
}

class PaymentContext {
    private PaymentStrategy strategy;
  
  	public PaymentContext() {}

    public PaymentContext(PaymentStrategy strategy) {
        this.strategy = strategy;
    }

    public void setStrategy(PaymentStrategy strategy) {
        this.strategy = strategy;
    }

    public void executePayment(int amount) {
        strategy.pay(amount);
    }
}

public class Client {
    public static void main(String[] args) {
        PaymentContext context = new PaymentContext();
      	context.setStrategy(new AliPay());
        context.executePayment(100);

        context.setStrategy(new AliPay());
        context.executePayment(200);
    }
}
/* 输出：
使用微信支付 100 元
使用支付宝支付 200 元
*/
```



## 状态模式 State

**允许对象在内部状态改变时改变其行为**

- **类数量膨胀**：每种状态都需要单独的类
- **切换逻辑分散**：状态切换逻辑可能分布在不同状态类中，维护困难

> 可以发现，策略模式和状态模式很像，但状态模式的状态之间是会自动切换的，而策略模式的策略之间必须由人为手动改变

![image-20250929090026488](https://dasi-blog.oss-cn-guangzhou.aliyuncs.com/Java/202509290900667.png)

```java
interface State {
    void switch(Context context);
}

class StartState implements State {
    @Override
    public void switch(Context context) {
        System.out.println("当前状态：开始");
        context.setState(new RunningState());
    }
}

class RunningState implements State {
    @Override
    public void switch(Context context) {
        System.out.println("当前状态：进行");
        context.setState(new StopState());
    }
}

class EndState implements State {
    @Override
    public void switch(Context context) {
        System.out.println("当前状态：停止");
        context.setState(new StartState());
    }
}

class Context {
    private State state;

    public Context(State state) {
        this.state = state;
    }

    public void setState(State state) {
        this.state = state;
    }

    public void request() {
        state.switch(this);
    }
}

public class Client {
    public static void main(String[] args) {
        Context context = new Context(new StartState());

        context.request(); // 当前状态：开始
        context.request(); // 当前状态：运行
        context.request(); // 当前状态：开始
    }
}
```