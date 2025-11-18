---
title: 应用层
tags:
  - Network
categories:
  - 笔记
description: 体系结构，HTTP，SMTP，DNS，CDN，P2P和socket
cover: /image/network.png
abbrlink: ab07b2ac
date: 2024-08-20 18:15:10
---
<meta name="referrer" content="no-referrer"/>

## 1. 网络应用原理

### 1.1 应用体系结构

客户-服务器体系结构（Client-Server）：一台主机充当服务器，其他主机充当客户，客户向服务器发送请求，服务器处理这些请求并返回响应
  - 客户之间不直接通信
  - 服务器需要同时服务多个客户

对等体系结构（Peer-to-Peer,P2P）：所有端点在网络中具有相同的地位，每个端点既可以充当客户也可以充当服务器
  - 对等方之间可以直接通信
  - 对等分即可以请求，也可以服务

![](https://gitee.com/wyw_0227/picture-bed/raw/master/Note/ComputerNetwork/chapter2/202408201713829.png)

### 1.2 进程通信

客户是发起通信的进程，服务器是在会话中监听请求的进程

套接字（socket）：是进程与计算机网络之间的可编程接口，是网络服务的应用编程接口（Application Programming Interface,API）

服务寻址：既要确定主机地址（IP地址），也需要确定进程地址（端口号）

![](https://gitee.com/wyw_0227/picture-bed/raw/master/Note/ComputerNetwork/chapter2/202408201713830.png)

### 1.3 应用服务

- 可靠性：是否确保数据在运输过程中不会丢失、重复或损坏，并且能够被接收方完整地接收到
- 带宽：发送进程能够向接收进程交付比特的速率的下限
- 定时：发送方注入套接字的每个比特到达接收方的套接字的时长上限
- 安全性：是否对数据进行加密处理

![](https://gitee.com/wyw_0227/picture-bed/raw/master/Note/ComputerNetwork/chapter2/202408201713831.png)

## 2. HTTP

### 2.1 WWW

**万维网（World Wide Web, WWW）**：是一个全球性的、分布式的、联机的信息系统
- **统一资源定位符（Uniform Resource Locator, URL）**：负责唯一标识万维网上的各种文档和资源
- **超文本传输协议（HyperText Transfer Protocol, HTTP）**：是万维网客户和万维网服务器进程之间传输数据所遵守的协议
- **超文本标记语言（HyperText Markup Language, HTML）**：用于Web页面的标记语言

**浏览器（browser）**：作为 WWW 中的客户端，根据用户输入或点击的 URL，向服务器发送 HTTP 请求来获取资源，同时将资源进行解析与渲染，从而呈现给用户

URL 格式：`<协议>://<主机>:<端口>/<路径>`
- 协议：用什么协议来获取万维网文档，如HTTP传输Web页面，FTP传输文件
- 主机：存放资源的主机在因特网中的域名或IP地址
- 端口：主机的服务进程所使用的端口号，如 HTTP 是 80 端口
- 路径：资源在主机上的具体位置

### 2.2 HTTP 流程

非持续连接：客户端每发起一个请求，就需要与服务器建立一个新的TCP连接，就会导致 2RTT 的开销

持续连接：客户端和服务器可以在同一个TCP连接上发送多个请求和响应
- 非流水线：完成一个请求才能发下一个请求
- 流水线：可以并发多个请求，而无需等待前一个请求完成

![](https://gitee.com/wyw_0227/picture-bed/raw/master/Note/ComputerNetwork/chapter2/202408201713833.png)

{% note warning flat %}
- HTTP是无连接的，这里的连接指的是HTTP依赖于底层TCP的连接
- HTTP是无状态的，服务器不会记录 HTTP 的客户信息
{% endnote %}

### 2.3 HTTP 报文格式

#### 2.3.1 请求报文

- **请求行**
  - 请求方法：声明请求的类型
    - GET：从服务器获取指定资源
    - POST：向服务器提交数据
    - PUT：更新或创建资源
    - HEAD：获取指定资源的元数据，不包括响应体
    - DELETE：请求删除服务器指定资源
    - PATCH：对指定资源进行部分修改
  - URL：指定请求的资源路径
  - HTTP版本：HTTP/1.1或HTTP/2或HTTP/3
- 首部行：每行都是一个键值对
  - Host：指示域名
  - User-Agent：浏览器类型
  - Connection：连接类型
  - Accept-Language：请求的语言版本
- 空行：首部行与实体体之间存在一个空行
- 实体体：要发送到服务器的数据（如账户密码，搜索码等）

![](https://gitee.com/wyw_0227/picture-bed/raw/master/Note/ComputerNetwork/chapter2/202408201713834.png)

```
PUT /path/to/index.html HTTP/1.1
Host: www.example.com
Connection: Keep-Alive
User-agent: Mozilla/5.0
Accept-language: cn

{
  "name": "Dasi",
  "school": "SYSU"
}
```

#### 2.3.2 响应报文

- **状态行**
  - HTTP版本：HTTP/1.1或HTTP/2或HTTP/3
  - 状态码和短语
    - 200 OK：表示服务器接受请求
    - 400 Bad Request：表示服务器不理解请求
    - 404 Not Found：表示服务器发现请求路径下不存在资源
- 首部行：每行都是一个键值对，其中键又称为**标头**
  - Date：响应报文的生成时间
  - Expires：响应的过期时间
  - Server：服务器类型
  - Connection：连接类型
  - Location：用于重定向的URL
  - Cache-Control：缓存控制指令
  - Content-Type：响应实体的数据类型
- 空行：首部行与实体体之间必须存在一个空行
- 实体体：从服务器获取的数据，如获取Web网页就是获取一个HTML文件

![](https://gitee.com/wyw_0227/picture-bed/raw/master/Note/ComputerNetwork/chapter2/202408201713835.png)


```
HTTP/1.1 200 OK
Connection: close
Date: Fri, 16 Aug 2024 12:00:00 GMT
Server: Apache/2.2.3 (CentOS)
Cache-Control: private, max-age=0
Content-Type: text/html; charset=UTF-8
Content-Length: 138

<!DOCTYPE html>
<html>
<head>
    <title>Sample Page</title>
</head>
<body>
    <h1>Hello, World!</h1>
    <p>This is a sample HTML response.</p>
</body>
</html>
```

### 2.4 Cookie

定义：是服务器发送到浏览器并保存在本地的一小块数据，浏览器会存储cookie并在下次向同一服务器发起请求时携带并发送到服务器上，是**键值对形式的小型文本文件**
- 会话状态管理：记录账号密码、登录状态、购物车和游戏分数等用户信息
- 个性化设置：用户自定义的浏览器偏好设置
- 行为跟踪：跟踪用户行为，用于分析用户、提供广告或改进服务

工作流程
1. 服务器设置Cookie：浏览器首次访问服务器时，请求报文中没有Cookie信息，服务器通过**Set-Cookie标头**在响应中将Cookie发送给浏览器
2. 浏览器存储Cookie：浏览器接收到Set-Cookie后，将其存储在本地
3. 客户端发送Cookie：在后续的请求中，浏览器通过**Cookie标头**在请求中附带信息，以便服务器识别和处理

常见的Cookie值
- Id：当前用户的Cookie名称
- expires：指定Cookie的过期时间（绝对时间）
- max-age：指定了从设置Cookie时间开始的有效时间长度（相对时间）
- path：指定Cookie的有效路径
- domain：指定可以访问Cookie的域名
- secure：指定是否使用HTTPS安全协议发送Cookie
- HttpOnly: 防止客户端脚本通过document.cookie属性访问Cookie

Cookie的生命周期
- 会话性：在关闭浏览器时会被自动删除
- 持久性：Cookie会一直保留在浏览器直到到达过期时间或被手动删除

![](https://gitee.com/wyw_0227/picture-bed/raw/master/Note/ComputerNetwork/chapter2/202408201713836.png)

### 2.5 Web缓存

Web缓存器(Web cache) / 代理服务器(proxy server)：代表初始Web服务器来满足HTTP请求的网络实体，具有自己的磁盘存储空间，保存最近请求过的对象的副本
- 大大减少请求的响应时间
- 减少一个机构的接入链路的通信量，进而无需增大带宽，节约成本
- 从整体上大大减少因特网上的Web流量，改善所有应用性能

流程
1. 浏览器创建一个到Web缓存器的TCP连接，并向其中对象发送一个HTTP请求报文
2. Web缓存器检查本地是否存储了对象副本，如有副本则向浏览器发送一个具有该对象的HTTP响应报文
3. 如Web缓存器没有对象副本，则会创建一个与该对象的初始服务器的TCP连接，然后向初始服务器中的对象发送一个HTTP请求报文
4. 初始服务器会向该Web缓存器发送一个具有该对象的HTTP响应报文
5. Web缓存器接收到该对象后，在本地存储空间保存一份副本，并向浏览器发送一个具有该对象的HTTP响应报文

{% note success flat %}
假设浏览器通过局域网接入因特网，则**响应时延 = 局域网时延 + 接入时延 + 因特网时延**
其中局域网的流量强度为0.2，接入链路的流量强度为0.9，因特网时延为2秒，Web缓存器的命中率为0.4，Web缓存器的访问时间为0.01秒，当流量强度小于0.8时可以忽略不计时延

- 初始：因为接入链路的流量强度为0.9，则响应时延会变得非常大
- 方案1：增大接入链路的带宽，使其流量强度降维0.2，则响应时间变为2s
- 方案2：安装一个Web缓存器，则响应时间变为0.4×0.01s+0.6×2.01s=1.21s

方案2的开销比方案1低得多，而且方案2的效果比方案1还要好得多
{% endnote %}

### 2.6 HTTP/2

|区别|HTTP/1.1|HTTP/2|
|-|-|-|
|数据格式|文本格式|二进制格式|
|多路复用|一个TCP连接一次只能处理一个对象|一个TCP连接可以同时处理多个对象|
|首部压缩|以明文形式发送|使用压缩算法|
|服务器推|客户必须请求每个对象|服务器可以主动推送关联对象|
|响应次序|时间次序|支持响应报文的优先级，根据请求的重要性优化对象加载顺序|

队首阻塞(Head Of Line,HOL)：队首请求在遇到延迟或阻塞时，会导致后续的请求无法被处理，直到前面的请求处理完成
  - HTTP/1.1解决：打开多个并行TCP连接，共享可用带宽
  - HTTP/2解决：将每个HTTP报文分成独立的小帧，然后交错发送，并在接收端将它们重新装配起来

## 3. SMTP

### 3.1 电子邮件系统

组成部分
- **用户代理**：是用户与电子邮件系统的接口
- **邮件服务器**：用于发送、接受、存储和通告电子邮件的服务器
- **邮件发送和接收协议**：用户代理向邮件服务器或者邮件服务器之间发送邮件使用 SMTP，用户代理从邮件服务器接受邮件使用 POP3/IMAP
- **邮箱(mailbox)**：具有专属的电子邮件地址，是邮件服务器下的一块存储区域

{% note warning flat %}
邮件服务器既表现为SMTP客户，也表现为SMTP服务器
{% endnote %}

流程
1. 发送方编写好电子邮件后，将邮件提交给发送方用户代理
2. 发送方用户代理使用SMTP协议将电子邮件传输到发送方邮件服务器的缓存队列中
3. 发送方的邮件服务器从缓存队列中提取该电子邮件，并创建了一个与接收方邮件服务器的TCP连接
4. 发送方服务器使用SMTP协议将电子邮件传输到接收方邮件服务器的邮箱中
5. 接收方用户代理使用POP3/IMA协议从接收方邮件服务器的邮箱中获取邮件

![](https://gitee.com/wyw_0227/picture-bed/raw/master/Note/ComputerNetwork/chapter2/202408201713826.png)

### 3.2 电子邮件协议

类型
- 简单邮件传输协议（Simple Mail Transfer Protocol, SMTP）：用于发送邮件，使用端口25
- 邮局通讯协议（Post Office Protocol, POP）：用于接收邮件，使用端口110
- 因特网邮件访问协议（Internet Message Access Protocol, IMAP）：用于管理邮件，使用端口143

SMTP握手阶段
1. 建立连接：客户端通过TCP连接到邮件服务器的端口（默认端口为25，但也可以是587或465，具体取决于是否使用加密），服务器会响应一个以`220`开头的代码，表示服务器已经准备好接受命令
2. 开始对话：客户端发送`HELO`命令表示开始会话，服务器会响应一个以`250`开头的代码
3. 认证：客户端发送`AUTH LOGIN`命令进行认证，服务器会做出响应并要求用户提供用户名和密码
4. 指定发件人：客户端`MAIL FROM:<xxx@example.com>`命令指定邮件的发件人地址，服务器会响应一个以`250`开头的代码
5. 指定收件人：客户端`RCPT TO:<xxx@example.com>`命令指定邮件的发件人地址，服务器会响应一个以`250`开头的代码
6. 开始撰写：客户端发送`DATA`命令表示将开始发送邮件正文，服务器会响应一个以`354`开头的代码
7. 发送报文：客户端发送邮件报文，最后以单独的`.`结束邮件内容，服务器会响应一个以`250`开头的代码并排队处理
8. 结束会话：客户端发送`QUIT`命令表示会话结束，服务器会响应一个以`221`开头的代码

![](https://gitee.com/wyw_0227/picture-bed/raw/master/Note/ComputerNetwork/course/202408181939041.png)

SMTP报文
1. 首部/头部：包含关于邮件的元数据，如发件人、收件人、主题等，格式是键值对字段，每个字段占据一行
  - From: 发件人地址
  - To: 收件人地址
  - Cc: 抄送地址
  - Bcc: 密送地址
  - Subject: 邮件主题
  - Date: 邮件发送日期
  - Reply-To: 回复地址
2. 正文：与头部之间隔一个空行，包含邮件的实际内容（纯文本、HTML、附件等），通常使用MIME格式来组织

## 4. DNS

### 4.1 域名

主机标识的两种方式
- IP地址（对计算机友好）
  - IPv4地址：32位地址，表示为4个十进制数，通过`.`分隔，如`192.0.2.172`
  - IPv6地址：128位地址，表示为8组16进制数，通过`:`分隔，如`2001:0db8:8b73:0000:0000:8a2e:0370:1337`
- 域名（对人友好）
  - 顶级域名：通常表示国家、地区或机构类型，如`.cn`表示中国、`.us`表示美国、如`.com`表示公司、`.gov`表示政府机构
  - 二级域名：通常表示组织、公司或品牌名称，如`.google`表示谷歌、`.baidu`表示百度
  - 三级域名：通常表示服务类型或子部门，如`.www`表示Web服务、`.mail`表示邮件服务、`.blog`表示博客服务

域名服务器：是域名系统的核心组件，负责将人类可读的域名转换为计算机可识别的IP地址
- 根域名服务器：管理顶级域名的域名服务器地址
- 顶级域名服务器：管理特定顶级域名下的二级域名服务器地址
- 权威域名服务器：管理特定域名的IP地址
- 本地域名服务器：代表客户主机向其他域名服务器发起查询，并将结果返回给客户主机

![](https://gitee.com/wyw_0227/picture-bed/raw/master/Note/ComputerNetwork/chapter2/202408201713817.png)

### 4.2 域名查询

多级域名服务器的意义：只有权威域名服务器才真正存储并返回域名与IP地址的映射关系，而根域名服务器和顶级域名服务器的作用主要是引导查询请求，将请求逐步转移到更具体的服务器上，主要目的是分担查询压力，并提高域名查询的效率和可靠性

查询方式
- 递归查询：本地域名服务器只需向根域名服务器查询一次，后面几次查询都是递归地在几个域名服务器之间进行
- 迭代查询：本地域名服务器先向根域名服务器查询，然后再向顶级域名服务器查询，最后向权威域名服务器查询

![](https://dasi-blog.oss-cn-guangzhou.aliyuncs.com/ComputerNetwork/chapter1-2/202501051654373.png)

DNS缓存（caching）：会缓存从其他DNS服务器获得的解析结果，减少对上游DNS服务器的请求频率，包括对域名-IP地址的缓存和对DNS服务器-IP地址的缓存

{% note info flat %}
事实上，绝大部分的DNS查询都绕过了根服务器
{% endnote %}

流程：假设客户端以迭代方式查询`www.baidu.com`
1. 客户端首先查询本地DNS服务器缓存，是否存在IP地址或者域名服务器的记录
2. 本地DNS服务器将查询请求发送到根DNS服务器，根DNS服务器根据`.com`返回顶级域DNS服务器的IP地址
3. 本地DNS服务器将请求发送到顶级域DNS服务器，顶级域DNS服务器根据`.baidu`返回权威DNS服务器的IP地址
4. 本地DNS服务器将请求发送到权威DNS服务器，权威DNS服务器根据`www.baidu.com`返回域名的IP地址
5. 本地DNS服务器获取到IP地址后缓存，然后返回到客户端

{% note warning flat %}
如果还存在四级甚至五级域名，需要查询多次权威DNS服务器
{% endnote %}

### 4.3 DNS记录

资源记录（Resource Record, RR）：
- Name：域名
- Value：根据Type决定Name映射的值
- Type：资源记录的类型
- TTL：能够在缓存中的存活时间

类型
|Type|Name|Value|Example|
|-|-|-|-|
|A|域名|IPv4地址|(www.baidu.com, 119.75.217.109, A, TTL)|
|AAAA|域名|IPv6地址|(www.baidu.com, 2409:8c54:870:34e:0:ff:b024:1916 AAAA, TTL)|
|CNAME|域名|另一个域名|(dasi.plus, dasi0227.github.io, CNAME, TTL)|
|NS|域名|权威DNS服务器的域名|(baidu.com, ns1.baidu.com, NS, TTL)|
|MX|域名|邮件服务器的域名|(qq.com, mail.qq.com, MX, TTL)|

### 4.4 DNS报文

DNS只有查询报文和回答报文，且具有相同格式
- 首部区域：报文的元信息
  - 标识符：唯一标识当前DNS查询报文和DNS响应报文
  - 标志：报文的类型，响应的状态，查询的方式等
  - 问题数：问题区域中问题的数量
  - 回答RR数：回答区域中的RR数量
  - 权威RR数：权威区域中的RR数量
  - 附加RR数：附加信息区域中的RR数量
- 问题区域：查询的具体信息
- 回答区域：响应的具体信息
- 权威区域：提供有关DNS服务器的信息
- 附加信息区域：提供额外的信息，有助于解析问题

![](https://gitee.com/wyw_0227/picture-bed/raw/master/Note/ComputerNetwork/chapter2/202408201713820.png)

## 5. P2P

### 5.1 自扩展性

因特网核心具有足够带宽，瓶颈都在因特网的接入链路
- 上载(upload)：将数据从本地传输到因特网，速率以$u$表示
- 下载(download)：将数据从因特网传输到本地，速率以$d$表示
- 分发时间(distribution)：所有N个对等方得到文件副本F比特所需要的时间

![](https://gitee.com/wyw_0227/picture-bed/raw/master/Note/ComputerNetwork/chapter2/202408201713821.png)

客户-服务器体系结构：服务器必须向全部对等方都传输一个副本，则一共要上载NF比特
- 服务器的上载时间：${NF}/{u_s}$
- 客户的下载时间：${F}/{d_c}$
- 分发时间：$D_{cs} \geq max\{NF/u_s,F/d_c\}$

P2P体系结构：每个对等方都可以帮助服务器分发副本，因此上载能力等于服务器的上载速率与对等方的上载速率之和
- 首次服务器上载时间：$F/u_s$
- P2P整体的上载时间：$NF/(u_s+u_{c1}+u_{c2}+....+u_{cN})$
- 对等方的下载时间：$F/d_c$
- 分发时间$D_{P2P} \geq max{F/u_s,F/d_c,NF/(u_s+u_{c1}+u_{c2}+....+u_{cN})}$

自扩展性：对等方除了是比特的消费者，还是它们的重新分发者

![](https://gitee.com/wyw_0227/picture-bed/raw/master/Note/ComputerNetwork/chapter2/202408201713822.png)

### 5.2 BitTorrent

术语
- 洪流(torrent)：参与一个特定文件分发的所有对等方的集合
- 种子(seeder)：已经下载了整个文件并留在洪流中继续上载块的对等方
- 文件块(chunk)：洪流中分发的文件被划分为的较小的数据块，通常为256KB
- 追踪器(tracker)：用于协调参与洪流的对等方之间的通信
- 邻近对等方(neighboring peers)：同一洪流中与当前对等方直接相连的其他对等方

流程：
1. 客户下载`.torrent`文件加入洪流成为对等方
2. 追踪器从洪流中随机选取若干个对等方与当前对等方直接相连
3. 对等方周期性地询问每个邻近对等方所具有的快列表
4. 对等方向邻近对等方请求它还没有的块
5. 对等方获得整个文件后，可以离开洪流，也可以留在洪流成为种子 

机制
- 最稀缺优先(rarest first)：优先下载邻近对等方中数量最少的块->目的是为了均衡每个块在洪流中的副本数量
- 一报还一报(tit-for-tat)：对等方A会周期性测量从对等方B接收到比特的速率，对等方B也会周期性测量从对等方A接收到比特的速率，如果对等方A和B都满足与此速率，则它们之间保持疏通->目的是对等方能够以趋向于找到彼此协调的速率上载

![](https://gitee.com/wyw_0227/picture-bed/raw/master/Note/ComputerNetwork/chapter2/202408201713823.png)

## 6. CDN

### 6.1 比特率

**比特率(bitrate)**：单位时间传输的比特量，衡量了**视频的压缩质量即视频的清晰度**
- 空间冗余：相邻的像素通常具有相似的颜色和亮度，因此可以用更少的数据来表示这些相似的像素
- 时间冗余：相邻帧之间的变化通常很小，因此可以只记录变化的部分而不是每一帧的完整数据

常见的清晰度和比特率关系
|清晰度|分辨率/px/|比特率/Mbps|
|-|-|-|
|标清(Standard Definition,SD)|720x480|1-2.5|
|高清(High Definition,HD)|1280x720|2.5-5|
|全高清 (Full High Definition,Full HD)|1920x1080|5-10|
|4K超高清(Ultra High Definition,4K UHD)|3840x2160|15-50|
|8K超高清(Ultra High Definition,8K UHD)|7680x4320|50-100|

### 6.2 DASH

HTTP流：通过HTTP协议传输和播放多媒体内容的技术
- 分段传输：媒体内容被分成多个片段，每个片段通过HTTP协议逐段传输
- 实时播放：浏览器接收到的片段只要超过预先设定的门限，就可以开始播放，而不用等到所有数据都下载完成

动态适应性流（Dynamic Adaptive Streaming, DASH）：允许客户自由地在视频不同的质量等级之间切换
1. 客户首先请求HTTP服务器获得一份告示文件，其中提供了各个版本视频的URL及其比特率
2. 客户根据可用宽带动态地请求来自不同版本的视频的片段，同时运行一个速率决定算法来选择下次请求的片段

### 6.3 CDN

为什么不建立单一的大规模数据中心来传输流式视频？
- 若客户远离数据中心，分组将跨越许多通信链路，带来很高的时延
- 流行的视频可能会经过相同的通信链路发送许多次，浪费了网络带宽，因特网公司不得不付费给ISP运营商
- 单点故障，即数据中心崩溃会导致任何视频流无法传输

内容分发网（Content Distribution Network, CDN）：是一种分布式的网络架构，通过在地理上分散的多个服务器上缓存和分发内容，来实现更快的访问速度和更高的可靠性

CDN的流程：假设URL是`http://video.baidu.com/movie`
1. 用户的客户端发起一个DNS查询请求，向本地DNS服务器询问video.baidu.com的IP地址
2. 用户的本地DNS服务器中继DNS请求到baidu的权威服务器
3. baidu的权威服务器不会直接返回域名的IP地址，而是返回baiduCDN的权威服务器地址
4. 用户的本地DNS服务器再一次中继DNS请求到baiduCDN的权威服务器
5. baiduCDN的权威服务器返回合适的CDN边缘服务器的IP地址
6. 用户的本地DNS服务器将CDN边缘服务器的IP地址返回给浏览器
7. 浏览器与CDN边缘服务器建立了一条直连的TCP连接，然后开始传输数据

CDN边缘服务器的选择策略
- 地理位置最近（geographically closet）：选择距离用户最近的CDN边缘服务器
- 基于响应时间/网络质量：对时延和丢包率进行周期性地实时测量
- 负载均衡：选择当前负载较低的CDN边缘服务器