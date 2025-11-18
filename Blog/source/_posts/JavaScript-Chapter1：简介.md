---
title: JavaScript：简介
tags:
  - JavaScript
categories:
  - 笔记
cover: /image/js.png
abbrlink: 627fa4e0
date: 2024-09-05 21:07:55
description: 初学JavaScript，一些基本知识
---
<meta name="referrer" content="no-referrer"/>

## 1. 什么是JavaScript

JavaScript：是一门用来与网页交互的脚本语言，简称JS

组成
- ECMAScript：定义了JavaScript的语言规范和核心功能
- DOM：文档对象模型（Document Object Model），提供与网页内容交互的方法和接口，用于在HTML中使用扩展的XML
  - 修改网页内容
  - 修改网页结构
  - 创建和添加新元素
- BOM：浏览器对象模型（Browser Object Model），提供与浏览器交互的方法和接口，用于支持访问和操作浏览器的窗口
   - 显示浏览器警告框
   - 打开新窗口
   - 提供关于浏览器的详尽信息

{% note info flat %}知名的Web浏览器：IE、FireFox、Chrome、Safari、Opera、Edge{% endnote %}

## 2. 如何使用JavaScript

实现：通过`<script>`元素，将JavaScript的代码嵌入到HTML页面中，或者通过src属性引入保存在外部文件中的JavaScript文件

`<script>`的属性
- src：指定外部脚本文件的URL
- charset：指定脚本文件的字符编码
- type：指定脚本的MIME类型，通常设置为`"text/javascript"`
- async：指定外部脚本是否异步加载
- defer：指定脚本是否延迟执行

标签位置
- 放在head：脚本最先执行，页面渲染会被阻塞，直到脚本加载和执行完成
- 放在body：脚本执行时间取决于其位置
- 放在bottom：脚本会在页面的所有内容都加载完毕后执行，提高页面加载速度

{% note success flat %}推荐放在bottom，会加速用户视角下的页面加载{% endnote %}

加载顺序
- 默认：浏览器会按照标签在页面出现的顺序依次解释
- 推迟：使用defer属性，脚本会被延迟到整个页面都解析完毕后再运行
- 异步：使用async属性，脚本会在后台并行加载，同时不会阻塞页面的渲染

{% note warning flat %}推迟和异步都只适用于外部JS{% endnote %}

外部文件的好处
- 可维护性：用一个目录存储所有要用到的JS文件，更容易统一管理和维护
- 灵活度高：不需要在对应页面的html文件中修改js代码，只需要找到js文件修改即可
- 缓存：如果多个页面使用相同的JS文件，浏览器会缓存第一次使用过的JS文件，之后只用从缓存中加载，而无需重新下载

{% note danger flat %}外部JS文件最好是下载到本地之后使用相对地址引用，而不是直接使用网页链接，这样可以避免由于外部服务器发生故障或链接失效而导致的脚本加载问题，以及不法人员对JS文件的恶意攻击{% endnote %}

## 3. 参考教程

{% link JavaScript实现,w3school,https://www.w3school.com.cn/js/pro_js_implement.asp %}