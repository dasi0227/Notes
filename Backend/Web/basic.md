## Java Web

几个 J
- JRE（Java Runtime Environment）：Java 运行环境，包含 JVM 和 JCL 以及其他配套资源
- JVM（Java Virtual Machine）：Java 虚拟机，负责把 Java 字节码（.class 文件）翻译成操作系统能执行的指令
- JCL（Java Class Libraries）：Java 类库，具备一大堆预定义好的 Java 类，提供开发中最基础的功能
- JDK（Java Development Kit）：Java 开发工具包，是写、编译、调试 Java 程序的一整套工具合集
- JDB（Java Debugger）：Java 调试工具，用来在命令行下调试 Java 程序，比如设置断点、单步执行、查看变量值
- JAR（Java Archive）：Java 归档包，把多个 .class 文件和资源文件打包成一个文件，方便部署、传输
- JSP（JavaServer Pages）：Java 服务器页面技术，让开发者能在HTML网页中直接嵌入Java代码或表达式，从而用来动态生成网页内容

Web 容器：运行在服务端，负责托管和管理 JavaWeb 应用的基础服务组件，提供必要的运行环境和基础服务
- 管理 Servlet 生命周期：实例化、初始化、销毁
- 请求接收与分发：监听指定端口（8080），接收来自浏览器的 HTTP 请求，并根据 URL 映射规则将请求分发到对应的 Servlet
- 业务处理：Servlet 调用业务层（比如 Service 或者 Dao）处理具体业务逻辑
- 响应生成与返回：将处理结果封装成响应数据（如 HTML、JSON、XML）发回给浏览器
- 扩展服务：如安全认证、会话管理、过滤器、监听器等

Servlet：一种基于Java的服务器端程序，规范上是实现了 Servlet 接口的类，通常继承 HttpServlet，用来接收请求、处理业务逻辑、生成响应的组件

关系：
- 通常由 Servlet 负责处理复杂的业务逻辑，将处理结果传递给 JSP 页面，由 JSP 负责将数据以合适的形式渲染成 HTML 页面返回给客户端
- JSP 会在服务器端被自动编译成 Servlet 类，因此 JSP 本质上就是一种更方便编写页面输出的特殊专属 Servlet

MVC 架构
- M（Model）：模型，处理业务逻辑和数据，比如和数据库打交道、做计算、保存状态啥的
- V（View）：视图，负责把数据美化好，展示给用户
- C（Controller）：控制器，负责接收和调度用户请求，协调 Model 和 View 的工作

## Tomcat 目录结构

根目录结构（Tomcat/)
- bin/：基本脚本，如启动和关闭 Tomcat
- conf/：配置文件，其中 server.xml 控制 Tomcat 怎么跑，web.xml 控制 Web 应用怎么跑，根据自己的业务需求调整
- lib/：库文件，Tomcat 自己运行时需要的 jar 包，一般不需要动这里
- logs/：日志，Tomcat 运行的运行日志，Tomcat 挂了来这里找原因
- webapps/：应用文件，正式部署 Web 应用的地方
- work/ 和 temp/：存放 Tomcat 运行时生成的临时文件，重启会清空

应用目录结构（Tomcat/webapps/myapp/）
```text
myapp/
├── index.html / index.jsp    （入口页面）
├── login.html / login.jsp    （其他页面）
├── static/                   （统一放静态资源）
│    ├── css/				  （样式文件）
│    │    └── style.css
│    ├── js/                  （脚本文件）
│    │    └── main.js
│    └── images/              （图片文件）
│         └── logo.png
└── WEB-INF/                  （隐藏区域，浏览器不可访问）
     ├── web.xml              （部署描述符，配置 Servlet、Filter 等）
     ├── classes/             （编译后的 .class 文件）
     │    └── com/
     │         └── dasi/
     │              └── appname/
     │                   └── MyServlet.class
     └── lib/                 （项目专属的jar包）
          └── mysql-connector-java-8.0.xx.jar
```

- index.html：入口页面，浏览器访问网址后第一个看到的页面
- static/：渲染页面时要用的 css、js 和图片等静态文件
- WEB-INF/：浏览器访问不到的地方，但是决定了浏览器的行为
- WEB-INF/web.xml：项目的核心配置文件，配置 Servlet、Filter、Listener，定义 URL 映射、初始化参数
- WEB-INF/classes/：存放业务逻辑程序即 Servlet 程序的字节码，对应后端具体要实现的服务
- WEB-INF/lib/：后端服务实现时需要用到的工具包

> web.xml 调设置，classes 打游戏，lib 加外挂

## 部署项目方式

方式1：把整个 myapp/ 文件夹复制到 Tomcat 的 webapps/ 目录下 ➡️ 本地开发，快速测试修改

方式2：配置 conf/server.xml，在 \<Host> 标签内部加上 `<Context docBase="/absolute/path/to/myapp" path="/myapp"/>`，其中 docBase 是你项目的真实位置，path 是访问的URL路径 ➡️ 每次改完都需要打包，通常交付和上线才使用

方式3：利用 IDE 打包成标准的 .war 包，然后放到 Tomcat 的 webapps/ 目录下 ➡️ 灵活部署，但是源路径改变一定要修改 server.xml

## 软件的生命周期

周期节点
- 开发（develop）：人敲键盘写代码的过程
- 构建（build）：把源代码编译、打包成可执行应用的过程，比如将 .java 编译成 .class，并和网页资源、依赖库一起打包进 .war 文件
- 部署（deploy）：把构建好的应用包放到服务器上运行，让其他用户通过网络访问到
- 测试（test）：检查应用是否按照预期工作，找出BUG，验证功能正确性的过程
- 运维（operate）：应用上线后的运行维护工作，包括服务器管理、监控、日志分析、备份恢复、故障排查等

资源类型
- 静态资源：无需在程序运行时动态生成的资源，在程序运行之前就已经写好的资源，如 css、js、img、音视频文件
- 动态资源：在程序运行时由代码动态生成的资源，在程序运行之前无法确定