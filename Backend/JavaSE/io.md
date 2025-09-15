# IO

## stream

Java 的 I/O 是基于流的，也就是将数据看作一连串的字节或字符，从源头到目标按顺序读写
- 字节流：InputStream/OutputStream
- 字符流：Reader/Writer
- 输入流：从文件（外存）到程序（内存）
- 输出流：从程序（内存）到文件（外存）

> 上面四个类都是抽象类，需要实现方法，都放在了 java.io 包下

## File

File 类不是文件内容的载体，而是对文件的抽象表示，本质是用于查询和操作文件的元信息，而不是修改其存储内容
- 构造方法（假设工作目录是 "/Users/dasi/projects"）
	- 一个路径（绝对or相对）："/Users/dasi/projects/data.txt" 或 "data.txt"
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
	- renameTo：移动文件或重命名文件（相当于mv）
	- length()：返回文件的字节大小，目录返回 0
	- lastModified：返回最后修改时间的时间戳
	- getName()：返回文件名（不含路径）
	- getPath()：返回路径
	- getAbsolutePath()：返回绝对路径
	- getParent()：返回上级目录
	- list()：列出目录下所有文件的 String 名字数组，如果不是目录返回null
	- listFiles()：列出目录下所有文件的 File 对象数组，如果不是目录返回null

> 目录也是特殊的文件，在这里如果没有特殊说明的时候不做区分

## IOException

必须通过 try–catch 语句捕获，或在方法签名中使用 throws IOException 声明向上抛出

常见子类
- FileNotFoundException：文件未找到
- EOFException：意外到达流末尾
- InterruptedIOException：I/O 操作被中断
- SocketException：网络 I/O 错误

抛出时机：
- 访问文件时发生权限不足
- 目录不存在
- 文件被锁定
- 读取／写入流时出现物理设备故障或网络中断

## FileInputStream / FileOutputStream

FileInputStream
- int read()：返回下一个字节（0–255），到末尾返回 -1
- int read(byte[] b)：读取最多 b.length 个字节到 b 中，返回实际读取到字节数，到末尾返回 -1
- int read(byte[] b, int off, int len)：读取最多 len 个字节到 b 从索引 off 开始存放，返回实际读取到字节数，到末尾返回 -1
- long skip(long n)：跳过并丢弃接下来的 n 个字节，返回实际跳过的字节数
- int available()：返回在不阻塞情况下可直接读取的字节数估计
- void close()：关闭此流并释放与之关联的系统资源

FileOutputStream
- void write(int b)：写入单个字节，将参数 b 的最低 8 位写入文件
- void write(byte[] b)：将字节数组 b 中的所有字节一次性写入文件
- void write(byte[] b, int off, int len)：从数组 b 的索引 off 开始，写入 len 个字节到文件
- void flush()：刷新此输出流，强制将所有缓冲区中的字节写入底层文件系统
- void close()：关闭此输出流并释放与之关联的系统资源

## FileReader / FileWriter

FileReader
- int read()：读取下一个字符（0–65535），到末尾返回 -1
- int read(char[] cbuf)：尝试读取最多 cbuf.length 个字符到 cbuf，返回实际读取数，末尾返回 -1
- int read(char[] cbuf, int off, int len)：从 cbuf[off] 开始写入最多 len 个字符，返回实际读取数，末尾返回 -1
- long skip(long n)：跳过并丢弃接下来的 n 个字符，返回实际跳过数
- boolean ready()：判断流是否已就绪可读（不会阻塞）
- boolean markSupported()：标记功能是否受支持（通常返回 false）
- void close()：关闭此流并释放与之关联的系统资源

FileWriter
- 构造函数可以传入参数 boolean append：true表示追加模式，false表示覆盖模式，不传入默认是覆盖模式
- void write(int c)：写入单个字符
- void write(char[] cbuf)：将整个字符数组写入
- void write(char[] cbuf, int off, int len)：从 cbuf[off] 开始写入 len 个字符
- void write(String str)：写入整个字符串
- void write(String str, int off, int len)：写入字符串 str 中从 off 开始的 len 个字符
- void flush()：刷新此流，强制将缓冲区数据写入底层文件系统
- void close()：关闭此流并释放与之关联的系统资源

