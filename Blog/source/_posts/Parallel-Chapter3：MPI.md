---
title: MPI
tags:
  - Parallel
categories:
  - 笔记
cover: /image/parallel.png
description: MPI 程序结构、点对点通信、集合通信、派生数据类型、性能评估、梯形积分、奇偶换位排序、矩阵向量乘法
abbrlink: 32b863e1
date: 2025-02-06 16:39:40
---
<meta name="referrer" content="no-referrer"/>

## 1. MPI 程序

### 1.1 概述

**消息传递接口（Message-Passing Interface, MPI）**是一组 C 函数库，而不是一种新的编程语言，主要用于**分布式内存系统中进程之间的通信**，通过**显式地发送和接收消息**来实现数据交换

1. 编写 MPI 程序时引入头文件，包含 MPI 标准接口的函数原型、常量和类型定义

   ```c
   #include <mpi.h>
   ```

2. 利用封装好的 mpicc 编译器生成可执行文件，自动将 MPI 头文件路径加入到编译器的搜索路径，并将 MPI 库路径加入到链接命令中

   ```bash
   mpicc -o main main.c
   ```

3. 启动并行程序，手动指定节点数量并启动多个 MPI 进程，同时为每个进程建立通信环境

   ```bash
   mpiexec -n 4 ./main
   ```

### 1.2 框架

| 过程 | 功能                           | MPI 函数                                                     |
| ---- | ------------------------------ | ------------------------------------------------------------ |
| 1    | 初始化 MPI 环境                | MPI_Init、MPI_Abort                                          |
| 2    | 获取当前进程的编号和总进程数量 | MPI_Comm_rank、MPI_Comm_size                                 |
| 3    | 调用 MPI 函数执行并行任务      | 点对点通信：MPI_Send、MPI_Recv<br />集合通信：MPI_Bcast、MPI_Scatter、MPI_Gather、MPI_Reduce |
| 4    | 设置同步路障                   | MPI_Barrier                                                  |
| 5    | 主进程输出汇总结果             | 无                                                           |
| 6    | 清理 MPI 环境                  | MPI_Finalize                                                 |

```c
#include <mpi.h>
#include <stdio.h>
#include <stdlib.h>

int main(int argc, char *argv[]) {
    // 1. 初始化 MPI 环境
    int err = MPI_Init(&argc, &argv);
    if (err != MPI_SUCCESS) {
        fprintf(stderr, "MPI_Init failed\n");
        MPI_Abort(MPI_COMM_WORLD, err);
    }

    // 2. 获取当前进程的编号和总进程数量
	  int rank, size, err;
    MPI_Comm_rank(MPI_COMM_WORLD, &rank);
    MPI_Comm_size(MPI_COMM_WORLD, &size);

    // 3. 并行任务区
  	...
  
    // 4. 同步路障
    MPI_Barrier(MPI_COMM_WORLD);
  	
  	// 5. 主进程输出结果
    if (rank == 0) {
        printf(...);
    }

    // 6. 清理 MPI 环境
    MPI_Finalize();
    return 0;
}
```

### 1.3 通信子

**通信子（communicator）**是 MPI 中描述**进程组的通信上下文**的对象，是 MPI 中**管理和组织进程通信的基本单位**

- **进程组**：明确了参与该通信子中通信的所有进程，只有同一通信子里的进程才能互相发送／接收消息
- **通信上下文**：保证消息隔离，不同通信子之间即使使用相同的消息标签、数据类型，也不会相互干扰
- **MPI_COMM_WORLD**：包含所有进程的全局通信子，是默认通信子
- **MPI_Comm**：通信子类型

通信子操作

- 复制已有的通信子，**拥有相同的进程组，但会创建新的上下文**

  ```c
  int MPI_Comm_dup(MPI_Comm comm, MPI_Comm *newcomm);
  ```

