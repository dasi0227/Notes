---
title: hexo魔改：外链美化（标签外挂）
tags:
  - hexo
categories:
  - 博客搭建
cover: /image/hexo.png
abbrlink: 2fa7a371
date: 2024-09-02 16:03:43
description: 单独给出链接过于单调，使用标签外挂实现外链美化
---
<meta name="referrer" content="no-referrer"/>

## 1. 效果预览

参考链接
{% link 魔改笔记七：分类条及外链卡片,LiuShen's Blog,https://blog.liushen.fun/posts/a64defb4/ %}
{% link hexo魔改：外链卡片,Dasi's Blog,https://dasi.plus/posts/2fa7a371/ %}

## 2. 教程

第一步：在路径`BlogRoot\themes\butterfly\scripts\tag`下新建文件`link.js`，写入以下内容

```javascript
function link(args) {
  args = args.join(' ').split(',');
  let title = args[0];
  let sitename = args[1];
  let link = args[2];

  // 定义不同域名对应的头像URL
  const avatarUrls = {
    'github.com': 'https://cdn.qyliu.top/i/2024/07/27/66a461a3098aa.webp',
    'csdn.net': 'https://cdn.qyliu.top/i/2024/07/27/66a461b627dc2.webp',
    'gitee.com': 'https://cdn.qyliu.top/i/2024/07/27/66a461c3dea80.webp',
    'zhihu.com': 'https://cdn.qyliu.top/i/2024/07/27/66a461cc20eb4.webp',
    'stackoverflow.com': 'https://cdn.qyliu.top/i/2024/07/27/66a461d3be02e.webp',
    'wikipedia.org': 'https://cdn.qyliu.top/i/2024/07/27/66a461db48579.webp',
    'baidu.com': 'https://cdn.qyliu.top/i/2024/07/27/66a461e1ae5b5.webp',
  };
  
  // 白名单域名
  const whitelistDomains = [
    'baidu.com'   // 修改此处，设置为自己的域名（也可以添加友联，','分隔）
  ];

  // 获取URL的根域名
  function getRootDomain(url) {
    const hostname = new URL(url).hostname;
    const domainParts = hostname.split('.').reverse();
    if (domainParts.length > 1) {
      return domainParts[1] + '.' + domainParts[0];
    }
    return hostname;
  }

  // 根据URL获取对应的头像URL
  function getAvatarUrl(url) {
    const rootDomain = getRootDomain(url);
    for (const domain in avatarUrls) {
      if (domain.endsWith(rootDomain)) {
        return avatarUrls[domain];
      }
    }
    return 'https://cdn.qyliu.top/i/2024/07/27/66a4632bbf06e.webp';  // 默认头像URL
  }

  // 检查是否在白名单中
  function isWhitelisted(url) {
    const rootDomain = getRootDomain(url);
    for (const domain of whitelistDomains) {
      if (rootDomain.endsWith(domain)) {
        return true;
      }
    }
    return false;
  }

  // 获取对应的头像URL
  let imgUrl = getAvatarUrl(link);

  // 判断并生成提示信息
  let tipMessage = isWhitelisted(link)
    ? "✅来自本站，可以放心食用~"
    : "🪧引用站外地址，不保证站点的可用性和安全性！";

  return `<div class='liushen-tag-link'><a class="tag-Link" target="_blank" href="${link}">
  <div class="tag-link-tips">${tipMessage}</div>
  <div class="tag-link-bottom">
    <div class="tag-link-left" style="background-image: url(${imgUrl});"></div>
    <div class="tag-link-right">
      <div class="tag-link-title">${title}</div>
      <div class="tag-link-sitename">${sitename}</div>
    </div>
    <i class="fa-solid fa-angle-right"></i>
  </div>
  </a></div>`;
}

hexo.extend.tag.register('link', link, { ends: false });
```

需要注意，上述函数只适用于二级根域名的判断，像博主是 dasi.plus，就无法判断。因此我是直接利用hostname判断，比较粗暴
```js
  // 检查是否在白名单中
  function isWhitelisted(url) {
    const hostname = new URL(url).hostname;
    return hostname === 'dasi.plus'
  }
```

第二步：在路径`BlogRoot\themes\butterfly\source\css\_tags`下新建文件`link.styl`，写入以下内容

```Stylus
:root
  --tag-link-bg-color white
  --tag-link-text-color black
  --tag-link-border-color white
  --tag-link-hover-bg-color rgb(141, 216, 233)
  --tag-link-hover-border-color black
  --tag-link-tips-border-color black
  --tag-link-sitename-color rgb(144, 144, 144)
  --tag-link-hover-sitename-color black

[data-theme=dark]
  --tag-link-bg-color #2d2d2d
  --tag-link-text-color white
  --tag-link-border-color black
  --tag-link-hover-bg-color #339297
  --tag-link-hover-border-color white
  --tag-link-tips-border-color white
  --tag-link-sitename-color rgb(144, 144, 144)
  --tag-link-hover-sitename-color white

#article-container
  .tag-Link
    background var(--tag-link-bg-color)
    border-radius 12px !important
    display flex
    border 1px solid var(--tag-link-border-color)
    flex-direction column
    padding 0.5rem 1rem
    margin-top 1rem
    text-decoration none !important
    color var(--tag-link-text-color)
    margin-bottom 10px
    transition background-color 0.3s, border-color 0.3s, box-shadow 0.3s

    &:hover
      border-color var(--tag-link-hover-border-color)
      background-color var(--tag-link-hover-bg-color)
      box-shadow 0 0 5px rgba(0, 0, 0, 0.2)

    .tag-link-tips
      color var(--tag-link-text-color)
      border-bottom 1px solid var(--tag-link-tips-border-color)
      padding-bottom 4px
      font-size 0.6rem
      font-weight normal

    .tag-link-bottom
      display flex
      margin-top 0.5rem
      align-items center
      justify-content space-around

      .tag-link-left
        width 60px
        min-width 60px
        height 60px
        background-size cover
        border-radius 25%

      .tag-link-right
        margin-left 1rem

        .tag-link-title
          font-size 1rem
          line-height 1.2

        .tag-link-sitename
          font-size 0.7rem
          color var(--tag-link-sitename-color)
          font-weight normal
          margin-top 4px
          transition color 0.3s

        &:hover .tag-link-sitename
          color var(--tag-link-hover-sitename-color)

      i
        margin-left auto
```

第三步：在markdown输入文本利用标签即可

```markdown
{% link your_title,website_title,website_url}
```

> <font color="deepskyblue">建议your_title写引用文章的题目，website_title写引用博主的网站名</font>