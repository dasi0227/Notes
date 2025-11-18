---
title: Numpy
tags:
  - DataAnalysis
categories:
  - 笔记
cover: /image/analysis.png
description: 数组属性、数据类型、创建/切片/索引/广播/迭代/变形/连接/分割/翻转/添加/删除操作、字符串/数学/统计学/线性代数/条件筛选运算、随机模块
abbrlink: 3be9a986
date: 2025-04-01 14:30:07
---
<meta name="referrer" content="no-referrer"/>

## 1. NumPy 基础

在 python 中引用 numpy 库格式为 `import numpy as np`，所以本笔记都用 `np` 代替 `numpy`

### 1.1 术语

NumPy 的数组实际上是一个 ndarray 对象，用于存放同类型元素的多维数组，以 0 开始作为索引

维度数量（ndim）：是数组中轴的数量，也称为秩（rank）

轴（axis）是数组中维度的索引
- axis=0：是沿着第一个维度/沿着行的方向，是“跨行/纵向”操作，也就是对每一列进行处理
- axis=1：是沿着第二个维度/沿着列的方向，是“跨列/横向”操作，也就是对每一行进行处理

形状（shape）：是数组在每个维度/轴的大小

### 1.2 数组属性

ndarray 作为对象，具有很多内部属性，这里列出一些常用的属性

|属性|说明|
|-|-|
|ndarray.ndim|数组的维度/秩/轴数|
|ndarray.shape|数组的形状，即数组在每个轴上的大小|
|ndarray.size|数组的元素个数，即每个轴上的大小的累乘|
|ndarray.dtype|数组元素的数据类型|
|ndarray.itemsize|每个元素的字节大小|
|ndarray.flags|包含内存布局的信息|
|ndarray.T|数组的转置属性，返回轴顺序的反转结果|

### 1.3 数据类型

常用的数据类型有：`np.bool`，`np.int32`，`np.int64`，`np.uint16`，`np.float32`，`np.float64`

`np.astype(a, dtype)` 或 `ndarray.astype(dtype)` 可以用于转换数据类型，但是它不是在原对象上进行转换，而是返回一个新的对象
```python
a = np.array([[1,2],[3,4]])
print(np.astype(a, np.bool)) # -> [[True True] [True True]]
print(a.astype(np.float16))  # -> [[1. 2.] [3. 4.]]
```

`np.dtype()` 可以用于结构化数组，传入一个列表，每个元素是一个元组，元组有两个值，原数组的每个元素都按照列表给定的结构来存储多个数据
- 第一个值是字段名称
- 第二个值是字段的数据类型（其中 i 表示 int，b 表示 bool，f 表示 float 等，后跟的数字表示占用内存的字节数量）
```python
student_type = np.dtype([('name','U20'), ('age', 'i1'), ('marks', 'f4')]) 
student = np.array([('abc', 21, 50),('xyz', 18, 75)], dtype = student_type)
print(student['name'])  # -> ['abc' 'xyz']
print(student['marks']) # -> [50.0 75.0]
```

### 1.4 创建数组

