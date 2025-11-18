---
title: 记录第一次更改域名
tags:
  - hexo
categories:
  - 博客搭建
cover: /image/hexo.png
abbrlink: e051aba8
date: 2025-03-24 19:42:29
description:
---
<meta name="referrer" content="no-referrer"/>


## 前言

最近刷到一个小视频，讲述了选择域名选择的三宗罪，分别是
1. **不要使用 .net**，因为它价格贵，但是在顶级域名中的 SEO 效果却不是很好，也就是性价比很低
2. **不要使用 .cn**，因为国外访问该网站可能会很慢，而且国家域名备案很复杂，而且还有很多限制
3. **不要使用二级域名**，因为它不利于 SEO，并且非常不利于用户记忆，这是大忌，同时如果要创立子域名，那么整个 URL 将会变得十分冗长
  
> 实际上短视频还讲了另外一宗罪，就是在前后加数字来买到便宜域名

看完之后，**我默默瞟了一眼我的域名 `dasi.net.cn`，嗯，`dasi.net.cn`，然后陷入了沉思...**

于是乎，原本打算在 7 月份域名到期到期后再更换，然而这学期是想宣传一下我的博客的，害怕懂行的看到我的域名，恶心到连昨天吃的饭都吐出来了，干脆一不做二不休，就在今天，重新找了若干个教程，花了将近两个多小时，踩了无数坑，实现了初步的域名更换。

**但是我有很强烈的预感，我将来某天还会更换我的域名**，特别是如果发达了，一定要搞个 `.com` 或者 `.cc` 这样一眼看过去就“厉害”的域名（我也不知道为什么很厉害，但是厉害的公司都是 .com）。因此，我觉得很有必要记录一下我的第一次更改域名经历，避免下一次还浪费几个小时做同样的工作，同时也是整理了完整的流程，介绍很多坑的解法，给有相同需求的朋友们提供一个明确教程。

> 需要注意的是，我这里都是以**hexo + Github Pages + 阿里云**为例，不要走，哪怕你用别的平台也是一模一样的，耐心看完！

## 1. 购买域名

