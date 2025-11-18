---
title: 利用Wireshark观察TCP三次握手
tags:
  - Network
categories:
  - 实验
cover: /image/network.png
abbrlink: 3828c331
date: 2024-09-10 11:36:58
description: 详细解释了TCP三次握手的原理，并利用Wireshark抓包，观察数据帧的首部来分析
---
<meta name="referrer" content="no-referrer"/>

***运输层知识请看***

{% link 计网：运输层,Dasi's Blog,https://dasi.plus/posts/bbea855c/ %}

## 1. TCP的三次握手

### 1.1 原理

三次握手流程
1. 客户端TCP向服务器端TCP发送<font color="orangered">SYN报文段</font>
   - 首部中的SYN标志位被置为1，ACK标志位被置为0
   - 客户会随机地选择一个初始序号（client_isn）
   - 确认号字段被置为0
2. 服务器端TCP接收到SYN报文段，为TCP连接分配缓存和变量，并向客户端TCP发送<font color="orangered">SYNACK报文段</font>
   - 首部中的SYN标志位被置为1，ACK标志位被置为1
   - 服务器会随机选一个初始序号（server_isn）
   - 确认号字段被置为client_isn+1
3. 客户端TCP接收到SYNACK报文段，为TCP连接分配缓存和变量，并向服务器端TCP发送<font color="orangered">ACK报文段</font>
   - 首部中的SYN标志位被置为0，ACK标志位被置为1
   - 序号字段被置为client_isn+1
   - 确认号字段被置为server_isn+1

![](https://dasi-blog.oss-cn-guangzhou.aliyuncs.com/ComputerNetwork/chapter3/202409092139126.png)

{% note info flat %}
为什么需要三次握手？
- 全双工通信
  - 第一次握手**确认客户端请求建立连接**
  - 第二次握手**确认服务器同意建立连接**，并且**服务器可以接收到客户数据**
  - 第三次握手**确认客户可以接收到服务器的数据**
- 可靠性：三次握手确保双方都能正确接收和处理对方的序列号和确认号，从而实现可靠数据传输
{% endnote %}

### 1.2 TCP报文段结构

|字段|长度/比特|作用|
|-|-|-|
|源端口号（Resource Port）|16|标识数据传输的起始端点|
|目的端口号（Destination Port）|16|标识数据传输的终止端点|
|序号（Sequence Number）|32|标识TCP数据流中的字节顺序|
|确认号（Acknowledgement Number）|32|标识下一个期望接收的字节序号|
|首部长度（Header Length）|4|指示TCP头部长度，以32位字为单位|
|保留区域（Reserved）|3|保留，可能会在未来的协议扩展中有新的用途|
|减少拥塞窗口（CWR）|1|发送方用于确认它已经响应了网络拥塞，调整了其拥塞窗口|
|显式拥塞通知（ECN-Echo）|1|接收方用于通知发送方网络发生了拥塞|
|标志（Flags）|6|控制位，标识特殊功能（具体在下面）|
|接收窗口（Window）|16|指定接收方的缓存区域大小|
|检验和（Checksum）|16|检验报文在传输过程中是否出错|
|紧急数据指针（Urgent Pointer）|16|指示紧急数据在数据流中的位置|
|选项（Options）|每项32位|用于传输协议的扩展功能|
|数据（Data）|可变|实际传输的应用数据部分|

![](https://dasi-blog.oss-cn-guangzhou.aliyuncs.com/ComputerNetwork/chapter3/202409092139115.png)

### 1.3 标志（按顺序）

- **URG（Urgent）**：紧急指示标志，表示有紧急数据需要优先处理
- **ACK（Acknowledgement）**：确认标志，用于确认收到的数据
- **PSH（Push）**：推送标志，表示接收方应尽快将数据推送到应用程序，而不是等待缓冲区满
- **RST（Reset）**：重置标志，用于重新初始化连接
- **SYN（Synchronize）**：同步标志，用于连接的建立阶段
- **FIN（Finish）**：结束标志，用于连接的终止阶段

## 2. 实验

### 2.1 实验流程

1. 打开Wireshark，点击控制栏的“开始捕获分组”，即蓝色鲨鳍图标
2. 打开Edge浏览器，输入要访问的网址，这里输入的是`www.baidu.com`
3. 打开Wireshark，点击控制栏的“停止捕获分组”，即红色方形图标
4. 打开Terminal，输入命令`ping www.baidu.com -4`，获取主机的IPv4地址`183.240.98.198`
![](https://dasi-blog.oss-cn-guangzhou.aliyuncs.com/ComputerNetwork/Wireshark-TCP/202409100017031.png)
5. 打开Wireshark，在控制栏底部的过滤器中输入`ip.addr == 183.240.98.198 and tcp`
![](https://dasi-blog.oss-cn-guangzhou.aliyuncs.com/ComputerNetwork/Wireshark-TCP/202409100017032.png)
6. 滚动滑到最上面栏目，不出意外的话前三个就是TCP的三次握手
![](https://dasi-blog.oss-cn-guangzhou.aliyuncs.com/ComputerNetwork/Wireshark-TCP/202409101706736.png)

{% note warning flat %}
需要说明的是，书本上都是以HTTP协议做例子，握手之后直接就可以传输数据
但现在的浏览器都**强制使用HTTPS协议**，在TCP连接建立之后，会进行**TLS握手阶段**（主要包括Client Hello、Server Hello、证书交换、密钥交换和握手完成），然后才传输数据
所以这里我们只看前三个TCP
{% endnote %}

### 2.2 首部分析（以第一个TCP为例）

![](https://dasi-blog.oss-cn-guangzhou.aliyuncs.com/ComputerNetwork/Wireshark-TCP/202409101302627.png)

`Frame 35: 66 bytes on wire (528 bits), 66 bytes captured (528 bits) on interface \Device\NPF_{7EF505B7-CAD7-4835-BC20-6D8015ED071D}, id 0`：**捕获数据帧的元信息**
- `Frame 35`：捕获的数据帧编号
- `66 bytes on wire (528 bits)`：数据帧在网络上实际传输的长度是66字节
- `66 bytes captured (528 bits)`：捕获的数据帧长度也是66字节，说明成功地捕捉到了全部内容
- `on interface \Device\NPF_{7EF505B7-CAD7-4835-BC20-6D8015ED071D}`：数据帧在指定的网络接口上捕获，这里由Wireshark使用

`Ethernet II, Src: Intel_c8:72:56 (8c:f8:c5:c8:72:56), Dst: NewH3CTechno_ba:6a:01 (28:e4:24:ba:6a:01)`：**链路层协议**
- `Ethernet II`：表示这是一个以太网II格式的数据帧
- `Src: Intel_c8:72:56 (8c:f8:c5:c8:72:56)`：表示数据帧的源MAC地址
- `Dst: NewH3CTechno_ba:6a:01`：表示数据帧的目的MAC地址

`Internet Protocol Version 4, Src: 172.19.59.243, Dst: 183.240.98.198`：**网络层协议**
- `Internet Protocol Version 4`：表示这是一个IPv4协议的数据帧
- `Src: 172.19.59.243`：表示数据帧的源IP地址
- `Dst: 183.240.98.198`：表示数据帧的目的IP地址

`Transmission Control Protocol, Src Port: 56996, Dst Port: 443, Seq: 0, Len: 0`：**运输层协议**
- `Transmission Control Protocol`：表示这是一个TCP协议的数据帧
- `Src Port: 56996`：表示数据帧的源端口
- `Dst Port`：表示数据帧的目的端口
- `Seq: 0`：表示数据帧的序列号
- `Len: 0`：表示数据帧的有效负载长度

{% note success flat %}接下来主要从运输层协议角度分析，并且只讲一些关键字段{% endnote %}

### 2.3 第一次握手：SYN

{% note success flat %}点击左边栏目的字段，右边栏目会将对应的字节高亮{% endnote %}

![](https://dasi-blog.oss-cn-guangzhou.aliyuncs.com/ComputerNetwork/Wireshark-TCP/202409100017033.png)

`Sequence Number (raw): 3595153809`：绝对序号是3595153809，16进制下是`d6 49 b1 91`

`Acknowledgment number (raw): 0`：在三次握手过程中，第一个SYN包的确认号通常是0，表示还没有任何数据被确认

`Flags: 0x002 (SYN)`：后六位是`000010`，SYN被置位，表示客户请求建立连接

`Options: (12 bytes), Maximum segment size, No-Operation (NOP), Window scale, No-Operation (NOP), No-Operation (NOP), SACK permitted`
- TCP Option - Maximum segment size: 1460 bytes：表示每个TCP数据段的最大有效负载（MSS）为1460字节
- TCP Option - Window scale: 8 (multiply by 256)：表示TCP窗口的实际大小是窗口字段值乘以256
- TCP Option - SACK permitted，表示允许接收方告知发送方哪些数据块已经成功接收，哪些需要重传
- TCP Option - No-Operation (NOP)：这是一个填充或对齐选项，长度为1字节，用于确保其他选项的对齐

{% note warning flat %}每个选项字段长都是4字节（32位），而有些选项值只需要1/2/3字节，因此需要1字节的NOP对齐到4字节边界{% endnote %}

### 2.4 第二次握手：SYN-ACK

![](https://dasi-blog.oss-cn-guangzhou.aliyuncs.com/ComputerNetwork/Wireshark-TCP/202409100017034.png)

`Sequence Number (raw): 2472347759`：绝对序号随机初始化为2472347759

`Acknowledgment number (raw): 3595153810`：绝对序号是3595153810，可以发现是**SYN报文段的序号（3595153809）+1**

`Flags: 0x012 (SYN, ACK)`：后六位是`010010`，ACK和SYN被置位，表示服务器允许并确认建立连接

### 2.5 第三次握手：ACK

![](https://dasi-blog.oss-cn-guangzhou.aliyuncs.com/ComputerNetwork/Wireshark-TCP/202409100017035.png)

`Sequence Number (raw): 3595153810`：绝对序号是3595153810，可以发现是**SYN报文段的序号（3595153809）+1**

`Acknowledgment number (raw): 2472347760`：绝对序号是2472347760，可以发现是**SYN-ACK报文段的序号（2472347759）+1**

`Flags: 0x010 (ACK)`：后六位是`010000`，ACK被置位，表示客户端确认了服务器端的连接请求，并准备好了进行数据交换

{% note warning flat %}可以发现，第三次握手的时候没有选项字段，这是因为在第一次和第二次握手中协商了部分选项（如最大段大小、窗口缩放等），这些选项已经被双方认可和接受，不需要再次声明{% endnote %}

### 2.5 相对序号

在Wireshark中使用相对序号而非绝对序号，主要是为了简化数据包分析过程，因为绝对序号在TCP流量中通常很长，且随着数据流量的增加而增加，这使得观察和比较变得复杂

利用相对序号概述一遍流程：
1. 客户端发送`Seq=0,ACK=0`的**SYN**报文来**请求连接**
2. 服务器发送`Seq=0,ACK=1`的**SYN-ACK**报文来**允许连接**
3. 客户端发送`Seq=1,ACK=1`的**ACK**报文来**确认连接**

## 3. 参考链接

{% link Wireshark抓包分析 TCP三次握手,我的小碗汤,https://cloud.tencent.com/developer/article/1538191 %}