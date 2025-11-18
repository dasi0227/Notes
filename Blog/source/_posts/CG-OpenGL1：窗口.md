---
title: OpenGL：窗口
tags:
  - OpenGL
categories:
  - 笔记
cover: /image/graphic.png
description: 一个OpenGL程序的基本要素，一切的开始！
abbrlink: c4eaa028
date: 2024-09-22 13:40:33
---
<meta name="referrer" content="no-referrer"/>

## 1. 头文件

```cpp
#include <glad/glad.h>
#include <GLFW/glfw3.h>
#include <iostream>
using namespace std;
```

引入glad加载库，glfw窗口库，iostream标准输入输出库

{% note warning flat %}
**一定要在包含GLFW的头文件之前包含了GLAD的头文件**，因为GLAD的头文件包含了正确的OpenGL头文件（例如GL/gl.h），所以需要在其它依赖于OpenGL的头文件之前包含GLAD
{% endnote %}

## 2. 初始化GLFW窗口

```cpp
glfwInit();
glfwWindowHint(GLFW_CONTEXT_VERSION_MAJOR, 3);
glfwWindowHint(GLFW_CONTEXT_VERSION_MINOR, 3);
glfwWindowHint(GLFW_OPENGL_PROFILE, GLFW_OPENGL_CORE_PROFILE);
```

