---
title: HTML
tags:
  - HTML
categories:
  - 笔记
cover: /image/frontend.png
abbrlink: 4ab788fc
date: 2024-11-05 23:43:47
description: html的基础知识，基本结构和基本元素
---
<meta name="referrer" content="no-referrer"/>

## 1. 基础概念

【HTML定义】

**超文本标记语言（HyperText Markup Language,HTML）**：是标签语言，而不是编程语言，用于**在网页中显示内容，而不是根据输入来输出结果**
- 超文本：指的是**图片、链接、表格等不局限于文本**的内容
- 标记：利用**标签标记超文本**

【HTML作用】

负责**构建网页结构和设置网页内容**，实际上任何网页本质上都是一个html文件，只不过添加了各种样式和功能

【HTMl元素】

html元素指的是**开始标签、内容和结束标签**三部分组成的整体，但是不是所有标签都是成对出现的，还有自闭合标签，如`<img />`

可以通过在标签中设置html元素的属性，格式需要满足
- 属性之间用空格隔开
- 属性名后需要跟一个`=`号
- 属性值用双引号`""`括起来

{% note warning flat %}
注意区分html和css设置属性值的区别！
{% endnote %}

【语义化元素】

实践中总是根据内容和内容结构来选择对应的标签，这样做不仅帮助开发者和浏览器理解网页内容，还对搜索引擎优化和无障碍访问有积极影响。

比如说文章可以使用`<article></article>`，章节可以使用`<section></section>`，页脚使用`<footer></footer>`等

【无语义元素】

html提供了`<div></div>`和`<span></span>`无语义标签，一般是为了实现特殊样式和特殊功能，配合class属性或id属性使用

{% note warning flat %}
元素非常便利但容易被滥用，只有在没有更好的语义方案时才选择它，而且要尽可能少用，否则文档的升级和维护工作会非常困难
{% endnote %}

## 2. html文件的基本结构

```html
<!DOCTYPE html>
<html>
  <head>
    <meta charset="UTF-8">
    <title>网页标题</title>
    <link rel="stylesheet" href="styles.css">
  </head>
  <body>
    网页内容
  </body>
  <script src="script.js"></script>
</html>
```

- `<!DOCTYPE html>`：**声明文档类型**

- `<html></html>`：根元素，包裹了页面的所有内容

- `<head></head>`：是html文件的首部，包含文档的**元数据**，这部分内容不会呈现在页面上
  - `<meta>`：定义页面的字符编码、作者、描述和关键字等
  - `<title></title>`：定义页面标题（不属于内容，不是内容标题！）
  - `<link>`：引入外部资源，常用于引入CSS文件

- `<body></body>`：包含页面的所有可视内容

- `<script></script>`：设置执行脚本

{% note warning flat %}
实践中总是将script标签放在页面的底部而不是首部中，因为这样可以先呈现页面内容，再加载页面行为，有利于降低用户视角下的网页加载时间
{% endnote %}

## 3. html内容的基本结构

```html
<header>
	<h1>网页标题</h1>
</header>

<nav>
	<ul>
	<li><a href="#home">首页</a></li>
	<li><a href="#services">服务</a></li>
	<li><a href="#contact">联系</a></li>
	</ul>
</nav>

<main>
    <article>
		<h2>文章标题</h2>
		<p>这是文章的第一段内容。</p>
    </article>
    <section>
		<h3>章节标题</h3>
		<p>这里是章节内容。</p>
    </section>
</main>

<aside>
    <h3>广告</h3>
    <ul>
		<li><a href="#">广告1</a></li>
		<li><a href="#">广告2</a></li>
		<li><a href="#">广告3</a></li>
    </ul>
</aside>

<footer>
	<p>禁止侵权！</p>
	<ul>
		<li><a href="#">隐私政策</a></li>
		<li><a href="#">服务条款</a></li>
	</ul>
</footer> 
```

- `<header></header>`：**页眉**，位于网页顶部，通常包含**大标题，导航菜单，logo图案**等内容
- `<nav></nav>`：导航，位于网页边上，通常包含**每个子页面的超链接和搜索栏目**
- `<main></main>`：**主体**，**位于网页中心**，通常包含**文章、图片、视频**等内容
- `<aside></aside>`：**侧边栏**，位于网页两边，通常包含**广告、目录**等内容
- `<footer></footer>`：**页脚**，位于网页底部，通常包含**版权声明、隐私政策**等内容

{% note warning flat %}
上述内容都是在html文件的`<body></body>`标签内，注意内容结构和文件结构的不同！
{% endnote %}

## 3. 文本标签

