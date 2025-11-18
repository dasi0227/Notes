---
title: 利用html制作静态百度页面
tags:
  - HTML
categories:
  - 实验
cover: /image/default.png
description: 利用HTML和CSS的基础知识，尝试完成一个静态百度页面的制作
abbrlink: 31ce41b8
date: 2024-02-01 16:54:29
---
<meta name="referrer" content="no-referrer"/>

## 1. 页面预览

![](https://i-blog.csdnimg.cn/blog_migrate/1e2de0297750043a217faec0c1e81424.png)

## 2. 代码

<font color="orangered">CSS代码放在style标签内，没有单独成立文件</font>

```html
<!DOCTYPE html>
<html>
<head>
    <meta charset="utf-8">
    <title>百度一下，你就知道</title>
    <style type="text/css">
        /*清除元素默认性质*/
        body { 
            margin: 0;
            padding: 0;
            list-style: none;
            text-decoration: none;
            font-size: 1;
            font-family: "宋体";
            background-color: white;
        }

        /*全部a元素的基础属性*/
        a {     
            color: #00c;
            text-decoration: none;
        }
        a:hover{
            color:red;
            text-decoration: underline;
        }

        /*顶部的行*/
        #topline {  
            text-align: right;
            font-size:20px;
            margin:10px 10px;
        }

        /*百度图标*/
        #logo {  
            margin-top: 10px;
            text-align: center;
        }

        /*百度应用*/
        #apps {  
            margin-top: 20px;
            text-align: center;
            font-size: 30px;
            font-weight: bold;
        }

        /*搜索*/
        #search {
            margin-top: 20px;
            text-align: center;
        }
        #search #enter{  /*搜索内容*/
            width:600px;
            height:30px;
            font-size: 20px;
            font-weight: 400;
            vertical-align: middle;
            border: 1px solid black;
            border-radius: 10px 10px 10px 10px;
        }
        #search #submit{  /*搜索按钮*/
            width:100px;
            height:37px;
            font-size: 20px;
            font-weight: 500; 
            vertical-align: middle;
            cursor: pointer;
            color: white;
            background-color:#3836E0;
            border: 1px solid black;
            border-radius: 10px 10px 10px 10px;
        }

        /*热搜*/
        #hotnews #title {margin-top: 50px;}
        #hotnews #title a{
            font-size: 20px;
            font-family: Arial Bold;
            font-weight: 900;
            color:black;
            margin-left: 485px;
        }
        #hotnews #hotlist{
            display: flex;
            justify-content: center;
        }
        #hotnews #hotlist ul {
            padding-top: 5px;
            width: 280px;
            display: inline-block;
        }
        #hotnews #hotlist li{
            height: 36px;
            line-height: 36px;
            font-size: 20px;
            text-align: left;
        }
        #hotnews #hotlist a{
            height: 36px;
            line-height: 36px;
            font-size: 20px;
            padding-left: 20px;
        }
        #hotnews ul{list-style-type:none;}
        #hotnews #top3{font-weight: bold;}
        #hotnews #top3 #one,#hotnews #top3 #one a{color: #cc061d;}
        #hotnews #top3 #two,#hotnews #top3 #two a{color: rgb(240, 105, 15);}
        #hotnews #top3 #three,#hotnews #top3 #three a{color: #f0a923;}
        #hotnews #else ul li,#hotnews #else ul li a{color:#72747d}

        /*底部的行*/
        #bottomline{
            margin-top: 240px;
            position: absolute;
            left: 50%;    
            transform: translateX(-50%); 
        }
    </style>
</head>
<body>
    <div id="topline">
        <a href="https://www.baidu.com/gaoji/advanced.html">设置</a>
        |
        <a href="https://passport.baidu.com/">登录</a>
    </div>
    <div id="logo">
        <a href="https://www.baidu.com/" target="_blank"><img src="https://www.baidu.com/img/PCtm_d9c8750bed0b3c7d089fa7d55720d6cf.png" title="点此进入百度官网" width="370" height="180"></a>
    </div>
    <div id="apps">
        <a href="http://news.baidu.com/" target="_blank">新闻</a>
        <a href="https://map.baidu.com/" target="_blank">地图</a>
        <a href="http://image.baidu.com/" target="_blank">图片</a>
        <a href="https://haokan.baidu.com/" target="_blank">视频</a>
        <a href="http://tieba.baidu.com/" target="_blank">贴吧</a>
        <a href="https://wenku.baidu.com/" target="_blank">文库</a>
        <a href="https://baike.baidu.com/" target="_blank">百科</a>
        <a href="https://www.baidu.com/more/" target="_blank">更多>></a>
    </div>
    <div id="search">
        <input id="enter" type="text" maxlength="25" value="最多输入20个字"/>
        <input id="submit" type="submit" value="百度一下"/>
    </div>
    <div id="hotnews">
        <div id="title">
            <a href="https://top.baidu.com/" target="_blank">百度热搜></a>
        </div>
        <div id="hotlist">
            <div id="top3">
                <ul>
                    <li id="one">1<a href="https://pranx.com/win10-update/" target="_blank">北京申奥成功</a></li>
                    <li id="two">2<a href="https://pranx.com/win10-update/" target="_blank">吴亦凡被判入狱</a></li>
                    <li id="three">3<a href="https://pranx.com/win10-update/" target="_blank">中大即将迎来100年建校</a></li>
                </ul>
            </div>
            <div id="else">
                <ul> 
                    <li id>4<a href="https://pranx.com/win10-update/" target="_blank">骑士抢七大战胜勇士</a></li>
                    <li id>5<a href="https://pranx.com/win10-update/" target="_blank">姆巴佩世界杯决赛帽子戏法</a></li>
                    <li id>6<a href="https://pranx.com/win10-update/" target="_blank">火影忍者完结</a></li>
                </ul>
            </div>
        </div>
    </div>
    <div id="bottomline">
        <a href="https://home.baidu.com/" target="_blank">关于百度</a>
         | 
        <a href="https://e.baidu.com/" target="_blank">企业推广</a>
         | 
        <a href="https://www.baidu.com/duty/" target="_blank">使用前必读</a>
         | 
        <a href="https://help.baidu.com/" target="_blank">帮助中心</a>
         | 
        <a href="https://beian.mps.gov.cn/#/query/webSearch" target="_blank">京公网安备11000002000001号</a>
    </div>
</body>
</html>
```

## 3. 不足之处

- 由于设置“百度热搜”的时候使用的是margin-left: 485px，所以这一行字将与页面的左边缘保持485px的距离，不会随页面放缩而改变，达不到预期效果

![](https://i-blog.csdnimg.cn/blog_migrate/616efd445a82f6af95d40f2b31a0ad13.png)

- 笔者尚不知道如何得到正确的像素值，目前都是估计数值大小，观察页面效果来判断是否正确，所以出现许多奇奇怪怪的像素值

- 笔者尚不知道如何将一段文字放到页面底部的中央，所以还是使用了margin-top: 240px，如果还需要在两个块之间添加东西，则需要改变像素值，十分麻烦

## 4. 后续学习和改进

- 输入文本后，点击百度搜索应该会跳转到相关页面，同时百度热搜这一块应该是时刻更新的，而不是通过文本设定的
- 学习JavaScript变成动态页面

