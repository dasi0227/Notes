# JVM



## 概念

### JDK（Java Development Kit）

是用于开发 Java 程序的完整套件，包含 JRE 和开发工具

- javac：将字符源码编译为字节码，也就是将 .java 文件编译为 .class 文件
- javadoc：从源码的 `/**...*/` 注释自动生成 API 文档
- jar：将 Java 程序打包为一个 .jar 文件，以及从 .jar 文件解包为 Java 程序
- jdb：命令行调试器，连接 JVM，支持断点、单步、打印变量、线程控制等操作

### JRE（Java Runtime Environment）

是用于运行 Java 程序的运行环境，包含 JVM 和标准类库

- java.base：包含 lang、util、io、nio 等，是 Java 程序的核心依赖类
- java.sql：提供数据库连接和 SQL 操作的标准接口

### JVM（Java Virtual Machine） 

是用于运行 Java 字节码（.class 文件）的虚拟机，通过封装底层硬件平台的差异，使得 Java 程序可以在不同平台运行

- 解释器（interpreter）：运行时逐条读取字节码并按语义直接在宿主上执行，不会为字节码生成本地机器码
- JIT（Just-In-Time）：在运行时把热点字节码编译为机器码并缓存

### 关系

<img src="https://dasi-blog.oss-cn-guangzhou.aliyuncs.com/Java/202509162330784.png" alt="image-20250916233051698" style="zoom: 50%;" />

### HotSpot

JVM 本质上只是一种思想和规范，具有很多实现如 HotSpot、JRockit、Zulu、ART 等，其中 HotSpot 是目前最广泛使用的实现，同时也是 OpenJDK 的默认实现



##内存

### 进程内存布局

JVM 内存：由 JVM 管理的内存，是预先设置好初始值和最大值的内存，主要有堆和栈

本地内存：由进程管理的内存，是从操作系统动态分配的内存，主要有元空间和直接内存

<img src="https://dasi-blog.oss-cn-guangzhou.aliyuncs.com/Java/202509162331896.png" alt="image-20250916233140809" style="zoom: 50%;" />



### 栈 Stack

#### 内存布局

这里的栈指的是一个线程所占据的内存空间，线程是 JVM 中执行代码的最小单位，每个线程都有自己的执行上下文和内存空间，同时也与其他线程共享堆和本地内存

<img src="https://dasi-blog.oss-cn-guangzhou.aliyuncs.com/Java/202509162332105.png" alt="image-20250916233237006" style="zoom:50%;" />

#### 虚拟机栈 / 本地方法栈

**虚拟机栈**：简称栈，是每个 Java 线程私有的内存区域，生命周期和线程一致，负责存放方法执行的栈帧，用于方法调用、局部变量保存、操作数计算和控制流管理

**栈帧**：每次方法调用时都会创建一个栈帧压入该线程的栈，方法返回时弹出并销毁该栈帧，每个栈帧包含局部变量表、操作数栈、动态链接、方法返回地址

- **局部变量表**：存放了编译期可知的方法参数、局部基本类型变量和对象引用，用于按索引快速访问方法数据，并作为字节码指令的读写目标
- **操作数栈**：存放方法执行过程中产生的临时数据与中间结果，用于字节码通过 LIFO 完成运算操作数的传递和返回值处理
- **动态链接**：存放指向当前方法所属类的运行时常量池的指针，用于在运行时找到符号引用并解析为直接引用，从而快速定位调用目标
- **方法返回地址**：存放当前方法的调用方在字节码中的返回位置，用于在当前方法执行完后能够返回调用点继续执行

本地方法栈和虚拟机栈发挥的结构和作用类似，只不过虚拟机栈是为虚拟机执行 Java 方法，而本地方法栈是为虚拟机执行 Native 方法

<img src="https://dasi-blog.oss-cn-guangzhou.aliyuncs.com/Java/202509162340065.png" alt="image-20250916234039981" style="zoom:50%;" />

#### 程序计数器

程序计数器（Program Counter Register）记录了线程当前执行字节码的地址，也可以记录下一行字节码的地址

- 每个线程都有自己的程序计数器
- 解释器根据程序计数器来读取并执行下一步操作
- 解释器也可以调整程序计数器来实现控制代码流程
- 当线程切换时，程序计数器保留了线程执行位置，以便切换回来后恢复执行

#### StackOverflowError

如果出现了无限递归，也就是一个方法会被无限次调用，这时候栈帧的深度会超过虚拟机栈允许的最大深度，则抛出 StackOverflowError 栈溢出错误

### 堆 Heap

#### 内存布局

这里的堆内存跟算法中的堆结构概念不一致，这里叫堆就是因为内存像一堆物品一样，需要的时候就拿走，不需要的时候就放回

在 JVM 中，**堆存放所有对象实例和数组，被所有线程共享**，线程通过对象引用来访问堆上的实例数据，同时堆也是垃圾回收器的主要作用对象

