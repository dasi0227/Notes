# CSS



* [CSS](#css)
   * [概述](#概述)
      * [定义](#定义)
      * [语法](#语法)
      * [设置手段](#设置手段)
      * [CSS 后台流程](#css-后台流程)
   * [选择器](#选择器)
      * [基本选择器](#基本选择器)
      * [属性选择器](#属性选择器)
      * [组合选择器](#组合选择器)
      * [伪元素选择器](#伪元素选择器)
   * [文本属性](#文本属性)
      * [color](#color)
      * [font-family](#font-family)
      * [font-size](#font-size)
      * [font-weight](#font-weight)
      * [font-style](#font-style)
      * [text-decoration](#text-decoration)
      * [letter-spacing](#letter-spacing)
      * [line-height](#line-height)
      * [text-align](#text-align)
      * [text-indent](#text-indent)
      * [white-spacecuno](#white-spacecuno)
   * [选择器优先级](#选择器优先级)
      * [特异度](#特异度)
      * [优先级](#优先级)
      * [继承](#继承)
   * [盒子模型](#盒子模型)
      * [组成](#组成)
      * [大小设置](#大小设置)
      * [border](#border)
      * [盒子类型](#盒子类型)
      * [外边距合并](#外边距合并)
      * [overflow属性](#overflow属性)
   * [盒子排版](#盒子排版)
      * [类型](#类型)
      * [flexbox](#flexbox)
      * [float](#float)
      * [position](#position)



## 概述

### 定义

**层叠样式表（Cascading Style Sheets,CSS）**：通过不同的规则来控制页面上元素的样式，并根据优先级应用不同的样式，使网页在不同设备和屏幕上都呈现良好的视觉体验

层叠性的体现：

- 来源的优先级：**内联样式优先级最高，接下来是内部样式表，最后是外部样式表**
- 选择器的优先级：从高到低依次是**内联样式、ID 选择器、类选择器、标签选择器**
- 顺序优先级：如果两个样式的来源和选择器相同，那么**后定义的样式会覆盖先定义的样式**

### 语法

属性后跟冒号`:`，属性值前面需要有空格，后面需要有分号

```
选择器 {
  属性1: 属性值1;
  属性2: 属性值2;
}
```

> 注意在 html 中是属性后跟等于号`=`

### 设置手段

- 外链：引用外部CSS文件（最常用，**实现css和html的分离**）

```html
<link rel="stylesheet" href="/url/to/style.css"
```

- 嵌入：写在css文件中的`<style></style>`标签内（一般用于全局设置和特殊页面的设置）

```html
<style>
  li { margin: 0; list-style: none; }
  p { margin: 1em 0; }
</style>
```

- 內联：作为标签内的属性值（不推荐，html的属性不应该用于样式）

```html
<p style="margin: 1em 0">contene</p>
```

### CSS 后台流程

1. 解析 HTML：浏览器会首先解析 HTML 文件，构建 DOM 树
2. 解析 CSS：浏览器会解析所有的 CSS 规则，它将根据不同的 CSS 文件、内联样式或内部样式表构建一个 CSSOM 树
3. 计算样式：浏览器会将 DOM 树和 CSSOM 树结合起来，计算每个 DOM 元素的最终样式
4. 布局：浏览器计算每个元素的确切位置和尺寸
5. 绘制：浏览器会将元素渲染到屏幕上，应用颜色、背景、边框、阴影等样式
6. 合成：当页面元素绘制完成后，浏览器会将各个图层合成在一起并最终呈现在用户屏幕上



## 选择器

### 基本选择器

- 通配选择器：使用`*`选择所有元素
- 元素/标签选择器：填写指定的html元素/标签名称
- ID 选择器：使用`#`选择具有唯一ID的元素
- 类选择器：使用`.`选择属于某个类的所有元素

> 类选择器可以其他选择器复合使用，比如`p.center`表示选择类为center中的所有p标签
> 可以一次性选择多个选择器，用逗号隔开，如`h1, h2, .center`

### 属性选择器

- `[attribute]`：选择具有某个属性的所有元素
- `[attribute="value"]`：选择具有特定属性值的元素
- `[attribute^="value"]`：选择属性值以指定字符串开头的元素
- `[attribute$="value"]`：选择属性值以指定字符串结尾的元素
- `[attribute*="value"]`：选择属性值包含指定字符串的元素

### 组合选择器

- 后代选择器：使用一个空格` `选择父元素的所有后代元素
- 子元素选择器：使用`>`选择父元素的直接子元素
- 相邻选择器：使用`+`选择紧邻某元素之后的第一个元素
- 兄弟选择器：使用`~`选择某元素后面的所有元素

### 伪元素选择器

- `::before`：在元素的内容之前插入内容（常用于添加图标）
- `::after`：在元素的内容之后插入内容（常用于添加分隔符）
- `::first-letter`：选择元素的首个字母（常用于大写字母）
- `::first-line`：选择元素的首行文本（常用于首行突出）
- `a:link`：选择未被访问的链接
- `a:visited`：选择已经被访问过的链接
- `a:hover`：选择鼠标悬停在的链接
- `a:active`：选择正在被点击的链接
- `input:focus`：选择当前具有焦点的元素（常用于表单填写）
- `tr:first-child`：选择父元素中的第一个子元素（常用于首行加粗）
- `td:last-child`：选择父元素中的第一个子元素（常用于首列加粗）

> 伪元素是**处于特殊状态的元素**，它不能被看作为一个新的 HTML 元素，也无法成为真正的 DOM 元素，但是可以添加独立的 CSS 样式，甚至改变页面布局



## 文本属性

### color

- **RGB**：通过红、绿、蓝三种色光的强度值表示颜色
    - 十六进制表示，每一字段从00到ff：`#rrggbb`
    - 十进制表示，每一字段从0到255：`rgb(red, green, blue)`
- **HSL**：通过色相、饱和度和亮度来表达颜色
    - Hue：控制颜色的色相（0-360）
    - Saturation：控制色彩的饱和度（0-100%），越大颜色越鲜艳
    - Lightness控制颜色的亮度（0-100%），越大颜色越亮
- **关键字**：black，white，skyblue，maroon等预定义的经典颜色
- **透明度（transparent）**：控制颜色的透明程度，范围从 0（完全透明）到 1（完全不透明），放在第四通道（rgba和hsla）

### font-family

font-family：用于指定文本的字体序列，浏览器会按顺序尝试使用第一个可用的字体，字体名称之间用逗号`,`分隔

通用字体族：font-familt的最后一个值，是浏览器都具有的字体风格

| 风格       | 字体样式   | 例子                  | 适用                 |
| ---------- | ---------- | --------------------- | -------------------- |
| serif      | 衬线字体   | Times New Roman、宋体 | 正式和传统的文本风格 |
| sans-serif | 无衬线字体 | Arial、黑提           | 现代和简洁的设计     |
| monospace  | 等宽字体   | Courier、中文         | 代码显示和技术文档   |
| cursive    | 手写字体   | Comic Sans、楷体      | 适合个性化的场景     |
| fantasy    | 装饰性字体 | Papyrus               | 通常用于特定主题设计 |

### font-size

- `px`：像素大小
- `%`和`em`：相对于父元素的比例
- `rem`：相对于根元素的比例
- 关键字：`small`、`medium`、`large`

### font-weight

- `normal`：正常字体粗细（相当于 400）
- `bold`：粗体（相当于 700）
- `bolder`：比父元素更粗
- `lighter`：比父元素更细
- 数字值：从 100 到 900

### font-style

- `normal`：使文本竖直（默认值）
- `italic`：使文本斜体
- `oblique`：使文本倾斜，通常比斜体的倾斜程度稍微小一些

### text-decoration

- `none`：移除任何装饰（通常用于去掉链接的下划线）
- `underline`：添加下划线
- `line-through`：添加删除线
- `overline`：添加上划线

### letter-spacing

- `normal`：使用浏览器默认的字符间距（默认值）
- 长度单位：可以使用px、em、rem等来修改字符之间的间距

### line-height

- `normal`：使用浏览器默认的行高（默认值）
- 单一数值：相对于字体大小的比例
- 比例：使用%，em，rem设置相对于字体大小的比例
- 像素单位：设置固定的行高

### text-align

- `left`：将文本对齐到容器的左边（默认值）
- `right`：将文本对齐到容器的右边
- `center`：将文本居中对齐
- `justify`：使文本两端对齐，行内文字会自动调整间距以填满整行

> `justify` 对最后一行不生效，因为最后一行内容较少，强行填满会破坏美观

### text-indent

- 单位可以是px、em、rem等长度单位
- 使用负值时，文本会向左缩进

> text-indent只影响段落的第一行，对其他行无效

### white-spacecuno

对空白符的处理

| 方式     | 合并空格 | 保留换行符 | 自动换行 |
| -------- | -------- | ---------- | -------- |
| normal   | 是       | 否         | 是       |
| nowrap   | 是       | 否         | 是       |
| pre      | 否       | 是         | 否       |
| pre-wrap | 否       | 是         | 是       |
| pre-line | 否       | 是         | 是       |



## 选择器优先级

### 特异度

1. ID选择器的数量
2. 类选择器、属性选择器、伪类的数量
3. 标签选择器、伪元素选择器的数量

考虑下面例子：前者的特异度比后者的特异度大

| 选择器               | id   | 类   | 标签 |
| -------------------- | ---- | ---- | ---- |
| #nav .list li a:link | 1    | 2    | 2    |
| .hd ul.link a        | 0    | 2    | 2    |

考虑下面代码：常用于设置基础样式和特殊样式

```css
<button class="btn">基础按钮</button>
<button class="btn special">特殊按钮</button>
<style>
  .btn {
    padding: .36em .8em;
    border: none;
    background: rgb(226, 69, 17);
    color: #090101;
  }

  .btn.special {
    color: #fff;
    background: #218de6;
  }
</style>
```

### 优先级

**!important > 内联样式 > ID选择器 > 类选择器 > 标签选择器 > 通配符**

### 继承

继承：属性值与父元素对应的属性值一样

- 自动继承：文本和字体相关的值
- 不自动继承：盒子模型相关的属性
- 显式继承：`inherit`
- 显式不继承：`initial`



## 盒子模型

> **布局是通过CSS样式将HTML元素按照特定的规则在网页中排列和分布，决定了页面的结构和视觉呈现**

### 组成

1. **内容（content）**：元素实际展示内容的区域，通过属性`width、height`控制
2. **内边距（padding）**：内容和边框之间的距离，通过属性`padding、padding-top、padding-right、padding-bottom、padding-left`控制
3. **边框（border）**：包裹住内容和内边距的框线，通过属性`border、border-width、border-style、border-color`控制
4. **外边距（margin）**：当前元素与相邻元素之间的距离，通过属性`margin、margin-top、margin-right、margin-bottom、margin-left`控制

![image-20250916094457330](https://dasi-blog.oss-cn-guangzhou.aliyuncs.com/Java/202509160944429.png)

### 大小设置

以 margin 为例子

- 一个值：`margin: 10px`，该值将同时应用于四个方向
- 两个值：`margin: 5px 15px`，第一个值作用于上下，第二个值作用于左右
- 三个值：`margin: 5px 10px 15px`，第一个值作用于上，第二个值作用于左右，第三个值作用于下
- 四个值：`margin 5px 10px 15px 20px`，按照**上、右、下、左**顺时针作用

### border

三个基本子属性：从左到右按顺序

- 宽度：长度单位或者关键字（thin细、medium中、thick粗）
- 样式：none没有边框、solid实线、dashed虚线、dotted点线、double双线、groove凹槽、ridge脊槽、inset嵌入式、outset突出
- 颜色：关键字、rgb、十六进制或hsl

```css
border: 2px solid red;
```

border是同时设置四个方向的边框，如果要单独设置，需要显式单独指定

```css
border-top: 2px solid red;
border-right: 3px dashed blue;
```

特殊设置

- 边框圆角（border-radius）：使元素的角变得圆润，单位是px
- 边框分离（border-collaspse）：常用于表格元素，默认值是合并边框，而`separate`使得表格的单元格边框保持分开，并通过`border-spacing`设置单元格间距

### 盒子类型

通过属性`box-sizing`设置盒子类型

| 类型     | content-box                                           | border-box                                            |
| -------- | ----------------------------------------------------- | ----------------------------------------------------- |
| 计算方式 | width和height只包括内容                               | width和height包括内容、内边距和边框                   |
| 常见用途 | 针对内容，元素尺寸 = 内容尺寸 + 内边距尺寸 + 边框尺寸 | 针对元素，内容尺寸 = 元素尺寸 - 边框尺寸 - 内边距尺寸 |
| 影响布局 | 内边距和边框增加了元素的外部空间                      | 内边距和边框不会影响外部空间                          |

### 外边距合并

`margin-collapse` 是默认行为，会将相邻的块级元素的**上下 margin**合并为一个边距，且大小取决于**较大**的margin值，而不是两个margin值的和

> 水平的margin是不会合并的

什么时候不会有外边距合并

- 存在边框和内边距
- 不是块级布局
- 存在`overflow`属性

### overflow属性

overflow属性是用于控制当一个元素的内容超出其区域时，如何显示多余的内容

- `visible`：溢出的内容会被显示出来（默认值）
- `hidden`：溢出的内容会被隐藏
- `scroll`：始终显示
- `auto`：只有超出才会显示滚动条。



## 盒子排版

### 类型

**CSS的控制对象是盒子，而HTML的控制对象是元素/标签，不同HTML元素会生成不同排版的CSS盒子**，通过属性`display`设置

- **常规流（normal flow）**：盒子按照文档顺序排列
    - **行级（inline）**：盒子**从左到右**排列，适合小盒子，如`<span>、<a>、<strong> `
    - **块级（block）**：盒子**从上到下**排列，适合大盒子，如`<div>、<p>、<h1>`
    - **行块级（inline-block）**：盒子可以像行级别一样从左到右排列，也可以像块级一样设置宽和高
    - **表格（table）**：盒子**以行和列的形式**排列，适用于表格布局，如`<table>、<tr>、<td>`
    - **弹性盒（flexbox）**：**沿主轴排列**子元素（水平或竖直），常用于响应式布局
    - **网格布局（grid）**：**同时定义行和列**，适用于复杂布局
- **浮动（float）**：盒子**浮动到容器的一侧**，后续元素会环绕浮动元素
- **定位（position）**：盒子**相对于某个位置进行定位**

> 行级盒子只有在一行放不下的时候才会换行

### flexbox

flexbox可以**将父元素定义为flex容器，子元素则自动成为flex项目**，从而实现统一控制flex项目的排版

基本属性

- `flex-direction`：定义主轴的方向，决定了项目的排列方式
    - `row`：从左到右（默认）
    - `column`：从上到下
    - `row-reverse`：从右到左
    - `column-reverse`：从下到上
- `flex-wrap`：决定项目是否换行
    - `no-wrap`：不允许换行（默认）
    - `wrap`：允许换行
    - `wrap-reverse`：换行但反向排列
- `justify-content`：决定项目之间的间隔
    - `flex-start`：项目紧靠容器的起始位置
    - `flex-end`：项目紧靠容器的结束位置
    - `center`：项目居中
    - `space-between`：项目之间有均等的空间，首尾没有间隔
    - `space-around`：项目之间有均等的空间，首尾有部分间隔
    - `space-evenly`：项目之间有均等的空间，首位也有相同大小的间隔
- `align-items`：决定项目的对齐方式
    - `stretch`：项目拉伸以填充容器（默认）
    - `flex-start`：项目对齐到交叉轴的起始位置
    - `flex-end`：项目对齐到交叉轴的结束位置
    - `center`：项目在交叉轴上居中对齐
    - `baseline`：项目按照其文本基线对齐

flexibility：控制项目的伸缩行为

- `flex-grow`：定义项目的放大比例，默认值是0，表示项目不会主动放大填充容器
- `flex-shrink`：定义项目的缩小比例，默认值是1，表示项目会缩小以适应容器
- `flex-basis`：定义项目的初始大小（px），默认值是auto，表示项目的初始大小由内容决定

### float

浮动的作用是让元素浮动到容器的一侧，其他内容会环绕在浮动元素周围，最常用的功能是实现**文字环绕图片**

通过`float`属性设置浮动，通过`clear`属性清除浮动

### position

1. 相对定位（relative）：相对于自身的原始位置进行定位
2. 绝对定位（absolute）：相对于最近的定位祖先进行定位
3. 固定定位（fixed）：始终相对于视口进行定位
4. 粘性定位（sticky）：在指定滚动范围内相对于视口定位

> relative实际上并没有脱离文档流