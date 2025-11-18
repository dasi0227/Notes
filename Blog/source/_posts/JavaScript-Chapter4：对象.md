---
title: JavaScript：对象
tags:
  - JavaScript
categories:
  - 笔记
cover: /image/js.png
description: 解释了JS中对象的基本含义，以及JS自带对象的属性和方法
abbrlink: b7ba4348
date: 2024-09-08 15:29:26
---
<meta name="referrer" content="no-referrer"/>

## 1. 引用值

引用值：又称对象，是某个特定引用类型的实例

引用类型：是把数据和功能组织到一起的结构

对象由特性（attribute）构成
- 如果特性是函数，它将被看作对象的方法（method）
- 如果特性是值（原始和引用），它被看作对象的属性（property）

ECMAScript是面向对象的
- 封装：把相关的信息存储在对象中的能力
- 聚集：把一个对象存储在另一个对象内的能力
- 继承：由另一个类得来类的属性和方法的能力
- 多态：编写能以多种方法运行的函数的能力

## 2. Date

### 2.1 日期格式

- 短日期：`"月/日/年"`，如"2/27/2004"

- 长日期：`"月名 日, 年"`，如"Feb 27, 2004"

- 完整日期：`"周几 月名 日 年 时:分:秒 时区"`，如"Fri Feb 27 2004 00:00:00 GMT+0800"

- ISO：`"YYYY-MM-DDThh:mm:ss:sssZ"`，如"2004-02-27T00:00:00:000Z"
- 日期和时间通过大写字母T来分隔
- UTC时间通过大写字母Z来定义

{% note info flat %}UTC（Universal Time Coordinated）/GMT (Greenwich Mean Time)：具有相同的时间值，作为世界标准时间{% endnote %}

### 2.2 日期初始化方法

- `Date.parse(string)`：传递上述日期格式的字符串

{% note info flat %}
1. 如果直接把string传给构造函数，后台实际上是通过调用Date.parse实现的
2. 如果直接把数值传给构造函数，后台实际上是创建一个1970年1月1日加上传参毫秒的新日期对象
3. 一天是86400000毫秒
{% endnote %}

- `Date.UTC(年, 月数, 日, 时, 分, 秒, 毫秒)`：依次传递数值
  - 只有年和月是必须的
  - 不提供日则默认是1日，其他默认是0
  - 月数是从零开始计数的，也就是1月是0，12月是11

### 2.3 日期设置和获取方法

- `setFullYear(),setMonth(),setDate(),setHours(),setSeconds()`：设置日期的某个部分（月从0开始）

- `getFullYear(),getMonth(),getDate(),getHours(),getSeconds()`：获取日期的某个部分

- `setTime()`：传递数值，表示从1970年1月1日至今的毫秒数

- `now()`：获取从1970年1月1日至今的毫秒数

### 2.4 继承方法

- `toString()`：将日期转换为当前时区的字符串
- `toUTCString()`：将日期转换为UTC下的字符串
- `valueOf()`：将日期自动转换为时间戳

```js
let a = new Date("Feb 27, 2004");
console.log(a.toString());    // Fri Feb 27 2004 00:00:00 GMT+0800 (中国标准时间)
console.log(a.toUTCString()); // Thu, 26 Feb 2004 16:00:00 GMT
console.log(a.valueOf());     // 1077811200000
```

## 3. RegExt

### 3.1 正则表达式语法

