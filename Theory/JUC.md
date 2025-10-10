# 并发编程



   * [线程](#线程)
      * [进程与线程](#进程与线程)
      * [创建线程](#创建线程)
      * [Thread API](#thread-api)
      * [对象监控锁](#对象监控锁)
      * [生命周期](#生命周期)
   * [多线程](#多线程)
      * [概念辨析](#概念辨析)
      * [应用场景](#应用场景)
      * [JMM](#jmm)
      * [线程安全](#线程安全)
      * [死锁](#死锁)
      * [一致性保障](#一致性保障)
   * [volatile](#volatile)
      * [解决可见性](#解决可见性)
      * [解决有序性](#解决有序性)
      * [没解决原子性](#没解决原子性)
   * [synchronized](#synchronized)
      * [底层实现](#底层实现)
      * [升级机制](#升级机制)
      * [使用方法](#使用方法)
   * [CAS](#cas)
      * [乐观锁与悲观锁](#乐观锁与悲观锁)
      * [Unsafe](#unsafe)
      * [原理](#原理)
      * [问题](#问题)
   * [JUC](#juc)
      * [ReentrantLock](#reentrantlock)
      * [Atomic](#atomic)
      * [Future](#future)
      * [CompletableFuture](#completablefuture)
         * [定义](#定义)
         * [创建任务](#创建任务)
         * [链式调用](#链式调用)
         * [组合任务](#组合任务)
         * [结果处理](#结果处理)
      * [ThreadPoolExecutor](#threadpoolexecutor)
         * [线程池](#线程池)
         * [提交任务](#提交任务)
         * [任务流程](#任务流程)
         * [ThreadPoolExecutor](#threadpoolexecutor)
         * [ThreadFactory](#threadfactory)
         * [线程池大小](#线程池大小)
         * [Executors](#executors)
   * [ThreadLocal](#threadlocal)
      * [作用](#作用)
      * [ThreadLocalMap](#threadlocalmap)
      * [InheritableThreadLocal](#inheritablethreadlocal)
      * [内存泄漏](#内存泄漏)
   * [AQS](#aqs)
      * [定义](#定义)
      * [ReentrantLock](#reentrantlock)
      * [Semaphore](#semaphore)
      * [CountDownLatch](#countdownlatch)



## 线程

### 进程与线程

在 Java 中当运行一个 main 函数时，实际上就是开启了一个 JVM 进程，而 main 函数本身实际上只是一个主线程

- **内核线程**：由操作系统内核管理和调度的线程
- **用户线程**：由用户空间程序管理和调度的线程，可以实现与内核线程一对一、一对多、多对一的映射关系
- **Java 线程**：是 JVM 提供的抽象，**通过 Thread 对象封装了对内核线程的使用**，开发者只需要操作 Thread API，不需要和底层 OS API 打交道

| **区别** | **进程** | **线程** |
| -------- | ---------------------------------------------------- | ------------------------------------------------------ |
| **定义** | 程序在操作系统中的一次运行实例，是资源分配的基本单位 | 进程中的一个执行流，是 CPU 调度的基本单位 |
| **内存空间** | 拥有独立的地址空间和资源 | 共享所在进程的地址空间和资源，但有独立的栈和程序计数器 |
| **开销** | 创建、切换开销大，需要操作系统分配和回收资源 | 创建、切换开销小，主要是寄存器和栈的切换 |
| **通信** | 进程间通信需要通过系统调用 | 线程间通信可以直接读写共享内存 |
| **独立性** | 一个进程崩溃通常不影响其他进程 | 一个线程崩溃可能导致整个进程崩溃 |

### 创建线程

所有方法**在底层都是需要 new 一个 Thread 实例并且调用 start 方法，这是 JVM 将 Java 的线程对象映射到到操作系统的内核线程的唯一途径**，以下方法只不过在这个基础上进行了封装

- 继承 Thread 类：重写 run 方法，调用 start() 启动线程

    ```java
    class MyThread extends Thread {
        @Override
        public void run() {
            System.out.println("继承 Thread");
        }
    }
    new MyThread().start();
    ```

- 实现 Runnable 接口：把任务传给 Thread 对象执行，专注于任务逻辑

    ```java
    Runnable task = () -> System.out.println("实现 Runnable");
    new Thread(task).start();
    ```

- 实现 Callable 接口：支持获取返回值和异常，但需要用 FutureTask 包装

    ```java
    Callable<String> task = () -> "实现 Callable";
    FutureTask<String> future = new FutureTask<>(task);
    new Thread(future).start();
    String ret = future.get());
    ```

- 使用 Executors 类：创建线程池，从中获取线程，并指定任务逻辑

    ```java
    ExecutorService pool = Executors.newFixedThreadPool(2);
    pool.execute(() -> System.out.println("使用 Executors"));
    pool.shutdown();
    ```

- 使用 CompletableFuture 类：启动一个异步线程来执行任务，并在任务完成后以链式方式处理结果

    ```java
    CompletableFuture
      .supplyAsync(() -> "使用 CompletableFuture")
      .thenAccept(System.out::println);
    ```

### Thread API

| **方法** | **说明** |
| ---------------------------- | ------------------------------------------------------------ |
| **setName(String name)** | 设置/获取线程名称 |
| **setDaemon(boolean on)** | 设置线程是否为守护线程 |
| **setPriority(int newPriority)** | 设置线程优先级 |
| **start()** | 启动线程，底层会调用 run() |
| **run()** | 线程执行逻辑，需要重写 |
| **join()** | 必须等待该线程执行完毕 |
| **join(long millis)** | 等待该线程执行完毕，但超时后会返回 |
| **sleep(long millis)** | 休眠线程，释放 CPU 但不会释放锁 |
| **yield()** | 提示调度器当前线程可以让出 CPU，但不保证 |
| **interrupt()** | 中断线程，设置中断标志，线程会抛出 InterruptedException 异常 |

> 直接手动调用 Thread 对象的 run 方法仅仅只是像调用普通对象的方法一样，不会创建线程

### 对象监控锁

在 Java 中，每一个对象都天然携带一把锁，这是 JVM 层面对对象的实现机制，同时因为所有对象都继承 Object 类，而 Object 类定义了 wait()、notify()、notifyAll() 方法，提供了操作锁的 API

- wait()：让当前线程进入等待状态，同时释放当前持有的对象锁
- notify()：随机唤醒等待队列中的一个线程
- notifyAll()：唤醒等待队列中的所有线程

### 生命周期

- **NEW**：初始状态，线程被创建出来但是没有调用 start 方法
- **RUNNABLE**：可运行状态，线程调用了 start 方法
    - **READY**：就绪状态，等待分配 CPU 时间片
    - **RUNNING**：正在运行状态，正在占据 CPU 时间片运行
- **BLOCKED**：阻塞状态，线程进入阻塞队列，需要等待锁释放或者系统调用执行完毕才能回到可运行状态
- **WAITING**：等待状态，线程进入等待队列，需要等待其他线程完成动作才能回到可运行状态
- **TIMED_WAITING**：超时等待状态，线程等待固定的时间后自动回到可运行状态
- **TERMINATED**：终止状态，线程已经运行完毕

![image-20250919170056048](https://dasi-blog.oss-cn-guangzhou.aliyuncs.com/Java/202509191700107.png)



## 多线程

### 概念辨析

- **并发（concurrent）**：多个任务在单核处理器的同一个时间段内交替执行
- **并行（parallel）**：多个任务在多核处理器上同时执行
- **同步（synchronous）**：调用方发出请求后，必须等待请求任务完成后才能继续执行
- **异步（asynchronous）**：调用方发出请求后，不需要等待请求任务执行完毕，可以立马继续执行

### 应用场景

- **提升资源利用率（利用并发）**：在 **I/O 密集型**场景（网络请求、数据库操作、文件读写），可以在某个线程等待 I/O 时，让单核切换到其他线程执行其他任务，提高 CPU 吞吐量
- **提高计算速度（利用并行）**：在 **CPU 密集型**场景（图像处理、科学计算、数据分析），可以将任务拆分为多个子任务，放在不同线程中并在多核上并行执行，提高完成速度
- **提高程序响应性（利用异步）**：在交互式场景（GUI、Web），将耗时操作放到**后台线程/守护线程**，避免阻塞主线程，提高用户体验

### JMM

Java Memory Model 是为了实现 JVM 跨平台而定义的一组关于多线程访问共享内存的规则，**是并发编程的语义描述和对机器内存的抽象模型，用来屏蔽不同硬件和操作系统的内存访问差异**，保证多线程环境下的数据一致性

- 主内存：所有线程的共享变量的存储区域
- 工作内存/本地内存：每个线程私有的存储区域，并保存了主内存中共享变量的副本

<img src="https://dasi-blog.oss-cn-guangzhou.aliyuncs.com/Java/202509191559210.png" alt="image-20250919155931157" style="zoom:50%;" />

### 线程安全

线程安全是指在多线程环境下，对于同一份数据，不管有多少个线程访问，都能保证这份数据的**正确性和一致性**

- 一致性
    - **原子性**：业务层面上的原子操作在代码层面会被分割为多条指令，导致执行时会被其他线程打断
    - **可见性**：一个线程修改了共享变量值，其他线程无法立刻看到最新值
    - **有序性**：由于编译器和 CPU 会自动执行指令重排来优化性能，导致实际执行顺序与代码逻辑不一致
- 正确性
    - **竞态**：多个线程竞争共享资源，结果依赖于线程调度顺序，可能会导致数据被反复覆盖或丢失
    - **死锁**：多个线程相互持有对方需要的锁，形成循环等待，导致所有线程永久阻塞
    - **活锁**：线程没有阻塞，但一直在互相让步或重试，导致任务无法推进
    - **饥饿**：某些线程由于优先级过低或资源长期被其他线程占用，始终无法获得执行机会

### 死锁

产生条件

- 互斥：一个资源同一时间只能被一个线程占用
- 占有：当一个线程请求其他资源时，不会释放已占用的资源
- 非抢夺：线程已经占用的资源，不能被其他线程抢夺
- 循环等待：存在一个线程-资源的循环等待链

处理方法

- **预防死锁（运行前）**：破坏上述四个条件中的任何一个
    - 破坏互斥：使用可共享资源
    - 破坏占有：必须一次性申请到所有资源才能执行
    - 破坏非抢占：当线程长时间阻塞时必须释放已经占有的资源，或者允许部分线程可以抢占别人的资源
    - 破坏循环等待：预先规定好资源的申请顺序，确保不会出现循环等待链
- **避免死锁（运行前）**：利用银行家算法，在分配资源前预先判断系统是否会进入不安全状态，如果会则拒绝线程的分配资源请求
- **破除死锁（运行后）**：可以利用 `jconsole` 工具检测死锁，如果存在则手动撤销线程或重启进程

### 一致性保障

- 原子性实现
    - 通过 synchronized 标记复合操作为**临界区**，保证复合操作的不可分割性
    - 通过 Unsafe 类直接执行 CPU 的**原子指令**，保证基本操作的不可分割性
- 可见性实现：volatile、synchronized、Lock 在编译后，JVM 会在合适的位置插入**内存屏障**
    - 如果是写操作会强制写出到主内存
    - 如果是读操作会强制从主内存读入
- 有序性实现
    - volatile 和 synchronized 在编译后，JVM 会在合适的位置插入**内存屏障**，强制禁止代码重排序
    - JMM 定义了一种偏序关系，用来约束哪些操作对另一些操作必须可见且有逻辑先后顺序，也就是说如果 A 的结果对 B 可见，则认为 A **happens-before** B，它们的先后顺序不允许改变，但它们可以和其他无关指令重排



## volatile

### 解决可见性

当一个线程修改了 volatile 变量的值，其他线程可以立即看见最新的值

```java
class Task implements Runnable {
    private volatile boolean running = true; 

    @Override
    public void run() {
        while (running) { }
        System.out.println("任务结束");
    }

    public void stop() {
        running = false;
    }
}

Task task = new Task();
Thread t = new Thread(task);
t.start();
// 当前线程立马写出 running 值到主内存
// 其他线程保证从主内存读入 running 值
// 否则线程很有可能死循环
task.stop();
```

### 解决有序性

禁止对线程创建 volatile 变量的过程进行指令重排，即严格按照**分配空间→初始化→指向地址**的顺序执行

```java
class Singleton {
		private volatile static Singleton instance;

    private Singleton() {}

    public static Singleton getInstance() {
        if (instance == null) {
            synchronized (Singleton.class) {
                if (instance == null) {
                    instance = new Singleton();
                }
            }
        }
      	// 如果指令重排，其他线程可能拿到未初始化的对象
        return instance;
    }
}
```

### 没解决原子性

对 volatile 变量的单一操作在底层拆分为复合操作时，不会保证原子性

```java
class Counter {
    private volatile int count = 0;
    public void increment() {
        count++;
    }
}

Counter c = new Counter();
Thread t1 = new Thread(() -> { for (int i = 0; i < 1000; i++) c.increment(); });
Thread t2 = new Thread(() -> { for (int i = 0; i < 1000; i++) c.increment(); });

t1.start(); t2.start();
t1.join(); t2.join();
// 自增实际上是三条指令：读 → 加 1 → 写
// 对这个对象的复合操作不是原子的，结果会 < 2000
System.out.println(c.count);
```



## synchronized

### 底层实现

synchronized 是 Java 提供的一种**互斥锁机制**，核心思想是**同一时刻，最多只有一个线程能够持有锁并执行代码块，其他线程必须等待锁被释放才能进入**，可以同时保证原子性、有序性和可见性

- Mark Word：存放了锁状态标识（无锁、偏向锁、轻量级锁、重量级锁）和一个指向 Monitor 的指针
- Monitor：每个对象在需要加重量级锁时，会关联到一个 Monitor 对象
    - Owner：当前持有锁的线程
    - EntryList：等待锁的阻塞队列
    - WaitSet：调用 wait 的等待队列

### 升级机制

| **锁状态** | **条件/触发场景** | **Mark Word** | **实现机制** | **特点** |
| ------------ | -------------------------- | ----------------------- | ----------------------------------------------------- | ----------------------------------- |
| **偏向锁** | 只有一个线程反复进入同步块 | 线程 ID | 在对象头记录线程 ID，再次进入无需 CAS | 几乎零开销，适合单线程反复访问 |
| **轻量级锁** | 多个线程交替进入 | 指向 Lock Record 的指针 | 使用 CAS 将对象头替换为指向当前线程栈中的 Lock Record | 线程自旋尝试获取锁，不会立刻阻塞 |
| **重量级锁** | 多个线程同时竞争 | 指向 Monitor 对象的指针 | 依赖操作系统的互斥量 | 有阻塞和唤醒，涉及用户态/内核态切换 |

### 使用方法

- 修饰实例方法：不同线程不能同时执行同一个对象实例的这个方法，线程安全在实例级别

    ```java
    public synchronized void instanceMethod() {
        // 锁的是当前实例 (this)
    }
    ```

- 修饰静态方法：不同线程不能同时执行任何对象实例的这个方法，线程安全在类级别

    ```java
    public static synchronized void staticMethod() {
        // 锁的是类对象 (Class<?>)
    }
    ```

- 修饰代码块：不同线程不能同时执行被 synchronized 包裹的代码块，线程安全取决于锁对象

    ```java
    public void doTask() {
        synchronized(lockObject) {  
            // 锁自定义的对象
        }
        synchronized(this) {  
            // 锁当前对象
        }
        synchronized(SomeClass.class) {  
            // 锁类对象
        }
    }
    ```



## CAS

### 乐观锁与悲观锁

- 乐观锁：认为并发冲突小概率发生，所以在任何时候都不加锁，等到更新时再判断数据是否冲突，如果是则重试，如 CAS 和 version
- 悲观锁：认为并发冲突一定会发生，所以在访问数据的时候就上好锁，确保只有一个线程能访问，如 synchronized 和 ReentrantLock

### Unsafe

**Unsafe** 是 JDK 提供的一个**封装了很多 native 方法的工具类**，没有 Java 实现，而是调用底层 C/C++ 代码，专门给 JVM 和核心类库来直接操作内存、线程、对象布局等

- **native**：是 Java 的一个关键字，用来**标记当前方法由本地代码实现**
- **JNI（Java Native Interface）**：是 Java 定义的一套接口规范/协议，**JVM 通过 JNI 把 native 方法映射到对应的 C/C++ 函数上**，规定了函数名、参数、返回值的对接方式
- C 函数：在 HotSpot 源码中实现的 C/C++ 方法，是 native 方法的真正实现

| **方法** | **说明** |
| ------------------------------------------------------------ | ------------------------------------------------------------ |
| **allocateMemory(long size)** | 像 C 的 malloc，分配堆外的直接内存 |
| **freeMemory(long address)** | 像 C 的 free，释放堆外的直接内存 |
| **putInt(long address, int value)** | 向指定的内存地址写入整型数据 |
| **getInt(long address)** | 从指定的内存地址读取整型数据 |
| **allocateInstance(Class<?> c)** | 绕过构造函数直接创建对象（不执行构造方法） |
| **objectFieldOffset(Field f)** | 获取对象字段的偏移量，用于定位对象内存中的字段 |
| **compareAndSwapInt(Object o, long offset, int expected, int update)** | 原子地比较并交换整型字段 |
| **compareAndSwapLong(Object o, long offset, long expected, long update)** | 原子地比较并交换长整型字段 |
| **compareAndSwapObject(Object o, long offset, Object expected, Object x)** | 原子地比较并交换对象引用 |
| **loadFence()** | 保证该屏障之前的所有读操作一定先于之后的读操作，且之后的读从主内存获取 |
| **storeFence()** | 保证该屏障之前的所有写操作一定先于之后的写操作，且之前的写立即刷到主内存 |
| **fullFence()** | 既约束读又约束写，相当于 loadFence + storeFence |

### 原理

1. Java：调用 Unsafe 类的 compareAndSwapInt(obj, offset, expected, update) 方法
2. Unsafe：读取出 object + offset 指向的内存地址里的当前值，和 expected 值做比较，如果相等则更新为值 update，否则返回 false 继续重试
3. JVM：不走 JNI，而是标记这个方法为 intrinsic 内建函数， JIT 编译时，直接把该方法替换成对应 CPU 的原子指令
4. CPU：x86 执行 lock cmpxchg 指令，arm 执行 LDREX / STREX 指令

### 问题

| **问题** | **描述** | **解决** |
| ------------------------ | ------------------------------------------------------------ | ------------------------------------------------------------ |
| **ABA 问题** | 如果值经过一系列更改后又恢复到初始值，CAS 无法检测到值中间有没有被修改过，它只关心值是否相等 | 给变量加上版本号或者时间戳 |
| **自旋开销大** | 如果 CAS 不成功将会一直循环执行直到成功，如果竞争激烈，就会消耗大量 CPU | 在失败次数过多时退让，结束自旋 |
| **只能保证一个变量的原子性** | 如果需要对多个变量同时更新，CAS 无法保证一致性 | 用 AtomicReference 把多个变量封装成一个对象，通过一次 CAS 更新 |



## JUC

> JUC 指的是 **java.util.concurrent** 下的类

### ReentrantLock

ReentrantLock 是 JUC 提供的一个**多功能锁**

- **重入（Reentrant）**：同一线程可以多次获取锁，调用 lock() 多少次，释放时就需要 unlock() 相同次数 
- **中断**：其他线程可以通过调用 lockInterruptibly() 方法中断锁，支持捕捉 InterruptedException 异常进行相应处理
- **公平**：可以选择严格按照先申请的线程先获得锁
- **通知**：可以通过 newCondition() 获取任意多个 Condition，即对应任意多个不同的阻塞队列，利用 await() / signal() 实现选择性阻塞和唤醒
- **超时**：提供了 tryLocl(timeout) 方法，如果超过等待锁的最长时间，就会自动认为加锁失败，不会无限制地等待下去
- **监控**：可以通过方法 isLocked()、hasQueuedThreads() 等查看锁状态

> synchronized 虽然功能少，但是在简单场景下的性能比 ReentrantLock 要好

```java
class BoundedBuffer<T> {
    private final int capacity = 10;
    private final Queue<T> queue = new LinkedList<>();
    private final ReentrantLock lock = new ReentrantLock();
    private final Condition notFull = lock.newCondition();
    private final Condition notEmpty = lock.newCondition();

    // 生产者
    public void put(T item) throws InterruptedException {
        lock.lock();
        try {
          	// 等待队列有空位
            while (queue.size() == capacity) {
                notFull.await();
            }
          	// 唤醒消费者
            queue.add(item);
            notEmpty.signal();
        } finally {
            lock.unlock();
        }
    }

    // 消费者
    public T take() throws InterruptedException {
        lock.lock();
        try {
          	// 等待队列有数据
            while (queue.isEmpty()) {
                notEmpty.await();
            }
            T item = queue.poll();
          
          	// 唤醒生产者
            notFull.signal();
            return item;
        } finally {
            lock.unlock();
        }
    }
}
```

### Atomic

Atomic 是 JUC 提供的**数值更新工具**，能在并发环境下保证线程安全和操作原子性，底层都是基于 **CAS + volatile** 实现

| **类别** | **代表类** |
| -------------------- | ------------------------------------------------------------ |
| **原子更新基本数据类型** | AtomicInteger、AtomicLong、AtomicBoolean |
| **原子更新数组中的元素** | AtomicIntegerArray、AtomicLongArray |
| **原子更新对象引用** | AtomicReference、AtomicStampedReference、AtomicMarkableReference |
| **原子更新某个类的字段** | AtomicIntegerFieldUpdater、AtomicLongFieldUpdater |

### Future

Future 是 JUC 提供的一种**异步结果容器**，可以在主线程异步提交任务后，在未来某个时间点获取执行结果

- Future：是一个接口，定义了异步任务的基本能力，但不能作为一个线程运行
    - get()：阻塞等待来获取结果
    - get(long timeout, TimeUnit unit)：带超时的阻塞等待来获取结果
    - cancel(boolean mayInterruptIfRunning)：取消任务，参数表示是否允许中断
    - isDone()：判断任务是否完成
    - isCancelled()：判断任务是否被取消
- FutureTask：实现了 Runnable 接口和 Future 接口的类，既作为任务也作为结果容器，可以作为一个线程运行
    - 状态：NEW、COMPLETING、NORMAL、EXCEPTIONAL、CANCELLED、INTERRUPTING、INTERRUPTED
    - 构造函数：传入 Callable/Runnable 对象
    - 创建线程：提交给线程池或直接放到线程中

```java
// 创建线程池
ExecutorService executor = Executors.newSingleThreadExecutor();

// 创建任务
Callable<String> task = () -> {
    Thread.sleep(2000);
    return "任务完成";
};

// 创建异步结果容器
Future<String> future = executor.submit(task);

// 主线程继续执行
...

// 异步获取结果
System.out.println("结果: " + future.get());
```

### CompletableFuture

#### 定义

CompletableFuture 是 Java8 提供的对 Future 的增强版，不仅能支持异步处理，还支持**链式调用、组合任务、异常处理**

![](https://dasi-blog.oss-cn-guangzhou.aliyuncs.com/Java/202509211604605.png)

#### 创建任务

| **方法** | **说明** |
| ------------------------- | ---------------------------------- |
| **runAsync(Runnable)** | 创建无返回值的异步任务 |
| **supplyAsync(Supplier\<T>)** | 创建有返回值的异步任务 |
| **get()** | 阻塞等待结果，会抛出受检异常 |
| **getNow(T valueIfAbsent)** | 立即获取结果，如果没有则返回默认值 |
| **join()** | 阻塞等待结果，会抛出非受检异常 |

```java
CompletableFuture<Void> runFuture = CompletableFuture.runAsync(() -> {
    System.out.println("创建任务：无返回值");
});

CompletableFuture<String> supplyFuture = CompletableFuture.supplyAsync(() -> {
    System.out.println("创建任务：有返回值");
  	return "任务完成";
});

String result = supplyFuture.get();
```

#### 链式调用

| **方法** | **说明** |
| ------------------------ | ---------------------------------------- |
| **thenApply(Function<T,R>)** | 获取上一步任务的返回值，并且返回新值 |
| **thenAccept(Consumer\<T>)** | 获取上一步任务的返回值，但不返回新值 |
| **thenRun(Runnable)** | 不获取上一步任务的返回值，并且不返回新值 |

```java
CompletableFuture.supplyAsync(() -> "Hello")
    .thenApply(s -> s + " World")
    .thenAccept(s -> System.out.println(s))
    .thenRun(() -> System.out.println("任务完成"));
```

#### 组合任务

| **方法** | **说明** |
| --------------------------------------------- | ---------------------------------- |
| **thenCombine(CompletionStage, BiFunction)** | 合并两个任务的结果 |
| **thenCompose(Function<T, CompletionStage\<R>>)** | 把上一步的结果作为下一步的输入任务 |
| **allOf(...)** | 等待多个任务全部完成，没有返回值 |
| **anyOf(...)** | 等待任意一个任务完成，有返回值 |

```java
CompletableFuture<String> cf1 = CompletableFuture.supplyAsync(() -> "任务 1");
CompletableFuture<String> cf2 = CompletableFuture.supplyAsync(() -> "任务 2");

cf1.thenCombine(cf2, (r1, r2) -> r1 + " + " + r2)
   .thenAccept(s -> System.out.println("合并任务：" + s));

cf1.thenCompose(r1 -> CompletableFuture.supplyAsync(() -> r1 + " -> 任务 3"))
   .thenAccept(s -> System.out.println("连接任务：" + s));

CompletableFuture<Void> all = CompletableFuture.allOf(cf1, cf2);
all.thenRun(() -> System.out.println("全部完成：" + cf1.join() + "，" + cf2.join()));

CompletableFuture<String> any = CompletableFuture.anyOf(cf1, cf2);
any.thenAccept(r -> System.out.println("最快完成：" + r));
```

#### 结果处理

| **方法** | **说明** |
| ------------------------------------- | -------------------- |
| **exceptionally(Function<Throwable, T>)** | 出现异常时返回默认值 |
| **handle(BiFunction<T, Throwable, R>** | 处理正常结果或异常 |

```java
cf.exceptionally(e -> "兜底值")
  .thenAccept(System.out::println);

cf.handle((result, exception) -> {
    if (ex != null) 
      return "捕获异常：" + exception.getMessage();
  	else 
	    return result;
}).thenAccept(System.out::println);
```

### ThreadPoolExecutor

#### 线程池

线程池是一种线程复用技术，其核心思想是与其每次都 new Thread 来创建和销毁，不如预先创建一批线程，需要时直接拿来用即可

- **降低资源消耗**：线程池里的线程可以重复利用的，避免频繁创建和销毁
- **提高响应速度**：有任务进来可以立即分配线程
- **增强可管理性**：可以配置**核心线程数、最大线程数、任务队列、线程工厂和拒绝策略**
- **方便调优**：线程池提供了额外的 API 来了解运行状态和线程情况

#### 提交任务

| **方法** | **参数类型** | **返回值** | **特点** | **场景** |
| --------- | ------------------- | ---------------- | ---------------------- | ------------------ |
| **execute** | Runnable | void | 无结果、无异常感知 | 只关心执行 |
| **submit** | Runnable / Callable | Future\<T> | 可获取结果、异常、取消 | 需要结果和控制感知 |
| **invokeAll** | 批量 Callable | List<Future\<T>> | 阻塞，等所有任务完成 | 批量任务并行 |
| **invokeAny** | 批量 Callable | T | 阻塞，最快任务返回 | 竞速执行任务 |

#### 任务流程

```text
提交任务 →
  threadNum < corePoolSize ？
    是 → 创建核心线程执行
    否 → 放入任务队列
          Queue.isFull ?
            否 → 进入队列等待
            是 → threadNum < maximumPoolSize？
                   是 → 创建非核心线程执行
                   否 → 执行拒绝策略
```

#### ThreadPoolExecutor

```java
public ThreadPoolExecutor(
        int corePoolSize,                		// 核心线程数
        int maximumPoolSize,             		// 最大线程数
        long keepAliveTime,              		// 非核心线程的存活时间
        TimeUnit unit,                   		// 存活时间的单位
        BlockingQueue<Runnable> workQueue, 	// 任务队列
        ThreadFactory threadFactory,     		// 线程工厂
        RejectedExecutionHandler handler 		// 拒绝策略
)
```

- 核心线程数：线程池中长期存活的线程数量，即使这些线程空闲也不会被回收
- 最大线程数：线程池会根据提交的任务数量动态创建线程，但是具有一个上限
- 存活时间：先前创建的非核心线程如果在存活时间内始终空闲会被回收
- 任务队列：存放等待执行任务的阻塞队列
    - LinkedBlockingQueue：有限/无限容量，容易导致 OOM
    - ArrayBlockingQueue：有限容量，超出会触发异常
    - SynchronousQueue：零容量，必须立即提交给线程
- 线程工厂：用于自定义线程创建方式，可以灵活地设置名称、优先级等
- 拒绝策略：当任务队列满且已达到最大线程数，线程池对新任务的应对策略
    - AbortPolicy：直接抛出 RejectedExecutionException
    - CallerRunsPolicy：交给提交任务的线程执行
    - DiscardPolicy：直接丢弃任务，不抛异常
    - DiscardOldestPolicy：丢弃队列中最旧的任务，然后尝试提交新任务

#### ThreadFactory

ThreadFactory 是一个函数接口，里面只有一个 newThread 方法，**传递要执行的 Runnable 任务，返回一个新建的 Thread 对象**，可以灵活地设置线程属性

```java
public final class MyThreadFactory implements ThreadFactory {

    private final AtomicInteger counter = new AtomicInteger(1);
    private final String factoryName;

    public MyThreadFactory(String factoryName) {
        this.factoryName = factoryName;
    }

    @Override
    public Thread newThread(Runnable r) {
        Thread t = new Thread(r);
        t.setName(factoryName + "[" + counter.getAndIncrement() + "]");
        t.setDaemon(false);
        t.setPriority(Thread.NORM_PRIORITY);
        return t;
    }
}
```

#### 线程池大小

$N_{thread} = N_{CPU} \times \big(1 + \frac{WaitTime}{ServiceTime}\big)$：目的是让 CPU 既不能空闲也不能过载

- CPU 密集型任务 → WaitTime ≈ 0 →  **N_thread = N_CPU + 1→ 线程大部分时间都在干活 → 多开线程会导致 CPU 过载**
- I/O 密集型任务 → WaitTime ≫ ServiceTime → **N_thread = 2 * N_CPU → 线程大部分时间都在等待 → 少开线程会导致 CPU 空闲**

#### Executors

Executors 是 JUC 提供的一个工具类，主要用来快速创建线程池，本质上是**对 ThreadPoolExecutor 构造函数的封装**

- newFixedThreadPool(int nThreads)：固定大小线程池
- newCachedThreadPool()：可变大小线程池
- newSingleThreadExecutor()：单线程线程池

> 然而 Executors 的策略在底层要么是使用无界队列导致 OOM，要么是使用无界线程导致 CPU 过载，没有办法自定义配置



## ThreadLocal

### 作用

ThreadLocal 本质上就是一个普通的 Java 泛型类，对外暴露了四个 API，其最核心的作用是**为每个线程提供独立的变量副本**

- **线程隔离**：同一个 ThreadLocal 对象，不同线程里存取的值互不干扰，避免多线程环境下共享变量带来的并发安全问题 
- **上下文标记**：可以把与线程绑定的参数放到 ThreadLocal，从而在线程的任何地方和时间都可以直接获取

```java
public class ThreadLocal<T> {
    public ThreadLocal() {} 					// 创建对象
    public T get() { ... }						// 取对象的值
    public void set(T value) { ... }	// 存对象的值
    public void remove() { ... }			// 移除对象
}
```

### ThreadLocalMap

ThreadLocal 的底层原理，就是它还定义了一个静态内部类 **ThreadLocalMap**

- 每个线程都有一个 ThreadLocalMap 的对象

    ```java
    public class Thread implements Runnable {
        ThreadLocal.ThreadLocalMap threadLocals = null;
    }
    ```

- ThreadLocalMap 的键是 ThreadLocal 对象

    ```java
    static class ThreadLocalMap {
        static class Entry extends WeakReference<ThreadLocal<?>> {
            Object value;
            Entry(ThreadLocal<?> k, Object v) {
                super(k);   // 弱引用 key：ThreadLocal
                value = v;  // 强引用 value：存储的数据
            }
        }
    
        private Entry[] table; // 真正存储的地方
    }
    ```

- ThreadLocal 暴露的 API 实际上是在调用内部静态类的方法

    ```java
    public void set(T value) {
      	// 获取当前线程的 ThreadLocalMap
        Thread t = Thread.currentThread();
        ThreadLocalMap map = getMap(t);
      	
      	// 将 this / 当前 ThreadLocal 作为 key 
        if (map != null)
            map.set(this, value);
        else
            createMap(t, value);
    }
    
    public T get() {
      	// 获取当前线程的 ThreadLocalMap
        Thread t = Thread.currentThread();
        ThreadLocalMap map = getMap(t);
      
      	// 根据 this / 当前 ThreadLocal 在 ThreadLocalMap 查值
        if (map != null) {
            ThreadLocalMap.Entry e = map.getEntry(this);
            if (e != null) {
                return (T)e.value;
            }
        }
      	
      	// 返回初始化值
        return setInitialValue();
    }
    ```

<img src="https://dasi-blog.oss-cn-guangzhou.aliyuncs.com/Java/202509220007745.png" alt="e34489aadc8912cbf4dd5e5bcd4b68f6" style="zoom:50%;" />

### InheritableThreadLocal

InheritableThreadLocal 是 ThreadLocal 的一个子类，提供了一种方法**让子线程可以继承父线程的 ThreadLocal**

1. Thread 类还有一个 inheritableThreadLocals 字段，区别于 threadLocals 字段（两个字段是独立的，不会互相拷贝）

    ```java
    class Thread implements Runnable {
        ...
        ThreadLocal.ThreadLocalMap threadLocals = null;
        ThreadLocal.ThreadLocalMap inheritableThreadLocals = null;
    }
    ```

2. 创建新线程时，会将父线程作为参数执行 `inheritThreadLocals`

    ```java
    private void init(ThreadGroup g, Runnable target, String name, long stackSize, AccessControlContext acc) {
        ...
        if (inheritThreadLocals && parent.inheritableThreadLocals != null)
            this.inheritThreadLocals(parent);
    }
    ```

3. 调用 ThreadLocal 类方法 `createInheritedMap ` 赋值给 inheritableThreadLocals 对象，传递父线程的 inheritableThreadLocals

    ```java
    void inheritThreadLocals(Thread parent) {
        this.inheritableThreadLocals =
            ThreadLocal.createInheritedMap(parent.inheritableThreadLocals);
    }
    ```

4. 调用静态类的有参构造方法 `ThreadLocalMap`，传递父线程的 inheritableThreadLocals

    ```java
    static ThreadLocalMap createInheritedMap(ThreadLocalMap parentMap) {
        return new ThreadLocalMap(parentMap);
    }
    ```

5. 遍历父线程的 inheritableThreadLocals，对于每个 Entry 键保持一致，值根据 childValue() 决定

    ```java
    private ThreadLocalMap(ThreadLocalMap parentMap) {
        Entry[] tab = parentMap.table;
        int len = tab.length;
        setThreshold(len);
        table = new Entry[len];
    
        for (Entry e : tab) {
            if (e != null) {
                ThreadLocal key = e.get();
                Object value = key.childValue(e.value); // 👈 调用 InheritableThreadLocal 的扩展点
                table[...] = new Entry(key, value);
            }
        }
    }

6. 默认是直接返回父线程的值，也就是复用一个对象，相当于浅拷贝，可以重写来实现深拷贝

    ```java
    protected T childValue(T parentValue) {
        return parentValue;
    }
    ```

### 内存泄漏

ThreadLocalMap 中的 **key 实际上是 ThreadLocal 对象的弱引用，也就是说，如果除了 ThreadLocalMap 没有其他对象强引用 ThreadLocal 对象，那么 ThreadLocal 对象会被回收**

此时 key = null 但是 value 存的值还在，又由于线程池里面的线程不会被销毁，所以 ThreadLocalMap 对象不会被回收，导致 **value 对象不会再被使用但是一直占据内存**

最佳解决办法就是**通过 try-finally 使用 remove 方法**，保证每次使用完 ThreadLocal 都会清理 ThreadLocalMap 对应的 entry

```java
public void remove() {
  	// 获取当前线程的 ThreadLocalMap
    Thread t = Thread.currentThread();
    ThreadLocalMap m = getMap(t);
  	// 以当前 ThreadLocal 对象作为 key，删除 entry
    if (m != null) {
        m.remove(this);
    }
}
```



## AQS

### 定义

**AQS（AbstractQueuedSynchronizer，抽象队列同步器）** 是 JUC 中实现各种锁和同步器的基础框架

- **exclusiveOwnerThread**：独占模式下，记录当前持有锁的线程
- **state 状态值**：一个 volatile int 值，用来表示资源状态（锁、计数器），提供原子操作 get、set 和 CAS
- **CLH 双向队列**：一个 FIFO 队列，具有头尾指针，用来存储竞争失败的线程
    - 初始化：只有一个空的 head = tail = new Node()
    - 入队/阻塞：先令 tail.next = newNode，再令 newNode.prev = tail，最后令 tail = newNode
    - 出队/唤醒：唤醒 head.next，然后令 head = head.next
- **Node 线程节点**：每个等待的线程会被封装成一个 Node
    - **waitStatus**：节点的等待状态，包括 INIT(0)、CANCELLED(1)、SIGNAL(-1)、CONDITION(-2)、PROPAGATE(-3)
    - **prev / next**：双向链表的前驱节点和后继节点
    - **thread**：当前节点封装的线程
    - **nextWaiter**：在条件队列中使用，区分共享模式和独占模式
- **获取/释放模版方法**：不同的同步器只需要重写 tryAcquire / tryRelease / tryAcquireShared / tryReleaseShared 来自定义 CLH 操作

![image-20250922102049717](https://dasi-blog.oss-cn-guangzhou.aliyuncs.com/Java/202509221020771.png)

### ReentrantLock

**可重入的独占锁，用于保证临界区的线程安全**

- nextWaiter = null：独占模式
- state：当前锁的持有次数，初始值为 0
- tryAcquire：调用 lock() 时执行，如果 state == 0 会 CAS 为 1，如果已经持有锁会 state++，成功则返回 true，否则返回 false
- tryRelease：调用 unlock() 时执行，直接 state--，此时如果 state == 0 会返回 true，否则返回 false

### Semaphore

**计数信号量，用于限制同时访问资源的线程数量**

- nextWaiter = SHARED：共享模式
- state：当前可用的许可数量，初始值为 permits
- tryAcquireShared：调用 acquire() 时执行，如果 state > 0 会 CAS 减少 1 并返回剩余许可数，否则返回 -1
- tryReleaseShared：调用 release() 时执行，直接 CAS 增加 1，成功则返回 true，否则返回 false

### CountDownLatch 

**倒计时门闩，用于等待线程完成**

- nextWaiter = SHARED：共享模式
- state：表示需要等待的事件数，初始值为 count
- tryAcquireShared：调用 await() 时执行，如果 state == 0 会返回 1，否则返回 -1
- tryReleaseShared：调用 countDown() 时执行，直接 CAS 减少 1，此时如果 count == 0 会返回 true，否则返回 false