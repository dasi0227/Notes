---
title: OpenGL：纹理
tags:
  - OpenGL
categories:
  - 笔记
cover: /image/graphic.png
abbrlink: 287384f0
date: 2024-09-24 21:12:30
description: 介绍了纹理的概念，环绕方式，过滤方式，加载方式，以及应用纹理
---
<meta name="referrer" content="no-referrer"/>

## 1. 什么是纹理？

**纹理（Texture）**：是一个**2D图片**，可以**无缝折叠贴合到物体表面**，用来添加物体的细节

**纹理坐标（Texture Coordinate）**：每个顶点可以绑定一个纹理坐标，用来标明纹理图片上的**哪个部分会被采样到该顶点**上
- 2D纹理坐标通常用`(s,t)`表示
- 纹理坐标起始于(0,0)即**纹理图片的左下角**, 终止于(1,1)即**纹理图片的右上角**
- **片段着色器**会对纹理坐标进行**插值计算**，得到片段的纹理坐标

```cpp
float texCoord[] = {
  0.0f, 0.0f, // 左上角
  1.0f, 0,0f, // 右下角
  0.5f, 1.0f, // 上中
}
```

![](https://dasi-blog.oss-cn-guangzhou.aliyuncs.com/ComputerGraphic/OpenGL202409291951528.png)

## 2. 纹理环绕方式

|环绕方式|描述|
|-|-|
|GL_REPEAT|重复纹理图形，是默认行为|
|GL_MIRRORED_REPEAT|重复纹理图形，但是会镜像翻转纹理|
|GL_CLAMP_TO_EDGE|对超出的纹理坐标会重复纹理边缘，产生一种边缘被拉伸的效果|
|GL_CLAMP_TO_BORDER|对超出的纹理坐标会使用用户指定的边缘颜色|

![](https://dasi-blog.oss-cn-guangzhou.aliyuncs.com/ComputerGraphic/OpenGL202409291951527.png)

绑定纹理环绕方式
```cpp
// 镜像反转重复
glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_WRAP_S, GL_MIRRORED_REPEAT);
glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_WRAP_T, GL_MIRRORED_REPEAT);
// 使用边缘颜色：需要传递一个颜色数组作为参数
float borderColor[] = { 1.0f, 1.0f, 0.0f, 1.0f };
glTexParameterfv(GL_TEXTURE_2D, GL_TEXTURE_BORDER_COLOR, borderColor);
```

## 3. 纹理过滤

**纹理过滤（Texture Filtering）**：当纹理的分辨率和显示的分辨率不一致的时候，需要对纹理像素进行过滤，从而得到显示像素颜色值

{% note warning flat %}
纹理坐标是连续值（可以取0到1内任何float值），纹理像素是离散值（可以取分辨率任何一个点）
{% endnote %}

|方式|描述|图像|
|-|-|-|
|邻近过滤（GL_NEAREST）|选择距离中心点最接近纹理坐标的像素颜色，是默认过滤方式|颗粒状图案|
|线性过滤（GL_LINEAR）|基于纹理坐标附近的纹理像素，计算出一个插值，距离坐标越近的颜色贡献越大|平滑图案，视觉效果更好|

![](https://dasi-blog.oss-cn-guangzhou.aliyuncs.com/ComputerGraphic/OpenGL202409291951526.png)

## 4. 多级渐远纹理

挑战：显示图像中有一些物体距离观察者远而有一些物体距离观察者近，但是它们都具有相同的纹理分辨率并采取一样的纹理过滤方式，这会使得距离观察者近的物体很清晰但距离观察者远的物体很模糊

**多级渐远纹理（Mipmap）**：它会自动生成不同级别的纹理图像，下一级的纹理图像分辨率是上一级纹理图像分辨率的二分之一，OpenGL会**根据物体距离观察者的距离自动选择合适的纹理图像**来进行纹理过滤

![](https://dasi-blog.oss-cn-guangzhou.aliyuncs.com/ComputerGraphic/OpenGL202409291951525.png)

```cpp
// 生成多级渐远纹理
glGenerateMipmap(GL_TEXTURE_2D);
```

|过滤方式|描述|
|-|-|
|GL_NEAREST_MIPMAP_NEAREST|使用最邻近的多级渐远纹理来匹配像素大小，并使用邻近插值进行纹理采样|
|GL_LINEAR_MIPMAP_NEAREST|使用最邻近的多级渐远纹理级别，并使用线性插值进行采样|
|GL_NEAREST_MIPMAP_LINEAR|在两个最匹配像素大小的多级渐远纹理之间进行线性插值，使用邻近插值进行采样|
|GL_LINEAR_MIPMAP_LINEAR|在两个邻近的多级渐远纹理之间使用线性插值，并使用线性插值进行采样|

## 5. 加载纹理数据

载入图像：利用`stb_image.h`单头文件图像加载库，并利用`stbi_load`函数获取图像数据：将图形的宽度、高度和颜色通道数填充进`width、height、nrChannels`中
```cpp
int width, height, nrChannels;
unsigned char *data = stbi_load("image_path", &width, &height, &nrChannels, 0);
```

{% label "生成纹理对象" orange %}
- 第一个参数：指定纹理对象，这里是指定绑定在`GL_TEXTURE_2D`的纹理对象
- 第二个参数：指定多级渐远纹理的级别，0表示基本级别
- 第三个参数：把纹理储存为何种格式，这里存储为RGB值
- 第四个参数：纹理的宽度
- 第五个参数：纹理的高度
- 第六个参数：设置为0，历史遗留问题
- 第七个参数：定义了原始图像的格式，这里是RGB值
- 第八个参数：定义了原始图像的数据类型，这里是unsigned byte数据类型
- 第九个参数：先前载入的纹理图像的数据
```cpp
glTexImage2D(GL_TEXTURE_2D, 0, GL_RGB, width, height, 0, GL_RGB, GL_UNSIGNED_BYTE, data);
```

## 6. 应用纹理

- 片段着色器利用uniform获取纹理图像
-  **采样器（sampler）**：是一个供纹理对象使用的**内建数据类型**，以**纹理类型作为后缀**
-  `vec4 texture(sampler2D sampler, vec2 coord);`：对纹理进行采样，返回一个vec4类型的颜色值

```cpp
// 片段着色器
#version 330 core
in vec3 ourColor;
in vec2 TexCoord;
out vec4 FragColor;
uniform sampler2D ourTexture;
void main() {
  FragColor = texture(ourTexture, TexCoord) * vec4(ourColor, 1.0);
}
```

## 7. 纹理单元

**纹理单元（Texture Unit）**：着色器需要访问纹理单元来获得纹理图像数据
```cpp
// 1. 生成纹理对象1
unsigned int texture1;
glGenTextures(1, &texture1);
// 2. 绑定纹理对象1
glBindTexture(GL_TEXTURE_2D, texture1);
// 3. 为纹理对象1设置环绕方式
glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_WRAP_S, GL_REPEAT);
glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_WRAP_T, GL_REPEAT);
// 4. 为纹理对象1设置过滤方式
glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_LINEAR);
glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_LINEAR);
// 5. 为纹理对象1加载纹理数据
int width, height, nrChannels;
unsigned char *data = stbi_load("path_to_img", &width, &height, &nrChannels, 0);
// 6. 生成纹理对象1的纹理图像
if (data) {
  glTexImage2D(GL_TEXTURE_2D, 0, GL_RGB, width, height, 0, GL_RGB, GL_UNSIGNED_BYTE, data);
  glGenerateMipmap(GL_TEXTURE_2D);
}
else {
  std::cout << "Failed to load texture" << std::endl;
}
// 7. 释放纹理对象1的纹理数据
stbi_image_free(data);
// 8. 为对应ID的着色器的uniform变量绑定纹理单元0
glUniform1i(glGetUniformLocation(shader.ID, "myTexture"), 0);
// 9. 激活纹理单元0
glActiveTexture(GL_TEXTURE0);
// 10. 绑定纹理单元0到纹理对象1
glBindTexture(GL_TEXTURE_2D, texture1);
```

## 8. 混合纹理

使用**mix函数**：前两个参数为纹理图像数据，三个参数为混合的比例
```cpp
FragColor = mix(texture(texture1, TexCoord), texture(texture2, TexCoord), 0.5);
```