---
title: hexo魔改：站点标题美化（动态改变）
tags:
  - hexo
categories:
  - 博客搭建
cover: /image/hexo.png
description: 实现从本站离开时和回到本站时改变站点标题
abbrlink: 2dbb3dd3
date: 2024-09-02 21:10:40
---
<meta name="referrer" content="no-referrer"/>

## 1. 自定义css和js

{% link hexo魔改：js和css文件的添加,Dasi's Blog,https://dasi.plus/posts/ecc80865/ %}

## 2. 教程

第一步：在路径`BlogRoot\source\js`下添加`sitetitle.js`，写入以下内容
```js
//动态标题
var OriginTitile = document.title;
var titleTime;
document.addEventListener("visibilitychange", function () {
  if (document.hidden) {
    //离开当前页面时标签显示内容
    document.title = "......";  // 修改这里
    clearTimeout(titleTime);
  } else {
    //返回当前页面时标签显示内容
    document.title = "......"; // 修改这里
    //变回正常标题
    titleTime = setTimeout(function () {
      document.title = OriginTitile;
    }, 2000); // 修改这里，单位是毫秒，2000就是两秒
  }
});
```

第二步：在`_config.butterfly.yml`中引入
```yml
  - <script src="/js/sitetitle.js"></script>
```

## 3. 参考链接

{% link butterfly 重装日记,安知鱼,https://blog.anheyu.com/posts/sdxhu.html#%E7%AB%99%E7%82%B9%E5%8A%A8%E6%80%81-title %}