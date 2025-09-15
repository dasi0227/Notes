## Tomcat 和 Servlet

### Tomcat 服务流程

1. Tomcat 接收到请求后，将 HTTP 报文解析，构造出 HttpServletRequest 对象封装请求行、头、体、参数等，并创建了一个空的HttpServletResponse 对象
2. Tomcat 根据请求的 URI 去 web.xml 映射或 @WebServlet 注解中查找对应的 Servlet
3. Tomcat 根据请求中的 URL，查找匹配的 web.xml 或 注解 @WebServlet 中配置的 Servlet 映射 
4. Tomcat 会实例化并初始化 Servlet 对象，并为每个请求新建一个线程，在该线程中调用 Servlet 的 service(request, response)
5. Tomcat 最终将 HttpServletResponse 对象转化为响应报文，发回给客户端，并释放该请求对应的线程

### IntelliJ 开发流程

1. 创建一个项目，并 Add Framework Support，添加 Web Application，变为一个 JavaWeb 项目
2. 给项目添加 Tomcat 依赖
3. 编写自己的 Servlet 类，继承 HttpServlet（因为暂时不需要实现全部接口）
4. 重写 protected void service(HttpServletRequest req, HttpServletResponse resp) 方法，自定义业务逻辑
   1. 从 request 对象中获取任何请求信息
   2. 业务处理
   3. 将响应数据放入 response 对象
5. 在 web.xml 中配置 Servlet 对应的 URL
   - \<servlet>：定义一个实例
     - \<servlet-name>：标识该 Servlet 的唯一名称
     - \<servlet-class>：指定该 Servlet 的全类名（含包名），容器会通过反射加载并实例化
   - \<servlet-mapping>：将上面定义好的某个 Servlet 与一个或多个 URL 模式关联
     - \<servlet-name>：与上面定义的名称保持一致
     - \<url-pattern>：指定该 Servlet 处理的请求路径模式
6. 配置 Tomcat 运行时的构建项目，自定义上下文路径

### 路径配置

