# JavaScript



   * [语法](#语法)
      * [数据类型](#数据类型)
      * [运算符](#运算符)
      * [分支结构](#分支结构)
      * [循环结构](#循环结构)
      * [函数](#函数)
      * [对象](#对象)
      * [常用对象](#常用对象)
      * [RegExp](#regexp)
   * [传输格式](#传输格式)
      * [JSON](#json)
      * [XML](#xml)
   * [BOM](#bom)
      * [定义](#定义)
      * [对象结构](#对象结构)
      * [window](#window)
      * [document](#document)
      * [location](#location)
      * [history](#history)
      * [navigator](#navigator)
      * [screen](#screen)
      * [console](#console)
      * [localStorage/sessionStorage](#localstoragesessionstorage)
   * [DOM](#dom)
      * [定义](#定义)
      * [DOM 树](#dom-树)
      * [获取元素](#获取元素)
      * [修改元素](#修改元素)
   * [Event](#event)
      * [定义](#定义)
      * [事件类型](#事件类型)
      * [事件模型](#事件模型)
   * [Ajax](#ajax)
      * [定义](#定义)
      * [XMLHttpRequest](#xmlhttprequest)
   * [ECMAScript 6](#ecmascript-6)
      * [let 和 const](#let-和-const)
      * [模板字符串](#模板字符串)
      * [解构赋值](#解构赋值)
      * [箭头函数](#箭头函数)
      * [rest 和 spread](#rest-和-spread)
      * [模块化](#模块化)



## 语法

### 数据类型

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

### 运算符

特殊运算符

- typeof：返回一个字符串表明操作数的原始类型
- instanceof：检查左侧对象是否是右侧的实例

算术

- 模零不会报错，而是 NaN
- 除零不会报错，而是 Infinity

比较

- ==：先做隐式转换再比较，如果两端数据类型不一致，会先转换为 number 再尝试对比，比如 1=="1" 和 1==true 都为真
- ===：严格比较，如果两端数据类型不一致，则直接返回 false

### 分支结构

JS 的 switch 使用严格相等比较，不做类型转换

JS 在 if(expr) 中会将 expr 做隐式转换，不要求一定是 boolean

- ""、0、null、undefined、NaN 都当作 false
- 非空字符串、非空对象、非 0 数值都当作 true

### 循环结构

for ... in ...：遍历可迭代对象的每个键
for ... of ...：遍历可迭代对象的每个值

### 函数

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

### 对象

区别

- 直接字面量创建，没有类的概念
- 属性和值均可在运行时增删改
- 内部都是键值对的形式，通过 ` 变量名.属性名/键值 ` 进行赋值和引用

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

### 常用对象

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

### RegExp

正则表达式字面量：/pattern/flags

常用标志

- g：全局匹配，每次调用 exec，都会从上一次结束的位置继续搜索，直到返回 null
- i：忽略大小写
- m：多行模式
- u：开启 Unicode 支持，处理中文字符和 Emoji
- s：点号.匹配包括换行在内的所有字符

属性

- test(str)：返回 boolean，表示是否匹配
- exec(str)：返回 match 对象，存储的是匹配结果
- re.source：获取模式
- re.flags：获取标志

常用正则表达式

- 用户名（4–16 位，允许字母、数字及下划线）：/^[A-Za-z0-9_]{4,16}$/
- 密码（8–16 位，至少包含字母和数字）：/^(?=.\*[A-Za-z])(?=.*\d)[A-Za-z\d]{8,16}$/
- 邮箱：/^[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}$/
- URL：/^(https?:\/\/)[\w.-]+(:\d+)?(\/[\^\s]*)?$/



## 传输格式

### JSON

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

### XML

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



## BOM

### 定义

BOM（Brower Object Model）浏览器提供的一组全局对象 API，用于操控浏览器而非页面内容

- 窗口与标签页管理：打开、关闭或重定位窗口/标签页，调整尺寸与位置，控制页面滚动
- URL 与历史导航：读取或修改地址栏，在不刷新页面的情况下增删历史记录，实现前进、后退、跳转等行为
- 环境检测：获取浏览器类型、版本、操作系统及网络状态，查询屏幕分辨率、色深和可用工作区大小
- 定时与异步执行：延迟执行一次性任务或周期性重复执行，用于动画、轮询、节流等场景
- 标准对话框：alert、confirm、prompt 等阻塞式对话框，用于提示、确认或简单输入
- 客户端存储：读写 Cookie，实现轻量级关键信息存储（可配合 Web Storage 使用）
- 跨窗口/跨域通信：在同源或不同源的窗口、iframe 之间安全地传递消息
- 调试与开发辅助：通过 console 对象进行日志输出、性能计时和断言

### 对象结构

- window：全局根对象，包含所有 BOM 成员与全局变量
- document：目前解析的 html 文档
- location：URL 管理与跳转
- history：浏览历史记录控制
- navigator：浏览器及平台信息
- screen：屏幕分辨率与可用区域信息
- console：开发者工具的控制台
- localStorage：本地数据持久化键值存储
- sessionStorage：本地数据会话级键值存储

### window

- alert(message)：显示一个带“确定”按钮的消息框，阻塞后续脚本执行，用于提示信息
- confirm(message)：显示带“确定/取消”按钮的对话框，返回布尔值 true/false，常用于用户确认操作
- prompt(message)：显示带输入框和“确定/取消”按钮的对话框，返回用户输入的字符串或 null，常用于获取简单文本输入
- open(url)：打开新窗口或标签页，可指定大小、位置和界面元素
- close()：关闭当前窗口（仅当窗口由脚本打开时有效）
- scrollTo(x, y) / scrollBy(dx, dy)：编程方式滚动页面到指定位置或按相对位移滚动
- setInterval(fn, interval)：每隔 interval 毫秒重复执行一次回调函数 f，返回一个定时器 ID，可通过 clearInterval(id) 停止后续执行
- setTimeout(fn, delay)：在延迟 delay 毫秒后仅执行一次回调函数 fn，返回一个定时器 ID，可通过 clearTimeout(id) 取消未到期的执行

### document

- document.getElementById(id)：按 ID 获取元素
- document.querySelector(selector)：按 CSS 选择器获取首个元素
- document.createElement(tagName)：创建新节点
- document.addEventListener(type, handler)：绑定全局事件
- document.removeEventListener(type, handler)：解绑全局事件

### location

- location.href：读取/设置当前 URL
- location.assign(url)：加载新页面（保留历史）
- location.replace(url)：替换当前页面（不留历史）
- location.reload(force)：刷新页面，force=true 可跳过缓存

### history

- history.back()：后退
- history.forward()：前进
- history.go(n)：相对跳转（可正可负） 
- history.pushState(state, title, url)：无刷新添加历史记录

### navigator

- navigator.userAgent：浏览器/平台标识
- navigator.language：首选语言 
- navigator.onLine：网络在线状态 
- navigator.cookieEnabled：Cookie 是否可用

### screen

- screen.width / screen.height：设备屏幕分辨率
- screen.availWidth / screen.availHeight：可用工作区大小
- screen.colorDepth：色深

### console

- console.log(...data)：普通日志
- console.warn(...data) / console.error(...data)：警告/错误输出
- console.time(label) / console.timeEnd(label)：性能计时
- console.table(obj)：以表格形式展示数组或对象

### localStorage/sessionStorage

- localStorage/sessionStorage.setItem(key, value)：存储字符串
- localStorage/sessionStorage.getItem(key)：读取值，若无返回 null
- localStorage/sessionStorage.removeItem(key)：删除对应条目
- localStorage/sessionStorage.clear()：清空所有存储

> sessionStorage 存储内容的生命周期仅限于当前标签页/窗口



## DOM

### 定义

DOM（Document Obejct Model）将 HTML/XML 文档抽象为一棵可编程的节点树，桥接文档结构与脚本行为，使页面内容可动态读取与更新

- 动态交互基础：脚本可增删改节点及其属性、样式，实时响应用户操作，构建单页应用和交互式体验
- 跨平台一致性：W3C 标准规范，各大浏览器实现同一模型，保障脚本一次编写、处处可用
- 分离关注点：将内容（HTML）、样式（CSS）与行为（JS）解耦，提升维护性与团队协作效率
- 内容与结构抽象：把标签、属性、文本都当作“节点”对象，统一接口，屏蔽底层解析差异
- 可扩展性：支持事件绑定、节点遍历和生命周期监控等高级功能，为现代框架（如 React/Vue）提供底层支撑

> BOM 专注于浏览器行为，而 DOM 专注于文档行为，实际上 DOM 属于 BOM

### DOM 树

- 根节点（document）：代表整个 HTML 文档，是 DOM 树的最顶层节点，可通过 document.documentElement 访问 <html> 元素
- 元素节点（element）：对应每个 HTML 标签
- 属性节点（attribute）：每个元素的键值对属性
- 文本节点（text）：元素内的纯文本内容以及元素标签之间的空白字符（空格、制表符、换行符）
- 注释节点（comment）：对应 HTML 注释 \<!-- 注释内容 -->

![img.png](https://dasi-blog.oss-cn-guangzhou.aliyuncs.com/Java/202509160853060.png)

### 获取元素

直接获取

- 按照 ID 获取：document.getElementById(id)，返回 Element 或 null，注意这里 Element 不是复数形式，因为 id 唯一
- 按照类名或许：document.getElementByClassName(className)，返回动态更新的 HTMLCollection
- 按照 name 属性获取：document.getElementByName(name)，返回静态的 NodeList
- 按照 HTML 标签名获取：document.getElementByTagName(tagName)，返回动态更新的 HTMLCollection

间接获取

- 根据子元素获取父元素：element.parentElement，返回一个 Element 或 null
- 根据父元素获取子元素集合：element.children，返回动态更新的 HTMLCollection
- 根据父元素获取第一个子元素：element.firstElementChild，返回 Element 或 null
- 根据父元素获取最后一个子元素：element.lastElementChild，返回 Element 或 null
- 根据当前元素获取前一个兄弟元素：element.previousElementSibling，返回 Element 或 null
- 根据当前元素获取后一个兄弟元素：element.nextElementSibling，返回 Element 或 null
- 根据当前元素获取所有子节点：element.childNodes，返回静态的 NodeList，这里不一定是元素节点

### 修改元素

内容修改

- 修改纯文本：element.textContent
- 修改子标签：element.innerHTML
- 修改属性：element.属性名
- 修改样式：element.style.样式名
- 插入元素
    - 添加到末尾：element.append(node)
    - 添加到开头：element.prepend(node)
    - 添加到某个子节点之前：element.insertBefore(newNode, referenceNode)
- 删除元素
    - 父节点指定移除子节点：element.removeChild(child)
    - 移除自己：element.remove()
- 替换元素
    - 父节点指定替换子节点：element.replaceChild(newNode, oldNode)
    - 替换自己：element.replaceWith(newNode)



## Event

### 定义

事件：是浏览器或用户交互触发的行为

- 利用元素的属性绑定：onXXX，如 onclick, onchange 等
- 通过 DOM 编程动态绑定：DOM0，DOM2

事件对象 event，承载了本次交互事件的所有上下文信息，常用属性／方法包括

- type：事件类型
- target：触发事件的最初元素
- currentTarget：当前执行处理函数的元素
- clientX/clientY：如果是鼠标事件，可以获取鼠标的视口坐标
- button：如果是鼠标事件，可以获取按键编号
- key：如果是键盘事件，可以获取按键值
- code：如果是键盘事件，可以获取按键编码
- timeStamp：事件发生的时间戳（毫秒）
- preventDefault()：阻止浏览器默认行为，如链接跳转和表单提交
- stopPropagation()：阻止事件继续冒泡／捕获

### 事件类型

鼠标事件

- click：在目标元素上按下并释放主按钮时触发
- dblclick：在系统双击阈值内连续两次触发 click 后触发
- mousedown：按下任意鼠标按钮时即时触发
- mouseup：释放鼠标按钮时触发
- mousemove：鼠标指针在元素内移动时持续触发，频率高
- contextmenu：在目标元素上点击次按钮或触发上下文菜单快捷键时触发

键盘事件

- keydown：按下任意键时立即触发，可用于检测按键开始
- keyup：释放按键时触发，可用于检测按键结束

表单事件

- input：用户每次修改 \<input>、\<textarea> 或可编辑区域的值时即时触发
- change：元素值更改并失去焦点后触发，常用于选项或文本框的最终确认
- focus：元素获得焦点时触发，可用于高亮或校验前准备
- blur：元素失去焦点时触发，可用于即时校验或样式恢复
- submit：表单提交时触发，常用 event.preventDefault() 阻止默认提交行为
- reset：表单重置时触发，可用于恢复自定义状态或清理副作用

全局事件

- load：在所有资源（HTML、CSS、图片、脚本）加载完毕后触发一次，用于初始化全局逻辑

### 事件模型

| **特性** | **OM0** | **OM2** | **OM3** |
| ---------------- | -------------------------- | ------------------------------------------------- | -------------------------------------------- |
| **绑定方式** | element.onclick = fn | element.addEventListener(type, fn, useCapture) | 同 OM2，但事件类型更丰富（如滚轮、输入事件） |
| **移除方式** | element.onclick = null | element.removeEventListener(type, fn, useCapture) | 同 OM2 |
| **支持多个处理函数** | 只能绑定一个，后者覆盖前者 | 可绑定多个，同一事件触发时依次执行 | 同 OM2 |
| **支持事件捕获** | 仅冒泡 | 第三个参数 true 表示捕获，false 表示冒泡 | 同 OM2 |
| **this 指向** | 绑定事件的元素 | 绑定事件的元素 | 绑定事件的元素 |
| **兼容性** | 所有浏览器都支持 | IE9+ / 现代浏览器 | 现代浏览器 |
| **典型应用** | btn.onclick = fn; | btn.addEventListener("click", fn); | input.addEventListener("input", fn); |



## Ajax

### 定义

发送请求的行为

- 浏览器输入 URL 回车，默认使用 GET 方法
- 静态资源标签自动加载，如 script、link、img
- 静态资源标签手动加载，如 a、form
- JavaScript 动态请求资源，通过 DOM 响应

AJAX（Asynchronous JavaScript and XML）是一种在不刷新整个页面的前提下，使用 JavaScript 在后台与服务器进行异步数据交互的技术集合

- A（Asynchronous）：异步执行，不阻塞用户操作
- J（JavaScript）：发请求、拿响应、更新 DOM 都在前端通过脚本完成
- X（XML）：除了 XML，也可以适用于 JSON 和 HTML

### XMLHttpRequest

XMLHttpRequest 是浏览器内置的 JS 对象，用于在不断刷新页面的前提下，与服务端进行异步 HTTP 通信

关键属性

- readyState：当前请求所处的阶段
    - 0 / UNSENT：创建了 XMLHttpRequest 实例，但是还没有调用 open() 方法
    - 1 / OPENED：已调用过 open()，但尚未调用 send() 方法
    - 2 / HEADERS_RECEIVED：已调用 send()，并且响应头已可获得，但响应体尚未开始接收
    - 3 / LOADING：响应体部分数据正在接收
    - 4 / DONE：响应已完全接收或请求已失败/中止
- status：HTTP 响应状态码
    - 200：请求已成功获得响应
    - 302：临时重定向
    - 404：请求的资源不存在
    - 500：服务端发生了错误
- response 内容
    - responseText：响应的字符串文本
    - responseXML：解析后的 DOM 文档
    - responseType：预期的响应类型


关键方法

- 构造发送
    - open(method, url)：初始化请求
    - setRequestHeader(header, value)：设置请求头信息
    - send(body)：设置请求体，并发送请求
    - abort()：立即取消请求
- 事件回调
    - onreadystatechange()：任意 readyState 变化时触发
    - onerror()：网络错误或跨域失败时触发
    - onload()：请求成功完成（readyState===4 且 status 在 200–299）时触发
    - ontimeout()：达到 timeout 时间后触发
    - onabort：调用 abort() 后触发

```js
// 1. 创建实例
const xhr = new XMLHttpRequest();

// 2. 初始化请求
xhr.open("GET", "https://jsonplaceholder.typicode.com/posts/1");

// 3. 监听状态变化
xhr.onreadystatechange = function () {
    // readyState 变化时都会触发
    if (xhr.readyState === 4) {
        if (xhr.status >= 200 && xhr.status < 300) {
            // 请求成功
            console.log("响应文本：", xhr.responseText);
            const data = JSON.parse(xhr.responseText);
            console.log("解析后的数据：", data);
        } else {
            // 请求失败
            console.error("请求失败，状态码：", xhr.status);
        }
    }
};

// 4. 发送请求
xhr.send();
```



## ECMAScript 6

> ECMAScript 实际上就是 JavaScript 的一次重大更新，提升了 JS 开发体验

### let 和 const

var 的局限性

- 只有全局作用域或函数作用域，不能在块内限定生命周期，易引发重名和覆盖
- var 声明会“提升”到函数或全局最顶端，导致在声明前就能访问到 undefined，增加调试难度

新增变量声明符

- let：块级作用域，声明后值与类型均可改变
- const：块级作用域，声明时必须初始化，声明后值与类型都不可变，但如果它引用的是对象或数组，对象内部仍可被修改

暂时性死区（TDZ, Temporal Dead Zone）：声明会自动提升到块级作用域顶部，但是在初始化前访问会抛出 ReferenceError

### 模板字符串

传统拼接：用双引号或单引号包裹，通过 + 拼接，需要 \\n 来实现换行

```js
let name = "dasi";
let msg = "hello " + name + "!\nWelcome";
```

模板字符串：用反撇号包裹，通过 ${...} 嵌入变量、方法或任意表达式，可以直接换行 

```js
let name = "dasi";
let msg = `hello ${name}!
Welcome`
```

### 解构赋值

使用一种声明式的语法，一次性从数组或对象中提取出多个值，并赋给相应的变量

- 简化变量声明
- 直接提取函数返回值和函数参数
- 交换变量值：[a, b] = [b, a]

数组解构

```js
// 传统方式
const arr = [1, 2, 3];
const a = arr[0];
const b = arr[1];

// 解构赋值：变量必须对应位置，若被解构的值数量不足变量数量，则多出的变量值为 undefined；
const [x, y, z] = [1, 2, 3];
console.log(x, y, z); // 1 2 3

// 跳过元素：使用逗号跳过，不占用变量
const [first, , third] = [10, 20, 30];
console.log(first, third); // 10 30

// 设置默认值：当对应元素为 undefined 时才使用默认值，而 null 等其他值不会触发默认
const [m = 5, n = 7] = [undefined, 2];
console.log(m, n);  // 5 2
```

对象解构

```js
// 传统方式
const user = { name: 'dasi', age: 21 };
const name1 = user.name;
const age1  = user.age;

// 解构赋值：名称必须相同，如果属性不存在，则为 undefined
const { name, age } = { name: 'dasi', age: 21 };
console.log(name, age); // dasi 21

// 解构赋值：重命名
const { name: uname, gender = 'male' } = { name: 'dasi' };
console.log(uname, gender); // dasi male
```

函数参数解构

```js
// 数组参数
function sum([a, b]) {
    return a + b;
}
console.log(sum([3, 4])); // 7

// 对象参数
function greet({ name, age = 21 }) {
    console.log(` 你好，${name}，${age} 岁 `);
}
greet({ name: 'dasi' }); // 你好，dasi，18 岁
```

### 箭头函数

箭头函数旨在提供一种更简洁、更安全、更符合现代开发习惯的函数写法

基本语法

```js
// 传统函数
function sum(a, b) {
    return a + b;
}

// 单条表达式无需大括号，默认返回该值
const sum = (a, b) => a + b;

// 单个参数可以省略小括号
const sq = x => x * x;

// 没有参数却不可以省略小括号
const sayHi = () => console.log('Hi');

// 多条表达式需要大括号
const cmp = (a, b) => {
    if (a > b) return 1;
    if (a < b) return -1;
    return 0;
};
```

this 绑定：箭头函数不有自己的 this，它的 this 始终指向定义时所在的外层作用域，适合在回调里保持上下文

```js
<button id="btn" value="abc">点我查看值</button>

<script>
    const widget = {
        value: 123,
    
        // 传统方式：this 指向触发事件的 DOM 元素，输出 abc
        bindWithFunction() {
        document.getElementById('btn').addEventListener('click', function() {
                console.log(this);
                console.log('function this.value =', this.value);
            });
        },

        // 箭头函数方式：this 指向 widget 对象，输出 123
        bindWithArrow() {
        document.getElementById('btn').addEventListener('click', () => {
            console.log(this)
            console.log('arrow this.value =', this.value);
            });
        }
    };

    // 选择一个方式
    widget.bindWithFunction();
    widget.bindWithArrow();
</script>
```

### rest 和 spread

rest：可以通过 ...rest 放在参数列表的最后，将剩余参数收集到一个数组里面

```js
function sum(...nums) {
    return nums.reduce((total, n) => total + n, 0);
}
console.log(sum(1, 2, 3));    // 6
```

spread：可以通过 ...spread 将一个可迭代对象展开成一列单独的值或属性

```js
// 数组展开
const nums = [1, 2, 3];
console.log(Math.max(...nums)); // 等同于 Math.max(1, 2, 3) → 3
const a = [1, 2];
const b = [3, 4];
const c = [...a, ...b]; // [1, 2, 3, 4]

// 对象展开：后面属性会覆盖前面
const o1 = { x: 1, y: 2 };
const o2 = { y: 3, z: 4 };
const o3 = { ...o1, ...o2 }; // { x:1, y:3, z:4 }
```

> spread 通常用于深拷贝：object_copy = [...object]

### 模块化

模块化：将代码按功能拆分到独立模块中的设计思想

- 高内聚、低耦合：每个模块只关注自己的一部分功能，暴露必要接口，其它细节对外隐藏
- 可维护性：模块代码独立、易读、易测、易复用
- 依赖管理：显式声明模块间依赖关系，避免全局变量冲突

模块实现

- 导出：通过 export 标记哪些属性和功能是对外可用的，明确“我能提供什么”
- 导入：通过 import 引入外部文件的哪些属性和功能，明确“我需要什么”
- 导出导入内容都是作为对象进行处理

导出方式

- 分别导出：每个要导出的绑定都单独加上 export 关键字
- 统一导出：先在模块内部定义，然后在底部一次性集中导出
- 默认导出：模块只能有一个默认导出，适用于该模块的主功能

导入方式

- 分别导入：使用 {} 括起需要导入的属性或功能，名称必须与导出时的名称一致，可以使用 as 进行 重命名
- 统一导入：可以利用通配符 * 导入，但是必须使用 as 进行重命名作为对象使用
- 默认导入：直接随意给定一个名称导入之前默认导出的东西，不需要与导出时的名称一致