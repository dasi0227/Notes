---
title: 排序
tags:
  - Algorithm
categories:
  - 算法
cover: /image/algorithm.png
abbrlink: 57fa915c
date: 2024-10-14 22:35:45
description:
---
<meta name="referrer" content="no-referrer"/>

## 1. 基础排序

{% note success flat %}
循环不变式满足三条性质
1. **初始：第一次迭代之前，循环不变式为真**
2. **保持：如果当次迭代前循环不变式为真，那么下次迭代前循环不变式依旧为真**
3. **终止：当循环终止时，循环不变式提供了一个有用的性质**
循环不变式的意义：**终止情况一定是结果情况，尝试找到一个初始情况和循环操作，使得每次迭代，保持某一段为真，并逐渐扩展该段，直到该段是整段**
{% endnote %}

### 1.1 插入排序

原理：**将每个元素都放到“比左边元素大，比右边元素小”的位置上**

循环不变式：数组的前i个元素（数组下标从0到i-1）都是排序好的
1. 初始：从i=1开始，此时之前只有一个元素即A[0]，肯定是排序好的
2. 保持：由于从0到i-1都是排序好的，所以肯定存在一个下标j使得`A[j]<=A[i]<=A[j+1]`，将A[j+1]、A[j+2]、...、A[i-1]向右平移，然后将A[i]的值插入到A[j+1]，即可使得从0到i都是排序好的
3. 终止：i等于数组长度

```python
def INSERT_SORT(array):
  for i in range(1,len(array)):
    j = i - 1
    while j >= 0 and array[j] > array[i]:
      array[i],array[j] = array[j],array[i]
      i = j
      j = i - 1
```

### 1.2 选择排序

原理：**选择每一段数组的最大元素放到数组末尾**

循环不变式：数组i之后的元素都是排序好的，n是数组长度
1. 初始：从i=n-1开始，此时i后的元素为空，是平凡排序好的
2. 保持：由于数组i之后元素是排序好的，即它们肯定比从0到i的任何元素都大，所以只需要找到这部分的最大值，将其与A[i]互换，即可使的i-1后的元素都是排序好的
3. 终止：i=0，此时只剩一个最小的元素正好在第一位，循环终止

```python
def SELECT_SORT(array):
  for i in range(len(array)-1,0,-1):
    max_index = 0
    for j in range(i+1):
      if array[j] > array[max_index]:
        max_index = j
    array[i],array[max_index] = array[max_index],array[i]
```

### 1.3 冒泡排序

原理：**每次都将相邻元素的较大值放到后面**

循环不变式：**和插入排序是一样的**，但是冒泡排序在遍历每一段数组的过程中，**都将较大元素尽可能往后放，而不是只是找到最大元素的索引**

```python
def BUBBLE_SORT(array):
  for i in range(len(array)-1,0,-1):
    for j in range(i):
      if array[j] > array[j+1]:
        array[j],array[j+1] = array[j+1],array[j]
```

## 2. 分治排序

{% note success flat %}
分治策略本质上就是分和治，分就是**将一个大问题分成多个小问题去解**，治就是**利用多个小问题的解来得出一个大问题的解**，分治策略大体上有以下三个步骤：
1. **分解（Divide）：将问题划分为一些子问题，子问题的形式与原问题完全一样，只是规模更小**
2. **解决（Conquer）：当问题规模足够小时，停止递归，求解出当前子问题**
3. **合并（combine/merge）：将子问题的解组合成原问题的解**
{% endnote %}

### 2.1 快速排序

原理：**将数组根据主元不断分为两部分，其中主元的位置就是最终排序的位置，且主元左边都是比主元小的元素，主元右边都是比主元大的元素，对两边的子数组递归调用排序**

循环不变式：总是取结尾为主元索引pivot，设置两个索引low和high，需要满足**索引比low小的都是小于主元的，索引比high大的都是大于等于主元的**
- 初始：low=0，high=n-2，此时low之前没有元素可认为比主元小，high之后只有主元
- 保持：如果$A[low]>=A[pivot]$，则将low和high的元素互换并将high-1，如果$A[low]<A[pivot]$，则先将low+1
- 终止：当$low=high$时，将$A[low]$和$A[pivot]$互换，即可实现放置主元于正确位置，且主元左边都比主元小，主元右边都比主元大

```python
def QUICK_SORT(array):
  if len(array) <= 1:
    return
  # 确定主元
  pivot = len(array) - 1
  low = 0
  high = pivot - 1
  # 分区过程
  while low != high:
    if array[low] < array[pivot]:
      low += 1
    elif array[low] >= array[pivot]:
      array[low],array[high] = array[high],array[low]
      high -= 1
  # 将主元放到正确的位置
  array[low],array[pivot] = array[pivot],array[low]
  # 递归排序左侧和右侧
  left = array[:low]
  QUICK_SORT(left)
  right = array[low+1:]
  QUICK_SORT(right)
  # 合并结果
  array[:] = left + [array[low]] + right
```

### 2.2 归并排序

原理：**递归地从中间分解数组，然后再合并排序好的结果**

