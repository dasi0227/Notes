---
title: hexo魔改：URL持久化
date: 2024-09-02 00:48:26
tags:
  - hexo
categories:
  - 博客搭建
cover: /image/hexo.png
abbrlink: 2dff033d
description: 基于butterfly主题，在hexo中设置持久化URL，并解释这样做的必要性和原因
---
<meta name="referrer" content="no-referrer"/>

## 1. 初始设置介绍

在_config.yml中找到`URL`配置项

```yml
# URL
url: https://dasi.plus # 主页的域名，可以是github的page页如https://username.github.io，也可以是自定义的域名如https://dasi.plus
permalink: :year/:month/:day/:title/	# 预设永久链接格式
permalink_defaults: # 默认永久链接格式（设置了预设值此处可以不用填写）
pretty_urls: # 美化url
  trailing_index: true/false # 是否在末尾添加`index.html`
  trailing_html: true/false # 是否在末尾添加`.html`
```

## 2. 必要性

永久链接（permalink）：是一个用来引用或链接到特定网页、博客文章或其他网络内容的固定URL

搜索引擎优化（search engine optimization,SEO）：提高网站在搜索引擎结果页中排名的过程

为什么要使用**持久化url**：确保链接的稳定性和一致性，<font color="orangered">一切都是为了SEO</font>

> 如果使用了:year/:month/:day或者:category/，一旦在文章的front-matter中修改了日期或分类，那么相应的url也会修改

permalink要求
- 建立一致的结构：提高用户体验和搜索引擎抓取效率
- 使用关键词：如使用post，music等，使URL更具描述性，有助于SEO
- 避免在URL中使用特殊字符：使URL更难以解析和记忆，甚至使URL失效
- 避免在URL中使用日期：过早日期会让搜索引擎误认为内容已经过时，从而降低SEO
- 避免URL过长：有助于SEO
- 避免使用中文：URL会对中文进行转码，这将会是一场灾难，不信你试试

## 3. 手动修改

第一步：修改`_config.yml`的URL配置项
``` yml
permalink: :permalink # 冒号表示利用文章front-matter中，键permalink对应的值
```

第二步：修改`HexoRoot/scaffolds/post.md`
```markdown
---
title: {{ title }}
date: {{ date }}
tags:
categories:
description:
cover:
permalink: # 添加该行，键是permalink，值是你自定义的永久链接内容，可以使用关键词/posts/，/article/，/music/等
---
```

## 4. 插件修改

手动修改的局限性
- 每一次都需要在新建的文章中添加permalink值
- <font color="orangered">起名是一件很难很难很难很难的事！</font>，如果利用序号区分很容易重复

> 利用插件可以实现实现自动化命名

第一步：在Hexo根目录下打开终端安装插件
```shell
npm install hexo-abbrlink --save
```

第二步：修改`_config.yml`的URL配置项
``` yml
permalink: posts/:abbrlink/
```
> 同上，可以看出这里使用了文章front-matter中，键abbrlink对应的值

第三步：在`_config.yml`中添加`hexo-abbrlink`配置项
```yml
# 持久化URL
abbrlink:
  alg: crc32 # algorithm算法：支持16位校验算法crc16(default)和32位校验算法crc32
  rep: hex # representation哈希值表示形式：支持十进制dec(default)和十六进制hex
```

> 不同设置对应的url
> - crc16 & hex：posts/66c8.html
> - crc16 & dec：posts/65535.html
> - crc32 & hex：posts/8ddf18fb.html
> - crc32 & dec：posts/1690090958.html
> 
> <font color="deepskyblue">使用crc32和hex：crc32的哈希冲突较低，hex的url较短</font>

## 5. 踩坑

如果你部署之后发现，点击页面不是跳转，而是下载了一个abbrlink名称且存储html代码的文件

![](https://gitee.com/wyw_0227/picture-bed/raw/master/Hexo/202409021510611.png)

说明你在`_config.yml`的URL配置项中，permalink最后漏了一个`/`，补上即可

## 6. 参考链接

{% link 优化 Hexo 网站的永久链接格式,Dejavu’s Blog,https://blog.dejavu.moe/posts/hexo-permalinks/ %}