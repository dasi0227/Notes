---
title: JavaScript：ECMAScript
tags:
  - JavaScript
categories:
  - 笔记
cover: /image/js.png
abbrlink: ac615d30
date: 2024-09-08 13:57:40
description: JavaScript的语言基础是ECMAScript，语义语法继承Java，与C和Python大差不差，不做过多介绍
---
<meta name="referrer" content="no-referrer"/>

## 1. ECMA语法

### 1.1 区分大小写

变量、函数名、运算符以及其他一切东西都是区分大小写

{% note warning flat %}test和Test是不同的{% endnote %}

### 1.2 标识符

- 第一个字符必须是一个字母、下划线或美元符号，其他字符可以是这些加上数字，如$jason、dasi0227,_github
- 使用驼峰命名，如getNumber、dasiNetChina
- 关键字，保留字、true、false和null不能作为标识符

图片

### 1.3 注释

与C一样，当行注释用`//`，多行注释用`/**/`

### 1.4 语句

要求每行代码以`;`结尾

在控制语句中使用代码块`{}`，哪怕只有一条语句！
```js
if (test) {
  console.log(test);
}
```

### 1.5 严格模式

使用：在全局开头或函数开头加上一行`"use strict"`，表示开启严格模式

意义：通过引入更严格的语法规则，可以帮助捕捉潜在的错误并防止一些不良的编程习惯，从而提高代码的安全性和性能

## 2. 变量

### 2.1 var

var的使用规则：
- 声明时，无需明确类型，也无需赋初值
```js
var test;
```
- 声明后，可以改变保存的值，也可以改变值的类型
```js
var test = "dasi";
test = "jason";
test = 10; // 合法，但是不推荐这样做
```
- 用同一个var语句定义的变量不必具有相同的类型
```js
var test1 = "dasi", test2 = 10;
```
- 函数作用域：只在声明它的函数内部使用
```js
function example1() {
  var x = 5;
}
console.log(x); // ReferenceError

function example2() {
  if (true) {
    var x = 10;
  }
  console.log(x); // 输出10
}
```
- 声明提升（hoist）：var变量的声明会自动提升到函数作用域顶部，但不会赋初值
```js
function example() {
  console.log(x); // 声明被提升，但是值是undefined
  var x = 5;      // 在这里才会被赋初值
  console.log(x); // 值是5
}
```

### 2.2 let

let的使用规则
- 块作用域，不允许在一个块内重复声明
```js
function example() {
  if (true) {
    let x = 20;
    console.log(x); // 输出20
    let x = 30; // SyntaxError
  }
  console.log(x); // ReferenceError
}
```
- 暂时性死区：let不会被提升，在声明之前的区域被称为暂时性死区，引用任何后面才声明的变量都会抛出`ReferenceError`
```js
console.log(test1) // undefined
console.log(test2) // ReferenceError
var test1 = 1;
let test2 = 2;
```

let和for循环
- 仅限于循环块内部
```js
for (var i = 0; i < 5; ++i){
  // 循环逻辑
}
console.log(i); // 输出5

for (let j = 0; j < 5; ++j){
  // 循环逻辑
}
console.log(j); // ReferenceError
```
- 迭代变量独立性
```js
for (var i = 0; i < 3; i++) {
  setTimeout(function() {
    console.log(i); // 输出: 3, 3, 3，因 var 的作用域是整个函数，所有回调函数访问的是同一个 i
  }, 0);
}

for (let j = 0; j < 3; j++) {
  setTimeout(function() {
    console.log(j); // 输出: 0, 1, 2，因 let 的作用域是每次循环的块级作用域，回调函数访问的是各自的 j
  }, 0);
}
``` 

### 2.3 const

