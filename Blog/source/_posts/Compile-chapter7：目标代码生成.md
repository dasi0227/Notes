---
title: 目标代码生成
tags:
  - Compile
categories:
  - 笔记
cover: /image/compile.png
description: 目标代码生成概述、目标代码（指令集、寻址模式、地址分配）、待用与活跃、寄存器分配（原则、待用信息链表算法、寄存器分配算法、代码生成算法）
abbrlink: ca3cf4ed
date: 2025-06-20 16:29:50
---
<meta name="referrer" content="no-referrer"/>

## 1. 程序任务

1. 输入：优化的三地址中间代码序列

2. 指令选取：选择与中间代码序列等价的目标代码序列

   - 空间复杂度小：生成的目标代码越短越好
   
   
      - 时间复杂度小：生成的目标代码执行得越快越好，多利用寄存器，减少对存储器的访问次数
   
3. 寄存器分配：利用寄存器资源，减少内存访问开销

   - 分配：选择变量的值暂时驻留在寄存器中

   - 指派：为某些变量分配具体的寄存器

4. 指令调度：重新排列指令顺序，减少因依赖关系导致的停顿，提升指令级并行

5. 输出：目标代码



## 2. 目标代码

### 2.1 指令集

| 类别               | 说明                                                         |
| ------------------ | ------------------------------------------------------------ |
| LD dst, addr       | 从内存 addr 读取数据到寄存器（Load）                         |
| ST x, Ri           | 将寄存器数据写入内存（Store）                                |
| OP dst, src1, src2 | 执行二元运算 dst = src1 op src2                              |
| OP dst, src        | 执行一元运算 dst = op src                                    |
| BR L               | 无条件跳转到标签 L（Branch）                                 |
| CMP R1, R2         | 比较两个寄存器的值                                           |
| B\<cond> L         | 根据比较条件跳转到标签 L，其中 cond 有 LT、LE、GT、GE、EQ、NE |

