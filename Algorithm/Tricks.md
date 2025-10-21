# Tricks



   * [集合](#集合)
      * [排序](#排序)
      * [移除元素](#移除元素)
   * [数组](#数组)
      * [排序](#排序)
      * [获取最大值](#获取最大值)
   * [字符串](#字符串)
      * [StringBuffer 的 API](#stringbuffer-的-api)



## 集合

### 排序

```java
Collections.sort(list);
```

### 移除元素

```java
// 如果直接写数字，移除的是索引对应的元素，会返回元素值
int num = list.remove(2); 
// 如果显式传递 Integer 对象，会移除第一个相等的值，返回是否删除成功
boolean success = list.remove(Integer.valueOf(2));
```



## 数组

### 排序

```java
// 升序排序整个数组
Arrays.sort(arr);
// 降序排序

// 区间排序，左闭右开
Arrays.sort(arr, fromIndex, toIndex);
```

### 获取最大值

```java
int max = Arrays.stream(arr).max().getAsInt();
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





