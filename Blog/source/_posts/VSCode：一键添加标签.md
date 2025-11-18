---
title: VSCode：一键添加标签
tags:
  - VSCode
categories:
  - 博客搭建
cover: /image/hexo.png
abbrlink: cbb2ed1a
date: 2024-09-04 17:59:03
description: 在VSCode编辑器下实现一键添加标签
---
<meta name="referrer" content="no-referrer"/>

## 1. 缘由

在用markdown写文章时，如果需要添加html/css标签，或者使用标签外挂的时候，需要多敲很多东西，这很不程序员（~~不是因为我懒~~），因此利用VSCode编辑器的自定义快捷键就可以实现一键添加标签

## 2. 教程

1. 根据图片提示，或者按下`ctrl k + ctrl s`，或者直接搜索文件`keybindings.json`

![](https://gitee.com/wyw_0227/picture-bed/raw/master/Hexo/202409042141449.png)

2. 添加以下内容
```json
// 将键绑定放在此文件中以覆盖默认值auto[]
[
    {
        "key": "ctrl+n",
        "command": "-workbench.action.files.newUntitledFile"
    },
    {
        "key": "f9 f9",
        "command": "python.execInTerminal-icon"
    },
    {
      "key": "ctrl+1",
      "command": "editor.action.insertSnippet",
      "when": "editorTextFocus",
      "args": {
        "snippet": "{% note  flat %}$TM_SELECTED_TEXT{% endnote %}",
      }
    },
    {
      "key": "ctrl+2",
      "command": "editor.action.insertSnippet",
      "when": "editorTextFocus",
      "args": {
        "snippet": "{% link ,,$TM_SELECTED_TEXT %}",
      }
    },
]
```

3. 自定义配置参数

- key：快捷键组合，可以自己选择
- command：`editor.action.insertSnippet`，用于插入代码片段
- when: `editorTextFocus`，编辑器文本框有焦点时快捷键才生效
- args：包含命令参数的对象，这里用来传递要插入`snippet`（一小段预定义的代码或文本）
- `$TM_SELECTED_TEXT`，是一个占位符，会被当前选中的文本替换`

{% note warning flat %}注意每一项之间有个英文逗号{% endnote %}

## 3. 参考链接

{% link 在 Visual Studio Code 中为代码片段（Code Snippets）添加快捷键,吕毅的博客,https://cloud.tencent.com/developer/article/1580595 %}