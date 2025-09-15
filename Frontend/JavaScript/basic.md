## 数据类型

原始类型：大小固定，保存在栈，复制值
- Undefined：变量声明后未赋值时的默认值，用于区分未初始化状态
- Null：表示空引用的值，明确指示变量指向“无”对象，与 Undefined 明确区分
- Boolean：只有 true 和 false 两个字面量
- Number：任意数值，包括整数、浮点数、NaN、Infinity 等
- String：16 位 Unicode 字符序列，可用单引号、双引号或反引号表示
- Symbol：用于创建的唯一标识，常用作对象属性键

复合类型：大小可变，保存在堆，复制指针
- Object：键值对集合，可动态增删属性
- Array：数组，索引为键并自动维护 length 属性，适合有序数据存储和遍历
- Function：函数，既可作为值传递也可返回
- Date：封装时间戳的对象，提供格式化、算术运算等日期操作方法
- RegExp：用于正则模式匹配的对象

var：声明变量，JS 是动态类型语言，声明时不需要指定类型，由运行时赋值决定
- 函数级作用域
- 可重复声明
- 声明后值与类型均可改变
- 声明会自动提升到函数作用域顶部，访问时不会报错，但是值为 undefined

## 运算符

特殊运算符
- typeof：返回一个字符串表明操作数的原始类型
- instanceof：检查左侧对象是否是右侧的实例

算术
- 模零不会报错，而是 NaN
- 除零不会报错，而是 Infinity

比较
- ==：先做隐式转换再比较，如果两端数据类型不一致，会先转换为 number 再尝试对比，比如 1=="1" 和 1==true 都为真
- ===：严格比较，如果两端数据类型不一致，则直接返回 false

## 分支结构

JS 的 switch 使用严格相等比较，不做类型转换

JS 在 if(expr) 中会将 expr 做隐式转换，不要求一定是 boolean
- ""、0、null、undefined、NaN 都当作 false
- 非空字符串、非空对象、非0数值都当作 true

## 循环结构

for ... in ...：遍历可迭代对象的每个键
for ... of ...：遍历可迭代对象的每个值

## 函数

语法
- function 函数名() {}：函数声明，在解析阶段整体提升，可在定义前调用
- var 函数名 = function() {}：函数表达式
- const 函数名 = () => {}：箭头函数
- 没有访问修饰符
- 没有返回值类型，直接 return 即可，类似 python

用法
- 可以传入任意数量的实参，未提供的参数值为 undefined
- arguments 是函数内部自动可用的类数组，包含所有实参
- 函数可赋值给变量、作为参数传递、作为返回值输出
- JS 不要求声明会抛出的异常类型，统一使用 throw 抛错，try…catch 捕获
- 函数本身也是一种特殊的对象，可以被当作内部逻辑来执行，也可以被 new 用于构造函数来创建新对象

## 对象

区别
- 直接字面量创建，没有类的概念
- 属性和值均可在运行时增删改
- 内部都是键值对的形式，通过 `变量名.属性名/键值` 进行赋值和引用

一个函数在通过 new 调用时，会作为构造函数，JavaScript 会按以下步骤创建并返回对象
1. 创建空对象
2. 将该对象的内部原型指向构造函数的 prototype 
3. 用这新对象作为 this 执行函数体，给它添加属性和方法
4. 若函数没有显式返回对象，则默认返回这个新对象；若显式返回非原始值对象，则返回该对象

```js
// 利用 this 给对象添加属性，作为构造函数
function Person(name) {
  this.name = name;
}
// 在 prototype 上定义方法，所有 Person 实例共享
Person.prototype.sayHi = function() {
  console.log(`Hi, I'm ${this.name}`);
};

