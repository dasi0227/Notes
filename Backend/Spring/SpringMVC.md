# SpringMVC



* [SpringMVC](#springmvc)
   * [概述](#概述)
      * [Servlet 与 MVC](#servlet-与-mvc)
      * [流程](#流程)
      * [模版引擎](#模版引擎)
   * [配置文件](#配置文件)
      * [web.xml](#webxml)
      * [springMVC.xml](#springmvcxml)
      * [开发流程](#开发流程)
   * [@RequestMapping](#requestmapping)
      * [Ant 风格路径](#ant-风格路径)
      * [使用方法](#使用方法)
   * [获取请求信息](#获取请求信息)
      * [HttpServletRequest](#httpservletrequest)
      * [@RequestParam / @RequestHeader](#requestparam-requestheader)
      * [注入对象](#注入对象)
   * [请求域内共享数据](#请求域内共享数据)
      * [HttpServletRequest](#httpservletrequest)
      * [ModerAndView](#moderandview)
      * [Model](#model)
      * [Map](#map)
      * [HttpSession](#httpsession)
      * [ServletContext](#servletcontext)
   * [视图映射](#视图映射)
      * [ThymeleafView](#thymeleafview)
      * [InternalResourceView](#internalresourceview)
      * [RedirectView](#redirectview)
      * [mvc:view-controller](#mvcview-controller)
      * [](#)
   * [RESTful](#restful)
      * [核心思想](#核心思想)
      * [PUT / DELETE](#put-delete)
   * [数据的读入与写出](#数据的读入与写出)
      * [读入](#读入)
      * [写出](#写出)
   * [文件的下载和上传](#文件的下载和上传)
      * [下载](#下载)
      * [上传](#上传)
   * [拦截器](#拦截器)
      * [概念](#概念)
      * [执行流程](#执行流程)
      * [在 springMVC.xml 注册拦截器](#在-springmvcxml-注册拦截器)
   * [异常处理器](#异常处理器)
      * [概念](#概念)
      * [执行流程](#执行流程)
      * [基于 XML 注册异常处理器](#基于-xml-注册异常处理器)
   * [注解配置](#注解配置)
      * [原理](#原理)
      * [WebInit](#webinit)
      * [WebConfig](#webconfig)



## 概述

### Servlet 与 MVC

Servlet 全称 Server Applet，是指**运行在服务器上的小型 Java 程序**，用来**接收浏览器请求、处理业务逻辑、并返回响应数据**，本质上是 javax.servlet.Servlet 接口

MVC 模式：一种软件架构模式，用来**分离业务逻辑、数据、显示**

- M（Model）：负责封装应用的核心数据和业务逻辑，与数据库交互，提供增删改查接口
- V（View）：负责把 Model 的数据呈现给用户，只关心显示，不包含业务逻辑和数据持久化逻辑
- C（Controller）：负责接收并解析用户输入，调用对应的 Model，处理完之后把 View 返回给用户

SpringMVC：是 Spring Framework 提供的一个基于 MVC 模式的 Web 框架

- 核心组件是 **DispatcherServlet**，本质上是一个继承自 HttpServlet 并实现 Servlet 接口的类，自动部署到了容器之中，任何请求到服务端都会先进入 DispatcherServlet
- 核心工作是**将请求映射到 Controller，并将 Model 渲染为 View 返回**

| 角色     | 传统                            | SpringMVC                                  |
| -------- | ------------------------------- | ------------------------------------------ |
| 请求接收 | HttpServlet                     | DispatcherServlet                          |
| 路由分发 | 手写 if/else 或 switch 判断 URL | HandlerMapping 自动匹配 Controller 方法    |
| 参数获取 | request.getParameter()          | 自动绑定到方法参数                         |
| 响应输出 | response.getWriter()            | 返回视图名 + 数据，自动渲染页面或返回 JSON |

### 流程

1. 客户端发送请求，进入 DispatcherServlet
2. DispatcherServlet 根据 URI 调用 HandlerMapping，找到对应的 Handler 和 Interceptor 链
3. 选择合适的 HandlerAdapter 来调用 Handler
4. 执行前置拦截器 preHandle()
5. SpringMVC 容器会自动准备 Handler 方法的参数
6. 执行 Handler（Controller 方法），处理业务逻辑
7. 返回 ModelAndView 给 DispatcherServlet
8. 执行后置拦截器 postHandle()
9. 选择 ViewResolver，解析视图名并返回 View 对象
10. View 对象负责渲染视图，生成 HTML、JSON 等数据内容
11. 执行完成拦截器 afterCompletion()
12. 将响应返回给客户端

### 模版引擎

模板引擎（Template Engine）是一种**将模板文件和数据结合生成最终文档**的工具

- 模板：带有占位符的静态文件，如 HTML、XML、Markdown、JSON 等
- 数据：从后端传过来的真实数据，可以是字符串、数值和对象
- 渲染：用数据替换模板中的占位符，生成最终的输出文件

| 类型           | 定义                                          | 优点                                       | 例子           |
| -------------- | --------------------------------------------- | ------------------------------------------ | -------------- |
| 服务端模版引擎 | 在后端把数据渲染成 HTML，直接返回给浏览器展示 | 首屏加载快、对 SEO 友好                    | Themeleaf、JSP |
| 客户端模版引擎 | 将数据交给前端，由前端进行渲染展示            | 页面交互灵活，局部刷新不必整个页面重新加载 | Vue、React     |



## 配置文件

### web.xml

web.xml 是 Java Web 应用的**部署描述文件**，位于 `WEB-INF/` 下，负责告诉容器

- 注册 DispatcherServlet，并告诉它去哪找 SpringMVC 的配置文件 springMVC.xml
- 设置 URL 和 Servlet 的映射规则
- 如何配置**过滤器、监听器**等

```java
<web-app>
    <servlet>
        <servlet-name>DispatcherServlet</servlet-name>
        <servlet-class>org.springframework.web.servlet.DispatcherServlet</servlet-class>
        <load-on-startup>1</load-on-startup>
    </servlet>
    <servlet-mapping>
        <servlet-name>DispatcherServlet</servlet-name>
        <url-pattern>/</url-pattern>
    </servlet-mapping>
</web-app>
```

### springMVC.xml

springMVC.xml 是 SpringMVC 框架的**核心配置文件**，位于 `resources/` 下，负责告诉容器

- 扫描哪些包里的 @Controller 类
- 设置 URL 和逻辑视图名称的映射规则
- 如何配置**文件上传器、视图解析器、拦截器、异常处理器**等

```java
<beans 命名空间忽略>
    <!-- 开启扫描组件 -->
    <context:component-scan base-package="com.dasi" />
    <!-- 开启注解驱动 -->
    <mvc:annotation-driven/>
    <!-- 配置视图映射 -->
    <mvc:view-controller path="/" view-name="index" />
    <!-- 强制要求静态资源的请求也走 DispatcherServlet -->
    <mvc:default-servlet-handler />
    <!-- 配置其他组件 -->
    <bean id="..." class="...">
      	...
    </beans>
</beans>
```

### 开发流程

1. 写 pom.xml，引入 jar 包依赖
2. 写 web.xml，注册 DispatcherServlet
3. 写 springMVC.xml，指定扫描包，配置组件
4. 写 index.html，设置模板文件及其逻辑视图名称
5. 写 controller，创建控制器类，执行业务逻辑，配置路径到逻辑视图名的映射



## @RequestMapping

### Ant 风格路径

| **符号** | **含义**                | **示例**                                                     |
| -------- | ----------------------- | ------------------------------------------------------------ |
| ?        | 匹配**任意单个字符**    | /user/?? 匹配 /user/ab、/user/x1                             |
| *        | 匹配 **0 个或多个字符** | /app/*.html 匹配 /app/index.html、/app/.html                 |
| **       | 匹配 **0 个或多个目录** | /a/** 匹配 /a/、/a/x、/a/x/y/z；<br />/**/a 匹配 /a、/x/a、/x/y/z/a |
| {var}    | 匹配并捕获路径段到变量  | /user/{id}/order 匹配 /user/42/order                         |

### 使用方法

位置

- 类：所有方法的路径都会自动以指定 value 为前缀
- 方法：直接指定完整路径

属性

- value：请求路径，满足一个即可，而且必须设置
- method：请求方法，满足一个即可，可以用 @GetMapping、@PostMapping 等代替
- params/headers：请求参数/请求头，必须全部满足，! 表示不允许有，= 表示必须为指定值，!= 表示必须不为指定值

```java
@Controller
public class TestController {
    @RequestMapping("/")
    public String index(){
        return "index";
    }
    @RequestMapping("/param")
    public String param(){
        return "param";
    }
}
```



## 获取请求信息

### HttpServletRequest

```java
@RequestMapping("/testServletAPI")
public String testServletAPI(HttpServletRequest request) {
    String username = request.getParameter("username");
    String password = request.getParameter("password");
    System.out.println("username:"+username+",password:"+password);
    return "success";
}
```

### @RequestParam / @RequestHeader

- value 指定请求参数名
- required 指定是否一定需要，如果为 false 但没提供，默认值是 null；如果是 true 但没提供，会报错
- default 指定缺省时的默认值，无论是否 required

```java
@RequestMapping("/testAnnotation")
public String testAnnotation(
        @RequestParam(value="username", required=true) String username,
        @RequestParam(value="password", defaultValue="123456") String password,
        @RequestHeader(value="Host") String host,
        @CookieValue(value="JSESSIONID") String JSessionID
) {
    System.out.println(
            "username:"+username+",password:"+password+"," +
            "host:"+host+",JSessionID:"+JSessionID
    );
    return "success";
}
```

### 注入对象

- 必须有无参构造器，因为 Spring 会先用 new User() 实例化对象
- 必须有 setter，因为 Spring 通过反射注入值
- 类的属性名必须和请求参数名完全一致

```java
@RequestMapping("/testP0J0")
public String testP0J0(User user) {
    System.out.println(user);
    return "success";
}
```



## 请求域内共享数据

### HttpServletRequest

声明一个 HttpServletRequest 参数，容器会自动加入该对象，之后利用该对象的 setAttribute 方法设置键值对，返回视图名称

```java
@RequestMapping("/testServletAPI")
public String testServletAPI(HttpServletRequest request) {
    request.setAttribute("keyServletAPI", "valueServletAPI");
    return "success";
}
```

### ModerAndView

在方法内创建 ModelAndView 对象，然后利用该对象的 addObject 方法设置键值对，同时利用 setViewName 方法设置视图名称，最后返回该对象

```java
@RequestMapping("/testModelAndView")
public ModelAndView testModelAndView() {
    ModelAndView mav = new ModelAndView();
    mav.addObject("keyModelAndView", "valueModelAndView");
    mav.setViewName("success");
    return mav;
}
```

### Model

声明一个 Model 参数，容器会自动加入该对象，之后利用该对象的 addAttribute 方法设置键值对，返回视图名称

```java
@RequestMapping("/testModel")
public String testModel(Model model) {
    model.addAttribute("keyModel", "valueModel");
    return "success";
}
```

### Map

声明一个 Map 参数，容器会自动加入该对象，之后利用该对象的 put 方法设置键值对，返回视图名称

```java
@RequestMapping("testMap")
public String testMap(Map<String, Object> map) {
    map.put("keyMap", "valueMap");
    return "success";
}
```

### HttpSession

声明一个 HttpSession 参数，容器会自动加入该对象，之后利用该对象的 setAttribute 方法设置键值对，返回视图名称

```java
@RequestMapping("/testHttpSession")
public String testHttpSession(HttpSession session) {
    session.setAttribute("keyHttpSession", "valueHttpSession");
    return "success";
}
```

### ServletContext

声明一个 HttpSession 参数，容器会自动加入该对象，之后利用该对象的 getServletContext 方法获取上下文对象，再调用 setAttribute 设置键值对，返回视图名称

```java
@RequestMapping("/testContext")
public String testContext(HttpSession session) {
    ServletContext application = session.getServletContext();
    application.setAttribute("keyContext", "valueContext");
    return "success";
}
```



## 视图映射

### ThymeleafView

当视图名称没有任何前缀时，会创建一个 ThymeleafView 视图，并由解析器构造一个完整路径，最后把请求转发到这个路径

```java
@RequestMapping("testThymeleafView")
public String testThymeleafView() {
    return "success";
}
```

### InternalResourceView

当视图名称有 `forward:` 前缀的时候，会创建一个 InternalResourceView 视图，然后将前缀去掉，转发到指定路径

```java
@RequestMapping("testForward")
public String testForward() {
    return "forward:/testThymeleafView";
}
```

### RedirectView

当视图名称有 `redirect:` 前缀的时候，会创建一个 RedirectView 视图，然后将前缀去掉，重定向到指定路径

```java
@RequestMapping("testRedirect")
public String testRedirect() {
    return "redirect:/testThymeleafView";
}
```

### mvc:view-controller

可以在 springMVC.xml 设置 `<mvc:view-controller>` 标签，利用 path 属性和 view-name 属性设置映射关系

```java
<!-- 开启注解驱动 -->
<mvc:annotation-driven/>
<!-- 利用标签配置路径视图映射 -->
<mvc:view-controller path="/index" view-name="index" />
```

### 



## RESTful

### 核心思想

- 把每个资源当作一种对象，对应一个 URI
- 用统一的 HTTP 接口实现交互（GET 查询，POST 添加，PUT 修改，DELETE 删除）
- 每一次请求都必须包含完成操作所需的全部信息，服务器不保留客户端上下文
- REST 风格是把发送给服务器的数据作为 URL 地址的一部分，而不是使用键值对

### PUT / DELETE

1. 在 web.xml 中加上 hiddenHttpMethodFilter，它会把带有 _method 参数的 POST 请求转成对应的 HTTP 方法

    ```xml
    <filter>
        <filter-name>HiddenHttpMethodFilter</filter-name>
        <filter-class>org.springframework.web.filter.HiddenHttpMethodFilter</filter-class>
    </filter>
    <filter-mapping>
        <filter-name>HiddenHttpMethodFilter</filter-name>
        <url-pattern>/*</url-pattern>
    </filter-mapping>
    ```
    
2. 在表单里添加隐藏类型，名称为 `_method`，值为 `delete` 或 `put`

    ```java
    <form th:action="@{/employee/{id}(id=${employee.id})}" method="post">
        <input type="hidden" name="_method" value="delete"/>
        <button type="submit">删除</button>
    </form>
    ```

3. 在 @RequestMapping 中设置请求方法

    ```java
    @RequestMapping(value = "/employee/{id}", method = RequestMethod.DELETE)
    public String deleteEmployee(@PathVariable("id") Integer id) {
        employeeDao.delete(id);
        return "redirect:/employee";
    }
    ```



## 数据的读入与写出

### 读入

@RequestBody：声明方法参数从 HTTP 请求体获取数据，底层通过 HttpMessageConverter.read() 将请求体反序列化为指定类型

```java
@RequestMapping("/testRequestBody")
public String testRequestBody(@RequestBody String requestBody) {
    System.out.println("requestBody:" + requestBody);
    return "success";
}
```

RequestEntity：声明方法参数为 RequestEntity 类型，底层除了通过 HttpMessageConverter.read() 反序列化请求体，还可同时获取 headers、method、url 信息

```java
@RequestMapping("/testRequestEntity")
public String testRequestEntity(RequestEntity<String> requestEntity) {
    System.out.println("请求头：" + requestEntity.getHeaders());
    System.out.println("请求体：" + requestEntity.getBody());
    return "success";
}
```

### 写出

HttpServletResponse：调用 Servlet API 直接向响应流写入数据

```java
@RequestMapping("/testResponse")
public void testResponse(HttpServletResponse response) throws IOException {
    response.getWriter().print("hello!");
}
```

@ResponseBody：底层是通过 HttpMessageConverter.write() 将返回值直接序列化

```java
@RequestMapping("/testResponseBody")
@ResponseBody
public String testResponseBody(){
    return "hello!";
}
```



## 文件的下载和上传

### 下载

```java
@RequestMapping("/testDown")
public ResponseEntity<byte[]> testResponseEntity(HttpSession session) throws IOException, FileNotFoundException {
    // 1. 从 HttpSession 拿到 ServletContext
    var servletContext = session.getServletContext();
    // 2. 获取服务器上文件的真实路径
    String realPath = servletContext.getRealPath("/static/img/avatar.jpg");
    // 3. 创建输入流和字节数组
    InputStream is = new FileInputStream(realPath);
    byte[] bytes = new byte[is.available()];
    // 3. 读取文件到字节数组
    is.read(bytes);
    is.close();
    // 4. 创建响应头
    MultiValueMap<String, String> headers = new HttpHeaders();
    // 6. 设置下载方式和文件名称
    headers.add("Content-Disposition", "attachment; filename=avatar.jpg");
    // 7. 返回 ResponseEntity
    return new ResponseEntity<>(bytes, headers, HttpStatus.OK);
}
```

### 上传

```java
@PostMapping("/testUp")
public String testUp(@RequestParam("photo") MultipartFile photo, HttpSession session) throws IOException, FileNotFoundException {
    // 1. 获取上传文件的原始文件名
    String fileName = photo.getOriginalFilename();
    // 2. 得到保存到本地的文件名
    String suffix = fileName.substring(fileName.lastIndexOf("."));
    String uuid = UUID.randomUUID().toString();
    fileName = uuid + suffix;
    // 3. 获取上下文路径，得到或创建文件夹
    ServletContext servletContext = session.getServletContext();
    String photoPath = servletContext.getRealPath("photo");
    File file = new File(photoPath);
    if (!file.exists()) {
        file.mkdirs();
    }
    // 4. 拼出文件的最终完整存储路径
    String filePath = photoPath + File.separator + fileName;
    // 5. 把文件写到本地
    photo.transferTo(new File(filePath));
    return "success";
}
```



## 拦截器

### 概念

**HandlerInterceptor 是位于 DispatcherServlet 与 Controller 之间的组件**，用来对请求进行预处理和后处理

| **方法**          | **调用时机**                  | **作用**                               |
| ----------------- | ----------------------------- | -------------------------------------- |
| preHandle()       | Controller 执行前             | 返回 true 继续执行；false 直接中断请求 |
| postHandle()      | Controller 执行后，视图渲染前 | 可修改 ModelAndView                    |
| afterCompletion() | 视图渲染后                    | 清理资源、记录日志、异常处理           |

```java
public interface HandlerInterceptor {
		boolean preHandle(HttpServletRequest request, HttpServletResponse response, Object handler) throws Exception {
        return true;
    }
    void postHandle(HttpServletRequest request, HttpServletResponse response, Object handler, @Nullable ModelAndView modelAndView) throws Exception {}
		void afterCompletion(HttpServletRequest request, HttpServletResponse response, Object handler, @Nullable Exception ex) throws Exception {}
}
```

### 执行流程

1. 客户端请求
2. DispatcherServlet 接收请求
3. 执行所有拦截器 preHandle()（顺序执行）
4. 调用 HandlerMapping → 找到并执行 Controller
5. 执行所有拦截器 postHandle()（倒序执行）
6. ViewResolver 解析视图并渲染
7. 执行所有拦截器 afterCompletion()（倒序执行）
8. 返回响应给客户端

> 如果某个 preHandle 返回 false，那么**只有已经 preHandle 成功的拦截器才会执行 afterCompletion()，而且所有 postHandle() 都不会执行**

### 在 springMVC.xml 注册拦截器

- 通过 bean 标签声明类位置，拦截所用请求
- 通过 ref 标签指定 bean 的 id，拦截所有请求
- 通过 mvc:interceptor 标签指定拦截路径和拦截器，可以指定路径，也可以排除路径

```xml
<mvc:interceptors>
    <bean class="com.dasi.interceptor.MyInterceptor" />
    <ref bean="myInterceptor" />
    <mvc:interceptor>
        <mvc:mapping path="/*"/>
        <mvc:exclude-mapping path="/"/>
        <bean class="com.dasi.interceptor.MyInterceptor" />
    </mvc:interceptor>
</mvc:interceptors>
```



## 异常处理器

### 概念

**HandlerExceptionResolver 会在 Controller 执行过程中抛出异常时被 SpringMVC 调用**，决定如何处理异常、跳转到哪里、返回什么数据

```java
public interface HandlerExceptionResolver {
    ModelAndView resolveException(
        HttpServletRequest request,
        HttpServletResponse response,
        Object handler,
        Exception ex
    );
}
```

> 如果返回 null，表示当前解析器不处理，而是交给下一个解析器

### 执行流程

1. DispatcherServlet 调用 Controller
2. Controller 抛出异常
3. DispatcherServlet 依次遍历所有 HandlerExceptionResolver
4. 找到能处理的解析器
5. 返回 ModelAndView
6. 渲染视图 / 返回数据

### 基于 XML 注册异常处理器

- exceptionMappings：设置异常类型与逻辑视图名称的映射关系
- exceptionAttribute：设置异常信息在请求域中的键值

```xml
<bean class="org.springframework.web.servlet.handler.SimpleMappingExceptionResolver">
    <property name="exceptionMappings">
        <props>
            <prop key="java.lang.ArithmeticException">error</prop>
        </props>
    </property>
    <property name="exceptionAttribute" value="ex" />
</bean>
```

基于注解注册异常处理器

- @ControllerAdvice：可以在这里建立 Controller 的公共共享逻辑
- @ExceptionHandler：value 是异常类数组
- Exception ex：SpringMVC 会自动把捕获到异常对象传入进来
- Model model：用于设置请求域数据，从而传递异常信息
- 返回逻辑视图名

```java
@ControllerAdvice
public class ExceptionController {
    @ExceptionHandler(value = {ArithmeticException.class, NullPointerException.class})
    public String testException(Exception ex, Model model) {
        model.addAttribute("ex", ex);
        return "error";
    }
}
```



## 注解配置

### 原理

1. 容器启动时，会自动查找实现 ServletContainerInitializer 接口的类
2. SpringMVC 自带实现类，内部会继续查找实现 WebApplicationInitializer 接口的类
3. SpringMVC 提供了基础实现类 AbstractAnnotationConfigDispatcherServletInitializer
4. 只需继承它并重写几个方法，就能完成容器配置，代替 web.xml 和 springMVC.xml

### WebInit

```java
public class WebInit extends AbstractAnnotationConfigDispatcherServletInitializer {

    // 1. 配置 Spring 容器
    @Override
    protected Class<?>[] getRootConfigClasses() {
        return new Class[]{SpringConfig.class};
    }

    // 2. 配置 SpringMVC 容器
    @Override
    protected Class<?>[] getServletConfigClasses() {
        return new Class[]{WebConfig.class};
    }

    // 3. 配置 DispatcherServlet 的 URL 映射
    @Override
    protected String[] getServletMappings() {
        return new String[]{"/"};
    }

    // 4. 配置 DispatcherServlet 过滤器
    @Override
    protected Filter[] getServletFilters() {
        CharacterEncodingFilter encodingFilter = new CharacterEncodingFilter();
        encodingFilter.setEncoding("UTF-8");
        encodingFilter.setForceEncoding(true);
        return new Filter[]{encodingFilter, new HiddenHttpMethodFilter()};
    }
}
```

### WebConfig

```java
// 标识为配置类
@Configuration
// 扫描组件
@ComponentScan("com.dasi")
// 开启注解驱动
@EnableWebMvc
public class WebConfig implements WebMvcConfigurer {
    // 静态资源处理
    @Override
    public void configureDefaultServletHandling(DefaultServletHandlerConfigurer configurer) {
        configurer.enable();
    }

    // 拦截器
    @Override
    public void addInterceptors(InterceptorRegistry registry) {
        registry.addInterceptor(new TestInterceptor()).addPathPatterns("/**");
    }

    // 视图映射
    @Override
    public void addViewControllers(ViewControllerRegistry registry) {
        registry.addViewController("/hello").setViewName("hello");
    }

    // 文件上传与下载
    @Bean
    public MultipartResolver multipartResolver() {
        return new StandardServletMultipartResolver();
    }

    // 异常处理
    @Override
    public void configureHandlerExceptionResolvers(List<HandlerExceptionResolver> resolvers) {
        SimpleMappingExceptionResolver resolver = new SimpleMappingExceptionResolver();
        Properties props = new Properties();
        props.setProperty("java.lang.ArithmeticException", "error");
        resolver.setExceptionMappings(props);
        resolver.setExceptionAttribute("exception");
        resolvers.add(resolver);
    }

    // 模板解析器
    @Bean
    public ITemplateResolver templateResolver() {
        SpringResourceTemplateResolver resolver = new SpringResourceTemplateResolver();
        resolver.setPrefix("/WEB-INF/templates/");
        resolver.setSuffix(".html");
        resolver.setTemplateMode(TemplateMode.HTML);
        resolver.setCharacterEncoding("UTF-8");
        resolver.setCacheable(false);
        return resolver;
    }

    // 模板引擎
    @Bean
    public SpringTemplateEngine templateEngine(ITemplateResolver templateResolver) {
        SpringTemplateEngine engine = new SpringTemplateEngine();
        engine.setTemplateResolver(templateResolver);
        return engine;
    }

    // 视图解析器
    @Bean
    public ViewResolver viewResolver(SpringTemplateEngine templateEngine) {
        ThymeleafViewResolver vr = new ThymeleafViewResolver();
        vr.setCharacterEncoding("UTF-8");
        vr.setTemplateEngine(templateEngine);
        return vr;
    }
}
```