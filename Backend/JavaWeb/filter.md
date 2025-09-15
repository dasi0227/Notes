# 过滤器

## 概述

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

## 配置过滤起

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

## doFilter

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


