# Session

## 概述

什么是会话：是为了在多次请求之间维持“同一个用户”或“同一次交互”而建立的一段服务器端状态存储与管理机制

为什么需要管理会话
- HTTP 是无状态的：HTTP 协议本身不保存前后请求的任何上下文，服务器无法通过 HTTP 协议来区分两次来自同意客户端的请求
- 身份识别：区分同一客户端在不同时刻发出的多次请求，确保服务端能将它们“看作”同一个会话，防止进行多次身份验证
- 状态持久化：在会话作用域内存储用户登录信息、购物车、临时数据等，使多个请求间能够共享
- 安全控制：通过会话控制访问权限，绑定验证码、CSRF 令牌等安全数据

会话标识：由服务端生成，在服务端全局唯一的字符串
- 默认机制：Cookie（JSESSIONID）
- 备用机制：URL 重写（;jsessionid=…）

## Cookie

工作流程
1. 客户端第一次向服务端发起请求
2. 服务端为客户端创建一个 Cookie，并放入响应对象中
3. Tomcat 容器将 Cookie 转化为 set-cookie 响应头，发送给客户端
4. 客户端会缓存 Cookie到本地
5. 客户端在该 Cookie 作用域内的每次请求，都会自动在请求头中加入 Cookie
6. 服务端读取到 Cookie，从而识别同一会话

组成
- 名称（Name）：作为键标识 Cookie
- 值（Value）：与名称配对的字符串，存储实际数据
- 域（Domain）：指明哪些域名能接收该 Cookie
- 路径（Path）：限定浏览器访问哪些 URL 时会带上此 Cookie
- 最大存活时间（Max-Age）/ 过期时间（Expires）：决定 Cookie 在客户端保存多久
- 安全标志（Secure）：仅在 HTTPS 环境下发送
- HttpOnly：防止客户端脚本（JavaScript）读取

特点：
- 安全性弱：内容通常是明文存储在客户端，易被查看或篡改，因此不存储敏感或隐私的数据
- 轻量级：每条 Cookie 大小通常限制在 4KB 左右

Cookie API
- new Cookie(String name, String value)：构造器，传递名称和值
- cookie.setDomain(String domain)：设置域名
- cookie.setPath(String path)：设置路径
- cookie.setMaxAge(int seconds)：设置存活时长（秒），-1 表示会话级，0 表示删除 Cookie
- cookie.setSecure(true)：设置仅 HTTPS 发送 
- cookie.setHttpOnly(true)：设置脚本不可访问 
- cookie.setComment(String comment)：设置注释 
- void response.addCookie(cookie)：调用响应对象设置 Cookie
- Cookie[] request.getCookies()：获取请求头中的所有 Cookie
- cookie.getName()：获取 cookie 名称
- cookie.getValue()：获取 cookie 值

## HttpSession

HttpSession 是 Servlet 容器为每个客户端会话维护的服务器端状态对象，用于在多次 HTTP 请求之间保存用户数据和上下文
- 每一个 HttpSession 对象对应一次客户端—服务器之间的会话，常用于在服务端记录敏感信息
- 每个会话由唯一的标识符 JSESSIONID 关联到对应的 HttpSession 
- HttpSession 缓存数据在服务端，但是仍然通过 Cookie 来维持 HttpSession 的会话

HttpSession 不是通过构造器获得的，而是通过 `request.getSession()` 获得，底层逻辑为：
1. 从 HttpServletRequest 中读取所有 Cookie，查找名称为 JSESSIONID 的 Cookie，如果没有，就检查请求 URI 上是否带有 ;jsessionid=<id> 片段
2. 如果找到，Manager 根据 Session ID 查找当前 Web 应用下所有活跃的 Session，如果找到则返回对应的 Session 对象
3. 如果没有 Session ID 或者没有找到对应的 Session 对象，则 Manager 会自动创建新 Session，并分配一个全局唯一的 ID，然后返回该 Session 对象
4. 如果本次调用创建了新 Session，容器会在后续的响应阶段生成 `Set-Cookie: JSESSIONID=<newId>; Path=<contextPath>; HttpOnly`

Session 生命周期维护
- 访问更新：每次请求访问时，容器都会在 Manager 中更新该 Session 的“最后访问时间”，用于超时淘汰
- 超时失效：定期调度或在下一次访问时，若 lastAccessed + maxInactiveInterval < now，容器会自动从 Manager 中移除会话
- 手动销毁：应用调用 session.invalidate()，容器立即清理属性并从全局表中删除，并在本次及后续请求中都不再返回旧 Session

HttpSession API
- 获取／创建会话
  - HttpSession request.getSession()：获取会话对象
- 会话标识与状态
  - String session.getId()：返回此次会话的唯一的 JSESSIONID
  - session.isNew()：判断会话是否刚刚创建
- 属性存取
  - void session.setAttribute(String name, Object value)：存储任意可序列化对象到会话作用域
  - Object session.getAttribute(String name)：获取指定名称的属性
  - void session.removeAttribute(String name)：删除指定属性
- 生命周期管理
  - void session.invalidate()：立即销毁会话，删除所有属性，并将其从容器中移除
  - void session.setMaxInactiveInterval(int seconds)：设置超时时间
  - int session.getMaxInactiveInterval()：获取超时时间
  - long session.getLastAccessedTime()：获取上次请求时间戳
  - long session.getCreationTime()：获取会话创建时间戳

## 域对象

域对象：指容器在不同生命周期/作用范围内，为我们自动维护的几种属性存储空间，本质上都是一组以字符串为键、任意对象为值的 Map，用来在不同组件或多次请求间共享数据

|域对象|生命周期|接口|常用|
|-|-|-|-|
|请求域（Request）| 一次 HTTP 请求|HttpServletRequest|多级转发间共享参数，存储本次服务要用到的临时数据|
|会话域（Session）|一个客户端会话|HttpSession|多请求间共享参数，存储登陆用户信息、购物车信息|
|应用域（Context）|一个 Web 应用|ServletContext|多路径间共享参数，存储全局配置|

三个 API
- void setAttribute(String name, Object value)：设置属性
- Object getAttribute(String name)：获取属性
- void removeAttribute(String name)：删除属性