- `<h1></h1>`：标题，支持级别1到级别6

- `<p></p>`：段落

- `<u></u>`：下划线

- `<strong></strong>`和`<b></b>`：强调，文本加粗

- `<em></em>`和`<i></i>`：着重，文本斜体

- `<code></code>`：代码，显示为等宽字体

- `<pre></pre>`：预格式化，保留空格和换行

- `<blockquote></blockquote>`和`<q></q>`：引用，会有文本缩进

- `<sup></sup>`和`<sub></sub>`：上标和下标

## 4. 列表标签

有序列表（ordered list,ol）

```html
<ol>
	<li>内容1</li>
	<li>内容2</li>
	<li>内容3</li>
<ol>
```

无序列表（unordered list,ul）

```html
<ul>
	<li>内容1</li>
	<li>内容2</li>
	<li>内容3</li>
<ul>
```

自定义列表（definition list,dl）

```html
<dl>
	<dt>项目</dt>
		<dd>python</dd>
		<dd>html</dd>
	<dt>人员</dt>
		<dd>小红</dd>
		<dd>小明</dd>
	<dt>时间</dt>
		<dd>一月</dd>
		<dd>二月</dd>
</dl>
```

## 5. 多媒体标签

{% note info flat %}
网址/URL/链接：虽然狭义上有区别，但是广义上都可以认为是指向html、文本、图像、视频和音频等可以在网络上保存的任何文件的指针
{% endnote %}

### 5.1 锚点链接

`<a></a>`：用于嵌入外部URL，又称为超链接/超文本引用（hypertext reference）
- `href`：超文本引用（hypertext reference），值为链接目标的URL
- `title`：提供链接的额外信息或提示文本，鼠标悬停时显示
- `download`：提供一个默认的保存文件名
- `target`：指定链接的打开方式
  - `_self`：在同一个窗口或标签页打开链接（默认值）
  - `_blank`：在新窗口或新标签页中打开链接
  - `_parent`：在父框架中打开链接
  - `_top`：在整个浏览器窗口中打开链接
- `rel`：定义当前页面与目标页面之间的关系，增强安全性和 SEO 效果
  - `noopener`：防止新页面访问当前页面的 window 对象，提高安全性
  - `noreferrer`：不仅防止新页面访问当前页面的 window 对象，还会隐藏引用来源，通常用于增强隐私性
  - `nofollow`：告诉搜索引擎不要跟踪该链接，用于防止传递链接权重
  - `external`：指示链接是外部链接

```html
<a href="https://dasi.plus/" target="_blank" title="即将进入dasi博客" rel="external">达斯的博客</a>
```

### 5.2 图片链接

【基本属性】

`<img>`：用于嵌入静态图像文件，是一个**自闭合**的标签
- `src`：指定图片的来源URL（必选）
- `alt`：指定图片的替代文本，在图片无法加载时显示（必选）
- `title`：指定了鼠标悬停在图片上显示的文本
- `width`和`height`：设置图片的显示宽度和高度
- `srcset`：提供不同分辨率或尺寸图片的URL，以适配不同的设备（电脑、手机、平板）
- `sizes`：指示图片在不同视口尺寸下的显示尺寸，配合`srcset`使用
- `loading`：设置图片的加载方式，可以帮助提升网页加载速度
  - `lazy`：懒加载，只有页面滚动到图片所在位置时才加载
  - `eager`：立即加载（默认值）

【绑定图片和描述】

```html
<figure>
  <img src="images/dinosaur.jpg" alt="dinosaur" 
		width="400" height="341" />
  <figcaption>
    A T-Rex on display in the Manchester University Museum.
  </figcaption>
</figure>
```

### 5.3 视频链接：`<video></video>`

【基本属性】

- `src`：指定视频的URL路径
- `width`和`height`：设置视频的宽度和高度
- `controls`：布尔属性，添加后启用视频控件，如播放、暂停、音量调节等
- `autoplay`：布尔属性，添加后自动播放
- `muted`：布尔属性，添加后静音播放
- `loop`：布尔属性，添加后会自动循环播放
- `poster`：指定视频加载或播放之前显示的封面
- `preload`：是否预加载，有助于增快页面加载
  - `auto`：自动加载
  - `metadata`：仅加载视频的元数据
  - `none`：不预加载
- `<source>`标签：提供不同格式的视频源
- `<track>`标签：用于添加字幕、说明等轨道信息
- 标签之间的备用文字：提供浏览器不支持音频播放时的提示信息

【指定不同播放源和轨道信息】

