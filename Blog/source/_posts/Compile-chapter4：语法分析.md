---
title: 语法分析
tags:
  - Compile
categories:
  - 笔记
cover: /image/compile.png
description: 语法分析概述、确定的文法、LL(1)（FIRST、FOLLOW、SELECT）、LR(0)（CLOSURE、GOTO、SHIFT、REDUCE）、SLR(1)、LR(1)、LALR(1)
abbrlink: 1a450c6f
date: 2025-03-24 15:33:40
---
<meta name="referrer" content="no-referrer"/>

## 1. 程序任务

1. 输入：token 流
2. 语法检查：token 是否语法规则
3. 语法推导：按照文法规则构造解析器，将 token 连接成结构化的语法树
4. 输出：语法树



## 2. 确定的文法

### 2.1 定义

性质：

- **无二义性**：每个输入串只有唯一的推导/语法树
- **由确定性解析方法唯一解析**：在推导过程中可以根据当前的输入符号唯一确定选哪个产生式往下推导

充分条件：
- **每个产生式的右部由终结符开头**
- **同一个非终结符的不同产生式的右部由不同的终结符开头**

### 2.2 改写流程

1. 消除左公因子： $A \to \alpha \beta_1 \mid \alpha \beta_2$，提取左公因子 $\alpha$，引入新的非终结符 $A'$，转换为 $A \to \alpha A', \quad A' \to \beta_1 \mid \beta_2$
2. 消除直接左递归： $A \to A\alpha \mid \beta$，引入新的非终结符 $A'$，转换为 $A \to \beta A', \quad A' \to \alpha A' \mid \varepsilon$，

3. 消除间接左递归：将非终结符按任意顺序排列，依次进行代入，如果存在直接左递归后消除，最后去掉不可到达的产生式
4. 消除起始符号的空产生式：$S \to \varepsilon$，引入新的起始符号 $S'$，转换为  $S' \to S \mid \varepsilon$
5. 消除所有空产生式：$S \to A\alpha$ 和 $A \Rightarrow \varepsilon$，转换为 $S \to A\alpha \mid \alpha$



## 3. 自顶向下分析

### 3.1 FIRST

定义：对任何符号串 α（可以是一个终结符、一个非终结符，或任何符号串），FIRST(α) 是「**α 能推导出的所有字符串的首个终结符**」的集合，特别地如果 α 能推导出空串 ε，则 ε 也属于 FIRST(α)

意义：当要展开非终结符 A 且输入字符是 a 的时候，**对于每个产生式 A→α，只要 a 在 FIRST(α) 里，就能确定使用 A→α**

计算规则：先求出所有非终结符和终结符的 FIRST 集，再求出每个产生式右部符号串的 FIRST 集

- 终结符：$FIRST(a)=\{a\}$，有且只有自己
- 非终结符：若 $A$ 的产生式有 $A\to X_1X_2\cdots X_k$，依次把 $X_i$ 的 FIRST 集合并入 FIRST(A)，直到遇到一个不包含 ε 的 $X_i$ 为止，如果所有 $X_1,\dots,X_k$ 都能推出 ε，则也把 ε 加入 FIRST(A)
- 符号串：对于 α= X₁X₂…Xₙ，把 FIRST(X₁) 去掉 ε 并入，若 FIRST(X₁) 包含 ε，则把 FIRST(X₂) 去掉 ε 并入，依此类推，如果所有 FIRST(Xᵢ) 都含 ε，最后把 ε 加入 FIRST(α)

计算流程

1. **先对所有产生式的左部分析，求出每个非终结符的 FIRST**
2. **再对所有产生式的右部分析，求出每个符号串的 FIRST**

### 2.2 FOLLOW

定义：对任何非终结符 A，FOLLOW(A) 是「**在所有可能的句型推导中，A 右侧紧跟着的终结符集合**」，特别地如果 A 能出现在句子末尾，则输入结束标记 $ 也属于 FOLLOW(A)

意义：当要展开非终结符 A 且输入字符是 a 的时候，**如果没有任何产生式 A→α 满足 a∈FIRST(α)，但 a 在 FOLLOW(A) 并且存在产生式 A→ε，就能确定使用 A→ε**

计算规则

