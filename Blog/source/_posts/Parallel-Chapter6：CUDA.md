---
title: CUDA
tags:
  - Parallel
categories:
  - 笔记
cover: /image/parallel.png
abbrlink: 575c3f93
date: 2025-06-23 19:56:05
description: 异构并行编程、SM、程序结构、线程组织、内存管理、Tile 化、Bank
---
<meta name="referrer" content="no-referrer"/>

## 1. 概念

### 1.1 异构并行编程

| 维度     | 同构                   | 异构                               |
| -------- | ---------------------- | ---------------------------------- |
| 硬件架构 | 全部都是 CPU           | 多种类型混合使用（CPU+GPU）        |
| 编程模型 | MPI、Pthreads、OpenMP  | CUDA、OpenCL                       |
| 数据流   | 在同一类设备内存中流动 | 需跨设备内存拷贝                   |
| 任务划分 | CPU 大包大揽           | CPU 负责串行控制，GPU 负责并行计算 |

![image-20250623200425905](https://dasi-blog.oss-cn-guangzhou.aliyuncs.com/Parallel/202506232004978.png)

### 1.2 CUDA + GPU + SM

**CUDA（Compute Unified Device Architecture）计算统一设备架构**：是英伟达公司提出的一种**并行计算平台和并行编程 API**，本质上就是对 C 的一种扩展，从而可以**让 CPU 利用 GPU 来实现并行计算**

**GPU（Graphics Processing Unit）图形处理器**：专门为大规模并行计算设计的硬件加速器，追求**高吞吐量**，极其适合**批量的简单同质**计算，如图形渲染、深度学习、科学计算、视频转码等

- 内部包含成百上千个简化的运算核心，可以同时启动成千上万个线程
- 采用 SIMT 模式，只用单一指令流驱动一大批线程执行
- 每个线程可以访问全局内存和每个 SM 的共享内存，同时每个线程也都有自己的寄存器
- warp 是由 32 个连续编号的 CUDA 线程组成的一组线程，是 GPU 调度的最小单位

**SM（Streaming Multiprocessor）流处理器**：是 GPU 内部的调度中枢，通常每个 GPU 有上百个 SM，每个 SM 管理若干个 warp，一定程度上决定了 GPU 的并行吞吐能力

- 维护若干个 warp 的执行上下文，当某个 warp 因访存或分支而等待时，SM 立即切换到另一个就绪的 warp
- SM 按照 warp 把同一条指令广播到 CUDA Core 执行
- SM 有自己的 L1 缓存，拥有线程块级别的共享内存，可以加速对全局内存的访问
- SM 完全由硬件实现，无法由程序员直接操控

**CUDA Core**：是 GPU 中可执行线程指令的微核心

- 一个 CUDA Core 包含至少一个 ALU 加上配套的寄存器和最基本的控制逻辑
- 大量 CUDA Core 同时工作，总体算力远超同等面积的 CPU 核心
- 每个线程都会动态分配一个 CUDA Core，并且只会占用它并行计算一个时钟周期

**ALU（Arithmetic Logic Unit）算术逻辑单元**：是硬件真正执行浮点和整数运算的地方

> CPU ➡️ CUDA ➡️ GPU ➡️ SM ➡️ Core ➡️ ALU



## 2. 编程模型

### 2.1 术语

- 主机（host）：运行在 CPU 上的程序和系统内存
- 设备（device）：运行在 GPU 上的计算单元和其本地内存
- 核（kernel）：在 GPU 上并行执行的函数

![image-20250624015129193](https://dasi-blog.oss-cn-guangzhou.aliyuncs.com/Parallel/202506240151249.png)

### 2.2 程序结构

1. 在主函数外面利用 `__global__` 定义核

    ```c
    __global__
    void vectorAdd(const float *A, const float *B, float *C, int N) {
        int idx = blockIdx.x * blockDim.x + threadIdx.x;
        if (idx < N) {
            C[idx] = A[idx] + B[idx];
        }
    }
    ```

2. 在 CPU 内存中分配并初始化输入数据

    ```c
    float *h_A, *h_B, *h_C;
    h_A = (float*)malloc(bytes);
    h_B = (float*)malloc(bytes);
    h_C = (float*)malloc(bytes);
    ```

3. 在 GPU 内存中分配相同大小的缓冲区

    ```c
    float *d_A, *d_B, *d_C;                 
    cudaMalloc(&d_A, bytes);
    cudaMalloc(&d_B, bytes);
    cudaMalloc(&d_C, bytes);
    ```

4. 将数据从 Host 拷贝到 Device

    ```c
    cudaMemcpy(d_A, h_A, bytes, cudaMemcpyHostToDevice);
    cudaMemcpy(d_B, h_B, bytes, cudaMemcpyHostToDevice);
    ```

5. 启动 kernel，指定线程的组织形式，传递核的参数

    ```c
    vectorAdd<<<blocksPerGrid, threadsPerBlock>>>(d_A, d_B, d_C, N);
    ```

6. 同步等待所有 kernel 执行完毕

    ```c
    cudaDeviceSynchronize();
    ```

7. 将结果从 Device 拷贝到 Host

    ```c
    cudaMemcpy(h_C, d_C, bytes, cudaMemcpyDeviceToHost);
    ```

8. 资源释放

    ```c
    cudaFree(d_A);
    cudaFree(d_B);
    cudaFree(d_C);
    free(h_A);
    free(h_B);
    free(h_C);
    ```



## 3. 线程组织

### 3.1 Block

- block 包含若干个 thread
- thread 的组织方式可以是一维、二维和三维，通过 dim3 定义
- 每个线程块都对应一个共享内存，同一个线程块的内存可以通过共享内存进行通信
- 每个线程块内部的线程有同步机制，但是不同线程块之间没有同步机制

### 3.2 Grid

- grid 包含若干个 block
- block 的组织方式可以是一维、二维和三维，通过 dim3 定义
- 一个 grid 对应一次 kernel 的全部并行执行空间

### 3.3 warp

线程块只是 CPU 分配线程的对象，CUDA 底层会把线程块按照每 32 个线程划分为一个 warp

- warp **是 GPU 的基本执行单元，是 SM 的直接操作对象**

- warp 划分时是按照线程的线性编号进行划分的，因此**绝大部分的 warp 中的线程可能都位于同一行，即 threadIdx.y 相同**

![image-20250624015338283](https://dasi-blog.oss-cn-guangzhou.aliyuncs.com/Parallel/202506240153331.png)

**warp 分叉**：同一个 warp 内的线程在执行 if-else 时走向了不同分支，而 warp 同一时刻只能发送相同的指令，因此 GPU 必须将线程拆分成真假分支集按顺序执行，导致 GPU 的性能至少下降了一半

1. 硬件先判断哪几条线程满足条件，将它们标记为真分支子集，其他标记为假分支子集
2. 执行真分支时，对真分支子集中的线程逐条发射指令，而假分支子集中的线程保持闲置
3. 执行假分支时，对假分支子集中的线程逐条发射指令，而真分支子集中的线程线程保持闲置
4. 全部分支执行完毕：warp 恢复原始的全活状态，继续执行后续指令

![image-20250624024211253](https://dasi-blog.oss-cn-guangzhou.aliyuncs.com/Parallel/202506240242323.png)

### 3.4 全局索引

`gridDim` 又可以叫做 `blocksPerGrid`，代表网格有多少个线程块；`blockDim` 又可以叫做 `threadsPerBlock`，代表线程块有多少个线程

```c
dim3 gridDim(gx, gy);
dim3 blockDim(bx, by);
kernel<<<gridDim, blockDim>>>(…);
```

> 这些不是关键字，只是语义化的变量名，实际上想取什么名字都可以

内置变量

- blockIdx.y：当前线程所处的线程块在网格中的行索引
- blockIdx.x：当前线程所处的线程块在网格中的列索引
- blockDim.y：一个块有多少行，即每列有多少个线程
- blockDim.x：一个块有多少列，即每行有多少个线程
- threadIdx.y：当前线程在所处的线程块的行索引
- threadIdx.x：当前线程在所处的线程块的列索引

```c
int row = blockIdx.y * blockDim.y + threadIdx.y;
int col = blockIdx.x * blockDim.x + threadIdx.x;
```

> 注意这里的 y 指的是第几行，x 指的是第几列，与平时表示不一样

![image-20250623213409762](https://dasi-blog.oss-cn-guangzhou.aliyuncs.com/Parallel/202506232134811.png)



## 4. 内存管理

### 4.1 内存类型

| 类型     | 作用域     | 速度         | 用途                                                         |
| -------- | ---------- | ------------ | ------------------------------------------------------------ |
| 寄存器   | 单个线程   | 访问速度最快 | 存放最经常使用的中间变量                                     |
| 本地内存 | 单个线程   | 访问速度慢   | 由于寄存器空间有限，寄存器溢出时变量 spill 到本地内存        |
| 共享内存 | 单个线程块 | 访问速度快   | 线程块内的线程交换或复用数据                                 |
| 全局内存 | 整个设备   | 访问速度最慢 | kernel 输入输出的主要存储区，用于跨线程块和 Host–Device 间通信 |
| 常量内存 | 整个设备   | 访问速度较快 | 存放只读不变数据，例如超参数、查表数组、定值等               |
| 纹理内存 | 整个设备   | 访问速度较快 | CUDA 为了加速二维/三维数据访问而引入的只读缓存机制，专门用于纹理渲染 |

![image-20250623215543997](https://dasi-blog.oss-cn-guangzhou.aliyuncs.com/Parallel/202506232155060.png)

### 4.2 共享内存声明

静态分配：直接指定大小

```c
__global__ void myKernel(float *in, float *out, int N) {
    __shared__ float tile[256];
    // ...
}
```

动态分配：将内存大小作为 kernel 的第三个启动配置 <<<gridDim, blockDim, sharedMemBytes>>>

```c
__global__ void myKernel_dyn(float *in, float *out, int N) {
    extern __shared__ float tile[];
    // ...
}
```

### 4.3 Tile 化

Tile 化是一种共享内存的分配模式，通常**将大规模的数据划分成与线程块规模相匹配的数据块**，从而一个线程块内的全部线程可以一次性把一个 Tile 加载到共享内存，之后每个线程就可以从共享内存中读取数据

- 传统做法： 点乘需要 1 个 A 元素和 1 个 B 元素，1 个 C 元素需要进行 N 次点乘的累加，一共有 $N^2$ 个 C 元素，所以一共需要进行 $2 \times N \times N^2 = 2N^3$ 次全局内存读取
- Tile 化：每次构建 tile 都需要全局读 $T^2$ 次，之后 Tile 的读取可以认为时间为零，对于每个矩阵需要构建 $(\frac{N}{T})^2$ 个 tile，需要构建 A 和 B，所以一共需要进行 $2 \times T^2 \times (\frac{N}{T})^2 = 2N^2$ 次全局内存读取

```c
#define TILE_SIZE 32

// blockDim 	= (TILE_SIZE, TILE_SIZE)
// blockPerGridRow = (N + TILE_SIZE - 1) / TILE_SIZE
// gridDim 		= (blockPerGridRow, blockPerGridRow)

__global__
void matMulTiledSimple(const float *A, const float *B, float *C, int N) {
  	// 1. 分配共享内存
		__shared__ float Atile[TILE_SIZE * TILE_SIZE];
  	__shared__ float Btile[TILE_SIZE * TILE_SIZE];
  	
  	// 2. 计算全局索引
    int row = blockIdx.y * TILE_SIZE + threadIdx.y;
    int col = blockIdx.x * TILE_SIZE + threadIdx.x;

  	float sum = 0.0f;
  	
  	// 3. 以块为单位计算
  	int numTiles = N / TILE_SIZE;
	  for (int t = 0; t < numTiles; ++t) {
      	// 3.1 加入 A 的子块（以行）
      	int aRow = row;
      	int aCol = t * TILE_SIZE + threadIdx.x;
      	if (aRow < N && aCol < N) {
          	// 左边是共享内存位置，也就是数据块的位置，与线程块的位置一样
          	// 右边是全局内存位置
          	Atile[threadIdx.y * TILE_SIZE + threadIdx.x] = A[aRow * N + aCol];
        } else {
          	Atile[threadIdx.y * TILE_SIZE + threadIdx.x] = 0.0f;
        }
      	
      	// 3.2 加入 B 的子块（以列）
        int bRow = t * TILE_SIZE + threadIdx.y;
        int bCol = col;
        if (bRow < N && bCol < N) {
            Btile[threadIdx.y * TILE_SIZE + threadIdx.x] = B[bRow * N + bCol];
        } else {
            Btile[threadIdx.y * TILE_SIZE + threadIdx.x] = 0.0f;
        }
      
      	// 3.3 同步，确保所有线程写入共享内存
      	__syncthreads();
      
      	// 3.4 在共享内存上做 TILE_SIZE 长度的点乘累加
        for (int k = 0; k < TILE_SIZE; ++k) {
            float aVal = Atile[threadIdx.y * TILE_SIZE + k];
            float bVal = Btile[k * TILE_SIZE + threadIdx.x];
            sum += aVal * bVal;
        }
      
      	// 3.5 同步，准备下一个 tile
      	__syncthreads();  
    }
  
  	// 4. 写回内存
  	if (row < N && col < N) {
      	C[row * N + col] = sum;
    }
  	
}
```

### 4.4 Bank 

#### 4.4.1 定义

实际上，共享内存并不是简单的一大块存储，而是会被系统分成 32 个宽度为一个字（1word=4bytes=32bit）的 Bank

- 之所以分成 32 个 bank，是为了对应于 warp 中 32 个线程，从而可以在理论上实现每个线程都可以对应于一个独立的 bank
- 每个 Bank 都有独立的数据总线和缓冲区，如果一个时钟周期内，线程访问映射到不同的 Bank，硬件就可以并行返回 Bank 数据
- 每个 Bank 在一个时钟周期内都可以返回 1 个字，大大提升了吞吐量
- Bank 编号 = (字节地址 / 4) % Bank 数量 = 字地址 % Bank 数量

![image-20250624011958473](https://dasi-blog.oss-cn-guangzhou.aliyuncs.com/Parallel/202506240119550.png)

#### 4.4.3 Bank 冲突 

**Bank Conflict**：当线程访问**同一 Bank 上的不同地址**，由于 Bank 的带宽限制，硬件只能将**请求串行化**，导致延迟骤增

```c
float x = tile[ threadIdx.x * TILE_SIZE + k ]; // TILE_SIZE = 32
```

跨列访问

1. k 对整个 warp 是同一个常数，threadIdx.x 对整个 warp 是 0-31 中 32 个不同的值
2. warp 中的 32 条访问，访问的是 32 个不同的共享内存地址
3. Bank_id = (threadIdx.x *32 + k) % 32 = k % 32，warp 中的线程访问的是同一个 Bank

**Bank Broadcast**：当线程访问**同一 Bank 上的相同地址**，硬件只会进行一次内存读取，然后广播给所有请求的线程，避免串行化

```c
float x = tile[ threadIdx.y * TILE_SIZE + k ];
```

跨行访问

1. k 和 threadIdx.y 对整个 warp 是同一个常数

2. warp 中的 32 条访问，会映射到同一个 bank_id，而且都是访问同一个共享内存地址

![image-20250624014943412](https://dasi-blog.oss-cn-guangzhou.aliyuncs.com/Parallel/202506240149461.png)



#### 4.4.3 Padding 策略

目的：打乱共享内存行/列跨度，使并行访问分布到不同 Bank 或对齐同地址触发广播，从而消除 Bank冲突

实现：将**共享数组的第二维设置为与 Bank 数量互质的长度**

原理：只要 S 与 32 互质，那么对于任意两个不同的整数 $x_1\neq x_2，x_1\cdot S \bmod 32 \;\neq\; x_2\cdot S \bmod 32$

```c
// 原声明（可能冲突）
__shared__ float tile[32][32];
// 加1列填充（无冲突）
__shared__ float tile[32][32 + 1];
```

当跨列访问时，`bank_id = (threadIdx.x * 33 + k) % 32 = (threadIdx.x + k) % 32`，在 k 不变的情况下，只要 threadIdx.x 不一样，那么映射到的 bank_id 肯定不一样
