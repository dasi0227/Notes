# AJAX



## 概述

发送请求的行为
- 浏览器输入 URL 回车，默认使用 GET 方法
- 静态资源标签自动加载，如 script、link、img
- 静态资源标签手动加载，如 a、form
- JavaScript 动态请求资源，通过 DOM 响应

AJAX（Asynchronous JavaScript and XML）是一种在不刷新整个页面的前提下，使用 JavaScript 在后台与服务器进行异步数据交互的技术集合
- A（Asynchronous）：异步执行，不阻塞用户操作
- J（JavaScript）：发请求、拿响应、更新 DOM 都在前端通过脚本完成
- X（XML）：除了 XML，也可以适用于 JSON 和 HTML

## XMLHttpRequest

XMLHttpRequest 是浏览器内置的 JS 对象，用于在不断刷新页面的前提下，与服务端进行异步 HTTP 通信

关键属性
- readyState：当前请求所处的阶段
  - 0 / UNSENT：创建了 XMLHttpRequest 实例，但是还没有调用 open() 方法
  - 1 / OPENED：已调用过 open()，但尚未调用 send() 方法
  - 2 / HEADERS_RECEIVED：已调用 send()，并且响应头已可获得，但响应体尚未开始接收
  - 3 / LOADING：响应体部分数据正在接收
  - 4 / DONE：响应已完全接收或请求已失败/中止
- status：HTTP 响应状态码
  - 200：请求已成功获得响应
  - 302：临时重定向
  - 404：请求的资源不存在
  - 500：服务端发生了错误
- responseText：响应的字符串文本
- responseXML：解析后的 DOM 文档
- responseType：预期的响应类型

关键方法
- 构造发送
  - open(method, url)：初始化请求
  - setRequestHeader(header, value)：设置请求头信息
  - send(body)：设置请求体，并发送请求
  - abort()：立即取消请求
- 事件回调
  - onreadystatechange()：任意 readyState 变化时触发
  - onerror()：网络错误或跨域失败时触发
  - onload()：请求成功完成（readyState===4 且 status 在 200–299）时触发
  - ontimeout()：达到 timeout 时间后触发
  - onabort：调用 abort() 后触发