|方式|说明|例子|
|-|-|-|
|`np.array(object)`|从 array-like 对象创建数组|`np.array([1, 2, 3])` -> [1 2 3]|
|`np.asarray(object)`|从 array-like 对象创建数组，但是视图而不是副本|`np.asarray([4, 5, 6])` -> [4 5 6]|
|`np.zeros(shape)`|创建所有元素为 0 的数组|`np.zeros((2, 3))` -> \[[0. 0. 0.] [0. 0. 0.]]|
|`np.zeros_like(ndarray)`|创建与给定数组具有相同形状的数组但是值都为 0 的数组|`np.zeros_like(np.array([[1, 2], [3, 4]]))` -> \[[0 0] [0 0]]|
|`np.ones_like(ndarray)`|创建与给定数组具有相同形状的数组但是值都为 1 的数组|`np.ones_like(np.array([[1, 2], [3, 4]]))` -> \[[1 1] [1 1]]|
|`np.ones(shape)`|创建所有元素为 1 的数组|`np.ones((2, 2))` -> \[[1. 1.] [1. 1.]]|
|`np.eye(shape)`|创建对角线为 1，其余为 0 的单位数组|`np.eye(3)` -> \[[1. 0. 0.] [0. 1. 0.] [0. 0. 1.]]|
|`np.empty(shape)`|创建未初始化的数组，值是随机的|`np.empty((2, 2))` -> 输出未初始化数组|
|`np.arange(begin, end, step)`|创建等间隔数组|`np.arange(0, 10, 2)` -> [0 2 4 6 8]|
|`np.linspace(begin, end, num)`|创建给定区间和数量的等差数组|`np.linspace(0, 1, 5)` -> [0.   0.25 0.5  0.75 1.  ]|
|`np.logspace(begin, end, num)`|创建给定区间和数量的等比数组|`np.logspace(0, 2, 3)` -> [  1.  10. 100.]|
|`np.full(shape, value)`|创建指定值填充的数组|`np.full((2, 3), 7)` -> \[[7 7 7] [7 7 7]]|

> 注意上面所有函数都可以传入参数 `dtype` 来指定数据类型

## 2. NumPy 操作

### 2.1 切片

slice 函数：通过 `slice(begin, end, step)` 构造内置的切片对象
```python
a = np.arange(10)
print(a[slice(2,7,2)])  # -> [2 4 6]
```

冒号语法：通过冒号分割切片参数 `begin:end:step`
```python
a = np.arange(10)
print(a[1:7:2]) # -> [1 3 5]
```

单切片：通过单独数字可以对应轴某个索引的元素
```python
b = np.array([[1, 2, 3], [4, 5, 6], [7, 8, 9]])
print(b[:,1:]) # -> [[2,3] [5,6] [8,9]] 获取第 1 列后的元素
```

全切片：通过 `:` 或 `...` 可以获得对应轴全部索引的元素
```python
b = np.array([[1, 2, 3], [4, 5, 6], [7, 8, 9]])
print(b[:,1:]) # -> [[2,3] [5,6] [8,9]] 获取第 1 列后的元素
print(1:,...)  # -> [[4,5,6] [7,8,9]]  获取第 0 行之后的元素
```

倒序切片：通过 `::-1` 获取数组对应轴的倒序
```python
a = np.arange(10)
print(a[::-1]) # -> [9 8 7 6 5 4 3 2 1 0]
```

### 2.2 索引

数组索引：使用一个值是索引值的数组来访问另一个数组的元素
```python
x = np.array([[1, 2], [3, 4], [5, 6]]) 
print(x[[0,0,0], [0,0,0]]) # -> [1 3 5]
print(x[[0,1,2], [0,1,0]]) # -> [1 4 5]
```

布尔索引：通过布尔运算来获取符合指定条件的元素的索引数组
```python
a = np.arange(10)
print(a[a > 5])         # -> [6 7 8 9]
print(a[a % 2 == 0])    # -> [0 2 4 6 8]
```

笛卡尔积索引：遍历每一轴给定的索引，得到对应的元素
```python
x=np.arange(18).reshape((3,6)) 
'''
[[ 0  1  2  3  4  5]
 [ 6  7  8  9 10 11]
 [12 13 14 15 16 17]]
'''
print(x[np.ix_([2,0], [5,1,3])])
'''
[[17 13 15]  -> 第 2 行的第 5, 1, 3 列元素
 [ 5  1  3]] -> 第 0 行的第 5, 1, 3 列元素
'''
```

### 2.3 广播