使用规则
- 声明变量的同时必须初始化，并且不能修改变量的值
```js
const test = 1;
test = 2; // TypeError
```
- 不允许重复声明
```js
const test = 1;
const test = 2; // SyntaxError
```
- 块作用域
```js
const test = 1;
if (true) {
  const test = 2;
  console.log(test); // 2
}
console.log(test); // 1
```
- const和对象：修改对象内部的属性不违反const规则
```js
const person = {
  age: 30
};
person.age = 31; // 正确
person = { age: 25 }; // TypeError
```

{% note success flat %}实践过程中，推荐多使用const，然后是let，最后是var：可以使得变量有明确的作用域、声明位置和不变的值{% endnote %}

## 3. 数据类型

### 3.1 undefined

情况：使用var或let声明一个变量但没有赋值，则变量的初始值就是undefined
```js
let message;
console.log(message == undefined); // true
```

{% note warning flat %}不应该显式地给变量赋值为undefined，字面值undefined通常拿来与null作比较{% endnote %}

### 3.2 null

情况：表示一个空对象指针，指示该变量尚未被分配实际的对象

- typeof：值是object而不是undefined
```js
let test = null;
console.log(typeof test); // object
```
- 占位符
```js
let test = {
  setting1: null,
  setting2: null
};
```

{% note warning flat %}undefined和null都是一个假值，做条件判断时要明确是要检测字面值，还是检测假值{% endnote %}

### 3.3 boolean

布尔值：有两个字面值true和false

{% note warning flat %}
区分大小写：True和False不是布尔值，而是有效的标识符
不同于数值：true不是1，false不是0
{% endnote %}

`Boolean()`转型函数：控制语句中会执行自动转换，将其他值转换为布尔值进行判断
|数据类型|转换为true|转换为false|
|-|-|-|
|String|非空字符串|空字符串""|
|Number|非零数值（包括无穷值）|0和NaN|
|Object|任意对象|null|
|Undefined|不存在|undefined|

### 3.4 number

#### 3.4.1 数值类型

表示形式
- 十进制：直接写出来即可
```js
let intNum = 55;
```
- 八进制：第一个数字必须是0，然后接着是0-7
```js
let octalNum1 = 070; // 表示十进制数56
let octalNum2 = 079; // 不是八进制，而是被当做十进制79
```
- 十六进制：前缀必须是0x，然后是0-9以及a-f（大小写均可）
```js
let hexNum1 = 0xA;  // 表示十进制的10
let hexNum2 = 0x1f; // 表示十进制的31
```
- 浮点值：小数点后必须有一个数字
```js
let floatNum1 = 1.1;
let floatNum2 = 0.1;
let floatNum3 = .1;  // 合法但不规范
let floatNum4 = 1.0; // 被当成1处理 
```
- 科学计数法：一个数值后跟字母e，再加上一个10的幂
```js
let floatNum = 3.125e7;  // 相当于31250000
let floatNum = 1e2;      // 相当于100
```

{% note danger flat %}
严格模式下，八进制的前缀0会判错，应该使用`0o`
永远不要测试某个特定的浮点值，这是计算机基于二进制计算产生的舍入误差导致的天生缺陷！
{% endnote %}

无穷值
- 最值：被保存在`Number.MIN_VALUE`和`Number.MAX_VALUE`
- 无穷值：如果某个计算的数值超过了最值，会被自动转换为正无穷值`Infinity`或负无穷值`-Infinity`
- `isFinite()`：用于判断一个值是否有限大

{% note info flat %}使用`Number.NEGATIVE_INFINITY`和`Number.POSITIVE_INFINITY`可以获得正负无穷值{% endnote %}

NaN：不是数值（Not a Number），可以使用`isNaN()`判断参数是否不是数值
```js
console.log(0/0);   // NaN
console.log(0/1);   // Infinity
console.log(NaN+1); // NaN
console.log(isNaN("string")); // true
```

{% note info flat %}在JavaScript中，出现错误计算不会中断代码执行，而是返回NaN值{% endnote %}

#### 3.4.2 数值转换

- `Number()`
  - true：1
  - false：0
  - null：0
  - undefined：NaN
  - 字符串：如下
