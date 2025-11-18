---
title: 套接字编程
tags:
  - Network
categories:
  - 实验
description: 利用python的套接字编程，实现服务器和客户的“聊天交互”
cover: /image/network.png
abbrlink: 1bcba982
date: 2024-10-14 21:10:10
---
<meta name="referrer" content="no-referrer"/>

## 1. 实验要求

使用 TCP 协议创建一个客户端-服务器聊天程序
1. 服务器能够接受多个客户端连接（不少于5个）
2. 当有一个新的客户与服务器建立连接，服务器端显示该客户的地址和端口号
3. 当有一个客户与服务器断开连接，服务器端显示该客户的地址和端口号
4. 当有一个客户向服务器发送消息，服务器显示来自该客户的信息

## 2. 实验原理

### 2.1 套接字

套接字（socket）是网络协议（TCP、UDP）和应用程序之间的接口，用于在计算机之间的数据交换，由ip地址和端口号标识

- 服务器套接字（server）：用于与客户端套接字建立连接
- 客户端套接字（client）：先用于与服务器套接字建立连接，然后用于发送和接收数据

### 2.2 python程序中的变量和函数

- `address`：是一个二元组，`(ip, port)`

- `socket(family, type)`：返回一个套接字
  - family：地址簇，`AF_INET` 用于 IPv4，`AF_INET6` 用于 IPv6
  - type：类型，`SOCK_STREAM` 用于 TCP，`SOCK_DGRAM` 用于 UDP

- `socket.listen(length)`：将一个套接字从非连接模式切换到监听模式，准备接受传入的连接请求，length指定了最大连接数

- `socket.connect(address)`：将客户的套接字连接到服务器

- `socket.bind(ip, port)`：将套接字绑定到指定ip地址和端口，其中ip设置为`0.0.0.0`表示接受来自任何 IP 地址的数据

- `socket.accept()`：服务器接受客户端的连接请求，返回客户套接字和客户端地址

- `socket.send(message)`：发送数据

- `socket.recv(buffersize)`：返回接收到的数据

- `encode(string)和decode(string)`：实现字符串类型和字节类型之间的转换

- `socket.close()`：关闭套接字，释放相关资源

## 3. 实验过程

### 3.1 server.py

```python
from socket import *
import threading

def handle_client(clientSocket, clientAddress):
  print(f"【连接建立】服务器建立与客户端{clientAddress}的连接")
  clientSocket.send("开始与 Dasi 聊天吧！".encode())
  while True:
    try:
      receiveMessage = clientSocket.recv(2048)
      # 客户端申请断连
      if receiveMessage.decode() == '':
        print(f"【连接异常】丢失与客户端 {clientAddress} 的连接")
        break
      if receiveMessage.decode() == 'exit':
        print(f"【连接断开】服务器断开与客户端 {clientAddress} 的连接")
        break
      # 服务器与客户端交互
      else:
        print(f"【接收消息】{clientAddress}: {receiveMessage.decode()}")
        sendMessage = input("【发送消息】")
        clientSocket.send(sendMessage.encode())
    except Exception as e:
      print(f"【连接错误】{clientAddress}抛出信息: {e}")
      break
  # 关闭客户端套接字
  clientSocket.close()

# 服务器套接字配置
serverPort = 12000
serverSocket = socket(AF_INET, SOCK_STREAM)
serverSocket.bind(('0.0.0.0', serverPort))
# 进入监听模式，最大连接数为5
serverSocket.listen(5)
print(f"等待客户端连接...")
while True:
  # 连接到客户端
  clientSocket, clientAddress = serverSocket.accept()
  # 为每个客户端连接创建一个“聊天线程”
  client_thread = threading.Thread(target=handle_client, args=(clientSocket, clientAddress))
  client_thread.start()
```

### 3.2 client.py

```python
from socket import *

# 服务器地址
serverIP = '192.168.56.1'
serverPort = 12000
serverAddress = (serverIP, serverPort)

# 客户端套接字
clientSocket = socket(AF_INET, SOCK_STREAM)
clientSocket.connect(serverAddress)
print(f"连接到{serverAddress}的聊天机器人Dasi")

while True:
  receiveMessage = clientSocket.recv(2048)
  print(f"Dasi: {receiveMessage.decode()}")
  sendMessage = input("你: ")
  clientSocket.send(sendMessage.encode())
  # 客户端主动断连
  if sendMessage == 'exit':
    print(f"断开与{serverAddress}的连接")
    clientSocket.close()
    break
```

## 4. 实验结果

**一个服务器与三个客户端连接**
![](https://dasi-blog.oss-cn-guangzhou.aliyuncs.com/ComputerNetwork/experiment/202410142114354.png)

**每个客户端都向服务器发送消息，服务器依次回复客户端的端口号**
![](https://dasi-blog.oss-cn-guangzhou.aliyuncs.com/ComputerNetwork/experiment/202410142114356.png)

**客户端主动申请断连**
![](https://dasi-blog.oss-cn-guangzhou.aliyuncs.com/ComputerNetwork/experiment/202410142114357.png)

**客户端手动强行断连（输入ctrl+c）**
![](https://dasi-blog.oss-cn-guangzhou.aliyuncs.com/ComputerNetwork/experiment/202410142114358.png)

**客户端手动强行关闭（关闭终端）**
![](https://dasi-blog.oss-cn-guangzhou.aliyuncs.com/ComputerNetwork/experiment/202410142114359.png)

## 5. 实验总结

本次实验的**局限性**主要有以下几点
- 由于在同一台pc上运行多个客户程序和服务器程序，所以客户和服务器的ip地址都是一样的
- 如果多个客户同时向服务器发送信息，服务器的显示会出错
- 服务器只能依次按接收的顺序回复，不能指定回复的客户
- 客户一次只能发送一条消息，且只有等到服务器回复后才能发送下一条，这属于“一问一答”模式，但是跟实际聊天的模式不符合
- 服务器程序无法手动控制关闭，只能通过关闭终端来关闭服务器套接字