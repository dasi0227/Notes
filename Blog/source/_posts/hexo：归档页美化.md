---
title: hexo魔改：归档页美化
tags:
  - hexo
categories:
  - 博客搭建
cover: /image/hexo.png
abbrlink: 2b7328c4
date: 2024-09-04 17:52:39
description: 默认归档页用时间轴过于单调，而且会很长，美化后实现双栏、动态变化和元信息展示
---
<meta name="referrer" content="no-referrer"/>

## 1. 效果预览

![](https://gitee.com/wyw_0227/picture-bed/raw/master/Hexo/202409041937490.png)

## 2. 教程

{% note info flat %}<a href="https://dasi.plus/posts/ecc80865/">自定义CSS教程</a>{% endnote %}

第一步：在路径`BlogRoot\source\css`下添加文件`layout.css`，并添加一些内容

```css
/* 归档页 */
.layout.hide-aside{
    max-width:1400px;
}

#archive,#tag,#category {
    background: var(--june-card-bg);
    padding: 25px 10px;
}

.article-sort-title{
    margin-top:30px;
    margin-bottom:20px;
}

.article-sort-item::before, .article-sort-title::before, .article-sort-title::after {
    content: none;
}

.article-sort .year{
    width:100%!important;
    border-bottom:dashed 5px var(--june-theme);
    font-size:26px;
    margin-top:20px;
}

.article-sort{
    border:none;
    display:flex;
    flex-wrap:wrap;
    margin:20px 20px;
    padding:0;
}

.article-sort-item:not(.year){
    padding:8px 10px;
    width:calc(50% - 0.8rem);
    margin:0.4rem;
    border:2px solid var(--june-theme);
    border-radius:15px;
    background:var(--card-bg);
    transition:0.5s;
    height:120px;
}

.article-sort-item-a{
    position:absolute;
    width:100%;
    height:100%;
}

.article-sort-item-img{
    transition:0.5s;
    height:90px;
    width:140px;
}

.article-sort-item > a >img{
    border-radius:15px;
}

.article-sort-item-title {
    font-size: 22px;
    padding-left: 10px;
    margin: 10px 0;
    line-height:25px;
    text-overflow:ellipsis;
}

.article-sort-item-title:hover{
    transform:none;
}

.article-sort-meta{
    height:max-content;
    position:relative;
}

.article-sort-meta > .article-meta-wrap{
    float:left;
}

.article-sort-meta > .article-sort-item-time{
    float:right;
}

.article-sort-item-categories,.article-sort-item-tags{
    margin:0 3px;
    padding:5px 8px;
    border-radius:25px;
    border:1px solid var(--dark-grey);
    font-size:12px;
    transition:0.5s;
}

.article-sort-item-info > div:not(.article-sort-meta){
    display:flex;
}

.article-sort-description,.article-sort-item > i{
    width:0;
    opacity:0;
    overflow:hidden;
    transition:0.5s;
}

.article-sort-description {
    width: 0;
    height: 59px;
    vertical-align: middle;
    margin: 5px 10px 0 15px;
    text-overflow:ellipsis;
}

.article-sort-item:hover:not(.year){
    background-color:var(--june-theme);
    box-shadow: 0 0 10px var(--june-theme);
}

.article-sort-item:hover:not(.year){
    background-color:var(--june-theme);
    box-shadow: 0 0 10px var(--june-theme);
}

.article-sort-item:hover:not(.year) .article-sort-description,.article-sort-item:hover:not(.year) > i{
    width:auto;
    opacity:1;
}

.article-sort-item:hover:not(.year) .article-sort-description{
    width:auto;
}

.article-sort-item:hover:not(.year) .article-sort-item-img{
    transition:0.5s;
    width:0;
}

.article-sort-item:hover:not(.year) .article-sort-item-title{
    color:var(--june-white)!important;
}

.article-sort-item:hover:not(.year) .article-meta-wrap a,.article-sort-item:hover:not(.year) .article-sort-description,.article-sort-item:hover:not(.year) .article-sort-item-time{
    color:var(--june-light-grey)!important;
}

.article-sort-item:hover:not(.year) .article-sort-item-categories{
    border:1.5px solid #212F3C;
}

.article-sort-item:hover:not(.year) .article-sort-item-tags{
    border:1.5px solid var(--june-blue);
}

.article-sort-item:hover:not(.year) .article-sort-item-categories:hover{
    background: #212F3C;
    box-shadow:0 0 5px #212F3C;
}

.article-sort-item:hover:not(.year) .article-sort-item-tags:hover{
    background: var(--june-blue);
    box-shadow:0 0 5px var(--june-blue);
}

@media screen and (max-width:768px) {
    .article-sort-item:not(.year) {
        width: 100%;
    }

    .article-sort-meta > .article-meta-wrap {
        display: none;
    }

    .article-sort-item-title {
        font-size: 16px;
    }

    .article-sort-item-img{
        width:90px;
    }
}
```

第二步：修改地址`BlogRoot\themes\butterfly\layout\includes\mixins`下的文件`\article-sort.pug`
```pug
mixin articleSort(posts)
  .article-sort
    - var year
    - posts.each(function (article) {
    - let tempYear = date(article.date, 'YYYY')
    - let no_cover = article.cover === false || !theme.cover.archives_enable ? 'no-article-cover' : ''
    - let title = article.title || _p('no_title')
    if tempYear !== year
      - year = tempYear
      .article-sort-item.year= year
    .article-sort-item(class=no_cover)
      a.article-sort-item-a(href=url_for(article.path) title=title)
      if article.cover && theme.cover.archives_enable
        a.article-sort-item-img(href=url_for(article.path) title=title)
          img(src=url_for(article.cover) alt=title onerror=`this.onerror=null;this.src='${url_for(theme.error_img.post_page)}'`)
      .article-sort-item-info
        div
          a.article-sort-item-title(href=url_for(article.path) title=title)= title
          .article-sort-description= article.description
        .article-sort-meta
          .article-meta-wrap
            if (theme.post_meta.page.categories && article.categories.data.length > 0)
              span.article-sort-item-categories
                each item, index in article.categories.data
                  a(href=url_for(item.path)).article-meta__categories #[=item.name]
                  if (index < article.categories.data.length - 1)
                    i.fas.fa-angle-right
            if (theme.post_meta.page.tags && article.tags.data.length > 0)
              each item, index in article.tags.data
                span.article-sort-item-tags
                  a(href=url_for(item.path)).article-meta__tags #[=item.name]
                  if (index < article.tags.data.length - 1)
                    span.article-meta__link
          .article-sort-item-time
            i.far.fa-calendar-alt
            time.post-meta-date-created(datetime=date_xml(article.date) title=_p('post.created') + ' ' + full_date(article.date))= date(article.date, config.date_format)
      i.fas.fa-chevron-right
    - })
```


## 3. 参考链接

{% link Butterfly归档、分类、标签美化,June's Blog,https://blog.june-pj.cn/posts/136bc46a/ %}