<img src="https://dasi-blog.oss-cn-guangzhou.aliyuncs.com/Java/202509171145360.png" alt="image-20250917114525262" style="zoom:50%;" />

#### 新生代

新生代存放刚刚创建的对象，其中又被细分为三部分

- Eden：“伊甸园”是亚当和夏娃创造人类的地方，即 **JVM 创建对象的地方**，大部分对象第一次都会被分配到这里
- Survivor：当 Eden 空间即将用尽的时候，JVM 会执行一次 Minor GC 清理 Eden 和 Survivor-From，没有被垃圾回收的“幸存者”将会被复制到 Survivor-To，然后 JVM 会**把 To 与 From 互换角色，从而保证每一次都有一个空的 Survivor-To 来接收幸存者**，因此S0/S1实际上没有任何区别，只不过在逻辑上交替作为 From 和 To

#### 老年代

新老的差别就在于年龄，而 JVM 的 GC 会为每个对象维护一个年龄信息叫做 **GC 分代年龄，本质上是对象在 Survivor 中的存活次数，每次对象在一次 Minor GC 中从 Eden 或 From 复制到 To，其年龄 +1**

- JVM 会保存一个 **MaxTenuringThreshold**，如果对象的年龄超过这个阈值，那么就会从新生代晋升到老年代，而这个阈值会随着 Survivor 的空间占用和晋升速率来动态调整
- 当老年代空间不足时，会触发 Full GC，清理不再需要的对象，代价会远高于 Minor GC
- 年龄信息只有 4 位，也就是年龄值只能在 0-15

#### OutOfMemoryError

OutOfMemoryError 是 JVM 在内存耗尽时抛出的 Error，表示无法为所需内存或资源完成分配

- JVM 花费太多时间执行 GC 但是只能回收很少的堆空间
- 一次性申请一个很大的对象，堆找不到足够的连续内存来分配
- 最大堆内存 -Xmx 配置过小，无法满足峰值负载
- 短时间内创建大量临时对象，GC 来不及回收
- Survivor 空间不足或晋升阈值设置不当，导致大量对象提前晋升占满老年代

### 元空间 Metaspace

#### 内存布局

Metaspace 是存放类元数据的堆外内存区域

- 类元信息（介绍书）：类名、父类、接口、访问标志、字段表、方法表、方法分派表等
- 方法元信息（说明书）：字节码属性、注解、异常声明、调试信息等
- 运行时常量池（符号表）：编译期常量、符号引用、解析缓存等

<img src="https://dasi-blog.oss-cn-guangzhou.aliyuncs.com/Java/202509171640862.png" alt="image-20250917164051759" style="zoom:50%;" />

#### 永久代和元空间

JDK 1.7 利用了堆的永久代来存储类的元数据，而 JDK 1.8 转移到了元空间之中，原因在于：

- 永久代需要通过 -XX:PermSize 和 -XX:MaxPermSize 指定大小，无法动态进行扩容，不灵活
- 元数据如果放在堆中，在动态生成大量类时，很容易产生 OOM 异常
- 永久代仍然受 GC 管理，会给整体带来不必要的复杂度，回收效率很低
- 为了统一 HotSpot VM 与 JRockit VM 所做的一种妥协

### 直接内存

这部分内存是 Java 程序**直接向操作系统申请的本地内存**，并不是虚拟机运行时数据区的一部分，也不是虚拟机规范中定义的内存区域

- **NIO（Non-Blocking I/O）**：通过 ByteBuffer.allocateDirect() 分配的堆外内存，通过 DirectByteBuffer 对象引用和操作堆外内存，常用于高性能 I/O，减少一次堆到缓冲区的复制
- **JNI（Java Native Interface）**：本地方法可以直接通过 JNI 调用 C/C++ 代码申请和使用堆外内存

### 对象内存

#### 内存布局

在 HotSpot 虚拟机中，一个对象在堆由三部分组成

- **对象头（Header）**：存储对象的元信息
    - **标记字段（Mark Word）**：存储对象运行时数据，如哈希码、GC 分代年龄、锁状态标识、锁指针等，会随着程序进行而动态改变
    - **类型指针（Class Pointer）**：指向在元空间中当前对象对应的类元信息，使得虚拟机可以确定对象的类
- **实例数据（Instance Data）**：存储对象的有效信息，即在程序中所定义的各种类型的字段内容
- **对齐填充（Padding）**：HotSpot 要求对象大小必须是 8 字节的整数倍，因此可能需要一部分空闲区域来对齐

<img src="https://dasi-blog.oss-cn-guangzhou.aliyuncs.com/Java/202509171802873.png" alt="image-20250917180240778" style="zoom:50%;" />

#### 对象的方法调用

1. 利用栈帧中保存的对象引用（直接指针），定位到堆中的对象实例
2. 从对象实例的对象头中取出类指针，定位到元空间中的类元信息
3. 在类元信息中找到方法表，根据方法索引定位到方法入口
4. 方法指向方法元信息中的字节码，由解释器逐条执行

