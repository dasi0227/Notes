# Matplotlib



* [Matplotlib](#matplotlib)
   * [1. 线图 plot](#1-线图-plot)
      * [1.1 使用](#11-使用)
      * [1.2 点的格式](#12-点的格式)
      * [1.3 线的格式](#13-线的格式)
      * [1.4 标签格式](#14-标签格式)
      * [1.5 轴的格式](#15-轴的格式)
      * [1.6 网格格式](#16-网格格式)
   * [2. 多图 subplot](#2-多图-subplot)
   * [3. 散点图 scatter](#3-散点图-scatter)
   * [4. 柱形图 bar/barh](#4-柱形图-barbarh)
   * [5. 饼图 pie](#5-饼图-pie)
   * [6. 直方图 hist](#6-直方图-hist)
* [假设有这样的情景，考试满分是120分，其中有20分是附加分，现在有一组成绩数据，需要知道糟糕（40-60）、不合格（40-60）、合格（60-80）、良好（80-90）和优秀（90-100）的人数，还需要知道成绩为合格及以上每十分的累加比例](#假设有这样的情景考试满分是120分其中有20分是附加分现在有一组成绩数据需要知道糟糕40-60不合格40-60合格60-80良好80-90和优秀90-100的人数还需要知道成绩为合格及以上每十分的累加比例)
   * [7. 图像处理 im](#7-图像处理-im)



## 1. 线图 plot

### 1.1 使用

`plt.plot()` 用于绘制线图，展示数据随时间或序列变化的趋势。线图通过连续的线段连接离散的数据点，常用于展示连续数据的变化趋势。
- x_points：每个离散点的 x 坐标，可以是任何 array-like 对象，如果不传递 x_points，系统会自动生成一个 y_points 的索引列表作为 x_points，即 [0, 1, 2, ..., len(y_points)-1]
- y_points：每个离散点的 y 坐标，可以是任何 array-like 对象
- formats：格式字符串 `[marker][line][color]`，用于一次性设置三个格式
- args：利用关键字参数自定义格式，常见的有
  - linewidth：设置线条的宽度
  - marker：设置数据点的标记样式
  - markersize：设置数据点标记的大小
  - linestyle：设置线条的样式
  - color：设置线条和标记的颜色
- label：设置图例中显示的标签

实际上，在 matplotlib 中绘制任何图形（圆、直线、方形），实际上都不是连续的，而是将一个个离散的点连线而成，下面给出一个简单的例子
```python
x = [1,2,3,4]
y = [1,4,9,16]
plt.plot(x, y)
```
![](https://dasi-blog.oss-cn-guangzhou.aliyuncs.com/DataAnalysis/202504011117179.png)

为了实现二次函数的连续曲线效果，我们获取更多更密的点
```python
x = np.linspace(1, 4, 10000)
y = x ** 2
plt.plot(x, y)
plt.show()
```
![](https://dasi-blog.oss-cn-guangzhou.aliyuncs.com/DataAnalysis/202504011117181.png)

可以利用 format 设置样式为“红色圆圈虚线”即 `ro--`
```python
plt.plot(x, y, "ro--")
```
![](https://dasi-blog.oss-cn-guangzhou.aliyuncs.com/DataAnalysis/202504011117182.png)

还可以利用参数指定样式
```python
plt.plot(x, y, color='green', marker='x', linestyle=':', linewidth=5, markersize=20)
```
![](https://dasi-blog.oss-cn-guangzhou.aliyuncs.com/DataAnalysis/202504011117183.png)

### 1.2 点的格式

常用的样式值有
|标记|样式|
|-|-|
|'.'|点|
|','|像素点|
|'o'|实心圆|
|'^'|上三角|
|'*'|星|
|'X'|填充叉|
|'x'|线条叉|
|'D'|菱|

常用的颜色值有
|标记|颜色|
|-|-|
|'r'|红色|
|'g'|绿色|
|'b'|蓝色|
|'c'|青色|
|'m'|品红色|
|'y'|黄色|
|'k'|黑色|
|'w'|白色|
|'none'|无色|

除了指定样式，我们还可以实现更多的自定义
- `markersize` 或 `ms`：定义标记的大小
- `markerfacecolor` 或 `mfc`：定义标记的内部颜色
- `markeredgecolor` 或 `mec`：定义标记的边框颜色

```python
plt.plot(x, y, marker='o', ms=10, mfc='g', mec='r')
```
![](https://dasi-blog.oss-cn-guangzhou.aliyuncs.com/DataAnalysis/202504011117184.png)

如果想实现空心圆的效果，我们可以让内部颜色为空即可
```python
plt.plot(x, y, marker='o', ms=20, mfc='none', mec='m')
```
![](https://dasi-blog.oss-cn-guangzhou.aliyuncs.com/DataAnalysis/202504011117185.png)

### 1.3 线的格式

常用的样式值有
|标记|简写|样式|
|-|-|-|
|'solid'|'-'|实线|
|'dotted'|':'|点虚线|
|'dashed'|'--'|破折线|
|'dashdot'|'-.'|点划线|
|'None'|''|不划线|

linestyle 参数也可以简写为 `ls`
```python
plt.plot(x, y, marker='o', ls='-.')
```
![](https://dasi-blog.oss-cn-guangzhou.aliyuncs.com/DataAnalysis/202504011117186.png)

我们可以利用不划线来实现散点图的一种绘制方式
```python
plt.plot(x, y, marker='o', ms=5, ls='none')
```
![](https://dasi-blog.oss-cn-guangzhou.aliyuncs.com/DataAnalysis/202504011117188.png)

我们可以通过参数 color 来设置线的颜色，再通过 mfc 和 mgc 来设置点的颜色，从而实现区分
```python
plt.plot(x, y, marker='o', ms=8, ls=':', color='b', markerfacecolor='r', markeredgecolor='r')
```
![](https://dasi-blog.oss-cn-guangzhou.aliyuncs.com/DataAnalysis/202504011117189.png)

我们可以传入多个 y_points 在一个图里面画出多条线，系统会自动设置不同颜色，我们也可以手动指定每个线图的颜色
```python
y1 = [3, 7, 5, 9]
y2 = [6, 2, 13, 10]
plt.plot(y1)
plt.plot(y2)
```
![](https://dasi-blog.oss-cn-guangzhou.aliyuncs.com/DataAnalysis/202504011117190.png)

### 1.4 标签格式

- `plt.legend(loc)` 显示图例，标识每个线图的事先设置的标签，可以通过传入以下 loc 参数值来指定图例位置

| 位置代码         | 说明             |
| ---------------- | ---------------- |
| `'best'`         | 自动选择最佳位置，默认值 |
| `'upper right'`  | 图例位于右上角     |
| `'upper left'`   | 图例位于左上角     |
| `'lower left'`   | 图例位于左下角     |
| `'lower right'`  | 图例位于右下角     |
| `'right'`        | 图例位于右侧       |
| `'center left'`  | 图例位于左侧中部   |
| `'center right'` | 图例位于右侧中部   |
| `'lower center'` | 图例位于底部中央   |
| `'upper center'` | 图例位于顶部中央   |
| `'center'`       | 图例位于图形中央   |

```python
x = np.linspace(0, 2*np.pi, 100)
y1 = np.sin(x)
y2 = np.cos(x)
plt.plot(x, y1, 'b-', label='sin(x)')
plt.plot(x, y2, 'r-', label='cos(x)')
plt.legend(loc='upper right')
```
![](https://dasi-blog.oss-cn-guangzhou.aliyuncs.com/DataAnalysis/202504011117191.png)

- `plt.xlabel(name, loc)` 设置 x 轴的标签，loc 值可以是 left, right, center
- `plt.ylabel(name, loc)` 设置 y 轴的标签，loc 值可以是 top, bottom, center
- `plt.title(name, loc)` 设置图的标题，loc 值可以是 left, right, center

```python
x = np.linspace(0, 2*np.pi, 100)
y1 = np.sin(x)
y2 = np.cos(x)
plt.plot(x, y1, 'b-', label='sin(x)')
plt.plot(x, y2, 'r-', label='cos(x)')
plt.xlabel("x")
plt.ylabel("f(x)")
plt.title("trigonometric function")
plt.legend(loc='best')
```
![](https://dasi-blog.oss-cn-guangzhou.aliyuncs.com/DataAnalysis/202504011117192.png)

> 需要注意的是 matplotlib 不支持中文，需要手动导入字体

### 1.5 轴的格式

> 对 x 轴的设置和对 y 轴的设置代码是一样的，只需把 x 替换成 y 即可，这里用 x 轴为例

Matplotlib 的坐标轴刻度会自动选择“好看的”数字显示，这些刻度可能并不与 x,y 数组中的某些具体值完全一致
```python
x = np.linspace(0, 2*np.pi, 100)
y = np.sin(x)
plt.plot(x, y, 'b-')
```
![](https://dasi-blog.oss-cn-guangzhou.aliyuncs.com/DataAnalysis/202504011117195.png)

`plt.xticks(values, names)`：设置 x 轴刻度的位置和标签
```python
plt.xticks([0, np.pi/2, np.pi, np.pi*3/2, np.pi*2], ['0', 'pi/2', 'pi', '3/2pi', '2pi'])
```
![](https://dasi-blog.oss-cn-guangzhou.aliyuncs.com/DataAnalysis/202504011117193.png)

`plt.xlim(min, max)`：设置 x 轴的显示范围，即传入最小值和最大值
```python
plt.xlim(np.pi/6, np.pi*4/3)
```
![](https://dasi-blog.oss-cn-guangzhou.aliyuncs.com/DataAnalysis/202504011117194.png)

`plt.xscale(type)`：设置 x 轴的刻度比例，type 值如下
- linear：用于常规数据，无需特殊转换
- log：当数据跨度巨大（多数量级）且数据全为正时使用
- symlog：适合数据既有正有负，且在零附近变化较快，远离零时呈对数增长的情况
- logit：专门针对概率数据，帮助揭示在接近 0 或 1 时微小差异的重要性

```python
x = np.linspace(1, 10000000, 100)
y = np.log(x)
plt.plot(x, y)
plt.xscale('log')
```
![](https://dasi-blog.oss-cn-guangzhou.aliyuncs.com/DataAnalysis/202504011117196.png)

### 1.6 网格格式

grid() 方法来设置图表中的网格线
- axis：设置显示哪个方向的网格线，可以取 'both', 'x' 和 'y'
- kwargs：设置网格样式，如颜色，样式和宽度

```python
x = np.arange(0, 10*np.pi, np.pi / 6)
y = np.sin(x)
plt.plot(x, y, 'b-')
plt.grid(axis='x', c='g', ls='-.', lw=2)
```
![](https://dasi-blog.oss-cn-guangzhou.aliyuncs.com/DataAnalysis/202504011117197.png)



## 2. 多图 subplot

`plt.subplot(nrows, ncols, index)` 来绘制多个子图
- nrows 和 ncols 将整个绘图区域分成 nrows 行和 ncols 列，然后从左到右，从上到下的顺序对每个子区域进行编号 1...N
- index 指定区域编号，接下来的绘图都是在这个区域进行

创建 1 行 3 列子图的图
```python
x = np.linspace(0, 4*np.pi, 100)
y1, y2, y3 = np.sin(x), np.cos(x), np.tan(x)
plt.figure(figsize=(10, 5))
plt.subplot(1,3,1)
plt.plot(x,y1)
plt.subplot(1,3,2)
plt.plot(x,y2)
plt.subplot(1,3,3)
plt.plot(x,y3)
```
![](https://dasi-blog.oss-cn-guangzhou.aliyuncs.com/DataAnalysis/202504011117198.png)

创建 2 行 2 列子图的图，通过 `plt.suptitle()` 设置整个图的标题
```python
x = np.array([0, 6])
y = np.array([0, 100])

plt.subplot(2, 2, 1)
plt.plot(x,y)
plt.title("plot 1")

plt.subplot(2, 2, 2)
plt.plot(x,-y)
plt.title("plot 2")

plt.subplot(2, 2, 3)
plt.plot(-x,y)
plt.title("plot 3")

plt.subplot(2, 2, 4)
plt.plot(-x,-y)
plt.title("plot 4")

plt.suptitle("RUNOOB subplot Test")
```
![](https://dasi-blog.oss-cn-guangzhou.aliyuncs.com/DataAnalysis/202504011117199.png)



## 3. 散点图 scatter

`plt.scatter()` 用于绘制散点图，展示数据点之间的分布和相关性。散点图仅显示离散数据点，不连接线条，适合用于观察变量之间的关系和数据的离散性
```python
x = np.random.randint(1, 10, 20)
y = np.random.randint(1, 10, 20)
plt.scatter(x, y, marker='o')
```
![](https://dasi-blog.oss-cn-guangzhou.aliyuncs.com/DataAnalysis/202504011117200.png)

`s` 参数可以用来指定散点的大小/面积，如果给定单个值则统一作用到每个散点，否则给定相同长度的数组作用于对应的散点
```python
x = np.random.randint(1, 10, 20)
y = np.random.randint(1, 10, 20)
size = np.random.choice([10,100,500], 20)
plt.scatter(x, y, s=size)
```
![](https://dasi-blog.oss-cn-guangzhou.aliyuncs.com/DataAnalysis/202504011117201.png)

`c` 参数可以用来指定散点的颜色，如果给定单个值则统一作用到每个散点，否则给定相同长度的数组作用于对应的散点；`alpha` 参数可以用来指定散点的透明度，但只能给定单个值则统一作用到每个散点
```python
x = np.random.rand(N)
y = np.random.rand(N)
colors = np.random.rand(N)
sizes = (30 * np.random.rand(N))**2
plt.scatter(x, y, s=sizes, c=colors, alpha=0.5)
```
![](https://dasi-blog.oss-cn-guangzhou.aliyuncs.com/DataAnalysis/202504011117202.png)

`cmap` 参数用于将标量数据映射为颜色，可以用 `plt.colorbar()` 来显示颜色条
- 'viridis'（默认）：从深紫到黄色的渐变色，色彩平衡且易于区分
- 'plasma'：较为鲜艳，从深蓝到橙色
- 'inferno'：暖色调，从黑色到黄色
- 'magma'：柔和色调，从深紫到白色
- 'jet'：经典的彩虹色，但不推荐用于科学数据可视化，因为色彩非线性且容易产生误导
```python
x = np.linspace(0, 10, 50)
y = np.sin(x)
colors = np.linspace(0, 1, 50)
plt.scatter(x, y, c=colors, cmap='jet', s=100, marker='o')
plt.colorbar()
```
![](https://dasi-blog.oss-cn-guangzhou.aliyuncs.com/DataAnalysis/202504011117203.png)



## 4. 柱形图 bar/barh

`plt.bar()`（用于垂直柱状图）和 `plt.barh()`（用于水平柱状图）用于绘制柱状图，展示不同类别数据之间的比较。柱状图通过条形的长度或高度来反映各类别的数值大小，适合比较不同分类数据的差异。

在这里 `x` 给出的是分类标签，`y` 给出的是柱形的高度
```python
x = ['label1', 'label2', 'label3']
y = [5, 15, 10]
plt.bar(x, y)
```
![](https://dasi-blog.oss-cn-guangzhou.aliyuncs.com/DataAnalysis/202504011117204.png)

对于 `plt.bar()` 使用参数 `width` 设置柱形宽度，对于 `plt.barh()` 使用参数 `height` 设置柱形宽度，如果给定单个值则统一作用到每个柱形，否则给定相同长度的数组作用于对应的柱形
```python
y = [5, 15, 10]
x = ['label1', 'label2', 'label3']
plt.subplot(1,2,1)
plt.bar(x, y, width=0.1)
plt.subplot(1,2,2)
plt.barh(x, y, height=[0.1,0.3,0.5])
```
![](https://dasi-blog.oss-cn-guangzhou.aliyuncs.com/DataAnalysis/202504011117205.png)

参数 `color` 可以设置柱形的填充色，如果给定单个值则统一作用到每个柱形，否则给定相同长度的数组作用于对应的柱形
```python
x = ['label1', 'label2', 'label3', 'label4']
y = [12, 22, 6, 18]
colors = ["#4CAF50","red","hotpink","#556B2F"]
plt.bar(x, y, color=colors)
```
![](https://dasi-blog.oss-cn-guangzhou.aliyuncs.com/DataAnalysis/202504011117206.png)



## 5. 饼图 pie

`plt.pie()` 用于绘制饼图，展示各部分占整体的比例，饼图将数据按比例分割为若干扇区，适用于显示组成部分的相对大小。

这里只用给出 `x` 浮点数数组表示每个扇形的面积比例
```python
x = [0.3, 0.15, 0.4, 0.15]
plt.pie(x)
```
![](https://dasi-blog.oss-cn-guangzhou.aliyuncs.com/DataAnalysis/202504011117207.png)

以下几个基本参数，都是给出数组来表示每个扇形的属性
- `colors`：各个扇形的颜色
- `labels`：各个扇形的标签
- `explode`：各个扇形之间的间隔
```python
x = [0.3, 0.15, 0.4, 0.15]
colors = ['green', 'blue', 'red', 'yellow']
labels = ['label1', 'label2', 'label3', 'label4']
explodes = [0, 0.1, 0, 0]
plt.pie(x, colors=colors, labels=labels, explode=explodes)
```
![](https://dasi-blog.oss-cn-guangzhou.aliyuncs.com/DataAnalysis/202504011117209.png)

此外，饼图还有很多参数可以自定义
- `autopct`：设置饼图内各个扇形百分比显示格式，如 `%d%%` 整数百分比，`%0.1f` 一位小数，`%0.1f%%` 一位小数百分比，`%0.2f%%` 两位小数百分比
- `labeldistance`：设置 `autopct` 距离扇形的距离
- `shadow`：布尔值，设置饼图的阴影
- `startangle`：指定饼图的起始角度，默认为从 x 轴正方向逆时针画起
- `counterclock`：布尔值，指定是否逆时针绘制扇形
- `radius`：设置饼图的半径
```python
x = [0.3, 0.15, 0.4, 0.15]
explodes = [0, 0.2, 0, 0]
plt.pie(x, explode=explodes, autopct='%0.1f', shadow=True, radius=1.3, startangle=90, counterclock=True)
```
![](https://dasi-blog.oss-cn-guangzhou.aliyuncs.com/DataAnalysis/202504011117210.png)



## 6. 直方图 hist

`plt.hist()` 用于绘制直方图，展示数据的分布情况。直方图将数据分成若干个区间，统计每个区间内数据的个数或比例，帮助观察数据的频率分布和集中趋势

这里 `x` 给出的是分布数据（可以是二维的，表示多组分布数据），系统会自动根据数据的值域分成若干个区间
```python
x = np.random.randint(0, 101, size=200)
plt.hist(x, histype='step')
```
![](https://dasi-blog.oss-cn-guangzhou.aliyuncs.com/DataAnalysis/202504011117211.png)

直方图有很多自定义的参数，常见的有
- `bins`：指定直方图的柱数，如果是整数则自动将数据分成该数目的等宽区间，如果是序列则需要明确指定各个区间的边界
- `range`：给出最小值和最大值组成的二元组，表示直方图的值域范围
- `density`：布尔值，True 显示比例，False 显示个数
- `culmulative`：布尔值，True 显示累积和
- `bottom`：设置基准线位置
- `rwidth`：柱子占据 bin 的比例，间接设置柱子间的间隔
```python
# 假设有这样的情景，考试满分是120分，其中有20分是附加分，现在有一组成绩数据，需要知道糟糕（40-60）、不合格（40-60）、合格（60-80）、良好（80-90）和优秀（90-100）的人数，还需要知道成绩为合格及以上每十分的累加比例
x = np.random.randint(0, 121, size=200)
plt.subplot(1,2,1)
plt.hist(x, bins=[0, 40, 60, 80, 90, 100], density=False, cumulative=False, bottom = 5, rwidth= 0.95)
plt.xticks(bins)
plt.subplot(1,2,2)
plt.hist(x, bins=4, range=(60,100), density=True, cumulative=True, bottom = 0, rwidth= 0.95)
```
![](https://dasi-blog.oss-cn-guangzhou.aliyuncs.com/DataAnalysis/202504011117212.png)


此外，还可以通过 `histtype` 设置柱子的样式
- `'bar'`（默认）：普通柱状图
- `'step'`：只绘制边界线
- `'stepfilled'`：边界线内填充颜色
- `'barstacked'`：堆叠柱状图，适用于多组数据堆叠显示
```python
data1 = np.random.randn(1000)
data2 = np.random.randn(1000) + 2

plt.figure(figsize=(12,5))
plt.subplots_adjust(wspace=0.3, hspace=0.3)
plt.suptitle('histtype')

plt.subplot(2,2,1)
plt.hist(data1, bins=30, histtype='bar', color='skyblue', edgecolor='black')
plt.title('bar')

plt.subplot(2,2,2)
plt.hist(data1, bins=30, histtype='step', color='skyblue', edgecolor='black')
plt.title('step')

plt.subplot(2,2,3)
plt.hist(data1, bins=30, histtype='stepfilled', color='skyblue', edgecolor='black')
plt.title('stepfilled')

plt.subplot(2,2,4)
plt.hist([data1, data2], bins=30, histtype='barstacked', color=['skyblue', 'salmon'], rwidth=0.9)
plt.title('barstacked')
```
![](https://dasi-blog.oss-cn-guangzhou.aliyuncs.com/DataAnalysis/202504011117213.png)



## 7. 图像处理 im

- `plt.imread(filename)`：读取常见格式的图像文件并返回一个 NumPy 数组，数组维度通常为 (height, width, channels)，灰度图像的通道数量为 1，彩色图像的通道数量为 3 或 4
- `plt.imsave(filename, arr)`：将数组中的图像数据保存到指定文件，支持多种图像格式，文件格式通常由文件扩展名确定
- `plt.imshow(arr)`：在当前的绘图区域中显示图像

设置插值方式
```python
n = 4
a = np.reshape(np.linspace(0,1,n**2), (n,n))

plt.subplot(121)
plt.imshow(a, cmap='viridis', interpolation='nearest')
plt.yticks(range(n))
plt.xticks(range(n))

plt.subplot(122)
plt.imshow(a, cmap='viridis', interpolation='bicubic')
plt.yticks(range(n))
plt.xticks(range(n))
```
![](https://dasi-blog.oss-cn-guangzhou.aliyuncs.com/DataAnalysis/202504011117214.png)

设置显示范围
```python
img_array1 = plt.imread('filename')
img_array2 = img_array1[100:400,500:800,:]
plt.subplot(1,2,1)
plt.imshow(img_array1)
plt.subplot(1,2,2)
plt.imshow(img_array2)
```
![](https://dasi-blog.oss-cn-guangzhou.aliyuncs.com/DataAnalysis/202504011117215.png)

设置颜色
```python
img_array = plt.imread('filename')
img_array1 = img_array.copy()
img_array1 = img_array1 / 255 * 0.3
img_array2 = img_array.copy()
img_array2[:,:,1:3] = 0
plt.subplot(1,2,1)
plt.imshow(img_array1)
plt.subplot(1,2,2)
plt.imshow(img_array2)
```
![](https://dasi-blog.oss-cn-guangzhou.aliyuncs.com/DataAnalysis/202504011117216.png)

转变为灰度图像
```python
img_array = plt.imread('filename')
gray = np.dot(img_array[...,:3], [0.299, 0.587, 0.114])
plt.imshow(gray, cmap='gray')
```
![](https://dasi-blog.oss-cn-guangzhou.aliyuncs.com/DataAnalysis/202504011117217.png)