## 经典的文件复制／读写字节流的模板

```java
FileInputStream fis = null;
FileOutputStream fos = null;
try {
	fis = new FileInputStream(inputPath);
	fos = new FileOutputStream(outputPath)
	
	byte[] buf = new byte[1024];
	int readLength;
	    while ((readLength = fis.read(buf)) != -1) {
	        fos.write(buf, 0, readLength);
	  	}
} catch (IOException e) {
	e.printStackTrace();
}
````

- 不能直接 write(buf)，因为可能读取的字节数不满 1024
- Java 中赋值表达式的返回值就是被赋的值本身

## 节点流/处理流

节点流：直接连接数据源的流，它是真正负责“和文件打交道”、“和内存通信”的那层
- 数据源：存储数据的地方，是数据的起点
- 文件系统：FileInputStream 连接到某个磁盘文件
- 内存：ByteArrayInputStream、CharArrayReader 连接到内存中的某个数组
- 网络连接：Socket.getInputStream() 连接远端主机发来的网络数据包
- 管道：PipedInputStream 获取多线程间管道的数据
- 标准输入：System.in 获取控制台输入或输入重定向的数据

## 处理流

处理流：不与数据源打交道，而是包裹在节点流外面的工具流，用来增强功能，可以链式地把多种处理流组合起来，为最简单的节点流不断添加新能力
- 转换流
  - InputStreamReader：将字节输入流转换为字符输入流，可指定字符编码
  - OutputStreamWriter：将字符输出流转换为字节输出流，可指定字符编码
- 缓冲流
  - BufferedInputStream / BufferedOutputStream：为字节流加缓冲区，提高 IO 效率
  - BufferedReader / BufferedWriter：为字符流加缓冲区，支持按行读写
- 基本数据流
  - DataInputStream：在输入流上提供 readInt()、readDouble()、readUTF() 等按原生类型读取的方法
  - DataOutputStream：提供 writeInt()、writeDouble()、writeUTF() 等按原生类型写入的方法
- 对象流
  - ObjectInputStream：读取对象流，将字节恢复成 Java 对象
  - ObjectOutputStream：将 Java 对象序列化成字节流写入输出流
- 其他
  - 检验流：CheckedInputStream / CheckedOutputStream，对输入流和输出流的内容做校验（CRC32、Adler32）
  - 连接流：SequenceInputStream，可将多个 InputStream 顺序合并成一个连续流进行读取

```java
public static void main(String[] args) {
    try {
        FileInputStream fis = new FileInputStream("/Users/wyw/Desktop/LearningJava/src/study/FILE/data.txt");
        InputStreamReader isr = new InputStreamReader(fis, "UTF-8");
        BufferedReader br = new BufferedReader(isr);


        String line;
        while ((line = br.readLine()) != null) {
            System.out.println("读取到一行：" + line);
        }
        br.close();
    } catch (IOException e) {
        throw new RuntimeException(e);
    }
}
```
把底层的 FileInputStream 包裹了两层处理流
- InputStreamReader：把 FileInputStream 读到的 byte[] 按指定的 "UTF-8" 编码转换成 char[]
- BufferedReader：在 InputStreamReader 之上增加了一个缓冲区，在缓冲区里按行读取并自动去掉换行符

## 对象处理流

序列化（Serialization）：把一个 Java 对象变成一串字节，让对象脱离 JVM，变成可传输的数据

反序列化（Deserialization）：把流中的对象数据重建回内存

注意
- 类必须实现 Serializable 接口
- 类的成员也必须实现 Serializable 接口
- 读写顺序必须一致
- 建议添加 `private static final long serialVersionUID = 1L;`，保证版本兼容性
- 不可序列化的字段需要用 transient 关键字修饰，跳过序列化
- transient 关键字修饰的字段不会被序列化写入文件，但是在反序列化时，这些字段会被自动赋值为默认值，因此不会报错
- 静态成员不会被序列化，因为它不属于对象，而是属于类