1. 对于开始符号，先把 $ 加入 FOLLOW(S)；对所有其他非终结符 A，令 FOLLOW(A) = ∅
2. 遍历所有产生式 $A \;\to\; X_1\,X_2\,\cdots\,X_n$：
   1. 将 FIRST($X_{i+1}$) 去掉 ε 后并入 FOLLOW($X_i$)
   2. 如果 FIRST($X_{i+1}$) 包含 ε，则继续看 $X_{i+2}$，将 FIRST($X_{i+2}$) - {ε} 并入 FOLLOW($X_i$)，直到遇到第一个 FIRST 不含 ε 的符号或扫描到末尾
   3. 如果 $X_1\,X_2\,\cdots\,X_n$ 都可以推出 $\varepsilon$，那么 $\forall\,i,\;FOLLOW(X_i)\;\supseteq\;FOLLOW(A)$
   4. 若扫描到末尾，则把 FOLLOW(A) 并入 FOLLOW($X_n$)，也就是说末尾的非终结符总是包含 FOLLOW(A)

计算流程

1. 遍历每个产生式，对产生式右边的非末尾符号，加入下一个符号的 FIRST，对于末尾符号，加入 FOLLOW(A)
2. 如果

### 3.3 SELECT

意义：对于非终结符 A 和输入符号 a，只要 a 在 SELECT(A→α)，就可以决定选择产生式 A→α

