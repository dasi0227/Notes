---
title: CSS Deep
tags:
  - CSS
categories:
  - 笔记
cover: /image/frontend.png
abbrlink: f5e1ee56
date: 2024-11-19 16:23:54
description: 选择器优先级、盒子模型和布局
---
<meta name="referrer" content="no-referrer"/>

## 1. 选择器的优先级问题

### 1.1 特异度（specificity）

1. ID选择器的数量
2. 类选择器、属性选择器、伪类的数量
3. 标签选择器、伪元素选择器的数量

考虑下面例子：前者的特异度比后者的特异度大

|选择器|id|类|标签|
|-|-|-|-|
|#nav .list li a:link|1|2|2|
|.hd ul.link a|0|2|2|

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

{% note success flat %}
优先级顺序：**!important > 内联样式 > ID选择器 > 类选择器 > 标签选择器 > 通配符**
{% endnote %}

### 1.2 继承

继承：属性值与父元素对应的属性值一样
- 自动继承：文本和字体相关的值
- 不自动继承：盒子模型相关的属性
- 显式继承：`inherit`
- 显式不继承：`initial`

## 2. 盒子模型

{% note warning flat %}
**布局是通过CSS样式将HTML元素按照特定的规则在网页中排列和分布，决定了页面的结构和视觉呈现**
{% endnote %}

### 2.1 组成

1. 内容（content）：元素实际展示内容的区域，通过属性`width、height`控制
2. 内边距（padding）：内容和边框之间的距离，通过属性`padding、padding-top、padding-right、padding-bottom、padding-left`控制
3. 边框（border）：包裹住内容和内边距的框线，通过属性`border、border-width、border-style、border-color`控制
4. 外边距（margin）：当前元素与相邻元素之间的距离，通过属性`margin、margin-top、margin-right、margin-bottom、margin-left`控制

图片

## 3. 四个方向的设置

以margin为例子
- 一个值：`margin: 10px`，该值将同时应用于四个方向
- 两个值：`margin: 5px 15px`，第一个值作用于上下，第二个值作用于左右
- 三个值：`margin: 5px 10px 15px`，第一个值作用于上，第二个值作用于左右，第三个值作用于下
- 四个值：`margin 5px 10px 15px 20px`，按照**上、右、下、左**顺时针作用

### 2.3 边框

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

{% note success flat %}
border的神奇应用：如果内容的宽度和高度都为0，那么边框之间会斜切形成一个三角形，此时再将颜色设置为透明`transparent`，则可以得到三角形
```css
<div class="a"></div>
<style>
  .a {
    height: 0px;
    width: 0px;
    border-top: 100px solid red;
    border-right: 100px solid transparent;
    border-bottom: 100px solid green;
    border-left: 100px solid yellow;
  }
</style>
```
图片
{% endnote %}

### 2.4 外边距合并

`margin-collapse`是默认行为，会将相邻的块级元素的**上下 margin**合并为一个边距，且大小取决于**较大**的margin值，而不是两个margin值的和

{% note warning flat %}
水平的margin是不会合并的
{% endnote %}

什么时候不会有外边距合并
- 存在边框和内边距
- 不是块级布局
- 存在`overflow`属性

### 2.5 盒子类型

通过属性`box-sizing`设置盒子类型

|类型|content-box|border-box|
|-|-|-|
|计算方式|width和height只包括内容|width和height包括内容、内边距和边框|
|常见用途|针对内容，元素尺寸 = 内容尺寸 + 内边距尺寸 + 边框尺寸|针对元素，内容尺寸 = 元素尺寸 - 边框尺寸 - 内边距尺寸|
|影响布局|内边距和边框增加了元素的外部空间|内边距和边框不会影响外部空间|

### 2.6 overflow属性

overflow属性是用于控制当一个元素的内容超出其区域时，如何显示多余的内容
- `visible`：溢出的内容会被显示出来（默认值）
- `hidden`：溢出的内容会被隐藏
- `scroll`：始终显示
- `auto`：只有超出才会显示滚动条。

## 3. 盒子排版

### 3.1 类型

**CSS的控制对象是盒子，而HTML的控制对象是元素/标签，不同HTML元素会生成不同排版的CSS盒子**

