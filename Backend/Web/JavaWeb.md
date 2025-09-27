# JavaWeb



   * [概述](#概述)
      * [定义](#定义)
      * [Web 容器](#web-容器)
      * [应用程序的生命周期](#应用程序的生命周期)
      * [几个 J](#几个-j)
      * [MVC 架构模式](#mvc-架构模式)
   * [HTTP](#http)
      * [HTTP 版本](#http-版本)
      * [HTTP 报文](#http-报文)
   * [Tomcat](#tomcat)
      * [根目录结构](#根目录结构)
      * [应用目录结构](#应用目录结构)
      * [开发流程](#开发流程)
      * [服务流程](#服务流程)
   * [路径配置](#路径配置)
      * [**url-pattern**](#url-pattern)
      * [**@WebServlet**](#webservlet)
   * [Servlet](#servlet)
      * [定义](#定义)
      * [生命周期](#生命周期)
      * [DefaultServlet](#defaultservlet)
      * [HttpServlet](#httpservlet)
      * [ServletConfig 和 ServletContext](#servletconfig-和-servletcontext)
   * [请求和响应](#请求和响应)
      * [HttpServletRequest](#httpservletrequest)
      * [HttpServletResponse](#httpservletresponse)
      * [请求转发](#请求转发)
      * [响应重定向](#响应重定向)
      * [乱码问题](#乱码问题)
      * [路径问题](#路径问题)
   * [Session](#session)
      * [定义](#定义)
      * [Cookie](#cookie)
      * [HttpSession](#httpsession)
   * [Listener](#listener)
      * [域对象](#域对象)
      * [类事件](#类事件)
      * [监听器](#监听器)
   * [Filter](#filter)
      * [概述](#概述)
      * [配置过滤器](#配置过滤器)
      * [doFilter](#dofilter)



## 概述

### 定义

**JavaWeb = 用 Java 技术开发基于 Web 的应用程序**

- Web 前端：HTML / CSS / JavaScript，负责页面展示和交互
- Web 后端：Servlet、JSP、JDBC，负责解析请求、生成响应、访问数据库以及页面渲染
- Web 容器：Tomcat，负责接收 HTTP 请求，返回 HTTP 响应，管理 Servlet 生命周期

工作流程

1. 用户在浏览器发出请求（http://…）
2. Web 容器（Tomcat）接收请求，找到对应的 Servlet
3. Servlet 执行业务逻辑，必要时访问数据库（JDBC、连接池）
4. 生成结果（JSP/HTML/JSON），返回给浏览器
5. 浏览器渲染结果，用户看到页面

### Web 容器

运行在服务端，负责托管和管理 Web 应用的基础服务组件，提供必要的运行环境和基础服务

- **管理 Servlet 生命周期**：实例化、初始化、销毁
- **请求接收与分发**：监听指定端口（8080），接收来自浏览器的 HTTP 请求，并根据 URL 映射规则将请求分发到对应的 Servlet
- **业务处理**：Servlet 调用业务层方法处理具体业务逻辑
- **响应生成与返回**：将处理结果封装成响应数据（如 HTML、JSON、XML）发回给浏览器
- **扩展服务**：安全认证、会话管理、过滤器、监听器等

### 应用程序的生命周期

- **开发（develop）**：人敲键盘写代码的过程
- **构建（build）**：把源代码编译、打包成可执行应用的过程，比如将 .java 编译成 .class，并和网页资源、依赖库一起打包进 .war 文件
- **部署（deploy）**：把构建好的应用包放到服务器上运行，让其他用户通过网络访问到
- **测试（test）**：检查应用是否按照预期工作，找出BUG，验证功能正确性的过程
- **运维（operate）**：应用上线后的运行维护工作，包括服务器管理、监控、日志分析、备份恢复、故障排查等

### 几个 J

- **JRE（Java Runtime Environment）**：Java 运行环境，包含 JVM 和 JCL 以及其他配套资源
- **JVM（Java Virtual Machine**）：Java 虚拟机，负责把 Java 字节码（.class 文件）翻译成操作系统能执行的指令
- **JCL（Java Class Libraries）**：Java 类库，具备一大堆预定义好的 Java 类，提供开发中最基础的功能
- **JDK（Java Development Kit）**：Java 开发工具包，是写、编译、调试 Java 程序的一整套工具合集
- **JDB（Java Debugger）**：Java 调试工具，用来在命令行下调试 Java 程序，比如设置断点、单步执行、查看变量值
- **JAR（Java Archive）**：Java 归档包，把多个 .class 文件和资源文件打包成一个文件，方便部署、传输
- **JSP（JavaServer Pages）**：Java 服务器页面技术，让开发者能在HTML网页中直接嵌入Java代码或表达式，从而用来动态生成网页内容

### MVC 架构模式

MVC = Model + View + Controller，是一种经典的软件设计模式，用于分离应用程序中的不同关注点，实现高内聚低耦合，提高代码的可维护性、可扩展性和可复用性

- Model 模型层：管理数据和业务逻辑，进行与数据库的交互 -> JavaBean, DAO, POJO
- View 视图层：展示数据，负责用户界面和交互 -> JSP, HTML, CSS, JS
- Controller 控制层：接收请求，返回响应，协调 Model 和 View -> Servlet

Model 的几个名词解析

- POJO（Plain Old Java Object）：普通的类，不继承任何特定类，不实现特定接口
- Bean：有规范的类，必须有无参构造器，属性必须是私有的，提供全部成员变量的 getter 和 setter
- DAO（Data Access Object）：专门负责跟数据库打交道的类，封装了 CRUD 方法



## HTTP

### HTTP 版本

在这里主要列举，后一个版本相比于前一个版本的改进之处

HTTP/0.9：初代协议

- 支持一种请求方法：GET
- 没有头部
- 没有状态码
- 底层基于 TCP 协议
- 默认使用 80 端口
- 直接返回资源内容，只支持 HTML 文件
- **每个请求都必须新建一个连接**
- 报文内容明文传输

HTTP/1.0：增加元信息

- 支持三种请求方法：GET、HEAD、POST
- 增加了请求头和响应头，能够携带元信息
- 引入状态码，更清晰地反馈请求结果
- 增加简单缓存控制，提高重复请求效率
- 内容类型能够传输 HTML 文件以外的文档
- 只支持短连接，即每个请求都必须新建一个连接

HTTP/1.1：官方标准

- 支持七种请求方法：GET、HEAD、POST、OPTIONS、PUT、DELETE、TRACE
- **支持管道化，客户端在收到响应前连续发送多个请求**
- **支持长连接，同一 TCP 连接可复用**
- 更完备的缓存与协商机制，优化带宽利用
- 状态码进行了扩展
- 虚拟主机支持，让一台服务器承载多个域名

HTTP/2：性能优化

- 采用二进制分帧与流模型
- **支持多路复用，单一 TCP 连接可并发处理任意数量的双向流，消除队头阻塞**
- 支持头部压缩
- 允许服务器主动推送资源

HTTP/3：移动优化

- 基于 UDP 重建了 QUIC 传输机制
- 更快速的连接建立与恢复，适应移动网络环境
- 强制加密简化安全配置，提高传输安全性

HTTPS：安全优化

- 在 HTTP(x.x) 之上增加 SSL/TLS 加密层，报文全程加密，防止中间人攻击、窃听、篡改 
- 服务器需持有 CA 颁发的 X.509 证书，客户端验证证书链与域名
- 需要先进行 TLS 握手，建立安全信道后再传输 HTTP 报文
- 默认使用 443 端口

### HTTP 报文

报文格式

- 行：
    - 请求：<方法> <路径> <版本>
    - 响应：<版本> <状态码> <原因短语>
- 头：一系列以 `字段名: 值` 形式出现的行，携带元信息
- 空行：CRLF 分隔首部与消息体
- 体：
    - 请求：表单数据、JSON、XML 等
    - 响应：HTML、图片、视频、脚本等

MIME（Multipurpose Internet Mail Extensions） 是一种标准，用于在互联网中标识和描述各种媒体类型的数据格式

- 作用：让客户端／服务器这是个什么文件，如何解析传来的机器编码
- 格式：主类型/子类型[; 参数]
- 请求头的键：`Accept`
- 响应头的键：`Content-Type`
- 类型
    - 文本：`text/html; charset=utf-8`
    - 图像：`image/jpeg，image/png`
    - 音视频：`audio/mpeg，video/mp4`
    - 应用数据：`application/json，application/xml`

状态码

- 1xx：信息类
    - 100 Continue：客户端应继续发送请求的剩余部分
    - 101 Switching Protocols：服务器已理解客户端请求，并将使用不同协议进行通讯
- 2xx：成功类
    - 200 OK：请求已成功，请求所希望的响应头或数据体随之返回
    - 201 Created：请求已成功且服务器创建了新的资源
    - 204 No Content：服务器成功处理了请求，但不返回任何内容
- 3xx：重定向类
    - 301 Moved Permanently：所请求的资源已永久移动到新 URI，客户端以后应使用新地址
    - 302 Found：资源临时移动，客户端仍应继续使用原有 URI 进行请求
    - 304 Not Modified：客户端缓存的资源未修改，可直接使用本地缓存，减少带宽
- 4xx：客户端错误类
    - 400 Bad Request：请求报文有语法错误或参数不合法，服务器无法理解
    - 401 Unauthorized：请求未通过身份验证，需提供有效凭证
    - 403 Forbidden：服务器理解请求但拒绝执行，权限不足或禁止访问
    - 404 Not Found：所请求的资源不存在或已被删除
    - 405 Method Not Allowed：客户端请求中的 HTTP 方法不被服务器允许用于所请求的资源 URL
    - 408 Request Timeout：客户端在服务器规定的等待时间内未发送完整请求
    - 429 Too Many Requests：客户端在给定时间内发送了过多请求，被服务器限流
- 5xx：服务端错误类
    - 500 Internal Server Error：服务器遇到意外情况，无法完成请求
    - 502 Bad Gateway：服务器作为网关或代理，从上游服务器收到无效响应
    - 503 Service Unavailable：服务器当前不可访问，无法处理请求
    - 504 Gateway Timeout：服务器作为网关或代理，但未及时从上游服务器收到响应



## Tomcat

### 根目录结构

```text
apache-tomcat-9.0.XX/
├── bin/               # 启动/关闭脚本
├── conf/              # 配置文件
│   ├── server.xml     # Tomcat 自身配置
│   ├── web.xml        # 默认 Web 应用配置
│   └── context.xml    # 应用上下文配置
├── lib/               # Tomcat 运行依赖 jar 包
├── logs/              # 运行日志
├── webapps/           # 部署 Web 应用目录
├── work/              # JSP 编译后生成的 class 文件等临时工作目录
└── temp/              # 临时文件目录 (重启清空)
```

### 应用目录结构

```text
myapp/                  # Web 应用的根目录 (项目名就是应用上下文路径)
├── index.html/jsp      # 网站入口页，可以直接通过浏览器访问
├── login.html/jsp      # 其他页面
├── static/             # 静态资源
│    ├── css/           # 样式文件
│    ├── js/            # 脚本文件
│    └── images/        # 图片文件
└── WEB-INF/            # 受保护的目录（浏览器无法直接访问）
     ├── web.xml        # 部署描述符 (配置Servlet/Filter/Listener)
     ├── classes/       # 编译好的 .class 文件（Servlet等）
     └── lib/           # 项目依赖的 jar 包 (如数据库驱动)
```

### 开发流程

1. 创建一个项目，并 Add Framework Support，添加 Web Application，变为一个 JavaWeb 项目
2. 给项目添加 Tomcat 依赖
3. 编写自己的 Servlet 类，继承 HttpServlet（因为暂时不需要实现全部接口）
4. 重写 protected void service(HttpServletRequest req, HttpServletResponse resp) 方法，自定义业务逻辑
    1. 从 request 对象中获取任何请求信息
    2. 业务处理
    3. 将响应数据放入 response 对象
5. 在 web.xml 中配置 Servlet 对应的 URL
6. 配置 Tomcat 运行时的构建项目，自定义上下文路径

### 服务流程

1. 浏览器发送 HTTP 请求到 Tomcat，Tomcat 解析请求报文，生成 HttpServletRequest 和 HttpServletResponse 对象
2. Tomcat 根据请求 URI，在 web.xml 或 @WebServlet 注解中查找对应的 Servlet 映射关系
3. 若 Servlet 实例不存在，Tomcat 通过反射创建并调用 init() 初始化；然后为请求分配线程，调用 service(request, response) 方法
4. Servlet 根据请求类型调用 doGet() 或 doPost() 等方法，完成业务逻辑处理，并将结果写入 HttpServletResponse
5. Tomcat 将 HttpServletResponse 转换为 HTTP 响应报文，发送回客户端，同时释放线程和请求资源



## 路径配置

### **url-pattern**

精确匹配 > 最长路径前缀匹配 > 扩展名匹配 > 根匹配，必须以 / 开头，通配符只能出现一次，同一个 url-pattern 只能映射给一个 Servlet，但是一个 Servlet 可以在多个 \<servlet-mapping> 中使用不同的 url-pattern

- 精准匹配：/xxx，只有请求路径完全相同时才命中  
- 前缀匹配/目录匹配：/xxx/*，匹配目录 /xxx/ 下的所有请求
- 后缀匹配/扩展名匹配：*.xxx，匹配所有文件后缀名是 xxx 的请求
- 根匹配：/，匹配所有请求

```xml
<servlet>
    <servlet-name>Servlet1</servlet-name>
    <servlet-class>com.dasi.servlet.Servlet1</servlet-class>
</servlet>

<servlet-mapping>
    <servlet-name>Servlet1</servlet-name>
    <url-pattern>/s1</url-pattern>
    <url-pattern>/ss1</url-pattern>
</servlet-mapping>
```

### **@WebServlet**

在代码块内编写以下键值对

- String name：Servlet 的逻辑名称
- String[] urlPatterns/value：一个 Servlet 对应的多个 URL 模式

```java
@WebServlet(value = {"/s1", "/ss1"})
public class Servlet1 extends HttpServlet {
    @Override
    public void service(ServletRequest req, ServletResponse res) throws ServletException, IOException {
        System.out.println("servlet1 runs");
    }
}
```

> web.xml 和 @WebServlet 只能选择一个，不能同时使用，否则会报错



## Servlet

### 定义

**Servlet（Server Applet） 是运行在 Web 容器中的 Java 服务端程序，它遵循 Servlet 规范，实现了 Servlet 接口，负责处理客户端发来的请求，并生成响应**

- **单实例**：每个 Servlet 在容器中默认只会被实例化一次
- **线程级别**：每次请求由容器从线程池中取出一个线程来执行 service() 方法
- **成员变量共享**：Servlet 的成员变量在多个线程中是共享的

```java
public interface Servlet {

    // 初始化方法：容器在加载 Servlet 时调用一次
    void init(ServletConfig config) throws ServletException;

    // 获取 Servlet 的配置信息
    ServletConfig getServletConfig();

    // 核心方法：处理请求并生成响应
    void service(ServletRequest req, ServletResponse res)
        throws ServletException, IOException;

    // 获取 Servlet 的信息（作者、版本等）
    String getServletInfo();

    // 销毁方法：容器卸载或关闭时调用一次
    void destroy();
}
```

### 生命周期

1. **加载 & 实例化**：第一次请求时或容器启动时加载，调用构造方法
2. **初始化**：调用 init() 方法
3. **请求处理**：每次请求调用 service()，根据请求类型分发到 doGet() / doPost()
4. **销毁**：容器关闭或卸载应用时调用 destroy()

### DefaultServlet

- 是容器提供的、用于高效服务静态资源的 servlet
- 被映射到 / 下，在容器层面优先级最低，确保所有动态请求先行处理
- 如果请求的是文件，会读取读取该文件的内容，写入响应
- 如果请求的是目录，并且目录下没有默认首页，会返回 404
- 可以通过修改 web.xml 或容器配置，调整它的缓存策略、目录列表、路径映射等

### HttpServlet

继承关系：Servlet -> GenericServlet -> HttpServlet

- 将原始的 ServletRequest、ServletResponse 转换为 **HttpServletRequest**、**HttpServletResponse**，这样就可以直接获取到请求内容
- 其 service(HttpServletRequest req, HttpServletResponse resp) 方法会根据请求方式自动调用对应的模板方法
- 提供了一系列 protected 的 doXxx 模板方法，开发者只需重写相应的 doXxx 方法即可

### ServletConfig 和 ServletContext

| 项目         | ServletConfig                           | ServletContext                                           |
| ------------ | --------------------------------------- | -------------------------------------------------------- |
| 作用对象     | 单个 Servlet 的初始化配置               | 整个 Web 应用的全局共享信息                              |
| 生命周期     | Servlet 创建时存在，Servlet销毁时消失   | 应用启动时存在，应用停止时销毁                           |
| 创建者       | 容器在实例化 Servlet 时创建             | 容器在启动 Web 应用时就创建                              |
| 数据内容     | 只有属于某个 Servlet 的 init-param 参数 | 整个项目（应用）范围内共享的资源、参数                   |
| 通常用来干嘛 | 给单个 Servlet 配一些启动参数           | 共享全局资源，比如全站路径、全局配置信息、项目级别的数据 |

在 web.xml 的 \<servlet> 标签中添加 \<init-param> 标签来配置 ServletConfig

```xml
<servlet>
    <servlet-name>servlet1</servlet-name>
    <servlet-class>com.dasi.servlet.Servlet1</servlet-class>
    <init-param>
        <param-name>keya</param-name>
        <param-value>valuea</param-value>
    </init-param>
    <init-param>
        <param-name>keyb</param-name>
        <param-value>valueb</param-value>
    </init-param>
</servlet>
```

在 @WebServlet 注解配置 initParamas 参数来配置 ServletConfig

```java
@WebServlet(
    name = "Servlet1",
    urlPatterns = {"/servlet1"},
    initParams = {
        @WebInitParam(name = "keya", value = "valuea"),
        @WebInitParam(name = "keyb", value = "valueb")
    }
)
```

在 web.xml 中使用标签 \<context-param> 来配置 ServletContext

```xml
<context-param>
    <param-name>key_a</param-name>
    <param-value>value_a</param-value>
</context-param>
<context-param>
    <param-name>key_b</param-name>
    <param-value>value_b</param-value>
</context-param>
```



## 请求和响应

### HttpServletRequest

HttpServletRequest 是 Servlet API 中代表 HTTP 请求的接口，扩展了通用的 ServletRequest 接口，增加了对 HTTP 协议特性的访问能力

- 请求行
    - String getMethod()：返回请求方法
    - StringBuffer getRequestURL()：返回完整请求 URL，含协议、主机、端口和 URI
    - String getRequestURI()：返回请求的资源路径部分，不含协议、主机和端口
    - String getContextPath()：返回当前 Web 应用的根路径
    - String getServletPath()：返回匹配到的 Servlet 映射路径
    - int getLocalPort()：返回接受此请求的本地网络接口的端口号
    - int getServerPort()：返回此请求发送到的服务器端口号
    - int getRemotePort()：返回发起此请求的客户端所使用的源端口号
- 请求头
    - String getHeader(String name)：获取指定请求头的值
    - Enumeration<String> getHeaderNames()：返回所有请求头名称
    - Cookie[] getCookies()：获取随请求发送的所有 Cookie，若无则返回 null
- 请求体
    - BufferedReader getReader()：以字符流读取请求体
    - ServletInputStream getInputStream()：以字节流读取请求体
    - String getContentType()：获取请求体的 MIME 类型
    - int getContentLength()：获取请求体长度（字节）
- 请求参数：既可以在 get 中的 url 中，也可以在 post 中的请求体中 
    - String getQueryString()：返回 URL 中 ? 后的查询字符串，但不含 ？
    - String getParameter(String name)：获取单个参数值，表单或 URL 查询参数
    - String[] getParameterValues(String name)：获取同名参数的所有值
    - Map<String,String[]> getParameterMap()：返回所有参数及其值
    - Enumeration<String> getParameterNames()：返回所有参数名

### HttpServletResponse

HttpServletResponse 是 Servlet API 中代表 HTTP 响应的接口，扩展了通用的 ServletResponse 接口，增加了对 HTTP 协议特性控制的能力

- 响应行
    - void setStatus(int sc)：设置 HTTP 响应的状态码
    - int getStatus()：获取当前已设置的状态码
    - void sendError(int sc)：发送指定错误状态码及容器默认的错误页面
    - void sendError(int sc, String msg)：发送错误状态码并携带自定义错误消息
    - void sendRedirect(String location)：发送重定向（302），将客户端导向新的 URL
- 响应头
    - void setHeader(String name, String value)：设置或覆盖单个响应头
    - void addHeader(String name, String value)：追加一个响应头
    - void setDateHeader(String name, long date)：以日期形式设置响应头
    - void setContentType(String type)：设置 Content-Type MIME 类型
    - void setContentLength(int len)：设置 Content-Length
- 响应体
    - PrintWriter getWriter()：获取字符输出流，向客户端写入文本内容
    - ServletOutputStream getOutputStream()：获取字节输出流，向客户端写入二进制内容
    - void setCharacterEncoding(String charset)：设置响应的字符编码

### 请求转发

Forwarding：在服务器内部将当前请求对象和响应对象从一个资源交给另一个资源

- 浏览器的 URL 地址不变
- 转发对客户端是屏蔽的
- 目标资源可以是动态资源如 Servlet，也可以是静态资源 html
- 目标资源不可以访问项目外部资源
- 通过请求转发，可以将请求转发到 WEB-INF 中受保护的资源
- 依旧是原对象返回响应报文，而不是转发对象，最终客户端只接收到一份响应
- RequestDispatcher HttpServletRequest.getRequestDispatcher(String path)：传递目标资源的 Web 路径，返回一个可用的分配器对象
- void RequestDispatcher.forward(ServletRequest request, ServletResponse response)：将对当前请求的请求对象和响应对象转发给另一个资源

### 响应重定向

Redirect：由服务器指示客户端发起新请求

- 服务器发送一个 302 状态码和 Location 头，告知浏览器去请求新的 URL
- 浏览器地址栏会更新为重定向后的新 URL
- 重定向对客户端是透明的，浏览器自动发起第二次请求
- 重定向路径可以是同一应用内的任意路径，也可指向外部域名或其他项目资源
- 重定向路径不能是 WEB-INF 中的路径
- 第一次响应是重定向指令，不包含业务数据，而第二次是对新 URL 的全新请求，使用新的 HttpServletRequest 和 HttpServletResponse
- sendRedirect(...) 发送的是一次 GET 请求，所以原来如果是 POST，第二次都会变成 GET
- HttpServletResponse.sendRedirect(String path)：自动设置为状态码为 302 和响应头为 path
- sendRedirect 调用之后会立即响应给客户端，即使 service 还没有执行完毕，也就是说之后对 response 的写入都是无意义的

### 乱码问题

字符集（Character Set）：字符与码点的映射表，规定了系统能识别和处理的所有字符范围

- 字符：人类语言中最小书写单元，如字母、汉字、符号、数字等
- 码点：字符在字符集里唯一的数字标识

常见的字符集

- ASCII：U+0000–U+007F（0–127），支持英文字母、数字、基本标点等
- ISO-8859-1/Latin-1：U+0000–U+00FF（0–255），支持西欧语言额外字符
- GBK：双字节表示，支持中文汉字
- Unicode：U+0000–U+10FFFF（0-1114112），覆盖几乎全球所有现代／古代文字、符号、表情等

乱码：在编码与解码不匹配时，文本中出现无法识别的符号或问号，表现为一堆异常文字

- 请求解决
    - GET：请求参数在 URI 中，需要在 server.xml 的 \<Connector> 标签上添加属性 URIEncoding=前端字符集
    - POST：请求参数在请求体中，需要在 request.getParameter() 调用之前执行 request.setCharacterEncoding(前端字符集)
- 响应解决
    - 响应体：通过 request.setCharacterEncoding(前端字符集)
    - 响应头：通过 request.setContentType(MIME;charset=前端字符集)

### 路径问题

相对路径：以当前资源的所在 Web 路径作为基准，去定位目标资源

- ./ 或直接写路径：表示当前目录下
- ../：表示上一级目录下
- 开发时 IDE 可能提示找不到资源，但实际浏览器可以正确解析，因为浏览器基于 URL/Web 路径而不是本地文件系统查找

绝对路径：从当前 Web 应用根路径作为基准，定位目标资源

- 以 / 开头
- Web 应用根路径是包含 Context Path 和服务器端口号的路径，若部署 myapp.war 则对应的应用根路径为 `http://localhost:8080/myapp`
- 前端：通过 \<base href="/myapp/"> 设置根路径，统一相对路径解析基准
- 后端：
    - 对内：包含 contextPath，无需手动添加，如请求转发
    - 对外：不包含 contextPath，需要使用 request.getContextPath() 获取根路径之后拼接，如请求重定向



## Session

### 定义

会话是**为了在多次请求之间维持“同一个用户”或“同一次交互”而建立的一段服务器端状态存储与管理机制**

- HTTP 是无状态的：HTTP 协议本身不保存前后请求的任何上下文，服务器无法通过 HTTP 协议来区分两次来自同意客户端的请求
- 身份识别：区分同一客户端在不同时刻发出的多次请求，确保服务端能将它们“看作”同一个会话，防止进行多次身份验证
- 状态持久化：在会话作用域内存储用户登录信息、购物车、临时数据等，使多个请求间能够共享
- 安全控制：通过会话控制访问权限，绑定验证码、CSRF 令牌等安全数据
- 会话标识是由服务端生成，在服务端全局唯一的字符串

### Cookie

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

### HttpSession

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



## Listener

### 域对象

**域对象是由容器维护的属性存储空间，本质是 Map<String, Object>，用于在不同组件或多次请求间共享数据**

- void setAttribute(String name, Object value)：设置属性
- Object getAttribute(String name)：获取属性
- void removeAttribute(String name)：删除属性

| 域对象            | 生命周期       | 接口               | 常用                                             |
| ----------------- | -------------- | ------------------ | ------------------------------------------------ |
| 请求域（Request） | 一次 HTTP 请求 | HttpServletRequest | 多级转发间共享参数，存储本次服务要用到的临时数据 |
| 会话域（Session） | 一个客户端会话 | HttpSession        | 多请求间共享参数，存储登陆用户信息、购物车信息   |
| 应用域（Context） | 一个 Web 应用  | ServletContext     | 多路径间共享参数，存储全局配置                   |

### 类事件

**是域对象对应的生命周期事件**

- **创建**：新会话、请求到达、应用启动
- **销毁**：请求结束、会话超时、应用卸载
- **属性变化事件**：setAttribute、removeAttribute
- **绑定/解绑**：对象与 HttpSession 绑定或移除
- **钝化/活化**：Session 序列化到磁盘或恢复到内存

### 监听器

**监听器是用于监听 Web 应用生命周期事件或域对象状态变化的组件，并不监听项目中所有组件，而是针对于三大域对象及其类事件**

- 按域对象划分
    - 应用域：ServletContextListener、ServletContextAttributeListener
    - 会话域：HttpSessionListener、HttpSessionAttributeListener、HttpSessionBindingListener、HttpSessionActivationListener
    - 请求域：ServletRequestListener、ServletRequestAttributeListener
- 按类事件划分
    - 创建与销毁：ServletContextListener、HttpSessionListener、ServletRequestListener
    - 属性变化：ServletContextAttributeListener、HttpSessionAttributeListener、ServletRequestAttributeListener
    - 绑定激活：HttpSessionBindingListener 、HttpSessionActivationListener



## Filter

### 概述

过滤器用于在请求到达 Servlet 前对数据进行预处理，或响应返回客户端前对数据进行后处理

- 日志记录：记录请求或响应信息，如 URL、客户端 IP、时间戳等，方便追踪用户操作和排查问题
- 性能分析：可以记录处理前后时间戳，从而计算得到耗时，统计到监控系统，用于分析各接口响应性能瓶颈
- 乱码处理：在预处理阶段强制设置请求和响应的字符编码，确保所有后续 Servlet/Filter 都以相同编码读写数据，彻底杜绝乱码
- 事务控制：在预处理时开启事务，完成业务逻辑后，根据执行结果决定提交还是回滚
- 登陆控制：在预处理阶段检查会话中是否已有登录标志，从而跳过验证
- 跨域处理：在预处理时为响应统一添加跨域允许头，让后端接口支持跨域访问

生命周期

1. 构造：容器部署 Web 应用时，会根据 web.xml 或 @WebFilter 实例化每个 Filter
2. 初始化：调用一次 filter.init(FilterConfig config)
3. 过滤：对于每次匹配的请求，容器都会调用一次 doFilter(ServletRequest req, ServletResponse res, FilterChain chain)
4. 销毁：容器关闭 Web 应用时，调用一次 filter.destroy()

### 配置过滤器

@WebFilter 配置的几个字段，注解的方式无法指定 filter 顺序

- filterName：过滤器名称，默认类名
- value/urlPatterns：要拦截的 URL 路径
- servletNames：要拦截的 Servlet 名称
- initParams：初始化参数

web.xml 配置方法，filter 顺序取决于 \<filter-mapping> 的先后顺序

```xml
  <!-- 1. 定义 Filter -->
  <filter>
    <filter-name>MyFilter</filter-name>
    <filter-class>com.dasi.filter.MyFilter</filter-class>
    <!-- 初始化参数 -->
    <init-param>
      <param-name>loginPage</param-name>
      <param-value>/login.jsp</param-value>
    </init-param>
  </filter>

  <!-- 2. 映射 Filter -->
  <filter-mapping>
    <filter-name>AuthFilter</filter-name>
    <url-pattern>/path/to/xxx</url-pattern>
    <url-pattern>*.html</url-pattern>
    <url-pattern>/servlet/*</url-pattern>
  </filter-mapping>
```

### doFilter

有三个模块

- 预处理：在调用下一个 Filter 或进入 Servlet 之前执行的代码，通常是对请求进行处理
- 放行：执行 chain.doFilter(request, response)，将控制权交给下一个 Filter 或最终的 Servlet
- 后处理：执行完 Servlet 之后执行的代码，通常是对响应进行处理

```java
public void doFilter(ServletRequest req, ServletResponse res, FilterChain chain)
        throws IOException, ServletException {
    // 1. 预处理
    long start = System.currentTimeMillis();
    // 2. 放行
    chain.doFilter(req, res);
    // 3. 后处理
    long duration = System.currentTimeMillis() - start;
    System.out.println("请求处理耗时：" + duration + "ms");
}
```

> Servlet 4.0 提供了 javax.servlet.http.HttpFilter，它已经给你写好了空的 init() 和 destroy()，因此可以只需要关心 doFilter()

FilterChain：表示一条由若干 Filter 和最终目标资源（Servlet/JSP）组成的链条

- 在容器内部构建
- 每次调用 chain.doFilter() 就会依次执行下一个 Filter
- Filter 的执行顺序和返回顺序相反