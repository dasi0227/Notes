---
title: 利用telnet发送qq邮件
tags:
  - Network
categories:
  - 实验
description: 实现利用Windows自带的telnet发送qq邮件，解决了过程中遇到的问题
cover: /image/network.png
abbrlink: 4ec1858c
date: 2024-08-20 13:22:38
---
<meta name="referrer" content="no-referrer"/>

### 问题1：即使在控制面板启用telnet客户端也无法使用telnet
解决：使用管理员权限打开cmd，执行命令：`dism /online /Enable-Feature /FeatureName:TelnetClient`，之后根据弹出信息键入Y重启即可
> 参考链接：https://www.cnblogs.com/Nov13/p/17559005.html

### 问题2：总是出现`502 invalid input from xxx to xxx`报错
解决：使用587端口而不是25端口，因为587端口会对数据进行加密，安全性能比25端口好
> 参考链接：https://mp.weixin.qq.com/s/0eDdFEG1aUer1vQQ4qfP2g

### 问题3：QQ邮箱的登录需要获取授权码
解决：在个人的`QQ邮箱首页->设置->账号->POP3/IMAP/SMTP/Exchange/CardDAV/CalDAV服务`中开启服务，通过短信验证后获得授权码。注意，授权码只会在一开始显示，退出页面后无法查看，只能再次获取新的授权码，所以要保存好

### 问题4：邮箱号和授权码需要进行Base64编码
解决：工具网址：https://tool.chinaz.com/Tools/Base64.aspx

### 问题5：还是出现`502 invalid input from xxx to xxx`报错
解决：在网上找了一个小时解决方案也没找到，最后我惊奇地发现，应该是telnet编辑器的问题！就是当你输入错误的时候，使用backspace回退到某个位置重新输入，视觉上是覆盖错误字符实现修改，但实际上它仍保留了一些字符，通过发送邮件显示出来这些字符是`[C`或`[D`，至于为什么就不得而知了。因此只需要确保第一次输入没有任何错误即可！
> 其实输错了也没关系，再输一次正确的就好了，只不过邮件内容那里如果输错了就不能重来了

### 问题6：邮件格式
解决：仅针对qq邮件，其他邮件服务器可能有不同格式
- 元信息：不需要Base64编码
  - from:xxx@qq.com
  - to:xxx@qq.com
  - subject:xxx
- subject后需要空一行写邮件内容
- 单独一行输入英文句号`.`结束

### 整个过程
`>`行表示用户输入，注意第一次不要输错，**建议在其他地方输入好之后复制粘贴**
```
>telnet smtp.qq.com 587
220 newxmesmtplogicsvrszc5-2.qq.com XMail Esmtp QQ Mail Server.
>helo name
250-newxmesmtplogicsvrszc5-2.qq.com-30.174.48.222-23051354
250-SIZE 73400320
250 OK
>auth login
334 VXNlcm5hbWU6
>QQ邮箱的Base64编码
334 UGFzc3dvcmQ6
>授权码的Base64编码
235 Authentication successful
>mail from:<xxx@qq.com>
250 OK
>rcpt to:<xxx@qq.com>
250 OK
>data
354 End data with <CR><LF>.<CR><LF>.
>from:xxx@qq.com
>to:xxx@qq.com
>subject:主题名
> 
>邮件内容
>.
250 OK: queued as.
>quit
221 Bye.


遗失对主机的连接。
```

### 图示

![](https://gitee.com/wyw_0227/picture-bed/raw/master/Note/ComputerNetwork/course/202408181939041.png)

![](https://gitee.com/wyw_0227/picture-bed/raw/master/Note/ComputerNetwork/course/202408181939040.png)