```js
let num0 = Number("JS");  // NaN
let num1 = Number("");    // 0
let num2 = Number("01");  // 1
let num3 = Number("12");  // 12
let num4 = Number("1.1"); // 1.1
let num5 = Number("0xf"); // 16 
```
- `parseInt()`：依次检测每个字符，直到字符串末尾，或碰到非数值字符
```js
let num1 = parseInt("123abc"); // 123
let num2 = parseInt("");       // NaN
let num3 = parseInt("0xA");    // 10
let num4 = parseInt("22.5");   // 22
```
- `parseFloat()`：第一次出现小数点是有效的
```js
let num1 = parseFloat("123abc"); // 123
let num2 = parseFloat("0xA");    // 0，只能解析十进制
let num3 = parseFloat("1.2.3");  // 1.2
let num4 = parseFloat("22.5");   // 22.5
let num5 = parseFloat("1.2e3");  // 1200
```

### 3.5 String

#### 3.5.1 字符串

格式：使用双引号、单引号和反引号框起来的16位Unicode字符序列

{% note info flat %}如果要在字符串中使用特殊字符，如换行符、制表符、反斜杠、双引号等，需要在前面加上反斜杠符`\`{% endnote %}

特点
- 不可变的（immutable）：要修改字符串变量的值，必须销毁原始字符串，然后将包含新值的另一个字符串保存到变量
```js
let str = "JAVA";
str = str + "Script"; // 销毁和重新赋值都是自动发生在后台
```
- `length`属性：返回字符串中16位字符的个数
{% note warning flat %}如果字符是双字节字符，则length返回的不是准确的字符数{% endnote %}
- `toString()`和`String()`函数：将一个值转换为字符串
```js
let num = 1;
let str1 = num.toString(); // "1"
let bool = true;
let str2 = bool.toString(); // "true"
let value1 = null;
let value2;
console.log(String(value1)); // "null"
console.log(String(value2)); // "undefined"
```

{% note warning flat %}不能对null和undefined使用toString()，但是可以使用String(){% endnote %}

#### 3.5.2 模版字面量

模版：必须使用反引号`\``，保留换行字符，可以跨行定义字符串，适用于编写HTML模版
```js
let pageHTML = `
<div>
  <a href='#'>
    <span>JavaScript</span>
  </a>
</div>
`
```

{% note warning flat %}模版字面量会保存反引号内的一切字符，因此使用缩进和空格是不一样的，要格外注意格式！{% endnote %}

原始：可以使用`String.raw`函数，获取模版字面量的原始内容
```js
console.log(`\n`);            // 换行
console.log(String.raw`\n`);  // \n
```

#### 3.5.3 字符串插值

方法：在模版字面量中可以使用`${}`插值，所有值会自动使用`toString()`转换为字符串
```js
let value1 = 5;
let value2 = 'second';
let str = `${value} to the ${value2} = ${value1*value1}` // 5 to the second = 25 
```

#### 3.5.4 标签函数

tag function：自动将模版字面量拆分为模版数组和字符串数组
```js
function simpleTag(strings,...expressions) {
  console.log(strings);
  console.log(expressions);
  let result = strings[0];
  for (let i = 0; i < expressions.length; i++) {
    result += expressions[i];
    result += strings[i+1]; 
  }
  return result;
}

let a = 1;
let b = 2;
let result = simpleTag`${a}+${b}=${a+b}`;
console.log(result);
/*
输出：
[ '', '+', '=', '' ]
[ 1, 2, 3 ]
1+2=3
*/
```

{% note warning flat %}
1. 注意参数前要加三个`.`
2. 对于n个插值的模版字面量，传给标签函数的参数个数始终是n，字符串个数始终是n+1
3. 如果模板字面量的开头或结尾是模板，那么strings数组的开头或结尾会是空字符串
{% endnote %}

### 3.6 Symbol

#### 3.6.1 基本用法

Symbol：用于创建唯一的标识符，且每个符号实例都是不可变的，传递字符串参数作为符号描述