`/pattern/flags`
- 模式串：字面量字符串
  - `.`：代替任何字符，如`/a.c/`是匹配 "aXc"、"a7c" 等
  - `[]`：匹配括号内的任意一个字符，如`/[abc]/`是匹配 "a"、"b" 或 "c"
  - `-`：匹配字符范围，如`/[a-z]/`是匹配小写字母
  - `+`：匹配前一个字符一次或多次，如`/a+/`是匹配 "a"、"aa"、"aaa" 等
  - `*`：匹配前一个字符零次或多次，如`/a*/`是匹配 ""、"a"、"aa" 等
  - `?`：匹配前一个字符零次或一次，如`/a?/`是匹配 "" 或 "a"
  - `{n,m}`: 匹配前一个字符n到m次，如`/a{2,4}/`是匹配 "aa"、"aaa" 或 "aaaa"
  - `^`：匹配字符串的开始，如`/^abc/`是匹配以 "abc" 开头的字符串
  - `$`：匹配字符串的结尾，如`/abc$/`是匹配以 "abc" 结尾的字符串
  - `|`：匹配任意一个字符串，如`/abc|def/`是匹配 "abc" 或 "def"
  - `(?=)`：匹配仅当后面跟着指定内容，如`/a(?=b)/`是匹配 "a" 仅当后面跟着 "b"
  - `(?!)`：匹配仅当后面不跟着指定内容，如`/a(?!b)/`是匹配 "a" 仅当后面不跟着 "b"
  - `\d`：匹配任何数字
  - `\w`：匹配任何字母、数字或下划线
- 标志位：控制搜索行为
  - `g`：全局，即查找全部内容而不是第一次匹配到就结束
  - `i`：不区分大小写
  - `m`：多行，即查找到一行末尾不会停止
  - `y`：粘附，只查找lastIndex开始及之后的字符串
  - `u`：启用Unicode匹配
  - `s`：dotAll，表示元字符匹配任何字符

### 3.2 属性

- `global, ignoreCase, unicode, sticky, lastIndex, multiline, dotAll`：查找是否有标记
- `source`：字面量字符串
- `flags`：标记字符串

```js
let pattern = /\[Dasi\]net\.cn/gi;
console.log(pattern.global);    // true
console.log(pattern.unicode);   // false
console.log(pattern.source);    // \[Dasi\]net\.cn
console.log(pattern.flags);     // gi
```

### 3.3 方法

`exec()`：只接受文本串参数，若有匹配项则返回包含第一个匹配信息的数组，否则返回null
- index：起始位置
- input：文本串

```js
const pattern = /.at/g;
const str = "cat, bat, sat";
let result;
while ((result = pattern.exec(str)) !== null) {
  console.log(result.index); // 依次输出0,5,10
  console.log(result[0]);    // 依次输出cat,bat,sat
}
```

`test()`：只测试模式是否匹配，不考虑匹配的内容
```js
const pattern = /\d{3}-\d{2}-\d{1}/;
const str1 = "000-00-0";
const str2 = "00-000-0";
console.log(pattern.test(str1)); // true
console.log(pattern.test(str2)); // false
```

### 3.4 构造函数属性

RegExt的属性
- `input`：最后搜索的字符串
- `lastMatch`：最后匹配的文本
- `lastParen`：最后匹配的捕获组
- `leftContent`：input字符串出现在lastMatch前面的文本
- `rightContent`：input字符串出现在lastMatch后面的文本

```js
const text = "Hello-i-am-dasi,welcome-to-my-blog";
const pattern = /(.)elcome/g;
if (pattern.test(text)) {
  console.log(RegExp.input); // Hello-i-am-dasi,welcome-to-my-blog
  console.log(RegExp.leftContext);// Hello-i-am-dasi,
  console.log(RegExp.rightContext); // -to-my-blog
  console.log(RegExp.lastParen); // w
  console.log(RegExp.lastMatch); // welcome
}
```

## 4. 原始值包装类型

特性：在执行方法和属性时将Boolean，Number和String视为对象，它们具有各自原始类型对应的特殊行为

```js
let s1 = "dasi";
let s2 = s1.substring(1); // asi
// 等价于
let s1 = new String("dasi");
let s2 = s1.substring(1);
s1 = null;
```

注意区分转型函数和构造函数
```js
let str = "25";
let num = Number(str);
let obj = new Number(str);
console.log(typeof num); // number
console.log(typeof obj); // object
```

一般用的比较多的是String，使用方法可以在使用时候参考教程，与C++中有关string函数差不多

