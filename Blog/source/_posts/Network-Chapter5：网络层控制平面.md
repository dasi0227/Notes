---
title: 网络层-控制平面
tags:
  - Network
categories:
  - 笔记
cover: /image/network.png
description: 控制层面架构、路由选择算法、OSPF、BGP、SDN、ICMP、SNMP
abbrlink: 6bdcc3ed
date: 2024-09-14 10:24:58
---
<meta name="referrer" content="no-referrer"/>

## 1. SDN

### 1.1 软件定义网络

**控制器**运行在控制平面，负责制定网络设备的路由选择和流量管理，**路由器/交换机**运行在数据平面，根据下发的规则执行具体的数据包转发

|特征|解释|
|-|-|
|**基于流的转发**|SDN控制的交换机使用流表规则来转发数据包，即匹配运输层、网络层、链路层的首部字段执行对应操作，实现精细化的流量管理|
|**数据平面和控制平面分离**|SDN的数据平面专注于数据包的实际转发，而SDN的控制平面则集中于策略制定和网络管理|
|**网络控制功能**|SDN的控制功能通过SDN控制器和网络控制应用程序实现|
|**可编程网络**|SDN允许管理人员通过编程接口对网络进行动态配置和管理，赋予了控制平面灵活的“智力”|

{% note info flat %}
SDN控制器运行在**多个服务器**上，且这些服务器可以部署在**不同物理位置**上，但**逻辑上是集中的**
{% endnote %}