- 将一个通信子划分为多个新的通信子，每个通信子有不同的上下文，其中 color 是划分依据，key 是排序依据

  ```c
  int MPI_Comm_split(MPI_Comm comm, int color, int key, MPI_Comm *newcomm);
  ```

- 基于指定的进程组创建一个新的通信子

  ```c
  int MPI_Comm_create(MPI_Comm comm, MPI_Group group, MPI_Comm *newcomm);
  ```

- 释放通信子占用的资源

  ```c
  int MPI_Comm_free(MPI_Comm *comm);
  ```

- 获取指定通信子中包含的进程总数，存储到 size 中

  ```c
  int MPI_Comm_size(MPI_Comm comm, int *size);
  ```

- 获取当前进程在指定通信子中的编号，存储到 rank 中

  ```c
  int MPI_Comm_rank(MPI_Comm comm, int *rank);
  ```



## 2. 点对点通信

### 2.1 特点

点对点通信的通信双方都是单个进程，是一对一的通信模式

- **进程悬挂**
  - 阻塞发送：发送方会阻塞后续执行，直到 MPI 确保数据已经复制到内部缓冲区或真正传输并被接收方接收
  - 阻塞接收：接收方会阻塞后续执行，直到收到匹配的消息并把数据拷贝进缓冲区
- **有序性/不可超越性**：对同一源–目标对的多次发送，MPI 保证接收端按发送顺序接收，无须额外同步
- 接收原则：每条消息都携带**三要素 (source, tag, comm)**，只有三者全部匹配才算“命中”并交付接收缓冲区

### 2.2 MPI_Send

**发送方发送消息传递数据**

```c
int MPI_Send(
  	const void *buf, int count, MPI_Datatype datatype, 
  	int dest, int tag, MPI_Comm comm
);
```

- buf：指向待发送数据的起始地址
- count：待发送数据的元素数量
- datatype：待发送数据的数据类型
- dest：接收进程在指定通信子中的编号
- tag：发送消息的标签，必须指定一个非负整数，通常设置为 0 
- comm：指定通信上下文的通信子

### 2.3 MPI_Recv

**接收方接收消息获取数据**

```c
int MPI_Recv(
  	void *buf, int count, MPI_Datatype datatype, 
  	int source, int tag, MPI_Comm comm, 
  	MPI_Status *status
);
```

- buf：指向接收缓冲区的起始地址，长度至少为 count
- count：最多可接收元素的个数
- datatype：预期接收的数据类型
- source：发送进程在指定通信子中的编号，可以使用通配符  `MPI_ANY_SOURCE` 
- tag：要接收消息的标签
- comm：指定通信上下文的通信子，可以使用通配符 `MPI_ANY_TAG`
- status：消息的状态对象，可以忽略 `MPI_STATUS_IGNORE` 
  - status.MPI_SOURCE：实际发送者 rank
  - status.MPI_TAG：实际接收的标签
  - `MPI_Get_count(&status, datatype, &num)`：实际收到的元素数存到 num 中

### 2.4 MPI_Sendrecv

点对点死锁：P0 在等待 P1 接收，P1 也在等待 P2 接收，由于点对点通信是阻塞式的，因此 P1 和 P2 永远都在循环等待，导致死锁

```c
// P0:
MPI_Send(buf, n, MPI_INT, 1, tag, MPI_COMM_WORLD);
MPI_Recv(buf, n, MPI_INT, 1, tag, MPI_COMM_WORLD, &status);

// P1:
MPI_Send(buf, n, MPI_INT, 0, tag, MPI_COMM_WORLD);
MPI_Recv(buf, n, MPI_INT, 0, tag, MPI_COMM_WORLD, &status);
```

将进程的发送消息和接收消息操作合并为一条调用，系统内部会优化指令顺序，从而避免死锁

```c
int MPI_Sendrecv(
    const void *sendbuf, int sendcount, MPI_Datatype sendtype, int dest, int sendtag,
    void *recvbuf, int recvcount, MPI_Datatype recvtype, int source, int recvtag,
    MPI_Comm comm, MPI_Status *status
);
```

