---
title: 词法分析
tags:
  - Compile
categories:
  - 笔记
cover: /image/compile.png
description: 词法分析程序、形式化描述工具（正规文法、正规式、有穷自动机）、转换流程、lex
abbrlink: 55180fbf
date: 2025-03-04 15:33:38
swiper_index: 3
---
<meta name="referrer" content="no-referrer"/>

## 1. 词法分析程序

### 1.1 程序任务

1. 输入：源程序字符流
2. 词法检查：字符流是否符合规范
3. 实现 token 二元组表示：<type, lexeme>
4. 输出：token 序列

### 1.2 Token

Token 用一个二元组 `(Type, Lexeme)` 表示

|Type|Lexeme|定义|
|-|-|-|
|关键字/保留字|本身|是由语言设计者预先定义的、在语言中具有特殊意义的词汇，如 if、while、begin、end 等
|标识符|指向标识符在符号表的入口的指针|用于表示变量、函数等用户自定义的名称，通常由语言设计者规定了构造标准，如只能由字母、数字和下划线构成
|常数|具体数值|程序中的固定值，如整数、浮点数、字符、字符串等
|运算符|本身|用于表达运算、赋值、逻辑判断等操作，如 +、-、*、/
|界符|本身|各种分隔符和括号，如分号、逗号、括号、花括号等
|空白符|忽略|空格、制表符、换行符|

