---
title: OpenGL：着色器
tags:
  - OpenGL
categories:
  - 笔记
cover: /image/graphic.png
description: GLSL的具体格式，如何封装一个着色器类并使用
abbrlink: 6c76ab46
date: 2024-09-24 21:12:00
---
<meta name="referrer" content="no-referrer"/>

## 1. GLSL

**GLSL（OpenGL Shading Language）**：是一种专门**为GPU设计**的编程语言，用于编写**顶点着色器**和**片段着色器**

```cpp
// 版本声明 
#version version_number
// 变量声明
in type in_variable_name;
out type out_variable_name;
uniform type uniform_name;
// 主函数
void main() {
  // 处理输入
  // 图形操作
  // 处理输出
}
```

## 2. 向量

**向量（vector）**：是一个包含有**n个分量**的容器，分量的类型可以是**基础数据类型int、float、double、uint和bool**

|类型|含义|
|-|-|
|vecn|包含n个float分量的向量|
|bvecn|包含n个bool分量的向量|
|ivecn|包含n个int分量的向量|
|uvecn|包含n个unsigned int分量的向量|
|dvecn|包含n个double分量的向量|

{% label "如何获取分量？" orange %}
- 通用/位置：使用`.x`、`.y`、`.z`、`.w`获取它们的(x,y,z,w)分量
- 颜色：使用`.r`、`.g`、`.b`、`.a`获取它们的(r,g,b,a)分量
- 纹理：使用`.s`、`.t`获取它们的(s,t)分量

**重组（Swizzling）**：将向量的分量重新组合成一个新的向量
```cpp
// 声明一个2分量向量
vec2 v1;
// 将v1的x,y分量重组赋值
vec4 v2 = v1.xyxx;
// 将v2的z,y,w分量重组赋值
vec3 v3 = v2.zyw;
// 将v1和v3的各个分量值先重组再相加
vec4 v4 = v1.xxxx + v3.yxzy;
// 还可以把向量作为参数传给向量构造函数
vec2 v1 = vec2(0.5, 0.7);
vec2 v2 = vec2(v1);
vec4 v3 = vec4(v1, 0.0, 0.0);
```

## 3. 输入输出

`layout (location = <索引>)`：顶点着色器不是获取顶点数组，而是直接获取**顶点数据**，因此需要指定**索引**来告诉OpenGL从哪个位置获取数据赋值给输入变量

```cpp
// 输入
layout (location = <索引>) in type in_variable_name;
// 输出
out type out_variable_name;
```

着色器通信：**在发送方着色器声明一个输出变量，在接收方着色器声明一个输入变量**，且这两个变量的**类型和名称必须一致**，否则OpenGL无法链接这两个变量

```cpp
// 考虑让顶点着色器为片段着色器提供颜色
// 顶点着色器
#version 330 core
layout (location = 0) in vec3 aPos;
out vec4 vertexColor; // 输出变量
void main() {
  gl_Position = vec4(aPos, 1.0);
  vertexColor = vec4(0.5, 0.0, 0.0, 1.0);
}
// 片段着色器
#version 330 core
in vec4 vertexColor; // 输入变量
out vec4 FragColor;
void main() {
  FragColor = vertexColor;
}
```

## 4. Uniform

Uniform是一种**从CPU向GPU发送数据**的方式，因为**GPU不允许CPU对其进行写操作**，所以我们需要一个**全局变量Uniform**，使得CPU可以写入值，而GPU可以读取值

```cpp
// 在着色器程序中声明一个uniform变量
uniform type uniform_name;

// 在主程序中设置uniform的值
// 1. 先找到unifrom变量的位置
int vertexColorLocation = glGetUniformLocation(shaderProgram, "uniform_name");
// 2. 然后激活着色器程序
glUseProgram(shaderProgram);
// 3. 设置这个uniform变量的值
glUniform4f(vertexColorLocation, color_value);
```

{% note warning flat %}
`glUniform`有一个特定的后缀，可以标识设定的类型，如f需要一个float类型，i需要一个int类型，3f需要一个3个float值，4f需要4个float值
{% endnote %}

## 5. 着色器处理多个属性

只需要通过`layout (location = <索引>)`来指定索引来获取不同索引的数据即可

**假设我们有如下数据**
```cpp
float vertices[] = {
  // 位置              // 颜色
  0.5f, -0.5f, 0.0f,  1.0f, 0.0f, 0.0f,   // 右下
  -0.5f, -0.5f, 0.0f,  0.0f, 1.0f, 0.0f,  // 左下
  0.0f,  0.5f, 0.0f,  0.0f, 0.0f, 1.0f    // 顶部
};
```

