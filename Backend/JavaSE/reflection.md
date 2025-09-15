# 反射

## 定义

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

## 流程

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

## ClassLoader

类加载器：Java 的一切都是类和对象，类加载器负责在运行时将字节码（.class 文件）加载到 JVM，并生成对应的 Class 对象

- Bootstrap（引导）：用原生代码实现，加载 JRE 中最基础的核心库，如java.lang.*、java.util.*、java.io.*、java.net.* 等

- Platform/Extension（平台/扩展）：由 Java 程序自己实现，加载 JRE 扩展目录下的类库，如第三方 JDBC 驱动、JVM 工具/监控 jar 等

- Application/System（应用/系统）：加载用户类路径下的所有类

## Class

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

## Field/Method/Constructor

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
=32，VOLATILE=64，TRANSIENT=128，NATIVE=256

## 通过反射创建对象

（假设对象是A）
1. 获取 Class 实例：forName
2. 获取 Constructor 实例：getConstructor/getDeclaredConstructor
3. private需要暴破：setAccessible(true)
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
        // 2. 无参public构造
        Object o1 = userClass.newInstance();
        System.out.println(o1);
        // 3. 有参public构造
        Constructor<?> constructor1 = userClass.getConstructor(String.class);
        Object o2 = constructor1.newInstance("wyw");
        System.out.println(o2);
        // 4. 有参private构造
        Constructor<?> constructor2 = userClass.getDeclaredConstructor(int.class, String.class);
        constructor2.setAccessible(true);
        Object o3 = constructor2.newInstance(18, "jason");
        System.out.println(o3);
    }
}
```


