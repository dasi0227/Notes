---
title: hexo魔改：背景美化（透明效果）
tags:
  - hexo
categories:
  - 博客搭建
cover: /image/hexo.png
abbrlink: 87f3e4
date: 2024-09-03 16:47:16
description: 设置背景颜色渐变，实现透明效果和毛玻璃效果，并详细分析代码
---
<meta name="referrer" content="no-referrer"/>

## 1. 效果预览

![](https://gitee.com/wyw_0227/picture-bed/raw/master/Hexo/202409041213770.png)

## 2. 教程

如何自定义CSS请看

{% link hexo 魔改：js 和 css 文件的添加,Dasi's Blog,https://dasi.plus/posts/ecc80865/ %}

在路径`BlogRoot/source/css`下添加文件`background.css`，输入以下内容

```css
/* 背景颜色 */
#body-wrap {
  background: -webkit-linear-gradient(
    90deg,
    rgba(247, 149, 51, 0.1) 0,
    rgba(243, 112, 85, 0.1) 15%,
    rgba(239, 78, 123, 0.1) 30%,
    rgba(161, 102, 171, 0.1) 44%,
    rgba(80, 115, 184, 0.1) 58%,
    rgba(16, 152, 173, 0.1) 72%,
    rgba(7, 179, 155, 0.1) 86%,
    rgba(109, 186, 130, 0.1) 100%
  );
  background: linear-gradient(
    90deg,
    rgba(247, 149, 51, 0.1) 0,
    rgba(243, 112, 85, 0.1) 15%,
    rgba(239, 78, 123, 0.1) 30%,
    rgba(161, 102, 171, 0.1) 44%,
    rgba(80, 115, 184, 0.1) 58%,
    rgba(16, 152, 173, 0.1) 72%,
    rgba(7, 179, 155, 0.1) 86%,
    rgba(109, 186, 130, 0.1) 100%
  );
}
/* 背景透明 */
#aside-content>.card-widget.card-info, /* 侧栏作者介绍组件 */
#aside-content>.card-widget.card-announcement, /* 侧栏公告组件 */
#aside-content>.sticky_layout>.card-widget.card-categories, /* 侧栏分类组件 */
#aside-content>.sticky_layout>.card-widget.card-tags, /* 侧栏标签组件 */
#aside-content>.sticky_layout>.card-widget.card-webinfo, /* 侧栏统计组件 */
#card-toc.card-widget, /* 文章页侧栏目录 */
#recent-posts>.recent-post-item, /* 首页近期文章组件 */
#archive>.article-sort>.article-sort-item, /* 归档页 */
#post, /* 文章 */
#page /* 自创页 */
{
  transform: translateZ(0);
  background: var(--light_bg_color);
  backdrop-filter: blur(10px); /* 应用高斯模糊效果，可以根据需要调整模糊程度 */
  -webkit-backdrop-filter: blur(10px); /* 兼容性前缀，适用于一些旧版本的浏览器 */
}

/* 黑夜模式 */
[data-theme=dark] #aside-content>.card-widget.card-info,
[data-theme=dark] #aside-content>.card-widget.card-announcement,
[data-theme=dark] #aside-content>.sticky_layout>.card-widget.card-categories,
[data-theme=dark] #aside-content>.sticky_layout>.card-widget.card-tags,
[data-theme=dark] #aside-content>.sticky_layout>.card-widget.card-webinfo,
[data-theme=dark] #card-toc.card-widget,
[data-theme=dark] #recent-posts>.recent-post-item,
[data-theme=dark] #archive>.article-sort>.article-sort-item,
[data-theme=dark] #post,
[data-theme=dark] #page
{
  transform: translateZ(0);
  background: var(--dark_bg_color);
  backdrop-filter: blur(10px); 
  -webkit-backdrop-filter: blur(10px); 
}

/* 页脚透明 */
#footer {
  background: rgba(255,255,255,0);
  color: #000;
  border-top-right-radius: 20px;
  border-top-left-radius: 20px;
  backdrop-filter: saturate(100%)
}
#footer::before {
  background: rgba(255,255,255,0)
}
#footer #footer-wrap {
  color: var(--font-color)
}
#footer #footer-wrap a {
  color: var(--font-color)
}
```

参考链接
{% link 关于我 Butterfly 主题的所有美化,小嘉的部落格,https://blog.imzjw.cn/posts/b74f504f/index.html#%E5%85%A8%E5%B1%80%E8%83%8C%E6%99%AF%E9%80%8F%E6%98%8E%E6%B8%90%E5%8F%98 %}

## 3. 分析

### 3.1 如何找组件

1. `hexo s`打开本地预览
2. 进入元素所在的网页
3. `F12`打开开发者工具
4. `ctrl+shift+c`开启设备仿真与元素检查，或者点击左上角按钮
  ![](https://gitee.com/wyw_0227/picture-bed/raw/master/Hexo/202409041246462.png)
5. 将鼠标移动到对应元素点击，就可以跳转到对应的代码，然后就可以看到当前元素所属的class和id
6. 进行自定义，语法可以参考以下链接

{% link CSS 教程,W3School,https://www.w3school.com.cn/index.html %}

参考链接
{% link Butterfly透明背景设置,云雨归海,https://www.cnblogs.com/glory-yl/p/15399411.html %}

### 3.2 慎用backdrop-filter！

如果要在透明的基础上实现毛玻璃效果，是基于backdrop-filter的高斯模糊算法实现的。如果当它应用于整个页面或者多个元素时，会<font color="orangered">极大程度增加计算负担，从而可能导致网页卡帧</font>

{% note info flat %}
你可以试试将blur值设置为较大值如100px，然后打开浏览器看看滚动效果，或者打开任务管理器看看浏览器使用CPU情况，~~或者听听你笔记本风扇的声音~~
{% endnote %}

既然这个效果要用到算法，GPU的计算能力比CPU要强，因此可以加上属性：`transform: translateZ(0);`

{% note warning flat %}虽然卡顿的问题有所缓解，但肯定还是没有自然的丝滑，一定要酌情使用！{% endnote %}

参考链接

{% link 高斯模糊的算法,阮一峰的网络日志,https://www.ruanyifeng.com/blog/2012/11/gaussian_blur.html %}

{% link 毛玻璃效果backdrop-filter:blur卡顿性能优化方案,陈华编程,http://www.ichenhua.cn/read/226 %}