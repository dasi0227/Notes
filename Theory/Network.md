# 计算机网络



## 网络分层模型

### OSI 七层模型和 TCP/IP 四层模型

1. 应用层 Application：负责为用户程序提供网络服务
2. 表示层 Presentation：负责将网络传输的数据进行格式化、压缩、加/解密、编/解码
3. 会话层 Session：负责管理（创建、维护、终止）应用之间会话
4. 传输层 Transport：负责为进程提供端到端的可靠/不可靠传输
5. 网络层 Network：负责路由选择和逻辑寻址，实现端到端的数据包传输
6. 链路层 Data Link：负责差错检测、流量控制，在物理层上提供可靠的数据帧传输
7. 物理层 Physical：负责比特流传输

OSI 七层模型的粒度过细，实际上更多采用的是 TCP/IP 四层模型，实际上就是 OSI 七层模型的包装和整合

1. 应用层：负责为用户程序提供完整的网络服务
2. 传输层：负责为进程提供端到端的可靠/不可靠传输
3. 网际层：负责路由选择和逻辑寻址
4. 网络接口层：负责底层的数据传输

![d5eec4dc32893dbad3587dd14cd7554d](https://dasi-blog.oss-cn-guangzhou.aliyuncs.com/Java/202509290942466.png)

### 意义

- **独立**：每一层只需关注自己的职责，不必关心其他层的实现细节，一个层的改变不会影响整体网络结构
- **灵活**：下层只需向上层提供标准化接口，具体实现可以自由修改或替换
- **扩展**：不同厂商只要遵循统一的接口协议，就能实现兼容、升级和扩展
- **化简**：将复杂的网络通信问题分解为若干小问题，逐层实现，降低设计与理解的难度



## HTTP

### 定义

**HTTP（HyperText Transfer Protocol, 超文本传输协议）**是一种无状态、基于请求-响应模式的应用层协议，主要用于客户端和服务器之间的通信，规定了浏览器如何向 Web 服务器拿数据，以及 Web 服务器如何返回数据

- 无状态（stateless）：协议本身不保存会话信息
- 请求-响应模型：客户端主动请求，服务器被动响应
- 明文传输：不会进行加密，要么依靠应用层，要么使用 HTTPS
- 扩展：可以自定义请求头和响应头来实现不同效果
- 灵活：支持多种数据格式，包括 HTML、JSON、XML、图片、音频、视频等
- 可靠：基于 TCP，保证数据传输的不丢包、不乱序

### HTTP 报文

请求报文

- 请求行：`方法 URI 协议版本>`
- 请求头：一组键值对，描述客户端的环境和请求信息
- 空行：分隔请求元信息和请求主体信息
- 请求体：携带表单数据、文件二进制流

```text
GET /index.html HTTP/1.1
Host: www.example.com
User-Agent: Mozilla/5.0 (Windows NT 10.0; Win64; x64)
Accept: text/html,application/xhtml+xml,application/xml,*/*
Accept-Language: zh-CN,zh,en
Connection: keep-alive
```

响应报文

- 状态行：`<协议版本 状态码 状态描述>`
- 状态头：一组键值对，描述服务器的环境和响应信息
- 空行：分隔响应元信息和响应主体信息
- 响应体：携带 HTML、XML、JSON、文件二进制流

```text
HTTP/1.1 200 OK
Date: Sun, 29 Sep 2025 03:30:00 GMT
Server: Apache/2.4.41 (Ubuntu)
Content-Type: text/html; charset=UTF-8
Content-Length: 137

<html>
<head><title>Example</title></head>
<body>
<h1>Hello, World!</h1>
<p>This is a simple HTTP response.</p>
</body>
</html>
```

状态码和状态描述

| 状态码 | 状态含义      | 状态描述               |
| ------ | ------------- | ---------------------- |
| 1XX    | Informational | 💡 提示处理情况         |
| 2XX    | Success       | ✅ 请求处理完毕         |
| 3XX    | Redirection   | ↩️ 需要进一步请求       |
| 4XX    | Client Error  | ⚠️ 服务器无法处理请求   |
| 5XX    | Server Error  | ❌ 服务器处理请求时出错 |

头字段

| 名称                | 说明                               | 示例                                                  |
| ------------------- | ---------------------------------- | ----------------------------------------------------- |
| **Host**            | 指定请求的目标主机                 | Host: www.example.com                                 |
| **User-Agent**      | 客户端信息，如浏览器、设备、系统等 | User-Agent: Mozilla/5.0 (Windows NT 10.0; Win64; x64) |
| **Accept**          | 客户端接受的内容类型               | Accept: text/html, application/json                   |
| **Accept-Language** | 客户端可接受的语言                 | Accept-Language: zh-CN, en-US                         |
| **Content-Type**    | 请求/响应体的数据类型              | Content-Type: application/json                        |
| **Content-Length**  | 请求/响应体的字节长度              | Content-Length: 348                                   |
| **Connection**      | 是否长连接                         | Connection: keep-alive                                |
| **Cookie**          | 客户端向服务器携带的 Cookie 数据   | Cookie: sessionId=abc123                              |
| **Set-Cookie**      | 服务器向客户端设置 Cookie          | Set-Cookie: sessionId=abc123; Path=/; HttpOnly        |

### TLS

要理解 TLS，首先需要理解三个有关安全的操作

| 类别     | 哈希 Hash                        | 加密 Encrypt                                                 | 签名 Signature                            |
| -------- | -------------------------------- | ------------------------------------------------------------ | ----------------------------------------- |
| **定义** | 把任意长度数据映射到固定长度的值 | 用密钥把明文转换为密文，再用密钥把密文还原为明文             | 先哈希消息得到摘要，再用密钥加密摘要      |
| **目的** | 防篡改                           | 防窃听                                                       | 防伪装                                    |
| **作用** | 做“指纹”，确保数据完整性         | 非对称加密用于保护密钥，对称加密用于保护传输数据             | 身份认证                                  |
| **可逆** | ❌ 不可逆                         | ✅ 可逆                                                       | ⚠️ 只能还原到摘要                          |
| 例子     | digest = Hash(plaintext)         | ciphetext = Encrypt(plaintext, key)<br />plaintext = Decrypt(ciphetext, key) | signature = Encrypt(Hash(plaintext), key) |

TLS 利用了四个技术确保了 HTTP 的安全性

- **对称加密**：加密和解密使用同一个密钥，效率都很高但是必须确保密钥不会泄漏，否则将彻底失去安全性
- **非对称加密**：加密和解密使用一对公钥和私钥，公钥加密只能用私钥解密，私钥加密只能用公钥解密，效率很低但是公钥泄漏对安全没有影响，因此**非对称加密在这里不是用于数据内容的，而是用于对称加密的密钥**
- **摘要算法**：实际上就是对输入数据进行哈希运算，得到固定长度的输出作为摘要，输入数据只要改动 1 个 bit，都会对摘要产生很大的影响，而且几乎不可能存在哈希冲突，因此摘要可以用来进行数据的完整性校验
- **数字证书**：由权威机构 CA（Certificate Authority）颁发，是对服务器的身份验证
    - **证书 Certificate**：服务器信息、服务器公钥、颁发者信息、有效期、序列号、签名算法（哈希算法+加密算法）
    - **签名 Signature**：使用证书中指定的签名算法和 CA 私钥生成对 Certificate 的签名

完整的流程为

1. 服务器提前向 CA 申请好数字证书并安装
2. 当客户端使用 https 第一次连接服务器的时候，会发送 ClientHello（包含客户端支持的加密算法列表和一个 ClientRandom）
3. 服务器会回复 ServerHello（包含数字证书、选定的加密算法和一个 ServerRandom）
4. 客户端利用 CertBody 中的签名算法中的哈希算法计算 Certificate 的 digest1，然后利用本地缓存的 CA 公钥对 Signature 进行解密得到 digest2，如果 digest1 == digest2 则说明验签成功，客户端认可服务器身份
5. 身份认证成功后，客户端就可以拿到 Certificate 中的服务器公钥
    1. 服务器会生成一个临时公私钥对（EphPub_server + EphPri_server），然后用服务器私钥对 EphPub_server 签名后发送，客户端用服务器公钥对 EphPub_server 验签后接收
    2. 客户端也会生成一个临时公私钥对（EphPub_client + EphPriv_client），然后直接明文把 EphPub_client 发送给服务器
    3. 客户端用 EphPriv_client + EphPub_server 而服务器用 EphPriv_server + EphPub_client 计算  pre-master secret
    4. 客户端和服务器再利用  pre-master secret + ClientRandom + ServerRandom 就可以得到最终的会话密钥 session_secret
6. 客户端会利用 session_secret 发送 Finished，服务器收到后也会利用 session_secret 返回 Finished
7. 当双方都收到 Finished 后就代表加密连接完成，可以开始加密传输

### HTTP vs HTTPS

实际上，HTTPS 就是比 HTTP 多了个 **TLS（Transport Layer Security）**，是 SSL（Secure Sockets Layer）的升级版

| **对比点**   | **HTTP**                   | **HTTPS**                                |
| ------------ | -------------------------- | ---------------------------------------- |
| **定义**     | 明文传输                   | 加密传输                                 |
| 前缀         | http://                    | https://                                 |
| **端口**     | 80                         | 443                                      |
| **性能**     | 无额外开销，速度快         | 有加解密开销                             |
| **证书**     | 不需要证书                 | 需要申请数字证书                         |
| **完整性**   | 无法保证数据是否被篡改     | 提供完整性校验，数据一旦被篡改就会被发现 |
| **应用场景** | 内网、对安全性要求低的场景 | 电商、支付、登录、敏感数据传输           |

### HTTP/1.0 vs HTTP/1.1

| **对比点**     | **HTTP/1.0**                                                 | **HTTP/1.1**                                                 |
| -------------- | ------------------------------------------------------------ | ------------------------------------------------------------ |
| **连接方式**   | 默认短连接：每次请求都要新建 TCP 连接，响应完立刻关闭        | 默认长连接：多个请求可复用同一个 TCP 连接                    |
| **带宽利用**   | 不支持范围请求，必须整个资源下载                             | 支持 Range 请求，可只请求部分内容                            |
| **缓存控制**   | 通过简单的 Expires 字段控制缓存，功能有限                    | 增强缓存控制，新增 Cache-Control、ETag、If-None-Match、If-Modified-Since 等更灵活的机制 |
| **Host 头部**  | 没有 Host 头部，一个 IP 地址只能绑定一个网站                 | 必须有 Host 头部，一个 IP 地址可以托管多个域名，推动了虚拟主机的发展 |
| 压缩           | 只支持端到端压缩，即资源本身被压缩了，不支持传输的时候会压缩 | 引入逐跳压缩，每一跳的中间节点都可能解码再编码               |
| **请求方法**   | GET、POST、HEAD                                              | 新增 PUT、DELETE、OPTIONS、TRACE 等                          |
| **错误状态码** | 只有 16 个                                                   | 引入新的状态码                                               |

### HTTP vs WebSocket vs SSE

| **特性**     | **HTTP**                               | **WebSocket**                                                | **SSE (Server-Sent Events)**                             |
| ------------ | -------------------------------------- | ------------------------------------------------------------ | -------------------------------------------------------- |
| **通信模式** | 半双工，客户端主动发起，服务器被动响应 | 全双工，客户端和服务器都能主动发消息                         | 单工，服务器主动发消息到客户端                           |
| **连接方式** | 短连接或长连接                         | 长连接                                                       | 长连接                                                   |
| **实时**     | 不实时，只能靠客户端轮询               | 实时双向通信                                                 | 实时单向推送                                             |
| **复杂度**   | 简单                                   | 较复杂，作为一个独立的应用层协议，需要服务端专门支持 WebSocket，也需要客户端调用 WebSocket API | 中等，封装在 HTTP 之上，使用 MIME 类型 text/event-stream |
| **使用场景** | 普通网页加载、表单提交、接口调用       | 聊天、协同编辑、游戏                                         | 消息推送、数据流更新                                     |

### Cookie

Cookie 从狭义上来讲就是**服务器要求存储在客户端的一个键值对**，服务器只需要在响应头中添加 `Set-Cookie` 来指定 `Name:Value` 和其属性

- **Domain**：指定生效的域名
- **Path**：指定生效的路径
- **Expires**/Max-Age：指定过期时间
- **HttpOnly**：禁止 JS 访问 Cookie
- **Secure**：只有在 HTTPS 才会传输
- **SameSite**：控制跨站请求时是否带 Cookie

```http
Set-Cookie: SESSIONID=abc123; Path=/; Domain=example.com; HttpOnly; Secure; Max-Age=3600; SameSite=Lax
```

Cookies 是浏览器当前在所有网站上保留的所有 Cookie，类似于一张表，浏览器会自动根据每个 Cookie 的属性来决定当前请求需要携带哪些 Cookie，从而在请求头中添加 `Cookie`，而且只需要加入 `Name:Value`，其他属性不需要加入

```http
Cookie: key1=value1; key2=value2; key3=value3
```

由于 Cookie 是明文存储的，所以 Cookie 不应该存储敏感信息，而是存储以下三类信息

- 存储用户偏好：浏览器进入某个页面可以直接切换到用户配置，如颜色、主题、快捷键、布局等
- 存储会话用户：在服务器创建 Session 对象代表当前对话并记录用户信息，但只保留一个 **JSESSIONID** 到客户端中，用来标识该 Session 对象
- 存储跟踪标识：广告商可以给当前主机设置一个 **TRACKINGID**，通过 JS 埋点，让浏览器每次请求都自动向广告商服务器发送一个携带 TRACKINGID 的请求，广告商就能在不同网站之间识别出同一个主机，从而构建操作当前主机的用户画像来实现精准投放

### CORS

**同源策略**：是浏览器的安全限制，**要求当前页面地址必须与请求资源地址的协议、域名、端口完全相同，才会允许 JS 代码访问响应数据**

- 像 \<img>、\<script>、\<link>、\<video>、\<audio> 等展示型资源的链接，JS 本来就不会访问响应数据，所以不会触发同源策略
- \<a> 跳转链接，不是让当前页面读取数据，而是直接换成了另一个页面，JS 代码会重新加载，所以也不会触发同源策略

**CORS（Cross-Origin Resource Sharing, 跨域资源共享）**：是一种基于 HTTP 响应头的机制，用来让浏览器确认某个跨域请求是不是被目标服务器允许的，如果目标服务器都允许了，那么浏览器自然没有拒绝的理由

| 类型     | 条件                                                         | 流程                                                         |
| -------- | ------------------------------------------------------------ | ------------------------------------------------------------ |
| 简单请求 | - 方法：GET/HEAD/POST<br />- POST 的 Content-Type 只能是 application/x-www-form-urlencoded、multipart/form-data、text/plain<br />- 不能有自定义请求头 | 直接发请求，然后检查响应里的 Access-Control-Allow-Origin 是否包含当前域名 |
| 复杂请求 | - 方法：PUT/DELETE/PATCH<br />- 请求头中有自定义字段         | 先发送一个 OPTIONS 预检请求，然后根据服务器的响应来判断是否可以真的发送目标请求 |

```http
预检请求：
Origin: https://a.com
Access-Control-Request-Method: PUT
Access-Control-Request-Headers: Authorization

预检响应：
Access-Control-Allow-Origin: https://a.com
Access-Control-Allow-Methods: GET, POST, PUT
Access-Control-Allow-Headers: Authorization
```



## DNS

### 定义

**DNS（Domain Name System, 域名管理系统）**：用来**把域名解析为 IP 地址的系统**

- 域名：人类容易理解的主机名，如 www.example.com
- IP 地址：机器容易理解的主机名，如 192.168.24.1

DNS 服务器：实际上我们根本就无法通过域名来访问目标服务器，**域名本身并不是目标服务器的属性，只是为了方便人类记忆和理解的“逻辑别名”，目标服务器只能通过 ip 地址标识**，但是程序员在注册域名后，可以把域名和 ip 地址的映射关系保存在 DNS 服务器上，浏览器会在后台自动访问 DNS 服务器来实现域名解析

1. 用户在浏览器地址栏输入域名，浏览器会先查本地的 DNS 缓存（浏览器缓存、操作系统缓存、hosts 文件）
2. 如果没有查到就向本地 DNS 服务器发起请求，获取目标服务器域名对应的 ip 地址
3. 浏览器把域名作为请求头的一个字段，然后基于 TCP 和目标服务器的 ip 地址与目标服务器建立连接
4. 目标服务器根据域名确定处理请求的进程，然后返回响应

### DNS 服务器的类型和处理过程

1. **本地 DNS 服务器（local）**：一般由互联网服务提供商提供，实际上它并不能完全算作是 DNS 服务器，而是作为代理来递归访问真正的 DNS 服务器
2. **根域名服务器（root）**：根据域名后缀提供顶级域名服务器的 IP 地址
3. **顶级域名服务器（TLD）**：根据域名前缀提供权威域名服务器的 IP 地址
4. **权威域名服务器（authoritative）**：负责将域名映射到目标服务器的 IP 地址

> 由于根域名服务器的数量很少而且并不是均匀分布，显然不可能处理全球每秒几十亿的 QPS，实际上本地 DNS 服务器缓存了大量顶级域名服务器和权威域名服务器的 IP 地址，绝大部分请求都会直接跳过根域名服务器，甚至还会跳过顶级域名服务器

<img src="https://dasi-blog.oss-cn-guangzhou.aliyuncs.com/Java/202509292227404.png" alt="image-20250929222756294" style="zoom:50%;" />

### DNS 记录

权威域名服务器在响应查询的是，会查询自己的数据库，其中的条目被称为资源记录（Resource Record, RR），是一个包含 Name、Value、Type 和 TTL 的四元组，不同的 Type 对应的 Name:Value 意义不同，而 TTL 是该资源记录的存活时间

> 在 DNS 配置里，**Name 是相对当前域名的写法，如果要表示当前域名则用 @**

| **Type** | **Name** | **Value**            | **说明**                         |
| -------- | -------- | -------------------- | -------------------------------- |
| A        | 域名     | IPv4 地址            | 把域名映射到 IPv4 地址           |
| AAAA     | 域名     | IPv6 地址            | 把域名映射到 IPv6 地址           |
| CNAME    | 域名     | 域名                 | 把一个域名设置为另一个域名的别名 |
| MX       | 域名     | 邮件服务器的域名     | 指定邮件服务器和优先级           |
| NS       | 域名     | 权威域名服务器的域名 | 指定管理该域名的权威域名服务器   |
| PTR      | IP       | 域名                 | 把 IP 地址映射回域名             |
| TXT      | 域名     | 文本信息             | 保存任意文本                     |

### DNS 劫持

**DNS 劫持（Hijacking）**指的是在 DNS 解析链路中被恶意篡改，使域名解析到错误的 IP，从而实现钓鱼、流量劫持、广告注入等

- 本地劫持：修改用户电脑上的本地 DNS 缓存，把域名解析为恶意 IP 地址
- 路由器劫持：修改路由器的 DNS 配置，把解析请求指向恶意 DNS 服务器
- 权威域名服务器劫持：如果用户关于域名注册商的账号密码丢失，黑客可以直接修改 A 记录解析为恶意 IP 地址





