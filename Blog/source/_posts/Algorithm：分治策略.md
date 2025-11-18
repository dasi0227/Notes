---
title: 分治策略
tags:
  - Algorithm
categories:
  - 算法
cover: /image/algorithm.png
abbrlink: 64bcbdce
date: 2024-10-10 11:29:17
description: 介绍分治策略的核心思路，分析若干经典例题
---
<meta name="referrer" content="no-referrer"/>

## 1. 分治策略

分治策略本质上就是分和治，分就是**将一个大问题分成多个小问题去解**，治就是**利用多个小问题的解来得出一个大问题的解**，分治策略大体上有以下三个步骤：
1. **分解（Divide）：将问题划分为一些子问题，子问题的形式与原问题完全一样，只是规模更小**
2. **解决（Conquer）：当问题规模足够小时，停止递归，求解出当前子问题**
3. **合并（combine/merge）：将子问题的解组合成原问题的解**

分治策略的核心是递归，分治的本质是**自己分解自己和自己合并自己**，递归的本质是**自己调用自己并自己处理自己的返回值**，递归过程中存在以下两种情况：
- 递归情况（recursive）：子问题足够大时，无法求解或者很难求解，需要将问题分解为子问题
- 基本情况（base）：子问题足够小时，无法分解或者没必要分解，直接求解子问题

```
分解:
  if 基本情况
    求解
  if 递归情况
    分解
    求解
  合并
```

递归式：$T(n) = aT(n/b) + f(n)$
- T(n)：是当前问题解决所需要的时间
- a：是当前问题分成的子问题的个数
- b：是当前问题分成的子问题的规模
- f(n)：是合并子问题的解所需要的时间

## 2. 归并排序

归并排序，根据分治策略分为以下三步：
1. 分解：可以从中间将当前数组分为两个子数组递归
2. 解决：如果当前数组长度为1，无法继续分，也可以认为已经排好序，停止递归，返回该数组
3. 合并：对两个已经排好序的数组，设立两个指针进行遍历，可以很轻松地合并为一个排好序的数组

递归式：$T(n) = 2T(n/2) + \Theta(n)$

```python
def merge(left,right):
  index1,index2 = 0,0
  len1,len2 = len(left),len(right)
  array = []
  while len(array) != (len1 + len2):
    if index2 == len2 or (index1 != len1 and left[index1] <= right[index2]):
      array.append(left[index1])
      index1 += 1
    elif index1 == len1 or (index2 != len2 and right[index2] < left[index1]):
      array.append(right[index2])
      index2 += 1
  return array

def divide(array):
  if len(array) == 1:
    return array
  mid = len(array) // 2
  left = divide(array[:mid])
  right = divide(array[mid:])
  array = merge(left,right)
  return array
```

## 3. 找到最大子数组

最大子数组指的是子数组的值相加最大，根据分治策略分为以下三步：
1. 分解：可以从中间将当前数组分为左子数组和右子数组递归，此外还有一种情况是跨域中间的子数组
2. 解决：如果当前数组的长度是1，直接返回值，此外还需要计算跨域中间的子数组的最大值
3. 合并：选取左子数组、右子数组和跨越中间的子数组的最大值

{% note warning flat %}
这道题的特殊性在于：**有一种情况是不能递归分解的，需要在当下直接解决**
{% endnote %}

递归式：$T(n) = 2T(n/2) + \Theta(n)$

```python
def merge(sum1,sum2,sum3):
  return max(sum1,sum2,sum3)

def crossmid(array,mid):
  # 初始总值是中间值，左边从mid-1开始遍历，右边从mid+1开始遍历
  l_index,r_index = mid-1,mid+1
  leftsum,rightsum = -float('inf'),-float('inf')
  maxsum = array[mid]
  # 计算从中间开始往左边/右边连续的和的最大值
  cursum = 0
  while l_index != -1:
    cursum += array[l_index]
    if cursum > leftsum:
      leftsum = cursum
    l_index -= 1
  cursum = 0
  while r_index != len(array):
    cursum += array[r_index]
    if cursum > rightsum:
      rightsum = cursum
    r_index += 1
  # 只有左边/右边的值大于0才可能让总值变大
  if leftsum > 0:
    maxsum += leftsum
  if rightsum >0:
    maxsum += rightsum
  return maxsum

def divide(array):
  if len(array) == 1:
    return array[0]
  mid = len(array) // 2
  l_sum = divide(array[:mid])
  r_sum = divide(array[mid:])
  m_sum = crossmid(array,mid)
  sum = merge(l_sum,r_sum,m_sum)
  return sum

array = [13,-3,-25,20,-3,-16,-23,18,20,-7,12,-5,-22,15,-4,7]
maxsum = divide(array)
```

## 4. 矩阵乘法的Strassn算法

{% note warning flat %}
这里要求两个矩阵都是nxn矩阵，而且n都是2的n次幂，即保证n/2是整数
{% endnote %}