![image-20250622144320495](https://dasi-blog.oss-cn-guangzhou.aliyuncs.com/Compile/202506221443541.png)

### 3.4 LL(1) 

#### 3.4.1 含义

- L：使用自顶向下的、基于最**左**推导的解析方法
- L：解析过程只需要从**左**到右扫描输入符号串
- 1：只需要向前看 **1** 个输入符号就能唯一确定下一步应使用哪条产生式
- 充要条件是**对每个非终结符的不同产生式，其 SELECT 集必须互不重叠**

#### 3.4.2 预测分析表

- 行对应非终结符，列对应终结符
- M[A,a] 的值表示是当非终结符 A 面临输入符号 a 时应该选择的产生式
- 对于 SELECT(A→α) 中的每个终结符 $a$，将产生式 A→α 放入 M[A, a] 中

#### 3.4.3 解析过程

4. 初始化：在栈底放入文件结束符 $，在栈顶放入起始符 S
2. 从栈顶弹出一个符号 A，获取当前输入符号 a
    1. 如果 A 是终结符：如果 A 与 a 一样，则消费 a 并继续，否则报错
    2. 如果 A 是非终结符：如果查表 M[A,a] 存在对应的产生式 A→α，将 α 逆序放入栈中，否则报错
3. 重复上述步骤，当且仅当栈空并且输入字符串全部被消费，才接受输入字符串，否则报错

![image-20250622145022303](https://dasi-blog.oss-cn-guangzhou.aliyuncs.com/Compile/202506221450415.png)

|step|stack|input|top|lookahead|action|
|-|-|-|-|-|-|
|1|\$E      |n+n*n\$|E  |n  |输出 $E \to TE'$，压入 E'T|
|2|\$E'T    |n+n*n\$|T  |n  |输出 $T \to FT'$，压入 T'F|
|3|\$E'T'F  |n+n*n\$|F  |n  |输出 $F \to n$，压入 n|
|4|\$E'T'n  |n+n*n\$|n  |n  |消费 n｜
|5|\$E'T'   |+n*n\$ |T' |+  |输出 $T'\to\varepsilon$|
|6|\$E'     |+n*n\$ |E' |+  |输出 $E'\to +TE'$，压入 E'T+|
|7|\$E'T+   |+n*n\$ |+  |+  |消费 n|
|8|\$E'T    |n*n\$  |T  |n  |输出 $T \to FT'$，压入 T'F|
|9|\$E'T'F  |n*n\$  |F  |n  |输出 $F\to n$，压入 n|
|10|\$E'T'n |n*n\$  |n  |n  |消费 n|
|11|\$E'T'  |*n\$   |T' |*  |输出 $T' \to \text{*}FT'$，压入 T'F\*|
|12|\$E'T'F*|*n\$   |*  |*  |消费 *|
|13|\$E'T'F |n\$    |F  |n  |输出 $F\to n$，压入 n|
|14|\$E'T'n |n\$    |n  |n  |消费 n|
|15|\$E'T'  |\$     |T' |\$ |输出 $T'\to\varepsilon$|
|16|\$E'    |\$     |E' |\$ |输出 $E'\to\varepsilon$|
|17|\$      |\$     |\$ |\$ |消费 \$|
|18|null    |null   |-  |-  |Accpet|

#### 3.4.4 恐慌模式

恐慌模式是一种**错误恢复策略**，当分析器遇到语法错误时，不尝试精确修复错误，而是持续读取并丢弃输入符号，直到遇到预先设定的同步标记，然后恢复正常分析
1. 对于 a∈FOLLOW(A)，预测分析表中 M[A, a] 处均填写同步符号 synch
2. 如果 M[top, lookahead] == empty，则跳过 lookhead 字符，栈保持不变
3. 如果 M[top, lookahead] == synch，则跳过栈顶，lookhead 字符不变
4. 如果 top != lookahead，则跳过栈顶，lookhead 字符不变

![image-20250622145152163](https://dasi-blog.oss-cn-guangzhou.aliyuncs.com/Compile/202506221451216.png)



## 4. 自底向上分析

### 4.1 算符优先归约

算符文法：任一产生式的右部都不含两个相邻的非终结符

算符优先：只考虑终结符之间的优先关系，来决定是执行归约还是执行移进

算符优先归约：取栈的第一个终结符 a，与输入终结符 b 进行比较

- 如果 a < b 或 a = b，执行移进，将 b 推入栈并消耗输入
- 如果 a > b，执行归约，从栈顶向左找到第一个终结符 c 满足 c < a，将 c 右侧到栈顶这一部分作为最左素短语规约成一个非终结符

![image-20250622145442082](https://dasi-blog.oss-cn-guangzhou.aliyuncs.com/Compile/202506221454164.png)

### 4.2 LR(0)

#### 4.2.1 含义

- L：从左到右扫描输入串
- R：最左归约
- 0：向前查看输入符号串的个数
- 可行前缀：那些在自底向上解析时，既不会跳过还没归约的句柄，也不会超出规约边界，分析器栈上合法出现的所有符号的串

#### 4.2.2 项目

**拓广文法**：添加加一个新的开始符号 $S’：S’ \;\to\; S$，为了让规约回原始开始符号时有个专用产生式来标志做完了，便于在解析表里定义 accept 动作

**项目**：是带点 $\bullet$ 的产生式，是 LR(0) 分析的最小单位，形如 $A \;\to\; \alpha\,\bullet\,\beta$，左侧 $\alpha$ 表示已归约或已移进到栈，右侧 $\beta$ 表示还没处理的输入

- 移进项目：$A \;\to\; \alpha\;\bullet\;a\;\beta$，$a$ 是终结符，表明把 $a$ 移进栈
- 待约项目：$A \;\to\; \alpha\;\bullet\;B\;\beta$，$B$ 是非终结符，表明表示对 A 的归约需要先归约 B
- 归约项目：$B \;\to\; \gamma\;\bullet$，$\gamma$ 是符号串，表明句柄已形成，可以进行将 $\gamma$ 归约到 $B$
- 接受项目：$S’ \;\to\; S\;\bullet$，表明输入串可归约为文法开始符，分析结束

**核**：所有形如 $A\to\alpha\bullet X\beta$  的项目，也就是点号不在最左边的项目

**Closure(I)**：给定一个项目集合，自动补**所有可能马上要派上用场**的项目

1. I 的项目均在 Closure(I) 中
2. 若 $A\to\alpha\;\bullet\;B\beta\in I$ 且 $B$ 是非终结符，则把所有产生式 $B\to\gamma 对应的 B\to\bullet\gamma$ 加进 $I$
3. 重复 2 直到 CLOSURE(I) 不再扩大为止

**GOTO(I, X)**：描述如果在状态 I 看到了某个符号 X，该跳到哪个下一个状态

1. 先把所有点在 X 前面的项目滑过 X，表示移进或归约了 X，$I' = \{\,A\to\alpha\,X\bullet\,\beta \mid A\to\alpha\bullet X\beta\in I\}$
2. 再对新项目集做闭包，补齐新状态内所有待展开的 $B\to\gamma$ 项，$\mathrm{GOTO}(I, X) = \mathrm{Closure}(I')$

#### 4.2.3 构造 DFA

1. 从拓广文法出发，拿初始项集 $I_0 = \mathrm{Closure}(\{S’\to\bullet S\})$
2. 对每个符号 X 调用 $\mathrm{GOTO}(I_0,X)$ 得到新集 $I_1,I_2…$
3. 对新集 $I_1,I_2…$ 做 $\mathrm{GOTO}$​，以此类推直到不再有新集

![image-20250622151143292](https://dasi-blog.oss-cn-guangzhou.aliyuncs.com/Compile/202506221511385.png)

#### 4.2.4 构造分析表

令 i 和 j 为项目下标，以下标代表项目；令 k 是预先给每个产生式的编号，只起到标识作用，无实际意义

1. 如果 $X$ 是终结符，则 $\text{ACTION}[i,X] = j$
2. 如果 $X$ 是非终结符，则 $\text{GOTO}[i,X] = j$
3. 如果  $I_i$ 包含项 $S’ \;\to\; S\;\bullet$​，则 $\text{ACTION}[i,\$] \;=\; \text{accept}$
4. 若 $I_i$ 包含项 $A \;\to\; \gamma\;\bullet$，则对任何终结符 $a$ 都有 $\text{ACTION}[i,a] \;=\; \text{reduce }(k)$
5. 其他格子为空，统一表示 $\text{error}$

![image-20250622151416370](https://dasi-blog.oss-cn-guangzhou.aliyuncs.com/Compile/202506221514467.png)

#### 4.2.5 分析流程

```text
初始化：
	令状态栈 = [S]
	令符号栈 = []
循环：
	取出状态栈顶状态 i
	取出当前输入符号 a
	查询动作 action = ACTION[i,a]
	if action = shift j：
		将 j 入状态栈，将 i 入符号栈
  else if action = reduce k：
  	将归约式右边的符号弹出，将归约式左边的符号入栈
  	将状态栈中相同数量的状态弹出
  	取出新的状态栈顶状态 t
  	取出新的符号栈顶符号 A
  	查询下一个状态 s = GOTO[t, A]
  	将 s 入状态栈
  else if action = accept:
  	接受
  else:
  	不接受		
```

#### 4.2.6 冲突情况

- 移进-归约冲突：移进项目 $A \;\to\; \alpha\;\bullet\;a\;\beta$  和归约项目 $B \;\to\; \gamma\;\bullet$ 同在一个项目集中，因此当面临输入符 $a$ 时，不能确定是移进 $a$ 还是归约 $\gamma$
- 归约-归约冲突：归约项目 $A \;\to\; \alpha\;\bullet$  和归约项目 $B \;\to\; \beta\;\bullet$ 同在一个项目集中，当面临任意输入符时，不能确定是归约 $\alpha$ 还是归约 $\beta$

### 4.3 变种

#### 4.3.1 SLR(1)

向前看 1 个符号，对于归约项目 $A \;\to\; \alpha\;\bullet$，当且仅当 $a \in \text{FOLLOW(A)}$ 才进行归约

![image-20250622152518659](https://dasi-blog.oss-cn-guangzhou.aliyuncs.com/Compile/202506221525717.png)

#### 4.3.2 LR(1)

向前看 1 个符号，对每个项目，都需要带 1 个具体**前瞻符**，对于归约项目 $A \;\to\; \alpha\;\bullet, \;a$，当且仅当输入字符正好为 $a$ 才进行归约

Closure(I)：若有项 $A\to\alpha\;\bullet\;B\,\beta\,,\,a$，则对文法中每条 $B\to\gamma$ 和每个终结符 $b\in \mathrm{FIRST}(\beta\,a)$ 加入项 $B\to\bullet\,\gamma\,,\,b$，意义在于预先把所有可能马上要遇到的终结符都加进来

![image-20250622153239569](https://dasi-blog.oss-cn-guangzhou.aliyuncs.com/Compile/202506221532737.png)

#### 4.3.3 LALR(1)

在 LR(1) DFA 中，若两个状态 $I_p$ 和 $I_q$ 的核完全相同，仅 lookahead 集有区别，就把它们合并成一个 LALR 状态，并把它们的 lookahead 集取并集，如果没有冲突，则是 LALR(1) 文法

![image-20250622153458862](https://dasi-blog.oss-cn-guangzhou.aliyuncs.com/Compile/202506221534039.png)

#### 4.3.4 对比总结

![image-20250622153517575](https://dasi-blog.oss-cn-guangzhou.aliyuncs.com/Compile/202506221535679.png)