{% note info flat %}Symbol数据类型提供了一种创建唯一标识符的机制，非常适合用于避免属性名冲突和定义对象的特殊行为{% endnote %}

`Symbol()`：创建符号
```js
let sym0 = Symbol();
let sym1 = Symbol("description");
let sym2 = Symbol("description");
console.log(sym0);          // Symbol()
console.log(sym1);          // Symbol(description)
console.log(sym1 == sym2);  // false
```

`Symbol.for()`：创建全局符号注册表
```js
const globalSymbol1 = Symbol.for('globalKey');
const globalSymbol2 = Symbol.for('globalKey');
console.log(globalSymbol1 === globalSymbol2); // true
```

`Symbol.keyFor()`：查询全局注册表
```js
let sym1 = Symbol.for("global");
let sym2 = Symbol("not global");
console.log(Symbol.keyFor(sym1)); // global
console.log(Symbol.keyFor(sym2)); // undefined
```
#### 3.6.2 内置符号

用于暴露语言内部行为，开发者可以**访问、模拟或重写**这些行为
- `Symbol.iterator`：定义对象默认迭代器，使对象可以使用`for...of`循环
- `Symbol.aysnIterator`：定义对象异步迭代器，使对象可以使用异步`for-await-of`循环
- `Symbol.hasInstance`：定义操作符`instanceof`，确定一个对象实例是否有原型
- `Symbol.match`：定义`String.prototype.match()`的行为，允许对象定义自己的匹配逻辑
- `Symbol.search`：定义`String.prototype.search()`的行为，允许对象定义如何搜索字符串
- `Symbol.split`：定义`String.prototype.split()`的行为，允许对象定义如何分割字符串
- `Symbol.replace`：定义`String.prototype.replace()`的行为，允许对象定义如何替换字符串

```js
/* 以Symbol.match为例子 */
class myMatch {
  constructor(pattern) {
    this.pattern = pattern;
  }
  [Symbol.match]() {
    return true;
  }
}
// 默认
console.log('JavaScript'.match('dasi'));  // null
// 自定义
console.log('JavaScript'.match(new myMatch('dasi'))); // true
```

### 3.7 Object

对象：存储一组键值对，包含属性和方法，通过new操作符后跟对象类型的名称来创建，可以在创建后随时添加、修改或删除属性和方法
```js
// 对象字面量
const person1 = {
  name: 'dasi',
  age: 20
};
// 利用new Object()
const person2 = new Object();
person2.name = 'dasi';
person2.age = 20;
```

属性
- `constructor`：指向对象的构造函数
```js
function Person(name) {
  this.name = name;
}
const john = new Person('John');
console.log(john.constructor); // [Function: Person]
```
- `Prototype`：用于定义所有由该构造函数创建的对象共享的属性和方法
```js
function Person(name) {
  this.name = name;
}
Person.prototype.sayHello = function() {
  return `Hello, ${this.name}!`;
};
const jason = new Person('jason');
const dasi = new Person('dasi');
console.log(jason.sayHello()); // Hello, jason!
console.log(dasi.sayHello()); // Hello, dasi!
```

方法
- `hasOwnProperty(property)`：检查对象是否具有指定的自有属性
```js
const obj = { a: 1 };
console.log(obj.hasOwnProperty('a')); // true
console.log(obj.hasOwnProperty('b')); // false
```
- `isPropertyOf(object)`：检查当前对象是否在指定对象的原型链上
```js
function Person(name) {
  this.name = name;
}
const john = new Person('John');
const dasi = new Object();
console.log(Person.prototype.isPrototypeOf(john)); // true
console.log(Person.prototype.isPrototypeOf(dasi)); // false
```
- `PropertyIsEnumerable(property)`：检查对象的指定属性是否可枚举
```js
const obj = { a: 1 };
console.log(obj.propertyIsEnumerable('a')); // true
Object.defineProperty(obj, 'b', { value: 2, enumerable: false });
console.log(obj.propertyIsEnumerable('b')); // false
```
- `toString()`：返回对象的字符串表示形式
```js
const obj1 = {
  name: 'John',
  toString() {
    return `Name: ${this.name}`; // 重写
  }
};
const obj2 = {
  name: 'dasi',
};
console.log(obj1.toString()); // Name: John
console.log(obj2.toString()); // [object Object]
```
- `valueOf()`：返回对象的原始值
```js
const obj = {
  name: 'dasi',
  age: 18,
};
console.log(obj.valueOf()); // { name: 'dasi', age: 18 }
```

