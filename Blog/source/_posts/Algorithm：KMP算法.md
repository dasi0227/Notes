---
title: KMP算法
tags:
  - Algorithm
categories:
  - 算法
cover: /image/algorithm.png
description: 从根本理解KMP算法，详细分析了最大公共前后缀长度
abbrlink: 2da0528d
date: 2023-10-14 12:55:17
---
<meta name="referrer" content="no-referrer"/>

## 1. 什么是最大公共前后缀长度

**一个串的前后缀**
- 前缀是指以串第一个字符开头且不包含最后一个元素的连续的子串
- 后缀是指以串最后一个字符结尾且不包含第一个元素的连续的子串

> <font color="deepskyblue">假设设串为ABCDEFGH，则前缀有A,AB,ABC等，后缀有H,GH,FGH等</font>

**一个串的公共前后缀**：如果前缀集合与后缀集合中存在一个相同的元素，即存在一个子串，它既可以是前缀也可以是后缀，则称这个子串为该串的公共前后缀

> <font color="deepskyblue">假设串为AB_CSDN_AB，则公共前后缀有AB</font>

**最大公共前后缀长度**：一个串的公共前后缀不一定只有一个，其中最长的公共前后缀的长度称为最大公共前后缀长度

> <font color="deepskyblue">假设串为ABA_CSDN_ABA，则公共前后缀有A,AB，即最大公共前后缀长度=3 (ABA)</font>

## 2. 为什么要找最大公共前后缀长度

假设文本串是`ABA_ABAY_CD`，模式串是`ABA_ABAX_CD`，用模式串去匹配文本串

首先要理解匹配的本质是：<font color="orangered">不断改变文本串头部（可以是一个字符，也可以是一个子串），直到满足从该头部开始，接下来的字符与模式串完全相同</font>
- 暴力：头部只有一个字符，一个字符一个字符地遍历文本串，发现匹配错误时，令模式串指回头部，令文本串指回原先的头部+1，再重新开始比较
- KMPSearch：头部是一个子串，一个子串一个子串地遍历文本串

在模式串的X位置之前的子串ABA_ABA中，我们可以找到最大公共前后缀ABA，它对应的长度是k=3，则代表：<font color="orangered">模式串X位置之前的k个元素和模式串的前k个字符是完全相同的</font>

> <font color="deepskyblue">注意“模式串X位置前的k个元素”和“模式串的前k个元素”的两个“前”的差别</font>

既然已经匹配到Y了，说明：<font color="orangered">文本串Y位置之前的k个元素 == 模式串X位置之前的k个元素 == 模式串的前k个元素</font>

相当于已经找到了一个新的头部：<font color="orangered">文本串Y位置之前的k个元素构成的子串，正好对应模式串的头部</font>

因此：<font color="orangered">文本串从Y开始即不动，模式串从第k个元素开始，重新开始匹配</font>

> <font color="deepskyblue">KMP算法：找到模式串每一个位置的最大公共前后缀长度，在匹配失败的时候，移动模式串的头指针，保持文本串的头指针不动</font>

## 3. 如何求最大公共前后缀长度

1. 初始化
  - 模式串为`char p[length]`
  - 每个位置的最大公共前后缀长度为`int [length]`
  - 模式串p的遍历指针`i`，p[i]代表新匹配的元素
  - 当前最大公共前后缀长度为`k`，p[k]代表<font color="orangered">公共前缀的下一个元素（因为序号从0开始）</font>
  - <font color="orangered">从changdu[0] = 0，i=1，k=0开始遍历模式串p</font>

2. 遍历
- **p[i] == p[k]**：新添加的元素等于当前最大公共前缀的后一个元素，
  - 此时<font color="orangered">新的后缀与新的前缀又相同了</font>
  - 最大公共前后缀长度加1，即<font color="orangered">changdu[i] = ++k</font>

- **p[i] != p[k]**：新添加的元素不等于当前最大公共前缀的后一个元素
  - 原先的公共前后缀被破坏，不再成立，需要找到一个更短的最大公共前后缀
  - 不断找<font color="orangered">公共前后缀的公共前后缀，即`k = changdu[k-1]`</font>

- **k==0**：无法继续递归，直接令`changdu[i] == k`

> ABABCABAB的changdu = [0, 0, 1, 2, 0, 1, 2, 3, 4]

## 3. 代码

### 3.1 getChangdu函数

```cpp
void getChangdu(char* p,int changdu[],int length) {
  changdu[0] = 0;
  int i = 1,k = 0;
  while (i < length) {
    if (p[i] == p[k]){
      changdu[i] = ++k;
      i++; 
    } 
    else if (k == 0){
      changdu[i] = k;
      i++; 
    }
    else
      k = changdu[k-1];
	}   
}
```
### 3.2 getNext函数：

```cpp
void getNext(int *next,int *changdu,int length){
	int temp[length];
	for (int i=0;i<length;i++)
		temp[i] = changdu[i];
	for (int i=1;i<length;i++)
		next[i] = temp[i-1];
	next[0] = -1;
}
```

### 3.3 KMPSearch

```cpp
int KMPSearch(char* maistr,char* substr,int length1,int length2,int* next) {
	int i=0,j=0;
	while (i<length1 && j < length2)
		if (j == -1 || maistr[i] == substr[j]){
			i++;j++;
		} 
		else
			j = next[j];
	if (j == length2)
		return i-length2;
	else 
		return -1;
}
```

> <font color="deepskyblue">因为进行KMPSearch时，进行到模式串p的位置i时，向右移动的距离实际上是changdu[i-1]，因此我们只需要将原来的changdu数组右移，并初始化changdu[0] = -1即可</font>
> 因此可以将getChangdu和getNext合二为一，具体的可以参考下面给出的链接：https://blog.csdn.net/v_JULY_v/article/details/7041827