[阿里云域名注册](https://wanwang.aliyun.com/domain/)，搜索你要注册的名字，选择你想要的域名，域名的不同可以问 gpt，简单来说就是好的域名的服务器多，搜索引擎会优先考虑，而且看起来更牛x，越好域名越贵。以下我们都用 `example.com` 代替。

> 当然如果你的名字很奇葩，比如说 `woshidashabi.com` 只用 83 一年，喜欢的可以下手了

## 2. 制定解析规则（坑：A 和 CNAME 的映射）

1. 进入域名控制台
2. 点击左侧的域名列表
3. 点击右侧的操作中的解析（注意不是点击域名）
4. 进入云解析 DNS
5. 点击添加记录如下四条记录（只用填给出的三个，其他默认就好）

|记录类型|主机记录|记录值|
|-|-|-|
|A|@|185.199.108.153|
|A|@|185.199.109.153|
|A|@|185.199.110.153|
|A|@|185.199.111.153|
|CNAME|www|\<username\>.github.io|

![](https://dasi-blog.oss-cn-guangzhou.aliyuncs.com/Hexo/202503242159206.png)

> 注意，**根域 `example.com` 用 A 指向官方的四个 IP 地址，子域 `www.example.com` 用 CNAME 指向 <username>.github.io，不能颠倒顺序**！这是因为 GitHub Pages 不允许用 CNAME 来指向根域，但是子域名是可以使用 CNAME 的，所以你必须使用 A 记录绑定固定 IP 才能让主域访问 GitHub Pages，GitHub 官方提供了 4 个 A 记录 IP，用于全球 CDN 加速，都填上以保证稳定性

## 3. 推送本地更改到远程仓库（坑：CNAME 文件）

1. 在 `~/source/` 下，新建一个名为 `CNAME` 的文件（不需要任何后缀），然后在里面填写你的域名 `example.com`
2. 修改根目录下的 `_config.yml`，修改一切与域名有关的内容为你自己的域名，特别是 `url: https://example.com`
3. 用终端打开根目录，输入 hexo 指令 `hexo clean && hexo g && hexo d`，推送本地更改到远程仓库

> 注意，CNAME 在本地是在 source 目录下的，不是根目录下，而且填写的时候不需要加 https！

## 4. Github Pages 自定义域名（坑：not be retrieved）

1. 进入你的 \<username\>.github.io 仓库
2. 点击上面一栏最右边的 Settings（注意是仓库而不是个人账户的 Settings）
3. 点击左栏的 Pages，滑倒最下面的 Custom domain
4. 填入你的域名，然后 Save 保存
5. 勾选 `Enforce HTTPS`（HTTPS = HTTP + SSL/TLS，而当下的浏览器默认只信任 HTTPS 网站，不信任 HTTP 网站，因此浏览器会弹出“该网站不安全”或“可能泄露信息”等信息，勾选后 GitHub Pages 会为你自动签发一个免费的 SSL 证书，就代表认证你的博客是专业、安全、可靠的！）
6. 用浏览器输入域名，99% 的概率你就可以访问你的网站了！

![](https://dasi-blog.oss-cn-guangzhou.aliyuncs.com/Hexo/202503242159200.png)

> 注意，这里你可能会收到这样的错误 `DNS record could not be retrieved!`。**不必担心，打一把王者荣耀，或者开一把金蝉蝉，回来刷新你就发现可以了**！这是因为 DNS 的全球同步和生效时间一般在几分钟到几小时之间，这不代表你配置错了，只是还没轮到你而已。
> 但是如果过了一个小时还不行，看看是不是之前的记录配置错了？或者看看 Github 仓库有没有 CNAME 文件？去阿里云进行生效检测看看是否配置成功了？

## 5. Cloudfare 部署 DNS（坑：循环重定向）

### 5.1 得到 Cloudfare 提供的名称服务器地址

1. 登陆/注册 cloudfare 账户
2. 点击账户主页
3. 点击添加域
4. 输入域名
5. 选择 free 计划
6. 删除平台自动配置的 NS 记录
7. 点击继续前往激活
8. 记录 cloudfare 提供的 DNS 服务器地址

![](https://dasi-blog.oss-cn-guangzhou.aliyuncs.com/Hexo/202503242159201.png)

### 5.2 更改域名的 DNS

1. 回到阿里云域名服务器
2. 点击域名列表中的域名
3. 点击左栏的 DNS 管理
4. 点击下面的 DNS 修改
5. 点击页面的修改 DNS 服务器
6. 填写先前记录的两个 DNS 服务器地址
7. 点击确定

![](https://dasi-blog.oss-cn-guangzhou.aliyuncs.com/Hexo/202503242159202.png)

### 5.3 更改加密模式

1. 回到 cloudfare 仪表板
2. 点击左侧的 SSL/TLS
3. 点击下面的概述
4. 把加密模式改成 Full (strict) 
5. 点击下面的边缘证书
6. 关闭永远使用 HTTPS 规则

![](https://dasi-blog.oss-cn-guangzhou.aliyuncs.com/Hexo/202503242159204.png)

> 如果不改，你使用浏览器访问域名的时候会出现**循环重定向**问题！
> 这里可能会显示错误 `domain does not belong to zone`。**没错，你没想错，再打一把王者荣耀，或者再开一把金蝉蝉，回来刷新你就发现可以了**，原因是一样的！

## 6. Google/Bing 收录网站（坑：站点地图无法获取）

这里**我不推荐你收录到百度，百度的配置比较复杂，而且这年头还有人用百度吗？有一说一有了 ai 连搜索引擎都很少用了（**

这里推荐看[另一个博客](https://blog.csdn.net/CoolBoySilverBullet/article/details/121802701)，图片多，适合小白

### 6.1 生成站点地图

1. 在你的 Hexo 根目录下运行
```bash
npm install hexo-generator-sitemap --save
```
2. 配置 _config.yml
```yml
sitemap:
  path: sitemap.xml
```
3. 利用 hexo 指令自动生成站点并上传到远程仓库
```bash
hexo clean && hexo g && hexo d
```
4. 访问如下网址，如果能看到 XML 格式的网页，说明生成成功了
```txt
https://example.com/sitemap.xml
```

### 6.2 收录网站

对于 [谷歌的 Google Search Console](https://search.google.com/search-console/about) 或者 [必应的 Bing Webmaster Tools](https://www.bing.com/webmasters/about)
1. 点添加属性 -> 选择 URL 前缀 -> 填入你的域名（带 https）
2. 验证方式选 TXT 验证，按照提示在你的 DNS 里自动加一条 TXT 记录
3. 验证通过后，进入左边栏编制索引下的站点地图 → 添加新的站点地图 -> 是上面生成的 `https://example.com/sitemap.xml`

> 注意，这里可能会显示站点地图无法抓取，你懂的我要说什么，**但这次不能打游戏了，睡个觉，起来你就发现可以了**

![](https://dasi-blog.oss-cn-guangzhou.aliyuncs.com/Hexo/202503242159205.png)

在 