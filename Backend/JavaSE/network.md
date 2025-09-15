# 网络

## 基础知识

区分
- 物理网卡（Network Interface Card, NIC）：属于物理层，是实际的硬件设备，比如插在主板上的以太网卡、Wi‑Fi 无线网卡、USB 有线网卡等，负责将数字信号转换为电/光/射频信号进行物理传输
- 网络接口（Network Interface）：属于链路层，是操作系统内核为每块物理网卡在软件中创建的抽象实体
- IP 地址：属于网络层，是分配给某个网络接口的逻辑地址，用于在不同主机间路由和寻址
- 端口（Port）：属于传输层，用于区分不同服务的标识，一个端口号加上一个 IP 地址就唯一标识网络上的一个“套接字”，即一条具体的网络连接

联系
- 操作系统内核加载物理网卡的驱动后，会为该硬件创建一个主网络接口，也可以创建任意多个虚拟接口
- 每个网络接口都可以分配一个或多个 IP 地址，IPv4 与 IPv6 各自独立
- IP 地址又可以对应很多个端口，表示对同一个远程对象使用不同服务

流程
1. 应用层的应用程序调用 Socket API，确定目标 IP + Port，将数据流（Stream）提交给传输层
2. 传输层将数据流切分成段（segment），添加源/目的端口等头信息，交给网络层
3. 网络层按目标 IP 查路由表，选定本地接口，添加源/目的 IP，封装为包（package）
4. 链路层在选定接口上添加源/目的 MAC，封装以太网帧（frame），发送到对应的网络接口
5. 物理层的物理网卡将每一帧的比特转换为电/光/射频信号，发往下一个网络节点

回环地址（Loopback）：用于主机的内部通信，不会发往物理网卡或真正的网络，常用于测试本地的协议栈是否正常
- IPv4：127.0.0.1
- IPv6：::1
- 主机名：localhost

通配符地址（Wildcard Address）：用于服务器程序绑定时，表示绑定到本机所有可用网络接口上的对应端口，常用于监听主机所有网卡的连接
- IPv4：0.0.0.0
- IPv6：:: 或 ::0

## InetAddress

位于 java.net 包里，本质是对一个 IP地址（IPv4或IPv6）和可选主机名（HostName）的封装，不含端口，也不带实际网络连接
- IPv4：长度为 4 的 byte[] 存储 32 位地址
- IPv6：长度为 16 的 byte[] 存储 128 位地址
- 主机名：String 对象，可选的保存，否则为 null

类方法/静态方法
- InetAddress getLocalHost()：返回本地主机的地址对象
- InetAddress getByName(String host)：传入主机名，返回对应的地址对象
- InetAddress[] getAllByName(String host)：返回主机名对应的所有地址对象组成的数组
- getByAddress(byte[] addr)：传入原始 IP 字节数组构造地址对象
- getByAddress(String host, byte[] addr)：同上，并在对象中保留指定的主机名

对象方法/实例方法
- String getHostName()：返回此地址的主机名
- String getHostAddress()：返回 IP 地址
- byte[] getAddress()：返回 IP 地址的字节数组
- boolean isReachable(int timeout)：尝试在指定毫秒内 ping 此地址，返回是否可达
- isLoopbackAddress()：判断是否为回环地址 
- isAnyLocalAddress()：判断是否为通配符地址

## Socket

Socket 套接字用于网络通信中的 TCP 连接，将某一端的地址和端口号封装，使得程序可以像读写本地流一样，从另一端接受数据或发送数据到另一端

InetSocketAddress：封装了 IP 地址和端口

客户端：java.net.Socket
- 构造器
  - Socket(String host, int port)：指定服务端的主机名和端口
  - Socket(InetAddress address, int port)：指定服务端的地址和端口 
  - Socket(String host, int port, InetAddress localAddr, int localPort)：指定服务端地址/端口，同时绑定本地地址/端口
- 方法
  - void connect(SocketAddress endpoint, int timeout)：显式发起连接，可设置毫秒级超时
  - InputStream getInputStream()：获取读取远端数据的流
  - OutputStream getOutputStream()：获取写入远端数据的流
  - void setSoTimeout(int timeout)：设置 read() 操作的阻塞超时
  - void setTcpNoDelay(boolean on)：开启/关闭 Nagle 算法
  - boolean isConnected() / isClosed()：返回连接状态
  - void close()：关闭连接并释放资源

服务端：java.net.ServerSocket
- 构造器
  - ServerSocket(int port)：ServerSocket(int port)：在所有本地接口上监听指定端口
  - ServerSocket(int port, int backlog)：指定端口和等待队列长度
  - ServerSocket(int port, int backlog, InetAddress bindAddr)：指定监听端口、队列长度和本地绑定地址