## 4. 操作符

{% note success flat %}与其他语言相似，不做过多解释和例子{% endnote %}

### 4.1 一元操作符

- 递增`++`和递减`--`：分为前缀和后缀
- 一元加`+`和一元减`-`：表示数值的符号

### 4.2 位操作符

- 按位非`~`（实际上是对数值取反并减1）
- 按位与`&`
- 按位或`|`
- 按位异或`^`
- 左移`<<`：按位补0，保留符号位
- 有符号右移`>>`
- 无符号右移`>>>`

### 4.3 布尔操作符

- 逻辑非`!`
- 逻辑与`&&`
- 逻辑或`||`

### 4.4 乘性操作符

- 乘法`*`
- 除法`/`
- 取模`%`
- 指数`**`

{% note warning flat %}注意Infinity和NaN的情况，但一般情况下用不到，不做过多解释{% endnote %}

### 4.5 加性操作符

- 加法`+`
- 减法`-`

### 4.6 关系操作符

- 小于`<`
- 大于`>`
- 小于等于`<=`
- 大于等于`>=`

### 4.7 相等操作符

- 等于`==`和不等于`!=`：自动转换操作数
- 全等`===`和不全等`!==`：不转换操作数

图片

### 4.8 条件操作符

- `?:`：如果...就...否则...

### 4.9 赋值操作符

- 普通赋值`=`
- 复合赋值`*=`,`+=`,`-=`,`/=`,`<<=`,`>>=`

### 4.10 逗号操作符

- 在一条语句中执行多个操作：`let num1 = 1, num2 = 2;`
- 返回表达式最后一个值：`let num = (1,2,3,4,5)`

## 5. 语句

### 5.1 简单语句

{% note success flat %}这些语句是其他语言中都有的，简单描述{% endnote %}

- `if (condition) {statement1} else {statement2}`：如果就，否则就
- `do {statement} while (expression)`：先执行一次，再测试循环条件
- `while(expression) {statement}`：先测试循环条件，再执行
- `for (initialization; expression; post-loop-expression) {statement}`：先初始化，然后检测循环条件，以及循环一次要执行的操作

### 5.2 for的拓展

- `for (property in expression) {statement}`：用于遍历对象的可枚举属性
- `for (preperty of expression) {statement}`：用于遍历可迭代对象的元素（如数组、字符串、集合、映射等）

### 5.3 循环语句

- `break`：立即退出循环
- `continue`：立即回到循环顶部执行
- `label: {statement}`：标签语句，通过在break和continue后面引用，使得嵌套循环更加清晰

### 5.4 with

`with (expression) {statement}`：将代码的作用域设置为特定的对象

```js
let num1 = object.name;
let num2 = object.age;
// 等价于
with (object) {
  let num1 = name;
  let num2 = age;
}
```
{% note danger flat %}with语句影响性能且难于调试，不建议使用{% endnote %}

### 5.5 switch

每个case相当于如果`expression === value`，则会执行后面的语句，否则执行默认语句

{% note warning flat %}注意，是全等，不执行自动类型转换{% endnote %}

```js
switch (expression) {
  case value1: {
    statement
    break;
  }
  case value2: {
    statement
    break;
  }
  default: {
    statement
  }
}
```

## 6. 函数

`function Name(arg0, arg1) {statement}`：JS的函数不需要指定返回值

{% note info flat %}函数相关将在后面讨论{% endnote %}