广播机制适用于两个形状不一致的数组进行算术操作
1. 对齐维度：在较少维度的数组前面“补”上 1，使它们的维度数一致 ➡️ A.shape = (3, 4)，B.shape = (4,)，B 会被看作 (1, 4)
2. 确定结果数组形状为所有输入数组在每个维度上尺寸的最大值 ➡️ 如果一个数组是 (3, 4)，另一个是 (1, 4)，结果数组的形状就是 (3, 4)
3. 维度匹配：对于每个维度，两个数组要么长度相同，要么其中一个数组的该维度长度是 1，此时小数组会拷贝该维度的值以匹配大数组
4. 如果维度匹配，则抛出 `ValueError: frames are not aligned` 异常

```python
a = np.array([[ 0, 0, 0], [10,10,10], [20,20,20], [30,30,30]])
b = np.array([0,1,2])
print(a + b) # -> [[0 1 2] [10 11 12] [20 21 22] [30 31 32]]
```

![](https://dasi-blog.oss-cn-guangzhou.aliyuncs.com/DataAnalysis/202504011117218.png)

### 2.4 迭代

`np.nditer(ndarray, order)` 提供了一种灵活访问一个或者多个数组元素的方式
```python
a = np.arange(0, 60, 5).reshape(3,4)
'''
[[ 0  5 10 15]
[20 25 30 35]
[40 45 50 55]]
'''
for x in np.nditer(a, order='C'):
    print(x, end=" ") # -> 0 5 10 15 20 25 30 35 40 45 50 55
for x in np.nditer(a, order='F'):
    print(x, end=" ") # -> 0 20 40 5 25 45 10 30 50 15 35 55
```

### 2.5 修改数组形状

|函数|说明|
|-|-|
|`np.reshpae(ndarray, shape)`|传入一个元组表示每个轴上的大小，在不改变数据的条件下修改形状，但必须保持修改前后的数组大小一致，返回的是视图|
|`np.ravel(ndarray)`|返回数组的一份试图，并将数组展平成一维数组，原始数组会受到影响|
|`ndarray.flatten()`|返回数组的一份拷贝，并将数组展平成一维数组，原始数组不会受到影响|

```python
a = np.array([[1,2],[3,4]])
print(np.reshape(a, (1, 4))) # -> [[1 2 3 4]]
print(np.ravel(a))           # -> [1 2 3 4]
```

### 2.6 翻转数组

|函数|说明|
|-|-|
|`np.transpose(ndarray, axes)`|传入新轴顺序来指定目标排列，注意不能传递重复的轴|
|`np.rollaxis(ndarray, axis, index)`|将指定轴滚动到目标位置，其它轴的位置相应调整|
|`np.swapaxe(ndarray, axis1, axis2)`|交换数组中两个指定的轴，返回新的数组|

```python
a = np.arange(24).reshape((2, 3, 4))
print(a)
'''
[[[ 0  1  2  3]
  [ 4  5  6  7]
  [ 8  9 10 11]]

 [[12 13 14 15]
  [16 17 18 19]
  [20 21 22 23]]]
'''
print(np.transpose(a, (1, 0, 2))) # 轴的映射关系：0->1,1->0,2->2
print(np.rollaxis(a, 1, 0))       # 将轴 1 移动到轴 0
print(np.swapaxes(a, 0, 1))       # 将轴 1 和轴 0 互换
'''
三种方法都得到如下数组：原先位于 (i,j,k) 的数据现在位于 (j,i,k)
[[[ 0  1  2  3]
  [12 13 14 15]]

 [[ 4  5  6  7]
  [16 17 18 19]]

 [[ 8  9 10 11]
  [20 21 22 23]]]
'''
```

> 以上三种方式返回的都是原数组的视图，即共享相同的内存，只是改变了索引映射的方式

### 2.7 修改数组维度

|函数|说明|
|-|-|
|`np.broadcast_to(ndarray, shape)`|将数组中大小为1的维度广播到指定形状|
|`np.expand_dims(ndarray, axis)`|在指定位置插入新的轴|
|`np.squeeze(ndarray, axis)`|删除数组中大小为1的维度|

```python
a = np.array([1, 2, 3])
print(np.broadcast_to(a, (3, 3))) # -> [[1 2 3] [1 2 3] [1 2 3]]
print(np.expand_dims(a, axis=0))  # -> [[1 2 3]]
print(np.squeeze(a))              # -> [1 2 3]
```

> 以上三种方式返回的都是原数组的视图，即共享相同的内存，只是改变了索引映射的方式

### 2.8 连接数组

|函数|说明|
|-|-|
|`np.concatenate((a1, a2,...), axes)`|连接沿着指定轴的数组|
|`np.stack((a1, a2,...), axes)`|沿着新的轴加入数组|
|`np.vstack((a1, a2,...))`|沿着第 0 轴的方向竖直堆叠|
|`np.hstack((a1, a2,...))`|沿着第 1 轴的方向水平堆叠|

```python
a = np.array([[1, 2], [3, 4]])
b = np.array([[5, 6], [7, 8]])
print(np.concatenate((a, b), axis=0)) # -> [[1 2] [3 4] [5 6] [7 8]]
print(np.concatenate((a, b), axis=1)) # -> [[1 2 5 6] [3 4 7 8]]
print(np.stack((a,b)))                # -> [[[1 2] [3 4]] [[5 6] [7 8]]]
print(np.vstack((a,b)))               # -> [[1 2] [3 4] [5 6] [7 8]]
print(np.hstack((a,b)))               # -> [[1 2 5 6] [3 4 7 8]]
```

### 2.9 分割数组

|函数|说明|
|-|-|
|`np.split(ndarray, num, axis)`|将一个数组沿着指定轴分割为多个子数组|
|`np.vsplit(ndarray, num)`|将一个数组沿着第 0 轴分割为多个子数组|
|`np.hsplit(ndarray, num)`|将一个数组沿着第 1 轴分割为多个子数组|

```python
a = np.arange(16).reshape((4, 4))
print(a)                # -> [[0 1 2 3] [4 5 6 7] [8 9 10 11] [12 13 14 15]]
print(np.vsplit(a, 2))  # -> [[0 1 2 3] [4 5 6 7]], [[8 9 10 11] [12 13 14 15]]
print(np.hsplit(a, 2))  # -> [[0 1] [4 5] [8 9] [12 13]], [[2 3] [6 7] [10 11] [14 15]]
```

### 2.10 添加与删除

`np.append(ndarray, values, axis)`：将值添加到数组末尾，如果不指定 axis 则会展平
```python
a = np.array([[1,2,3],[4,5,6]])
print(np.append(a, [7,8,9]))
# [1 2 3 4 5 6 7 8 9]
print(np.append(a, [[7,8,9]], axis = 0))
# [[1 2 3] [4 5 6] [7 8 9]]
print(np.append(a, [[5,5,5],[7,8,9]],axis = 1))
# [[1 2 3 5 5 5] [4 5 6 7 8 9]]
```

`np.insert(ndarrray, index, values, axis)`：插入值到指定位置后面，会广播值数组来配输入数组，如果不指定 axis 则会展平
```python
a = np.array([[1,2],[3,4],[5,6]])
print(np.insert(a,3,[11,12]))
# [1 2 3 11 12 4 5 6]
print(np.insert(a,1,[11],axis = 0))
# [[1  2] [11 11] [3  4] [5  6]]
print(np.insert(a,1,11,axis = 1))
# [[1 11 2] [3 11 4] [5 11 6]]
```

`np.delete(ndarray, index, axis)`：删除指定位置的值，如果不指定 axis 则会展平
```python
a = np.arange(12).reshape(3,4)
# [[0 1 2 3] [4 5 6 7] [8 9 10 11]]
print(np.delete(a,1))
# [0 2 3 4 6 7 8 9 10 11]
print(np.delete(a,1,axis = 1))
# [[0 2 3] [4 6 7] [8 10 11]]
print(np.delete(a,1,axis = 0))
# [[0 1 2 3] [8 9 10 11]]
```

`np.unique(ndarray, return_index, return_inverse, return_counts)`：会展开成一维数组，返回排序好的去重元素
- return_index：如果为true，返回新列表元素在旧列表中的位置（下标）
- return_inverse：如果为true，返回旧列表元素在新列表中的位置（下标）
- return_counts：如果为true，返回去重数组中的元素在原数组中的出现次数

```python
a = np.array([5,2,6,2,7,5,6,8,2,9])
print(a)
# [5 2 6 2 7 5 6 8 2 9]
print(np.unique(a))
# [2 5 6 7 8 9]
print(np.unique(a, return_index=True)[1])
# [1 0 2 4 7 9]
print(np.unique(a, return_inverse=True)[1])
# [1 0 2 0 3 1 2 4 0 5]
print(np.unique(a, return_counts=True)[1])
# [3 2 2 1 1 1]
```

## 3. NumPy 运算

### 3.1 字符串运算

| 函数 | 说明 |
| --- | --- |
| `np.char.add(a, b)` | 对两个字符串数组逐元素连接 |
| `np.char.multiply(a, n)` | 将字符串重复 n 次 |
| `np.char.center(a, width, fillchar=' ')` | 将字符串居中，并用指定字符填充至给定宽度 |
| `np.char.capitalize(a)` | 将字符串首字母大写，其余字母小写 |
| `np.char.title(a)` | 将字符串中每个单词的首字母大写 |
| `np.char.lower(a)` | 将字符串转换为小写 |
| `np.char.upper(a)` | 将字符串转换为大写 |
| `np.char.strip(a, chars)` | 删除字符串首尾处的指定字符，默认删除空格 |
| `np.char.split(a, sep)` | 按指定分隔符拆分字符串 |
| `np.char.find(a, sub)` | 查找子字符串首次出现的位置 |
| `np.char.replace(a, old, new)` | 将字符串中的子串替换为新字符串 |

### 3.2 数学运算

| 函数 | 说明 |
| --- | --- |
| `np.add(x, y)` | 逐元素相加 |
| `np.subtract(x, y)` | 逐元素相减 |
| `np.multiply(x, y)` | 逐元素相乘 |
| `np.divide(x, y)` | 逐元素相除 |
| `np.power(x, y)` | 逐元素求幂（x 的 y 次方） |
| `np.sqrt(x)` | 逐元素开平方 |
| `np.exp(x)` | 逐元素计算指数函数 e^x |
| `np.log(x)` | 逐元素计算自然对数 |
| `np.sin(x)` | 逐元素计算正弦 |
| `np.cos(x)` | 逐元素计算余弦 |
| `np.tan(x)` | 逐元素计算正切 |
| `np.abs(x)` | 逐元素取绝对值 |
| `np.floor(x)` | 逐元素向下取整 |
| `np.ceil(x)` | 逐元素向上取整 |

### 3.3 统计运算

| 函数 | 说明 |
| --- | --- |
| `np.sum(a, axis)` | 返回数组所有元素的和 |
| `np.mean(a, axis)` | 返回数组元素的均值 |
| `np.median(a, axis)` | 返回数组元素的中位数 |
| `np.std(a, axis)` | 返回数组元素的标准差 |
| `np.var(a, axis)` | 返回数组元素的方差 |
| `np.min(a, axis)` | 返回数组中的最小值 |
| `np.max(a, axis)` | 返回数组中的最大值 |
| `np.ptp(a, axis)` | 返回数组的极差，即最大值和最小值之差 |
| `np.percentile(a, q, axis)` | 返回数组中位于 q 百分位数处的值（q 为 0～100 的数字） |
| `np.quantile(a, q, axis)` | 返回数组中位于 q 分位数处的值（q 在 0～1 之间） |
| `np.cumsum(a, axis)` | 返回数组的累积和 |
| `np.cumprod(a, axis)` | 返回数组的累积乘积 |
| `np.average(a, axis, weights)` | 计算数组按照给定权重的加权平均值 |
| `np.sort(a, axis, kind, order)` | 返回输入数组的排序副本 |

### 3.4 线性代数运算

| 函数 | 说明 |
| --- | --- |
| `np.dot(a, b)` | 计算向量内积或矩阵乘法；当 a 和 b 为一维时，返回向量内积；当其中一个或两个是二维及以上时，执行矩阵乘法 |
| `np.vdot(a, b)`           | 对两个数组执行向量点积。先将输入数组展平为一维（对于复数数组，会对第一个数组取共轭），然后计算对应元素乘积的和。 |
| `np.inner(a, b)`          | 计算两个数组的内积。对于一维数组，效果与向量内积相同；对于多维数组，内积是对最后一个轴与倒数第二个轴进行乘积后求和。 |
| `np.matmul(a, b)` | 矩阵乘法，与 `@` 操作符等效 |
| `np.linalg.inv(a)` | 计算方阵 a 的逆矩阵 |
| `np.linalg.det(a)` | 计算方阵 a 的行列式 |
| `np.linalg.eig(a)` | 计算方阵 a 的特征值和特征向量，返回元组 (w, v)，其中 w 为特征值，v 为特征向量组成的矩阵 |
| `np.linalg.solve(a, b)` | 解线性方程组 Ax = b，其中 a 为系数矩阵，b 为常数向量或矩阵 |
| `np.linalg.norm(a, ord=None)` | 计算向量或矩阵的范数；ord 参数可指定范数类型，如 L2 范数（默认）、L1 范数、无穷范数等 |


### 3.4 条件筛选运算

| 函数 | 说明 |
| --- | --- |
| `np.argsort(a, axis, kind, order)` | 返回的是数组值从小到大的索引值 |
| `np.argmin(a, axis)` | 返回数组中的最小值的索引 |
| `np.argmax(a, axis)` | 返回数组中的最大值的索引 |
| `np.nonzero(a, axis)` | 返回数组中非零元素的索引 |
| `np.where(condition)` | 返回数组中满足条件的索引 |
| `np.extract(condition, a)` | 从 arr 中提取出满足条件的元素，返回一维数组 |

## 4. 随机模块

| 函数 | 说明 |
| --- | --- |
| `np.random.rand(d0, d1, ...)` | 生成 [0,1) 之间均匀分布的随机浮点数数组，参数为数组各维度的大小 |
| `np.random.randn(d0, d1, ...)` | 生成标准正态分布（均值为0，标准差为1）的随机数数组，参数为数组各维度的大小 |
| `np.random.normal(loc, scale, shape)` | 生成服从给定均值和标准差的正态分布/高斯分布的随机数，shape 指定输出数组的形状 |
| `np.random.randint(low, high, shape)` | 从 [low, high) 区间内生成随机整数，shape 指定输出数组的形状 |
| `np.random.choice(a, shape, replace=True, p=None)` | 从一维数组 a 中随机抽取样本，shape 为输出样本的数量，replace 控制是否可重复抽样，p 为每个元素的概率分布 |
| `np.random.shuffle(x)` | 原地随机打乱数组 x 的顺序（仅适用于一维或多维数组的第一个轴） |
| `np.random.permutation(x)` | 返回 [0, x) 的随机排列 |

## 5. 注意

很多 NumPy 函数在功能上都有与之对应的 ndarray 对象的内置方法，例如可以通过 a.reshape()、a.transpose()、a.sum()、a.mean() 等直接调用，而不用显式地使用 np.reshape(a, ...) 等形式。

但需要注意的是，并不是所有的 NumPy 函数都有对应的 ndarray 方法，有些函数仅作为顶层函数存在