![image-20250622140205627](https://dasi-blog.oss-cn-guangzhou.aliyuncs.com/Compile/202506221402747.png)

### 1.3 程序流程

1. 获取源代码字符流中的下一个字符
2. 识别并过滤掉空白：跳过**空格、制表符、换行符**等非实际语义的空白字符
3. 识别关键字或标识符：如果当前字符是字母，则将它以及后续的字母和数字存入缓冲区，**直到遇到字母/数字字符为止**，构成一个完整的字符串
4. 识别数字：如果当前字符是数字，则持续读入连续的数字字符，**直到遇到非数字字符为止**，将得到的字符串转移为整数
5. 识别运算符或界符：如果是多字符组合，需要**读取下一个字符以判断是否匹配**，否则只识别单字符符号
6. 如果当前字符不符合上述五个大类中的任何一种，则认为它是**未知或非法**的单词，进行错误处理或报告
7. 根据识别的单词，设置全局变量

![](https://dasi-blog.oss-cn-guangzhou.aliyuncs.com/Compile/202503051510269.png)

## 2. 形式化描述工具

### 2.1 正规文法

正规文法：要求文法 $G = (V_N,V_T,S,P)$ 中的规则满足右线性形式：$A \to a$ 或 $A \to aB$，其中 A 和 B 是非终结符，a是终结符

![](https://dasi-blog.oss-cn-guangzhou.aliyuncs.com/Compile/202503051510268.png)

### 2.2 正规式

正规式是描述正规集的工具，用于构造复杂的字符串模式
- 连接：$ab$ 表示字符 a 后紧跟 b
- 并集：$a|b$ 表示字符 a 或 b
- 闭包：$a^*$ 表示**零个或多个**字符 a
- 正闭包：$a^+$ 表示**一个或多个**字符 a

代数规律

- 并集的交换律：$r | s = s | r$
- 并集的可结合律：$r | (s | t) = (r | s) | t$
- 并集的抽取律：$r | r = r$
- 并集的吸收率：$R | S = S$ 当且仅当 $R \subseteq S$
- 连接的可结合律：$(rs)t = r(st)$
- 连接的恒等律：$\varepsilon r = r, r\varepsilon = r$
- 并集和连接的分配律：$r(s | t) = rs | rt, (s | t)r = sr | tr$
- 闭包的幂等律：$(r^*)^* = r^*, r^*r^* = r^*$
- 闭包的递归律：$r^* = \varepsilon | rr^*$

![](https://dasi-blog.oss-cn-guangzhou.aliyuncs.com/Compile/202503051510267.png)

### 2.3 正则表达式

- \s：任何空白字符
- \S：任何非空白字符
- \d：任何数字字符
- \D：任何非数字字符
- \w：任何单词字符（字母+数字+下划线）
- \W：任何非单词字符
- a：单个字符 a
- ab：a 后紧跟 b
- a|b：a 或 b
- $a^*$：零个或多个字符 a
- $a^+$ ：一个或多个字符 a
- .：任何字符
- \\.：点字符
- [a,b,c]：a 或 b 或 c
- [a-z]：a 到 z
- [0-9]：0 到 9
- [ ^a ]：除了 a

等价表达

- $b(ab)^* = (ba)^*b$
- $(a|b)* = (a^*b^*)^*$

常见表达

- 标识符：`[A-Za-z_][A-Za-z0-9_]*`
- 十进制数：`0|([1-9][0-9]*)`

### 2.4 有穷自动机

五元组表示 $M = (S, \Sigma, \delta, q_0, F)$

- $S$：有穷状态集合，每个状态用单边框圆形表示
- $\Sigma$：输入字母表
- $\delta$：转换函数，输入前置状态和字母，给出后继状态
- $q_0$：初始状态，用一个箭头指向圆形
- $F$：终止状态集合，每个状态用双边框圆形表示

![](https://dasi-blog.oss-cn-guangzhou.aliyuncs.com/Compile/202503051510263.png)

DFA

- 每个状态对于每个输入只对应一个转换
- 没有空转换
- 只有一个 moves 序列，没有到达则不被接受
- 空间复杂度 $O(2^N)$，因为 $N$ 个状态的 NFA 的理论子集个数有 $2^N$ 个
- 时间复杂度 $O(n)$，因为每个输入只对应一个转换

![image-20250622140954372](https://dasi-blog.oss-cn-guangzhou.aliyuncs.com/Compile/202506221409419.png)

NFA

- 每个状态对于每个输入可对应多个转换
- 有空转换
- 有多个 moves 序列，只要有一个到达则被接受
- 空间复杂度 $O(N^2)$，因为最坏情况下每个状态都可以连到其他状态
- 时间复杂度 $O(n*N^2)$，因为最坏情况下每个输入都需要对 N 个状态遍历所有边

![image-20250622141002564](https://dasi-blog.oss-cn-guangzhou.aliyuncs.com/Compile/202506221410729.png)



## 3. 转换流程

![](https://dasi-blog.oss-cn-guangzhou.aliyuncs.com/Compile/202503111049547.png)

### 3.1 正规文法 --> 正规式

- $A \to xB, B \to y$ 变为 $A = xy$
- $A \to xA|y$ 变为 $A = x^*y$
- $A \to x, A \to y$ 变为 $A = x|y$

![](https://dasi-blog.oss-cn-guangzhou.aliyuncs.com/Compile/202503051510265.png)

### 3.2 正规式 --> NFA

Thompson 构造算法

- 对于正规式$\varepsilon$，构造$x \xrightarrow{\varepsilon} y$
- 对于正规式$a$，构造$x \xrightarrow{a} y$
- 对于正规式$r=s|t$，构造$x \xrightarrow{\varepsilon} N(s) \xrightarrow{\varepsilon} y$ 和$x \xrightarrow{\varepsilon} N(t) \xrightarrow{\varepsilon} y$
- 对于正规式$r=st$，则将$N(s)$ 的终态和$N(t)$ 的初态相结合
- 对于正规式$r=s^*$，构造$x \xrightarrow{\varepsilon} N(s) \xrightarrow{\varepsilon} y$ 和$x \xrightarrow{\varepsilon} y$ 以及$N(s) \xrightarrow{\varepsilon} N(s)$（从终态指向初态）

 $r=(a|b)^*abb$

![](https://dasi-blog.oss-cn-guangzhou.aliyuncs.com/Compile/202503051510247.png)

### 3.3 NFA --> DFA

概念

- I 是 NFA 中的状态集合
- ε-closure (I) 是 I 中任何状态 S 经过任意条 ε 弧能到达的状态集合
- move (I, a) 是 I 中任何状态经过一条 a 弧能到达的状态集合

![](https://dasi-blog.oss-cn-guangzhou.aliyuncs.com/Compile/202503111025207.png)

子集构造算法

1. 计算 NFA 初始状态的 ε-closure (S) 作为 DFA 的初始状态 S，作为未标记的状态加入 DFA 中
2. 如果 DFA 中存在没有被标记的状态 T，对每个输入符号 a，计算 move (T, a)
3. 计算 U = ε-closure (move (T, a))
4. 如果 U 没有出现在 DFA 中，则将 U 作为未标记的状态加入 DFA 中
5. 重复 2-4，直到没有新的状态集合被发现为止

![](https://dasi-blog.oss-cn-guangzhou.aliyuncs.com/Compile/202503051510259.png)

### 3.4 DFA --> 简化 DFA

- 等价条件

  - 一致性条件：状态 s 和 t 必须同时为可接受状态或不可接受状态

  - 蔓延性条件：对于所有输入符号，状态 s 和 t 必须转移到等价状态

- 分割子集法

  1. 将状态集合分为两个子集，一个由接受态组成，一个由不可接受态组成
  2. 对每个子集，若其内部状态对于某个输入符号的转移结果落在不同子集，则将原子集分割
  3. 不断分割，直到最后不可分割的子集内的状态可以合并

  ![](https://dasi-blog.oss-cn-guangzhou.aliyuncs.com/Compile/202503051510257.png)

### 3.5 DFA --> Table-driven

![](https://dasi-blog.oss-cn-guangzhou.aliyuncs.com/Compile/202503111057980.png)

```c
// 状态编码
enum State { S = 0, T = 1, U = 2, NUM_STATES };

// 输入符号编码
int symbolOf(char c) {
    return (c == '0') ? 0
         : (c == '1') ? 1
         : -1;  // 非法输入
}

// 转移表 next[state][symbol]
int next[NUM_STATES][2] = {
    //  0     1
    {   T,    U   },  // from S: on '0'→T, on '1'→U
    {   T,    U   },  // from T: on '0'→T, on '1'→U
    {   T,    U   }   // from U: on '0'→T, on '1'→U
};

// 接受态表
bool isAccept[NUM_STATES] = {
    false,   // S 不是接受态
    false,   // T 不是接受态
    true     // U 是接受态
};

// 转移函数
bool runDFA(const char *input) {
    State st = S;
    for (const char *p = input; *p; ++p) {
        int sym = symbolOf(*p);
        if (sym == -1) {
            return false;
        }
        st = next[st][sym];
    }
    return isAccept[st];
}
```



## 4. lex

### 4.1 概述

自动构造工具：是一类利用形式化描述如正规表达式自动生成程序的工具，也就是说，**用户只需要用正规表达式描述单词模式，自动构造工具就可以自动生成用于词法分析的代码**

lex：读入用户编写的一个 `lex.l` 的描述文件，生成一个名为 `lex.yy.c` 的 C 源程序文件，其中包含函数 `yylex()`，用于读取源程序的字符流，并返回下一个 Token

![](https://dasi-blog.oss-cn-guangzhou.aliyuncs.com/Compile/202503051510243.png)

全局变量

- yytext：指向当前 token 的指针
- yyleng：当前 token 的长度
- yylineno：当前 token 所在的行号
- yyin：输入文件指针
- yyout：输出文件指针

lex 的正规表达式匹配原则

1. **最长匹配**：如果有多个正规表达式都能匹配当前输入的一部分，则 Lex 会选择**匹配字符数最多**的那个规则
2. **顺序匹配**：如果存在两个或多个规则匹配同样长度的字符串，则 Lex 会选择**在描述文件中先出现**的规则

### 4.2 构建流程

1. 首先为每个正则式各自利用 Thompson 构造成一个 NFA $N_i$，并在它的接受状态上标记这是“第 i 个 token”
2. 在所有这些 $N_i$ 前再插一个新起始状态 $q_0$，从它到每个 $N_i$ 的原始起始状态各加一条 $\varepsilon$ 边
3. 把这个合并后的 NFA 进行一次 NFA→DFA →最小化→转移表的转换，并且把各个模式的接受状态标签都带了过来
4. 当 DFA 在某个接受状态集合里同时包含多条标签，Lex 会依据“定义顺序”或“最长匹配”规则来决定到底归哪种 Token
5. 运行时，Lex 只维护一个 DFA 转移表，每读一字符就查转移表，从不回头，一旦走不动了，就退回到最后的接受状态，把那段字符切成一个 Token，重置到起始状态，继续扫描下一个

### 4.3 扫描流程

假设有两个 pattern：ID = [A-Za-z]+ 和 NUM = [0-9]+；输入流是：abc123xyz

1. Lex 一开始在起始态，读 a→跳到 ID 状态（接受态），记下“位置1可接受”；
2. 读 b→仍在 ID 接受态，记“位置2可接受”；
3. 读 c→记“位置3可接受”；
4. 读 1→没法在 ID 上跳，因为 1 不是字母，Lex 走不动了；
5. 回退输入指针到 1，相当于撤销对 1 的“读入”操作，使 1 还在输入缓冲区，没有被消费；
6. 切出 abc 作为一个 ID token；
7. 重置 Lex 回到起始态，开始下一个 token 的扫描，从 1 重新扫描；
8. 以此类推，得到 (ID, abc), (NUM, 123) 和 (ID, xyz) 三个 token

### 4.4 描述文件

lex 描述文件：描述各种单词的模式，并为每种模式指定对应的 C 语言动作代码，每个部分之间用 `%%` 分割

1. **定义部分**：设定词法分析器的全局环境和基础配置
   - C 部分：包含在 %{ ... %} 中
     - 头文件：如 `#include <stdio.h>`
     - 全局变量声明：如 `int num_lines=0;`
     - C 中的宏定义：如 `#define ADDCOL() Column += yyleng;`
   - lex 部分
     - lex 中的宏定义：如 `D  [0-9]`
     - 选项：如 `%option noyywrap` 表示不自动调用 `yywrap()`
     - 起始条件声明：如 `%x COMMENT`

2. **规则部分**：定义了词法分析器如何从输入中识别各类单词，同时应该作出什么反应，格式通常为 `正则表达式 {动作代码}`
   - 正则表达式：如 `"if"` 或 `[ \t\n]`
   - 动作代码：如 `{ return IF; }` 或 `{ return ~YYEOF; }`

3. **辅助代码部分**：实现了词法分析器的运行入口及相关功能，可以配合后续语法分析器使用
   - 主函数：用于启动词法分析，如`int main() { yylex(); return 0; }`
   - 自定义 lex 函数：如 `yywrap()` 或 `yyerror()`
   - 自定义辅助函数：通常用于打印调试信息

> `~YYEOF` 是一个特殊的返回值，用来表明匹配到了无效字符，从而让词法分析器忽略当前匹配，继续扫描下一个 token

### 4.5 使用案例

1. 编写 lex 描述文件命名为 `mylexer.l`
2. `$ lex mylexer.l`：生成 lex C 源程序文件 `lex.yy.c`
3. `$ gcc lex.yy.c -ll -o mylexer`：链接 lex 库，生成可执行文件 `mylexer`
4. `./mylexer < input.txt`：传递输入文件，执行可执行文件

```lex
%{
#include <stdio.h>
#include <stdlib.h>
int num_lines = 1;
int num_chars = 0;
int num_numbers = 0;
%}
%option noyywrap
%%
\n             { ++num_lines; ++num_chars; }
[ \t]+         { num_chars += yyleng; }
[0-9]+         { ++num_numbers; printf("Number: %s\n", yytext); num_chars += yyleng; }
[a-zA-Z]+      { printf("Word: %s\n", yytext); num_chars += yyleng; }
.              { ++num_chars; }
%%
int main(void) {
    yylex();
    printf("\nLines: %d, Characters: %d, Numbers: %d\n", num_lines, num_chars, num_numbers);
    return 0;
}
```

输入文本
```txt
Hello world！
Here is dasi aged 21
1 + 2 = 3
```

输出结果
```
Word: Hello
Word: world
Word: Here
Word: is
Word: dasi
Word: aged
Number: 21
Number: 1
Number: 2
Number: 3

Lines: 3, Characters: 45, Numbers: 4
```