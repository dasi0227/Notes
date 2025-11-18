---
title: hexo魔改：js和css文件的添加
tags:
  - hexo
categories:
  - 博客搭建
cover: /image/hexo.png
description: 掌握js和css文件的添加，才是走上魔改的第一步
abbrlink: ecc80865
date: 2024-09-02 22:30:57
---
<meta name="referrer" content="no-referrer"/>

## 1. 建立文件夹

为了统一管理，建议按照文件类型来建立文件夹，路径在`BlogRoot/source`下

一般来说，我们需要3个文件夹
- js：存放 JavaScript 文件，用于实现网站的动态功能和交互效果（如导航菜单的展开、图像轮播、表单验证等）
- css：存放 CSS 文件，用于定义网站的样式（包括颜色、字体和布局等）
- image：存放图片文件，用于网站的视觉元素（如图标、背景图、封面图等）

![](https://gitee.com/wyw_0227/picture-bed/raw/master/Hexo/202409030123448.png)

## 2. 创建文件

鼠标右键<font color="orangered">新建文本文件</font>，然后修改后缀名为`.js`或`.css`，最后用VSCode等编辑器打开添加内容即可

## 3. 引用

要在`_config_butterfly.yml`中倒数第二个配置项，即`inject`配置项中引用

> 可以直接拉到最后，或者添加书签，因为这个配置项经常会用到

1. css文件要在`head`下
```yml
  head:
    - <link rel="stylesheet" href="/css/filename1.css?1">
    - <link rel="stylesheet" href="/css/filename2.css?1">  
```

2. js文件要在`bottom`下
```yml
  bottom:
    - <script src="/js/filename1.js?1"></script>
    - <script src="/js/filename2.js?1"></script>
```

## 4. 补充

建议
- 每次只需要复制粘贴前一行，然后修改一下文件名即可
- 在静态文件后面添加`?1`，浏览器会识别这是一个新的URL，从而强制重新下载文件而不是使用缓存的旧版本，有助于确保用户总是能看到最新的内容

注意
- 可以通过外链来引用文件，但是外链如果失效会导致样式丢失，因此<font color="orangered">慎用</font>
- 路径开头直接是`/`，而不是`./`
- <font color="orangered">缩进，列表符和空格</font>不能遗漏
- 特殊情况下，两个相关联的文件的引用顺序有强制要求

## 5. 参考文章

{% link Hexo博客添加自定义css和js文件,Leonus,https://blog.leonus.cn/2022/custom.html %}