分治策略：
1. 分解：可以从中间将当前数组分为两个子数组递归
2. 解决：如果当前数组长度为1，无法继续分，也可以认为已经排好序，停止递归，返回该数组
3. 合并：对两个已经排好序的数组，设立两个指针进行遍历，可以很轻松地合并为一个排好序的数组

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

## 3. 堆排序

原理：**将数组构造成最大堆，不断去除并获取堆顶元素放到数组末尾**

实现：详细请看另一篇关于堆的文章

```python
def SORT_MAX_HEAP(heap):
  BUILD_MAX_HEAP(heap)
  sort_heap = [0] * len(heap)
  last = len(heap) - 1
  while last >= 0:
    maxnum = EXTRACT_MAX_HEAP(heap)
    sort_heap[last] = maxnum
    last -= 1
  heap[:] = sort_heap
```

## 4. 线性排序

{% note success flat %}
之前所讨论的排序都是依赖于元素之间的比较，时间复杂度都是$O(nlg(n))$（堆排序、归并排序、快速排序）或$O(n^2)$（插入、选择、冒泡），而线性时间排序的方法是**根据数组中元素的特定属性**，并且**不是原址操作，会牺牲一定空间**
{% endnote %}

### 4.1 计数排序

原理：**对每个元素i，计算小于等于i的元素个数j，则元素i最终的索引就在j-1**

实现：数组满足最小元素是0，最大元素maxnum，且元素都是整数
1. 创建一个长为maxnum+1的数组count，对于count的索引i，count[i]就是i出现在array的次数
2. 对于count的索引i，在数组array中小于等于i的元素个数就是count[0] + coun[1] + ... + count[i]
3. 创建一个临时数组temp，遍历array的元素，根据count将元素放到temp正确的排序位置，然后更新count

```python
def COUNT_SORT(array,maxnum):
  length = maxnum + 1
  count = [0] * (length)
  temp = [0] * len(array)
  for num in array:
    count[num] += 1
  for i in range(1,length):
    count[i] += count[i-1]
  for i in range(len(array)):
    num = array[i]
    index = count[num] - 1
    temp[index] = num
    count[num] -= 1
  array[:] = temp
```

### 4.2 基数排序

原理：从低到高按位排序，假设遍历到第i位，相同数值内的顺序是按照第i-1位的排序情况

实现：给定数组中具有最多位元素的位数maxbit，且元素都是整数
1. 每一位都采用计数排序，当前位的数值等于$array // exp \% 10$
2. 由于上一位已经排序好，所以当前位要从后往前遍历数组，才能保证上一位的排序情况

```python
def RADIX_SORT(array,maxbit):
  exp = 1
  for _ in range(maxbit):
    temp = [0] * len(array)
    count = [0] * 10
    for num in array:
      num = num // exp % 10
      count[num] += 1
    for i in range(1,10):
      count[i] += count[i-1]
    for i in range(len(array)-1,-1,-1):
      num = array[i] // exp % 10
      index = count[num] - 1
      temp[index] = array[i]
      count[num] -= 1
    array[:] = temp
    exp *= 10
```

### 4.3 桶排序

原理：**将数组分为多个连续的区间，区间里面排好序之后再合并**

实现：给定数组中最大的元素maxnum
1. 首先计算足够多的桶的数量并创建桶
2. 遍历数组的元素，用元素大小除以桶的数量可以得到位于哪个桶


```python
def BUCKET_SORT(array,maxnum):
  size = maxnum // len(array) + 1
  buckets = [[] for _ in range(size)]
  for num in array:
    index = num // size
    buckets[index].append(num)
  for i in range(len(buckets)):
    buckets[i].sort()
  temp = []
  for bucket in buckets:
    temp += bucket
  array[:] = temp
```

## 5. 区别分析

性质
- **时间复杂度**：平均（随机情况）、最好（已经排好序）、最坏（完全逆序或其他特殊情况）
- **稳定性**：在排序过程中，相等的元素相对位置是否保持不变
- **数据情况**：数量情况，原始排序情况，数值情况

|排序|平均时间|最坏时间|最好时间|稳定性|数据情况|
|-|-|-|-|-|-|
|插入|O(n²)|O(n²)|O(n)|稳定|数据量小，基本有序|
|选择|O(n²)|O(n²)|O(n²)|不稳定|数据量小，需要最值|
|冒泡|O(n²)|O(n²)|O(n)|稳定|数据量小，基本有序|
|快速|O(n log n)|O(n²)|O(n log n)|不稳定|数据量大，乱序|
|归并|O(n log n)|O(n log n)|O(n log n)|稳定|数据量大，外部排序|
|堆|O(n log n)|O(n log n)|O(n log n)|不稳定|数据量大且需要最值|
|计数|O(n + k)|O(n + k)|O(n + k)|稳定|数据范围有限且是整数时，大量重复元素|
|基数|O(nk)|O(nk)|O(nk)|稳定|数据范围有限且数据较大时|
|桶|O(n + k)|O(n²)|O(n + k)|稳定|数据均匀分布|