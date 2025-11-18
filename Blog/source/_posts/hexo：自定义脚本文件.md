---
title: hexo魔改：自定义脚本文件
tags:
  - hexo
categories:
  - 博客搭建
cover: /image/hexo.png
abbrlink: 307cfcf5
date: 2024-09-03 15:36:26
description: 输入hexo三连过于繁琐，编写一个脚本文件实现一键预览和一键部署
---
<meta name="referrer" content="no-referrer"/>

## 1. 一键预览

创建一个文本文件（任意地址均可），然后输入一下内容，最后修改后缀名为`.bat`
```bat
@echo off
cd /d "BlogRoot"
call hexo clean
call hexo g
start cmd /k "hexo s && exit"
timeout /t 5 /nobreak >nul
start http://localhost:4000
```

`@echo off`：关闭命令回显，即执行命令的时候不显示命令，只显示结果

`cd /d "BlogRoot"`：切换到博客根目录，<font color="orangered">修改为你自己的地址</font>，`/d`选项允许更改驱动器及其目录

`call hexo clean`和`call hexo g`：执行相应命令

`start cmd /k "hexo s && exit"`：启动一个新的命令提示符窗口，运行hexo s命令，并命令执行完成后自动关闭窗口

> <font color="deepskyblue">为什么要开启一个新的窗口：因为hexo s执行需要手动键入`ctrl + c`才能终止，导致下一个命令不会执行，实现不了自动打开浏览器的效果</font>

`timeout /t 5 /nobreak >nul`：暂停，`\t 5`表示暂停5秒钟，`/nobreak`防止用户按任意键中断，`>nul`将输出重定向到空设备，屏蔽显示

> <font color="deepskyblue">为什么要暂停：本地服务器部署需要一定时间，如果立刻打开浏览器，会显示还没加载好或者还没加载完的页面，暂停可以确保打开浏览器直接预览</font>

`start http://localhost:4000`：启动默认浏览器并打开Hexo本地服务器的地址（默认端口是4000）

## 2. 一键部署

```bat
@echo off
cd /d "BlogRoot"
call hexo clean
call hexo g
call hexo d
```

原理同上，但是建议这里<font color="orangered">不要加入exit</font>，因为部署的时候可能会出错，需要查看error信息来debug，因此不能直接关闭窗口

> <font color="deepskyblue">如果有使用glup压缩，在`call hexo g`和`call hexo d`之间加入`call glup`</font>

## 3. 效果

双击批处理文件 (.bat)即可

![](https://gitee.com/wyw_0227/picture-bed/raw/master/Hexo/202409031706161.png)