```html
<video controls>
  <source src="example.mp4" type="video/mp4" />
  <source src="example.webm" type="video/webm" />
  <track kind="subtitles" src="subtitles_es.vtt" srclang="es" label="Spanish" />
</video>
```

### 5.4 音频链接：`<audio></audio>`

【基本属性】

- `src`：指定音频的 URL 路径
- `controls`：布尔属性，添加后启用音频控件，如播放、暂停、音量调节等
- `autoplay`：布尔属性，添加后自动播放
- `muted`：布尔属性，添加后静音播放
- `loop`：布尔属性，添加后会自动循环播放
- `preload`：是否预加载，有助于增快页面加载
  - `auto`：自动加载
  - `metadata`：仅加载音频的元数据
  - `none`：不预加载
- `<source>`标签：提供不同格式的音频源
- 标签之间的备用文字：提供浏览器不支持音频播放时的提示信息

【指定不同播放源】

```html
<audio controls autoplay muted loop >
	<source src="audio.mp3" type="audio/mpeg" />
	<source src="audio.ogg" type="audio/ogg" />
	您的浏览器不支持 HTML5 音频。
</audio>
```

## 6. 表格标签

```html
    <table border="1">
      <caption>考试成绩表</caption>
      <thead>
      <tr>
        <th>姓名</th>
        <th>科目</th>
        <th>分数</th>
      </tr>
      </thead>
      <tbody>
      <tr>
        <td rowspan="2">张三</td> <!-- 跨两行 -->
        <td>语文</td>
        <td>85</td>
      </tr>
      <tr>
        <td>数学</td>
        <td>90</td>
      </tr>
      <tr>
        <td colspan="2">总分</td> <!-- 跨两列 -->
        <td>175</td>
      </tr>
      </tbody>
    </table>
  </body>
```

【基本标签】

- `<table></table>`：声明一个表格
- `<caption></caption>`：设置表格标题，显示在表格上方并居中
- `<th></th>`：设置表头内容，字体默认加粗
- `<tr></tr>`：声明表格的一行
- `<td></td>`：设置单元格数据
- `<thead></thead>`，`<tbody></tbody>`和`<tfood></tfood>`：将表格分为表头、表体和表脚，便于组织和样式化

【合并单元格】

使用 colspan 属性将一个单元格跨越多列
使用 rowspan 属性将一个单元格跨越多行

## 5. 表单标签

### 5.1 输入标签：`<input />`

`type`：指定输入框的类型
  - `text`：单行文本输入框
  - `password`：密码输入框，输入的内容会被隐藏
  - `email`：邮箱输入框，浏览器会自动验证格式是否有效
  - `number`：数字输入框，限制用户只能输入数字
  - `radio`：单选按钮
  - `checkbox`：复选框
  - `button`：普通按钮
  - `file`：文件选择器
  - `date`：日期输入框
  - `time`：时间输入框
  - `submit`：上传按钮，用于提交表单
- `name`：指定输入字段的名称，表单提交时会使用该名称作为键
- `value`：指定选型的值
- `maxlength`：限制输入框中可输入的最大字符数
- `size`：设置输入框的可见字符宽度
- `placeholder`：占位符文本，帮助用户理解要输入什么内容
- `required`：布尔属性，指定当前输入框为必填
- `readonly`：布尔属性，指定当前输入框为只读
- `pattern`：指定一个正则表达式，用于验证输入值的格式
- `min`和`max`：指定能够输入的数量最值

### 5.2 其他常用标签

`<button></button>`：用于创建按钮，可以在表单中使用，也可以作为单独的控件，支持更灵活的内容和样式，常用类型有：
- `submit`：提交表单
- `reset`：用于重置表单所有字段
- `button`：用于 javascript 事件

```html
<!-- 提交按钮 -->
<button type="submit">提交</button>
<!-- 重置按钮 -->
<button type="reset">重置</button>
<!-- 普通按钮 -->
<button type="button" onclick="alert('按钮被点击了')">普通按钮</button>
```

`<textarea></textarea>`：用于创建多行文本输入框，以接收较长的文本数据，需要指定行和列的长度
```html
<textarea rows="4" cols="50" placeholder="请输入评论"></textarea>
```

`<select></select>`、`<optgroup></optgroup>`和`<option></option>`：第一个标签对定义了一个下拉列表，第二个标签对定义选项分组，第三个标签设置列表中的每个选项

```html
<select name="fruits">
    <optgroup label="常见水果">
        <option value="apple">苹果</option>
        <option value="banana">香蕉</option>
    </optgroup>
    <optgroup label="热带水果">
        <option value="mango">芒果</option>
        <option value="papaya">木瓜</option>
    </optgroup>
</select>
```