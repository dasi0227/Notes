# Core



   * [I/O](#io)
      * [stream](#stream)
      * [File](#file)
      * [FileInputStream](#fileinputstream)
      * [FileOutputStream](#fileoutputstream)
      * [FileReader](#filereader)
      * [FileWriter](#filewriter)
   * [泛型](#泛型)
      * [定义](#定义)
      * [常用符号](#常用符号)
      * [边界指定](#边界指定)
      * [注意](#注意)
   * [线程](#线程)
      * [定义](#定义)
      * [流程](#流程)
      * [线程状态](#线程状态)
      * [用户线程和守护线程](#用户线程和守护线程)
      * [常见方法](#常见方法)
      * [Runnable 和 Thread](#runnable-和-thread)
      * [线程终止](#线程终止)
      * [同步机制](#同步机制)
   * [反射](#反射)
      * [定义](#定义)
      * [流程](#流程)
      * [ClassLoader](#classloader)
      * [Class](#class)
      * [Field/Method/Constructor](#fieldmethodconstructor)
      * [通过反射创建对象](#通过反射创建对象)
   * [网络](#网络)
      * [基础知识](#基础知识)
      * [传输层协议](#传输层协议)
      * [InetAddress](#inetaddress)
      * [Socket](#socket)
      * [DatagramSocket](#datagramsocket)
      * [DatagramPackage](#datagrampackage)
   * [JDBC](#jdbc)
      * [概述](#概述)
      * [建立连接的方式](#建立连接的方式)
      * [Connection](#connection)
      * [ResultSet](#resultset)
      * [Statement](#statement)
      * [SQL 注入](#sql-注入)
      * [PreparedStatement](#preparedstatement)
      * [事务](#事务)
      * [批处理](#批处理)
      * [连接池](#连接池)
      * [DBUtils](#dbutils)



## I/O

### stream

Java 的 I/O 是基于流的，也就是将数据看作一连串的字节或字符，从源头到目标按顺序读写

- 节点流：直接连接数据源的流，它是真正负责“和文件打交道”、“和内存通信”的那层
    - 文件系统：FileInputStream 连接到某个磁盘文件
    - 内存：ByteArrayInputStream、CharArrayReader 连接到内存中的某个数组
    - 网络连接：Socket.getInputStream() 连接远端主机发来的网络数据包
    - 管道：PipedInputStream 获取多线程间管道的数据
    - 标准输入：System.in 获取控制台输入或输入重定向的数据
- 处理流：不与数据源打交道，而是包裹在节点流外面的工具流，用来增强功能，可以链式地把多种处理流组合起来，为最简单的节点流不断添加新能力
    - 转换流：InputStreamReader/OutputStreamWriter，将字节流转换为字符流
    - 缓冲流：BufferedInputStream/BufferedOutputStream/BufferedReader/BufferedWriter，为字节/字符流添加缓冲区
    - 数据流：DataInputStream/DataOutputStream，可以按原生类型读取和写入
    - 检验流：CheckedInputStream / CheckedOutputStream，对输入流和输出流的内容做校验
    - 连接流：SequenceInputStream，可将多个 InputStream 顺序合并成一个连续流进行读取
    - 对象流：ObjectInputStream/ObjectOutputStream，将对象进行序列化和反序列化
        - 类和类的成员必须实现 Serializable 接口
        - 不可序列化的字段需要用 transient 关键字修饰，跳过序列化
        - transient 关键字修饰的字段不会被序列化写入文件，但是在反序列化时，这些字段会被自动赋值为默认值，因此不会报错
        - 静态成员不会被序列化，因为它不属于对象，而是属于类

### File

File 类不是文件内容的载体，而是对文件的抽象表示，本质是用于查询和操作文件的元信息，而不是修改其存储内容

- 构造方法（假设工作目录是 "/Users/dasi/projects"）
    - 一个路径（绝对 or 相对）："/Users/dasi/projects/data.txt" 或 "data.txt"
    - 上级路径+一个文件名："/Users/dasi/projects" + "data.txt"
    - 上级路径+下级路径："/Users/dasi" + "projects/data.txt"
- 核心方法
    - exists()：是否存在
    - isFile()：是否是普通文件
    - isDirectory()：是否是目录
    - canRead()/canWrite()/canExecute()：判断当前用户对该文件的权限
- createNewFile()：创建新文件，若存在则返回 false
    - mkdir()：创建单级目录
    - mkdirs()：递归创建目录
    - delete()：删除文件或清空目录
    - renameTo：移动文件或重命名文件（相当于 mv）
    - length()：返回文件的字节大小，目录返回 0
    - lastModified：返回最后修改时间的时间戳
    - getName()：返回文件名（不含路径）
    - getPath()：返回路径
    - getAbsolutePath()：返回绝对路径
    - getParent()：返回上级目录
    - list()：列出目录下所有文件的 String 名字数组，如果不是目录返回 null
    - listFiles()：列出目录下所有文件的 File 对象数组，如果不是目录返回 null

> 目录也是特殊的文件，在这里如果没有特殊说明的时候不做区分

### FileInputStream

- int read()：返回下一个字节（0–255），到末尾返回 -1
- int read(byte[] b)：读取最多 b.length 个字节到 b 中，返回实际读取到字节数，到末尾返回 -1
- int read(byte[] b, int off, int len)：读取最多 len 个字节到 b 从索引 off 开始存放，返回实际读取到字节数，到末尾返回 -1
- long skip(long n)：跳过并丢弃接下来的 n 个字节，返回实际跳过的字节数
- int available()：返回在不阻塞情况下可直接读取的字节数估计
- void close()：关闭此流并释放与之关联的系统资源

### FileOutputStream

- void write(int b)：写入单个字节，将参数 b 的最低 8 位写入文件
- void write(byte[] b)：将字节数组 b 中的所有字节一次性写入文件
- void write(byte[] b, int off, int len)：从数组 b 的索引 off 开始，写入 len 个字节到文件
- void flush()：刷新此输出流，强制将所有缓冲区中的字节写入底层文件系统
- void close()：关闭此输出流并释放与之关联的系统资源

### FileReader

- int read()：读取下一个字符（0–65535），到末尾返回 -1
- int read(char[] cbuf)：尝试读取最多 cbuf.length 个字符到 cbuf，返回实际读取数，末尾返回 -1
- int read(char[] cbuf, int off, int len)：从 cbuf[off] 开始写入最多 len 个字符，返回实际读取数，末尾返回 -1
- long skip(long n)：跳过并丢弃接下来的 n 个字符，返回实际跳过数
- boolean ready()：判断流是否已就绪可读（不会阻塞）
- boolean markSupported()：标记功能是否受支持（通常返回 false）
- void close()：关闭此流并释放与之关联的系统资源

### FileWriter

- 构造函数可以传入参数 boolean append：true 表示追加模式，false 表示覆盖模式，不传入默认是覆盖模式
- void write(int c)：写入单个字符
- void write(char[] cbuf)：将整个字符数组写入
- void write(char[] cbuf, int off, int len)：从 cbuf[off] 开始写入 len 个字符
- void write(String str)：写入整个字符串
- void write(String str, int off, int len)：写入字符串 str 中从 off 开始的 len 个字符
- void flush()：刷新此流，强制将缓冲区数据写入底层文件系统
- void close()：关闭此流并释放与之关联的系统资源



## 泛型

### 定义

Java 泛型是一种参数化类型机制，可以在类、接口、方法中定义时使用占位符代表类型，使用时再指定具体类型，提高代码的复用性和类型安全性

- 类泛型：class Box<T1,T2,...> {...}
- 接口泛型：interface MyList<T1,T2,...> {...}
- 方法泛型：<T1, T2, ...> 返回类型 方法名(参数列表) { ... }

> 注意区分使用类泛型的方法和利用泛型的方法

### 常用符号

| **符号** | **含义** |
| ---- | --------------------- |
| **T** | Type，任意类型 |
| **E** | Element，集合元素类型 |
| **K** | Key，键 |
| **V** | Value，值 |
| **?** | 通配符，未知类型 |


### 边界指定

- \<?>：支持任意类型
- \<? extends A>：上界，只能是 A 或其子类
- \<? super A>：下界，只能是 A 或其父类

### 注意

- 泛型擦除：指定泛型类型是为了编译器而不是 JVM，也就是为了应付编译而不是应付运行，编译器会根据你传递的类型进行类型检查、自动类型推从而省去强转，编译通过后，编译器会直接用 Object 代替泛型参数
    - 不能 new T[]：因为运行时 T 已经被擦除，JVM 无法确定数组的真实类型
    - 不能 instanceof T：因为运行时没有 T 的类型信息，类型已被擦除，无法进行类型判断
- 类加载机制：类先加载再使用，静态内容属于类，不依赖对象
    - 静态变量/方法不能使用类的 T：因为静态变量/方法属于类级别，而泛型 T 是对象级别，类加载时还无法解析 T
    - 没有指定泛型参数时，默认使用 Object
- 泛型类型限制
    - 泛型只能是引用类型，不能是基本数据类型
    - 给泛型指定具体类型后，可以传入该类型或其子类类型



## 线程

### 定义

线程由进程或者其他线程创建的，程序中可以并发执行的最小单位，每个线程都有自己独立的栈空间和执行路径，多个线程可以同时跑不同的代码段

- 单线程：同一时刻只有一个线程执行
- 多线程：同一时刻，多个线程执行
- 并发：同一时刻，多个任务在同个核心交替执行，微观下是轮流执行，宏观下是同时执行
- 并行：同一时刻，多个任务在不同核心同时执行，微观和宏观都是同时执行 
- 异步（Asynchronous）：不等结果，调用者继续执行
- 同步（Synchronous）：顺序执行，调用者会等待任务完成后再继续执行

### 流程

1. Java 程序启动
2. 操作系统创建了一个 JVM 进程
3. JVM 创建 main 线程（运行代码）
4. JVM 创建守护线程
    - GC Thread：垃圾回收线程，自动释放内存
    - Finalizer：调用对象的 finalize() 方法
    - Reference Handler：处理软引用/弱引用/虚引用等机制
    - Signal Dispatcher：处理操作系统信号，如 Ctrl+C 等
5. main 线程执行 main 方法
6. main 线程继续创建多个子线程（用户线程） 
7. 当所有非守护线程执行完，守护线程会被强制终止，操作系统销毁 JVM 进程

### 线程状态

- NEW（新建）：线程对象刚被创建，还未调用 start()，尚未与任何底层线程关联
- RUNNABLE（可运行）/READY（就绪）：线程已调用 start()，正等待 JVM 和操作系统调度，一旦获取到 CPU 时间片，就执行 run() 方法
- RUNNING（允许中）：线程正在占用 CPU 时间片，执行 run 方法
- BLOCKED（阻塞）：因锁被其他线程持有而挂起，等待锁释放
- WAITING（等待）：线程主动放弃 CPU，并无限期等待另一个线程的通知／中断／定时等待结束
- TIMED_WAITING（超时等待）：在有超时参数的等待方法中挂起，到期后自动唤醒或被中断
- TERMINATED（终止）：run() 方法执行完毕正常返回，或抛出未捕获异常，线程生命周期结束，再也不会被调度

### 用户线程和守护线程

- 用户线程（User）：也称为“前台线程”，是完成应用程序核心业务逻辑的线程，JVM 会一直等待所有用户线程结束后，才允许进程退出
- 守护线程（Daemon）：也称为“后台线程”或“服务线程”，通常用来执行一些辅助性工作，如垃圾回收、监控、日志清理等，当 JVM 发现只剩下守护线程 在运行时，会自动结束进程，不再等待它们完成（没有了用户线程，守护线程守护什么呢？）

必须在 start() 之前调用 setDaemon()，否则抛出 IllegalThreadStateException，因为操作系统的线程属性一旦创建，无法在运行时再更改守护/后台标志

- setDaemon(true)：将调用线程标记为守护线程
- setDaemon(false)：将调用线程标记为非守护线程（默认行为）
- isDaemon()：查询线程当前是否为守护线程

### 常见方法

- start()：启动线程，异步执行
- run()：是线程的执行体，定义了线程启动后要执行的具体逻辑
- static Thread currentThread()：返回对当前正在执行代码的线程对象的引用，常用于在线程内部自我检测
- setName(String name)、getName()：设置和获取线程的名称
- setPriority(int newPriority)、getPriority()：设置和获取线程的调度优先级
    - Java 定义了从 Thread.MIN_PRIORITY（1）到 Thread.MAX_PRIORITY（10）共 10 个级别
    - 默认优先级是 Thread.NORM_PRIORITY（5）
    - 高优先级线程相比低优先级线程更容易获得 CPU 时间片，但具体调度行为依赖于操作系统的线程调度策略，不能提供绝对保证！
- sleep(long millis)：是一个静态方法，用于让当前正在执行的线程暂停指定毫秒数
    - 在睡眠期间，线程放弃了 CPU 使用权，但不会释放已占有的锁资源
    - 如果在睡眠中被其他线程调用了 interrupt()，就会抛出 InterruptedException 并清除中断标志
- interrupt()：向目标线程发送中断信号
    - 并不会强制终止线程，而是设置线程的中断标志
    - 如果线程正阻塞在 sleep()、wait()、join() 等方法上，就会抛出一个 InterruptedException
    - 如果线程正运行中，则需要在合适的位置通过 Thread.interrupted() 或 isInterrupted() 来检测并响应中断
- yield()：提示当前线程让出 CPU 执行权，进入可运行（RUNNABLE）状态，但是无法确定何时让出，也无法确定是否让出
- join()：让当前线程阻塞，直到调用该方法的线程执行完毕，可以传入毫秒，表示最多阻塞时间

### Runnable 和 Thread

```java
Runnable task = new MyTask();
Thread thread = new Thread(task, "Worker-1");
thread.start();
```

- Runnable 接口：很小，内部只有 run 方法，定义了一段可在独立线程中执行的逻辑
- Thread 接口：很大，除了 run 还有很多其他方法
- 上述做法的好处
    1. 将任务和线程分离，让你的业务逻辑只关心实现 run 方法本身，而不必与线程创建、启动的细节耦合
    2. 任务类依然可以继承其他父类或实现更多接口
    3. 只需把同一个 Runnable 实例交给不同的 Thread 对象即可轻松共享状态，无需为每个线程都写一个新的子类

Thread 底层本质流程

1. JVM 在构造函数里把传入的 Runnable 对象赋给 this.target，并设置线程名称、优先级等，状态为 NEW
2. 用户线程执行 thread.start()
3. thread.start() 内部调用 start0()
4. start0() 内部根据操作系统类型调用 pthread_create（Linux）或 CreateThread（Windows）等，将资源（栈、TLS、调度上下文）分配给新线程，标记为可运行
5. 操作系统在某个时间片决定运行该内核线程，CPU 跳转到 HotSpot 提供的 JNI 入口
6. 在 JNI 入口完成 JVM 线程环境挂载后，调用 Java 层的 thread.run()
7. 如果构造时传入了 Runnable，则执行 target.run()，否则执行 this.run()

### 线程终止

1. run 正常执行完毕，线程自动终止
2. 如果 run() 方法内部抛出一个未被捕获的异常，JVM 会在本地入口捕获该异常，并终止线程
3. 调用 interrupt() 时，方法 Thread.currentThread().isInterrupted() 会返回中断，可以在 run 中循环判断从而终止
4. 也可以在 run 方法循环判断一个成员变量，并提供一个接口允许外部修改成员变量，从而实现终止


### 同步机制

同步含义

1. 互斥：保证同一时刻只有一个线程能执行某段访问共享资源的代码，避免出现竞争条件
2. 可见性：保证一个线程对共享变量的修改，能被其他线程及时且正确地看到

内置互斥锁：synchronized，由 JVM 在编译字节码时插入 monitorenter（获得锁） 和 monitorexit（释放锁） 指令

- 正常退出：当线程执行到同步代码块或同步方法末尾
- 正常跳出：break 或 return 等跳出执行流的操作
- 异常退出：抛出未捕获异常
- 方法调用：调用了 wait()

同步代码块

- 锁对象可以是任意非空引用类型
    - 实例锁/this：保证同一个实例的多个线程不会并发执行该代码块
    - 类锁/class：控制所有该类实例间的互斥
    - 自定义私有锁：事先在类中声明一个私有的 final Object lock = new Object()，不会被外部代码意外地或恶意地锁住或释放，适用于类的内部上锁
- 只有获取到锁对象的线程才能执行这里代码块里的代码

```java
synchronized (锁对象) {
    // 代码
}
```

同步方法：在方法声明上加 synchronized

- 非静态方法：等同于在方法体最外层做 synchronized(this){…}
- 静态方法：等同于在方法体最外层做 synchronized(MyClass.class){…}

```java
public synchronized void foo() {}
public static synchronized void bar() {}
```



## 反射

### 定义

指的是程序在运行时能够动态地获取类的信息（如类名、字段、方法、构造器等），并能够操作这些信息（创建实例、调用方法、访问字段）的一种机制

尽管反射带来一定性能开销并略微破坏封装，但在高度动态化场景下，反射是 Java 生态繁荣的基石之一

- 灵活性：反射能根据运行时环境（配置、注解、网络协议）来决定加载与调用哪段代码
- 可扩展性：系统核心代码无需预见所有业务场景，通过反射动态“插入”新功能，新类可以按需加入
- 解耦与自动化：将对象创建、依赖管理、方法调用交给运行期框架，业务代码只关注“做什么”，无需关心“怎么拿到对象”，提高开发效率

核心反射类：构成了 Java 在运行时动态发现并操纵类结构的能力

- Class：表示已加载到 JVM 中的一个类或接口
- Method：封装一个类中的单个方法
- Field：封装一个类中的单个字段
- Constructor：封装一个类的构造器

### 流程

加载（Loading）

1. 定位（Locate）：根据全限定名、类路径、自定义 ClassLoader 查找 .class 文件中的字节码流
2. 读取（Read）：将字节码读入内存缓冲区，准备交给 JVM 处理
3. 生成（Generate）：在方法区创建一个 java.lang.Class 实例，代表该类的运行时数据结构

链接（Linking）

1. 验证（Verification）：校验字节码文件格式、元数据一致性、控制流合法性等，确保不破坏 JVM 安全和稳定
2. 准备（Preparation）：为类的所有静态变量在方法区分配内存，并将它们初始化为默认值
3. 解析（Resolution）：将运行时常量池中的符号引用替换成直接引用

内存布置

- 方法区
    - java.lang.Class 对象实例：标识、加载器、继承与接口关系、字段、方法、构造器等
    - 运行时常量池：编译期的字面量值（数字、String 字面量等）和符号引用（类名、字段名+描述符、方法名+签名）
    - 静态数据：所有 static 字段的存储区
- 堆
    - 每个类的对象实例：通过 new、反射或数组创建的所有对象
    - 数组实例：各种维度的基本类型数组和引用类型数组，连续存放在堆上
    - 字符串常量池：String 字面量

区分

- 编译期常量：内联到每个用到它的类的运行时常量池中，不占用方法区的静态存储
- 运行时常量：和普通 static 字段一样，存放在方法区静态区，经 <clinit> 初始化结束后拥有最终值
- 符号引用：在编译期存入 .class 文件和类的运行时常量池中，以字符串形式标识目标
- 直接引用：解析完成后，将符号引用替换成具体的内存地址、指针或句柄

### ClassLoader

类加载器：Java 的一切都是类和对象，类加载器负责在运行时将字节码（.class 文件）加载到 JVM，并生成对应的 Class 对象

- Bootstrap（引导）：用原生代码实现，加载 JRE 中最基础的核心库，如 java.lang.*、java.util.*、java.io.*、java.net.* 等
- Platform/Extension（平台/扩展）：由 Java 程序自己实现，加载 JRE 扩展目录下的类库，如第三方 JDBC 驱动、JVM 工具/监控 jar 等
- Application/System（应用/系统）：加载用户类路径下的所有类

### Class

每个在 JVM 中加载的类或接口，都会对应一个唯一的 Class 对象

- Class 对象不是 new 出来，而是系统自动创建的
- Class 对象有且只有一个，因为类之被加载一次

常用方法

- 对象获取 
    - 全限定名加载：static Class<?> forName(String className)
    - 基础类型：String.class、int.class
    - 包装类：Integer.Type、Character.Type
    - 实例：obj.getClass()
- 元信息获取
    - Class<?> getClass()：获取运行时类型
    - Package getPackage()：获取所属 Package 信息
    - String getName()：获取含包类名
    - String getSimpleName()：获取不含包类名
    - ClassLoader getClassLoader()：获取加载此类的类加载器
- 层次获取
    - Class<? super T> getSuperclass()：获取直接父类
        - Class<?>[] getInterfaces()：获取直接实现的接口列表
- 字段获取
    - Field[] getFields()：返回含父类所有 public 字段
    - Field[] getDeclaredFields()：返回本类所有字段
    - Field getField(String name)：按名获取含父类的 public 字段
    - Field getDeclaredField(String name)：按名获取本类的字段
- 方法获取
    - Method[] getMethods()：返回含父类的所有 public 方法
    - Method[] getDeclaredMethods()：返回本类所有方法
    - Method getMethod(String name, Class<?>... paramTypes)：按签名获取含父类的 public 方法 
    - Method getDeclaredMethod(String name, Class<?>... paramTypes)：按签名获取本类的方法
- 构造器获取
    - Constructor<T>[] getConstructors()：本类所有 public 构造器
    - Constructor<T>[] getDeclaredConstructors()：本类所有构造器
    - Constructor<T> getConstructor(Class<?>... paramTypes) / getDeclaredConstructor(...)：按签名获取

### Field/Method/Constructor

通用 API

- String getName()：返回字段名
- int getModifiers()：返回修饰符
- boolean isAccessible()：检查是否可以访问
- void setAccessible(boolean flag)：强制设置 Java 访问权限

Field

- Class<?> getType()：返回字段类型
- Object get(Object obj)：读取指定对象实例的该字段值（静态字段传入 null）
- void set(Object obj, Object value)：为指定对象实例设置该字段值

Method

- Class<?> getReturnType()：返回方法返回值类型
- Class<?>[] getParameterTypes()：返回参数类型数组
- Class<?>[] getExceptionTypes()：返回方法声明抛出的异常类型
- Object invoke(Object obj, Object... args)：调用方法，obj 为实例（静态方法传 null）

Constructor

- Class<?>[] getParameterTypes()：返回构造器的参数类型数组
- T newInstance(Object... initargs)：使用此构造器创建新实例

> getModifiers() 返回一个位掩码（bit‐mask）整数，其中 PUBLIC=1， PRIVATE=2，PROTECTED=4，STATIC=8，FINAL=16，SYNCHRONIZED
> =32，VOLATILE=64，TRANSIENT=128，NATIVE=256

### 通过反射创建对象

（假设对象是 A）

1. 获取 Class 实例：forName
2. 获取 Constructor 实例：getConstructor/getDeclaredConstructor
3. private 需要暴破：setAccessible(true)
4. 创建 A 实例：newInstance(参数列表)

```java
public class User {
    private int age = 21;
    private String name = "dasi";

    public User() {

    }

    public User(String name) {
        this.name = name;
    }

    private User(int age, String name) {
        this.age = age;
        this.name = name;
    }

    public String toString() {
        return "User[ age=" + age + ", name=" + name + "] ";
    }
}

public class instanceDemo {
    public static void main(String[] args) throws ClassNotFoundException, InstantiationException, IllegalAccessException, NoSuchMethodException, InvocationTargetException {
        String userPath = "study.REFLECTION.ClassTest.ReflectInstance.User";
        // 1. 反射获取 Class 对象
        Class<?> userClass = Class.forName(userPath);
        // 2. 无参 public 构造
        Object o1 = userClass.newInstance();
        System.out.println(o1);
        // 3. 有参 public 构造
        Constructor<?> constructor1 = userClass.getConstructor(String.class);
        Object o2 = constructor1.newInstance("wyw");
        System.out.println(o2);
        // 4. 有参 private 构造
        Constructor<?> constructor2 = userClass.getDeclaredConstructor(int.class, String.class);
        constructor2.setAccessible(true);
        Object o3 = constructor2.newInstance(18, "jason");
        System.out.println(o3);
    }
}
```



## 网络

### 基础知识

区分

- 物理网卡（Network Interface Card, NIC）：属于物理层，是实际的硬件设备，比如插在主板上的以太网卡、Wi‑Fi 无线网卡、USB 有线网卡等，负责将数字信号转换为电/光/射频信号进行物理传输
- 网络接口（Network Interface）：属于链路层，是操作系统内核为每块物理网卡在软件中创建的抽象实体
- IP 地址：属于网络层，是分配给某个网络接口的逻辑地址，用于在不同主机间路由和寻址
- 端口（Port）：属于传输层，用于区分不同服务的标识，一个端口号加上一个 IP 地址就唯一标识网络上的一个“套接字”，即一条具体的网络连接

联系

- 操作系统内核加载物理网卡的驱动后，会为该硬件创建一个主网络接口，也可以创建任意多个虚拟接口
- 每个网络接口都可以分配一个或多个 IP 地址，IPv4 与 IPv6 各自独立
- IP 地址又可以对应很多个端口，表示对同一个远程对象使用不同服务

流程

1. 应用层的应用程序调用 Socket API，确定目标 IP + Port，将数据流（Stream）提交给传输层
2. 传输层将数据流切分成段（segment），添加源/目的端口等头信息，交给网络层
3. 网络层按目标 IP 查路由表，选定本地接口，添加源/目的 IP，封装为包（package）
4. 链路层在选定接口上添加源/目的 MAC，封装以太网帧（frame），发送到对应的网络接口
5. 物理层的物理网卡将每一帧的比特转换为电/光/射频信号，发往下一个网络节点

回环地址（Loopback）：用于主机的内部通信，不会发往物理网卡或真正的网络，常用于测试本地的协议栈是否正常

- IPv4：127.0.0.1
- IPv6：::1
- 主机名：localhost

通配符地址（Wildcard Address）：用于服务器程序绑定时，表示绑定到本机所有可用网络接口上的对应端口，常用于监听主机所有网卡的连接

- IPv4：0.0.0.0
- IPv6：:: 或 ::0

### 传输层协议

| **特性** | **TCP** | **UDP** |
| -------- | -------------------------------------------------- | ------------------------------------------ |
| **传输模式** | 面向连接：通信前需建立三次握手 | 无连接：无需握手，直接发送 |
| **可靠性** | 提供可靠传输：丢包重传、校验、确认与超时重发 | 不保证可靠：不重传，不确认 |
| **数据顺序** | 保证按发送顺序到达 | 无顺序保证：包可能乱序或丢失 |
| **流量控制** | 有：基于滑动窗口控制发送速率 | 无：发送速率由应用自主 |
| **拥塞控制** | 有：动态调整拥塞窗口 | 无 |
| **头部开销** | 20–60 字节（含可选选项字段） | 固定 8 字节 |
| **传输效率** | 较低：额外的可靠性与控制开销 | 较高：无额外控制，适合实时或小数据量应用 |
| **应用场景** | 文件传输(FTP)、网页(HTTP/HTTPS)、邮件(SMTP/POP3)等 | 视频/语音(VoIP)、DNS 查询、DHCP、在线游戏等 |

### InetAddress

位于 java.net 包里，本质是对一个 IP 地址（IPv4 或 IPv6）和可选主机名（HostName）的封装，不含端口，也不带实际网络连接

- IPv4：长度为 4 的 byte[] 存储 32 位地址
- IPv6：长度为 16 的 byte[] 存储 128 位地址
- 主机名：String 对象，可选的保存，否则为 null

类方法/静态方法

- InetAddress getLocalHost()：返回本地主机的地址对象
- InetAddress getByName(String host)：传入主机名，返回对应的地址对象
- InetAddress[] getAllByName(String host)：返回主机名对应的所有地址对象组成的数组
- getByAddress(byte[] addr)：传入原始 IP 字节数组构造地址对象
- getByAddress(String host, byte[] addr)：同上，并在对象中保留指定的主机名

对象方法/实例方法

- String getHostName()：返回此地址的主机名
- String getHostAddress()：返回 IP 地址
- byte[] getAddress()：返回 IP 地址的字节数组
- boolean isReachable(int timeout)：尝试在指定毫秒内 ping 此地址，返回是否可达
- isLoopbackAddress()：判断是否为回环地址 
- isAnyLocalAddress()：判断是否为通配符地址

### Socket

Socket 套接字用于网络通信中的 TCP 连接，将某一端的地址和端口号封装，使得程序可以像读写本地流一样，从另一端接受数据或发送数据到另一端

客户端：java.net.Socket

- 构造器
    - Socket(String host, int port)：指定服务端的主机名和端口
    - Socket(InetAddress address, int port)：指定服务端的地址和端口 
    - Socket(String host, int port, InetAddress localAddr, int localPort)：指定服务端地址/端口，同时绑定本地地址/端口
- 方法
    - void connect(SocketAddress endpoint, int timeout)：显式发起连接，可设置毫秒级超时
    - InputStream getInputStream()：获取读取远端数据的流
    - OutputStream getOutputStream()：获取写入远端数据的流
    - void setSoTimeout(int timeout)：设置 read() 操作的阻塞超时
    - void setTcpNoDelay(boolean on)：开启/关闭 Nagle 算法
    - boolean isConnected() / isClosed()：返回连接状态
    - void close()：关闭连接并释放资源

服务端：java.net.ServerSocket

- 构造器
    - ServerSocket(int port)：ServerSocket(int port)：在所有本地接口上监听指定端口
    - ServerSocket(int port, int backlog)：指定端口和等待队列长度
    - ServerSocket(int port, int backlog, InetAddress bindAddr)：指定监听端口、队列长度和本地绑定地址
- 方法
    - Socket accept()：阻塞等待并接收新连接，返回对应的客户端 Socket
    - void setSoTimeout(int timeout)：设置 accept() 的超时时间
    - void setReuseAddress(boolean on)：允许重用已释放的监听端口
    - int getLocalPort()：获取正在监听的本地端口
    - InetAddress getInetAddress()：获取本地绑定的地址
    - boolean isBound() / isClosed()：检查监听状态
    - void close()：停止监听并释放端口

流程

1. 客户端直接构造连接 / 先构造再 connect
2. 客户端配置选项
3. 客户端通过输出流写入数据
4. 服务端在端口构造监听
5. 服务端阻塞直到有新连接或超时
6. 服务端通过输入流读取数据

交互

- ServerSocket 的职责只在于监听和接收新的连接，但并不负责接发数据，而是不断 accept() 出若干个 Socket，每个 Socket 都代表了一个「客户端－服务端」通信会话，通过 Socket 实现接发数据
- 服务端可以通过一个 ServerSocket 创建出多个 Socket，从而实现一个服务端服务多个客户端，可以在循环中或为每个连接创建一个线程/任务来处理它们，这就是高并发的原型

### DatagramSocket

DatagramSocket 用于 UDP 无连接通信，既可发送也可接收 DatagramPacket

构造器

- DatagramSocket()
- DatagramSocket(int port)
- DatagramSocket(int port, InetAddress laddr)
- DatagramSocket(SocketAddress bindAddr)

API

- void send(DatagramPacket p)：向指定目标发送一个 UDP 包
- void receive(DatagramPacket p)：接收一个 UDP 包（阻塞），填充到 p 的缓冲区
- void connect(InetAddress address, int port)：“连接”到特定远端，以后只能与该地址/端口通信
- void disconnect()：取消 connect 后的固定目标限制
- boolean isConnected()：判断是否已 connect
- void setSoTimeout(int timeout)：设置 receive() 的阻塞超时（毫秒），超时抛 SocketTimeoutException
- void setBroadcast(boolean on)：开启/关闭允许发送广播包
- int getLocalPort() / InetAddress getLocalAddress()：获取本地绑定的端口和地址
- SocketAddress getRemoteSocketAddress()：如果已 connect()，返回远端地址/端口
- void close()：关闭 socket 并释放端口

### DatagramPackage

构造器

- DatagramPacket(byte[] buf, int length)
- DatagramPacket(byte[] buf, int offset, int length)
- DatagramPacket(byte[] buf, int length, InetAddress address, int port)
- DatagramPacket(byte[] buf, int offset, int length, InetAddress address, int port)
- DatagramPacket(byte[] buf, int offset, int length, SocketAddress address)
- DatagramPacket(byte[] buf, int length, SocketAddress address)

API

- byte[] getData()：返回缓冲区数组
- int getLength()：返回数据长度
- void setData(byte[] buf)／void setData(byte[] buf, int offset, int length)：设置缓冲区
- InetAddress getAddress()：返回目标（发送时）或源（接收时）IP
- int getPort()：返回目标或源端口
- SocketAddress getSocketAddress()：返回目标或源的 SocketAddress
- void setAddress(InetAddress addr)／void setPort(int port)：修改目标地址/端口
- int getOffset()：返回缓冲区偏移
- void setLength(int length)：设置预计接收的最大长度（接收时用）



## JDBC

### 概述

JDBC 是 Java 提供的一套标准 API，用于在 Java 程序中统一地访问各种关系型数据库，使得程序员不必关心底层数据库厂商的细节，就能使用统一的接口进行增删改查，实现跨数据库的可移植性

java.sql：是 Java 标准库里定义 JDBC API 的包，主要包含了操作关系型数据库所需的核心接口和类

- Driver：定义了数据库驱动必须实现的接口，负责将 JDBC 调用转为数据库厂商的网络协议
- DriverManager：加载并管理一组 Driver，通过它的 getConnection(...) 方法为应用提供 Connection
- Connection：表示与数据库的会话。可以用它来创建 Statement、开启/提交/回滚事务、获取元数据等
- Statement：执行静态 SQL
- PreparedStatement：执行带参数的预编译 SQL
- CallableStatement：调用存储过程
- ResultSet：封装 SELECT 查询结果，以游标方式逐行读取
- SQLException：所有 JDBC 操作抛出的异常类型，包含错误码和 SQL 状态码等信息
- DatabaseMetaData：用于查询数据库的元信息
- ResultSetMetaData：用于查询结果集的元信息

JDBC 流程

1. 加载驱动
2. 建立与数据库的连接
3. 创建 SQL
4. 执行 SQL
5. 处理返回的结果
6. 关闭资源

> 从 mysql 5.1.6 开始就不需要再注册驱动，因为底层已经自动帮我们实现了

### 建立连接的方式

利用 DriverManager.getConnection

```java
Connection conn = DriverManager.getConnection(url, user, password);
```

利用 DataSource

```java
MysqlDataSource ds = new MysqlDataSource();
ds.setURL(url);
ds.setUser(user);
ds.setPassword(password);
Connection conn = ds.getConnection();
```

### Connection

- Statement createStatement()：创建一个用于执行静态 SQL 的 Statement
- PreparedStatement prepareStatement(String sql)：创建一个可绑定参数的预编译 SQL 语句对象
- CallableStatement prepareCall(String sql)：创建一个调用存储过程的 CallableStatement
- DatabaseMetaData getMetaData()：获取此连接所对应数据库的元数据
- boolean isValid(int timeout)：检查连接在给定秒数内是否仍有效
- void setReadOnly(boolean readOnly)：将连接置为只读模式
- boolean isReadOnly()：检查是否只读
- String getSchema()：设置当前连接的默认模式
- void setSchema(String schema)：获取当前连接的默认模式
- boolean isClosed()：检查连接是否已关闭
- void close()：关闭连接

### ResultSet

ResultSet 就是对查询结果的“游标”（Cursor）封装，允许你以编程方式在它返回的行集合中移动、读取甚至更新

- boolean next()：移到下一行，返回 false 表示已到末尾
- boolean previous()：移到上一行，返回 false 表示已到开头
- boolean rs.first()：移到第一行
- boolean rs.last()：移到最后一行
- boolean absolute(int row)：移动到指定行号，正数从头数，负数从尾数
- rs.beforeFirst()：移到第一行之前，用于正序遍历
- rs.afterLast()：移到最后一行之后，用于倒序便利
- int getRow()：返回当前行号
- XXX getXXX(int columnIndex)：按列索引读取指定类型的值
- XXX getXXX(String columnLabel)：按列名称读取指定类型的值
- boolean wasNull()：判断上一次读取的列值是否为 SQL NULL
- void updateXXX(...)：修改当前行的列值
- void updateRow()：提交对当前行的修改
- void insertRow()：在插入行区域提交新行
- void deleteRow()：删除当前行
- void close()：关闭游标并释放资源
- ResultSetMetaData getMetaData()：获取列的元信息 
    - int getColumnCount()：返回结果集中列的总数
    - String getColumnName(int column)：返回第 column 列的名称
    - int getColumnType(int column)：获取第 column 列的 SQL 类型
    - boolean isAutoIncrement(int column)：判断是否自动增长

### Statement

- ResultSet executeQuery(String sql)：执行 SELECT 语句，返回查询结果的 ResultSet
- int executeUpdate(String sql)：执行 INSERT、UPDATE、DELETE、CREATE、DROP，返回受影响行数
- boolean execute(String sql)：通用执行方法，返回 true 表示返回 ResultSet，返回 false 表示返回受影响函数
- ResultSet getResultSet()：获取 ResultSet
- int getUpdateCount()：获取受影响行数
- void setMaxRows(int max) / int getMaxRows()：设置／获取查询返回的最大行数
- void setQueryTimeout(int seconds) / int getQueryTimeout()：设置／获取 SQL 执行的超时时间（秒）
- void close() / boolean isClosed()：关闭此 Statement 并释放资源／检查是否已关闭  

### SQL 注入

SQL 注入（SQL Injection）是一种常见的安全漏洞，攻击者通过在应用程序的输入中注入恶意的 SQL 片段，使后台数据库执行非预期的命令，从而达到窃取、篡改甚至删除数据的目的

```java
System.out.print("用户名：");
String inputUser = sc.nextLine().trim();
System.out.print("密码：");
String inputPwd  = sc.nextLine().trim();

// ⚠️ 漏洞写法：直接拼接用户输入到 SQL
String sql = "SELECT * FROM users "
			+ "WHERE username = '" + inputUser + "' "
			+   "AND passwd   = '" + inputPwd  + "'";
System.out.println("执行 SQL: " + sql);
```

假设用户名为 dasi，密码为 666

正常情况

```text
用户名：dasi
密码：666
执行 SQL: SELECT * FROM users WHERE username = 'dasi' AND passwd   = '666'
登录成功，欢迎 dasi

用户名：dasi
密码：999
执行 SQL: SELECT * FROM users WHERE username = 'dasi' AND passwd   = '999'
用户名或密码错误
```

SQL 注入

```text
用户名：whatever
密码：whatever' OR '1' = '1
执行 SQL: SELECT * FROM users WHERE username = 'whatever' AND passwd   = 'whatever' OR '1' = '1'
登录成功，欢迎 dasi
```

### PreparedStatement

PreparedStatement 实际上是继承 Statement 的子接口，相比于 Statement 的优点

- 预编译：在数据库端对 SQL 语句做一次解析、校验和执行计划生成，后续执行只需绑定新参数即可，性能更好
- 防止 SQL 注入：所有用户输入都通过 ? 占位符绑定，不会被当作 SQL 语句的一部分拼接执行
- 可重用：同一个 PreparedStatement 对象可多次设置不同参数并执行，无需每次都重新构造 SQL 语句

构造的 sql 语句：需要输入的字段用 ? 代替，序号从 1 开始

常用 API

- void setXXX(int parameterIndex, XXX x)：绑定类型
- void clearParameters()：清除之前所有已设置的参数
- ResultSet executeQuery()：执行 SELECT，返回查询结果 
- int executeUpdate()：执行 INSERT/UPDATE/DELETE/CREATE/DROP，返回受影响行数 
- boolean execute()：通用执行
    - 返回 true 则可调用 getResultSet() 取结果
    - 返回 false 则可调用 getUpdateCount() 取更新计数
- void addBatch()：将当前已绑定参数的 SQL 加入批处理
- int[] executeBatch()：批量执行所有已添加的批处理，返回每条执行结果
- void clearBatch()：清空批处理列表
- void close() / boolean isClosed()：关闭此 PreparedStatement 或检查是否已关闭

### 事务

事务要么全部成功提交，要么全部失败回滚，以下 API 都属于 Connection

- void setAutoCommit(boolean autoCommit)：开启或关闭自动提交模式
- boolean getAutoCommit()：查看当前自动提交模式
- void commit()：提交当前事务 
- void rollback()：回滚当前事务自上次提交
- Savepoint setSavepoint()：设置事务保存点
- void rollback(Savepoint savepoint)：回滚到指定保存点
- void releaseSavepoint(Savepoint savepoint)：释放保存点
- int getTransactionIsolation()：获取事务隔离级别
- void setTransactionIsolation(int level)：设置事务隔离级别
    - TRANSACTION_READ_UNCOMMITTED：允许脏读、允许不可重复读、允许幻读
    - TRANSACTION_READ_COMMITTED：禁止脏读、允许不可重复读、允许幻读
    - TRANSACTION_REPEATABLE_READ：禁止脏读、禁止不可重复读、允许幻读
    - TRANSACTION_SERIALIZABLE：禁止脏读、禁止不可重复读、禁止幻读

```java
try {
    connection.setAutoCommit(false);
    // 数据库处理...
    connection.commit();
} catch (Exception e) {
    connection.rollback();    
}
...
```

### 批处理

批处理是将多条 SQL 语句合并到一次网络往返中执行的机制，能够显著减少客户端与数据库服务器之间的交互次数，从而提高大量插入／更新／删除操作的性能

以下 API 都属于 Statement/PreparedStatement

- void addBatch(String sql)：将指定的 SQL 加入批处理
- void addBatch()：将预编译的 SQL 加入批处理
- int[] executeBatch()：批量执行已加入的 SQL，返回每条语句的更新计数数组
- void clearBatch()：清空当前批处理中的所有 SQL

```java
for (int i = 1; i <= 5000; i++) {
    ps.setString(...);
    ps.addBatch();
    if (i % 1000 == 0) {
        ps.executeBatch();
        ps.clearBatch();
    }
}
```

### 连接池

什么是连接池：预先创建多个数据库连接并缓存起来的组件，当应用需要数据库连接时，从池里“借用”一个而不是重新建立，使用完毕后再归还给池而不是关闭

- 建立一个 JDBC 连接通常需要数十到数百毫秒，批量请求时如果每次都新建连接，开销巨大
- 池可以限制最大连接数，防止因过多并发连接而耗尽数据库资源
- 应用代码不用关心连接的创建、销毁和异常回收，只需借用/归还即可

常用方法

- 初始化
    - void setInitialPoolSize(int size)：在连接池启动时预先创建并缓存的连接数
    - void setMinPoolSize(int size)：连接池中始终保持的最小空闲连接数
    - void setMaxPoolSize(int size)：连接池允许分配的最大连接数，超过此数量时，借用连接会阻塞或超时
    - void setMaxIdleTime(int seconds)：空闲连接在池中保留的最长时间（秒），超过时会被回收并关闭
    - void setCheckoutTimeout(int ms)：从池中借用连接时的最大等待时长（毫秒），超出会抛出超时异常
- 状态监控
    - int getNumBusyConnectionsDefaultUser()：当前已借出的活动连接数
    - int getNumIdleConnectionsDefaultUser()：当前未借出的连接数
    - int getNumConnectionsDefaultUser()：当前池中总连接数
- 连接监测
    - boolean isValid(int timeout)：检测一个物理连接在指定超时时间内是否还能正常工作
    - void setValidationQuery(String sql)：指定一个简单的 SQL 用来检测连接有效性
    - void setTestConnectionOnCheckout(boolean flag)：在借出连接前执行验证查询，保证返回给应用的连接都是可用的
    - void setTestConnectionOnCheckin(boolean flag)：在归还连接时执行验证查询，确保池中的连接长期健康
    - void setIdleConnectionTestPeriod(int seconds)：设定一个周期（秒），让连接池在后台定时对所有空闲连接执行验证查询
- 销毁资源
    - void close()：释放所有空闲与活动连接，并清理内部资源

> 惰性初始化：系统不知道你是否真的要使用资源，因此池子并不会在 ComboPooledDataSource 构造时就马上建好 3 个连接，而是在第一次真正向它请求连接的时候，才一次性按初始化的数量创建那么多连接

### DBUtils

QueryRunner 是 Apache Commons DBUtils 中的核心类，用来简化 JDBC 操作

- 自动获取并关闭 Connection、PreparedStatement 和 ResultSet，避免大量手写 try-catch
- 更方便地设置 SQL 参数，并且直接返回 Java 对象
- 支持将同一条带参数的 SQL 与多组参数打包，批量执行

ResultSetHandler<T> 是用来将 ResultSet 转换成任意 Java 对象的核心接口

- BeanHandler<T>：把 ResultSet 的第一行映射为一个 JavaBean
- BeanListHandler<T>：把整个结果集的每一行都映射成一个 Bean，返回 Bean 组成的 List<T>
- MapHandler：取结果集的第一行，返回 Map<String,Object>，Key = 列标签，Value = 列值
- MapListHandler：把所有行都做 MapHandler，返回 List<Map<String,Object>>
- ScalarHandler<T>：返回第一行的第一列值。常用于 COUNT(*)、聚合或获取单个标量值
- ColumnListHandler<T>：返回某一列的所有值为一个 List<T>

Bean：用来承载一行查询结果的类，通常与表对应，要求

- 必须有一个 public 的无参构造函数
- 属性名与列名必须一一对应
- 所有要映射的字段都必须声明为 private
- 对应每个属性有标准的 public setter/getter
- 如果 Bean 中有额外的属性，而 SQL 并不返回对应列，DBUtils 会自动跳过，不会报错
- 映射时大小写不敏感，ID、id、Id 都能对应 setId()

常用方法：

- QueryRunner(DataSource)：自动绑定连接池中的一个连接
- int update(String sql, Object... params)：执行一条带占位符的 DML/DDL，params 按顺序填充占位符，返回受影响行数
- int[] batch(String sql, Object[][] params)：批量执行同一条带参 SQL，同时传递一个二维数组提供多组参数
- <T> T query(String sql, ResultSetHandler<T> rsh, Object... params)：执行 SELECT 查询，并将结果交给 ResultSetHandler 去处理
- void fillStatement(PreparedStatement ps, Object... params)：将可变参数 params 按顺序绑定到给定的 PreparedStatement 上，然后就可以手动调用 ps 执行，实际上用于重写来实现额外功能