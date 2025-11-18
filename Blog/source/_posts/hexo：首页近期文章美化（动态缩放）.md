---
title: hexo魔改：首页近期文章美化（动态缩放）
tags:
  - hexo
categories:
  - 博客搭建
cover: /image/hexo.png
abbrlink: 290c75b9
date: 2024-09-04 17:53:21
description: 在首页近期文章增加了动态缩放效果，鼠标悬停会有响应
---
<meta name="referrer" content="no-referrer"/>

## 1. 效果预览

进入首页查看即可：https://dasi.plus/

## 2. 教程

{% note info flat %}<a href="https://dasi.plus/posts/ecc80865/">自定义CSS教程</a>{% endnote %}

在路径`BlogRoot\source\css`下添加文件`homeArticle.css`，并增加以下内容

```css
/* 默认 */
#recent-posts>.recent-post-item>.recent-post-info>.content {
  opacity: 0.9;
  line-height: 1.5;
  transition: all .2s;
}
/* 鼠标悬停 */
#recent-posts>.recent-post-item:hover .recent-post-info .content {
  
  opacity: 1; /* 透明度改变 */
  line-height: 2; /* 行高改变 */
  font-size: 120%; /* 字体大小改变 */
  transition: all .2s;
}
/* 标题大小 */
#recent-posts>.recent-post-item>.recent-post-info>.article-title {
  font-size: 30px
}
```