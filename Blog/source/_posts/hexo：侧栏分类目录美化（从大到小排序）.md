---
title: hexo魔改：侧栏分类目录美化（从大到小排序）
tags:
  - hexo
categories:
  - 博客搭建
cover: /image/hexo.png
abbrlink: 5e7a5e9b
date: 2024-09-04 15:30:40
description: 实现侧栏分类目录从大到小排序
---
<meta name="referrer" content="no-referrer"/>

## 1. 效果预览

![](https://gitee.com/wyw_0227/picture-bed/raw/master/Hexo/202409041535117.png)

## 2. 教程

找到路径`BlogRoot\themes\butterfly\scripts\helpers`下的`aside_categories.js`文件，修改源代码：
```js
  // name按照名称排序，length按照文章数排序
  const orderby = options.orderby || 'length'
  // 1是升序，-1是降序
  const order = options.order || -1
```

## 3. 参考链接

{% link hexo-theme-butterfly 修改侧边栏分类排序规则,洛语 の Blog,https://luoyuy.top/posts/8cb0fd83894c/ %}