![](https://dasi-blog.oss-cn-guangzhou.aliyuncs.com/ComputerNetwork/chapter5/202409151601472.png)

|层次|作用|功能|
|-|-|-|
|抽象层/北向接口|负责与网络控制应用程序进行交互|路由选择、接入控制、负载均衡|
|管理层|负责管理网络|监控、检测、控制、优化|
|通信层/南向接口|负责与交换机进行通信|获取设备状态，执行网络配置|

![](https://dasi-blog.oss-cn-guangzhou.aliyuncs.com/ComputerNetwork/chapter5/202409151601473.png)

### 1.2 控制层面

- **每路由器控制**：每台路由器都有一个路由选择组件，用于与其他路由器通信，并计算转发表的值

![](https://dasi-blog.oss-cn-guangzhou.aliyuncs.com/ComputerNetwork/chapter5/202409151601463.png)

- **逻辑集中制控制**：外部控制器与路由器上的控制代理（Control Agent）进行交互，以配置和管理路由器的转发表

![](https://dasi-blog.oss-cn-guangzhou.aliyuncs.com/ComputerNetwork/chapter5/202409151601464.png)

网络的拓扑图表示
- 节点：路由器
- 边：路由器之间的链路
- 权值：传输开销
- 邻居：物理相连的路由器
- 路径：节点序列$(x_1,x_2,...,x_n)$

![](https://dasi-blog.oss-cn-guangzhou.aliyuncs.com/ComputerNetwork/chapter5/202409151601465.png)

路由类型
- **集中式**：算法知道全局节点信息
- **分散式**：每个节点仅有邻居节点信息
- **静态**：路由随时间的变化非常缓慢，通常由人工进行手动调整
- **动态**：随着网络流量的**负载或拓扑**的变化而变化
- **负载敏感**：链路开销会动态地变化以反映出**拥塞水平**
- **负载迟钝**：链路开销不明确地反映拥塞水平

## 2. 路由选择算法

### 2.1 链路状态算法

**链路状态算法（Link State, LS）**
1. 通过 Hello 报文发现直接连接的邻居
2. 将本地链路状态信息广播给网络中的所有路由器
3. 路由器根据收到的链路状态信息构建网络的完整拓扑图
4. 使用 Dijkstra 算法计算到其他路由器的最短路径
5. 根据计算结果更新路由表

局限性
- Dijkstra 算法计算复杂度较高
- 每个路由器需要存储整个网络的拓扑信息，增加了路由器的存储负担
- 泛洪机制会增加网络流量，导致网络拥堵

Dijkstra 算法
1. 选择源节点加入可拓展节点，设置到自己的距离为0，到其他节点的距离为正无穷
2. 从可拓展节点列表中，选择当前距离最小的节点进行拓展，如果通过当前节点到达其他节点的路径更短，则更新其他节点的距离
3. 如果拓展节点的邻居节点不在已拓展节点列表中，则加入邻居节点到可拓展列表
4. 将可拓展节点列表按照距离排序
5. 重复第2-4步，一直到可拓展列表为空

{% note success flat %}
LS算法过程：**假设u为源**
|迭代|已拓展|可拓展|正在拓展|u->u|u->v|u->w|u->x|u->y|u->z|
|-|-|-|-|-|-|-|-|-|-|
|0|无|u|无|0|$\infin$|$\infin$|$\infin$|$\infin$|$\infin$|
|1|无|u|最小是u|0|2（更新）|5（更新）|1（更新）|$\infin$|$\infin$|
|2|u|x,v,w|最小是x|0|2|4（更新）|1|2（更新）|$\infin$|
|3|u,x|v,y,w|最小是v|0|2|4|1|2|$\infin$|
|4|u,v,x|y,w|最小是y|0|2|3（更新）|1|2|4（更新）|
|5|u,v,x,y|w,z|最小是w|0|2|3|1|2|4|
|6|u,v,x,y,w|z|最小是z|0|2|3|1|2|4|
|7|u,v,x,y,w,z|无|无|0|2|3|1|2|4|

![](https://dasi-blog.oss-cn-guangzhou.aliyuncs.com/ComputerNetwork/chapter5/202409151601465.png)
{% endnote %}

**路由振荡**：网络结构和路径开销的动态变化，导致**频繁更换路由**

{% note success flat %}
如下图考虑y到w的路由，a时刻决定b时刻顺时针走，b时刻c时刻逆时针走，c时刻决定d时刻顺时针走，d时刻决定下次逆时针走
![](https://dasi-blog.oss-cn-guangzhou.aliyuncs.com/ComputerNetwork/chapter5/202409151712659.png)
{% endnote %}

### 2.2 距离向量算法

**距离向量算法（Distance Vector, DV）**
- **距离向量**：包含从该节点到网络中所有其他节点的**当前已知**的最短路径
- **距离向量表/路由选择表**：包含当前获得的邻居的距离向量

**Bellman-Ford算法**：$d_x[y]=\min\{c(x,v) + d_v(y)\}$
- $v$是x的所有邻居
- $c(x,v)$表示当前节点x到邻居节点v的开销
- $d_x(y)$表示当前节点x到其他节点y到开销

DV算法过程
1. 每个节点初始化自己的距离向量表，到直接连接的邻居节点的距离为实际距离，而到其他节点的距离为无穷大
2. 节点定期将距离向量信息发送给邻居节点
3. 节点根据收到的距离向量信息，填入自己的距离向量表，然后使用 Bellman-Ford 方程更新自己的距离向量
4. 如果节点的距离向量发生变化，会发送更新报文给邻居节点
5. 重复上述过程，直到所有节点的距离向量表不再变化

![](https://dasi-blog.oss-cn-guangzhou.aliyuncs.com/ComputerNetwork/chapter5/202409151601466.png)

### 2.3 区别

|属性|LS算法|DV算法|
|-|-|-|
|类型|集中式|分布式|
|发送对象|广播更新报文到全部节点|发送更新报文到邻居节点|
|收敛速度|固定为为$O(n^2)$|很慢|
|健壮性|路由计算在某种程度上是独立的，具有一定的健壮性|一台路由器出现延迟可能导致整个网络路由改变|

### 2.4 路由选择环路

定义数据包在网络中**由于错误的路由信息而在多个路由器之间无限循环**，无法到达目标地址的现象

原因
- 路由器之间的路由信息不一致，导致数据包被错误地转发
- 路由协议在拓扑变化时收敛速度较慢，可能导致临时环路
- 路由信息在短时间内频繁变化，可能导致数据包在网络中循环

解决
1. **最大跳数**：当数据包的跳数超过最大跳数值时，数据包将被丢弃
2. **毒性逆转**：当路由器检测到某条路径失效时，将该路径的距离设置为无穷大，并立即通知邻居
3. **水平分割**：路由器不会将从一个邻居学到的路由信息再发送回该邻居

## 3. AS

**自治系统（Autonomous System, AS）**：是网络管理的基本单位，是在一个**统一的管理域内**运行的一组路由器，这些路由器使用**相同的路由策略和路由协议**
- **路由管理的模块化**：将网络管理划分为一个个域，降低路由器的计算和存储开销
- **路由策略的灵活性**：不同的网络可能有不同的路由需求（如优先级、流量控制、安全策略等）
- **提高网络的可靠性和扩展性**：每个 AS 只需维护内部路由和少量外部路由信息，避免了单点故障，支持互联网的持续扩展

路由协议
- 内部网关协议（Interior Gateway Protocol, IGP）：用于 AS 内部的路由选择
- 外部网关协议（Exterior Gateway Protocol, EGP）：用于 AS 之间的路由选择

## 4. OSPF

**开放最短路优先（Open Shortest Path First, OPSF）**：用于在自治系统内部交换路由信息的协议

{% note warning flat %}
OSPF 是网络层协议，不用 UDP 或 TCP，而是直接使用 IP 数据包传送
{% endnote %}

OSPF 分组类型
- Hello 分组：用于发现邻居路由器并建立邻居关系
- 数据库描述分组（DataBase Description, DBD）：用于交换链路状态数据库的摘要信息
- 链路状态请求分组（Link-State Request, LSR）：用于请求缺失的链路状态信息
- 链路状态更新分组（Link-State Update, LSU）：用于发送链路状态信息
- 链路状态确认分组（Link-State Acknowledgement, LSAck）：用于确认接收到的链路状态信息

OSPF 流程
1. 邻居发现：通过 Hello 分组发现邻居并建立邻居关系
2. 数据库同步：通过 DBD 分组交换 LSDB 的摘要信息
3. 请求缺失信息：通过 LSR 分组请求缺失的链路状态信息
4. 更新链路状态：通过 LSU 分组发送链路状态信息
5. 确认接收：通过 LSAck 分组确认接收到的链路状态信息

区域划分
- 将一个AS划分为**多个逻辑区域**，每个区域拥有自己独立的**链路状态数据库**
- 所有区域必须连接到**骨干区域（Area 0）**，确保区域间的路由信息传播

## 5. BGP

### 5.1 工作机制

**边界网关协议（Broder Gateway Protocol, BGP）**：用于在不同自治系统之间交换路由信息的协议

{% note warning flat %}
BGP是应用层协议，是基于TCP的
{% endnote %}

BGP工作流程
1. AS选择一个路由器作为自己的边界网关路由器（eBGP），其他路由器则作为内部路由器（iBGP）
2. eBGP发送 OPEN 报文与其他 eBGP 建立关系
3. eBGP 通告 AS 所能到达的 CIDR 前缀子网信息
4. eBGP 根据路径属性（`AS-PATH`、`NEXT-HOP`、`LOCAL-PREF`）和路由选择算法进行路由
5. 只有在路由信息发生变化时，eBGP 才会立即发送 Update 报文
6. eBGP 会定期发送 Keepalive 报文 维护邻居关系

![](https://dasi-blog.oss-cn-guangzhou.aliyuncs.com/ComputerNetwork/chapter5/202409151601467.png)

![](https://dasi-blog.oss-cn-guangzhou.aliyuncs.com/ComputerNetwork/chapter5/202409151601468.png)

![](https://dasi-blog.oss-cn-guangzhou.aliyuncs.com/ComputerNetwork/chapter5/202409151601469.png)

### 5.2 路由选择

#### 5.2.1 热土豆

**总是选择具有最小最短路径开销的网关**
- 最短：当前节点到所有其他节点的所有路径中最短的路径
- 最小：当前节点到所有网关节点的最短路径中最小的路径

局限性：**没有考虑AS间的端到端开销，只为了减小在AS内部的开销**

{% note info flat %}
AS 希望赶紧将它扔给别的 AS
{% endnote %}

#### 5.2.2 消除规则

按顺序地调用下列消除规则直到余下一条路由供选择

1. 选择**最高LOCAL-PREF**的路由（最高优先级，由人为设定）
2. 选择**最短AS-PATH长度**的路由（全局最短）
3. 选择**最靠近NEXT-HOP**的路由（热土豆，局部最短）
4. 使用**最高BGP标识符**的路由（最高的接口ip地址或loopback接口ip地址）

### 5.3 IP任播

**IP任播（anycast）**：允许多个不同的服务器或网络节点共享同一个 IP 地址，当客户端向这个 IP 地址发送请求时，网络会将请求路由到最近的或最优的服务器节点，而不是固定的某个节点
- **降低延迟**：用户请求可以快速被路由到最近的服务器
- **提高可靠性**：如果一个节点出现故障，流量会自动转发到其他健康的节点
- **负载均衡**：通过共享相同的IP地址，网络可以将流量均匀地分配到多个节点上

{% note success flat %}
IP任播技术广泛用于**CDN、DNS、DHCP**
{% endnote %}

![](https://dasi-blog.oss-cn-guangzhou.aliyuncs.com/ComputerNetwork/chapter5/202409151601470.png)

### 5.4 多宿接入的边界客户网络

多宿：客户网络通过多个ISP接入互联网

边界：客户网络位于网络边界，不会用于转发流量

优势
- 提高可靠性：如果一个 ISP 故障，流量会自动切换到另一个 ISP
- 提高性能：流量可以分配到多个 ISP，减少单一链路的压力

![](https://dasi-blog.oss-cn-guangzhou.aliyuncs.com/ComputerNetwork/chapter5/202409151601471.png)

## 6. ICMP

### 6.1 报文

**网际控制报文协议（Internet Control Messages Protocol, ICMP**）：用于主机和路由器之间沟通网络层信息

{% note warning flat %}
ICMP 是网络层协议，ICMP 报文是承载在IP报文中的，即作为 IP 数据包的有效载荷
{% endnote %}

|类型|编码|描述|
|-|-|-|
|0|0|回显应答|
|3|0|目的网络不可达|
|3|1|目的主机不可达|
|3|2|目的协议不可达|
|3|3|目的端口不可达|
|3|6|目的网络未知|
|3|7|目的主机未知|
|4|0|源抑制：用于拥塞控制|
|8|0|回显请求|
|9|0|路由器通告：通告当前路由器的存在和配置信息|
|10|0|路由器发现：请求别的路由器发送通告|
|11|0|TTL过期|
|12|0|IP首部受损|

核心用途
- 终点不可达：通告源设备无法到达目标设备
- 源点抑制：防止网络设备过载，缓解拥塞问题
- 时间超过：帮助诊断网络路径问题，避免数据包无限转发
- 参数问题：帮助源设备发现并修正数据包格式问题
- 改变路由：通知源设备更新路由表

### 6.2 ping

1. 源主机发送一个**类型8编码0**的ICMP报文到指定ip地址或域名的主机，请求回显
2. 目的主机收到回显请求报文后，会发送一个**类型0编码0**的ICMP报文到源主机，响应回显
3. ping命令的结果会指示**往返时间和丢包率**

![](https://dasi-blog.oss-cn-guangzhou.aliyuncs.com/ComputerNetwork/chapter5/202409151601478.png)

### 6.3 tracert

1. 源主机不断发送**TTL递增且端口不可达**的IP数据包到目的主机，从而实现对路径的追踪
2. 当到达中间路由器且TTL过期时，中间路由器会返回一个**类型11编码0**的ICMP报文
3. 当到达目的主机时，目的主机会返回一个**类型3编码3**的ICMP报文
4. tracert命令的结果会指示往返时延和途径ip地址，如果超时会显示`*`

![](https://dasi-blog.oss-cn-guangzhou.aliyuncs.com/ComputerNetwork/chapter5/202409151601480.png)

## 7. SNMP

网络管理是对计算机网络及其设备进行监控、配置、控制和优化的活动，旨在确保网络的高效、安全和可靠运行

**简单网络管理协议（Simple Network Management Protocol, SNMP）**：是一个**应用层协议**，用于管理站和代理之间传递管理控制报文
- **管理站（Network Management Station,NMS**）：向代理发送管理请求，接收代理的响应和通知
- **代理（Agent）**：部署在被管设备上，维护管理信息库（MIB），响应管理站的请求，报告异常情况
- **管理信息库（Management Information Base,MIB）**：描述被管理设备的属性的标准化数据结构

![](https://dasi-blog.oss-cn-guangzhou.aliyuncs.com/ComputerNetwork/chapter5/202409151601476.png)

SNMP报文：作为**UDP**的有效载荷，使用**161**端口进行请求报文和响应报文的传输，使用**162**端口进行陷阱报文的传输
|类型|方向|描述|
|-|-|-|
|GetRequest|管理者->代理|请求取得指定MIB对象实例值|
|GetNextRequest|管理者->代理|请求取得下一个MIB对象实例值|
|GetBulkRequest|管理者->代理|请求批量取得多个MIB对象实例值|
|InformRequest|管理者->管理|通知另一个管理相关信息|
|SetRequest|管理者->代理|请求设置MIB对象的实例值|
|Response|代理->管理者or管理者->管理者|对请求的响应|
|Trap|代理->管理者|向管理者通知一个异常事件|

{% note warning flat %}
陷阱报文是由代理产生的，并且只从代理到管理者，不要求Response，报文结构和其他报文不一样
{% endnote %}

![](https://dasi-blog.oss-cn-guangzhou.aliyuncs.com/ComputerNetwork/chapter5/202409151601477.png)