Strassen算法的基本步骤如下：
1. **分解矩阵**：
$$
A = \begin{pmatrix}
A_{11} & A_{12} \\
A_{21} & A_{22}
\end{pmatrix}, \quad
B = \begin{pmatrix}
B_{11} & B_{12} \\
B_{21} & B_{22}
\end{pmatrix}
$$
2. **计算中间值**
$$
\begin{align*}
P_1 &= A_{11} \times (B_{12} - B_{22}) \\
P_2 &= (A_{11} + A_{12}) \times B_{22} \\
P_3 &= (A_{21} + A_{22}) \times B_{11} \\
P_4 &= A_{22} \times (B_{21} - B_{11}) \\
P_5 &= (A_{11} + A_{22}) \times (B_{11} + B_{22}) \\
P_6 &= (A_{12} - A_{22}) \times (B_{21} + B_{22}) \\
P_7 &= (A_{11} - A_{21}) \times (B_{11} + B_{12})
\end{align*}
$$
3. **组合结果**
$$
\begin{pmatrix}
C_{11} & C_{12} \\
C_{21} & C_{22}
\end{pmatrix} =
\begin{pmatrix}
P_5 + P_4 - P_2 + P_6 & P_1 + P_2 \\
P_3 + P_4 & P_1 + P_5 - P_3 - P_7
\end{pmatrix}
$$

核心：**减少了一次矩阵乘法，增加常数次矩阵加法**，以此实现更小的时间复杂度，根据分治策略分为以下三步：
1. 分解：将每个大矩阵分成四个角的子矩阵
2. 解决：如果两个矩阵是1x1的，则直接求矩阵成绩
3. 合并：按照Stassen算法将7个解组合成四个角的子矩阵，最后组合成一个结果矩阵

```python
import numpy as np

def merge(P1,P2,P3,P4,P5,P6,P7):
  C11 = P5 + P4 - P2 + P6
  C12 = P1 + P2
  C21 = P3 + P4
  C22 = P5 - P3 - P7 + P1
  # 水平拼接
  top = np.hstack((C11, C12))
  bottom = np.hstack((C21, C22))
  # 竖直拼接
  C = np.vstack((top, bottom))
  return C

def divide(A,B,n):
  if len(A) == 1:
    return A * B
  mid = n // 2
  A11,A12,A21,A22 = A[:mid,:mid],A[:mid,mid:],A[mid:,:mid],A[mid:,mid:]
  B11,B12,B21,B22 = B[:mid,:mid],B[:mid,mid:],B[mid:,:mid],B[mid:,mid:]
  P1 = divide(A11, B12 - B22, mid)
  P2 = divide(A11 + A12, B22, mid)
  P3 = divide(A21 + A22, B11, mid)
  P4 = divide(A22, B21 - B11, mid)
  P5 = divide(A11 + A22, B11 + B22, mid)
  P6 = divide(A12 - A22, B21 + B22, mid)
  P7 = divide(A11 - A21, B11 + B12, mid)
  C = merge(P1,P2,P3,P4,P5,P6,P7)
  return C

A = np.array([[1, 2, 3, 4],
              [5, 6, 7, 8],
              [9, 10, 11, 12],
              [13, 14, 15, 16]])
B = np.array([[1, 0, 0, 0],
              [0, 1, 0, 0],
              [0, 0, 1, 0],
              [0, 0, 0, 1]])
C = divide(A,B,4)
print(C)
```

## 5. 二分查找

根据分治策略分为以下三步：
1. 分解：将数组从中间分为左子数组和右子数组
2. 解决：如果当前数组的长度是1，直接返回数组仅有的元素值
3. 合并：取左子数组的最大值和右子数组的最大值的较大值返回

```python
def merge(num1,num2):
  return max(num1,num2)

def divide(array):
  if len(array) == 1:
    return array[0]
  mid = len(array) // 2
  num1 = divide(array[:mid])
  num2 = divide(array[mid:])
  num = merge(num1,num2)
  return num

array = [1,2,3,4,5,6,7,8,9]
maxnum = divide(array)
```

## 6. 数列的逆序对

根据分治策略分为以下三步：
1. 分解：将数组从中间分为左子数组和右子数组
2. 解决：如果当前数组的长度为1，则返回0，此外还需要计算左数组相较于右数组的逆序对数
3. 合并：将左子数组的逆序对、右子数组的逆序对、左数组相较于右数组的逆序对数相加

```python
def merge(num1,num2,num3):
  return num1 + num2 + num3

def count(array,mid):
  num = 0
  l_index = mid - 1
  while l_index != -1:
    r_index = mid
    while r_index != len(array):
      if array[l_index] > array[r_index]:
        num += 1
      r_index += 1
    l_index -= 1
  return num

def divide(array):
  if len(array) == 1:
    return 0
  mid = len(array) // 2
  l_num = divide(array[:mid])
  r_num = divide(array[mid:])
  m_num = count(array,mid)
  sum = merge(l_num,r_num,m_num)
  return sum

array = [3, 2, 1, 5, 4]
num = divide(array)
```