![](https://dasi-blog.oss-cn-guangzhou.aliyuncs.com/ComputerGraphic/OpenGL202409291951530.png)

**在顶点着色器中获取位置和颜色**
```cpp
#version 330 core
layout (location = 0) in vec3 aPos;
layout (location = 1) in vec3 aColor;
out vec3 ourColor;  // 将获取的颜色数据输出给片段着色器
void main() {
  gl_Position = vec4(aPos, 1.0);
  ourColor = aColor;
}
```

**在片段着色器中获取颜色**
```cpp
#version 330 core
in vec3 ourColor;
out vec4 FragColor;
void main() {
  FragColor = vec4(ourColor, 1.0);
}
```

**需要更新VAO**
```cpp
// 位置
glVertexAttribPointer(0, 3, GL_FLOAT, GL_FALSE, 6 * sizeof(float), (void*)0);
glEnableVertexAttribArray(0);
// 颜色
glVertexAttribPointer(1, 3, GL_FLOAT, GL_FALSE, 6 * sizeof(float), (void*)(3 * sizeof(float)));
glEnableVertexAttribArray(1);
```

![](https://dasi-blog.oss-cn-guangzhou.aliyuncs.com/ComputerGraphic/OpenGL202409291951529.png)

{% note info flat %}
为什么三角形不是单纯的红蓝绿？
**片段插值（Fragment Interpolation）**：片段着色器隐式地将三角形内每个片段的颜色**通过三个顶点的颜色插值得到**，比如，如果一条线的上端是绿色而下端是蓝色，位于线段靠上三等分点的位置的片段颜色将是66.7%蓝色和33.3%绿色的**线性组合**，最终呈现出**颜色渐变**的效果
{% endnote %}

## 6. 着色器类

### 6.1 结构

{% label "为什么需要一个着色器类？" orange %}
- 如果每一个着色器都需要在`main文件`中编程，那么代码将会复杂且冗余，因此我们希望可以编写一个**类文件**来**封装**这些**形式相同，类型和数据不同**的函数操作，使得`main函数`可以利用类来使用着色器
- 着色器代码手动填写到字符串中，不利于编写和维护，因此我们希望可以**从硬盘中读取着色器代码**

```cpp
// 避免多个文件重复包含和编译类文件，防止链接冲突
#ifndef SHADER_H
#define SHADER_H
// 不需要创建窗口，因此不需要GLFW头文件，但是需要使用OpenGL函数，因此需要GLAD头文件
#include <glad/glad.h>; 
// 需要用到的C++标准库头文件
#include <string>
#include <fstream>
#include <sstream>
#include <iostream>
using namespace std;
class Shader {
  public:
    // 程序ID
    unsigned int ID;
    // 构造函数：读取并构建着色器
    Shader(const char* vertexPath, const char* fragmentPath);
    // 使用/激活程序
    void use();
    // set函数用于查询uniform变量的位置并赋值
    void setBool(const string &name, bool value) const;  
    void setInt(const string &name, int value) const;   
    void setFloat(const string &name, float value) const;
};

#endif
```

### 6.2 构造函数

```cpp
Shader(const char* vertexPath, const char* fragmentPath) {
  // 1. 声明变量
  string vertexCode; // 顶点着色器代码字符串
  string fragmentCode; // 片段着色器代码字符串
  ifstream vShaderFile; // 顶点着色器文件
  ifstream fShaderFile; // 片段着色器文件
  // 2. 读取文件
  vShaderFile.open(vertexPath);
  fShaderFile.open(fragmentPath);
  stringstream vShaderStream, fShaderStream;
  vShaderStream << vShaderFile.rdbuf();
  fShaderStream << fShaderFile.rdbuf();
  vShaderFile.close();
  fShaderFile.close();
  // 3. 读取代码
  vertexCode = vShaderStream.str();
  fragmentCode = fShaderStream.str();
  const char* vShaderCode = vertexCode.c_str();
  const char* fShaderCode = fragmentCode.c_str();
  // 4. 编译着色器
  unsigned int vertex, fragment;
  vertex = glCreateShader(GL_VERTEX_SHADER);
  fragment = glCreateShader(GL_FRAGMENT_SHADER);
  glShaderSource(vertex, 1, &vShaderCode, NULL);
  glShaderSource(fragment, 1, &fShaderCode, NULL);
  glCompileShader(vertex);
  glCompileShader(fragment);
  // 5. 链接着色器
  ID = glCreateProgram();
  glAttachShader(ID, vertex);
  glAttachShader(ID, fragment);
  glLinkProgram(ID);
  // 7. 删除着色器
  glDeleteShader(vertex);
  glDeleteShader(fragment);
}
```

### 6.3 成员函数

```cpp
// use函数：使用/激活程序
void use() { 
  glUseProgram(ID);
}
// 一系列set函数：查询uniform变量的位置并赋值
void setBool(const string &name, bool value) const {
  glUniform1i(glGetUniformLocation(ID, name.c_str()), (int)value);
}
void setInt(const string &name, int value) const {
  glUniform1i(glGetUniformLocation(ID, name.c_str()), value);
}
void setFloat(const string &name, float value) const {
  glUniform1f(glGetUniformLocation(ID, name.c_str()), value);
}
```

### 6.4 使用着色器类

在main函数中使用着色器类
```cpp
// 实例化着色器类
Shader ourShader("path/to/shader.vs", "path/to/shader.fs");
while(...){
  // 激活着色器
  ourShader.use();
  // 设置uniform变量
  ourShader.setFloat("someUniform", 1.0f);
  // 渲染
  [...];
}
```
