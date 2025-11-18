---
title: hexo魔改：右键菜单
tags:
  - hexo
categories:
  - 博客搭建
cover: /image/hexo.png
abbrlink: 1e3bf641
date: 2024-09-04 20:20:27
description: 传统右键是浏览器自带的，功能几乎用不到，自建一个右键菜单会十分个性化
---
<meta name="referrer" content="no-referrer"/>

## 1. 效果预览

在本页面点击右键即可

![](https://gitee.com/wyw_0227/picture-bed/raw/master/Hexo/202409042135193.png)

## 2. 教程

第一步：在路径`BlogRoot\themes\butterfly\layout\includes`下新建一个`rightmenu.pug`文件，填入以下代码

```pug
#rightMenu
  .rightMenu-group.rightMenu-small
    a.rightMenu-item(href="javascript:window.history.back();")
      i.fa-solid.fa-arrow-left
    a.rightMenu-item(href="javascript:window.location.reload();")
      i.fa-solid.fa-arrow-rotate-right
    a.rightMenu-item(href="javascript:window.history.forward();")
      i.fa-solid.fa-arrow-right
    a.rightMenu-item#menu-radompage(href="javascript:window.location.href = window.location.origin;")
      i.fa-solid.fa-house
  .rightMenu-group.rightMenu-line.hide#menu-text
    a.rightMenu-item(href="javascript:rmf.copySelect();")
      i.fa-solid.fa-copy
      span='复制'
  .rightMenu-group.rightMenu-line
    a.rightMenu-item(href="javascript:rmf.switchDarkMode();")
      i.fa-solid.fa-circle-half-stroke
      span='昼夜切换'
    a.rightMenu-item(href="javascript:rmf.switchReadMode();")
      i.fa-solid.fa-book
      span='阅读模式'
  .rightMenu-group.rightMenu-line
    a.rightMenu-item(href="javascript:rmf.scrollToTop();")
      i.fa-solid.fa-arrow-up
      span='置顶'
    a.rightMenu-item(href="javascript:rmf.copyPageUrl();")
      i.fa-solid.fa-link
      span='复制链接'
```

{% note danger flat %}pug文件对缩进非常敏感，所有子元素必须与父元素的缩进保持一致，用tab和用空格是不一样的！{% endnote %}

第二步：在路径`BlogRoot\themes\butterfly\layout\includes`下的`layout.pug`文件，在最下方的位置添加一行代码

```pug
include ./rightside.pug
!=partial('includes/third-party/search/index', {}, {cache: true})
!=partial('includes/rightmenu', {}, {cache: true}) // 这行是新增的
include ./additional-js.pug
```

第三步：在路径`BlogRoot\source\css`下新建`rightmenu.css`文件，填入以下代码

```css
/* rightMenu 右键菜单 */
#rightMenu{
	display: none;
	position: fixed;
	width: 160px;
	height: fit-content;
	top: 10%;
	left: 10%;
	background-color: var(--card-bg);
	border: 1px solid var(--font-color);
	border-radius: 8px;
	z-index: 100;
}
#rightMenu .rightMenu-group{
	padding: 7px 6px;
}
#rightMenu .rightMenu-group:not(:nth-last-child(1)){
	border-bottom: 1px dashed #4259ef23;
}
#rightMenu .rightMenu-group.rightMenu-small{
	display: flex;
	justify-content: space-between;
}
#rightMenu .rightMenu-group .rightMenu-item{
	height: 30px;
	line-height: 30px;
	border-radius: 8px;
	transition: 0.3s;
	color: var(--font-color);
}
#rightMenu .rightMenu-group.rightMenu-line .rightMenu-item{
	display: flex;
	height: 40px;
	line-height: 40px;
	padding: 0 4px;
}
#rightMenu .rightMenu-group .rightMenu-item:hover{
	background-color: var(--text-bg-hover);
}
#rightMenu .rightMenu-group .rightMenu-item i{
	display: inline-block;
	text-align: center;
	line-height: 30px;
	width: 30px;
	height: 30px;
	padding: 0 5px;
}
#rightMenu .rightMenu-group .rightMenu-item span{
	line-height: 30px;
}

#rightMenu .rightMenu-group.rightMenu-line .rightMenu-item *{
	height: 40px;
	line-height: 40px;
}
.rightMenu-group.hide{
	display: none;
}
```

第四步：在路径`BlogRoot\source\js`下新建`rightmenu.js`文件，填入以下代码

```js
// RightMenu 鼠标右键菜单
let rmf = {};

// 显示右键菜单
rmf.showRightMenu = function(isTrue, x=0, y=0){
    let $rightMenu = $('#rightMenu');
    $rightMenu.css('top',x+'px').css('left',y+'px');

    if(isTrue){
        $rightMenu.show();
    }else{
        $rightMenu.hide();
    }
}

// 昼夜切换
rmf.switchDarkMode = function(){
    const nowMode = document.documentElement.getAttribute('data-theme') === 'dark' ? 'dark' : 'light'
    if (nowMode === 'light') {
        activateDarkMode()
        saveToLocal.set('theme', 'dark', 2)
        GLOBAL_CONFIG.Snackbar !== undefined && btf.snackbarShow(GLOBAL_CONFIG.Snackbar.day_to_night)
    } else {
        activateLightMode()
        saveToLocal.set('theme', 'light', 2)
        GLOBAL_CONFIG.Snackbar !== undefined && btf.snackbarShow(GLOBAL_CONFIG.Snackbar.night_to_day)
    }
    // handle some cases
    typeof utterancesTheme === 'function' && utterancesTheme()
    typeof FB === 'object' && window.loadFBComment()
    window.DISQUS && document.getElementById('disqus_thread').children.length && setTimeout(() => window.disqusReset(), 200)
};

// 阅读模式
rmf.switchReadMode = function(){
    const $body = document.body
    $body.classList.add('read-mode')
    const newEle = document.createElement('button')
    newEle.type = 'button'
    newEle.className = 'fas fa-sign-out-alt exit-readmode'
    $body.appendChild(newEle)

    function clickFn () {
        $body.classList.remove('read-mode')
        newEle.remove()
        newEle.removeEventListener('click', clickFn)
    }

    newEle.addEventListener('click', clickFn)
}

// 复制文本
rmf.copySelect = function() {
  const selection = window.getSelection();
  const selectedText = selection.toString();
  if (selectedText) {
      navigator.clipboard.writeText(selectedText).then(function() {
          console.log('文本已复制到剪贴板');
      }).catch(function(err) {
          console.error('复制失败:', err);
      });
  } else {
      console.log('没有选中的文本');
  }
}

//回到顶部
rmf.scrollToTop = function(){
    btf.scrollToDest(0, 500);
}

//复制url
rmf.copyPageUrl = function(){
  const url = window.location.href;
  navigator.clipboard.writeText(url).then(function() {
      console.log('页面链接已复制到剪贴板');
  }).catch(function(err) {
      console.error('复制失败:', err);
  });
}


// 右键菜单事件
if(! (navigator.userAgent.match(/(phone|pad|pod|iPhone|iPod|ios|iPad|Android|Mobile|BlackBerry|IEMobile|MQQBrowser|JUC|Fennec|wOSBrowser|BrowserNG|WebOS|Symbian|Windows Phone)/i))){
    window.oncontextmenu = function(event){
        $('.rightMenu-group.hide').hide();
        //如果有文字选中，则显示 文字选中相关的菜单项
        if(document.getSelection().toString()){
            $('#menu-text').show();
        }

        // console.log(event.target);
        let pageX = event.clientX + 10;
        let pageY = event.clientY;
        let rmWidth = $('#rightMenu').width();
        let rmHeight = $('#rightMenu').height();
        if(pageX + rmWidth > window.innerWidth){
            pageX -= rmWidth+10;
        }
        if(pageY + rmHeight > window.innerHeight){
            pageY -= pageY + rmHeight - window.innerHeight;
        }



        rmf.showRightMenu(true, pageY, pageX);
        return false;
    };

    window.addEventListener('click',function(){rmf.showRightMenu(false);});
    // window.addEventListener('load',function(){rmf.switchTheme(true);});
}
```

## 3. 参考链接

{% link 【Hexo博客】魔改美化 Butterfly 主题右键菜单,百里飞洋,https://blog.meta-code.top/2022/06/12/2022-68/ %}