| 方法                   | 描述                                                   |
|------------------------|--------------------------------------------------------|
| `charAt()`             | 返回指定位置处的字符。                                 |
| `charCodeAt()`         | 返回指定位置处字符编码。                               |
| `codePointAt()`        | 返回字符串中索引（位置）处的 Unicode 值。             |
| `concat()`             | 返回两个或多个连接的字符串。                           |
| `constructor`          | 返回字符串的构造函数。                                 |
| `endsWith()`           | 返回字符串是否以指定值结尾。                           |
| `fromCharCode()`       | 将 Unicode 值作为字符返回。                             |
| `includes()`          | 返回字符串是否包含指定值。                             |
| `indexOf()`           | 返回值在字符串中第一次出现的位置。                     |
| `lastIndexOf()`       | 返回值在字符串中最后一次出现的位置。                   |
| `length`               | 返回字符串中的字符数。                                 |
| `localeCompare()`      | 使用基于本地的顺序来比较字符串。                       |
| `match()`              | 在字符串中搜索值或正则表达式，并返回匹配项。           |
| `prototype`            | 允许您向对象添加属性和方法。                           |
| `repeat()`             | 返回拥有多个字符串副本的新字符串。                     |
| `replace()`            | 在字符串中搜索值或正则表达式，并返回替换值的字符串。   |
| `search()`             | 检索字符串中与正则表达式匹配的子串。                   |
| `slice()`              | 提取字符串的一部分并返回新字符串。                     |
| `split()`              | 将字符串拆分为子字符串数组。                           |
| `startsWith()`         | 检查字符串是否以指定字符开头。                         |
| `substr()`             | 从字符串中抽取子串，该方法是 `substring()` 的变种。     |
| `substring()`          | 从字符串中抽取子串。                                   |
| `toLocaleLowerCase()`  | 使用主机的语言环境返回转换为小写字母的字符串。         |
| `toLocaleUpperCase()`  | 使用主机的语言环境返回转换为大写字母的字符串。         |
| `toLowerCase()`        | 返回转换为小写字母的字符串。                           |
| `toString()`           | 将字符串或字符串对象作为字符串返回。                 |
| `toUpperCase()`        | 返回转换为大写字母的字符串。                           |
| `trim()`               | 返回删除了空格的字符串。                               |
| `trimEnd()`            | 返回从末尾删除空格的字符串。                           |
| `trimStart()`          | 返回从开头删除空格的字符串。                           |
| `valueOf()`            | 返回字符串或字符串对象的原始值。                     |

## 5. 内置对象

### 5.1 Global

事实上，JS中不存在全局变量或全局函数，它们实际上都是**Global的属性和方法**

- URL编码：`encodeURIComponent()`和`decodeURIComponent()`，用于编码统一资源标识符，以便浏览器可以识别
```js
let url = "https://达斯Blog.net.cn/";
console.log(encodeURI(url)); // https://%E8%BE%BE%E6%96%AFBlog.net.cn/
console.log(encodeURIComponent(url)); // https%3A%2F%2F%E8%BE%BE%E6%96%AFBlog.net.cn%2F
```

{% note warning flat %}
- encodeURI：不会编码URL组件的特殊字符，如冒号、斜杠、问号、井号
- encodeURIComponent：编码一切非标准字符
{% endnote %}

- `eval()`：传递ECMAScript字符串，并执行
```js
eval(console.log("dasi"));
// 等价于
console.log("dasi");
```

- window对象：浏览器将window当做了Global对象的代理，所有全局作用域的变量和函数都是window的属性

{% note warning flat %}ECMAScript没有直接访问Global对象的方式！{% endnote %}

### 5.2 Math

- 属性：一些数学中的特殊值
  - `Math.E`：自然对数
  - `Math.PI`：圆周率
- 方法
  - `Math.min`：求最小值
  - `Math.max()`：求最大值
  - `Math.ceil()`：向上舍入
  - `Math.floor()`：向下舍入
  - `Math.round()`：四舍五入
  - `Math.random()`：得到一个0-1的随机数