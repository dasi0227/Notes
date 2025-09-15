# wrapper

## 包装类

包装类是 Java 提供的、用于把基本数据类型封装成对象的类
- 包装类是不可变对象，一旦赋值就不能改变其内部值
- 有些地方只能放对象，而不能放基本数据类型
- 有以下八大包装类
	- byte    → Byte
	- short   → Short
	- int     → Integer
	- long    → Long
	- float   → Float
	- double  → Double
	- char    → Character
	- boolean → Boolean


## 自动装箱/拆箱

装箱/拆箱本质就是实现类和基本数据类型之间的转换

自动
```java
Integer inte = 100;
int b = a + 1;
```

手动
```java
int n1 = 1;
Integer integer1 = new Integer(n1);
Integer integer2 = Integer.valueOf(n1);
int i = integer1.intValue();
```

## 常用的包装类方法

- 通用的
	- xxx.valueOf(...)：装箱
	- xxx.xxxValue()：拆箱
- 数值类：Integer / Float / Long / Short / Double
	- toString()：转换为字符表示
	- compare(x, y)：比较两个基本类型，返回 -1，0，1
	- max(x, y)：获取最大值
	- min(x, y)：获取最小值
	- parseXxx(String s, int radix)：指定字符串的进制解析
- Character
	- isDigit(char c)：判断是否是数字字符
	- isLetter(char c)：判断是否是字母
	- isUpperCase(char c)：判断大写
	- isLowerCase(char c)：判断小写
	- toUpperCase(char c)：返回大写
	- toLowerCase(char c)：返回小写

## String 和其他包装类的转换

String → 包装类（字符串转成对应类型）
- parseXXX(String)
    ```java
    int i = Integer.parseInt(s);
    ```
- Wrapper.valueOf(String ...)
    ```java
    int i = Integer.valueOf(s);
    ```

包装类 → String
- Wrapper.toString()
    ```java
    String s = i.toString();
    ```
- String.valueOf(Wrapper ...)
    ```java
    String s = String.valueOf(i);
    ```
- 拼接字符串
    ```java
    String s = i + "";
    ```

## Integer 比较

手动装箱：每次 new 一个新对象，此时比较的是内存地址，因此是 false
```java
Integer i = new Integer(1); // or Integer i = 1;
Integer j = new Integer(1); // or Integer j = 1;
System.out.println(i == j); // false
```

自动装箱：从缓存池中返回一个对象（范围是-128~127），m 和 n 是同一个对象，因此是 true
```java
Integer m = Integer.valueOf(1);
Integer n = Integer.valueOf(1);
System.out.println(m == n); // true
```

超出缓存范围：因此会隐式 new 一个 Integet 对象并返回，因此是 false
```java
Integer x = Integer.valueOf(128); // or Integer x = 128;
Integer y = Integer.valueOf(128); // or Integer y = 1;
System.out.println(x == y); // false
```

包装类和基本数据类型：此时比较的是值而不是地址，因此是 true
```java
Integer a = Integer.valueOf(128);
int b = 128;
System.out.println(a == b); // true
```

## String

暂时跳过这部分内容

## StringBuffer

StringBuffer 是 Java 提供的一个可变字符串类，底层用一个字符数组 `char[]` 存储字符内容，并用一个 `count` 字段记录当前字符串的有效长度。
- String 是不可变类（immutable），每次修改字符串都会生成一个新的对象，旧的内容不会被改变
- StringBuffer 是可变类（mutable），所有修改操作都在原有的字符数组上进行，不会新建对象，因此效率更高
- StringBuffer 初始容量是 16，超过后自动扩容

核心方法
- append(...)：追加字符（会自动转化为字符）
- insert(offset, ...)：在指定位置插入内容
- delete(start, end)：删除指定区间的字符（左闭右开）
- replace(start, end, String str)：替换指定区间内容
- reverse()：反转整个字符串
- toString()：将当前 StringBuffer 转为新的 String 对象
- indexOf(String str)：返回子串首次出现的索引位置，未找到返回 -1
- length()：返回字符串长度
- capacity()：返回字符串容量

## StringBuilder

|特性|String|StringBuffer|StringBuilder|
|----|------|------------|-------------|
|可变性|不可变|可变|可变|
|线程安全|✅ 安全（不可变）|✅ 安全（方法加锁）|❌ 不安全|
|性能|最慢|较慢|最快|
|适用场景|固定文本内容|多线程拼接|单线程拼接|
|父类|Object|AbstractStringBuilder|AbstractStringBuilder|
|是否推荐使用|只读文本|并发拼接|普通拼接首选|



