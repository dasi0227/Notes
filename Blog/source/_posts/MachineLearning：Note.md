---
title: 机器学习
tags:
  - AI
categories:
  - 笔记
description: 定义、线性回归/分类，支持向量机，神经网络，决策树，线性降维，聚类，高斯混合模型，生成模型，集成学习，表示学习，推荐系统，异常检测，多模态学习
cover: /image/ml.png
abbrlink: 5b80d779
date: 2025-01-02 14:22:38
---
<meta name="referrer" content="no-referrer"/>

## 机器学习大纲

![](https://dasi-blog.oss-cn-guangzhou.aliyuncs.com/MachineLearning/chapter1-18/202501022056970.png)

## 什么是机器学习

机器学习是一种通过**数据和算法**使计算机系统能够自动改进其性能的技术。
机器**利用已给数据和学习算法来得到一个程序**，而不是利用程序来接受输入从而产生输出。

![](https://dasi-blog.oss-cn-guangzhou.aliyuncs.com/MachineLearning/chapter1-18/202501022056968.png)

本质上都是数据驱动学习，但是可以细分为以下四类：
- **监督学习（Supervised）**：标签驱动，**学习特征和标签的映射关系，目标是在新的特征上准确预测输出**，如分类任务、判断任务、检测任务、回归任务
- **无监督学习（Unsupervised）**：关系驱动，**学习数据内部之间的关系和规律，目标是得到数据的结构信息**，如聚类任务、降维任务
- **强化学习（Reinforcement）**：环境驱动，**学习智能体对环境信息的反应，目标是得到最优策略和最大化累计奖励**，如自动控制、游戏智能
- **数据挖掘（Data Mining）**：价值驱动，**学习海量数据，目标是总结数据价值和模式**，如自然语言处理，相似性搜索、推荐系统

## 线性回归

### 回归

回归是根据输入，预测输出。数学来说，就是根据一组自变量，学习函数表达式，来得到因变量

线性回归：上述函数表达式是线性表达式，也就是$f(x) = w_0 + w_1x_1 + ... + w_mx_m$，其中$w$是模型参数，$m$是数据维度

线性回归任务：找到最合适的模型参数$w$，使得模型预测的$y_{pred}$能够尽可能真实值$y_{true}$，也就是说让误差$y_{true}-y_{pred}$尽可能小

### 单特征

线性回归表示为
![](https://dasi-blog.oss-cn-guangzhou.aliyuncs.com/MachineLearning/chapter1-18/202501022056971.png)

可以利用均方误差度量误差
![](https://dasi-blog.oss-cn-guangzhou.aliyuncs.com/MachineLearning/chapter1-18/202501022056972.png)

令误差梯度=0，即表示此时误差已经是最小值，就可以得到最优参数
![](https://dasi-blog.oss-cn-guangzhou.aliyuncs.com/MachineLearning/chapter1-18/202501022056973.png)

### 多特征

线性回归表示为
![](https://dasi-blog.oss-cn-guangzhou.aliyuncs.com/MachineLearning/chapter1-18/202501022056974.png)

利用向量可以表示为
![](https://dasi-blog.oss-cn-guangzhou.aliyuncs.com/MachineLearning/chapter1-18/202501022056975.png)

因此再次利用均方误差度量误差，写成向量形式，并用范数表示
![](https://dasi-blog.oss-cn-guangzhou.aliyuncs.com/MachineLearning/chapter1-18/202501022056976.png)

令误差梯度=0，即表示此时误差已经是最小值，就可以得到最优参数
![](https://dasi-blog.oss-cn-guangzhou.aliyuncs.com/MachineLearning/chapter1-18/202501022056977.png)

最优参数的几何解释：$Xw$的本质是向量$X$张成的一个空间，要在这个空间上找到一个向量，使得其尽可能靠近$y$，而$y$不在该列空间上，也就是我们要让$Xw$尽可能接近$y$$在列空间的投影
![](https://dasi-blog.oss-cn-guangzhou.aliyuncs.com/MachineLearning/chapter1-18/202501022056978.png)

### 梯度下降

梯度：是**函数沿着最快方向的变化速率**，如果梯度是9，那么自变量改变0.1，因变量就会改变0.9

通常情况下，无法闭式解$w^*$不存在或者求$w^*$的计算复杂度太高，导致得不到$w^*$，因此可以通过迭代的方法，不断优化$w$，经过大量迭代次数后使得$w$趋近于$w^*$
![](https://dasi-blog.oss-cn-guangzhou.aliyuncs.com/MachineLearning/chapter1-18/202501022056979.png)

如果不设置学习率，优化过程会失去对步长的控制，只能简单地沿着梯度方向变化一个单位长度，而学习率实际上可以被视为一种缩放因子，它**控制了参数更新的步长/程度**
- 如果学习率过小，更新的步长很短，导致下降过程非常缓慢，需要进行大量的迭代才能接近最优解
- 如果学习率过大，更新的步长很大，导致参数跳过最优点，甚至让损失函数值反复波动，无法收敛到正确的结果

在处理大规模数据集时，计算整个数据集的梯度成本非常高。此时，可以将数据随机分成多个小批次，然后**对每个批次计算梯度并更新参数**，这样可以显著降低了计算复杂度
- 如果批次太小，每次计算的梯度可能会偏离真实梯度，导致优化过程不够稳定
- 如果批次太大，则失去了计算效率优势
![](https://dasi-blog.oss-cn-guangzhou.aliyuncs.com/MachineLearning/chapter1-18/202501022056980.png)

## 线性分类

### 二分类

相比于线性回归，区别最大的在于标签值是离散的，标签值无法直接用特征值的线性组合函数来表示，因此我们需要一个激活函数，它用于将线性组合值从[-∞,+∞]映射到[0,1]
![](https://dasi-blog.oss-cn-guangzhou.aliyuncs.com/MachineLearning/chapter1-18/202501022056981.png)

MSE 假设输出是连续的，这与分类问题的离散输出不匹配，而且分类问题中预测和标签的差值一般都很小，用 MSE 的训练速度会很慢。
![](https://dasi-blog.oss-cn-guangzhou.aliyuncs.com/MachineLearning/chapter1-18/202501022056982.png)

因此我们考虑对差值使用对数函数
1. log 函数的导数就是自变量的倒数，计算极其简单
2. log 函数是凸函数，即梯度保持最优参数方向
3. log 函数具有突变性，即当预测值和真实值相差较大时，log 函数会给出非常大的损失值

考虑如下格式，如果真实分类结果是1，我们希望激活函数的输出越接近于1，那么误差$-log(\sigma(xw))$的值就越接近于0，如果真实分类结果是0，我们希望激活函数的输出越接近于0，那么误差$-log(1-\sigma(xw))$的值就越接近于0
![](https://dasi-blog.oss-cn-guangzhou.aliyuncs.com/MachineLearning/chapter1-18/202501022056983.png)

实际上，我们可以避免使用判断语句，而是利用数学特征来优化，得到如下式子，也就是交叉熵损失。
![](https://dasi-blog.oss-cn-guangzhou.aliyuncs.com/MachineLearning/chapter1-18/202501022056984.png)

通过链式法则可以发现，梯度就是等于$(\sigma(xw)-y_{true}) \cdot x$
![](https://dasi-blog.oss-cn-guangzhou.aliyuncs.com/MachineLearning/chapter1-18/202501022056985.png)

我们可以根据$xw$是否大于0来确定预测值，也根据$\sigma(xw)$是否大于0.5来确定预测值，这样得到的线性超平面$xw$称为决策平面
![](https://dasi-blog.oss-cn-guangzhou.aliyuncs.com/MachineLearning/chapter1-18/202501022056986.png)

### 多分类

方法一：训练 K 个二分类器，**每个分类器用于对其中一类进行预测属于/不属于**，模型输出的预测值作为对应类别的预测得分，选择预测得分最高的分类器对应的类别作为最终预测
![](https://dasi-blog.oss-cn-guangzhou.aliyuncs.com/MachineLearning/chapter1-18/202501022056987.png)

方法二：引入 Softmax 函数和矩阵运算来集成分类的整个过程。构造一个参数矩阵 W ，其中每一列参数向量$W_k$对应于一个类别的分类器。这种方式将原本需要训练多个分类器的任务整合为一次训练，通过矩阵运算统一计算所有类别的预测得分。然后再利用 Softmax 函数将多个二分类器的预测得分汇总到一起，最终输出一个对所有类别的概率分布

其中指数函数具有以下作用
1. 非负性：确保概率值都是正
2. 突变性：可以放大两个输入值的差异
3. 单调性：输入值越大，输出值也越大
4. 归一性：将输出变为概率分布

$$
\text{Softmax}(z_i) = \frac{e^{z_i}}{\sum_{j=1}^K e^{z_j}}
$$

实际上，我们的**优化目标主要是让预测标签尽可能接近真实标签，而并没有显式去让预测标签尽可能远离错误标签**，令$y_k^{\text{pred}}$是真实类别k的预测概率，则损失函数为
$$
L = -\ln(y_k^{\text{pred}})
$$
![](https://dasi-blog.oss-cn-guangzhou.aliyuncs.com/MachineLearning/chapter1-18/202501022056990.png)

## 概率角度分析回归和分类

概率视角：关注给定x预测得到y的概率是多少，即求$p(y|x)$，通过建模概率分布，得到预测值就是概率分布的均值

回归可以看作成是高斯分布
$$
p(y|\mathbf{x}; \mathbf{w}) = \mathcal{N}(y; \mathbf{x}\mathbf{w}, \sigma^2)
$$

分类可以看作为是伯努利分布
$$p(y|\mathbf{x}) = \sigma(\mathbf{x}\mathbf{w})^y \cdot (1 - \sigma(\mathbf{x}\mathbf{w}))^{1-y}
$$
对于概率分布，最小化损失函数 == 最大化似然函数，即让误差尽可能小 == 让条件概率尽可能大

然而在计算联合概率的时候，概率都是浮点数，且存在较小值，概率的连乘会导致复杂计算，因此需要对其取对数，转化为对数的加法
$$
\log p(y_1, y_2, \dots, y_N | x_1, x_2, \dots, x_N; \theta) = \sum_{i=1}^N \log p(y_i | x_i; \theta)
$$
为了统一优化目标是求损失函数的极小值，定义为负对数似然函数
$$
L(\theta) = -\log p(y|\mathbf{x}; \theta)
$$
## 泛化能力

### 基函数

可以利用基函数将特征进行非线性变换，从而**将数据从低维线性空间扩展到高维非线性空间**，比如进行多项式扩展$x \to [x, x^2, x^3]$

变换后的模型虽然对特征 x 是非线性的，但对模型参数 w 仍是线性的
![](https://dasi-blog.oss-cn-guangzhou.aliyuncs.com/MachineLearning/chapter1-18/202501022056991.png)

### 过拟合

当模型过于复杂，**虽然训练数据表现得很好，但在测试数据上表现可能很差**
![](https://dasi-blog.oss-cn-guangzhou.aliyuncs.com/MachineLearning/chapter1-18/202501022056992.png)

通常来说，模型的复杂度和泛化能力之间存在平衡，即**当模型复杂度超过一定程度时，模型复杂度越高，泛化能力反而越低**
![](https://dasi-blog.oss-cn-guangzhou.aliyuncs.com/MachineLearning/chapter1-18/202501022056993.png)

### 模型评估

将原始数据集划分一部分作为测试集，然后选择在测试集上表现最好的模型。

然而有时候数据集大小有限，我们需要使用**K-折交叉验证**来充分利用数据，也就是将数据分为 K 份，轮流用 K-1 份训练，剩下 1 份验证，最后取平均性能，作为模型总性能
![](https://dasi-blog.oss-cn-guangzhou.aliyuncs.com/MachineLearning/chapter1-18/202501022056994.png)

### 信息准则

适用于概率模型，用于平衡模型复杂度和数据拟合度选择模型，其中 M 是模型参数数量，L 是模型的对数似然，N 是数据样本数量。**信息准则的值越小越好，就要求 M 不能过大， L 不能过小**。同时如果 N 很大的情况下，训练程度足够深，应该进一步限制参数数量
- $AIC = 2M - 2\log L$
- $BIC = M \log N - 2\log L$

{% note warning flat %}
取对数是为了防止数值增长过快
{% endnote %}

### 正则化

本质是改进损失函数，即**在损失函数中加上一个参数项，从而在降低损失函数的同时也能够抑制模型复杂度的提高**
- L1正则化，适合**减少参数的数量**，在损失函数中加上参数的绝对值和：$Q(w) = L(w) + \lambda \sum_{i=1}^M |w_i|$
- L2正则化，适合**减小参数的大小**，在损失函数中加上参数的范数平方和$Q(w) = L(w) + \lambda \sum_{i=1}^M w_i^2$
- 正则化强度$\lambda$：正则化强度越大，迫使模型越简单，但可能会导致欠拟合

![](https://dasi-blog.oss-cn-guangzhou.aliyuncs.com/MachineLearning/chapter1-18/202501022056995.png)

## 神经网络

### 激活函数

作用：引入多层非线性变换，使模型可以很好拟合非线性数据

![](https://dasi-blog.oss-cn-guangzhou.aliyuncs.com/MachineLearning/chapter1-18/202501131224705.png)

Sigmoid: 输出范围 (0, 1)，适合处理概率问题，但当输入远离零时梯度接近零，容易导致梯度消失
$$
\sigma(x) = \frac{1}{1 + e^{-x}}
$$
Tanh: 输出范围为(-1, 1)，更适合处理带有正负的信号，但仍存在梯度消失问题
$$
\tanh(x) = \frac{e^x - e^{-x}}{e^x + e^{-x}}
$$
ReLU: 输出范围为(0, +∞)，计算简单，没有梯度消失问题，但是会导致神经元死亡
$$
f(x) = \max(0, x)
$$
Leaky ReLU: 在x < 0时引入小斜率，解决ReLU的“死亡神经元”问题
$$
f(x) = \begin{cases}
x, & x > 0 \\
\alpha x, & x \leq 0
\end{cases}
$$
![](https://dasi-blog.oss-cn-guangzhou.aliyuncs.com/MachineLearning/chapter1-18/202501131224710.png)

### 损失函数

对于回归任务，利用均方误差
$$
L_\text{MSE} = \frac{1}{n} \sum_{i=1}^n (y_i - \hat{y}_i)^2
$$
对于分类任务，利用负对数似然
$$
L_\text{CrossEntropy} = - \sum_{i=1}^n y_i \log \hat{y}_i
$$
### 反向传播

1. 前向传播：计算每层的激活值和输出
2. 计算损失：通过损失函数衡量预测值与真实值的差异
3. 反向传播：依次计算每一层的梯度：
4. 权重更新：通过梯度下降调整每一层的权重和偏置
$$
\mathbf{w}_{t+1} = \mathbf{w}_t - \eta \cdot \nabla L
$$
### 典型神经网络

卷积神经网络（CNN）：用于图像数据
- 卷积层：提取局部特征，实现参数共享，每一个卷积核对应一种特征
- 激活函数层：引入非线性，增强模型的表达能力
- 池化层：提取主要特征，减少数据维度
- 全连接层：综合全局信息，完成任务输出

卷积和池化对尺寸的影响：输入图像的尺寸为$h$，卷积核/池化核的尺寸为$k$，填充大小为$p$，步长为$s$，那么输出图像的尺寸为
$$
\left\lfloor \frac{h + 2p - k}{s} \right\rfloor + 1
$$
![](https://dasi-blog.oss-cn-guangzhou.aliyuncs.com/MachineLearning/chapter1-18/202501131224706.png)

循环神经网络（RNN）：用于序列数据，引入隐藏状态$h_t$，捕捉序列数据中的时间序列依赖关系
$$
\mathbf{h}_t = f(\mathbf{W}_{xh} \mathbf{x}_t + \mathbf{W}_{hh} \mathbf{h}_{t-1} + \mathbf{b}_h)\\[1em]
\mathbf{y}_t = g(\mathbf{W}_{hy} \mathbf{h}_t + \mathbf{b}_y)
$$
![](https://dasi-blog.oss-cn-guangzhou.aliyuncs.com/MachineLearning/chapter1-18/202501131224707.png)

长短期记忆网络（LSTM）：在 RNN 的基础上引入遗忘门、输入门和输出门，解决长期依赖问题

![](https://dasi-blog.oss-cn-guangzhou.aliyuncs.com/MachineLearning/chapter1-18/202501131224708.png)

### Transformer

Transformer结构由**编码器-解码器**架构组成，每部分由多个堆叠的层组成，利用**自注意力机制**和**并行处理**来捕获序列中任意位置的依赖关系

自注意力机制：计算序列中每个元素与其他元素的相关性，生成依赖关系的权重
- Q：查询矩阵，表示当前元素需要关注的元素（需求，问题）
- K：键矩阵，表示当前元素能够提供的信息（供给，答案）
- V：值矩阵，Q和K越匹配，注意力分数越大，值进行加权
$$
\text{Attention}(Q, K, V) = \text{softmax}\left(\frac{QK^T}{\sqrt{d_k}}\right)V
$$
位置编码：通过正弦和余弦函数将序列的位置信息加入到输入特征中，使模型能够感知序列顺序
$$
\text{PE}(pos, 2i) = \sin\left(\frac{pos}{10000^{2i/d_{model}}}\right)\\[1em]
\text{PE}(pos, 2i+1) = \cos\left(\frac{pos}{10000^{2i/d_{model}}}\right)
$$
多头注意力：通过并行计算多个注意力头，捕获输入不同维度的特征关系，最会将所有头的输出拼接起来，并通过线性变换得到最终输出

编码器
1. 输入嵌入与位置编码：将输入序列通过嵌入层映射到连续向量空间，并加上位置编码
2. 多头自注意力：计算每个词与序列中其他词的关系，提取特征
3. 前馈网络：两层全连接网络，用于非线性变换和特征提取
4. 残差连接与归一化：每个子层后加入残差连接，并进行层归一化以稳定训练

解码器
1. 目标嵌入与位置编码：对目标序列进行嵌入和位置编码
2. 掩盖多头自注意力：计算目标序列中每个词的依赖关系，并通过遮掩机制防止未来信息泄露
3. 编码器-解码器注意力：结合编码器的输出与目标序列的嵌入，捕获目标与输入之间的关系
4. 前馈网络与输出生成：通过全连接网络进行特征变换，并用 softmax 生成目标序列的概率分布

![](https://dasi-blog.oss-cn-guangzhou.aliyuncs.com/MachineLearning/chapter1-18/202501131224709.png)

## 支持向量机

### 最大间隔分类器

支持向量机的特殊之处在于，它不仅仅是找到一个超平面能分割样本点，还渴望找到所有可行超平面中最优的超平面，支持向量机通过计算离超平面最近的点到超平面的距离，然后最大化这个距离，即**最大化数据点和超平面的最小间隔**来定义最优：$\max_{w,b} \frac{1}{\|\mathbf{w}\|} \min_{i} y_i (\mathbf{w}^T \mathbf{x}_i + b)$

![](https://dasi-blog.oss-cn-guangzhou.aliyuncs.com/MachineLearning/chapter1-18/202501022056996.png)

### 优化分析

首先超平面的表达式如下，其中$\mathbf{w}$表示超平面的法向量，$b$表示超平面到原点的偏移
$$
\mathbf{w}^T \mathbf{x} + b = 0
$$
首先我们需要明确，需要优化的是距离超平面最近的点到超平面的距离，而不是所有点到超平面距离的总和，我们将这些点称作**支持向量**，支持向量到超平面的距离定义如下，其中分子$|\mathbf{w}^T \mathbf{x}_i + b|$是数据向量在超平面法向量方向上的投影，分母$\|\mathbf{w}\|$是法向量的长度
$$
d = \frac{| \mathbf{w}^T \mathbf{x}_i + b |}{\|\mathbf{w}\|} \quad \forall i \in \text{支持向量}
$$
如果直接对这个$d$去优化，涉及分子和分母的比值，这会带来复杂的非线性优化问题，因此我们可以假设所有支持向量都满足以下条件
$$
|\mathbf{w}^T \mathbf{x} + b| = 1
$$
那么就有$\mathbf{w}^T \mathbf{x} + b = 1$是正类支持向量所在的超平面，$\mathbf{w}^T \mathbf{x} + b = -1$是负类支持向量所在的超平面，两个分类超平面到决策超平面的间隔都是$\frac{1}{\|\mathbf{w}\|}$，因此分类间隔就是两个超平面的间隔，优化目标就是最大化这个分类间隔
$$
\max_{\mathbf{w}, b} = \frac{2}{\|\mathbf{w}\|}
$$
优化目标是最大化这个分类间隔，但是为了满足标准格式同时方便计算，我们转化优化目标为
$$
\min_{\mathbf{w}, b} \frac{1}{2} \|\mathbf{w}\|^2
$$
为了确保正确分类，所有样本点都需要满足约束
$$
\text{正样本：}(\mathbf{w}^T \mathbf{x}_i + b) \geq 1\\
\text{负样本：}(\mathbf{w}^T \mathbf{x}_i + b) \leq 1
$$
在支持向量机中，我们可以规定正负样本的标签值是1和-1而不是1和0，这样就可以将约束条件简化为
$$
y_i (\mathbf{w}^T \mathbf{x}_i + b) \geq 1, \quad  \forall i \in \text{样本}
$$
综上，支持向量机的优化目标就是
$$
\min_{\mathbf{w}, b} \frac{1}{2} \|\mathbf{w}\|^2 \quad \text{s.t.} \quad y_i (\mathbf{w}^T \mathbf{x}_i + b) \geq 1, \forall i
$$
### 软间隔

上述支持向量的定义是所有数据点到超平面距离中最小的一个，也称为**硬间隔**。然而硬间隔可能会导致模型过于复杂，甚至无法找到一个能够满足所有样本点的超平面。

因此有一种**软间隔**的方式，允许样本点出现在对应分类超平面的另一侧，同时设置容忍程度和惩罚项，也就是**引入了松弛变量和添加正则化项，平衡间隔最大化与分类错误的代价**。
$$
\min_{\mathbf{w}, b, \xi} \frac{1}{2} \|\mathbf{w}\|^2 + C \sum_{i=1}^n \xi_i, \quad \text{s.t.} \quad y_i (\mathbf{w}^T \mathbf{x}_i + b) \geq 1 - \xi_i, \quad \xi_i \geq 0, \quad \forall i
$$
![](https://dasi-blog.oss-cn-guangzhou.aliyuncs.com/MachineLearning/chapter1-18/202501022056997.png)

{% note warning flat %}
需要注意的是，软间隔只是在一定程度上**缓解线性不可分，它实际上还是用了线性超平面**
{% endnote %}

### 核函数

如果数据在二维空间无法分开，我们可以将数据从低维特征空间映射到高维特征空间，以便在高维空间中实现更好的分类效果

核函数$K(\mathbf{x}_i, \mathbf{x}_j)$的本质上是在低维空间中计算高维映射后的点积值，而无需显式地进行高维映射
- 线性：$K(\mathbf{x}_i, \mathbf{x}_j) = \mathbf{x}_i \cdot \mathbf{x}_j$
- 多项式：$K(\mathbf{x}_i, \mathbf{x}_j) = (\mathbf{x}_i \cdot \mathbf{x}_j + c)^d$
- 高斯：$K(\mathbf{x}_i, \mathbf{x}_j) = \exp\left(-\frac{\|\mathbf{x}_i - \mathbf{x}_j\|^2}{2\sigma^2}\right)$
- sigmoid：$K(\mathbf{x}_i, \mathbf{x}_j) = \tanh(\alpha \mathbf{x}_i \cdot \mathbf{x}_j + c)$

### 损失

通过定义一个中间变量$z = y \cdot h(x) = y \cdot (\mathbf{w}^T \mathbf{x} + b)$来统一分析不同的损失

理想损失：无穷大的惩罚会导致优化问题不可解
- 当正确分类即z >= 1时：损失为0
- 当错误分类即z < 1时：损失为无穷大

对数损失：关注所有样本点，适用于概率模型
- 当正确分类即z >= 1时：无论z多大，损失都很接近于log1即0
- 当错误分类即z < 1时：z越小，损失迅速增大
$$
E_{\text{LR}}(z) = \log(1 + \exp(-z))
$$
hinge损失：强调分类间隔，只对支持向量进行惩罚
- 当正确分类即z >= 1时：无论z多大，损失都是0
- 当错误分类即z < 1时：损失随着z变小而线性增大
$$
E_{\text{SV}}(z) = \max(0, 1 - z)
$$
可以看出，支持向量机只对$z <= 1$的向量惩罚，这些向量是落在分类边界或间隔边界上的点，被称为支持向量，而$z \geq 1$的非支持向量位于间隔边界外，不影响分类边界的位置或者影响很小。

## 训练技巧

### 梯度算法

SGD：随机抽样，只用部分数据来计算梯度，减小计算复杂度，但是收敛速度慢，容易陷入局部最优
$$
\mathbf{w}_{t+1} = \mathbf{w}_t - lr \cdot \nabla f(\mathbf{w}_t)
$$
SGD Momentum：在SGD的基础上，引入“动量”，将历史梯度也考虑进来，加速收敛
$$
\mathbf{v}_t = \rho \mathbf{v}_{t-1} + \nabla f(\mathbf{w}_t)\\
\mathbf{w}_{t+1} = \mathbf{w}_t - lr \cdot \mathbf{v}_t
$$
RMSProp：在SGD的基础上，加权平均梯度平方，动态调整学习率，解决不同维度梯度尺度不一致的问题
$$
\mathbf{s}_t = \rho \mathbf{s}_{t-1} + (1 - \rho) (\nabla f(\mathbf{w}_t))^2\\
w_{t+1} = w_t - \frac{lr}{\sqrt{s_t}} \cdot \nabla f(\mathbf{w}_t)
$$
Adam：综合了Momentum和RMSProp的优点，既引入历史梯度，又动态调整学习率
$$
\mathbf{m}_t = \beta_1 \mathbf{m}_{t-1} + (1 - \beta_1)\nabla f(\mathbf{w}_t)\\
\mathbf{s}_t = \beta_2 \mathbf{s}_{t-1} + (1 - \beta_2)(\nabla f(\mathbf{w}_t))^2\\
\mathbf{w}_{t+1} = \mathbf{w}_t - \frac{lr}{\sqrt{\mathbf{s}_t}} \cdot \mathbf{m}_t
$$
### 预处理

预处理：在特征尺度差异较大的情况下，提升优化过程中的梯度收敛速度
- 居中化：减去均值，使数据分布以零为中心，$x_i{\prime} = x_i - \mu$
- 标准化：标准化方差，使每个特征的范围一致，$x_i{\prime} = \frac{x_i - \mu}{\sigma}$
- 白化：使数据具有单位协方差矩阵，消除特征之间的相关性

对于大规模数据集，直接对整个数据集进行一次性预处理可能**计算复杂度过高，也可能随着数据分布变化而失效**，可以在每次训练前，对单一批次进行预处理

### 初始化权重

合理的权重初始化可以避免梯度消失或梯度爆炸问题，并使网络更快地达到收敛

对于浅层网络，**使用高斯分布初始化权重，打破对称性，确保每个神经元的初始输出不同，从而学习到不同的特征**

对于深层网络，可以根据前一层神经元数量调整高斯分布的方差$\sigma_w^2 = \frac{1}{n_{\text{in}}}$，**保证正向传播中输入和输出方差一致，避免因方差不匹配导致的梯度爆炸或消失**

### Dropout

训练阶段：按照概率p，随机丢弃一定比例的神经元
- 防止过拟合，适当降低模型复杂度，增强泛化能力
- 模拟集成学习，相当于在训练多个子网络

测试阶段：将每个神经元的输出乘上1-p，按比例缩小神经元输出
- 因为神经元以概率1-p被保留，保持期望输出的一致性
- 测试必须稳定，不能随意丢弃神经元

![](https://dasi-blog.oss-cn-guangzhou.aliyuncs.com/MachineLearning/chapter1-18/202501022056000.png)

### 超参数调优

超参数是需要在训练之前设置的参数，它们不会在模型训练过程中更新，比如学习率、批次大小、dropout比例、隐藏层数目、神经元数量等

数据集划分：在训练集上训练模型，在验证集上调整超参数，在测试集上评估最终性能
![](https://dasi-blog.oss-cn-guangzhou.aliyuncs.com/MachineLearning/chapter1-18/202501022056001.png)

网格搜索（Grid Search）：枚举所有可能的参数的排列组合，通过交叉验证评估每个组合的性能，从而学习最佳超参数。

## 决策树

### 结构

决策树：适用于有标签的分类任务，通过递归地选择特征属性，将数据集划分为子集，最终将数据分类到不同的类别中
![](https://dasi-blog.oss-cn-guangzhou.aliyuncs.com/MachineLearning/chapter1-18/202501022056002.png)
![](https://dasi-blog.oss-cn-guangzhou.aliyuncs.com/MachineLearning/chapter1-18/202501022056003.png)

结构
- 内部节点：属性
- 边：属性的取值
- 叶节点：分类结果
- 分支：根据节点属性和边的取值对数据集进行划分
- 路径：决策依据和决策结果，可以看作为一系列if-else的规则集合

### 如何选择划分属性？

熵：是一种用来衡量目标变量不确定性的度量，熵值越大，说明数据集的分类结果越混乱、不稳定

分类目标：每次划分数据时的目标是找到一个属性，使得**划分后的子数据集尽可能纯净，即能够最大程度地降低数据集的熵**

在决策树中，目标变量Z是标签
$$
H(Z) = -\sum_{i=1}^{n} p_i \log(p_i)
$$
条件熵：在属性Y被用作划分后标签的熵
$$
H(Z|Y) = \sum_{y \in Y} P(Y=y) H(Z|Y=y)
$$
信息增益：熵降低的量化指标，反映了某个属性在分类中提供的信息量，即原始标签熵 - 利用属性Y进行划分后的熵，**信息增益越大，某个属性的信息量越多，应该被用来作为决策树的内部节点**
$$
IG(Y) = H(Z) - H(Z|Y)
$$
### 如何构建决策树

1. 计算每个属性的信息增益，**选择信息增益最大的属性作为当前划分节点**
2. 根据该属性的不同取值，将数据集划分为多个子集，并为每个子集生成一个子节点
3. 对每个子节点重复上述过程，选择下一个属性进行扩展，**同一条分支上，一个属性不能重复作为划分属性**
4. 停止条件
   1. 所有剩余实例的标签相同
   2. 没有更多属性可供选择
   3. 树的深度达到预设的最大值
   4. 信息增益小于某个阈值

### 剪枝

- 预剪枝：最大深度，最多子节点个数，最小节点包含样本数，最小节点信息增益
- 后剪枝：在树构建完成后，基于验证集的表现，移除贡献较低的分支

## 集成学习

集成学习：结合多个弱分类器来构建一个强分类器
- 弱分类器：在部分数据上表现较好，但在整个数据集上表现一般
- 强分类器：在整个数据集上表现良好，但是学习起来十分复杂

重点在于：如何构造弱分类器？如何结合弱分类器？

### Bagging

核心思想：通过**自助采样**生成多个子数据集，并在每个子数据集上训练一个分类器，最终通过多数投票或平均来结合这些分类器的预测结果
1. 从训练集中有放回地随机抽取N个样本，重复K次，得到K个子数据集
2. 在每个子数据集上训练一个分类器
3. 将所有分类器的预测结果通过多数投票或平均来得到最终预测

![](https://dasi-blog.oss-cn-guangzhou.aliyuncs.com/MachineLearning/chapter1-18/202501022056005.png)

存在问题：如果分类器之间的错误模式相似，投票机制无法显著提高整体性能，需要引入额外的随机性，从而减少分类器之间的相关性

随机森林：使用决策树模型作为弱分类器，在 Bagging 的基础上，每次划分节点时，**随机选择部分特征（而非所有特征）进行划分，降低树的相关性**

![](https://dasi-blog.oss-cn-guangzhou.aliyuncs.com/MachineLearning/chapter1-18/202501022056006.png)

### Boosting

核心思想：使用同一个数据集进行多次迭代，每次迭代让当前弱分类器关注前一个弱分类器犯的错误，从而逐步优化自己

AdaBoost算法

1. 初始化样本权重为同一值 -> 保证第一轮的训练公平，所有样本对模型的贡献相同
$$
w_i = \frac{1}{n} 
$$
2. 计算当前样本权重弱学习器的分类误差 -> 衡量当前弱分类器的性能，误差越小，弱分类器效果越好
    - $\mathbb{I}(h_t(x_i) \neq y_i)$是指示函数，当分类器预测错误时值为1，否则值为0
    - 误差 $\varepsilon_t$是错误样本的权重之和
$$
\varepsilon_t = \frac{\sum_{i=1}^n w_i \cdot \mathbb{I}(h_t(x_i) \neq y_i)}{\sum_{i=1}^n w_i}
$$
3. 根据弱分类器的错误率$\varepsilon_t$，计算其在最终强分类器中的权重 -> 赋予性能较好的弱分类器更大的权重，影响最终强分类器的决策
    - 如果$\varepsilon_t < 0.5$：分类器正确率高于随机猜测，权重为正且较大
    - 如果$\varepsilon_t > 0.5$：分类器表现差于随机猜测，权重为负且较小
    - 如果$\varepsilon_t = 0.5$：分类器效果等同随机猜测，权重为 0
$$
\alpha_t = \frac{1}{2} \ln \left(\frac{1 - \varepsilon_t}{\varepsilon_t}\right)
$$
4. 根据当前弱分类器的表现调整样本权重 -> 增加分类错误样本的权重，让下一轮弱分类器更多关注这些样本
    - 分类正确，指数项为负，减小权重
    - 分类错误，指数项为正，增大权重
    - 弱分类器性能较好时，它的决策对样本权重的调整影响更大
    - 弱分类器性能较差时，它的决策对样本权重的调整影响较小
$$
w_i \leftarrow w_i \cdot \exp\left(\alpha_t \cdot -(y_i \cdot h_t(x_i))\right)
$$
5. 通过所有弱分类器的加权投票，得到最终的强分类器 -> 将多个弱分类器的优势结合起来，提升整体分类性能
$$
H(x) = \text{sign} \left( \sum_{t=1}^T \alpha_t \cdot h_t(x) \right)
$$
{% note warning flat %}
弱分类器的权重不需要归一化，但是样本权重需要归一化
{% endnote %}

![](https://dasi-blog.oss-cn-guangzhou.aliyuncs.com/MachineLearning/chapter1-18/202501022056007.png)

## 线性降维：PCA

为什么需要降维

- **缓解维度灾难**：许多数据的维度非常高，直接处理会导致计算复杂度急剧增加
- **减少噪声**：高维数据中可能包含许多无关或冗余特征，需要提取数据的主要特征，增强信号的清晰度
- **提高数据可视化**：样本在高维空间中变得稀疏，降维可以直观地理解数据的分布，更好地观察数据的聚类特性或分类边界

![](https://dasi-blog.oss-cn-guangzhou.aliyuncs.com/MachineLearning/chapter1-18/202501022056008.png)

PCA原理
- **最大化投影方差**：找到一组正交方向，使得数据在这些方向上的投影方差最大 -> 最大程度保留数据的分布信息 -> 最佳正交方向$u_i$是协方差矩阵的特征向量
$$
\max u_i^T S u_i
$$
- **最小化投影误差**：找到一组正交方向，使得数据在这些方向上的投影能够最小化重构误差 -> 最大程度保留数据的数值信息 -> 最佳正交方向$u_i$是协方差矩阵的特征向量
$$
\min \|x - \sum_{i=1}^M (u_i^T)xu_i\|^2
$$
PCA的算法步骤
1. 将数据的每个特征减去其均值，使得数据的均值为0，得到中心化的数据矩阵
2. 计算协方差矩阵：$S = \frac{1}{N}X^TX$
3. 对协方差矩阵S进行特征值分解，得到特征值和特征向量
4. 按照特征值从大到小排序，选择前M个特征值对应的特征向量作为主成分方向
5. 将原始数据投影到选定的主成分方向上，得到降维后的数据

奇异值分解：任意矩阵A都满足以下式子
- U：列向量是数据的主成分方向
- $\Sigma$：对角矩阵，其对角线元素是奇异值，表示每个主成分方向的重要性
- $V^T$：列向量是数据的主成分方向
$$
A = U \Sigma V^T
$$
![](https://dasi-blog.oss-cn-guangzhou.aliyuncs.com/MachineLearning/chapter1-18/202501022056009.png)

## 聚类：K-means

聚类：将一组数据实例划分为不同的簇，**使得同一簇内的实例相似度高，不同簇之间的实例相似度低**

应用场景
- 图像分组与分割
- 文档聚类和语义分析
- 社交网络人群划分
- 相似基因判断
- 市场细分

K-means流程
1. 随机选择 K 个数据点作为初始质心
2. 将每个数据点分配到距离最近的质心所属的簇
3. 重新计算每个簇的质心，即计算簇内数据点的均值
4. 重复分配和更新步骤，直到质心收敛或达到最大迭代次数

![](https://dasi-blog.oss-cn-guangzhou.aliyuncs.com/MachineLearning/chapter1-18/202501022056010.png)

目标函数：最小化所有数据点与其所属簇质心的距离之和，其中$r_ik$是指示函数，表示第i个样本是否属于簇k，目标函数是**单调减少**的，因此保证收敛
$$
J = \sum_{i=1}^{N} \sum_{k=1}^{K} r_{ik} \| \mathbf{x}i - \mu_k \|^2
$$
改进一：超参数簇的数量K如何选择？
- 簇数量太少：聚类效果差
- 簇数量太多：过拟合
- 肘部法（Elbow）：通过绘制簇数量K与目标函数J的关系曲线，选择曲线减缓的点作为最佳K值

![](https://dasi-blog.oss-cn-guangzhou.aliyuncs.com/MachineLearning/chapter1-18/202501022056011.png)

改进二：初始质心如何选择？
- 随机选择：完全随机选择点作为质心，质心可能分布十分不均匀，训练速度慢，收敛到局部最优解，分类性能差
- 距离选择：选择距离现有质心最远的点：可能选择到异常点
- 结合随机和距离：**距离越远的点越有可能被选中**

Kmeans++流程
1. 从数据集中随机选取一个点作为第一个簇中心
2. 对于数据集中每个点x，计算其与当前所有簇中心中最近簇中心的距离
3. 每个点被选择为簇中心的概率与其距离平方成正比，计算全部数据的概率分布
$$
    P(x) = \frac{D(x)^2}{\sum_{x{\prime} \in X} D(x{\prime})^2}
    $$
4. **随机取一个0-1的数，落到哪个区间，就选择哪个点作为新的质心**
5. 重复2-4步，直到选择出K个簇中心

改进三：分配方式
- 硬分配：每个数据点确定性地属于一个簇
- 软分配：使用概率或权重表示样本与每个簇的关联程度

Soft-Kmeans流程
1. 选择初始的K个质心
2. 计算隶属度，即当前样本n属于簇k的概率，其中$\beta$控制软分配程度的参数，值越大，分配越接近硬划分
    $$
    r_{ik} = \frac{\exp(-\beta \cdot ||x_i - \mu_k||^2)}{\sum_{j=1}^K \exp(-\beta \cdot ||x_i - \mu_j||^2)}
    $$
3. 根据隶属度更新每个簇的中心
    $$
    \mu_k = \frac{\sum_{i=1}^n r_{ik} \cdot x_i}{\sum_{i=1}^n r_{ik}}
    $$
4. 重复执行2-3步，直到簇中心不再发生显著变化或达到最大迭代次数

局限性
- Kmeans对异常值十分敏感
- **欧氏距离假设簇是球形的，对不规则形状的聚类效果差**

## 隐变量模型

### LVM

隐变量：不是直接给出来的数据，但对数据分布有潜在影响的随机变量，主要用于**构建复杂模型和揭示隐藏结构**

{% note warning flat %}
实际上我们假设隐变量的含义，但无法完全解释隐变量
{% endnote %}

隐变量模型：包含显变量x和隐变量z，通过概率分布描述数据
- 先验分布$p(\mathbf{z})$：隐变量的概率分布
- 条件分布$p(\mathbf{x}|\mathbf{z})$：隐变量对显变量的作用效果
- 联合分布$p(\mathbf{x}, \mathbf{z}) = p(\mathbf{z}) p(\mathbf{x}|\mathbf{z})$：隐变量和显变量共同作用效果
- 边缘分布$p(\mathbf{x}) = \int p(\mathbf{x}, \mathbf{z}) d\mathbf{z}$：显变量的作用效果
- 后验分布$p(\mathbf{z}|\mathbf{x}) = p(\mathbf{x}, \mathbf{z})/p(\mathbf{x})$：显变量对隐变量的作用效果

隐变量模型的学习目标：让观测数据尽可能地符合边际分布，也就是找到一组最优参数来**最大化对数边际似然**：$\max_{\theta} \sum_{i=1}^N \log p(\mathbf{x}_i)$

取对数：因为对概率的连乘计算复杂度太高，且容易导致数值溢出，通过取对数，将乘法变为加法，不仅降低了计算复杂度，还提高了数值稳定性

### Gaussian LVM

高斯隐变量模型
1. 假设观测变量由隐变量和高斯噪声线性组合而成：$x = \mu + Wz + \epsilon$，且$\epsilon \sim \mathcal{N}(0, \sigma^2 I)$
2. 假设隐变量服从零均值，单位协方差矩阵的高斯分布（先验分布）：$p(z) = \mathcal{N}(z; 0,I)$
3. 给定隐变量的时候，观测变量也服从高斯分布（条件分布）：$p(x|z) = \mathcal{N}(x; Wz + \mu, \sigma^2 I)$
4. 观测变量的整体分布仍是高斯分布（边际分布）：$p(x) = \int p(x|z)p(z) dz = \mathcal{N}(x; \mu, WW^T + \sigma^2 I)$

### GMM

高斯混合模型：观测变量的分布是多个高斯分布的加权和：$p(x) = \sum_{k=1}^K \pi_k \mathcal{N}(x | \mu_k, \Sigma_k)$
-  $\pi_k$：混合权重，反映了第k个高斯分布在整体模型中的贡献度/参与度/责任值
-  $\mu_k, \Sigma_k$：是第k个高斯分布的均值和协方差矩阵

GMM的隐变量
- 不是一个连续的高斯分布变量，而是一个离散变量：假如说有K个高斯分布，则隐变量表示为$z_i = [z_1, z_2, \dots, z_K]$
- 隐变量的概率分布：$p(z_k = 1) = \pi_k, \quad \sum_{k=1}^K \pi_k = 1$，表示数据属于第k个高斯分布的概率

GMM的隐变量模型
- 先验分布：$p(z_k = 1) = \pi_k$
- 条件分布：$p(x | z_k = 1) = \mathcal{N}(x | \mu_k, \Sigma_k)$
- 联合分布：$p(x,z) = \pi_k\mathcal{N}(x | \mu_k, \Sigma_k)$
- 边际分布：$p(x) = \sum_{k=1}^K \pi_k \mathcal{N}(x | \mu_k, \Sigma_k)$
- 后验分布：$p(z_k = 1 | x) = \frac{\pi_k \mathcal{N}(x | \mu_k, \Sigma_k)}{\sum_{j=1}^K \pi_j \mathcal{N}(x | \mu_j, \Sigma_j)}$

GMM的学习目标
1. **最大化数据的对数边缘似然函数**来优化模型参数，其中N是样本数，K是高斯分布数：$\max_{\{\pi_k, \mu_k, \Sigma_k\}_{k=1}^K } \sum_{i=1}^Nlog(\sum_{k=1}^K \pi_k \mathcal{N}(x_i|\mu_k, \Sigma_k))$
2. 学习**隐变量的最佳后验分布**，即得到描述每个数据点属于每个高斯分布的最合适概率，从而实现软分配聚类

### 其他LVM

**隐马尔可夫模型（Hidden Markov Model, HMM）**：用于序列数据，隐变量挖掘状态对时间的依赖关系，应用于语音识别、时间序列分析

**信念网络（Sigmoid Belief Networks, SBN）**：用于图像生成，挖掘高维数据的分布和结构，应用于图像生成和修复

**隐狄利克雷分布（Latent Dirichlet Allocation, LDA）**：用于文本数据，挖掘文本中的潜在主题结构，应用于主题建模和文本分析

### EM算法

隐变量模型的学习目标是最大化观测变量的对数边际似然$\log p(x; \theta)$，这里的$\theta=\{\pi_k, \mu_k, \Sigma_k\}$
- 连续：$\log p(x; \theta) = \log \int p(\mathbf{x}, \mathbf{z}; \theta) d\mathbf{z}$
- 离散：$\log p(x; \theta) = \log \sum_z p(x, z; \theta)$

但是直接求参数的最优解是不现实的，因此我们采取迭代优化的方式，即EM算法
1. E步：在第t次迭代时，使用当前模型参数$\theta^{(t)}$ ，计算隐变量z的后验分布
    $$
    \gamma_{ik} = p(z_i = k | x_i; \theta^{(t)}) = \frac{p(x_i, z_i = k; \theta^{(t)})}{p(x_i; \theta^{(t)})} = \frac{\pi_k \mathcal{N}(x | \mu_k, \Sigma_k)}{\sum_{j=1}^K \pi_j \mathcal{N}(x | \mu_j, \Sigma_j)}
    $$
2. E步：用后验分布计算联合对数似然的期望
    $$
    \begin{aligned}
    Q(\theta; \theta^{(t)}) &= \int p(z | x; \theta^{(t)}) \cdot \log p(x, z; \theta) \, dz \\
    &= \int p(z | x; \theta^{(t)}) \cdot \big[ \log p(x | z; \theta) + \log p(z; \theta) \big] \, dz \\
    &= \int p(z | x; \theta^{(t)}) \cdot \log p(x | z; \theta) \, dz + \int p(z | x; \theta^{(t)}) \cdot \log p(z; \theta) \, dz
    \end{aligned}
    $$
3. M步：最大化 Q 函数以更新参数
    $$
    \theta^{(t+1)} = \arg \max_{\theta} Q(\theta; \theta^{(t)})\\[1em]
    \pi_k = \frac{\sum_{i=1}^N \gamma_{ik}}{N}\\[1em]
    \mu_k = \frac{\sum_{i=1}^N \gamma_{ik} x_i}{\sum_{i=1}^N \gamma_{ik}}\\[1em]
    \Sigma_k = \frac{\sum_{i=1}^N \gamma_{ik} (x_i - \mu_k)(x_i - \mu_k)^T}{\sum_{i=1}^N \gamma_{ik}}
    $$
4. 当对数似然$\log p(x; \theta)$收敛时停止

最关键的步骤在于Q函数的引入，因为直接优化$\log p(x; \theta)$计算复杂，包含隐变量的求和/积分，而**先求出后验概率，再用后验概率求期望，可以将隐变量的影响“分离”到期望计算中**，优化变得简单

## 表示学习

### 定义

什么是表示学习：将任意格式的数据（如图像、文本、语音等）表示在低维向量空间中，目的是保留数据的**关键特征信息**，而不是所有信息
- **数据压缩**：特征更加紧凑，减少了存储和计算的开销
- **提升效率**：丢弃无关信息，只保留重要的语义信息
- **通用性**：可以用于多种下游任务，如分类、聚类、相似性搜索、异常检测等

### 图像表示

卷积神经网络：**卷积层+池化层+全连接层**提取图像的局部特征，并将这些特征组合成更高层次的语义表示
![](https://dasi-blog.oss-cn-guangzhou.aliyuncs.com/MachineLearning/chapter1-18/202501022056013.png)

自编码器：PCA就可以看作成一种线性自编码器，通过线性变换将数据映射到低维空间
![](https://dasi-blog.oss-cn-guangzhou.aliyuncs.com/MachineLearning/chapter1-18/202501022056014.png)

生成模型：从数据中学习其潜在的概率分布，并基于学习到的分布生成与训练数据相似的样本
![](https://dasi-blog.oss-cn-guangzhou.aliyuncs.com/MachineLearning/chapter1-18/202501022056015.png)

对比学习：**构造正样本对（对同一个图片进行旋转、遮挡、裁剪、翻转、颜色抖动等操作）和负样本对（不同的两张图）**，最大化正样本对之间的相似性，最小化正样本对与负样本对之间的相似性，从而学习到能够反映数据的特征表示
![](https://dasi-blog.oss-cn-guangzhou.aliyuncs.com/MachineLearning/chapter1-18/202501022056016.png)

### 文本表示

#### 传统方法

one-hot：每个词用一个独热向量表示，句子表示为独热向量的拼接
![](https://dasi-blog.oss-cn-guangzhou.aliyuncs.com/MachineLearning/chapter1-18/202501022056017.png)

BOW（Bag Of Word）：忽略词序，仅记录词频
![](https://dasi-blog.oss-cn-guangzhou.aliyuncs.com/MachineLearning/chapter1-18/202501022056018.png)

**w表手单词word，d表示单个文件document，D表示文件集合Documents**
- 词在单个文档中出现的频率（Term Frequency, TF）：词如果出现在同一个文档中的次数越多，从而说明价值越高
    $$
    \text{TF}(w, d) = \frac{\text{num of w in d}}{\text{num of d}}
    $$
- 词在整个文档集合中的普遍程度（Inverse Document Frequency, IDF）：**词如果出现在不同文档的次数越多，反而说明价值越低**
    $$
    \text{IDF}(w, D) = log(\frac{\text{num of D}}{1 + \text{num of w in D}})
    $$
- TF-IDF：纵观全局，衡量词的重要性
    $$
    \text{TF-IDF}(w, d, D) = \text{TF}(w, d) \times \text{IDF}(w, D)
    $$

![](https://dasi-blog.oss-cn-guangzhou.aliyuncs.com/MachineLearning/chapter1-18/202501022056019.png)

上述方法的局限性：**维度高，稀疏，繁琐，无法反映词之间的语义相似性**

#### Word2Vec

- Skip-Grams：通过目标词预测上下文词，更注重局部关系，适合捕捉稀疏语料中的语义信息
- CBOW：通过上下文词预测目标词，更注重整体上下文，适合处理较小规模的数据集

![](https://dasi-blog.oss-cn-guangzhou.aliyuncs.com/MachineLearning/chapter1-18/202501022056020.png)

上述方法的局限性：**只注重邻近单词之间的联系，但不考虑整个句义，无法表达单词在不同语境下的多义性**

#### Sentence Embedding

ELMo：基于双向 LSTM 的语言模型，为每个词生成上下文相关的词向量，利用句子中的前后语境信息
![](https://dasi-blog.oss-cn-guangzhou.aliyuncs.com/MachineLearning/chapter1-18/202501022115081.png)

BERT：基于 Transformer 的预训练模型，输入词嵌入、段嵌入和位置嵌入，通过掩码语言模型和下一句预测任务进行预训练，生成上下文相关的词嵌入
- 掩码语言模型（MLM）：训练模型预测句子中被随机掩码的词
- 下一句预测（NSP）：训练模型判断两个句子是否是连续的

![](https://dasi-blog.oss-cn-guangzhou.aliyuncs.com/MachineLearning/chapter1-18/202501022056021.png)

## 生成模型

### 定义

生成模型也是一种隐变量模型，描述了数据的生成过程
- PCA：令隐变量是正交基向量，数据由正交基向量的线性组合而成
- GMM：令隐变量是软分配向量，数据由软分配向量的高斯分布加权组合而成

深度生成模型：将隐变量通过网络变换生成观测变量，建模能力更强，$p(\mathbf{x}, \mathbf{z}) = p(\mathbf{x}|T(\mathbf{z}))p(\mathbf{z})$，其中$T(\cdot)$表示神经网络的输出
![](https://dasi-blog.oss-cn-guangzhou.aliyuncs.com/MachineLearning/chapter1-18/202501022056022.png)

### KL散度

**用来衡量两个概率分布之间差异的一个非对称度量，又称为相对熵**，其中P是目标分布、Q是参考分布
- 离散：$\text{KL}(P \| Q) = \int P(x) \log \frac{P(x)}{Q(x)} dx$
- 连续：$\text{KL}(P \| Q) = \int P(x) \log \frac{P(x)}{Q(x)} dx$

由于神经网络的使用，深度生成模型的后验分布$p(\mathbf{z}|\mathbf{x}; \theta)$和联合概率均值都难以直接求解

### VB-EM框架

定义近似后验分布
$$
q_\phi(\mathbf{z}|\mathbf{x}) = \mathcal{N}(\mathbf{z}; \mu_\phi(\mathbf{x}), \sigma_\phi^2(\mathbf{x}))
$$

改变优化函数
$$
\mathcal{L}(\mathbf{x}; \theta, \phi) = \mathbb{E}_{q{\phi}(\mathbf{z}|\mathbf{x})} \left[ \log p_{\theta}(\mathbf{x}|\mathbf{z}) \right] - \text{KL}\left[q_{\phi}(\mathbf{z}|\mathbf{x}) \| p(\mathbf{z})\right]
$$

优化函数：
- 第一项是期望对数似然项：鼓励模型生成与数据一致的样本
- 第二项是KL散度项：作为正则化约束，鼓励近似后验分布与先验分布之间尽量相似

### MCMC技巧

- **采样**：为了近似地求出优化函数，我们可以从分布$q_\phi(\mathbf{z}|\mathbf{x})$中采样多组$\mathbf{z}^{(i)}$，然后用这些采样点的平均值来估计期望
- **重参数化**：随机采样是离散的点，不方便求梯度，因此可以将采样过程转换为一个可微分的形式：$\mathbf{z} = \mu_\phi(\mathbf{x}) + \sigma_\phi(\mathbf{x}) \cdot \epsilon$，其中，$\epsilon \sim \mathcal{N}(0, I)$是一个标准正态分布的随机变量，隐变量的随机性被显式地分离到$\epsilon$中，从而可以使用梯度下降优化

## 推荐系统

### 定义

推荐系统：帮助用户从大量物品（如商品、电影、音乐等）中找到他们可能感兴趣的物品，应用于电商平台（如亚马逊）、流媒体服务（如Netflix）、社交媒体（如YouTube）等

形式化模型
- 用户集合X，物品集合S，评分集合R
- 评分函数$u: X \times S \rightarrow R$
- 评分矩阵：用户对物品的评分矩阵，通常非常稀疏

### 基于内容

核心思想：根据用户历史喜欢的物品，推荐相似的物品
- **物品画像**：每个物品的特征向量
- **用户画像**：用户喜欢的物品画像的加权平均
- **预测评分**：计算用户画像与物品画像的相似度来预测评分

优点
- 个性化推荐
- 推荐具有可解释性

缺点
- 缺乏多样性，可能导致“信息茧房”
- 对复杂物品（音乐、图像）的绘制画像难度大

### 协同过滤

核心思想：通过用户之间或物品之间的相似性进行推荐
- 用户-用户协同过滤：利用相似用户对同一物品的评分来预测目标用户的评分
- 物品-物品协同过滤：利用同一用户对相似物品的评分来预测目标物品的评分

优点
- 推荐结果更加多样化
- 无需提取物品本身的特征

缺点
- **冷启动问题，新用户或新物品没有足够评分，无法进行有效推荐**
- **流行度偏差，倾向于推荐热门物品，无法推荐冷门物品**
- 随着用户和物品数量的增加，计算相似度的复杂度急剧上升

### 矩阵分解

核心思想：将用户-物品评分矩阵分解为两个低维矩阵，分别表示用户和物品的潜在特征
- 用户矩阵P：每行表示一个用户的潜在特征向量
- 物品矩阵Q：每行表示一个物品的潜在特征向量
- 预测评分：通过用户和物品的潜在特征向量的内积来预测评分

优点
- 泛化能力强，支持发现用户潜在的喜好
- 降维操作降低了计算复杂度，适合大规模数据

缺点
- **冷启动问题，新用户或新物品没有足够评分，无法进行有效推荐**
- 随着用户和物品数量的增加，分解复杂度增加

### 评估指标

- 均方根误差：预测评分与真实评分之间的差异
- 准确率：在推荐的物品中，被用户实际喜欢的物品所占的比例
- 召回率：用户实际喜欢的物品中，被推荐出来的比例
- 排名相关性：输出的物品排序与用户真实偏好排序之间的相关性
- 多样性：衡量推荐结果中物品之间的差异性
- 覆盖率：衡量推荐结果覆盖的物品和用户数量
- 推荐解释性：推荐结果是否可以解释并且被用户理解
- 体验友好性：用户是否满意推荐结果

## 异常检测

### 定义

异常检测（Anomaly）/ 离群点检测（Outlier）/ 新颖性检测（Novelty）：检测与大多数数据样本显著不同的数据样本，表现为**多样性高、无法明确表征、无法穷举**
- 点异常（Point）：单个数据点本身可被确定为异常
- 上下文异常（Contextual）：在特定上下文中，单个实例可能看起来异常
- 集体异常（Collective）：一组实例在一起检查时可能被视为异常
![](https://dasi-blog.oss-cn-guangzhou.aliyuncs.com/MachineLearning/chapter1-18/202501022056023.png)

### 方法

基于距离：将**远离大多数实例**的实例看作异常，计算到第k个最近邻居的距离，如果距离高于某个阈值，则视为异常
- 对k值敏感，难以找到好的距离度量
- 复杂度高$O(n^2)$

![](https://dasi-blog.oss-cn-guangzhou.aliyuncs.com/MachineLearning/chapter1-18/202501022056024.png)

基于密度：将**落在低密度区域的实例**看作异常，计算正常数据的概率密度分布，如果某个实例的概率低于阈值，则视为异常
- 计算复杂度高
- 可能没有很好的概率分布模型可以使用

![](https://dasi-blog.oss-cn-guangzhou.aliyuncs.com/MachineLearning/chapter1-18/202501022056025.png)

基于重构：将**无法重构的实例**看作异常，在正常数据实例上训练自编码器，如果某个实例无法很好被解码重构，则视为异常
- 需要大量正常数据进行训练
- 对未见过的正常样本也判定为异常

![](https://dasi-blog.oss-cn-guangzhou.aliyuncs.com/MachineLearning/chapter1-18/202501022056026.png)

基于单分类器：将**不在超球体内的实例**看作异常，利用支持向量构造决策边界，如果某个实例在边界之外，则视为异常
- 计算复杂度较高
- 难以选择核函数和参数

![](https://dasi-blog.oss-cn-guangzhou.aliyuncs.com/MachineLearning/chapter1-18/202501022056027.png)

### 评估

||实际为真|实际为假|
|-|-|-|
|预测为真|TP|FP|
|预测为假|FN|TF|

ROC曲线：以TPR为纵轴，FPR为横轴，绘制出的曲线，其面积用于衡量分类器的整体性能
- 真阳性率：检测出的正样本中实际为正的比例，$TPR = \frac{TP}{TP + FN}$
- 假阳性率：检测出的负样本中实际为正的比例，$FPR = \frac{FP}{FP + TN}$

PR曲线：以Precision为纵轴，Recall为横轴，绘制出的曲线，其面积用于评估分类器在检测异常点上的性能表现
- 精确率：检测出的正样本中实际为正的比例，$Precision = \frac{TP}{TP + FP}$
- 召回率：实际正样本中被正确检测出的比例，$Recall = \frac{TP}{TP + FN}$

F1分数：是精确率和召回率的调和平均数，用于综合评估分类器在平衡这两个指标时的性能表现
$$
F1 = 2 \cdot \frac{Precision \cdot Recall}{Precision + Recall}
$$

## 多模态学习

多模态学习：旨在同时处理和理解来自多种模态（例如文本、图像、音频、视频等）的数据，学习不同模态之间的关联与交互关系，以实现信息的有效融合和综合分析

Vision Transformer, ViT（图像理解）
1. 把图像拆成小块 patch，通过线性变换转换为向量，并加上位置嵌入以保留位置信息
2. 用 Transformer 模型处理向量，通过自注意力机制学习图像的整体表示
3. 通过一个 MLP 分类头输出图像的类别

![](https://dasi-blog.oss-cn-guangzhou.aliyuncs.com/MachineLearning/chapter1-18/202501022056028.png)

Contrastive Language–Image Pretraining, CLIP（图文对齐）
1. 图像通过图像编码器变成向量，文本通过文本编码器变成向量
2. 让匹配的图像和文本向量在空间中靠近，不匹配的远离
3. 模型能够将图像和文本映射到共享的向量空间中，实现跨模态检索和分类，通俗的来说，就是根据文本描述直接找到对应的图片或者根据图片生成对应的文字描述

![](https://dasi-blog.oss-cn-guangzhou.aliyuncs.com/MachineLearning/chapter1-18/202501022056029.png)

Bootstrapping Language-Image Pretraining, BLIP（图文生成）
1. 图像通过图像编码器变成向量，文本通过文本编码器变成向量
2. 对比学习：将匹配的图像和文本特征向量在共享的多模态空间中拉近距离，而将不匹配的特征向量推远
3. 生成学习：对输入图像生成描述性文本，过滤低质量、无意义或不相关的文本描述
4. 联合生成损失和对比损失，通过“自产自销”提升模型性能

![](https://dasi-blog.oss-cn-guangzhou.aliyuncs.com/MachineLearning/chapter1-18/202501022056030.png)