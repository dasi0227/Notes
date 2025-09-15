## 概述

BOM（Brower Object Model）浏览器提供的一组全局对象 API，用于操控浏览器而非页面内容
- 窗口与标签页管理：打开、关闭或重定位窗口/标签页，调整尺寸与位置，控制页面滚动
- URL 与历史导航：读取或修改地址栏，在不刷新页面的情况下增删历史记录，实现前进、后退、跳转等行为
- 环境检测：获取浏览器类型、版本、操作系统及网络状态，查询屏幕分辨率、色深和可用工作区大小
- 定时与异步执行：延迟执行一次性任务或周期性重复执行，用于动画、轮询、节流等场景
- 标准对话框：alert、confirm、prompt 等阻塞式对话框，用于提示、确认或简单输入
- 客户端存储：读写 Cookie，实现轻量级关键信息存储（可配合 Web Storage 使用）
- 跨窗口/跨域通信：在同源或不同源的窗口、iframe 之间安全地传递消息
- 调试与开发辅助：通过 console 对象进行日志输出、性能计时和断言

BOM编程的对象结构
- window：全局根对象，包含所有 BOM 成员与全局变量
- document：目前解析的 html 文档
- location：URL 管理与跳转
- history：浏览历史记录控制
- navigator：浏览器及平台信息
- screen：屏幕分辨率与可用区域信息
- console：开发者工具的控制台
- localStorage：本地数据持久化键值存储
- sessionStorage：本地数据会话级键值存储

## window

- alert(message)：显示一个带“确定”按钮的消息框，阻塞后续脚本执行，用于提示信息
- confirm(message)：显示带“确定/取消”按钮的对话框，返回布尔值 true/false，常用于用户确认操作
- prompt(message)：显示带输入框和“确定/取消”按钮的对话框，返回用户输入的字符串或 null，常用于获取简单文本输入
- open(url)：打开新窗口或标签页，可指定大小、位置和界面元素
- close()：关闭当前窗口（仅当窗口由脚本打开时有效）
- scrollTo(x, y) / scrollBy(dx, dy)：编程方式滚动页面到指定位置或按相对位移滚动
- setInterval(fn, interval)：每隔 interval 毫秒重复执行一次回调函数 f，返回一个定时器 ID，可通过 clearInterval(id) 停止后续执行
- setTimeout(fn, delay)：在延迟 delay 毫秒后仅执行一次回调函数 fn，返回一个定时器 ID，可通过 clearTimeout(id) 取消未到期的执行

## document

- document.getElementById(id)：按 ID 获取元素
- document.querySelector(selector)：按 CSS 选择器获取首个元素
- document.createElement(tagName)：创建新节点
- document.addEventListener(type, handler)：绑定全局事件
- document.removeEventListener(type, handler)：解绑全局事件

## location

- location.href：读取/设置当前 URL
- location.assign(url)：加载新页面（保留历史）
- location.replace(url)：替换当前页面（不留历史）
- location.reload(force)：刷新页面，force=true 可跳过缓存

## history

- history.back()：后退
- history.forward()：前进
- history.go(n)：相对跳转（可正可负） 
- history.pushState(state, title, url)：无刷新添加历史记录

## navigator

- navigator.userAgent：浏览器/平台标识
- navigator.language：首选语言 
- navigator.onLine：网络在线状态 
- navigator.cookieEnabled：Cookie 是否可用

## screen

- screen.width / screen.height：设备屏幕分辨率
- screen.availWidth / screen.availHeight：可用工作区大小
- screen.colorDepth：色深

## console

- console.log(...data)：普通日志
- console.warn(...data) / console.error(...data)：警告/错误输出
- console.time(label) / console.timeEnd(label)：性能计时
- console.table(obj)：以表格形式展示数组或对象

## localStorage/sessionStorage

- localStorage/sessionStorage.setItem(key, value)：存储字符串
- localStorage/sessionStorage.getItem(key)：读取值，若无返回 null
- localStorage/sessionStorage.removeItem(key)：删除对应条目
- localStorage/sessionStorage.clear()：清空所有存储

> sessionStorage 存储内容的生命周期仅限于当前标签页/窗口