const p1 = new Person('Alice');
const p2 = new Person('Bob');
p1.sayHi(); // Hi, I'm Alice
p2.sayHi(); // Hi, I'm Bob
console.log(p1.sayHi === p2.sayHi); // true，同一个函数引用
```

## 常用对象

- Array
  - 利用 [] 或 new Array() 创建，可以声明时传递值进行初始化
  - 元素类型不受限制，可混合不同类型
  - 可跳过下标赋值，中间索引会是 empty
  - length 属性可读写，赋值小于当前长度会截断数组，赋值大于当前长度会填充空位
  - push/pop 末尾删除元素、shift/unshift 头部添加/删除元素
  - forEach(fn) / map(fn) / filter(fn) / reduce(fn, init)：遍历、映射、筛选、归并操作

- Date 
  - 通过 getXXX 方法可以获取时间字段
  - 通过 setXXX 方法可以修改时间字段
  - 底层以 UTC 毫秒数存储，显示时受本地时区与夏令时影响，跨区域处理要用统一时区

- Number
  - toFixed(digits)：四舍五入后保留指定位数小数，返回字符串
  - toExponential(fractionDigits)：科学计数法表示，返回字符串
  - toString(radix)：按指定基数（2–36）输出字符串
  - isXXX(value)：类型检测，如 NaN、Integer、Finite

String 和 Number
- 隐式转换
  - 非 + 运算符（如 -、*、/、%）会先将字符串转换为数值再运算
  - + 若运算符的任一操作数为字符串，则执行字符串拼接，其它操作数会转换为字符串
- 显示转换
  - 一元加号 +str 字符串转成数字，非数值字符串得到 NaN，空串得到 0
  - 使用 Number(str)：字符串转成数字，非数值字符串得到 NaN，空串得到 0
  - String(num)：把数字转成字符串
- 利用 API
  - Number.parseInt：从字符串头部解析整数直至遇到非数字字符，可指定基数
  - Number.parseFloat：从字符串头部解析小数直至遇到非数字字符

## RegExp

正则表达式字面量：/pattern/flags

常用标志
- g：全局匹配，每次调用 exec，都会从上一次结束的位置继续搜索，直到返回 null
- i：忽略大小写
- m：多行模式
- u：开启 Unicode 支持，处理中文字符和Emoji
- s：点号.匹配包括换行在内的所有字符

属性
- test(str)：返回 boolean，表示是否匹配
- exec(str)：返回 match 对象，存储的是匹配结果
- re.source：获取模式
- re.flags：获取标志

常用正则表达式
- 用户名（4–16 位，允许字母、数字及下划线）：/^[A-Za-z0-9_]{4,16}$/
- 密码（8–16 位，至少包含字母和数字）：/^(?=.*[A-Za-z])(?=.*\d)[A-Za-z\d]{8,16}$/
- 邮箱：/^[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}$/
- URL：/^(https?:\/\/)[\w.-]+(:\d+)?(\/[^\s]*)?$/

## JSON

JavaScript Object Notation，一种轻量级、基于文本的数据交换格式，本质就是嵌套键值对
- 跨平台互通：几乎所有主流语言都内建或提供成熟库来读写 JSON
- 轻量且高效：相比 XML 等格式，JSON 语法更简洁，传输和解析开销更小
- 人机双友好：JSON 文本结构层次清晰，使用 {} 和 [] 表示对象与数组

基本数据类型
- 字符串：必须由双引号 “” 包裹，注意只能是双引号！
- 数值：可以是整数或浮点数，不需要引号
- 布尔值：只有 true 和 false 两个值
- null：表示空值或无数据

复合数据类型
- 对象：由一对大括号 {} 包裹，内部由零个或多个键值对构成，键必须是字符串，键和值之间用冒号：分隔，每个键值对之间用逗号，分隔（注意最后一个键值对不需要额外的逗号）
- 数组：由一对方括号 [] 包裹，内部包含零个或多个元素，各元素之间用逗号，分隔，元素可以是任意 JSON 支持的数据类型

通常最外层表示一个对象，内层键值对表示若干属性，数组表示属性的若干取值
```js
var personJson = '{"name":"dasi", "age":21, "gf":{"name":"didi"}, "hobby":["basketball", "music", "movie"]}'
var person = JSON.parse(personJson)
console.log(personJson)
console.log(person.name)
console.log(person.age)
console.log(person.gf)
console.log(person.hobby)
```

## XML

XML（Extensible Markup Language）可扩展标记语言，是基于文本的、用于描述数据结构和存储信息的通用标记语言
- 配置文件：Java 的 web.xml、Maven 的 pom.xml、Spring 的 applicationContext.xml
- 文档交换与订阅：博客、新闻聚合、播客等通过 RSS/Atom XML 源推送动态内容，消费端只需解析标签就能获得标题、摘要、链接等信息
- Web 服务：用 XML 封装请求和响应报文，并结合 WSDL 定义接口和数据类型，实现跨语言、跨平台调用

语法规则
- 文档声明：`<?xml version="1.0" encoding="UTF-8"?>`
  - version：XML 版本，通常为 1.0
  - encoding：字符编码，通常为 UTF-8 或 GBK
- 唯一根元素：整个 XML 必须且只能有一个最外层元素
- 标签对：所有元素必须成对出现，既有开始标签和结束标签
- 嵌套：父标签内的子标签先闭合
- 严格区分标签和属性名的大小写：`<Item>` 和 `<item>` 不是同一个元素
- 属性书写：必须放在开始标签内，为名–值对形式，属性名不能重复，值用单引号或双引号包裹
- 实体引用：特殊字符（<、& 等）须用 &lt;、&amp; 等实体替代

约束：保证文件的格式一致，从而使得文件可以跨平台跨系统读取，同时会校验非法标签、缺失字段或取值超标，提前拦截错误数据
- 良好结构约束（Well-formedness）：遵循上面的语法规则 
- XSD 约束
  - 结构约束：哪些元素可以出现，以及它们出现的顺序和次数
  - 数据约束 ：元素或属性的取值类型、以及取值的范围、长度、模式或枚举
  - 身份约束：哪些字段必须唯一，哪些字段相互之间必须引用对应关系


Dom4j 使用
```java
public class TestDom4j {
    public static void main(String[] args) throws DocumentException {
        // 通过类加载器获得指向字节码根路径下的指定文件的输入流
        InputStream resourceAsStream = TestDom4j.class.getClassLoader().getResourceAsStream("jdbc.xml");
        // 通过输入流获得配置文件，解析成一个 document 对象
        SAXReader saxReader = new SAXReader();
        Document document = saxReader.read(resourceAsStream);
        // 从 document 对象上获取配置文件中的元素节点
        Element rootElement = document.getRootElement();
        System.out.println(rootElement.getName());
        // 获取元素下的子元素
        List<Element> elements = rootElement.elements();
        for (Element element : elements) {
            System.out.println("\t" + element.getName());
            // 从元素上获取属性
            Attribute attribute = element.attribute("id");
            if (attribute != null) {
                System.out.println("\t\t" + attribute.getName() + "=" + attribute.getValue());
            }
            // 继续读取子元素
            List<Element> subelements = element.elements();
            for (Element subelement : subelements) {
                System.out.println("\t\t" + subelement.getName() + ":" + subelement.getText());
            }
        }
    }
}
```