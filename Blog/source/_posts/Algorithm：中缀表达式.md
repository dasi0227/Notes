---
title: 中缀表达式计算
tags:
  - Algorithm
categories:
  - 算法
cover: /image/algorithm.png
description: 自定义符号函数，轻松解决中缀表达式的计算
abbrlink: 508b8581
date: 2024-08-31 17:03:37
---
<meta name="referrer" content="no-referrer"/>

## 1. 基础概念

栈：**先进后出**的数据结构

中缀表达式：运算符位于数字之间的表达式，如22+33、1+2*(3+6/2-2)+6

前提：输入保证除数不为0，且各运算结果都为整数，除了第一个数之外不存在负数

## 2. 方法

需要两个栈：**符号栈symbol**和**数值栈number**，顾名思义用来存运算符和运算数

输入：表达式的长度n和表达式的字符序列

输出：运算结果

过程：根据各个符号进行操作，然而<font color="orangered">每个符号对应的操作内容都是相同</font>的，因此可以自定义一个符号函数，再用<font color="orangered">if语句设置每个符号的执行条件</font>即可

1. 用string类型记录表达式中的字符

2. 循环遍历字符串，分析各个字符的情况

3. 若是数字字符（ASCII码在48到57之间）
   1. 如果是一位数，直接入数值栈，用字符-48即可
   2. 如果是多位数，用temp记录数值，不断乘10再与下一位相加，直到遇到非数字字符

4. 若是符号字符
   1. 如果是' ( '，则直压入符号栈
   2. 如果是' ) '，调用”符号函数”，直到遇到' ( '，并最后弹出' ( '
   3. 如果是加减号，调用“符号函数”，直到符号栈为空或遇到' ( '
   4. 如果是乘除号，调用“符号函数”，直到符号栈为空或符号栈顶非乘除号

5. 遍历完字符串后，将符号栈剩余的元素依次调用“符号函数”，直到符号栈为空

6. 最后数值栈的栈顶元素即为中缀表达式的运算结果

## 3. 符号函数
1. 无返回值，传参为两个栈symbol和number
2. 首先得到数值栈头部两个元素num1，num2
3. 其次用switch-case结构分支符号栈顶元素对应的不同运算操作，即基本的加减乘除，得到运算结果
4. 最后弹出符号栈的栈顶元素和数值栈的两个栈顶元素，同时压入计算结果到数值栈中

## 4. 注意事项
- 注意符号栈为空的判断条件要置于首位，防止发生下溢情况
- 传参也必须声明stack的数据类型<int>或<char>
- 由于要对传参内容进行修改，需要设置为引用

## 5. 代码

```cpp
//中缀表达式的运算，保证除数不为0且商为整数，除了第一个数不存在负数 
#include <iostream>
#include <stack>
#include <string>
using namespace std;

//符号判断，将一个符号栈顶和两个数值栈顶弹出，得到运算结果压入数值栈 
void fuhao(stack<char> &sym,stack<int> &num){
	int num1 = num.top();
	num.pop();
	int num2 = num.top();
	num.pop();
	int temp;
    switch (sym.top()){
        case '+' : temp = num2 + num1; break;
        case '-' : temp = num2 - num1; break;
        case '*' : temp = num2 * num1; break;
        case '/' : temp = num2 / num1; break;
        default : break;
    }
    sym.pop();
    num.push(temp);
}

int main(){
    string s;
    cin >> s;
    stack<char> symbol;
    stack<int> number;
	number.push(0);// 用来应对第一个数是负数的情况 
    int len = s.length();
    int i=0;
    while (i < len){
    	// 如果是数值，压入数值栈，注意多位数该如何表示 
        if (s[i] > 47 && s[i] < 58){
            int temp = 0;
            while (s[i] > 47 && s[i] < 58){
                temp = temp*10 + s[i] - 48;
                i++;
            }
            number.push(temp);
        }
		// 左括号直接压入符号栈 
        else if (s[i] == '('){
            symbol.push(s[i]);
            i++;
        }
		// 右括号判断符号，直到遇到左括号 
        else if (s[i] == ')'){
            while (1){
            	fuhao(symbol,number);
                if (symbol.top() == '(')
                    break;
            }
            symbol.pop();
            i++;
        }
		// +-判断符号，直到遇到栈为空或者左括号 
        else if (s[i] == '+' || s[i] == '-'){
        	while (1){
        		if (symbol.empty() || symbol.top() == '(')
        			break;
        		fuhao(symbol,number);
			}
			symbol.push(s[i]);
			i++;
		}
		// */判断符号，直到遇到栈为空或者非*/号 
		else if (s[i] == '*' || s[i] == '/'){
        	while (1){
        		if (symbol.empty() || (symbol.top() != '*' && symbol.top() != '/') )
        			break;
        		fuhao(symbol,number);
			}
			symbol.push(s[i]);
			i++;
		}
    }

    // 将符号栈剩余的符号判断 
    while (!symbol.empty())
    	fuhao(symbol,number);
    //最后数值栈顶为中缀表达式运算结果 
    cout << number.top();
    return 0;
}
```

## 6.参考文献

https://blog.csdn.net/waldeinNJU/article/details/108446855