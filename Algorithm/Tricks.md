# Tricks



   * [集合](#集合)
      * [排序元素](#排序元素)
      * [移除某个指定元素](#移除某个指定元素)
      * [移除所有符合条件元素](#移除所有符合条件元素)
      * [初始化列表](#初始化列表)
      * [截取子列表](#截取子列表)
   * [数组](#数组)
      * [排序](#排序)
      * [获取最大值](#获取最大值)
      * [截取子数组](#截取子数组)
      * [打印数组](#打印数组)
   * [字符串](#字符串)
      * [StringBuffer 的 API](#stringbuffer-的-api)



## 集合

### 排序元素

```java
Collections.sort(list);
```

### 移除某个指定元素

```java
// 如果直接写数字，移除的是索引对应的元素，会返回元素值
int num = list.remove(2); 
// 如果显式传递 Integer 对象，会移除第一个相等的值，返回是否删除成功
boolean success = list.remove(Integer.valueOf(2));
```

### 移除所有符合条件元素

```java
list.removeIf(Objects::isNull); // 移除所有 null
list.removeIf(s -> s.isEmpty()); // 移除所有空字符串
list.removeIf(x -> x < 0); // 移除所有负数
list.removeIf(name -> name.length() < 5); // 移除所有长度小于 5 的元素
```

### 初始化列表

```java
// 用列表
List<Integer> list = new ArrayList<>(list2);
// 用数组
List<Integer> list = new ArrayList<>(Arrays.asList(arr));
// 用数据
List<Integer> list = new ArrayList<>(Arrays.asList(1, 2, 3, 4));
```

### 截取子列表

```java
List<Integer> subList = new ArrayList<>(list.subList(1, 4));
```



## 数组

### 排序

```java
// 整体排序
Arrays.sort(arr);
// 区间排序
Arrays.sort(arr, fromIndex, toIndex);
```

### 获取最大值

```java
int max = Arrays.stream(arr).max().getAsInt();
```

### 截取子数组

```java
int[] subArr = Arrays.copyOfRange(arr, 1, 4);
```

### 打印数组

```java
// 一维数组
System.out.println(Arrays.toString(arr));
// 二维数组
System.out.println(Arrays.deepToString(matrix));
```



## 字符串

### StringBuffer 的 API

```java
// 构造
StringBuffer sb = new StringBuffer(str);
// 转换
String s = sb.toString(); 
// 长度
int len = sb.length();  
// 获取
char c = sb.charAt(0);   
// 截取
String sub = sb.substring(start, end);
// 修改
sb.setCharAt(0, 'A');   
// 追加
sb.append("world"); 
// 插入
sb.insert(0, "Hello "); 
// 删除区间
sb.delete(2, 5); 
// 删除字符
sb.deleteCharAt(1); 
// 清空
sb.setLength(0);
// 替换区间
sb.replace(0, 5, "HELLO");
// 反转
sb.reverse();
```