![image-20250622171227065](https://dasi-blog.oss-cn-guangzhou.aliyuncs.com/Compile/202506221712110.png)

![image-20250622171237580](https://dasi-blog.oss-cn-guangzhou.aliyuncs.com/Compile/202506221712620.png)

### 2.2 寻址模式

| 模式  | 名称         | 说明                                             | 代价 |
| ----- | ------------ | ------------------------------------------------ | ---- |
| C     | 立即数       | 立刻就把常量 C 当作操作数                        | 1    |
| R     | 寄存器直接   | 操作数就存在寄存器里，无需再做寻址               | 0    |
| (R)   | 寄存器间接   | R 中存的是内存地址，CPU 取出后还要一次内存访问   | 0    |
| a(R2) | 直接变址寻址 | 计算地址 R + a，再去该内存单元取值               | 1    |
| *a(R) | 间接变址寻址 | 计算地址 R + a，再从该内存单元取地址，最后才取值 | 1    |
| x     | 直接内存寻址 | 地址 x 是一常量或符号地址，直接访问该内存单元    | 1    |
| *x    | 间接内存寻址 | 先从内存位置 x 得到一个地址，然后在该地址取值    | 1    |

![image-20250622171414997](https://dasi-blog.oss-cn-guangzhou.aliyuncs.com/Compile/202506221714046.png)

![image-20250622171423211](https://dasi-blog.oss-cn-guangzhou.aliyuncs.com/Compile/202506221714258.png)

### 2.3 地址分配

#### 2.3.1 静态分配

在编译的时候就为每个过程分配两块固定地址区间作为活动记录，调用时不会改变栈指针 SP

- codeArea：存放该过程对应机器指令的连续内存区间
- staticArea：存放每次调用的活动记录，比如返回地址、局部变量等

```text
假设现在要调用过程 p，假设每个指令占用 10 字节地址，每个 action 伪指令占用 10 字节地址

假设 p.staticArea = 564，p.codeArea = 300

...
100: action 						// 调用过程 p 之前的指令
120: ST 364, #140				// 将过程的返回地址存到 staticArea
130: BR 300							// 跳转到 codeArea 执行过程 p
140: action 						// 调用过程 p 之后的指令
150: ... 
...
200: action 						// 过程 p 的指令
210: BR *564						// 跳转到 564 存储的内存地址
...
564: #140
...
```

#### 2.3.1 栈分配

每次调用过程时都在运行时用栈指针动态分配活动记录，调用／返回时需要调整栈指针并读写栈指针相对偏移

- stackStart：调用点之前栈指针值
- recordSize：每次调用时要在栈上分配的活动记录大小（字节数）

```text
假设现在过程 m 要调用过程 p，过程 p 要调用过程 q，假设每个指令占用 10 字节地址，每个 action 伪指令占用 10 字节地址

假设过程 m 的 stackStart = 600，每个过程的 recordSize = 60

...
100: LD SP, #600			// 初始化栈指针为内存高端地址 600
110: action						// 调用过程 p 之前的指令
120: ADD SP, SP, 60		// 为过程 p 分配活动记录空间
130: ST *SP, #150			// 将过程 p 返回地址存入栈顶
140: BR 300						// 执行过程 p
150: SUB SP, SP, 60		// 收回分配的空间
160: action						// 调用过程 p 之后的指令
...
200: action						// 过程 q 的指令
210: BR *0(SP)				// 跳转回返回点
...
300: action						// 调用过程 q 之前的指令
310: ADD SP, SP, 60		// 为过程 q 分配活动记录空间
320: ST *SP, #340			// 将过程 q 的返回地址存入栈顶
330: BR 200						// 执行过程 q
340: SUB SP, SP, 60		// 收回分配的空间
350: action						// 调用过程 q 之后的指令
360: BR *0(SP)				// 跳转回返回点
... 
660: #150							// 存过程 p 的返回点
720: #340							// 存过程 q 的返回点
```



## 3. 代码生成器

### 3.1 待用与活跃

基本块：一段只能顺序执行，从头到尾没有分支也没有分支目标的指令序列

- 单一入口：除了起始指令，不能从别的地方跳转到中间执行
- 单一出口：除了末尾指令，不能从中间跳转到别的地方执行

`i: A := B op C`

- 定值：三地址指令的左侧目标变量，旧值会被新值覆盖，也就是**确定了值**

- 引用：三地址指令的左侧操作变量，只会利用值不会改变值，也就是**引用了值**

- 活跃：如果当前位置 i 之后，变量还会被引用，则称变量在当前位置 i 是活跃的

- 待用：从 i 开始向后看（包括i），第一次引用变量的指令号 j 为变量在 i 的待用

  > 待用一定活跃，活跃不一定待用

变量类型

- **用户变量**：在源代码明确定义的变量，总是假设在基本块的出口处仍然是活跃的
- **临时变量**：在生成中间代码时自动插入的存储中间结果的变量，通常只在单个基本块内被定义和引用，总是假设在基本块的出口处是不活跃的

![image-20250622172156002](https://dasi-blog.oss-cn-guangzhou.aliyuncs.com/Compile/202506221721056.png)

### 3.2 寄存器分配

#### 3.2.1 原则

- **最大化寄存器驻留**：当生成某变量的目标代码时，尽量让变量的中间结果或值保留在寄存器中
- **块边界**：进入基本块时所有寄存器是空闲的，离开基本块时释放所有占用的寄存器
- **及时回收**：不再被引用的变量所占用的寄存器需要尽早释放

#### 3.2.2 待用信息链表算法

为每个变量维护一个二元组表示是否待用（x表示在x待用，F表示非待用）和是否活跃（L表示活跃，F表示非活跃），将未来的信息回溯给先前的每个指令

1. 初始化所有用户变量为非待用和活跃 (F, L)，初始化所有临时变量为非待用和非活跃 (F, F)
2. 从后往前扫描基本块内的四元式 `i: A := B op C`
   1. 将 A 改为 (F, F)：A 的旧值被更改了，所以既不会被引用也不是活跃的
   2. 将 B 和 C 改为 (i, L)：B 和 C 的值未来会在 i 被引用，B 和 C 的值在之前是活跃的

![image-20250622172356677](https://dasi-blog.oss-cn-guangzhou.aliyuncs.com/Compile/202506221723733.png)

#### 3.2.3 寄存器分配算法

寄存器描述数组 RVALUE：标记当前正驻留在寄存器 R 中的变量

- RAVALUE[R] = {A}：A 独占寄存器 R
- RAVALUE[R] = {A, B}：B 和 C 共占寄存器 R（比如赋值 B:=C)
- RAVALUE[R] = {}：寄存器 R 空闲

变量地址描述数组 AVALUE：当前变量的值的存储位置描述

- AVALUE[A] = {R_k}：变量存在寄存器 R_k 中
- AVALUE[A] = {addr_a}：变量存在内存 addr_a 中
- AVALUE[A] = {R_k, addr_a}：变量既存在寄存器 R_k 中又存在内存 addr_a 中（率先使用寄存器）

寄存器分配函数 GETREG：将四元式 `i: A := B op C` 的编号 i 输入，按照以下优先级顺序返回寄存器来存结果 A

1. 如果 A 已经在某个寄存器 R，则返回 R
2. 如果 B 独占 R，且 B 不再被引用，则返回 R
3. 如果有空闲的 R，则返回 R
4. 选择引用位置最远的寄存器 R，如果占用这个 R 的变量不在内存，则需要先加载到内存防止数据丢失 `ST R, addr(v)`，然后再返回 R

```text
function GETREG(i: instruction index, A: Var) -> Reg:
		// 1. 已经分配
		for each R in Regs:
				if A in RVALUE[R]:
						return R
		
		// 2. B 没有引用
		if AVALUE[B] has R and Live[i][B] == false:
        return R
		
		// 3. 空闲寄存器
		for each R in Regs:
				if RVALUE[R] is {}:
						return R
		
		// 4. 最优搜索，写回内存
		bestR = find() // （此处省略伪代码）
		for each v in RVALUE[bestR]:
				if AVALUE[v] not has addr_v:
						emit ST bestR, addr(v)
						AVALUE[v] += { addr_v }
    return bestR
```

#### 3.2.4 代码生成算法

1. **给结果分配寄存器**：调用 R_k = GETREG(`A := B op C`)  给结果 A 分配寄存器
2. **利用寄存器执行计算**：利用 AVALUE[B] 和 AVALUE[C] 确定 B 和 C 的存储位置 B', C'
   1. 如果 B 的存储位置是 R_j ≠ R_k 或 addr_b，则生成：`LD R_k, B'; op R_k, C';`
   2. 如果 B 的存储位置就是 R_j = R_k，则生成：`op R_k, C';`
3. **清空 R_k**：对任何在 RVALUE[R_k] 的变量 v，令 AVALUE[v] -= {R_k}
4. **确定 A 的存储位置**：令 AVALUE[A] += {R_k}，RVALUE[R_k] += {A}
5. **及时恢复被无效占用的寄存器**：如果 B 或 C 的是非引用和非活跃，且其值存在于某个 R_j 中，则删除 RVALUE[R_j] 中的 B 或 C，删除 AVALUE[B] 或 AVALUE[C] 中的 R_j
6. **恢复所有寄存器**：如果到达基本块的末尾，对所有活跃变量，如果占用寄存器 R_k，则需要
   1. 把寄存器的值先存进内存，生成：`ST R_k, addr(v)`
   2. 令 AVALUE[v] = {addr_v}，令 RVALUE[R_k] = {}

```text
for each i: A := B op C do:
		// 1. 分配寄存器
		Rk = GETREG(i, A)
		
		// 2. 确定 B 和 C
    if ∃ Rj ∈ AVALUE[B] then B′ = Rj else B′ = addr(B)
  	if ∃ Rj ∈ AVALUE[C] then C′ = Rj else C′ = addr(C)
  	
		// 3. 生成目标代码
		if B' != Rk:
				emit LD Rk, B'
    emit OP Rk, C'
    
    // 4. 清除旧值
    for each v in RVALUE[R_k]:
        RVALUE[R_k] -= { v }
        AVALUE[v]   -= { R_k }
    for each Rj in AVALUE[A]:
    		RVALUE[Rj] 	-= { A }
    		AVALUE[A]		-= { R_j }
    
    // 5. 更新映射
    AVALUE[A]   += { Rk }
  	RVALUE[Rk]  += { A }
  	
  	// 6. 回收寄存器
  	for v in { B, C }:
  			for each (Rj in AVALUE[v]):
  					if Live[i][v] == false:
  							emit ST Rj, addr(v)
  							RVALUE[Rj] -= { v }
  							AVALUE[v]  -= { Rj }
 
// 7. 基本块出口
for each Rk in Regs:
		for each v in RAVLUE[Rk]:
				if Live[exit][v] == true:
						emit ST Rk, addr(v)
						RVALUE[Rk] -= { v }
						AVALUE[v]  = { addr(v) }
```

![image-20250622172659929](https://dasi-blog.oss-cn-guangzhou.aliyuncs.com/Compile/202506221726992.png)