- sendbuf：指向本进程待发送数据起始地址
- sendcount：要发送的元素数量
- sendtype：发送数据的 MPI 类型
- dest：目标进程在 comm 中的 rank
- sendtag：发送消息的标签
- recvbuf：指向本进程接收缓冲区起始地址
- recvcount：接收缓冲区能容纳的最大元素数量
- recvtype：接收数据的 MPI 类型（应与发送端匹配）
- source：指定接收哪一 rank 的消息；可用 MPI_ANY_SOURCE
- recvtag：指定要接收的标签；可用 MPI_ANY_TAG
- comm：通信子，决定参与点对点的进程组
- status：输出参数，调用完成后可通过它获取实际接收的源、标签及元素数量

### 2.5 归约

归约指的是把**每个进程产生的多个局部值用某种结合性运算“汇总”成一个全局结果**

| 归约模式 | 说明                                                         | 时间复杂度 |
| -------- | ------------------------------------------------------------ | ---------- |
| 单点归约 | 所有非 0 进程将本地结果发送到主进程，主进程按顺序收到后逐一进行处理 | $p$        |
| 树形归约 | 把 p 个进程看作完全二叉树的叶子，按层两两配对归约，每轮进程数减半，直到根节点 | $\log_2 p$ |

```c
// 每一组中两个线程的 rank 间隔
double local = 0;
int step = 1;
while (step < p) {
  	// 每个线程在当前层的顺序索引
  	int idx = rank / step;
  	// 偶数索引则接收信息，并在本地归约局部结果
    if (id % 2 == 0) {
        int src = rank + step;
      	double tmp;
        MPI_Recv(&tmp, 1, MPI_DOUBLE, src, tag, comm, MPI_STATUS_IGNORE);
        local += tmp;
    }
	  // 奇数索引则发送信息
    else {
        int dst = rank - step;
        MPI_Send(&local, 1, MPI_DOUBLE, dst, tag, comm);
    }
    step *= 2;
}
```

