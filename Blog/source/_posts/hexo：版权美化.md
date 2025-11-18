---
title: hexo魔改：版权美化
tags:
  - hexo
categories:
  - 博客搭建
cover: /image/hexo.png
abbrlink: f32f8bf8
date: 2024-09-04 15:42:20
description: 自带的版权声明过于简单，添加样式实现版权美化
---
<meta name="referrer" content="no-referrer"/>

## 1. 效果预览

![](https://gitee.com/wyw_0227/picture-bed/raw/master/Hexo/202409041555121.png)

## 2. 教程

第一步：在路径`BlogRoot\themes\butterfly\layout\includes\post`下重写文件`post-copyright.pug`

```pug
if theme.post_copyright.enable && page.copyright !== false
  - let author = page.copyright_author ? page.copyright_author : config.author
  - let url = page.copyright_url ? page.copyright_url : page.permalink
  .post-copyright
    .post-copyright__title
      span.post-copyright-info
        h #[=page.title]
    .post-copyright__type
      span.post-copyright-info
        a(href=url_for(url))= theme.post_copyright.decode ? decodeURI(url) : url
    .post-copyright-m
      .post-copyright-m-info
        .post-copyright-a(style="display: inline-block;width: 120px")
            h 作者
            .post-copyright-cc-info
                h=author
        .post-copyright-c(style="display: inline-block;width: 120px")
            h 发布于
            .post-copyright-cc-info
                h=date(page.date, config.date_format)
        .post-copyright-u(style="display: inline-block;width: 120px")
            h 更新于
            .post-copyright-cc-info
                h=date(page.updated, config.date_format)
        .post-copyright-c(style="display: inline-block;width: 120px")
            h 许可协议
            .post-copyright-cc-info
                a.icon(rel='noopener' target='_blank' title='Creative Commons' href='https://creativecommons.org/')
                  i.fab.fa-creative-commons
                a(rel='noopener' target='_blank' title='CC BY 4.0' href='https://creativecommons.org/licenses/by/4.0/deed.zh') CC BY 4.0
```

第二步：在路径`BlogRoot\themes\butterfly\source\css_layout`下，修改`post.styl`文件

{% note warning flat %}修改范围：`.post-copyright` 至 `.post-outdate-notice`{% endnote %}

```Stylus
.post-copyright
    position: relative
    margin: 2rem 0 .5rem
    padding: .5rem .8rem
    border: 1px solid var(--light-grey)
    transition: box-shadow .3s ease-in-out
    overflow: hidden
    border-radius: 12px!important
    background-color: rgb(239 241 243)

    &:before
      background var(--heo-post-blockquote-bg)
      position absolute
      right -26px
      top -120px
      content '\f25e'
      font-size 200px
      font-family 'Font Awesome 5 Brands'
      opacity .2

    &:hover
      box-shadow: 0 0 8px 0 rgba(232, 237, 250, .6), 0 2px 4px 0 rgba(232, 237, 250, .5)

    .post-copyright
      &-meta
        color: $light-blue
        font-weight: bold

      &-info
        padding-left: .3rem

        a
          text-decoration: none
          word-break: break-word

          &:hover
            text-decoration: none

  .post-copyright-cc-info
    color: $theme-color;

  .post-outdate-notice
    position: relative
    margin: 0 0 20px
    padding: .5em 1.2em
    border-radius: 3px
    background-color: $noticeOutdate-bg
    color: $noticeOutdate-color
```

第三步：在路径`BlogRoot\source\css`下添加文件`copyright.css`，输入以下内容

{% note info flat %}<a href="https://dasi.plus/posts/ecc80865/">自定义CSS教程</a>{% endnote %}

```css
[data-theme="dark"]
  #post .post-copyright {
    background-color: rgb(7 8 10);
    text-shadow: #bfbeb8 1px 0 4px;
  }
[data-theme="dark"]
  #post .post-copyright {
    border: 1px solid rgb(19 18 18 / 35%);
  }
[data-theme="dark"]
  .post-copyright-info {
    color: #e0e0e4;
  }
#post .post-copyright__title{
    font-size:22px;
}
#post .post-copyright__notice{
    font-size:15px;
}
```

## 3. 参考链接

{% link butterfly版权美化教程,小N同学,https://www.imcharon.com/117/ %}