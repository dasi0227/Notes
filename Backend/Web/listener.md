# Listener

## 概述

监听器：用于对容器事件做出监听和响应的组件，通过在特定时机被容器自动调用
- 并不监听项目中所有组件，而是针对于三大域对象
- 按对象划分
  - 应用域：ServletContextListener、ServletContextAttributeListener
  - 会话域：HttpSessionListener、HttpSessionAttributeListener、HttpSessionBindingListener、HttpSessionActivationListener
  - 请求域：ServletRequestListener、ServletRequestAttributeListener
- 按事件划分
  - 创建与销毁：ServletContextListener、HttpSessionListener、ServletRequestListener
  - 属性变化：ServletContextAttributeListener、HttpSessionAttributeListener、ServletRequestAttributeListener
  - 绑定激活：HttpSessionBindingListener 、HttpSessionActivationListener

## 以应用域为例介绍通用接口

ServletContextListener 接口
- contextInitialized：Web 应用启动并且 ServletContext 被创建后，
- contextDestroyed：Web 应用停止或卸载前

ServletContextAttributeListener 接口
- attributeAdded：调用 context.setAttribute(name, value) 后
- attributeRemoved：调用 context.removeAttribute(name) 后
- attributeReplaced：对已存在属性再次调用 context.setAttribute(name, newValue)

## 特殊的两个接口

行为解释
- 绑定：将一个 Java 对象添加到会话的属性之中，执行 session.setAttribute("key", obj)
- 解绑：将一个 Java 对象从会话的属性之中替换/移除，执行 session.removeAttribute("key")
- 钝化：容器对会话及其属性进行序列化，放入磁盘进行持久化存储的过程
- 活化：容器将会话从持久化存储或集群其他节点恢复到当前 JVM 内存，并反序列化回 HttpSession 对象的过程

HttpSessionBindingListener
- valueBound：绑定行为发生（setAttribute）时
- valueUnbound：解绑行为发生（removeAttribute 或 替换属性）时

HttpSessionActivationListener
- sessionWillPassivate：会话及其属性要被序列化之前
- sessionDidActivate：序列化数据被反序列化、会话恢复到内存之后