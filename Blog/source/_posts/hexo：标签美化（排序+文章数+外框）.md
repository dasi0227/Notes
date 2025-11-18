---
title: hexo魔改：标签美化（排序+文章数+外框）
tags:
  - hexo
categories:
  - 博客搭建
cover: /image/hexo.png
abbrlink: 67f74a9a
date: 2024-09-04 14:33:04
description: 实现给标签添加文章数目的上下标
---
<meta name="referrer" content="no-referrer"/>

## 1. 效果预览

![](https://gitee.com/wyw_0227/picture-bed/raw/master/Hexo/202409041458633.png)

## 2. 教程

如何自定义CSS请看

{% link hexo 魔改：js 和 css 文件的添加,Dasi's Blog,https://dasi.plus/posts/ecc80865/ %}

第一步：在路径`BlogRoot\themes\butterfly\scripts\helpers`下找到`page.js`文件，在文件中找到函数`cloudTags`进行修改：

```javascript
hexo.extend.helper.register('cloudTags', function(options = {}) {
  const env = this
  // 设置标签排序：根据文章数目'length'从小到大排序，然后再翻转实现从大到小排序
  let source = options.source
  source = source.sort('length').reverse()
  // 设置标签上限：显示全部标签
  const limit = options.limit
  if (limit > 0) source = source.limit(limit)
  // 设置标签格式
  let result = ''
  source.forEach(tag => {
    // 随机取(100,100,100)~(255,255,255)的鲜艳颜色，为了更好地显示
    const color = 'rgb(' + Math.floor(Math.random()*156+100) + ', ' + Math.floor(Math.random()*156+100) + ', ' + Math.floor(Math.random()*156+100) + ')'
    // 增加 (${tag.length})内容，显示文章数目
    result += `<a href="${env.url_for(tag.path)}" style="color: ${color}">${tag.name} (${tag.length})</a>`
  })
  return result
})
```

第二步：在路径`BlogRoot\source\css`下新建文件`tag.css`，添加内容
```css
/* 侧栏标签 */
#aside-content .card-tag-cloud a {
  border: 1px solid;
  line-height: 1.5;
  border-radius: 6px;
  margin: 3px;
  padding: 0 5px;
}
/* 标签页 */
.tag-cloud-list a {
  border: 1px solid;
  line-height: 1.5;
  border-radius: 6px;
  padding: 5px 15px;
  font-size: 1.2rem;
  margin: 5px;
}
```

## 3. 补充

### 3.1 自定义文章数目格式

修改函数`cloudTags`
```js
/* 括号 */
result += `<a href="${env.url_for(tag.path)}" style="color: ${color}">${tag.name} (${tag.length})</a>`
/* 上标 */
result += `<a href="${env.url_for(tag.path)}" style="color: ${color}">${tag.name} <sup>${tag.length}</sup></a>`
/* 下标 */
result += `<a href="${env.url_for(tag.path)}" style="color: ${color}">${tag.name} <sub>${tag.length}</sub></a>`
```

### 3.2 自定义标签颜色

修改函数`cloudTags`
```js
// 预定义的颜色列表
const colors = [
    'rgb(255, 0, 0)',   // 红色
    'rgb(0, 255, 0)',   // 绿色
    'rgb(255, 165, 0)'  // 橙色
    /* more */
];
// 设置标签格式
let result = ''
source.forEach(tag => {
    // 从预定义的颜色列表中随机选择一种颜色
    const color = colors[Math.floor(Math.random() * colors.length)];
    result += `<a href="${env.url_for(tag.path)}" style="color: ${color}">${tag.name} (${tag.length})</a>`
})
return result
```

## 4. 参考链接

{% link Hexo博客标签的魔改,Leonus,https://blog.leonus.cn/2022/tags.html %}