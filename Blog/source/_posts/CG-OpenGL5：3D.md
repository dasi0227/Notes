---
title: OpenGL：3D
tags:
  - OpenGL
categories:
  - 笔记
cover: /image/graphic.png
abbrlink: d65938ac
date: 2024-10-10 21:12:50
description: 坐标系统、变换矩阵、观察、投影、视口
---
<meta name="referrer" content="no-referrer"/>

## 1. 数学基础

### 1.1 向量

一个有方向（Direction）和大小（Magnitude）的量，向量的每一项叫做分量，默认**向量的起点是原点**，因此只需要指定向量的终点就可以指示一个方向

|向量运算|描述|
|-|-|
|标量运算|一个向量加/减/乘/除一个标量，相当于对向量的每个分量分别进行该运算|
|取反|将向量的每个分量取反|
|加减|两个向量的对应分量进行加减|
|长度|对分量进行平方和后开根号|
|归一|每个分量除以向量的长度得到单位向量|
|点积|将对应分量逐个相乘|
|叉积|生成一个正交于两个输入向量的第三个向量|

### 2. 矩阵

一个二维数组，矩阵中每一项叫做矩阵的元素（element），矩阵可以通过`(i, j)`进行索引，i是行，j是列，矩阵的行数和列数分别叫做矩阵的维度（dimension）

|矩阵运算|描述|
|-|-|
|加减|两个矩阵对应位置的元素进行加减|
|数乘|矩阵的每个元素乘以一个标量|
|相乘|新矩阵每一个元素是对应行和对应列的线性组合|

{% note warning flat %}
向量可以看作是一个**Nx1的矩阵**
{% endnote %}

### 3. GLM

**GLM（OpenGL Mathematics）**：专门为OpenGL量身定做的数学库，它提供了许多数学函数和数据类型，用于处理图形学中的各种数学运算

```cpp
// 使用的时候需要包含这三个头文件
#include <glm/glm.hpp>
#include <glm/gtc/matrix_transform.hpp>
#include <glm/gtc/type_ptr.hpp>

// 数据类型
glm::vec3 vector1 = glm::vec3(1.0f, 1.0f, 1.0f);
glm::vec4 vector2 = glm::vec4(1.0f, 1.0f, 1.0f, 1,0f);
glm::mat3 matrix1 = glm::mat3(1.0f); // 初始化为3x3单位矩阵
glm::mat4 matrix2 = glm::mat4(0.0f); // 初始化为4x4零矩阵

// 运算
float mult_matrix = matrix1 * matrix2; // 矩阵乘法
float glm::dot(const glm::vec3 &x, const glm::vec3 &y); // 点乘
glm::vec3 glm::cross(const glm::vec3 &x, const glm::vec3 &y); // 叉乘
glm::vec3 glm::normalize(const glm::vec3 &v); // 归一
glm::mat4 glm::transpose(const glm::mat4 &m); // 转置
glm::mat4 glm::inverse(const glm::mat4 &m); // 取逆

// 变换
glm::mat4 glm::scale(const glm::mat4 &m, const glm::vec3 &scale); // 缩放
glm::mat4 glm::translate(const glm::mat4 &m, const glm::vec3 &offset); // 位移
glm::mat4 glm::rotate(const glm::mat4 &m, float angle, const glm::vec3 &axis); // 旋转
```

## 2. 变换

### 2.1 缩放

**缩放（Scale）**：对向量的不同分量大小进行**倍增或倍减**

缩放矩阵：**左对角线上每一个值是对应分量的缩放倍数**

