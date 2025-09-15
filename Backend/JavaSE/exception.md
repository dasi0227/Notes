# Exception

## 介绍

异常是程序运行时发生的错误情况，会导致程序退出，而不是语法错误（变量名拼错，无法通过编译）或逻辑错误（无限循环，无法结束）

- Error：无法解决，程序崩溃
	- StackOverflowError：栈溢出，方法递归过深导致栈空间耗尽
	- OutOfMemoryError：内存溢出，数组开得过大导致内存资源耗尽
	- NoClassDefFoundError：类定义在运行时未找到

- Exception：可以解决，修复后程序可以继续运行
	- 运行时异常（RuntimeException）：非受检异常，运行时才能发现出错
		- NullPointerException：空指针访问
		- ArithmeticException：算术异常，如除 0 错误
		- IndexOutOfBoundsException：数组/集合下标越界
		- ClassCastException：类转换异常
		- NumberFormatException：数字格式异常
		- IllegalArgumentException：参数非法
	- 编译时异常（CheckedException）：受检异常，编译器要求必须处理
		- IOException：I/O 失败
		- SQLException：数据库错误
		- ClassNotFoundException：类加载失败
		- FileNotFoundException：文件未找到
		- EOFException：已到输入流末尾仍尝试读取数据

## try-catch-finally

```java
try {

        } catch(Exception e) {

        } finally {

        } 
```
- try：运行代码 ➡️ 预感到可能有异常，尝试运行
- catch：捕获异常 ➡️ 赋值给最顶级父类 Exception 的对象实例，然后进行处理
- finally：善后，通常用来收尾清理资源 ➡️ 不管是否有异常发生，都需要执行，即使 try 或 catch 里有 return

注意
- catch 语句块要先写子类异常类型，再写父类异常类型，也就是捕获必须先精细化再泛化，不然永远也捕获不到精细化的异常
- finally 如果写了 return，会覆盖原来的 return 值

## throws

```java
import java.io.FileNotFoundException;

public void func() throws FileNotFoundException, NullPointerException {}
```
throws 是方法签名的一部分，用来声明该方法可能抛出一个或多个异常，用于让调用者来处理异常
- 受检异常/编译异常必须显式声明 throws，否则会报错
- 非受检异常/运行异常默认使用了 throws，可以不用显式说明
- 子类重写父类方法时，所抛出的异常类型要么和父类一致，要么是父类抛出异常类型的子类（本质是多态和动态加载）

## throw

throw 是方法体的一部分，用于主动抛出一个异常对象，并终止当前方法的正常执行流程
- throw 后面必须跟一个 Throwable 对象，即 Exception 或 Error 的子类，不接受任何其他类型
- 一旦 throw，直接终止当前位置的执行流，往上抛给调用者，如果没人 catch，就一路传到 main，如果 main 也没 catch，那么 JVM 的默认异常处理器会接住异常，并直接终止整个程序（JVM 表示它很忙的，没空给你精细化处理，有事就给我停）

## 自定义异常

新建一个异常类，必须继承
- extends Exception ➡️ 表示这是一个受检异常（Checked）
- extends RuntimeException ➡️ 表示这是一个非受检异常（Unchecked）
- 一般都是继承 RuntimeException，因为可以使用默认处理机制，否则每个父类都需要显式地处理编译异常
- super(String)：利用构造函数指定错误信息

## 常用方法

Exception 对象不只是爆炸提示，它还能告诉你：炸在哪、为啥炸、谁炸的、上游是谁
- getMessage()：获取异常的详细信息，也就是传给构造函数的 message 字符串
- printStackTrace()：把异常的完整堆栈信息输出到控制台
- getCause()：获取异常的根本原因
- toString()：返回异常的字符串表示，一般包含类名和 message