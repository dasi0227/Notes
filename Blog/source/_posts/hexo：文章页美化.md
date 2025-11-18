---
title: hexo魔改：文章页美化
tags:
  - hexo
categories:
  - 博客搭建
cover: /image/hexo.png
abbrlink: 8347bba9
date: 2024-09-04 17:20:37
description: 文章页是博客的灵魂，对每一个元素进行自定义美化
---
<meta name="referrer" content="no-referrer"/>

## 1. 自定义CSS
{% note info flat %}<a href="https://dasi.plus/posts/ecc80865/">自定义CSS教程</a>{% endnote %}

在路径`BlogRoot\source\css`下添加文件`post.css`

## 2. 教程

### 2.1 标题居中

```css
/* 标题居中 */
#post-info {
  text-align: center;
}
```

参考链接
{% link 【butterfly教程】更改文章页的文章相关信息布局,梦如烟的博客,https://moonruyan.github.io/post/84dc2e1a.html %}

### 2.2 字体大小

```css
/* 各级标题大小 */
#article-container > h2 {
  font-size: 40px;
}
#article-container > h3 {
  font-size: 30px;
}
#article-container > h4 {
  font-size: 20px;
}
#article-container > h5 {
  font-size: 15px;
}
/* 目录字体 */
#card-toc>.toc-content{
  font-size: 20px;
}
```

### 2.3 顶部图模糊
```css
/* 顶部图模糊 */
#page-header.post-bg::before{
  backdrop-filter: blur(10px);
  -webkit-backdrop-filter: blur(10px);
}
```

## 3. 持续更新...