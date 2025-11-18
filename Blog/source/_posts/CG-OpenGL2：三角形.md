---
title: OpenGL：三角形
tags:
  - OpenGL
categories:
  - 笔记
cover: /image/graphic.png
description: 介绍图形渲染管线，详解VBO、VAO和着色器编程，最后绘制一个简单的三角形
abbrlink: 7fdffb64
date: 2024-09-22 15:06:13
---
<meta name="referrer" content="no-referrer"/>

## 1. 图形渲染管线

**管线/流水线（Pipeline）**：将一堆原始图形数据途经一个输送管道，期间经过各种变化处理最终出现在屏幕的过程，主要有以下两步
1. 将顶点的3D坐标转换为2D坐标
2. 将顶点的2D坐标转变为屏幕的像素

{% note warning flat %}
坐标和像素是不同的，坐标是空间中一个精确的点，而像素只是分辨率中的一个方块，可以认为**像素是坐标的近似**！
{% endnote %}

**着色器（Shader）**：用于图形渲染的GPU程序，负责管线内的各个操作
- **顶点着色器（vertex）**：处理单个顶点的输入，负责坐标变换、光照计算
- **几何着色器（geometry）**：处理一组顶点的输入，负责增加或改变顶点
- **图元装配（Primitive Assembly）**：将顶点组合成图元
- **光栅化（Rasterization）**：把图元映射为最终屏幕上相应的像素
- **片段着色器（fragment）**：处理每个片段的颜色和纹理，计算最终的像素值
- **测试（Test）**：包括深度测试和模板测试，确定哪些片段可见，哪些被丢弃
- **混合（Blend）**：将多个片段的颜色结合，处理透明度和颜色混合效果