- `glfwInit`函数用来初始化GLFW
- `glfwWindowHint`函数来配置GLFW：第一个参数代表选项的名称（以GLFW_开头的枚举值），第二个参数接受一个整型用来设置这个选项的值（[GLFW's window handling](http://www.glfw.org/docs/latest/window.html#window_hints)）
  - **将主版本号（Major）和次版本号（Minor）都设为3**：因为当前大部分驱动程序和显卡都是基于OpenGL3.3版本
  - **使用核心模式**：不包括旧版本中的向后兼容特性，只向前兼容，简化开发过程，处理更加高效

## 3. 创建窗口对象

```cpp
GLFWwindow* window = glfwCreateWindow(800, 600, "LearnOpenGL", NULL, NULL);
if (window == NULL) {
  cout << "Failed to create GLFW window" << endl;
  return -1;
}
glfwMakeContextCurrent(window);
```

- `glfwCreateWindow`：创建一个窗口对象，参数分别是（宽度，高度，标题，监视器，监视器）
- `glfwMakeContextCurrent`：用于设置当前的OpenGL上下文，使后续的OpenGL操作作用于指定的窗口

## 4. 初始化GLAD

```cpp
if (!gladLoadGLLoader((GLADloadproc)glfwGetProcAddress)) {
  cout << "Failed to initialize GLAD" << endl;
  return -1;
}
```

- `GLADloadproc`：函数指针类型，这里将glfwGetProcAddress转换为GLADloadproc类型
- `glfwGetProcAddress`：用于获取OpenGL函数指针
- `gladLoadGLLoader`：用于根据OpenGL函数指针来加载OpenGL函数

## 5. 初始化视口和回调视口

**视口（viewport）**：是窗口中渲染图形的实际尺寸大小，理论上不能大于窗口但可以小于等于窗口
**回调（callback）**：用户可以改变窗口大小，而视口大小也应该跟着窗口大小的改变而改变

```cpp
// 前两个参数控制窗口左下角的位置。第三个和第四个参数控制渲染窗口的宽度和高度
void framebuffer_size_callback(GLFWwindow* window, int width, int height) {
  glViewport(0, 0, width, height);
}
// 传递窗口对象和视口回调函数，用于实现每次窗口大小被调整的时候都被自动调用（第一次创建窗口的时候也会被调用，相当于初始化了）
glfwSetFramebufferSizeCallback(window, framebuffer_size_callback);
```

## 6. 渲染循环

```cpp
while(!glfwWindowShouldClose(window)) {
  glfwSwapBuffers(window);
  glfwPollEvents();    
}
```

**渲染循环（Render Loop）**：在GLFW退出前保持运行，从而能让开发者持续观察渲染效果

- `glfwWindowShouldClose`：检查窗口关闭请求（如用户点击窗口关闭按钮）
- `glfwSwapBuffers`：交换前后缓冲，将渲染的图像显示到窗口上，在每次渲染循环的最后进行，以确保屏幕上显示的内容是最新的
- `glfwPollEvents`：检查有没有触发什么事件（如键盘输入，鼠标移动，窗口调整）

{% note info flat %}
**双缓冲（Double Buffer）**：通过交换前后缓冲，可以**立即**将图像呈现出来，从而消除**逐渐渲染的图像闪烁**问题
- 前缓冲：当前显示在屏幕窗口上的图像
- 后缓冲：正在被绘制的图像
{% endnote %}

## 7. 销毁窗口

```cpp
glfwDestroyWindow(window);
glfwTerminate();
return 0;
```

- `glfwDestroyWindow`：销毁指定的窗口，释放与窗口相关的所有资源
- `glfwTerminate`：清理GLFW库，终止使用GLFW，通常在程序结束或程序出错时调用

## 8. 键盘输入

```cpp
// 以返回键(Esc)为例
void processInput(GLFWwindow *window) {
  if(glfwGetKey(window, GLFW_KEY_ESCAPE) == GLFW_PRESS)
    glfwSetWindowShouldClose(window, true);
}
```

- `glfwGetKey`：用于检查特定键的当前状态，`GLFW_PRESS`表示当前被按下，`GLFW_REPEAT`表示当前被持续按住，`GLFW_RELEASE`表示当前未被按下
- `glfwSetWindowShouldClose`：明确告诉GLFW窗口应当关闭，常用于响应用户输入

## 9. 清空颜色

```cpp
// 以清空颜色为例
glClearColor(0.2f, 0.3f, 0.3f, 1.0f);
glClear(GL_COLOR_BUFFER_BIT);
```

- `glClearColor`：设置清除后的颜色(R,G,B,A)
- `glClear`：清除指定的缓冲区，`GL_COLOR_BUFFER_BIT`表示颜色缓冲区

## 10. 完整代码

```cpp
#include <glad/glad.h>
#include <GLFW/glfw3.h>
#include <iostream>
using namespace std;

// 回调函数
void framebuffer_size_callback(GLFWwindow* window, int width, int height) {
  glViewport(0, 0, width, height);
}

// 键盘输入函数
void processInput(GLFWwindow *window) {
  if(glfwGetKey(window, GLFW_KEY_ESCAPE) == GLFW_PRESS)
    glfwSetWindowShouldClose(window, true);
}

int main() {
  // 初始化GLFW
  glfwInit();
  glfwWindowHint(GLFW_CONTEXT_VERSION_MAJOR, 3); // 设置主版本为3
  glfwWindowHint(GLFW_CONTEXT_VERSION_MINOR, 3); // 设置次版本为3
  glfwWindowHint(GLFW_OPENGL_PROFILE, GLFW_OPENGL_CORE_PROFILE); // 设置使用核心模式

  // 创建窗口
  GLFWwindow* window = glfwCreateWindow(800, 600, "Simple Triangle", nullptr, nullptr);
  if (!window) {
    cerr << "Failed to create GLFW window" << endl;
    return -1;
  }
  glfwMakeContextCurrent(window); // 设置为上下文

  // 初始化GLAD
  if (!gladLoadGLLoader((GLADloadproc)glfwGetProcAddress)){
    cout << "Failed to initialize GLAD" << endl;
    return -1;
  }

  // 初始化视口
  glViewport(0, 0, 800, 600);
  glfwSetFramebufferSizeCallback(window, framebuffer_size_callback);

  // 渲染循环
  while (!glfwWindowShouldClose(window)) {
    // 输入
    processInput(window);
    // 渲染
    glClearColor(0.0f, 0.0f, 0.0f, 0.0f);
    glClear(GL_COLOR_BUFFER_BIT);
    // 呈现
    glfwSwapBuffers(window);
    glfwPollEvents();
  }

  // 销毁窗口
  glfwDestroyWindow(window);
  glfwTerminate();
  return 0;
}
```

