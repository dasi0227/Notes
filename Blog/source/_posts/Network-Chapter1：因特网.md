---
title: 因特网
tags:
  - Network
categories:
  - 笔记
description: 因特网，网络边缘，网络核心，分组交换网，协议层次和网络攻击
cover: /image/network.png
abbrlink: 99ade850
date: 2024-08-20 18:12:42
---
<meta name="referrer" content="no-referrer"/>

## 1. 因特网

### 1.1 因特网组成

网络（network）：由若干节点和连接这些节点的链路组成

节点：计算设备，又称为**主机（host）**或**端系统（end system）**，如计算机、交换机、路由器、集线器等

链路：**通信链路（communication link）**，分为有线链路和无线链路，如光纤、铜缆、无线电等

**分组/包（packet）**：是网络中数据传输的基本单位

**交换机（switch）**：将若干个计算机连成一个小网络

**路由器（router）**：将若干个小网络连成一个大网络

**链路(route/path)**：一个分组从一台主机经历一系列路由器和交换机到另一台主机的路径

**互连网（internet）**：由若干网络和连接这些节点网络的路由器组成，即**网络的网络**

**因特网/互联网（Internet）**：世界范围的互连网

{% note warning flat %}
互连网是一个通用名词，泛指一切网络互连形成的网络，而因特网是一个专有名词，特指遵循TCP/IP协议且覆盖全球的一个特殊互连网
{% endnote %}

