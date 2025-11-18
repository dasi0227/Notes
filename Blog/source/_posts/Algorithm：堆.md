---
title: 堆
tags:
  - Algorithm
categories:
  - 算法
cover: /image/algorithm.png
description: 介绍了堆的数组标识，序号性质，操作，以及堆的经典例题
abbrlink: fab451a5
date: 2024-10-11 11:28:55
---
<meta name="referrer" content="no-referrer"/>

## 1. 堆的数组表示

**堆（Heap）**：是一种特殊的**完全二叉树**，其中**最大堆是指任何父节点的值都大于等于其子节点的值，最小堆是指指任何父节点的值都小于等于其子节点的值**（叶子结点的子结点可以看作成是负无穷）

堆的数组表示：数组的下标可以被看作成是二叉树的结点序号，**二叉树从顶点，自上而下，自左向右进行标号即是对应的数组下标**

![](https://dasi-blog.oss-cn-guangzhou.aliyuncs.com/Algorithm/202410111849061.jpeg)

堆的序号性质：
- 如果二叉树有n个结点且序号从1开始：
  - 最后一个结点的序号是$n$
  - 最后一个叶子结点的序号是$\lfloor n/2 \rfloor + 1$
  - 序号$i$的父结点的序号是$\lfloor i/2 \rfloor$
  - 序号$i$的左子结点序号是$2i$，右子结点序号是$2i+1$
- 如果二叉树有n个结点且序号从0开始：
  - 最后一个结点的序号是$n-1$
  - 最后一个叶子结点的序号是$\lfloor (n-1-1)/2 \rfloor + 1$
  - 序号$i$的父结点的序号是$\lfloor (i-1)/2 \rfloor$
  - 序号$i$的左子结点序号是$2i+1$，右子结点序号是$2i+2$

{% note warning flat %}
代码中由于数组的下标是从0开始，所以我们按照第二种计算方式
理论题数组的下标可能是从1开始，所以要按第一种方式
{% endnote %}

![](https://dasi-blog.oss-cn-guangzhou.aliyuncs.com/Algorithm/202410111849059.jpeg)

## 2. 堆的操作（以最大堆为例）

### 2.1 维护最大堆性质

`MAX_HEAPIFY(heap,i)`：输入数组A和下标i，**其中结点i的所有后代结点都满足最大堆的性质，但是结点i可能不满足最大堆的性质**
- 如果左子结点和右子结点都小于A[i]，说明此时已满足最大堆性质
- 否则选择比A[i]大的子结点（如果左/右子结点都大于A[i]，就选择两者之中的较大值）与A[i]的值交换
- 上述做法可能会改变i的子结点的最大堆性质，因此对i的子结点递归调用

{% note success flat %}
时间分析：因为以子结点为根结点的子树大小至多是2n/3，所以递归式是$T(n) <= T(2n/3) + \Theta(1)$，时间复杂度是$O(lg(n))$
{% endnote %}

```python
def MAX_HEAPIFY(heap,i):
  last = len(heap) - 1
  if i >= (last-1) // 2 + 1:
    return
  root = heap[i]
  left = heap[2*i+1] if 2*i+1 <= last else -float('inf')
  right = heap[2*i+2] if 2*i+2 <= last else -float('inf')
  if root >= left and root >= right:
    return
  elif root < left and left > right:
    heap[i] = left
    heap[2*i+1] = root
    MAX_HEAPIFY(heap,2*i+1)
  elif root < right and right > left:
    heap[i] = right
    heap[2*i+2] = root
    MAX_HEAPIFY(heap,2*i+2)
```

## 3. 建堆

`BUILD_MAX_HEAP`：上述维护堆的前提是结点i的所有后代结点都满足最大堆性质的，因此为了建最大堆，我们要利用**循环不变式，即每一次循环，对于序号i，结点i+1一直到最后一个结点都满足最大堆性质**，所以初始条件我们要**从第一个非叶子结点开始从后往前遍历调用MAX_HEAPIFY**，这是因为**叶子结点始终满足最大堆性质**

```python
def BUILD_MAX_HEAP(heap):
  last = len(heap) - 1
  i = (last-1) // 2
  while i >= 0 :
    MAX_HEAPIFY(heap,i)
    i -= 1
```

## 4. 堆的删除和插入

`EXTRACT_MAX_HEAP(heap)`：删除指的是将堆顶元素去除并返回其值，可以将最后一个结点和栈顶结点互换，然后再删除最后一个结点，这样能保证根结点的所有后代结点都满足最大堆性质，只需要对根结点调用`MAX_HEAPIFY(heap,0)`即可
```python
def EXTRACT_MAX_HEAP(heap):
  last = len(heap) - 1
  heap[0],heap[last] = heap[last],heap[0]
  maxnum = heap.pop()
  MAX_HEAPIFY(heap,0)
  return maxnum
```

`INSERT_MAX_HEAP(heap,key)`：插入指的是将值为key的元素插入到堆中，先将该值插入到堆的最后，然后自底向上不断比较大小，交换父结点和子结点，直到满足最大堆性质或到达根结点
```python
def INSERT_MAX_HEAP(heap,key):
  heap.append(key)
  i = len(heap) - 1
  j = (i-1) // 2
  while j >= 0 and heap[i] > heap[j]:
    heap[j],heap[i] = heap[i],heap[j]
    i = j
    j = (i-1) // 2
```

## 5. 堆排序

`SORT_MAX_HEAP(heap)`：利用最大堆的根结点都是数组的最大值，不断删除根结点，获取每次最大堆的最大值
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

## 6. 经典例题

### 6.1 最大的第K个数

`Kth(heap,k)`：先建堆，然后删除k次堆顶，第k次删除得到的堆顶就是第k个最大元素，需要注意相同值的元素需要跳过
```python
def Kth(heap,k):
  BUILD_MAX_HEAP(heap)
  k_max = -float('inf')
  count = 0
  while count != k:
    temp = EXTRACT_MAX_HEAP(heap)
    if temp != k_max:
      k_max = temp
      count += 1
  return k_max
```

### 6.2 最小的前K个数

`TopK(heap,k)`：不断插入数组元素到最大堆，并且**始终保持最大堆的结点个数只有k个**，一旦超出，就将堆顶结点踢出，遍历完数组后，剩下的K个结点的值就是最小的前K个数
```python
def TopK(heap,k):
  array = []
  for num in heap:
    INSERT_MAX_HEAP(array,num)
    if len(array) > k:
      EXTRACT_MAX_HEAP(array)
  return array
```

## 7. 参考链接

{% link 数据结构-堆的原理和常见算法问题,春水煎茶·王超的个人博客,https://writings.sh/post/data-structure-heap-and-common-problems#%E6%95%B0%E7%BB%84%E8%A1%A8%E7%A4%BA %}