url-pattern 的匹配方式：精确匹配 > 最长路径前缀匹配 > 扩展名匹配 > 根匹配 
- 精准匹配：/xxx，只有请求路径完全相同时才命中  
- 前缀匹配/目录匹配：/xxx/*，匹配目录 /xxx/ 下的所有请求
- 后缀匹配/扩展名匹配：*.xxx，匹配所有文件后缀名是 xxx 的请求
- 根匹配：/，匹配所有请求

注意
- 路径匹配都必须以 / 开头
- 通配符只能出现一次
- 同一个 url-pattern 只能映射给一个 Servlet，不能重复
- 一个 Servlet 可以在多个 \<servlet-mapping> 中使用不同的 url-pattern，实现多路访问

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


注解 @WebServlet 的匹配方式，在代码块内编写以下键值对
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

> 注意，web.xml 和 @WebServlet 只能选择一个，不能同时使用，否则会报错

## Servlet

### 生命周期

1. 实例化：容器查找并加载对应的 Servlet 类，然后使用无参构造函数创建该类的一个实例
2. 初始化：容器通过调用 Servlet.init(ServletConfig config) 方法，对刚创建的实例进行一次性初始化
3. 服务：每当有客户端请求到来，容器会调用先前 Servlet 实例的 service(HttpServletRequest req, HttpServletResponse resp) 方法
4. 销毁：当容器决定卸载该 Servlet，容器会调用一次 Servlet.destroy()

Servlet 特性
- Servlet 在容器里只会被实例化一次
- 当有请求到达，容器会从内部维护的线程池里取出一个线程来调用 service 方法
- Servlet 的成员变量在多个线程中是共享的

### DefaultServlet

- 是容器提供的、用于高效服务静态资源的 servlet
- 被映射到 / 下，在容器层面优先级最低，确保所有动态请求先行处理
- 如果请求的是文件，会读取读取该文件的内容，写入响应
- 如果请求的是目录，并且目录下没有默认首页，会返回 404
- 可以通过修改 web.xml 或容器配置，调整它的缓存策略、目录列表、路径映射等

### 继承结构

Servlet -> GenericServlet -> HttpServlet -> MyServlet

Servlet 接口：定义了 Servlet 的核心生命周期和行为
- void service(ServletRequest req, ServletResponse res) throws ServletException, IOException
  - 传入请求对象和响应对象
  - 每有一次客户端请求到达，容器就会在新的线程中调用此方法
- void init(ServletConfig config) throws ServletException
  - Servlet 被容器加载并实例化后调用并只调用一次，用于完成初始化操作
  - 参数 ServletConfig 提供初始化配置信息
- void destroy()
  - 在容器卸载 Servlet 或关闭应用时调用一次，用于释放占用资源
- ServletConfig getServletConfig()
  - 在 Servlet 运行期间，获取对应的配置信息
- String getServletInfo()
  - 返回 Servlet 的简要描述信息，供管理监控使用

GenericServlet：保存配置，并提供了除 service 方法的平庸实现
- 实现了 void init(ServletConfig config)，保存 ServletConfig 引用并调用无参 init()
- 平庸实现了无参 init()、destroy()、getServletConfig()、getServletInfo()
- 抽象了 service(ServletRequest, ServletResponse)，留给子类去实现具体协议

HttpServlet：实现了对 HTTP 协议的支持
- 重写了 service(ServletRequest, ServletResponse)，将参数转换为 HttpServletRequest / HttpServletResponse，然后再调用对应的 service
- 定义了 service(HttpServletRequest, HttpServletResponse)，根据请求方法分发到相应的 doXXX 方法
- 提供了一系列 protected 的 doXxx 模板方法，子类可选择性覆盖，专注处理对应 HTTP 方法的逻辑

MyServlet：完成自定义业务逻辑
- 重写 service 方法
- 重写 doXXX 方法

### ServletConfig 和 ServletContext

| 项目     | ServletConfig                                   | ServletContext                                                             |
|--------|-------------------------------------------------|----------------------------------------------------------------------------|
| 作用对象   | 单个 Servlet 的初始化配置                               | 整个 Web 应用 的全局共享信息                                                          |
| 生命周期   | Servlet 创建时存在，Servlet销毁时消失                      | 应用启动时存在，应用停止时销毁                                                            |
| 创建者    | 容器在实例化 Servlet 时创建                              | 容器在启动 Web 应用时就创建                                                           |
| 数据内容   | 只有属于某个 Servlet 的 init-param 参数                  | 整个项目（应用）范围内共享的资源、参数                                                        |
| 通常用来干嘛 | 给单个 Servlet 配一些启动参数                             | 共享全局资源，比如全站路径、全局配置信息、项目级别的数据                                               |

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

两者的通用方法：
- ServletConfig getServletConfig()：获取配置信息
- ServletContext getServletContext()：获取全局信息
- Enumeration<String> getInitParameterNames()：获取所有键名
- String getInitParameter(key)：获取键对应的值

ServletContext 的其他关键 API
- String getRealPath(String path)：把 Web 路径转换成磁盘上的绝对路径
- String getContextPath()：返回当前 Web 项目的根路径
- URL getResource(String path)：根据 Web 路径，返回这个资源的 URL 对象
- InputStream getResourceAsStream(String path)：根据 Web 路径拿到资源的输入流，用于读取文件内容
- void setAttribute(String key, Object value)：在整个应用范围存储一个属性，用于跨模块、跨会话的数据共享
- Object getAttribute(String key)：获取先前存储的全局属性值

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

> HttpServletResponse 还有缓冲的设置，之后学习

### 请求转发和响应重定向

请求转发（Forward）：在服务器内部将当前请求对象和响应对象从一个资源交给另一个资源
- 浏览器的 URL 地址不变
- 转发对客户端是屏蔽的
- 目标资源可以是动态资源如 Servlet，也可以是静态资源 html
- 目标资源不可以访问项目外部资源
- 通过请求转发，可以将请求转发到 WEB-INF 中受保护的资源
- 依旧是原对象返回响应报文，而不是转发对象，最终客户端只接收到一份响应
- RequestDispatcher HttpServletRequest.getRequestDispatcher(String path)：传递目标资源的 Web 路径，返回一个可用的分配器对象
- void RequestDispatcher.forward(ServletRequest request, ServletResponse response)：将对当前请求的请求对象和响应对象转发给另一个资源

### 响应重定向

响应重定向（Redirect）：由服务器指示客户端发起新请求
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
- Web 应用根路径是包含 Context Path 和服务器端口号的路径，若部署 myapp.war 则对应的应用根路径为 http://localhost:8080/myapp
- 前端：通过 \<base href="/myapp/"> 设置根路径，统一相对路径解析基准
- 后端：
  - 对内：包含 contextPath，无需手动添加，如请求转发
  - 对外：不包含 contextPath，需要使用 request.getContextPath() 获取根路径之后拼接，如请求重定向

## MVC 架构模式

MVC = Model + View + Controller，是一种经典的软件设计模式，用于分离应用程序中的不同关注点，实现高内聚低耦合，提高代码的可维护性、可扩展性和可复用性
- Model 模型层：管理数据和业务逻辑，进行与数据库的交互 -> JavaBean, DAO, POJO
- View 视图层：展示数据，负责用户界面和交互 -> JSP, HTML, CSS, JS
- Controller 控制层：接收请求，返回响应，协调 Model 和 View -> Servlet

Model 的几个名词解析
- POJO（Plain Old Java Object）：普通的类，不继承任何特定类，不实现特定接口
- JavaBean：有规范的类，必须有无参构造器，属性必须是私有的，提供全部成员变量的 getter 和 setter
- DAO（Data Access Object）：专门负责跟数据库打交道的类，封装了 CRUD 方法

规范模式
- 数据库的表明通常是下划线模式，而 Java 中的类名通常是驼峰式，它们的名字通常是对应的
- 包名统一全部小谢
- URL 路径用小写+中划线
- 需要给自定义类写上基本信息，比如作业、时间、版本、内容，还需要给自定义方法写上注释

Lombok：自动生成getter、setter、构造器、toString、hashCode、equals、builder等方法，只需要给出成员变量的定义即可