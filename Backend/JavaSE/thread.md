# thread

## 基础

线程由进程或者其他线程创建的，程序中可以并发执行的最小单位，每个线程都有自己独立的栈空间和执行路径，多个线程可以同时跑不同的代码段
- 单线程：同一时刻只有一个线程执行
- 多线程：同一时刻，多个线程执行
- 并发：同一时刻，多个任务在同个核心交替执行，微观下是轮流执行，宏观下是同时执行
- 并行：同一时刻，多个任务在不同核心同时执行，微观和宏观都是同时执行 
- 异步（Asynchronous）：不等结果，调用者继续执行
- 同步（Synchronous）：顺序执行，调用者会等待任务完成后再继续执行

## 流程

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

## 线程状态

- NEW（新建）：线程对象刚被创建，还未调用 start()，尚未与任何底层线程关联
- RUNNABLE（可运行）/READY（就绪）：线程已调用 start()，正等待 JVM 和操作系统调度，一旦获取到 CPU 时间片，就执行 run() 方法
- RUNNING（允许中）：线程正在占用 CPU 时间片，执行 run 方法
- BLOCKED（阻塞）：因锁被其他线程持有而挂起，等待锁释放
- WAITING（等待）：线程主动放弃 CPU，并无限期等待另一个线程的通知／中断／定时等待结束
- TIMED_WAITING（超时等待）：在有超时参数的等待方法中挂起，到期后自动唤醒或被中断
- TERMINATED（终止）：run() 方法执行完毕正常返回，或抛出未捕获异常，线程生命周期结束，再也不会被调度

## 用户线程和守护线程

- 用户线程（User）：也称为“前台线程”，是完成应用程序核心业务逻辑的线程，JVM 会一直等待所有用户线程结束后，才允许进程退出
- 守护线程（Daemon）：也称为“后台线程”或“服务线程”，通常用来执行一些辅助性工作，如垃圾回收、监控、日志清理等，当 JVM 发现只剩下守护线程 在运行时，会自动结束进程，不再等待它们完成（没有了用户线程，守护线程守护什么呢？）

必须在 start() 之前调用 setDaemon()，否则抛出 IllegalThreadStateException，因为操作系统的线程属性一旦创建，无法在运行时再更改守护/后台标志
- setDaemon(true)：将调用线程标记为守护线程
- setDaemon(false)：将调用线程标记为非守护线程（默认行为）
- isDaemon()：查询线程当前是否为守护线程

## 常见方法

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

## Runnable 和 Thread

```java
Runnable task = new MyTask();
Thread thread = new Thread(task, "Worker-1");
thread.start();
```
- Runnable 接口：很小，内部只有 run 方法，定义了一段可在独立线程中执行的逻辑
- Thread 接口：很大，除了 run 还有很多其他方法
- 上述做法的好处
  1. 将任务和线程分离，让你的业务逻辑只关心实现run方法本身，而不必与线程创建、启动的细节耦合
  2. 任务类依然可以继承其他父类或实现更多接口
  3. 只需把同一个 Runnable 实例交给不同的 Thread 对象即可轻松共享状态，无需为每个线程都写一个新的子类

Thread 底层本质流程
1. JVM 在构造函数里把传入的 Runnable 对象赋给 this.target，并设置线程名称、优先级等，状态为 NEW
2. 用户线程执行 thread.start()
3. thread.start() 内部调用 start0()
4. start0() 内部根据操作系统类型调用 pthread_create（Linux）或 CreateThread（Windows）等，将资源（栈、TLS、调度上下文）分配给新线程，标记为可运行
5. 操作系统在某个时间片决定运行该内核线程，CPU 跳转到 HotSpot 提供的 JNI 入口
6. 在 JNI 入口完成 JVM 线程环境挂载后，调用 Java 层的 thread.run()
6. 如果构造时传入了 Runnable，则执行 target.run()，否则执行 this.run()

## 线程终止

1. run 正常执行完毕，线程自动终止
2. 如果 run() 方法内部抛出一个未被捕获的异常，JVM 会在本地入口捕获该异常，并终止线程
3. 调用 interrupt() 时，方法 Thread.currentThread().isInterrupted() 会返回中断，可以在 run 中循环判断从而终止
4. 也可以在 run 方法循环判断一个成员变量，并提供一个接口允许外部修改成员变量，从而实现终止


## 同步机制

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

