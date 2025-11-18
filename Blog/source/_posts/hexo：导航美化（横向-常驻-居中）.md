---
title: hexo魔改：导航美化（居中+横向+常驻）
tags:
  - hexo
categories:
  - 博客搭建
cover: /image/hexo.png
abbrlink: ae54bd6f
date: 2024-09-04 13:39:52
description: 实现导航美化，包括导航居中，导航子菜单横向居中和导航常驻
---
<meta name="referrer" content="no-referrer"/>

## 1. 效果预览

![](https://gitee.com/wyw_0227/picture-bed/raw/master/Hexo/202409041402758.png)

## 2. 教程

如何自定义CSS请看

{% link hexo 魔改：js 和 css 文件的添加,Dasi's Blog,https://dasi.plus/posts/ecc80865/ %}

在路径`BlogRoot\source\css`下添加文件`nav.css`，输入以下内容

```css
/* 导航居中 */
#nav .menus_items {
  position: absolute;
  width: fit-content;
  left: 50%;
  transform: translateX(-50%);
}

/* 子菜单横向 */
.menus_item_child li:not(#sidebar-menus li){
  float: left;
  border-radius: 6px!important;
  -webkit-border-radius: 6px!important;
  -moz-border-radius: 6px!important;
  -ms-border-radius: 6px!important;
  -o-border-radius: 6px!important;
}
.menus_item_child:not(#sidebar-menus ul){
  left:50%;
  translate:-50%;
}

/* 导航常驻 */
.nav-fixed #nav{
  transform: translateY(58px)!important;
  -webkit-transform: translateY(58px)!important;
  -moz-transform: translateY(58px)!important;
  -ms-transform: translateY(58px)!important;
  -o-transform: translateY(58px)!important;
}
#nav{
  transition: none!important;
  -webkit-transition: none!important;
  -moz-transition: none!important;
  -ms-transition: none!important;
  -o-transition: none!important;
}
```

## 3. 分析

居中：将`.menus_items`元素的定位设置为绝对定位，并使用`left: 50%`和`transform: translateX(-50%)`来水平居中

横向：将`.menus_item_child`下的所有`li`元素横向排列，并设置圆角`border-radius`；将子菜单的左边距设置为50%并使用`translate`来居中

常驻：将`#nav`元素向下移动58px，通常用于固定位置的导航栏；禁用所有过渡效果`transition`，确保导航栏的变化不带动画。


## 4. 参考链接

{% link buterfly博客导航栏居中,Leonus,https://blog.leonus.cn/2022/hexoCenter.html %}