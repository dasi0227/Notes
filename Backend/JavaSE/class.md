# Class



   * [常用类](#常用类)
      * [Math](#math)
      * [Arrays](#arrays)
      * [System](#system)
      * [BigInteger/BigDecimal](#bigintegerbigdecimal)
      * [LocalDate/LocalTime/LocalDateTime](#localdatelocaltimelocaldatetime)
   * [ENUM](#enum)
      * [定义](#定义)
      * [底层](#底层)
      * [使用](#使用)
      * [API](#api)
   * [Exception](#exception)
      * [定义](#定义)
      * [try-catch-finally](#try-catch-finally)
      * [throws](#throws)
      * [throw](#throw)
      * [自定义异常](#自定义异常)
      * [API](#api)
   * [Wrapper](#wrapper)
      * [定义](#定义)
      * [自动装箱/拆箱](#自动装箱拆箱)
      * [API](#api)
      * [String 和其他包装类的转换](#string-和其他包装类的转换)
      * [Integer 比较](#integer-比较)
   * [StringBuffer](#stringbuffer)
      * [定义](#定义)
      * [API](#api)
      * [字符串相关类的比较](#字符串相关类的比较)
   * [RegExp](#regexp)
      * [语法](#语法)
      * [Pattern](#pattern)
      * [Matcher](#matcher)
      * [案例](#案例)



## 常用类

### Math

Math 是 Java 提供的数学工具类，包含了大量常用的数学运算方法，全部都是静态方法，可以直接通过 `Math.` 调用，无需创建对象

- Math.abs(x)：返回绝对值
- Math.max(x, y)：返回最大值
- Math.min(x, y)：返回最小值
- Math.pow(a, b)：a 的 b 次幂
- Math.sqrt(x)：平方根
- Math.cbrt(x)：立方根
- Math.ceil(x)：向上取整（返回 >= x 的最小整数）
- Math.floor(x)：向下取整（返回 <= x 的最大整数）
- Math.round(x)：四舍五入（返回 long 或 int）
- Math.random()：返回 [0.0, 1.0) 范围内的随机数（double）
- Math.log(x)：自然对数（底为 e）
- Math.log10(x)：以 10 为底的对数
- Math.exp(x)：e 的 x 次幂
- Math.sin(x), cos(x), tan(x)：三角函数（x 单位是弧度）
- Math.toRadians(deg)：角度转弧度
- Math.toDegrees(rad)：弧度转角度
- Math.PI：圆周率 π ≈ 3.14159
- Math.E：自然常数 e ≈ 2.71828

### Arrays

Arrays 是 Java 提供的数组工具类，位于 `java.util` 包下

- Arrays.toString(array)：将一维数组转换为字符串（可打印）
- Arrays.deepToString(array)：将多维数组转换为字符串（递归打印）
- Arrays.sort(array)：对数组排序（默认升序）
- Arrays.copyOf(array, newLength)：复制数组到新长度
- Arrays.copyOfRange(array, from, to)：复制指定范围的子数组
- Arrays.equals(a1, a2)：判断两个数组内容是否相等（按值）
- Arrays.deepEquals(a1, a2)：判断多维数组是否相等
- Arrays.fill(array, value)：用指定值填充数组
- Arrays.binarySearch(array, key)：对已排序的数组进行二分查找
- Arrays.setAll(array, lambda)：用函数生成数组内容

### System

`System` 是 Java 提供的系统工具类，位于 `java.lang` 包下，提供了访问系统属性、标准输入输出、内存控制、时间戳等功能，全部方法和字段都是静态的，直接通过 `System.` 调用，无需创建对象

- System.out.print(...) / println(...)：标准输出，控制台打印
- System.err.print(...) / println(...)：标准错误输出
- System.in：标准输入流（通常结合 Scanner 使用）
- System.currentTimeMillis()：返回时间戳
- System.nanoTime()：纳秒级别高精度时间戳，本身没有意义，通常成对出现用于记录时间间隔
- System.exit(status)：会立刻终止虚拟机，不执行 finally 块，0 表示正常退出
- System.gc()：建议 JVM 进行垃圾回收，但也仅建议
- System.arraycopy(src, srcPos, dest, destPos, length)：高效复制数组
- System.getProperty(String key)：获取系统属性
- System.getenv(String name)：获取环境变量
- System.in：标准输入流（InputStream）
- System.out：标准输出流（PrintStream）
- System.err：标准错误输出流（PrintStream）

### BigInteger/BigDecimal

BigInteger：用于处理任意长度的整数，可以用于运算

- add(b)：加法
- subtract(b)：减法
- multiply(b)：乘法
- divide(b)：整除
- mod(b)：取模
- pow(n)：a 的 n 次方
- compareTo(b)：比较大小（返回 -1 / 0 / 1）
- gcd(b)：最大公约数
- abs()：绝对值
- negate()：取负数
- isProbablePrime(certainty)：判断是否为质数

BigDecimal：用于处理任意精度的小数

- add(b)：加法
- subtract(b)：减法
- multiply(b)：乘法
- divide(b, scale, roundingMode)：除法，指定保留位数和舍入模式
- setScale(scale, roundingMode)：设置小数精度
- compareTo(b)：比较大小（返回 -1 / 0 / 1）
- abs()：绝对值
- negate()：取负数
- movePointLeft(n)：相当于除以 10^n
- movePointRight(n)：相当于乘以 10^n
- stripTrailingZeros()：去除末尾多余 0

### LocalDate/LocalTime/LocalDateTime

- LocalDate
    - LocalDate.now()：获取当前日期（系统默认时区）
    - LocalDate.of(year, month, day)：指定年月日创建日期对象（月份从 1 开始）
    - getYear() / getMonth() / getDayOfMonth()：获取年、月、日
    - plusDays(n) / plusMonths(n) / plusYears(n)：加时间（返回新对象）
    - minusDays(n) / minusWeeks(n)：减时间（返回新对象）
    - isBefore(date)、isAfter(date)、isEqual(date)：比较时间先后或相等
    - lengthOfMonth()：当前月的天数
    - getDayOfWeek()：获取星期几（枚举值）
    - withDayOfMonth(n)：设置为某天（返回新对象）
- LocalTime
    - LocalTime.now()：获取当前时间（时分秒）
    - LocalTime.of(hour, minute, second)：指定时分秒创建时间对象
    - getHour() / getMinute() / getSecond()：获取时间字段
    - plusHours(n) / plusMinutes(n) / plusSeconds(n)：加时间（返回新对象）
    - minusHours(n) / minusMinutes(n)：减时间（返回新对象）
    - isBefore(time)、isAfter(time)、equals(time)：比较先后或相等
    - withHour(n)：修改指定字段（返回新对象）
- LocalDateTime
    - LocalDateTime.now()：获取当前日期和时间
    - LocalDateTime.of(year, month, day, hour, min, sec)：指定日期时间
    - getYear() / getMonth() / getHour() / getMinute() 等：获取字段
    - plusDays(n)、plusHours(n)、plusMinutes(n)：加时间（返回新对象）
    - minusDays(n)、minusHours(n)：减时间（返回新对象）
    - isBefore(dt)、isAfter(dt)、equals(dt)：比较时间先后
    - withDayOfMonth(n)、withHour(n)：修改字段（返回新对象）
    - toLocalDate()：提取日期部分
    - toLocalTime()：提取时间部分



## ENUM

### 定义

枚举是用来表示一组固定常量的类型，比如星期、颜色、状态、方向这种就特别适合用枚举，因为它们的取值是固定且有限的

### 底层

枚举本质上是类型为 public static final 的 ENUM 类的实例

```java
enum Color {
    RED, GREEN, BLUE;
}
// 等价于
final class Color extends Enum<Color> {
    public static final Color RED = new Color("RED", 0);
    public static final Color GREEN = new Color("GREEN", 1);
    public static final Color BLUE = new Color("BLUE", 2);
}
```

如果是自己实现的 enum 类

```java
enum Season {
    Spring("春天", "潮湿"),
    Summer("夏天", "炎热"),
    Autumn("秋天", "温和"),
    Winter("冬天", "寒冷");

    private final String name;
    private final String desc;

    Season(String name, String desc) {
        this.name = name;
        this.desc = desc;
    }

    public String getName() {
        return name;
    }

    public String getDesc() {
        return desc;
    }
}
```

### 使用

- enum 关键字创建的类默认继承 java.lang.Enum，不能再继承其他类
- enum 创建的类是一个 final 类，也就是不可被继承（因为枚举值不希望被更改），但是可以实现接口
- JVM 会把每个枚举值变成当前类的**静态常量实例**，即 public static final，本质是对象
- 枚举构造函数必须是 private，不能被外部实例化
- 枚举值必须写在最前面/最上面，后面才能定义字段和方法
- 枚举值可以没有字段，此时使用的是默认的无参构造函数
- 枚举值也可以自定义字段，用有参构函数赋值
- 自定义字段不能与枚举值重名
- 构造函数得到的枚举对象必须放在第一行

### API

- name()：返回枚举常量在定义时的名字，不可重写
- toString()：返回枚举值，可重写
- ordinal()：返回枚举值的位置，按照声明顺序，从 0 开始
- values()：返回所有枚举值，是一个 Enum[] 数组
- valueOf(String name)：将字符串转化为对应的枚举值，大小写敏感
- equals(Object o)：判断是否为同一个枚举实例
- compareTo(Enum e)：返回当前枚举对象的编号 - 传递的枚举对象的编号



## Exception

### 定义

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

### try-catch-finally

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

### throws

```java
import java.io.FileNotFoundException;

public void func() throws FileNotFoundException, NullPointerException {}
```

throws 是方法签名的一部分，用来声明该方法可能抛出一个或多个异常，用于让调用者来处理异常

- 受检异常/编译异常必须显式声明 throws，否则会报错
- 非受检异常/运行异常默认使用了 throws，可以不用显式说明
- 子类重写父类方法时，所抛出的异常类型要么和父类一致，要么是父类抛出异常类型的子类（本质是多态和动态加载）

### throw

throw 是方法体的一部分，用于主动抛出一个异常对象，并终止当前方法的正常执行流程

- throw 后面必须跟一个 Throwable 对象，即 Exception 或 Error 的子类，不接受任何其他类型
- 一旦 throw，直接终止当前位置的执行流，往上抛给调用者，如果没人 catch，就一路传到 main，如果 main 也没 catch，那么 JVM 的默认异常处理器会接住异常，并直接终止整个程序（JVM 表示它很忙的，没空给你精细化处理，有事就给我停）

### 自定义异常

新建一个异常类，必须继承 Exception

- extends Exception ➡️ 表示这是一个受检异常（Checked）
- extends RuntimeException ➡️ 表示这是一个非受检异常（Unchecked）
- 一般都是继承 RuntimeException，因为可以使用默认处理机制，否则每个父类都需要显式地处理编译异常
- super(String)：利用构造函数指定错误信息

### API

Exception 对象可以提供：炸在哪、为啥炸、谁炸的

- getMessage()：获取异常的详细信息，也就是传给构造函数的 message 字符串
- printStackTrace()：把异常的完整堆栈信息输出到控制台
- getCause()：获取异常的根本原因
- toString()：返回异常的字符串表示，一般包含类名和 message



## Wrapper

### 定义

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


### 自动装箱/拆箱

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

### API

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

### String 和其他包装类的转换

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

### Integer 比较

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



## StringBuffer

### 定义

StringBuffer 是 Java 提供的一个可变字符串类，底层用一个字符数组 `char[]` 存储字符内容，并用一个 `count` 字段记录当前字符串的有效长度。

- String 是不可变类（immutable），每次修改字符串都会生成一个新的对象，旧的内容不会被改变
- StringBuffer 是可变类（mutable），所有修改操作都在原有的字符数组上进行，不会新建对象，因此效率更高
- StringBuffer 初始容量是 16，超过后自动扩容

### API

- append(...)：追加字符（会自动转化为字符）
- insert(offset, ...)：在指定位置插入内容
- delete(start, end)：删除指定区间的字符（左闭右开）
- replace(start, end, String str)：替换指定区间内容
- reverse()：反转整个字符串
- toString()：将当前 StringBuffer 转为新的 String 对象
- indexOf(String str)：返回子串首次出现的索引位置，未找到返回 -1
- length()：返回字符串长度
- capacity()：返回字符串容量

### 字符串相关类的比较

| **特性** | **String** | **StringBuffer** | **StringBuilder** |
| ------------ | ---------------- | --------------------- | --------------------- |
| **可变性** | 不可变 | 可变 | 可变 |
| **线程安全** | ✅ 安全（不可变） | ✅ 安全（方法加锁） | ❌ 不安全 |
| **性能** | 最慢 | 较慢 | 最快 |
| **适用场景** | 固定文本内容 | 多线程拼接 | 单线程拼接 |
| **父类** | Object | AbstractStringBuilder | AbstractStringBuilder |
| **是否推荐使用** | 只读文本 | 并发拼接 | 普通拼接 |



## RegExp

### 语法

| **语法** | **含义** | **示例** | **匹配结果示例** |
| -------- | ---------------------------------- | ----------- | ------------------- |
| **a、b、中** | 普通字符，直接匹配本身 | a | "a" |
| **.** | 匹配除换行符外的任意单个字符 | a.c | "abc", "a9c" |
| **[abc]** | 匹配集合内任一字符 | [abc] | "a", "b", "c" |
| **[^abc]** | 匹配集合外任一字符 | [^abc] | "d", "1" |
| **[a-z]** | 匹配 a–z 范围内的字符 | [a-z] | "g" |
| **\d** | 数字（digit，等价于 [0-9]） | \d\d | "12" |
| **\w** | 单词字符（字母/数字/下划线） | \w+ | "hello_123" |
| **\s** | 空白字符（空格、Tab、换行） | a\s+b | "a  b" |
| **^** | 匹配输入的开始位置 | ^abc | "abc123" |
| **$** | 匹配输入的结束位置 | abc$ | "123abc" |
| **\b** | 单词边界 | \bjava\b | "java rocks" |
| **** | 零次或多次重复 | ab* | "a", "ab", "abbb" |
| **+** | 一次或多次重复 | ab+ | "ab", "abbb" |
| **?** | 零次或一次 | ab? | "a", "ab" |
| **{n}** | 恰好 n 次 | a{3} | "aaa" |
| **{m,n}** | 至少 m 次，至多 n 次 | a{2,4} | "aa", "aaa", "aaaa" |
| **`a** | b` | 或 | `cat |
| **(exp)** | 分组，捕获子表达式 | (ab)+ | "abab" |
| **\1、\2…** | 在正则中反向引用第 1、2…个分组结果 | (.)\1 | "aa", "11" |
| **$1、$2…** | 在替换模板中引用分组结果 | (.)\1+ → $1 | "hellooo" → "helo" |

### Pattern

- Pattern 表示一个编译后的正则表达式模版，是不可变的
    - static Pattern compile(String regex)：编译给定的正则表达式为一个 Pattern 对象，用于后续匹配
    - static Pattern compile(String regex, int flags)：带标志位地编译正则表达式
    - static boolean matches(String regex, CharSequence input)：对整个输入序列执行一次完整匹配
    - String pattern()：返回编译此 Pattern 时用的正则表达式字符串
    - int flags()：返回编译时使用的标志位
    - Matcher matcher(String input)：返回 Matcher 对象实例 
- 标志位：
    - Pattern.CASE_INSENSITIVE：忽略大小写
    - Pattern.MULTILINE：多行模式，识别行首和行为，不仅限于输入的首尾
    - Pattern.DOTALL：单行模式，. 会匹配换行符
    - Pattern.UNICODE_CASE：启用 Unicode 方式的大小写折叠
    - Pattern.COMMENTS：允许包含空白和注释
    - Pattern.LITERAL：将整个模式当作字面文本
    - Pattern.UNICODE_CHARACTER_CLASS：使预定义字符类采用 Unicode 而不是 ASCII

### Matcher

Matcher 表示一次“针对某个输入文本”的匹配会话，其绑定了唯一的 Pattern 正则表达式实例和 String 输入字符串实例，内部维护了当前匹配的各种信息

- Matcher matcher(CharSequence input)：基于此 Pattern 创建一个作用于指定输入序列的 Matcher
- boolean matches()：尝试对整个输入序列进行完整匹配
- boolean find()：按顺序搜索下一个匹配子序列，每调用一次向后推进搜索位置
- boolean find(int start)：从指定索引位置开始搜索下一个匹配
- boolean lookingAt()：尝试从输入序列开始位置匹配，但不要求匹配到末尾
- String group(int group)：返回第 group 个捕获组匹配的子序列，不传则为 0
- int groupCount()：返回此 Pattern 中定义的捕获组数量
- int start(int group)：返回第 group 个捕获组匹配的起始索引，不传则为 0
- int end(int group)：返回第 group 个捕获组匹配结束的索引，不传则为 0
- Matcher reset()：重置 Matcher，将其状态恢复到最初
- String replaceAll(String replacement)：将所有匹配项替换为 replacement，并返回替换后的新字符串
- String replaceFirst(String replacement)：将第一个匹配项替换为 replacement，并返回替换后的新字符串

### 案例

```java
public class JieBa {
    public static void main(String[] args) {
        String text = "我...现在在在在...在就...就要要要要..要..学学.学学学....JJJJavaaaaaa";
        System.out.println("原始字符串：" + text);

        // 1. 去掉所有的点
        text = text.replaceAll("[.]+", "");
        System.out.println("去掉点后：" + text);

        // 2. 去掉重复字符：捕获一个字符 (.)
        // \1 表示“第 1 组捕获到的字符”
        // \1+ 表示“该字符重复出现多次”
        // 替换模板 $1 表示“只保留一个”
        text = text.replaceAll("(.)\\1+", "$1");
        System.out.println("去掉重复后：" + text);
    }
}
```