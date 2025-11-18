---
title: JavaScript：变量、作用域和内存
tags:
  - JavaScript
categories:
  - 笔记
cover: /image/js.png
description: JS中变量类型和作用域，并介绍了JS中垃圾回收和内存管理
abbrlink: a242eea0
date: 2024-09-08 15:17:37
---
<meta name="referrer" content="no-referrer"/>

## 1. 数据类型

原始值（primitive）：Undefined、Null、Boolean、Number、String、Symbol
- 大小固定，保存在**栈**
- 复制值的副本

引用值（reference）：Object
- 大小可变，保存在**堆**
- 复制指针，变量指向同一个对象

操作符
- `typeof`：确定值的原始数据类型
- `isinstanceof`：确定值是否是引用数据类型

```js
let a = "dasi";
let b = new Object();
console.log(typeof a); // string
console.log(typeof b); // object
console.log(a instanceof Object); // false 
console.log(b instanceof Object); // true
```

## 2. 执行上下文

作用域：是一个变量和函数的可访问区域，分为全局作用域和局部作用域，其中局部作用域包含函数作用域和块级作用域

作用域链（scope chain）：作用域链的层级是由函数创建的作用域环境形成的，标识符解析是通过沿作用域链逐级搜索标识符名称完成的

不使用var、let、const定义的变量是全局作用域

{% note success flat %}这部分内容学过C的都知道了，本质上就是通过上下文栈的堆叠和转换实现的，不再赘述{% endnote %}

## 3. 垃圾回收

### 3.1 方法

标记清理（Mark-and-Sweep）：标记所有变量，然后将当前处于上下文的变量的标记清除，垃圾回收程序将销毁带标记变量并回收内存
- 局限：清理过程消耗资源，导致程序暂停

引用计数（Reference Counting）：每个对象都维护一个引用计数器，用于记录有多少个引用指向该对象，当对象的引用计数器变为零时，垃圾回收程序将销毁并回收内存
- 局限：维护计数器消耗内存，且无法处理循环引用的问题

## 4. 内存管理

内存限制：分配给浏览器的内存很少
- 原因：出于安全考虑，避免运行大量JS的网页消耗系统内存从而导致操作系统崩溃
- 影响：变量分配、调用栈、一个线程中执行的语句数量

内存泄漏：未能释放不再使用的内存，导致这些内存无法被回收，从而造成程序的内存占用不断增加
- 全局变量：不小心将变量声明为全局变量
- 闭包：外部函数的变量可能被内部函数保持引用
- 定时器和回调：设置的定时器没有被清除，一直被回调

如何减少垃圾回收的频率
- 减少对象创建：避免在高频率操作中频繁创建临时对象，尽量重用对象
- 使用适当的数据结构：选择Map和Set，可以提高内存管理效率
- 优化DOM操作：尽量合并操作，减少重排和重绘