![](https://dasi-blog.oss-cn-guangzhou.aliyuncs.com/ComputerGraphic/OpenGL202409291951524.png)

### 2.2 位移

**位移（Translate）**：对向量的不同分量**加上一个值**进行位移

位移矩阵：**最后一列的每个值是对应分量加上的值**

![](https://dasi-blog.oss-cn-guangzhou.aliyuncs.com/ComputerGraphic/OpenGL202409291951523.png)

### 2.3 旋转

**旋转（Rotate）**：指定**一个旋转轴和一个旋转角度**

旋转矩阵

![](https://dasi-blog.oss-cn-guangzhou.aliyuncs.com/ComputerGraphic/OpenGL202409291951522.png)

### 2.4 组合变换

之所以利用矩阵表示变换，就是因为可以**通过矩阵乘法可以将多个变换矩阵合并到一个变换矩阵**，但由于**矩阵乘法不满足交换律但满足结合律且变换顺序不同会导致结果不同**，所以变换一般遵从以下顺序：**缩放-旋转-位移**

由于是**利用矩阵左乘向量，所以计算式要从右往左读**，即$Transform = Translate * Rotate * Scale$

![](https://dasi-blog.oss-cn-guangzhou.aliyuncs.com/ComputerGraphic/OpenGL202409291951520.png)

## 3. 坐标系统

### 3.1 五个坐标系统

|名称|描述|作用|
|-|-|-|
|局部空间（Local）/物体空间（Object）|相对于物体自身原点的坐标系统|用于定义和操控物体自身的几何形状和运动|
|世界空间（World）|相对于固定的世界原点的坐标|用于将多个物体放在一个世界场景|
|观察空间（View）/视觉空间（Eye）|相对于相机/观察者的坐标|确定从相机视角看到的物体位置，从而进行投影|
|裁剪空间（Clip）|标准化设备坐标|用于确定哪些物体可以被看到，从而决定渲染哪些部分|
|屏幕空间（Screen）|相对于屏幕上窗口的坐标|用于最终渲染图像的坐标系统，使得物体能够正确地显示在屏幕上|

### 3.2 三个变换矩阵

|矩阵|变换|作用|
|-|-|-|
|观察（View）|世界到观察，3D->3D|用于确定在相机视角下的物体坐标|
|投影（Projection）|观察到裁剪，3D->2D|用于确定在相机视角下能被看到的物体和渲染后的物体|
|视口（ViewPort）|裁剪到屏幕，2D->2D|用于确定显示在相机屏幕上的物体|

### 3.3 右手坐标系

**食指向上表示y轴正方向，大拇指向右表示x轴正方向，中指向内表示z轴正方向**

## 4. 观察

### 4.1 摄像机

**如何定义摄像机**
|元素|定义|计算|注意|
|-|-|-|-|
|摄像机位置|摄像机位于世界空间中的位置|由用户自定义|z轴的正方向是指出屏幕，因此为了将镜头拉远，需要将摄像机位置沿着z轴的正方向移动|
|前轴|观察空间的z轴正方向|前轴向量 = 摄像机的位置向量 - 拍摄场景的原点向量|从拍摄场景指向摄像机的|
|右轴|观察空间的x轴正方向|右轴向量 = 上向量 x 前向向量|上向量是世界空间中指向y轴正方向的(0,1,0)|
|上轴|观察空间的y轴正方向|上轴向量 = 前向向量 x 右轴向量|上轴是观察空间的y轴，上向量是世界空间的y轴|

![](https://dasi-blog.oss-cn-guangzhou.aliyuncs.com/ComputerGraphic/OpenGL202410131901772.png)

**LookAt矩阵**：即观察矩阵，记位置向量为P，前向向量为F，右轴向量为R，上轴向量为U，则有
$$
\begin{bmatrix}
R_x & R_y & R_z & 0 \\
U_x & U_y & U_z & 0 \\
F_x & F_y & F_z & 0 \\
0 & 0 & 0 & 1
\end{bmatrix}
\times
\begin{bmatrix}
1 & 0 & 0 & -P_x \\
0 & 1 & 0 & -P_y \\
0 & 0 & 1 & -P_z \\
0 & 0 & 0 & 1
\end{bmatrix}
$$

glm提供的lookAt方法
```cpp
glm::mat4 viewMatrix = glm::lookAt(cameraPosition, targetPosition, upDirection);
```

### 4.2 基于摄像机的旋转

**欧拉角**：是可以表示3D空间中任何旋转的3个值
- **俯仰角（Pitch）**：绕X轴旋转的角度
- **偏航角（Yaw）**：绕Y轴旋转的角度
- **滚转角（Roll）**：绕Z轴旋转的角度

{% note success flat %}
可以这样理解，一个飞机目标沿着z轴正方向的航线飞行，遵循右手定则
- 飞机绕着x轴旋转，相当于机头翘起或垂落，也就是飞机俯仰姿态
- 飞机绕着y轴旋转，相当于机头向左或向右，也就是飞机偏离航线
- 飞机绕着z轴旋转，相当于机头顺指针或逆时针，也就是飞机滚转机身
{% endnote %}

![](https://dasi-blog.oss-cn-guangzhou.aliyuncs.com/ComputerGraphic/OpenGL202410131901771.png)

摄像机系统只关心俯仰角和偏航角，满足
- $forward.x = cos(pitch) * cos(yaw)$
- $forward.y = sin(pitch)$
- $forward.z = cos(pitch) * cos(yaw)$

![](https://dasi-blog.oss-cn-guangzhou.aliyuncs.com/ComputerGraphic/OpenGL202410131901770.png)
![](https://dasi-blog.oss-cn-guangzhou.aliyuncs.com/ComputerGraphic/OpenGL202410131901768.png)

### 4.2 一些摄像机操作

### 4.2.1 摄像机按照圆形轨迹移动

假设摄像机的圆形轨迹是位于X-Z平面的，因此要先定义距离世界坐标中心的半径radius，然后利用三角函数算出X坐标和Z坐标，最后传递给lookAt矩阵即可

```cpp
float radius = 10.0f;
float camX = sin(glfwGetTime()) * radius;
float camZ = cos(glfwGetTime()) * radius;
glm::mat4 view = glm::lookAt(glm::vec3(camX, 0.0, camZ), glm::vec3(0.0, 0.0, 0.0), glm::vec3(0.0, 1.0, 0.0));
```

### 4.2.2 摄像机根据键盘方向键移动

假设保持方向向量不变和移动速度不变
- **摄像机向前或向后移动，就将位置向量加上或减去方向向量**
- **摄像机向左或向右移动，就将位置向量加上或减去方向向量叉乘上向量得到的右轴向量**

```cpp
void processInput(GLFWwindow *window) {
  float cameraSpeed = 0.05f;
  if (glfwGetKey(window, GLFW_KEY_W) == GLFW_PRESS)
      cameraPos += cameraSpeed * cameraFront;
  if (glfwGetKey(window, GLFW_KEY_S) == GLFW_PRESS)
      cameraPos -= cameraSpeed * cameraFront;
  if (glfwGetKey(window, GLFW_KEY_A) == GLFW_PRESS)
      cameraPos -= glm::normalize(glm::cross(cameraFront, cameraUp)) * cameraSpeed;
  if (glfwGetKey(window, GLFW_KEY_D) == GLFW_PRESS)
      cameraPos += glm::normalize(glm::cross(cameraFront, cameraUp)) * cameraSpeed;
}
```

### 4.2.3 鼠标控制视角

鼠标水平移动影响偏航角，鼠标竖直移动影响俯仰角，可以通过存储上一帧鼠标的位置并获取当前帧鼠标的位置来计算

```cpp
// 应该隐藏光标并捕捉
glfwSetInputMode(window, GLFW_CURSOR, GLFW_CURSOR_DISABLED);
// 注册回调函数
glfwSetCursorPosCallback(window, mouse_callback);
// 监听鼠标移动
void mouse_callback(GLFWwindow* window, double xpos, double ypos) {
  // 如果这是第一次调用，则记录鼠标位置值
  if (firstMouse) {
    lastX = xpos;
    lastY = ypos;
    firstMouse = false;
  }
  // 计算
  float xoffset = xpos - lastX;
  float yoffset = lastY - ypos; 
  lastX = xpos;
  lastY = ypos;
  // 灵敏度因子，控制鼠标移动程度
  float sensitivity = 0.05;
  xoffset *= sensitivity;
  yoffset *= sensitivity;
  // 更新角度
  yaw   += xoffset;
  pitch += yoffset;
  // 避免翻转
  if(pitch > 89.0f)
    pitch = 89.0f;
  if(pitch < -89.0f)
    pitch = -89.0f;
  // 计算前向向量
  glm::vec3 front;
  front.x = cos(glm::radians(yaw)) * cos(glm::radians(pitch));
  front.y = sin(glm::radians(pitch));
  front.z = sin(glm::radians(yaw)) * cos(glm::radians(pitch));
  cameraFront = glm::normalize(front);
}
```

### 4.2.4 鼠标控制缩放

缩放是通过投影矩阵的fov参数实现的

```cpp
// 注册回调函数
glfwSetScrollCallback(window, scroll_callback);
// 鼠标滚轮控制缩放
void scroll_callback(GLFWwindow* window, double xoffset, double yoffset) {
  // 调整视野fov
  if(fov >= 1.0f && fov <= 45.0f)
    fov -= yoffset;
  // 控制上下限
  if(fov <= 1.0f)
    fov = 1.0f;
  if(fov >= 45.0f)
    fov = 45.0f;
}
// 调用投影函数获得投影矩阵
projection = glm::perspective(glm::radians(fov), 800.0f / 600.0f, 0.1f, 100.0f);
```

## 5. 投影

### 5.1 正射投影

**正射（Orthographic）**：所有的投影线都是平行的，意味着在投影过程中物体的**大小和形状不会发生变化**

正射投影：定义了一个**方体**，由**宽、高、近平面和远平面**所指定，在方体内，所有的物体都被投影到一个二维平面上，在方体外，所有的物体都被裁剪掉

```cpp
mat4 orthoMatrix = ortho(left, right, bottom, top, near, far);
```

![](https://dasi-blog.oss-cn-guangzhou.aliyuncs.com/ComputerGraphic/OpenGL202409291951519.png)

### 2.2 透视投影

**透视（Perspective）**：物体的大小和形状在投影过程中会发生变化，**越靠近观察者的物体越大，越远离观察者的物体越小**，依据透视除法有最后输出的顶点坐标为`(x/w,y/w,z/w)`

透视投影：定义了一个**锥体**，由**视野（Fov）、宽高比、近平面和远平面**所指定，在锥体内，所有的物体都被投影到一个二维平面上，在锥体外，所有的物体都被裁剪掉

### 2.3 深度缓冲

深度缓冲（Depth Buffer）/z缓冲（Z-buffer）：存储所有片段的深度信息/z值

深度测试：在渲染每个片段时，比较当前片段的深度值和深度缓冲中的值，**如果当前的片段在其它片段之后，它将会被丢弃，否则将会覆盖**

```cpp
// 启动深度测试
glEnable(GL_DEPTH_TEST);
// 清除深度缓冲
glClear(GL_DEPTH_BUFFER_BIT);
```
![](https://dasi-blog.oss-cn-guangzhou.aliyuncs.com/ComputerGraphic/OpenGL202409291951518.png)

## 6. 视口变换

