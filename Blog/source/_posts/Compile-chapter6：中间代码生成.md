---
title: 中间代码生成
tags:
  - Compile
categories:
  - 笔记
cover: /image/compile.png
description: 中间代码生成概述、中间表示（AST、DAG、TAC）、中间代码生成（布尔表达式的直接计算和间接计算）、回填技术
abbrlink: 546b580b
date: 2025-05-27 16:28:22
---
<meta name="referrer" content="no-referrer"/>

## 1. 程序任务

输入：抽象语法树和符号表

过程：对抽象语法树进行后跟遍历，针对不同类型的节点，结合符号表和临时变量，按照三地址规范各自生成中间代码

输出：三地址指令组成的中间代码序列



## 2. 中间表示

### 2.1 AST

分号、括号、关键字本身等都不会当节点，只保留运算符、标识符、常量、语句等关键符号

![image-20250622163035825](https://dasi-blog.oss-cn-guangzhou.aliyuncs.com/Compile/202506221630876.png)



### 2.2 DAG

1. 用一个哈希表记录已有节点
   1. 【ID, Identifier, Value】：代表叶子结点，记录标识符的词法值，是唯一的
   2. 【ID, Opeation, left_id, right_id】：代表内部节点，记录操作符及其左右节点，不是唯一的
2. 对 AST 做一次后序遍历：如果哈希表命中，则跳过，否则新建一个节点

> 与 AST 的不同之处：一个标识符只对应唯一一个叶子结点，可以复用相同的公共表达式

| ID   | 标识符/运算符 | left_id | right_id | 表达式                    |
| ---- | ------------- | ------- | -------- | ------------------------- |
| 1    | Identifier：a |         |          | a                         |
| 2    | Identifier：b |         |          | b                         |
| 3    | Identifier：c |         |          | c                         |
| 4    | Opeation：-   | 2       | 3        | b-c                       |
| 5    | Opeation：*   | 1       | 4        | a*(b-c)                   |
| 6    | Opeation：+   | 1       | 5        | a+(a*(b-c))               |
| 7    | Identifier：d |         |          | d                         |
| 8    | Opeation：*   | 4       | 7        | (b-c)*d                   |
| 9    | Opeation：+   | 6       | 8        | (a+(a\*(b-c)))+((b-c)\*d) |

![image-20250622163128729](https://dasi-blog.oss-cn-guangzhou.aliyuncs.com/Compile/202506221631787.png)

### 2.3 TAC

#### 2.3.1 三地址码

**地址**：并不是指机器运行时的**物理内存地址**，而是一种**符号化的存放位置标识**，用来描述三地址代码中**每个操作数或结果的来源／去向**

- 临时变量：用于存放中间计算结果，不直接对应源程序中的变量
- 源变量：直接引用程序中的命名
- 尝量：需考虑表达式中的类型转换问题
- 标签：用于条件跳转或无条件跳转的目标

**三地址码**：每条指令至多包含三个“地址”字段

**指令**

- 双目运算：`x = y op z`
- 单目运算：`x = op y`
- 赋值运算：`x = y`
- 无条件跳转：`goto L`
- 有条件跳转：`if x goto L / if op x goto L / if x op y goto L`
- 数组访问：`x = y[i]`
- 数组存储：`x[i] = y`
- 设置传参：`param x`
- 函数调用：`y = call f, n`
- 返回值：`return x`
- 获取地址：`x = &y`
- 获取值：`x = *y`
- 赋值地址：`*x = y`
- 标签定义：`L:`

#### 2.3.2 直接三元式

没有显式的 result 字段，结果是通过对位置的引用完成的，引用索引就是指令索引

```text
op arg1 arg2
```

![image-20250622163957470](https://dasi-blog.oss-cn-guangzhou.aliyuncs.com/Compile/202506221639519.png)

#### 2.3.3 间接三元式

与直接三元式类似，但是引用索引不是指令索引，而是一个单独的表索引，而表项指向指令索引

![image-20250622164722292](https://dasi-blog.oss-cn-guangzhou.aliyuncs.com/Compile/202506221647357.png)

```text
如果要在 0 和 1 之间加入一条指令
P[0] = &T[0]
P[1] = &T[1]
P[2] = &T[2]
直接放到最后
T = [ T[0], T[1], T[2], T_new ] 
然后循环更改逻辑表
for i = size-1 downto 1:
  P[i+1] = P[i]
P[1] = &T_new
```

#### 2.3.4 四元式

增加一个 result 元素存放指令结果

- 单目运算和赋值运算不需要使用 arg2
- 传递参数不需要使用 arg2 和 result
- 跳转将目标标号放入 result

![image-20250622165138995](https://dasi-blog.oss-cn-guangzhou.aliyuncs.com/Compile/202506221651049.png)



## 3. 中间代码生成

### 2.1 生成方案

**增量生成**：在分析过程中遇到动作就立刻输出一小段中间代码

**代码拼接**：在每条归约的语义动作中，将非终结符的地址属性和操作符拼接成完整的三地址序列，并添加到代码属性

- addr：子表达式的结果临时变量
- code：这颗子树对应的中间代码列表
- gen(...)：当前归约步骤产生的中间代码

![image-20250622165513601](https://dasi-blog.oss-cn-guangzhou.aliyuncs.com/Compile/202506221655657.png)

### 2.2 布尔表达式的直接计算

![image-20250622165821459](https://dasi-blog.oss-cn-guangzhou.aliyuncs.com/Compile/202506221658522.png)

![image-20250622165846450](https://dasi-blog.oss-cn-guangzhou.aliyuncs.com/Compile/202506221658502.png)

![image-20250622165852707](https://dasi-blog.oss-cn-guangzhou.aliyuncs.com/Compile/202506221658758.png)

![image-20250622165858640](https://dasi-blog.oss-cn-guangzhou.aliyuncs.com/Compile/202506221658703.png)

### 2.3 布尔表达式的间接计算

![image-20250622165943251](https://dasi-blog.oss-cn-guangzhou.aliyuncs.com/Compile/202506221659308.png)

![image-20250622170013826](https://dasi-blog.oss-cn-guangzhou.aliyuncs.com/Compile/202506221700886.png)

### 2.4 回填技术

表达式的真假出口对应的行号是不知道的，因此需要用占位符 ? 进行占位，在之后的分析中到了真假出口才可以确定行号，此时再回填到之前的占位符

- trueList：存条件为真的时候跳转的指令行号
- falseList：存条件为假的时候跳转的指令行号
- merge(x, y)：将两个链表的元素合并
- backpatch(x, y)：用第二个值填入第一个值

![image-20250622170751068](https://dasi-blog.oss-cn-guangzhou.aliyuncs.com/Compile/202506221707126.png)

```text
源代码：a < b  or  c < d  and  e > f

- 令 A 表示 a < b
- 令 B 表示 c < d
- 令 C 表示 e > f
- 令 D 表示 c < d  and  e > f
- 令 F 表示 a < b  or  c < d  and  e > f

// a < b 生成的中间代码
1: j<, a, b, ? 				// A.trueList 	= [1], A.begin = 1
2: j , -, -, ? 				// A.falseList  = [2]

// c < d 生成的中间代码
3: j<, c, d, ?				// B.trueList 	= [3], B.begin = 3
4: j , -, -, ?  			// B.falseList  = [4]

// e < f 生成的中间代码
5: j<, e, f, ?   			// C.trueList 	= [5], C.begin = 5
6: j , -, -, ? 				// C.falseList  = [6]

// 触发 and-回填
D.begin			= B.begin				= 3
B.trueList 	= C.begin 			= [5]
D.trueList 	= C.trueList 		= [5]
D.falseList = B+C.falseList = [4, 6]

// 触发 or-回填
F.begin 		= A.begin				= 3
A.falseList = D.begin 			= [3]
F.trueList 	= A+D.trueList 	= [1, 5]
F.falseList = D.falseList 	= [4, 6]

// 生成真假出口
1: j<, a, b, Ltrue
2: j , -, -, 3
3: j<, c, d, 5
4: j , -, -, Lfalse
5: j<, e, f, Ltrue
6: j , -, -, Lfalse
7: Ltrue:
		// 真分支
x: Lfalse:
		// 假分支
```