盒子排版：通过属性`display`设置
- **常规流（normal flow）**：盒子按照文档顺序排列
  - **行级（inline）**：盒子**从左到右**排列，适合小盒子，如`<span>、<a>、<strong> `
  - **块级（block）**：盒子**从上到下**排列，适合大盒子，如`<div>、<p>、<h1>`
  - **行块级（inline-block）**：盒子可以像行级别一样从左到右排列，也可以像块级一样设置宽和高
  - **表格（table）**：盒子**以行和列的形式**排列，适用于表格布局，如`<table>、<tr>、<td>`
  - **弹性盒（flexbox）**：**沿主轴排列**子元素（水平或竖直），常用于响应式布局
  - **网格布局（grid）**：**同时定义行和列**，适用于复杂布局
- **浮动（float）**：盒子**浮动到容器的一侧**，后续元素会环绕浮动元素
- **定位（position）**：盒子**相对于某个位置进行定位**

{% note warning flat %}
行级盒子只有在一行放不下的时候才会换行，
{% endnote %}

### 3.2 弹性盒（flexbox）

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

```css
<div class="container">
  <div class="a">A</div>
  <div class="b">B</div>
  <div class="c">C</div>
</div>
<style>
  .container {
    display: flex;
    flex-direction: row-reverse;
    justify-content: space-evenly;
    border: 2px solid #966;
    align-items: baseline;
  }

  .a,
  .b,
  .c {
    text-align: center;
    padding: 1em;
  }

  .a {
    background: #fcc;
    height: 10px;
  }

  .b {
    background: #cfc;
    height: 20px;
  }

  .c {
    background: #ccf;
    height: 5px;
  }
</style>
```

图片

### 3.3 网格（grid）

grid是一种二维的布局系统，可以**同时控制行和列的排列**
1. grid先将父元素定义为grid容器，其子元素自动成为grid项目
2. 划分grid容器为网格格子
3. 设置网格线为grid项目分配网格区域

图片

如何划分网格区域
- 属性
  - `gird-template-columns`：定义一共有多少列，每列格子的宽度是多少
  - `gird-template-rows`: 定义一共有多少行，每行格子的宽度是多少
- 单位
  - `px`：直接指定绝对长度
  - `%`：基于容器的百分比宽度或高度
  - `auto`：自动适配内容，列或行的大小由内容决定
  - `fr`：根据剩余空间等比例分配的单位

```css
grid-template-columns: 100px 100px 200px;
grid-template-rows: 50px 50% 2fr;
```

如何设置网格线来分配网格区域：画四条线，四条线形成的区域就是网格区域，线用数字标识，如下图

图片

```css
grid-row-start: 1;
grid-column-start: 1;
grid-row-end: 3;
grid-column-end: 3;
/* 或者 */
grid-area: 1/1/3/3; 
```

### 3.4 浮动（float）

浮动的作用：让元素浮动到容器的一侧，其他内容会环绕在浮动元素周围，最常用的功能是实现**文字环绕图片**

通过`float`属性设置浮动，通过`clear`属性清除浮动

```css
<section>
    <img src="https://p4.ssl.qhimg.com/t017aec0e7edc961740.jpg" width="300" alt="mojave" />
    <p>
      莫哈韦沙漠不仅纬度较高，而且温度要稍微低些，是命名该公园的短叶丝兰——约书亚树的特殊栖息地。
      约书亚树以从茂密的森林到远远间隔的实例等各种形式出现。
      除了约书亚树森林之外，该公园的西部包括加州沙漠里发现的最有趣的地质外观。
    </p>
</section>

<style>
    img {
        float: left;
    }

    p {
        clear: both;
        line-height: 1.8;
    }
</style>
```

{% note warning flat %}
float 布局在现代布局中逐渐被 Flexbox 和 Grid 取代
{% endnote %}

### 3.5 定位（position）

1. 相对定位（relative）：相对于自身的原始位置进行定位
2. 绝对定位（absolute）：相对于最近的定位祖先进行定位
3. 固定定位（fixed）：始终相对于视口进行定位
4. 粘性定位（sticky）：在指定滚动范围内相对于视口定位

{% note warning flat %}
relative实际上并没有脱离文档流
{% endnote %}