![](https://gitee.com/wyw_0227/picture-bed/raw/master/Note/ComputerNetwork/chapter1/202408121410616.png)

### 1.2 因特网服务

1. 数据通信
2. 资源共享
3. 分布式处理
4. 提高可靠性
5. 负载均衡

### 1.3 因特网协议

**报文（message）**：是网络中交换与传输的数据单元

**协议的内容**：定义了通信实体之间交换的报文的格式和顺序，以及报文发送/接受一条报文时所采取的动作

最常见的四种协议
- **传输控制协议（Transmission Control Protocol,TCP）**:规定了在网络通信中如何确保数据传输的可靠性和顺序性
- **互联网协议（Internet Protocol,IP）**：规定了在互联网上如何寻址和路由
- **超文本传输协议（Hypertext Transfer Protocol,HTTP）**：规定了在Web浏览器和Web服务器之间如何传输和交换超文本文档
- **简单邮件传输协议（Simple Mail Transfer Protocol,SMTP）**：规定了在网络上如何传输电子邮件

## 2. 网络边缘

### 2.1 端

端系统（End System）：位于因特网的边缘，即无法再向外层拓展，如桌面计算机，移动计算机，客户端，服务器

主机：是容纳应用程序的机器的统称

**客户机（client）**：请求服务或资源的一端

**服务器（server）**：提供资源或服务的一端

{% note info flat %}

|区别|处理器|操作系统|硬件标准|
|-|-|-|-|
|PC|基于Intel或AMD的x86处理器|Windows、Linux|IBM PC硬件标准|
|MAC|基于ARM的M系列处理器|macOS|苹果自家设计的硬件标准|

{% endnote %}

### 2.2 接入网

**接入网（access network）**：将端系统连接到边缘路由器的网络

**边缘路由器（edge router）**：端系统到任何其它远程系统的路径上的第一台路由器

#### 2.2.1 家庭接入

- **数字用户线（Digital Subscriber Line,DSL）**：家庭通过本地电话线接入的本地电话公司处获得因特网接入
- **电缆（cable）**：家庭通过本地电视线接入的本地电视公司处获得因特网接入
- **光纤到户（Fiber To The Home,FTTH）**：直接将光纤连接到家庭
- **无线宽带**：数据以无线方式从供应商基站发送到家庭中的调制解调器

![](https://gitee.com/wyw_0227/picture-bed/raw/master/Note/ComputerNetwork/chapter1/202408121410617.png)
![](https://gitee.com/wyw_0227/picture-bed/raw/master/Note/ComputerNetwork/chapter1/202408121410620.png)
![](https://gitee.com/wyw_0227/picture-bed/raw/master/Note/ComputerNetwork/chapter1/202408121410618.png)

#### 2.2.2 公司/学校接入

- **以太网（Ethernet）**：是一种有线的局域网技术，使用物理连接将设备连接到局域网
- **无线保真（Wireless Fidelity,WiFi）**：是一种无线的局域网技术，使用无线信号将设备连接到局域网

![](https://gitee.com/wyw_0227/picture-bed/raw/master/Note/ComputerNetwork/chapter1/202408121419018.png)

#### 2.2.3 广域接入

- **蜂窝网（Cellular Network）**：通过无线信号将移动设备连接到分布在全国各地的移动网络提供商的基站，从而接入因特网（3G，4G，5G）
- **无线广域网（Wireless Wide Area Network,WWAN）**：使用卫星、WiFi或专用的长距离无线连接来提供广域的互联网接入服务

### 2.3 传输媒介

|类型|媒介|适用范围|
|-|-|-|
|双绞铜线|两根绝缘铜线缠绕在一起|局域网、电话线|
|同轴电缆|内外导体、内外绝缘层|局域网、电视线|
|光纤|玻璃或塑料纤维|长距离传输、互联网主干网、数据中心连接|
|陆地无线电信道|无线电波|蜂窝网、蓝牙、WiFi、广播电视|
|卫星无线电信道|地球轨道卫星|全球范围的通信、卫星电话、卫星电视、GPS|

## 3. 网络传输

### 3.1 数据交换

|类型|定义|优势|缺点|
|-|-|-|-|
|电路交换|在通信开始前，建立一条专用的物理路径，通信结束后释放该路径|时延低，稳定|建立连接耗时、电路空闲仍占用带宽|
|报文交换|将整个报文作为一个整体进行存储和转发，每个节点接收完整报文后再转发|不需要预先建立连接|存储转发机制导致时延较高|
|分组交换|将报文分割成多个较小的分组并添加首部，每个分组独立传输，到达目的地后再重新组装|资源利用率高、时延低|需要重新排序，附加信息开销大|

![](https://gitee.com/wyw_0227/picture-bed/raw/master/Note/ComputerNetwork/chapter1/202408121410621.png)

### 3.2 时延类型

转发时延（forwarding）：从接收分组到完成转发所花费的时间，**转发时延=接收时延->处理时延->排队时延->传输时延**
- **接收时延**（reception）：网络设备从入接口的链路接收分组到缓冲区的耗时
- **处理时延**（processing）：网络设备对分组检查头部信息，检索转发表等操作的耗时
- **排队时延**（queuing）：如果网络设备的出接口正在发送其他分组，当前分组需要进入队列等待的耗时
- **传输时延**（transmission）：网络设备从缓冲区发送分组到出接口的链路上的耗时

![](https://gitee.com/wyw_0227/picture-bed/raw/master/Note/ComputerNetwork/chapter1/202408121410625.png)

传播时延：分组从发送端到接收端过程中，在物理介质中传播所花费的时间

{% note warning flat %}
传输是分组从路由器到链路，传播是分组在链路中，相当于传输是车经过收费站的速度，而传播是车在高速的行驶速度
{% endnote %}

流量强度：**到达率 / 服务率**，

{% note danger flat %}
流量强度不能大于1，否则排队时延会接近无限大，甚至导致丢包
{% endnote %}

![](https://gitee.com/wyw_0227/picture-bed/raw/master/Note/ComputerNetwork/chapter1/202408121410626.png)

### 3.3 性能指标

性能指标
- 传输速率（rate）：数据在通信链路中传输的速度
- 带宽（bandwidth）：通信链路的最大传输能力
- 吞吐量（throughout）：指单位时间内通过网络或系统成功传输的**有效数据量**
- 时延：数据从发送端到接收端所花费的时间，总时延=传输时延+传播时延+接收时延+处理时延+排队时延
- 丢包率：网络传输过程中丢失的数据包占总发送数据包的比例
- 往返时延（Round-Trip Time, RTT）：发送端从发送到接收到接收端的确认所经历的时间
- 时延带宽积：发送端发送的第一个比特即将到达终点时，发送端已发出了多少比特
- 信道利用率：信道有百分之多少的时间有数据通过

**瓶颈链路（bottleneck link）**：在计算机网络中传输速度最慢的那一部分链路，它限制了整个网络的性能，也就是说对于吞吐量为R1,R2,……,Rn的n链路网络，其实际吞吐量为**min{R1,R2,……,Rn}**

![](https://gitee.com/wyw_0227/picture-bed/raw/master/Note/ComputerNetwork/chapter1/202408121410627.png)

## 4. 网络协议

### 4.1 协议分层

**协议栈（protocol stack）**：一组按栈层次组织的网络协议，每层负责不同的功能，从而确保数据在网络中的正确传输

![](https://gitee.com/wyw_0227/picture-bed/raw/master/Note/ComputerNetwork/chapter1/202408121410628.png)

|分层（自顶向下）|传输对象|功能|协议|数据称呼|
|-|-|-|-|-|
|应用层|应用程序之间的通信|提供用户接口|HTTP、SMTP、FTP|报文（message）|
|运输层|端到端的通信|提供可靠或不可靠的数据传输|TCP、UDP|报文段（segment）|
|网络层|路由器之间的通信|实现不同网络之间的互联|IP|数据报（datagram）|
|链路层|交换机之间的通信|负责节点之间的数据传输|Ethernet（802.3）、Wi-Fi（802.11）|帧（frame）|
|物理层|物理介质上的传播|负责将比特流转换为电信号、光信号或无线信号|DSL、光纤、同轴电缆|比特流（bit stream）|

### 4.2 封装

封装：在每一层协议中，将上一层的数据加上自己的首部信息进行封装，形成新的数据格式
- 首部（header）：控制信息，提供了必要的元数据
- 有效载荷（payload）：实际要传输的数据内容，承载了来自上一层的数据

![](https://gitee.com/wyw_0227/picture-bed/raw/master/Note/ComputerNetwork/chapter1/202408121410629.png)

### 4.3 三要素

**语法**：规定了数据的结构和格式，即数据如何组织和表示

**语义**：规定了数据的含义，即数据表示什么以及如何处理

**时序**：规定了通信的顺序和时机，即数据何时发送、接收和响应

## 5. 网络攻击

1. 恶意软件（Malware）：通过网络传播的有害程序
   - 病毒（virus）：附着在合法程序或文件上进行破坏
   - 蠕虫（worm）：利用网络漏洞来自我复制并自动扩散
   - 木马（Trojan Horse）：伪装成合法软件来欺骗用户安装
   - 间谍软件（spyware）：秘密监控用户活动，收集敏感信息
   - 僵尸网络（botnet）：发送垃圾邮件、挖矿
2. 拒绝服务攻击（Deniel-of-Service,DoS）：让互联网设施和服务不能被合法用户使用
   - 弱点攻击：利用计算机系统或软件中的漏洞和缺陷进行攻击
   - 宽带洪泛：发送大量分组占用目标网络的带宽，导致网络拥堵或服务中断
   - 连接洪泛：创建大量半开或全开的网络连接请求，耗尽服务器资源，导致正常的连接请求无法得到处理
3. 分组嗅探（Packet Sniffing）：监控和捕获网络上传输的数据包，常用于网络分析，但也可以用于窃取数据
4. IP哄骗（IP Spoofing）：伪造源IP地址，使其看起来像是来自合法的来源，从而绕过安全措施进行恶意操作