![](https://dasi-blog.oss-cn-guangzhou.aliyuncs.com/ComputerGraphic/OpenGL202409291952577.png)

{% note info flat %}
图元（primitive）：有三种基本类型，**点（GL_POINTS）**、**线（GL_LINE_STRIP）**、**三角形（GL_TRIANGLES）**
片段（fragment）：是OpenGL渲染一个像素所需的所有数据，是**像素的前身**
{% endnote %}

## 2. VBO

### 2.1 什么是VBO？

**顶点缓冲对象（Vertex Buffer Object,VBO）**：是存储顶点数据的图形对象，是**CPU和GPU之间传递数据**的桥梁

{% label "为什么要使用VBO？" orange %}
关键在于理解B即**Buffer**的含义，缓冲代表VBO可以暂时存储多个顶点的数据，之后可以**一次性发送多个顶点数据到显卡**，而不是每个顶点都发送一次，这样使得顶点着色器能**立即同时访问到全部顶点**，从而**充分发挥GPU并行计算**的功能，极大程度**加快渲染效率**

{% label "常见的顶点数据" orange %}
- **位置（Position）**：顶点在三维空间中的坐标(x,y,z)
- **颜色（color）**：顶点的颜色(r,g,b,a)
- **纹理（texture）**：用于映射纹理到顶点的坐标(s,t)

![](https://dasi-blog.oss-cn-guangzhou.aliyuncs.com/ComputerGraphic/OpenGL202409291952576.png)

{% note warning flat %}
**标准化坐标设备（Normalized Device Coordinates,NDC）**：OpenGL中的顶点坐标需要经过NDC处理转换为值在[-1.0,1.0]范围内的标准化坐标，才能最终显示在屏幕上！
{% endnote %}

```cpp
float vertices[] = {
  // 位置             // 颜色             // 纹理
  0.5f, 0.5f, 0.0f,   1.0f, 0.0f, 0.0f,  1.0f, 1.0f, // 右上
  0.5f, -0.5f, 0.0f,  0.0f, 1.0f, 0.0f,  1.0f, 0.0f, // 右下
  -0.5f, -0.5f, 0.0f, 0.0f, 0.0f, 1.0f,  0.0f, 0.0f, // 左下
  -0.5f, 0.5f, 0.0f,  1.0f, 1.0f, 0.0f,  0.0f, 1.0f  // 左上
};
```

### 2.2 如何创建VBO？

首先，**生成具有唯一ID的VBO对象**
```cpp
unsigned int VBO;
glGenBuffers(1, &VBO);
```
然后，**将VBO绑定到指定缓冲类型**，`GL_ARRAY_BUFFER`表示顶点数组（这一步相当于**C中声明一个变量的数据类型**）
```cpp
glBindBuffer(GL_ARRAY_BUFFER, VBO)
```
最后，**将数据添加到VBO中**
- 第一个参数是目标缓冲的类型
- 第二个参数指定传输数据的大小（以字节为单位）
- 第三个参数是发送的实际数据
- 第四个参数指定了显卡如何管理给定的数据
  - `GL_STATIC_DRAW`数据不会或几乎不会改变（静态图像通常使用这个）
  - `GL_DYNAMIC_DRAW`数据会被改变很多
  - `GL_STREAM_DRAW`数据每次绘制时都会改变
```cpp
glBufferData(GL_ARRAY_BUFFER, sizeof(vertices), vertices, GL_STATIC_DRAW)
```

## 3. VAO

### 3.1 什么是VAO？

{% note warning flat %}
VBO实际上就是存储了一大堆数据，但是OpenGL中的GPU事先根本不知道这些数据的**组织结构和含义**是什么，GPU视角下它可能只是看到了**一堆毫无意义的数字**！这种时候我们就需要VAO
{% endnote %}

**顶点数组对象（Vertex Array Object,VAO）**：保存了与顶点数据对应属性的对象，用于**给GPU解释绑定的VBO的数据含义**

![](https://dasi-blog.oss-cn-guangzhou.aliyuncs.com/ComputerGraphic/OpenGL202409291952571.png)

{% label "为什么VAO是必要的？" orange %}
实际上，我们可以不用VAO，只是用一些命令告知GPU数据组织构造和含义即可。但这样做的话，**每一个构造相同的VBO都需要重复上述命令**，如果一个图形有几百个构造相同的VBO，那么就可能需要编写和执行几千条甚至几万条一模一样的代码，这显然是**不合适且不合理**的！因此，我们只需要**根据某一构造的VBO写一个VAO**，就可以只用一个VAO来处理全部相同构造的VBO

### 3.2 如何创建VAO？

首先，**生成具有唯一ID的VAO对象**
```cpp
unsigned int VAO;
glGenVertexArrays(1, &VAO);
```
然后，**绑定VAO到指定缓冲类型**
```cpp
glBindVertexArray(VAO);
```
接着，**配置VAO即定义如何解析顶点数据**
- index：顶点数据的索引
- size：顶点数据的分量个数
- type：顶点数据的类型
- 参数4：顶点数据是否需要标准化
- 参数5：顶点数据的步长，即单个顶点的数据长度
- 参数6：顶点数据的在缓冲起始位置的偏移量
```cpp
glVertexAttribPointer(index, size, type, normalized, stride, (void*)pointer);
```
最后，**启用顶点属性**
```cpp
glEnableVertexAttribArray(index);
```

### 3.3 VAO实例分析

{% note info flat %}
假设一个顶点有两个属性，先是位置，然后是颜色
{% endnote %}

```cpp
glVertexAttribPointer(0, 3, GL_FLOAT, GL_FALSE, (3 + 4) * sizeof(float), offset);
glEnableVertexAttribArray(0);
```
- 位置是第一个属性，所以index是0
- 位置有(x,y,z)共3个值构成，所以size是3
- 坐标值是32位的浮点值，所以type是GL_FLOAT
- 由于传输的数据已经标准化了，所以normalized是GL_FALSE
- 步长即是单个顶点的字节数，位置有3个浮点值，颜色有4个浮点值，所以stride是(3 + 4) * sizeof(float)
- 位置是第一个属性，所以偏移量是(void*)pointer

![](https://dasi-blog.oss-cn-guangzhou.aliyuncs.com/ComputerGraphic/OpenGL202409291952575.png)

```cpp
glVertexAttribPointer(1, 4, GL_FLOAT, GL_FALSE, (3 + 4) * sizeof(float), (void*)(3 * sizeof(float)));
glEnableVertexAttribArray(1);
```
- 颜色是第二个属性，所以index是1
- 位置有(r,g,b,a)共4个值构成，所以size是4
- 颜色值是32位的浮点值，所以type是GL_FLOAT
- 由于颜色数据无需标准化了，所以normalized是GL_FALSE
- 步长即是单个顶点的字节数，位置有3个浮点值，颜色有4个浮点值，所以stride是(3 + 4) * sizeof(float)
- 位置是第二个属性，前一个是位置属性，所以偏移量是(void*)(3 * sizeof(float))

### 3.4 VAO如何实现一对多？

![](https://dasi-blog.oss-cn-guangzhou.aliyuncs.com/ComputerGraphic/OpenGL202409291952572.png)

```cpp
// 绑定 VAO
glBindVertexArray(VAO);
// 绑定第一个 VBO
glBindBuffer(GL_ARRAY_BUFFER, VBO[0]);
glBindBuffer(GL_ARRAY_BUFFER, 0);
// 绑定第二个 VBO
glBindBuffer(GL_ARRAY_BUFFER, VBO[1]);
glBindBuffer(GL_ARRAY_BUFFER, 0); // 解绑颜色 VBO
// 解绑 VAO
glBindVertexArray(0);
```

## 4. 着色器编程

{% note info flat %}
着色器本质上是**GPU的可执行渲染程序**，主要进行三步：编程-编译-链接
- **编程（programme）**：使用着色器语言（GLSL）编写代码
- **编译（Compiler）**：使用OpenGL API将GLSL代码提供给着色器对象并编译
- **链接（Link）**：将已编译的着色器附加到一个程序对象上，并进行链接
{% endnote %}

### 4.1 着色器编程

以下自定义的顶点着色器实现了：**将每个输入顶点的位置从模型空间转换到裁剪空间，为后续的图形渲染做好准备**

```cpp
// 使用GLSL 3.3版本的核心模式
#version 330 core
// 从渲染管线的location处接收顶点数据，存储到名为aPos的三维向量vec3中（这里是位置数据）
layout(location = 0) in vec3 aPos;
// 设置顶点最后的输出位置gl_Position=(x,y,z,w)，其中w=1.0表示这个点是一个位置而不是方向
void main() {
  gl_Position = vec4(aPos.x, aPos.y, aPos.z, 1.0);
}
```

以下自定义的片段着色器实现了：为每个片段指定一个固定的颜色，生成一个统一的橙色效果

```cpp
// 使用GLSL 3.3版本的核心模式
#version 330 core
// 从渲染管线输出顶点数据FragColor，是存储最终的颜色值的四维向量
out vec4 FragColor;
// 设置FragColor的具体值
void main() {
  FragColor = vec4(1.0f, 0.5f, 0.2f, 1.0f);
} 
```

### 4.2 着色器编译

```cpp
// 1. 将源码存储在字符串中
const char *vertexShaderSource = "#version 330 core\n"
  "layout (location = 0) in vec3 aPos;\n"
  "void main() {\n"
  " gl_Position = vec4(aPos.x, aPos.y, aPos.z, 1.0);\n"
  "}\0";
const char *fragmentShaderSource = "#version 330 core\n"
  "out vec4 FragColor;\n"
  "void main() {\n"
  " FragColor = vec4(1.0f, 0.5f, 0.2f, 1.0f);\n"
  "}\0";

// 2. 创建顶点着色器对象，传递着色器类型参数
unsigned int vertexShader;
vertexShader = glCreateShader(GL_VERTEX_SHADER);
unsigned int fragmentShader;
fragmentShader = glCreateShader(GL_FRAGMENT_SHADER);

// 3. 把着色器源码附加到着色器对象上，第一个参数是着色器对象，第二个参数是源码字符串数量，第三个参数是源码字符串
glShaderSource(vertexShader, 1, &vertexShaderSource, NULL);
glShaderSource(fragmentShader, 1, &fragmentShaderSource, NULL);

// 4. 编译着色器源码
glCompileShader(vertexShader);
glCompileShader(fragmentShader);
```

### 4.3 着色器链接

```cpp
// 1. 创建一个着色器程序对象
unsigned int shaderProgram;
shaderProgram = glCreateProgram();

// 2. 把着色器对象附加到了程序上
glAttachShader(shaderProgram, vertexShader);
glAttachShader(shaderProgram, fragmentShader);

// 3. 链接着色器对象
glLinkProgram(shaderProgram);

// 4. 删除着色器对象
glDeleteShader(vertexShader);
glDeleteShader(fragmentShader);
```

## 5. 元素缓冲对象

**元素缓冲对象（Element Buffer Object，EBO）**：用于存储**索引数据**，以消除**顶点数据的重复**

{% note warning flat %}
OpenGL的基本图元类型是三角形，如果我们想要画一个矩形，就需要**两个三角形（6个顶点）**拼凑到一起，但这样有两个顶点重复了，因此实际上我们**只需要四个顶点**即可
```cpp
float vertices[] = {
  // 第一个三角形
  0.5f, 0.5f, 0.0f,   // 右上角
  0.5f, -0.5f, 0.0f,  // 右下角（重复）
  -0.5f, 0.5f, 0.0f,  // 左上角（重复）
  // 第二个三角形
  0.5f, -0.5f, 0.0f,  // 右下角（重复）
  -0.5f, -0.5f, 0.0f, // 左下角
  -0.5f, 0.5f, 0.0f   // 左上角（重复）
};
```
{% endnote %}

**索引（index）**：是创建数组时，顶点数据在数组中的位置。`glDrawElements`函数从当前绑定到`GL_ELEMENT_ARRAY_BUFFER`目标的`EBO`中获取其索引
```cpp
// 数据
float vertices[] = {
  0.5f, 0.5f, 0.0f,   // 右上角，索引0
  0.5f, -0.5f, 0.0f,  // 右下角，索引1
  -0.5f, -0.5f, 0.0f, // 左下角，索引2
  -0.5f, 0.5f, 0.0f   // 左上角，索引3
};
// 索引
unsigned int indices[] = {
  0, 1, 3, // 第一个三角形
  1, 2, 3  // 第二个三角形
};

// 1. 创建对象
unsigned int VBO, VAO, EBO;
glGenVertexArrays(1, &VAO);
glGenBuffers(1, &VBO);
glGenBuffers(1, &EBO);
// 2. 绑定VAO
glBindVertexArray(VAO);
// 3. 给VBO添加数据
glBindBuffer(GL_ARRAY_BUFFER, VBO);
glBufferData(GL_ARRAY_BUFFER, sizeof(vertices), vertices, GL_STATIC_DRAW);
// 4. 给EBO添加索引
glBindBuffer(GL_ELEMENT_ARRAY_BUFFER, EBO);
glBufferData(GL_ELEMENT_ARRAY_BUFFER, sizeof(indices), indices, GL_STATIC_DRAW);
// 5. 给VAO添加属性
glVertexAttribPointer(0, 3, GL_FLOAT, GL_FALSE, 3 * sizeof(float), (void*)0);
glEnableVertexAttribArray(0);
```

{% note warning flat %}
当你绑定一个 VAO 时，最后一次绑定到该 VAO 的 EBO 会被自动绑定，当你使用 glDrawElements 绘制对象时，不再需要手动绑定 EBO
{% endnote %}

## 5. 渲染循环中绘制图形

```cpp
// 指定怎样处理顶点
glUseProgram(shaderProgram);
// 指定怎样解析顶点
glBindVertexArray(VAO);
// 指定怎样绘制顶点（没有EBO）
glDrawArrays(mode, index, count);
// 指定怎样绘制顶点（有EBO）
glDrawElements(mode, count, type, index);
```

- mode是图元类型：一般是`GL_TRIANGLES`
- type是数据类型：一般是`GL_UNSIGNED_INT`
- index是顶点数组中的起始索引
- count是绘制的顶点数量