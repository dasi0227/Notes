## 常用的类

## Math

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

## Arrays

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

## System

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

## BigInteger/BigDecimal

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

## Date/Calendar/LocalDate

第一代日期：Date
- new Date()：获取当前时间
- getTime()：获取时间戳
- toString()：将日期对象转为字符串
- before(date)：判断当前对象是否在参数指定时间之前
- after(date)：判断当前对象是否在参数指定时间之后
- setTime(ms)：设置当前对象的时间戳，单位是 ms

第二代日期：Calendar
- Calendar.getInstance()：获取当前时间
- get(...)：获取指定字段的值
- set(...)：设置日期或指定字段的值
- add(...)：对指定字段加减时间
- getTime()：返回 Date 对象

> Calendar.MONTH 的值是 0-11，表示 1-12 月

第三代日期
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

## Properties

用于维护键值对的配置数据，常用于加载和存储 xxx.properties 文件，防止将数据写在程序中，父类是 Hashtable

获取和修改
- String getProperty(String key)：获取键对应的属性，不存在则返回 null
- Object setProperty(String key, String value)：设置/修改属性
- Set<String> stringPropertyNames()：返回键和值均为 String 的属性名称集合，不含默认属性

读取和写入
- void load(InputStream is)：从字节流读取属性，使用 ISO‑8859‑1 编码
- void load(Reader reader)：从字符流读取属性
- void store(OutputStream out, String comments)：以字节流方式写出属性，使用 ISO‑8859‑1 编码，并在首行写入注释 
- void store(Writer writer, String comments)：以字符流方式写出属性，支持任意字符集
- void list(PrintStream out)：将属性列表打印到指定的字节输出流
- void list(PrintWriter out)：将属性列表打印到指定的字符输出流