<img src="https://dasi-blog.oss-cn-guangzhou.aliyuncs.com/Java/202509171901713.png" style="zoom: 50%;" />

### 对象创建全过程

#### 1️⃣ 类加载检查

虚拟机遇到一条 new 指令时，JVM 首先检查运行时常量池中是否有该类的符号引用，如果没有，则会通过类加载器将 .class 文件加载到元空间中，并创建对应的 Class 对象放在堆中

#### 2️⃣ 内存分配

虚拟机会在堆上为对象分配内存，所需的内存大小在类加载完成便可以确定

- **指针碰撞（适用于堆内存规整）**：用过的内存全部整合到一边，没有用过的内存放在另一边，边界用一个分界指针存储，虚拟机只需要将分界指针向着没用过的内存方向移动对象大小即可
- **空闲列表（适用于堆有碎片）**：虚拟机会维护一个列表，其中记录了内存块的起始位置和可用大小，只需要找一块足够大的内存块分配给对象即可

> 取决于 GC 的实现方式，本质上取决于 GC 算法是“清除”还是“整理”

内存分配存在一个问题，即多个线程都在请求创建对象，此时需要确保并发安全

- **CAS（Compare And Swap）**：一种乐观锁的实现方式，在分配内存前会比较分界指针是否等于预期值，如果不相等则会重新尝试分配内存，直到成功为止
- **TLAB（Thread Local Allocation Buffer）**：虚拟机先为每个线程在堆中分配一小块私有的 Eden 区，又称为 TLAB，线程优先在各自的 TLAB 中分配内存给对象，如果 TLAB 不足，再退回到公共 Eden 区使用 CAS

#### 3️⃣ 内存初始化零值

分配完内存之后，虚拟机会先将内存空间清零（int=0，引用=null），然后在对象头写入对象的元数据，这样子对象即使不赋初值，也可以程序访问到零值

#### 4️⃣ 执行 init 方法

虚拟机会调用 \<init> 方法即类的构造方法，对类进行程序层面的初始化，逻辑由开发者指定



## 垃圾回收

### Java 的内存管理特性

在 C 和 C++ 中，内存管理是手动的，其中 **C 需要 malloc 和 free，而 C++ 需要 new 和 delete**，存在以下隐患：

- **内存泄露**：未显式释放内存，导致内存长期占用
- **重复释放**：同一块内存多次释放，运行时抛出错误
- **悬空指针**：访问已释放的内存
- **野指针**：访问没有初始化的指针，指针会指向随机内存

在 Java 中，内存管理是自动的**，JVM 会在 new 一个对象的时候自动分配内存，GC 会在对象不再被引用时自动回收内存**

### GC 定义

垃圾回收（GC, Garbage Collection）是 JVM 的核心功能，用于自动管理堆内存，主要负责**对象存活判定、对象内存清理和堆内存整理**，分为了**新生代回收（Minor GC / Young GC）、老年代回收（Major GC / Old GC）和整堆回收（Full GC）**

此前讲过 Minor GC 会清理新生代，每次清理后部分对象可能会晋升到老年代，而如果 Survivor-To 的内存不够，多余出来的对象可能也会被迫晋升到老年代。因此**为了保证老年代有足够的空间可以接受晋升的对象，在执行 Minor GC 之前，会检查老年代的连续空间是否大于新生代对象总大小或者历次晋升的平均大小，如果足够则进行 Minor GC，否则转而进行 Full GC**

###存活判定

#### 引用计数法

给每个对象维护一个引用计数器，每当有一个地方引用它，计数器 +1，每当引用失效时，计数器 -1，当计数器为 0 时，对象不会再被访问，可以被回收

但是如果存在循环引用，那么其中任何一个对象的引用计数器就不可能为 0，即使他们都不会再被使用

#### 可达性分析法

从一组称为 GC Roots 的对象出发，沿着引用向下搜索，如果对象在引用链上可达，那么就认为对象可活，但如果对象不可达，GC 会检查这个对象有没有重写 finalize() 方法

- 没有重写：立马回收
- 重写了但是已经执行过：立马回收
- 重写了并且没有执行过：暂时保留，放入 Finalizer 队列，会**由专门的 Finalizer 线程异步调用这些对象的 finalize() 方法**，如果在该方法中重新建立了与 GC Roots 的引用链实现“自救”，那么就不会回收，否则立马回收

为了解决循环引用问题，GC Roots 必须选择的是绝对存活的对象，这些对象可以确保一定不会被回收，否则程序将会被破坏

- **虚拟机栈或本地方法栈的局部变量表中引用的对象**：在方法执行期间，这些对象必须存活，否则方法里的指令无法正确执行
- **元空间中类的静态属性引用的对象**：静态变量属于类层级，只要类还没卸载，静态属性引用的对象就必须存活，否则类本身无法正常使用
- **元空间中常量引用的对象**：常量池中的常量在运行过程中可能随时被使用，因此必须保留，不能回收
- **正在运行的线程对象**：GC 不会打断线程的运行
- **锁对象和被同步锁持有的对象**：GC 不能破坏同步机制和并发控制

