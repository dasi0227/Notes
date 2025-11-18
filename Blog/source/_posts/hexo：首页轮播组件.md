---
title: hexo魔改：首页轮播组件
tags:
  - hexo
categories:
  - 博客搭建
cover: /image/hexo.png
abbrlink: 5f3e08e1
date: 2024-09-04 17:49:23
description: 添加一个首页轮播组件卡片，可以实现文章置顶或展示重点文章的效果
---
<meta name="referrer" content="no-referrer"/>

## 1. 效果预览

![](https://gitee.com/wyw_0227/picture-bed/raw/master/Hexo/202409041923547.png)

## 2. 教程

第一步：在博客根目录下打开终端，运行以下指令：
```bash
npm install hexo-butterfly-swiper --save
```

第二步：在站点配置文件`_config.yml`添加配置信息
```yml
# 文章轮播
swiper:
  enable: true
  priority: 5 
  enable_page: / 
  timemode: date 
  layout: 
    type: id
    name: recent-posts  
    index: 0
  default_descr: 想一个默认描述好难的！
  swiper_css: https://npm.elemecdn.com/hexo-butterfly-swiper/lib/swiper.min.css #swiper css依赖
  swiper_js: https://npm.elemecdn.com/hexo-butterfly-swiper/lib/swiper.min.js #swiper js依赖
  custom_css: https://npm.elemecdn.com/hexo-butterfly-swiper/lib/swiperstyle.css # 适配主题样式补丁
  custom_js: https://npm.elemecdn.com/hexo-butterfly-swiper/lib/swiper_init.js # swiper初始化方法
```

第三步：自定义配置参数

- 【选填】priority：过滤器优先级，数值越小，执行越早，默认为10，
- 【必填】enable：是否开启
- 【选填】enable_page：应用地址，主页就填`/`，分类页面就填`/categories/`，所有页面就填`all`，默认为all
- 【选填】timemode：`date`为显示创建日期，`updated`为显示更新日期，默认为date
- 【选填】layout.type：挂载容器类型`id/class`，不填则默认为id
- 【必填】layout.name：挂载容器名称
- 【选填】layout.index：当layout.type为class，此项用来确认究竟排在第几位
- 【选填】default_descr	text：默认文章描述

第四步：在文章的`front-matter`中使用
```markdown
title: 文章标题
date: 创建日期
updated: 更新日期
cover: 文章封面
description: 文章描述
swiper_index: 1 #置顶轮播图顺序，非负整数，数字越大越靠前
```

## 3. 参考链接

{% link Swiper Bar,Akilar,https://akilar.top/posts/8e1264d1/ %}