# Grammar



   * [初识 Java](#初识-java)
      * [基础知识](#基础知识)
      * [JVM](#jvm)
      * [main](#main)
      * [package](#package)
      * [Annotation](#annotation)
      * [Java 开发流程](#java-开发流程)
   * [语法](#语法)



## 初识 Java

### 基础知识

Java 基础

- 源文件的基本组成部分是 class
- java 语言严格区分大小写，每个语句以 ; 结束，大括
- java 程序的执行入口是 main 方法
- 一个源文件只能有一个 public 类，但可以有多个非 public 类
- 如果源文件存在 public 类，那么该文件应该用类名命名

文档注释

- 当行注释：//，用于解释代码
- 多行注释：/**/，用于解释代码
- javadoc注释：@标签 标签值，用于给类说明代码的作者、版本的元信息

模版

- main/psvm：生成 public static void main(String[] args)
- sout：生成 System.out.println()
- fori：生成 for (int i = 0; i <  ; i++) {}
- ifn：生成 if (var == null)
- inn：生成 if (var != null)

Java 程序三大阶段

- 编译（Compile）：用 javac 将 .java 源文件翻译成与平台无关的字节码 .class
    - 语法检查：构建抽象语法树（AST），检测报告拼写、括号匹配、关键字使用等语法错误
    - 类型检查：在 AST 基础上验证操作数和表达式的类型兼容性
- 加载（Load）：类加载器把 .class 文件读入内存，生成对应的 Class 对象
    - 验证：检查字节码的合法性
    - 准备：为静态变量分配内存并设置默认值
    - 解析：将常量池的符号引用转化为直接引用
- 运行（Run）：JVM 对已加载的字节码执行各项操作
    - 类初始化：执行 <clinit> 方法，按源码中出现顺序为静态字段赋予显式初始值并运行静态代码块
    - 执行用户代码：从 main 入口开始，JVM 调用 JIT 执行字节码，直到程序正常退出或因异常终止

### JVM

JVM 是用来执行 Java 字节码（`.class` 文件）的运行环境，它不是 Java 语言的一部分，而是运行 Java 的“执行器”，相当于 Java 程序的“宿主机”。

- **堆（Heap）**：存放对象实例，是垃圾回收器（GC）主要管理的区域，所有对象和数组都分配在堆中。
- **栈（Stack）**：每个线程都有独立栈帧，用于存放局部变量、方法调用过程、返回值等，生命周期与线程一致。
- **元空间（MetaSpace）**：JDK 8 之后取代永久代（PermGen），用于存储类结构信息、常量池、静态变量等，分配在本地内存。
- **程序计数器（PC Register）**：每个线程有独立的程序计数器，记录当前线程正在执行的字节码指令地址。
- **本地方法栈（Native Method Stack）**：用于支持 Java 中调用 Native 方法（通过 JNI 接口调用的 C/C++ 本地代码），结构与 Java 栈类似，但执行的是本地代码。

Java 程序不是直接运行在操作系统上，无论你是 mac 还是 windows，而是运行在 JVM 上。JVM 负责跨平台、内存管理、代码执行、异常处理等一切底层脏活累活！

### main

```java
public static void main(String[] args){}
```

- public：必须是公开的，JVM 才能从外部访问此方法
- static：不依赖对象实例，JVM 无需创建对象就能调用它
- void：无返回值，程序从这里开始执行，不需要返回，不然返回给谁？
- main：固定方法名，JVM 会寻找 main，大小写敏感
- String[] args：命令行参数传入口，字符串数组类型，程序运行时从命令行接收参数

### package

Java 的包（package） = C++的命名空间（namespace） = 文件夹（folder）：用于组织类的一种方式，是代码归类管理系统 + 访问权限控制器 + 防命名冲突机制

```java
package com.example.myapp;
```

- package 指令必须放在程序第一行，并且只能有一句
- import 用于引入别的类，紧跟在 package 下面
- 包名与所在文件夹结构必须一一对应，用 `.` 代替 `/`
- 声明为 public 类才能在别的程序中访问

常见的包

| 包名            | 用途说明                                                     |
| --------------- | ------------------------------------------------------------ |
| `java.lang`     | 核心类库，自动导入，如 `String`、`Object`、`Math`、`System`  |
| `java.util`     | 工具类和集合框架，如 `List`、`Map`、`Date`、`Collections`    |
| `java.io`       | 输入输出流，文件读写相关                                     |
| `java.nio`      | NIO（New IO），支持缓冲区、通道，适合高性能 IO               |
| `java.net`      | 网络编程，支持 `URL`、`Socket` 等                            |
| `java.time`     | 日期和时间 API（Java 8+），如 `LocalDate`、`Instant`         |
| `java.math`     | 高精度数学运算，如 `BigDecimal`、`BigInteger`                |
| `java.sql`      | JDBC 数据库访问相关接口                                      |
| `java.security` | 加密与安全机制，如 `MessageDigest`、`KeyStore`               |
| `javax.*`       | Java 扩展库，如 `javax.servlet`（Web）、`javax.swing`（GUI） |

### Annotation

注解是给 Java 代码添加元数据的语法结构，它不会直接改变代码逻辑，但可以被编译器、运行时、框架处理，产生间接行为效果。

- @Override：检查方法是否真的是重写，而不是创建新函数，只能修饰方法
- @Deprecated：标记方法已经过时，但是不代表不可用，不推荐使用，因为在之后可能被删除或更改接口，可以修饰类、方法、属性等
- @SuppressWarnings({"警告类型"})：用于关闭/抑制指定类型的编译警告，作用域跟放置位置有关
    - "all"：全部警告
    - "rawtypes"：忽略未使用泛型的原始类型
    - "unchecked"：忽略泛型未检查转换的警告
    - "deprecation"：忽略使用 @Deprecated 的警告
    - "unused"：忽略未使用已定义的方法或变量的警告

元注解：用于注解注解的注解

- @Target： 限制注解使用的位置（类、方法、字段等）
    - `ElementType.TYPE`：类、接口、枚举
    - `ElementType.METHOD`：方法
    - `ElementType.FIELD`：字段
    - `ElementType.CONSTRUCTOR`：构造器
    - `ElementType.PARAMETER`：参数
    - `ElementType.ANNOTATION_TYPE`：注解类型（用于注解注解）

- @Retention：注解在代码中的保留时长
    - `RetentionPolicy.SOURCE`：编译器阶段有效，class 文件中不保留（如 @Override）
    - `RetentionPolicy.CLASS`：编译进 class 文件，运行时不可见（默认）
    - `RetentionPolicy.RUNTIME`：运行时可通过反射读取（Spring 最爱）

- @Documented：是否包含在 Javadoc 中，通常用于公共 API 注解，让它出现在文档中

- @Inherited：子类是否可以继承父类的注解 只作用于类注解

### Java 开发流程

1. 分析：需求收集、可行性研究、制定需求文档
2. 设计：架构设计、模块划分、接口与数据库设计
3. 实现：编码开发、单元测试、代码评审
4. 测试：集成测试、系统测试、性能与安全测试
5. 实施：部署上线、用户培训、运维交接
6. 维护：故障修复、性能优化、功能迭代



## 语法

有 C、C++ 和 Python 基础，不再赘述，也没必要做笔记，直接查看：[菜鸟教程](https://www.runoob.com/java/java-tutorial.html)