#### 无用的类

除了堆中的对象会被回收，元空间中的类也会被回收/卸载，只要类同时满足下述三个条件，就会被视为无用的类，只不过无用的类也是可回收而不是会回收，具体要看 GC 策略

- 该类的所有实例都已经被回收，否则说明类仍然有对象在使用
- 加载该类的 ClassLoader 对象也已经被回收，否则说明类的定义仍然被持有
- 该类对应的 Class 对象没有被引用，否则说明类的元信息仍然在被使用

### 引用类型

| 类型   | 回收时机                     | 类型             | 典型用途                          |
| ------ | ---------------------------- | ---------------- | --------------------------------- |
| 强引用 | GC 永远不会回收              | new Object()     | 普通对象，业务逻辑中使用          |
| 软引用 | 只有在内存不足时 GC 才会回收 | SoftReference    | 缓存                              |
| 弱引用 | 只要执行 GC 就会回收         | WeakReference    | ThreadLocal 和 WeakHashMap 的 key |
| 虚引用 | 只要执行 GC 就会回收         | PhantomReference | 跟踪对象回收、释放堆外内存        |

需要注意的是，虽然虚引用和弱引用的回收时机是一样的，但是虚引用的含义是跟没有引用一样，因为无法通过虚引用来获取实例对象，而且它必须关联一个 ReferenceQueue 对象，**当 GC 回收对象时发现有虚引用，会把该引用对象本身放入 ReferenceQueue 中**，程序员可以利用这个机制进行一些额外处理，不过**无法阻止和延迟回收**

### 垃圾收集算法

#### 标记清除

利用可达性分析法标记所有可达对象，完成后统一回收掉所有没有被标记的对象

- 标记和清除的效率都很低下
- 直接清除会留下大量不连续的内存碎片