![](https://dasi-blog.oss-cn-guangzhou.aliyuncs.com/Parallel/202502272001125.png)



## 3. 集合通信

### 3.1 特点

集合通信指的是一个通信子内的所有进程都要参与通信，无须显式指定目标或源

- **隐式同步**：大多数阻塞型集合通信，会在内部完成必要的同步，调用返回时保证数据已在所有进程就位
- **语义丰富**：适合进行**分发、收集、归约、广播、同步**等操作
- **算法自优化**：MPI 实现通常会根据消息大小、进程数、底层网络拓扑自动选择最优算法

### 3.2 MPI_Bcast

**根进程广播数据到通信子内的进程**

```c
int MPI_Bcast(
  	void *buf, int count, MPI_Datatype datatype, 
  	int root, MPI_Comm comm
);
```

- buf：广播方指向待广播数据的起始地址，接收方指向接收数据缓冲区的起始地址
- count：每个进程要发送／接收的元素数量
- datatype：元素的数据类型
- root：广播进程在指定通信子的编号
- comm：指定参与广播的进程组

### 3.3 MPI_Scatter

**根进程将发送缓冲区中的数据，按进程编号顺序以等块方式分发到通信子内所有进程的接收缓冲区**

```c
int MPI_Scatter(
    const void *sendbuf, int sendcount, MPI_Datatype sendtype,
    void *recvbuf,       int recvcount, MPI_Datatype recvtype,
    int root, MPI_Comm comm
);
```

- sendbuf：根进程的发送缓冲区起始地址，接收方填 NULL
- sendcount：根进程向每个进程发送的元素数量，接收方填 0
- sendtype：发送数据的类型，接收方填 MPI_DATATYPE_NULL
- recvbuf：各进程用于接收数据的缓冲区起始地址
- recvcount：每个进程接收的元素数量
- recvtype：接收数据的类型
- root：指定分发数据的根进程 rank
- comm：通信子，指定参与分发的进程组

> sendcount 和 recvcount 是一样的，不是指一共需要发送的数据数量

### 3.4 MPI_Gather

**将通信子内所有进程的发送缓冲区中的数据，按进程编号顺序，收集并拼接到根进程的接收缓冲区中**

```c
int MPI_Gather(
    const void *sendbuf, int sendcount, MPI_Datatype sendtype,
    void *recvbuf,       int recvcount, MPI_Datatype recvtype,
    int root, MPI_Comm comm
);
```

- sendbuf：各进程本地要发送的数据缓冲区起始地址
- sendcount：每个进程发送的元素数量
- sendtype：发送数据的类型
- recvbuf：根进程用于接收所有进程数据的缓冲区起始地址，发送方填 NULL
- recvcount：根进程为每个发送进程预留的接收元素数量，发送方填 0
- recvtype：接收数据的类型，发送方填 MPI_DATATYPE_NULL
- root：汇集数据的根进程 rank
- comm：通信子，指定参与收集的进程组

> recvcount 和 sendcount 是一样的，不是指一共需要接受的数据数量

### 3.5 MPI_Allgather

**将通信子内所有进程的发送缓冲区中的数据，按进程编号顺序，收集并拼接到所有进程的接收缓冲区中**

> 说白了就是每个进程都可以拿到聚集结果，而不单单是根进程，所以不再需要 root 参数，其他参数用法一致

```c
int MPI_Allgather(
    const void *sendbuf, int sendcount, MPI_Datatype sendtype,
    void       *recvbuf, int recvcount, MPI_Datatype recvtype,
    MPI_Comm    comm
);
```

### 3.6 MPI_Reduce

**对通信子内所有进程的发送缓冲区中的数据，使用指定的归约操作进行聚合，并将最终结果存放在根进程的接收缓冲区中**

```c
int MPI_Reduce(
    const void *sendbuf, void *recvbuf, int count, MPI_Datatype datatype, 
  	MPI_Op op,
  	int root, MPI_Comm comm
);
```

- sendbuf：各进程要归约的本地数据缓冲区起始地址
- recvbuf：根进程用于接收归约结果的缓冲区起始地址；非根进程可填 NULL
- count：要归约的元素数量（不是归约结果的元素数量）
- datatype：数据类型
- op：归约操作符
- root：接收和保存全局结果的根进程 rank
- comm：通信子，指定参与归约的进程组

![](https://dasi-blog.oss-cn-guangzhou.aliyuncs.com/Parallel/202502272001126.png)

注意

- MPI_Reduce 是对**长度为 N 的缓冲区做下标归约**，而不是扁平化归约
- 所有进程必须调用相同操作的归约函数
- 不允许使用同一个缓冲区**同时是输入缓冲和输出缓冲**，这样的结果是不可预测的

```text
0: [1 2 3 4 5]
1: [1 2 3 4 5]
2: [1 2 3 4 5]
求和的归约结果是 0: [3 6 9 12 15]，而不是：[45]
```



## 4. 派生数据类型

### 4.1 定义

派生数据类型允许用户自定义与原生类型不同的的**内存布局**，以便在一次通信调用中发送／接收非连续或结构化的数据块

- MPI 通信的成本是较大的，与其将基础类型分多次通信，不如将多个基础数据组合成一个派生数据类型，只需一次通信调用，就能把各段数据打包发送，显著**减少多次调用带来的启动延迟**
- 如果同一个布局会被多次发送／接收，提前创建并多次重用派生类型，可以把**创建／提交的成本摊薄，提高长期性能**
- 对于**非常复杂的非连续模式**，派生类型通常能带来更好的可维护性和性能，但是相对简单的非连续模式可能达不到好的效果，甚至会降低性能

使用流程

1. 创建：调用相应的 `MPI_Type_*`函数，描述布局
2. 提交：调用 `MPI_Type_commit(&newtype)` 让 MPI 知道新类型的含义
3. 使用：在 MPI 通信函数中的 datatype 参数中使用
4. 释放：调用 `MPI_Type_free(&newtype)` 释放新类型占用的资源

### 4.2 MPI_Type_contiguous

**将若干个连续的元素合并成一个新的派生类型**

```c
int MPI_Type_contiguous(int count, MPI_Datatype oldtype, MPI_Datatype *newtype);
```

- count：要合并的元素个数
- oldtype：已有的基础类型或已提交的派生类型
- newtype：输出的新类型句柄

### 4.3 MPI_Type_create_struct

**将若干块不同类型的数据组合成一个新的派生类型**

```c
int MPI_Type_create_struct(
    int count,
    const int blocklens[],
    const MPI_Aint displs[],
    const MPI_Datatype types[],
    MPI_Datatype *newtype
);
```

- count：块的数量
- blocklens[i]：第 i 块中元素的个数
- displs[i]：第 i 块相对于结构体起始地址的字节偏移
- types[i]：第 i 块的元素 MPI 类型
- newtype：输出的新类型句柄

构建流程

```c
// 0. 定义结构体
struct Particle {
		double 	pos[3];
		int			id;
		float 	mass;
} particle;

// 1. 确定块数
int count = 3;

// 2. 确定每块的元素数量
int blocklens[] = { 3, 1, 1 };

// 3. 确定每块的数据类型
MPI_Datatype types[] = { MPI_DOUBLE, MPI_INT, MPI_FLOAT };

// 4. 获取每块的地址
MPI_Aint base, addr_pos, addr_id, addr_mass;
MPI_Get_address(&particle,       &base);
MPI_Get_address(&particle.pos,   &addr_pos);
MPI_Get_address(&particle.id,    &addr_id);
MPI_Get_address(&particle.mass,  &addr_mass);

// 5. 计算每块的偏移
MPI_Aint displs[3];
displs[0] = addr_pos - base;
displs[1] = addr_id  - base;
displs[2] = addr_mass- base;

// 6. 创建并提交类型
MPI_Datatype MPI_PARTICLE;
MPI_Type_create_struct(count, blocklens, displs, types, &MPI_PARTICLE);
MPI_Type_commit(&MPI_PARTICLE);

// … 在通信里使用 MPI_PARTICLE …

// 7. 用完释放
MPI_Type_free(&MPI_PARTICLE);
```



## 5. 性能评估

### 5.1 计时

| **时间类型** | **定义**                                                     |
| ------------ | ------------------------------------------------------------ |
| 程序运行时间 | 从程序**开始运行到结束运行**所耗费的墙钟时间，包含初始化、通信、I/O 和计算等各部分的总耗时 |
| CPU 时间     | 程序实际**占用 CPU 执行指令**的时间，不包括等待 I/O 或其他阻塞操作的停用时间 |
| 并行计算时间 | 所有进程**执行并行计算部分**所花费的时间，以最慢进程的耗时为准 |

```c
// 0. 声明变量
double t0, t1;
// 1. 所有进程从同一起点开始
MPI_Barrier(comm); 
// 2. 记录开始时间
double t0 = MPI_Wtime();
// ... 任务执行...
// 3. 所有线程都需要等待最慢进程
MPI_Barrier(comm); 
// 4. 记录结束时间
double t1 = MPI_Wtime();
// 5. 只有主进程负责输出
if (rank == 0) {
  	printf("Elapsed = %fs\n", t1 - t0);
}
```

> 由于操作系统的不可预知性，同一段程序的运行时间不可能每次都完全一样

### 5.2 问题规模 vs 进程数量

- 问题规模不变，随着进程数量增加，运行时间逐渐下降：更多进程意味着更强的计算能力，**展现了强扩展性**

- 进程数量不变，随着问题规模增加，运行时间逐渐上升：更多数据意味着更多计算
- 当问题规模较小且进程数量较少的时候，或者问题规模较大且进程数量较多的时候，增加进程数量可以显著降低运行时间：每个进程拿到的计算适中，并行收益大于开销成本
- 当问题规模较小且进程数量较多的时候，增加进程数量不会使得运行时间显著下降，甚至会导致运行时间提升：每个进程拿到的计算太少，导致开销成本大于并行收益
- 当问题规模较大且进程数量较多的时候，近似线性效率：增加进程数量可以适配增大问题规模，**展现了弱扩展性**
- 当问题规模较小且进程数量较多的时候，效率严重下降：并行粒度过细，单位进程的有效工作时间微乎其微

![](https://dasi-blog.oss-cn-guangzhou.aliyuncs.com/Parallel/202502272001131.png)

## 6. 实践

### 6.1 梯形积分法

#### 6.1.1 公式推导

$$
\begin{aligned}
\int_a^b f(x)\,\mathrm{d}x 
&\approx \frac{h}{2}\Bigl[f(x_0)+f(x_1)\Bigr]+\cdots+\frac{h}{2}\Bigl[f(x_{n-1})+f(x_n)\Bigr]\\
&= \frac{h}{2}\Bigl[f(x_0)+2f(x_1)+\cdots+2f(x_{n-1})+f(x_n)\Bigr]\\
&= \frac{h}{2}\Bigl[f(x_0) + f(x_n)\Bigr] + h\Bigl[f(x_1) + \cdots + f(x_{n-1})\Bigr]
\end{aligned}
$$

![](https://dasi-blog.oss-cn-guangzhou.aliyuncs.com/Parallel/202502272001123.png)

#### 6.1.2 串行算法

```text
h = (b-a) / n
for (i = 0; i < n; i++) {
  x_i = a + i * h
  x_j = a + (i + 1) * h
  y += f(x_i) + f(x_j)
}
y = h / 2 * y
```

#### 6.1.3 并行算法

```c
#include <mpi.h>
#include <stdio.h>
#include <stdlib.h>

// 函数，不关注如何实现
double f(double x) {...}

int main(int argc, char** argv) {
  	// 1. 初始化环境
    int err = MPI_Init(&argc, &argv);
    if (err != MPI_SUCCESS) {
        fprintf(stderr, "MPI_Init failed\n");
        MPI_Abort(MPI_COMM_WORLD, err);
    }
  	
  	// 2. 获取环境信息
  	int size, rank;
  	MPI_Comm_rank(MPI_COMM_WORLD, &rank);
  	MPI_Comm_size(MPI_COMM_WORLD, &size);
  	
  	// 3. 初始化数据，假设 f(x)=x^2
  	double a = 1, b = 10;
  	int n = 10000;
  	double h = (b - a) / n;
  
  	// 4. 每个进程负责的区间
  	int base = n / size;
  	int rest = n % size;
    int local_n = base + (rank < rest ? 1 : 0);
  	int start 	= rank * base + (rank < rest ? rank : rest);
  	int end 		= start + local_n;
  	
  	// 5. 每个进程负责的计算
  	double x_i = 0.0, x_j = 0.0, local_y = 0.0;
  	for (int i = start; i < end; i++) {
      	x_i = a + i * h;
      	x_j = a + (i + 1) * h;
      	local_y += f(x_i) + f(x_j);
    }
  	
  	// 6. 集合通信
  	double y = 0.0;
  	MPI_Reduce(&local_y, &y, 1, MPI_DOUBLE, MPI_SUM, 0, MPI_COMM_WORLD);
  	y *= h * 0.5;
  	
  	// 7. 主进程负责输出
  	if (rank == 0) {
      	printf("Integral from %g to %g of f(x)=x^2 ≈ %.6f\n", a, b, y);
    }
  
    // 8. 清理环境
  	MPI_Finalize();
		return 0;
}
```

### 6.2 并行奇偶换位排序算法

#### 6.2.1 原理

反复交替执行两个阶段来排序，**每个阶段内的【比较交换】操作彼此独立**，因此可以并行执行，同时可以确保**如果序列有 n 个键值，那么经过 n 个阶段后，序列一定可以排好序**

#### 6.2.2 串行算法

- 奇数阶段：比较序列中索引为奇数的元素与其后面的相邻元素，如果前者大于后者，则交换
- 偶数阶段：比较序列中索引为偶数的元素与其后面的相邻元素，如果前者大于后者，则交换

{% note success flat %}
起始：5，9，4，3
0 偶数：5，9，3，4
1 奇数：5，3，9，4
2 偶数：3，5，4，9
3 奇数：3，4，5，9
{% endnote %}

#### 6.2.3 并行算法

1. 数据分发：主进程通过 MPI_Scatter 将待排序数组分发给各个进程（可以在本地做先做一次排序）
2. 偶数阶段
   - 如果进程号为偶数，则发送本地数组到右侧进程
   - 如果进程号为奇数，则发送本地数组到左侧进程
3. 奇数阶段
   - 如果进程号为奇数，则发送本地数组到右侧进程
   - 如果进程号为偶数，则发送本地数组到左侧进程
4. 合并数据：将本地数组和接收数组进行合并排序，小编号进程保留小半部分，大编号进程保留大半部分
5. 数据汇总：主进程通过 MPI_Gather 得到全局排序数组

> 第一个进程可能没有左侧进程，最后一个进程可能没有右侧进程，可以设置 `MPI_PROC_NULL` 来表示空通信，也可以直接跳过

```C
#include <mpi.h>
#include <stdio.h>
#include <stdlib.h>

// 合并数组并进行排序，不关注如何实现
void merge_sort(int *a, int *b, int *out, int length) {...}
// 初始化数组，不关注如何实现
void init(int *x, int length){...}

int main(int argc, char** argv) {
  	// 1. 初始化环境
    int err = MPI_Init(&argc, &argv);
    if (err != MPI_SUCCESS) {
        fprintf(stderr, "MPI_Init failed\n");
        MPI_Abort(MPI_COMM_WORLD, err);
    }
  	
  	// 2. 获取环境信息
  	int size, rank;
  	MPI_Comm_rank(MPI_COMM_WORLD, &rank);
  	MPI_Comm_size(MPI_COMM_WORLD, &size);
  
  	// 3. 初始化数据（不考虑不可整除）
  	int n = 1000;
  	int local_n = n / size;
  	int *x 			= malloc(sizeof(int) * n);
  	int *local_x = malloc(sizeof(int) * local_n);
  	int *local_y = malloc(sizeof(int) * local_n);
  	int *local_z = malloc(sizeof(int) * local_n * 2);
  	init(x, n);
  
  	// 4. 分发数据
    MPI_Scatter(
      x,       local_n, MPI_INT,
      local_x, local_n, MPI_INT, 
      0, MPI_COMM_WORLD
    );
  	
  	// 5. 奇偶交换排序
  	for (int phase = 0; phase < size; phase++) {
      	// 5.1 寻找发送对象
      	int partner;
      	// 偶数阶段
      	if (phase % 2 == 0) {
          	partner = rank % 2 == 0 ? rank + 1 : rank - 1;
        }
      	// 奇数阶段
      	if (phase % 2 != 0) {
          	partner = rank % 2 != 0 ? rank + 1 : rank - 1;
        }
      
      	// 5.2 发送本地数组，进行合并排序
      	if (partner >= 0 && partner < size) {
          	MPI_Sendrecv(
            	local_x, local_n, MPI_INT, partner, 0,
              local_y, local_n, MPI_INT, partner, 0,
             	MPI_COMM_WORLD, MPI_STATUS_IGNORE
            );
          	merge_sort(local_x, local_y, local_z, local_n);
        }
      
      	// 5.3 更新本地数组
        if (rank < partner) {
						memcpy(local_x, local_z, local_n * sizeof(int));
        }
      	if (rank > partner) {
          	memcpy(local_x, local_z + local_n, local_n * sizeof(int));
        }
    }
  
  	// 6. 集合通信
  	MPI_Gather(
      	local_x, local_n, MPI_INT,
      	x, 			 local_n, MPI_INT,
      	0, MPI_COMM_WORLD, 
    );
  	
  	// 7. 主进程负责输出
  	if (rank == 0) {
        printf("Sorted array:\n");
        for (int i = 0; i < n; i++) {
            printf("%d ", x[i]);
        }
        printf("\n");
    }
  
    // 8. 清理环境
  	MPI_Finalize();
  	free(x);
  	free(local_x);
  	free(local_y);
  	free(local_z);
		return 0;
}
```

### 6.3 矩阵乘法

![image-20250624133817398](https://dasi-blog.oss-cn-guangzhou.aliyuncs.com/Parallel/202506241338469.png)

```c
#include <mpi.h>
#include <stdio.h>
#include <stdlib.h>

// 初始化矩阵，不关注如何实现
void initMat(int rows, int cols, double *M) {...}

int main(int argc, char** argv) {
  	// 1. 初始化环境
    int err = MPI_Init(&argc, &argv);
    if (err != MPI_SUCCESS) {
        fprintf(stderr, "MPI_Init failed\n");
        MPI_Abort(MPI_COMM_WORLD, err);
    }
  	
  	// 2. 获取环境信息
  	int size, rank;
  	MPI_Comm_rank(MPI_COMM_WORLD, &rank);
  	MPI_Comm_size(MPI_COMM_WORLD, &size);
  
		// 3. 读取命令行参数
  	int m = atoi(argv[1]);
	  int n = atoi(argv[2]);
	  int k = atoi(argv[3]);
  
  	// 4. 根进程负责分配内存，并初始化数据 A 和 B 的数据
    double *A = NULL, *B = NULL, *C = NULL;
  	if (rank == 0) {
     		A = malloc(m * n * sizeof(double));
        B = malloc(n * k * sizeof(double));
        C = malloc(m * k * sizeof(double));
        initMat(m, n, A);
        initMat(n, k, B); 	
    } else {
      	B = malloc(n * k * sizeof(double));
    }
  
  	// 5. 根进程分发 A 给所有进程（假设可以整除）
  	int m_local = m / size;
    double *A_local = malloc(m_local * n * sizeof(double));
    double *C_local = malloc(m_local * k * sizeof(double));
  	MPI_Scatter(
      	A, 				m_local * n, MPI_DOUBLE, 
      	A_local, 	m_local * n, MPI_DOUBLE, 
      	0, MPI_COMM_WORLD
    );
  
  	// 6. 根进程广播 B 给所有进程
  	MPI_Bcast(B, n * k, MPI_DOUBLE, 0, MPI_COMM_WORLD);
  
  	// 7. 执行矩阵乘法
  	for (int i = 0; i < m_local; i++) {
      	for (int j = 0; j < k; j++) {
          	double sum = 0.0;
          	for (int t = 0; t < n; t++)
              	sum += A_local[i * n + t] * B[t * k + j];
          	C_local[i * k + j] = sum;
        }
    }
    
  	// 8. 汇总结果
  	MPI_Gather(
      	C_local, m_local * k, MPI_DOUBLE,
      	C, 			 m_local * k, MPI_DOUBLE,
      	0, MPI_COMM_WORLD, 
    );
  
    // 8. 清理环境
  	if (rank == 0) {
      free(A);
      free(B);
      free(C);
    }
  	else {
      free(B);
    }
    free(A_local);
  	free(C_local);
  	MPI_Finalize();
		return 0;
}
```