- 方法
  - Socket accept()：阻塞等待并接收新连接，返回对应的客户端 Socket
  - void setSoTimeout(int timeout)：设置 accept() 的超时时间
  - void setReuseAddress(boolean on)：允许重用已释放的监听端口
  - int getLocalPort()：获取正在监听的本地端口
  - InetAddress getInetAddress()：获取本地绑定的地址
  - boolean isBound() / isClosed()：检查监听状态
  - void close()：停止监听并释放端口

流程
1. 客户端直接构造连接 / 先构造再 connect
2. 客户端配置选项
3. 客户端通过输出流写入数据
4. 服务端在端口构造监听
5. 服务端阻塞直到有新连接或超时
6. 服务端通过输入流读取数据

## 交互

可以发现 ServerSocket.accept() 的返回值是一个 Socket
- ServerSocket 的职责只在于监听和接收新的连接，但并不负责接发数据，而是不断 accept() 出若干个 Socket，每个 Socket 都代表了一个「客户端－服务端」通信会话，通过 Socket 实现接发数据
- 服务端可以通过一个 ServerSocket 创建出多个 Socket，从而实现一个服务端服务多个客户端，可以在循环中或为每个连接创建一个线程/任务来处理它们，这就是高并发的原型

消息的接发
- 单条消息结束：可以发送端写完后立即 flush()，也可以在发送端在尾部添加结束标记，然后接收端 readline()
- 全部消息结束：shutdownOutput() 或者直接 close()

## DatagramSocket

DatagramSocket 用于 UDP 无连接通信，既可发送也可接收 DatagramPacket

|特性|TCP|UDP|
|-|-|-|
|传输模式|面向连接：通信前需建立三次握手|无连接：无需握手，直接发送|
|可靠性|提供可靠传输：丢包重传、校验、确认与超时重发|不保证可靠：不重传，不确认|
|数据顺序|保证按发送顺序到达|无顺序保证：包可能乱序或丢失|
|流量控制|有：基于滑动窗口控制发送速率|无：发送速率由应用自主|
|拥塞控制|有：动态调整拥塞窗口|无|
|头部开销|20–60字节（含可选选项字段）|固定8字节|
|传输效率|较低：额外的可靠性与控制开销|较高：无额外控制，适合实时或小数据量应用|
|应用场景|文件传输(FTP)、网页(HTTP/HTTPS)、邮件(SMTP/POP3)等|视频/语音(VoIP)、DNS查询、DHCP、在线游戏等|

构造器
- DatagramSocket()
- DatagramSocket(int port)
- DatagramSocket(int port, InetAddress laddr)
- DatagramSocket(SocketAddress bindAddr)

核心方法
- void send(DatagramPacket p)：向指定目标发送一个 UDP 包
- void receive(DatagramPacket p)：接收一个 UDP 包（阻塞），填充到 p 的缓冲区
- void connect(InetAddress address, int port)：“连接”到特定远端，以后只能与该地址/端口通信
- void disconnect()：取消 connect 后的固定目标限制
- boolean isConnected()：判断是否已 connect
- void setSoTimeout(int timeout)：设置 receive() 的阻塞超时（毫秒），超时抛 SocketTimeoutException
- void setBroadcast(boolean on)：开启/关闭允许发送广播包
- int getLocalPort() / InetAddress getLocalAddress()：获取本地绑定的端口和地址
- SocketAddress getRemoteSocketAddress()：如果已 connect()，返回远端地址/端口
- void close()：关闭 socket 并释放端口

## DatagramPackage

构造器
- DatagramPacket(byte[] buf, int length)
- DatagramPacket(byte[] buf, int offset, int length)
- DatagramPacket(byte[] buf, int length, InetAddress address, int port)
- DatagramPacket(byte[] buf, int offset, int length, InetAddress address, int port)
- DatagramPacket(byte[] buf, int offset, int length, SocketAddress address)
- DatagramPacket(byte[] buf, int length, SocketAddress address)

方法
- byte[] getData()：返回缓冲区数组
- int getLength()：返回数据长度
- void setData(byte[] buf)／void setData(byte[] buf, int offset, int length)：设置缓冲区
- InetAddress getAddress()：返回目标（发送时）或源（接收时）IP
- int getPort()：返回目标或源端口
- SocketAddress getSocketAddress()：返回目标或源的 SocketAddress
- void setAddress(InetAddress addr)／void setPort(int port)：修改目标地址/端口
- int getOffset()：返回缓冲区偏移
- void setLength(int length)：设置预计接收的最大长度（接收时用）