![image-20250918103409087](https://dasi-blog.oss-cn-guangzhou.aliyuncs.com/Java/202509181034154.png)

#### 标记压缩

利用可达性分析法标记所有可达对象，完成后把所有标记对象压缩到一边，然后一次性清理掉边界之外的内存

- 不会存在内存碎片
- 移动对象的开销很大

![image-20250918103438138](https://dasi-blog.oss-cn-guangzhou.aliyuncs.com/Java/202509181034211.png)

#### 标记复制

将内存划分为两个大小相等的区域，每次只用一块，利用可达性分析法标记所有可达对象，完成后只把存活的对象按顺序复制到另一块，并清理当前区域

- 不会存在内存碎片
- 内存需要之前的两倍
- 如果存活对象数量很大，复制效率会很低

![image-20250918103451393](https://dasi-blog.oss-cn-guangzhou.aliyuncs.com/Java/202509181034453.png)

#### 分代收集

根据对象生命周期的不同，把堆分为新生代和老年代

- 新生代的对象存活率低，采用标记复制
- 老年代的对象存活率高，采用标记清除或标记压缩

### 垃圾收集器

#### Serial

利用单线程执行 GC，而**执行 GC 的时候会暂停所有其他用户线程，称为 Stop-The-World，这是为了确保回收速度能够跟上垃圾产生速度**，开销最小但停顿时间最长，适合 Client 模式

#### ParNew

是 Serial 的多线程版本，利用**并行机制**可以快速执行垃圾收集算法，从而缩短停顿时间，适合 Server 模式

#### Parallel Scavenge

Parallel Scavenge 又叫**吞吐量优先收集器**，虽然实现机制和 ParNew 一样，但是它更关注提高整体的吞吐量，可以**自适应调节策略**，适合后台计算任务

#### CMS

CMS（Concurrent Mark-Sweep）是第一个**面向服务端并以获取最短回收停顿时间为目标**的垃圾收集器，分为以下几个步骤：

1. 初始标记：只开启 GC 线程，对用户线程 STW，标记直接与 GC Roots 相关联的对象
2. 并发标记：同时开启 GC 线程和用户线程，标记从 GC Roots 出发的可达对象
3. 重新标记：只开启 GC 线程，对用户线程 STW，修正并发标记阶段因为用户线程继续运行而产生的遗漏标记
4. 并发清除：同时开启 GC 线程和用户线程，清理不可达对象

CMS 最大的特点在于**部分阶段允许用户线程和 GC 线程同时并发执行**，从而显著降低停顿时间，极大提升用户体验，但是这样做也存在以下问题

- CPU 资源敏感：并发标记和并发清理阶段 GC 线程都会和用户线程竞争资源
- 无法处理浮动垃圾：并发清理时用户线程产生的新垃圾无法在当前 GC 处理，只能等下次 GC
- 内存碎片：采用标记清除算法的固有弊端

#### G1

G1（Garbage First）的目标是**兼顾吞吐量和延迟**，分为以下几个步骤：

1. 将堆划分为多个大小相等的 Region，每个 Region 动态扮演 Eden、Survivor、Old、Humongous
2. 如果 Eden 区满了，会触发 Young GC，执行标记复制算法，快速清理短命对象，保证新对象能分配内存
3. 如果堆使用率达到阈值，会触发并发标记（类似 CMS），但是不会执行回收，而是统计各 Region 的存活率和回收价值，形成回收候选集
4. 并发标记完成后会执行 Mixed GC，回收整个新生代，但是只回收价值高的老年代 Region，并且采用的是标记压缩算法
5. 如果 Mixed GC 无法腾出足够空间，才会执行 Full GC，回收整个堆和元空间

G1 最大的特点在于**既能处理大堆，又能提供可预测的停顿时间**

- 处理大堆：通过 Region 分区管理和筛选回收，避免了全堆扫描
- 可预测的停顿时间：支持用户设置期望停顿时间，G1 会根据每个 Region 的大小、存活对象量等信息预测回收成本，从而在停顿预算内动态选择要回收的 Region 数量

#### ZGC

Z 的含义表示 Z 世代，即新一代垃圾回收器，最大的特点是**拓展了并发支持**

- **Region 化**：ZGC 的 Region 大小是动态可变的，支持超大堆
- **着色指针**：利用引用地址的高位比特来存储标记信息，不再需要额外的数据结构，极大程度加快了标记效率和访问对象速度
- **负载屏障**：ZGC 执行复制和压缩也是并发的，因为在用户线程进行对象访问时，ZGC 会自动插入检查逻辑，确保拿到的是正确地址



## 类加载

### 类文件

#### 结构

类文件就是 .class 文件，是 Java 源代码通过 javac 编译后的产物，也是 JVM 直接识别并执行的二进制格式文件，并且严格遵守字节码结构规范

```java
ClassFile {
    u4             magic;
    u2             minor_version;
    u2             major_version;
    u2             constant_pool_count;
    cp_info        constant_pool[constant_pool_count-1];
    u2             access_flags;
    u2             this_class;
    u2             super_class;
    u2             interfaces_count;
    u2             interfaces[interfaces_count];
    u2             fields_count;
    field_info     fields[fields_count];
    u2             methods_count;
    method_info    methods[methods_count];
    u2             attributes_count;
    attribute_info attributes[attributes_count];
}
```

![e72fb8df7a7cc8ae16e81bb39ea0faaa](https://dasi-blog.oss-cn-guangzhou.aliyuncs.com/Java/202509181059298.png)

#### 魔数

`magic` 位于文件开头的 4 个字节，是固定值 0xCAFEBABE，用来标识这是一个合法的 Java 类文件，如果不是这个值 JVM 会拒绝加载

#### 版本号

前 2 个字节存**次版本号 `minor_version`，记录了不同小更新或小补丁的版本**；后 2 个字节存**主版本号 `major_version`，记录了类文件由哪一代 JDK 编译器生成**，低版本的 JVM 无法运行高版本的 JDK 编译器生成的类文件

#### 常量池

`constant_pool_count`：占用 2 字节，表示类中常量的数量

- **字面量**：文本字符串以及声明为 final 的常量值
- **符号引用**：类和接口的全限定名、字段的名称和描述符、方法的名称和描述符

`cp_info constant_pool[]`：常量池实际上是一个表结构，最多可以存 constant_pool_count - 1 个常量池项，占用 2 字节，其中**有效常量值的索引值从 1 开始，索引 0 专门表示“没有引用任何常量”**，每一个常量池项都是 `cp_info` 元素，由 **tag + info** 组成

| tag               | info                   |
| ----------------- | ---------------------- |
| 1（Utf8）         | UTF-8 编码的字符串     |
| 3（Integer）      | int 字面量             |
| 4（Float）        | float 字面量           |
| 5（Long）         | long 字面量            |
| 6（Double）       | double 字面量          |
| 7（Class）        | 类或接口的符号引用     |
| 8（String）       | 字符串类型字面量       |
| 9（FieldRef）     | 字段的符号引用         |
| 10（MethodRef）   | 方法的符号引用         |
| 12（NameAndType） | 字段或方法的名字和类型 |

```text
// String name = "dasi";
#1  = String             #2
#2  = Utf8               dasi

// Integer age = 21;
#3  = Integer            21
#4  = Methodref          #5.#6
#5  = Class              #7
#6  = NameAndType        #8:#9
#7  = Utf8               java/lang/Integer
#8  = Utf8               valueOf
#9  = Utf8               (I)Ljava/lang/Integer;

// User user = new User(name, age);
#10 = Class              #11
#11 = Utf8               User
#12 = Methodref          #10.#13
#13 = NameAndType        #14:#15
#14 = Utf8               <init>
#15 = Utf8               (Ljava/lang/String;Ljava/lang/Integer;)V
```

#### 类头信息

类头信息指的就是大括号外的信息

- `access_flags`：占用 2 字节，每一位表示一个布尔属性，用来描述类的修饰符标志信息
- `this_class`：占用 2 字节，是常量池的索引，指向常量池中的 Class 项，再通过 info 指向 Utf8 项，得到当前类的全限定名
- `super_class`：占用 2 字节，指向常量池中的  Class 项，再通过 info 指向 Utf8 项，得到父类的全限定名
- `interfaces_count`：占用 2 字节，存储类实现的接口数量
- `interfaces`：是一张表，**每个元素都是常量池索引**，占用 2 字节，指向常量池中的 Class 项，再通过 info 指向 Utf8 项，得到接口的全限定名

#### 类体信息

类体信息就是大括号里面的信息

- `fields_count` / `methods_count`：占用 2 字节，表示类中字段/方法的数量，包括实例字段/方法和静态/方法

- `field_info fields[]` / `method_info methods[]`：是一个数组，每个元素是一个 field_info / method_info 结构，用来描述一个具体的字段/方法

    - **access_flags**：占用 2 字节，修饰符，如 public、private、protected、static、transient、final、volatile 等

    - **name_index**：占用 2 字节，常量池的索引，指向 Utf8，表示字段/方法名

    - **descriptor_index**：占用 2 字节，常量池索引，指向 Utf8，表示字段/方法的类型

    - **attributes_count**：占用 2 字节，是字段/方法属性的数量

    - **attribute_info attributes[]**：记录了字段/方法的额外信息，如 SourceFile、Deprecated、Synthetic 等

- `Code`：方法的属性除了和字段一样的通用属性，最大不同在于其 **Code 属性存储了方法体的字节码指令**

#### 属性信息

除了字段和方法有属性信息外，类本身也可以有属性信息，直接用 `attributes_count` 和 `attribute_info attributes[]` 记录

- `attribute_name_index`：常量池索引，指向 Utf8，表示属性名
- `attribute_length`：属性数据的字节长度
- `info[]`：具体的数据内容，不同属性的内容不同

#### 访问标志对照表

| **标志名**           | **十六进制值** | 类 (Class) | **字段 (Field)** | **方法 (Method)** | **含义**                                           |
| -------------------- | -------------- | ---------- | ---------------- | ----------------- | -------------------------------------------------- |
| **ACC_PUBLIC**       | 0x0001         | ✅          | ✅                | ✅                 | public 可见性                                      |
| **ACC_PRIVATE**      | 0x0002         | ❌          | ✅                | ✅                 | private 可见性                                     |
| **ACC_PROTECTED**    | 0x0004         | ❌          | ✅                | ✅                 | protected 可见性                                   |
| **ACC_STATIC**       | 0x0008         | ❌          | ✅                | ✅                 | static 修饰符                                      |
| **ACC_FINAL**        | 0x0010         | ✅          | ✅                | ✅                 | final 修饰符（类不可继承/字段不可变/方法不可覆盖） |
| **ACC_SUPER**        | 0x0020         | ✅          | ❌                | ❌                 | 使用新的 invokespecial 语义（历史遗留）            |
| **ACC_SYNCHRONIZED** | 0x0020         | ❌          | ❌                | ✅                 | 方法同步（monitorenter/monitorexit）               |
| **ACC_VOLATILE**     | 0x0040         | ❌          | ✅                | ❌                 | 字段的 volatile 语义                               |
| **ACC_BRIDGE**       | 0x0040         | ❌          | ❌                | ✅                 | 编译器生成的桥接方法（泛型擦除时使用）             |
| **ACC_TRANSIENT**    | 0x0080         | ❌          | ✅                | ❌                 | 字段的 transient 修饰符（序列化时忽略）            |
| **ACC_VARARGS**      | 0x0080         | ❌          | ❌                | ✅                 | 方法是可变参数（varargs）                          |
| **ACC_NATIVE**       | 0x0100         | ❌          | ❌                | ✅                 | 方法是 native 方法（JNI）                          |
| **ACC_INTERFACE**    | 0x0200         | ✅          | ❌                | ❌                 | 声明这是一个接口                                   |
| **ACC_ABSTRACT**     | 0x0400         | ✅          | ❌                | ✅                 | 抽象类 / 抽象方法                                  |
| **ACC_STRICT**       | 0x0800         | ❌          | ❌                | ✅                 | strictfp 修饰符（严格浮点语义）                    |
| **ACC_SYNTHETIC**    | 0x1000         | ✅          | ✅                | ✅                 | 编译器自动生成，不出现在源码中                     |
| **ACC_ANNOTATION**   | 0x2000         | ✅          | ❌                | ❌                 | 声明这是一个注解类型                               |
| **ACC_ENUM**         | 0x4000         | ✅          | ✅                | ❌                 | 声明这是一个枚举类型/枚举字段                      |
| **ACC_MODULE**       | 0x8000         | ✅          | ❌                | ❌                 | 声明这是一个模块（module-info）                    |

### 类加载过程

#### 1️⃣ 加载

1. 通过全类名找到 .class 文件（可能来自磁盘、网络或 jar 包），把字节码加载到内存
2. 在元空间中生成该类的类元信息
3. 在堆中生成一个该类的 Class 对象

####2️⃣ 链接

1. **验证**：确保字节码格式正确，符合 JVM 规范，避免按群问题，包括**文件格式、元数据、字节码、符号引用**
2. 准备：正式为类变量/静态变量在元空间分配内存，并赋予零值/默认值，除非用了 final 关键字修饰，才会直接赋予字面量
3. 解析：将常量池内的符号引用替换为直接引用，如类名 → 类元信息指针，字段名 → 内存偏移量，方法名 → 方法表入口地址

#### 3️⃣ 初始化

执行编译生成的 \<clinit> 方法，把静态变量赋值为源码里的初始值，并执行类中的静态代码块，但是初始化只有在以下情况才会触发

- 创建类实例
- 访问或修改类的静态字段（除 final）
- 调用类的静态方法
- 通过反射调用类
- 初始化子类时，会初始化父类
- JVM 启动时加载的主类
- 调用接口的 default 方法

### 类加载器

#### 定义

类加载器是 JVM 中负责把类文件加载到内存的组件，负责完成整个加载流程

- 在元空间中，每一个类的元信息都会记录它是由哪个类加载器加载的
- 在堆中，每一个类的 Class 对象都有一个自己对应的 ClassLoader 的引用
- 每一个类都必须通过某个类加载器加载
- 一个类加载器对同一个类只会加载一次，不会重复加载
- 相同的类文件可以被不同的类加载器加载，但是 JVM 会认为它们是不同的类
- 类是按需加载的，只有在第一次使用时才会触发加载

#### 内置

- **BootstrapClassLoader**：由 C++ 编写，是最顶层的类加载器，负责加载 %JAVA_HOME%/lib 下的所有 jar 包和类，以及被 `-Xbootclasspath `参数指定路径下的所有类
- **ExtensionClassLoader / PlatformClassLoader**：由 Java 编写，负责加载 %JAVA_HOME%/lib/ext 下的所有 jar 包和类，用于扩展 JDK 的功能
- **Application ClassLoader**：由 Java 编写，是直接面向用户的类加载器，负责加载当前应用的类路径下的所有 jar 包和类

> 无法在 Java 程序获取到 BootstrapClassLoader 对象，因为它是由 C++ 在底层实现的，在 Java 中没有对应的类

#### 双亲委派模型

##### 定义

双亲委派模型是 JVM 类加载机制的核心设计，不过需要注意的是，这里的双亲是 parent 的直译，同时并不是 Java 继承关系里的 extends 父类，而是 ClassLoader 抽象类中定义的父加载器引用

```java
public abstract class ClassLoader {
  private final ClassLoader parent;
  protected ClassLoader(ClassLoader parent) {
       this(checkCreateClassLoader(), parent);
  }
  private ClassLoader(Void unused, ClassLoader parent) {
    this.parent = parent;
}
  ...
}
```

##### loadClass

双亲委派模型的思想是，当一个类加载器接到类加载请求时，它不会自己先尝试加载，而是**把加载任务交给父加载器，如果父加载器做不到，才会亲自下场加载**，逻辑集中在 loadClass 方法

```java
protected Class<?> loadClass(String name, boolean resolve)
    throws ClassNotFoundException
{
  	// 利用同步锁，保证多线程安全：同一个类名只会被加载一次
    synchronized (getClassLoadingLock(name)) {
        // 1. 检查是否已经加载过该类
        Class c = findLoadedClass(name);
        if (c == null) {
            long t0 = System.nanoTime();
            try {
              	// 2. 检查是否有父加载器
                if (parent != null) {
                  	// 2.1 有的话则调用父加载器的 loadClass 方法
                    c = parent.loadClass(name, false);
                } else {
                  	// 2.2 没有的话则直接交给 Bootstrap ClassLoader 加载
                    c = findBootstrapClassOrNull(name);
                }
            } catch (ClassNotFoundException e) {
                
            }
						// 3. 如果父加载器无法加载，则调用自己的 findClass 方法来加载
            if (c == null) {
                long t1 = System.nanoTime();
                c = findClass(name);
                sun.misc.PerfCounter.getParentDelegationTime().addTime(t1 - t0);
                sun.misc.PerfCounter.getFindClassTime().addElapsedTimeFrom(t1);
                sun.misc.PerfCounter.getFindClasses().increment();
            }
        }
      	// 4. 是否需要执行链接
        if (resolve) {
            resolveClass(c);
        }
      
      	// 5. 返回加载得到的 Class 对象
        return c;
    }
}
```

##### findClass

因此为了自定义类加载器，只需要**继承 ClassLoader 抽象类并重写findClass(String name) 方法**，实际上我们只需要**定义如何找到类文件并读取字节码**，之后再通过统一的 defineClass 方法转换为 Class 对象

```java
private final String classPath = "/usr/dev/JVM";

@Override
protected Class<?> findClass(String name) throws ClassNotFoundException {
    try {
        // 1. 在自定义的目录下找字节码文件
        String fileName = classPath + "/" + name.replace('.', '/') + ".class";
        
        // 2. 读取字节码到 byte[]
        byte[] data = Files.readAllBytes(Paths.get(fileName));
        
        // 3. 定义类得到 Class 对象
        return defineClass(name, data, 0, data.length);
    } catch (IOException e) {
        throw new ClassNotFoundException(name, e);
    }
}
```

##### Tomcat

**如果要打破双亲委派模型，就必须重写 loadClass 方法**。而 Tomcat 作为一个 Web 容器，要同时运行多个应用，需要确保每个 WebApp 都有自己单独的类加载器，而且同一个类名在不同应用中可以共存。因此 Tomcat 在 JVM 内置类加载器（Bootstrap、Ext、App）之外，又增加了自己的类加载器层次，来实现 **多应用隔离**和**共享机制**

| 类加载器                | 加载目录                       | 作用范围                            |                                |
| ----------------------- | ------------------------------ | ----------------------------------- | ------------------------------ |
| **CommonClassLoader**   | Tomcat/common/*                | 所有 Web 应用和 Tomcat 内部都能访问 | 公共依赖库，应用和容器共享     |
| **CatalinaClassLoader** | Tomcat/server/*                | 仅 Tomcat 内部使用                  | 应用不可见，专供容器使用       |
| **SharedClassLoader**   | Tomcat/shared/*                | 所有 Web 应用共享，Tomcat 内部不用  | 多应用共享依赖                 |
| **WebAppClassLoader**   | Tomcat/webapps/{app}/WEB-INF/* | 仅当前 Web 应用可见                 | 打破双亲委派，支持隔离与热部署 |

![image-20250918171525201](https://dasi-blog.oss-cn-guangzhou.aliyuncs.com/Java/202509181715264.png)



## 参数总结

### 内存相关

| **参数**                              | **作用**                          |
| ------------------------------------- | --------------------------------- |
| -Xms\<size>[unit]                     | 设置 JVM 初始堆大小               |
| -Xmx\<size>[unit]                     | 设置 JVM 最大堆大小               |
| -Xss\<size>[unit]                     | 设置线程的虚拟机栈大小            |
| -Xmn\<size>[unit]                     | 设置新生代固定大小                |
| -XX:NewSize=\<size>[unit]             | 设置新生代初始大小                |
| -XX:MaxNewSize=\<size>[unit]          | 设置新生代最大大小                |
| -XX:SurvivorRatio=\<ratio>            | 设置 Eden:Survivor 的内存大小比例 |
| -XX:NewRatio=\<ratio>                 | 设置 Old:Young 的内存大小比例     |
| -XX:MaxTenuringThreshold=\<threshold> | 设置新生代晋升为老年代的年龄阈值  |
| -XX:MetaspaceSize                     | 设置元空间初始大小                |
| -XX:MaxMetaspaceSize                  | 设置元空间最大大小                |
| -XX:MaxDirectMemorySize               | 设置直接内存大小                  |

### 垃圾回收器相关

| **参数**                | **作用**             |
| ----------------------- | -------------------- |
| -XX:+UseSerialGC        | 使用 Serial 收集器   |
| -XX:+UseParallelGC      | 使用 Parallel 收集器 |
| -XX:+UseConcMarkSweepGC | 使用 CMS 收集器      |
| -XX:+UseG1GC            | 使用 G1 收集器       |
| -XX:+UseZGC             | 使用 ZGC             |

### GC 日志相关

| **参数**                           | **作用**                   |
| ---------------------------------- | -------------------------- |
| -XX:+PrintGC                       | 打印 GC 简要日志           |
| -XX:+PrintGCDetails                | 打印 GC 详细日志           |
| -XX:+PrintGCDateStamps             | 打印 GC 日志时间戳         |
| -Xloggc:\<path>                    | 指定 GC 日志文件的输出路径 |
| -XX:+PrintTenuringDistribution     | 打印对象年龄分布情况       |
| -XX:+PrintReferenceGC              | 打印各种引用对象的处理情况 |
| -XX:+PrintGCApplicationStoppedTime | 打印 GC 导致应用停顿的时间 |

### 性能调优相关

| **参数**                        | **作用**                           |
| ------------------------------- | ---------------------------------- |
| -XX:+HeapDumpOnOutOfMemoryError | 开启 OOM 时导出堆转储文件          |
| -XX:HeapDumpPath=\<path>        | 指定 OOM 堆转储文件路径            |
| -XX:+UseGCOverheadLimit         | 开启检查 GC 时间过多但回收效果太差 |
| -XX:+PrintFlagsFinal            | 打印所有 JVM 参数及最终值          |
| -XX:+PrintCommandLineFlags      | 打印显式和隐式使用的参数           |
| -XX:+DisableExplicitGC          | 禁止 System.gc()                   |

