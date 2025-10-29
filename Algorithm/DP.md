# Dynamic Planning



   * [方法论](#方法论)
      * [DP 定义](#dp-定义)
      * [核心步骤](#核心步骤)
      * [类型区别](#类型区别)
   * [线性 DP](#线性-dp)
      * [最长上升子序列](#最长上升子序列)
      * [最大子数组和](#最大子数组和)
      * [最大子数组乘积](#最大子数组乘积)
      * [环形抢劫](#环形抢劫)
   * [划分 DP](#划分-dp)
      * [单词拆分](#单词拆分)
      * [回文串拆分](#回文串拆分)
   * [网格 DP](#网格-dp)
      * [最大正方形](#最大正方形)
      * [不同路径](#不同路径)
   * [树形 DP](#树形-dp)
      * [树形抢劫](#树形抢劫)
      * [二叉树中的最大路径和](#二叉树中的最大路径和)
   * [区间 DP](#区间-dp)
      * [回文子串个数](#回文子串个数)
      * [最长回文序列](#最长回文序列)
      * [戳气球](#戳气球)
   * [背包 DP](#背包-dp)
      * [分割等和子集](#分割等和子集)
      * [二进制串凑数](#二进制串凑数)
      * [零钱兑换](#零钱兑换)
      * [完全平方和](#完全平方和)
   * [状态机 DP](#状态机-dp)
      * [股票买卖含手续费](#股票买卖含手续费)
      * [股票买卖含冷冻期](#股票买卖含冷冻期)
      * [股票买卖含上限次数](#股票买卖含上限次数)
   * [双序列 DP](#双序列-dp)
      * [编辑距离](#编辑距离)
      * [最长公共子序列](#最长公共子序列)
      * [不同子序列个数](#不同子序列个数)



## 方法论

### DP 定义

动态规划是一种算法思想，通过**把复杂的父问题分解成形式相同的子问题**，记录并利用子问题的最优解来反推出父问题的最优解，本质上是利用**空间换时间**，通过 DP Table 记录子问题的最优解，来避免重复计算子问题

- **最优子结构**：父问题可以分解为子问题，并且父问题的最优解可以由子问题的最优解构成
- **重叠子问题**：不同父问题的分解可能会得到相同子问题，但子问题的最优解不会因为路径不同而变化
- **无后效性**：求解路径的影响被完全封装在最优解中，因此父问题的最优解仅依赖于子问题的最优解，而与子问题的求解路径无关

### 核心步骤

本质上就是定义状态和构造 DP Table

1. 状态表示：**明确 `dp[i]` 或 `dp[i][j]` 表示什么子问题的最优解**，为状态转移建立条件
2. 状态初始化：**明确边界条件和平凡状态的最优解**，为状态转移提供起点
3. 状态转移：**明确当前问题和其子问题之间的关系以及可执行的决策**，从子问题的最优解中构建当前问题的最优解
4. 答案提取：**明确最终答案的来源**，有时候直接是最终状态，有时候需要聚合不同状态

### 类型区别

| **类型** | **状态含义** | **依赖关系** | **转移形式** | **经典问题** |
| --------- | ------------------------------------------------------------ | ---------------------------------------------- | -------------- | -------------- |
| **线性 DP** | dp\[i] 表示按顺序遍历到第 i 个元素的最优解 | 依赖于前几个状态 | $dp[i] = f(dp[i-1], dp[i-2], \dots)$ | 最长上升子序列 |
| **网格 DP** | dp\[i][j] 表示按行序 / 列序遍历到 (i, j) 位置的最优解 | 依赖于当前位置的左方，上方或左上方 | $dp[i][j] = f(dp[i-1][j],\ dp[i][j-1],\ dp[i-1][j-1])$ | 最小路径和 |
| **树形 DP** | dp\[u] 表示以节点 u 为根时的最优解 | 依赖于树的子节点 | $dp[u] = f\big({dp[v] \mid v \in \text{children}(u)}\big)$ | 打家劫舍 |
| **区间 DP** | dp\[i][j] 表示区间 [i, j] 的最优解 | 依赖于长度更小的区间 | $dp[i][j] = \min_{i \le k < j} \{dp[i][k] + f(i, j) + dp[k+1][j]\}$ | 矩阵连乘 |
| **背包 DP** | dp\[i][j] 表示前 i 个物品，容量为 j 时的最优解 | 依赖于“取”或“不取” | $dp[i] = \max \{dp[i],\ dp[i- c_i] + v_i\}$ | 分割等和子集 |
| **划分 DP** | dp[i] 表示前 i 个元素的最优解 | 依赖于从 0 到 i 的不同划分点 | $dp[i] = \min_{0 \le j < i}\{dp[j] + cost(j+1, i)\}$ | 单词拆分 |
| **状态机 DP** | dp\[i][state] 表示第 i 个阶段、状态为 state 的最优解 | 依赖于前一个阶段的不同状态 | $dp[i][s] = \max_{t \in \text{prev}(s)}\{dp[i-1][t] + w(t \to s)\}$ | 股票买卖 |
| **双序列 DP** | dp\[i][j] 表示序列 A 的前 i 个元素和序列 B 的前 j 个元素下的最优解 | 依赖于序列 A 的前 i-1 个元素和序列 B 的前 j-1 个元素 | $dp[i][j] = f(dp[i-1][j],\ dp[i][j-1],\ dp[i-1][j-1])$ | 编辑距离 |

> 以下所有问题都整理到了：[Dasi 的 DP LeetCode 题单](https://leetcode.cn/problem-list/Ymzpk8xL/)



## 线性 DP

### 最长上升子序列

【问题描述】

```text
给定一个整数数组 nums，返回其中最长严格上升子序列的长度。子序列的元素在原数组中可以不连续，但必须保持相对顺序。
```

【原理分析】

每个元素作为结尾的最长上升子序列长度，只有可能是之前比他小的元素的最长上升子序列长度 + 1。

【状态表示】

dp[i] 表示以 nums[i] 结尾的最长上升子序列长度。

【转移方程】

$$
dp[i] = \max_{0 \le j < i} 
\begin{cases}
dp[j] + 1, & \text{if } nums[j] < nums[i] \\
1, & \text{otherwise}
\end{cases}
$$


【代码实现】

```java
class Solution {
    public int lengthOfLIS(int[] nums) {
        int n = nums.length;
        int[] dp = new int[n];
        
        int ans = 1;
        for (int i = 0; i < n; i++) {
            dp[i] = 1;
            for (int j = 0; j < i; j++) {
                if (nums[j] < nums[i]) {
                    dp[i] = Math.max(dp[i], dp[j] + 1);
                }
            }
            ans = Math.max(ans, dp[i]);
        }

        return ans;
    }
}
```

### 最大子数组和

【问题描述】

```text
给定一个整数数组 nums，找出一个具有最大和的连续子数组（子数组最少包含一个元素），返回其最大和。
```

【原理分析】

每个元素作为结尾的最大子数组要么是 nums[i] 字节，要么是前一个元素的最大子数组加上当前元素。

【状态表示】

dp[i] 表示以 nums[i] 结尾的最大连续子数组和。

【转移方程】

$$
dp[i] = max(nums[i], dp[i-1] + nums[i])
$$

【代码实现】

```java
class Solution {
    public int maxSubArray(int[] nums) {
        int n = nums.length;
        int ans = nums[0];
        int[] dp = new int[n];
        dp[0] = nums[0];

        for (int i = 1; i < n; i++) {
            dp[i] = Math.max(nums[i], dp[i-1] + nums[i]);
            ans = Math.max(ans, dp[i]);
        }

        return ans;
    }
}
```

### 最大子数组乘积

【问题描述】

```text
给定一个整数数组 nums，找出一个连续子数组，使得该子数组内的所有数字的乘积最大，返回这个最大乘积。
```

【原理分析】

负数会改变正负关系，即将最大值变为最小值，最小值变为最大值，而正数不会改变正负关系，最大值只会更大，最小值只会更小。因此在计算最大乘积时，必须同时维护当前位置的最大乘积和最小乘积。

【状态表示】

maxDp[i] 表示以 nums[i] 结尾的连续子数组的最大乘积；而 minDp[i] 表示 以 nums[i] 结尾的连续子数组的最小乘积。

【转移方程】

$$
\begin{aligned}

dp\_max[i] &= \max(nums[i],\ dp\_max[i-1] \times nums[i],\ dp\_min[i-1] \times nums[i]) \
\\
dp\_min[i] &= \min(nums[i],\ dp\_max[i-1] \times nums[i],\ dp\_min[i-1] \times nums[i])

\end{aligned}
$$

【代码实现】

```java
class Solution {
    public int maxProduct(int[] nums) {
        int n = nums.length;
      
        int[] maxDp = new int[n];
        int[] minDp = new int[n];
        maxDp[0] = nums[0];
        minDp[0] = nums[0];
      
        int ans = nums[0];
        for (int i = 1; i < n; i++) {
            maxDp[i] = Math.max(nums[i], Math.max(maxDp[i - 1] * nums[i], minDp[i - 1] * nums[i]));
            minDp[i] = Math.min(nums[i], Math.min(maxDp[i - 1] * nums[i], minDp[i - 1] * nums[i]));
            ans = Math.max(ans, maxDp[i]);
        }

        return ans;
    }
}
```

### 环形抢劫

【问题描述】

```text
给定一个代表每个房屋金额的数组 nums，房屋围成一个圈，不能偷相邻的两间房，求能偷到的最大金额。
```

【原理分析】

由于房屋首尾相连，偷取第一间房会导致最后一间房无法被偷取，因此可以看作为区间 [1, n-1] 和 [0, n-2] 两种情况。同时若偷当前房屋则不能偷上一个，只能考虑是否偷上上个，而如果不偷当前房屋，则为前上一个的最优结果。

【状态表示】

dp[i] 表示前 i 个房屋中能偷到的最大金额。

【转移方程】

$$
dp[i] = \max(dp[i-1], dp[i-2] + nums[i])
$$

【代码实现】

```java
class Solution {
    public int rob(int[] nums) {
        int n = nums.length;
        if (n == 1) return nums[0];
        if (n == 2) return Math.max(nums[0], nums[1]);

        int[] dp = new int[n];

        // 不偷首屋
        dp[1] = nums[1];
        dp[2] = Math.max(nums[1], nums[2]);
        for (int i = 3; i < n; i++) {
            dp[i] = Math.max(dp[i - 1], dp[i - 2] + nums[i]);
        }

        // 不偷尾屋
        dp[0] = nums[0];
        dp[1] = Math.max(nums[0], nums[1]);
        for (int i = 2; i < n - 1; i++) {
            dp[i] = Math.max(dp[i - 1], dp[i - 2] + nums[i]);
        }

      	// 先计算不偷首屋，这样结果保留在 dp[n-1]，不会被不偷尾屋的情况干扰
        return Math.max(dp[n-1], dp[n-2]);
    }
}
```



## 划分 DP

### 单词拆分

【问题描述】

```text
给定字符串 s 和字典 wordDict，判断 s 能否由字典中单词拼接组成，单词可以不使用或使用多次。
```

【原理分析】

遍历字符串的每个前缀，枚举每个划分点，若存在某个划分点使前段可达且后段在字典中，则整个前缀可达。

【状态表示】

dp[i] 表示 s[1..i] 是否能被拆分。

【转移方程】

$$
dp[i] = \exists j < i,\ dp[j]\ \text{and}\ (s[j+1..i] \in wordDict)
$$

【代码实现】

```java
class Solution {
    public boolean wordBreak(String s, List<String> wordDict) {
        int n = s.length();
        s = " " + s;
        
      	boolean[] dp = new boolean[n + 1];
        dp[0] = true;
        
        for (int i = 1; i <= n; i++) {
            for (int j = 0; j < i; j++) {
                String sub = s.substring(j + 1, i + 1);
                if (dp[j] && wordDict.contains(sub)) {
                    dp[i] = true;
                    break;
                }
            }
        }

        return dp[n];
    }
}
```

### 回文串拆分

【问题描述】

```text
给定一个字符串 s，将其分割成若干子串，使得每个子串都是回文串，返回最少需要分割几次才能满足条件。
```

【原理分析】

对于位置 i，枚举所有可划分位置 j，若 s[j..i] 是回文串，则说明可以在 j 之前切一刀，将问题转化为位置 j-1 的最优解 + 1，最后取最小值即可。由于判断相同区间是否为回文子串会频繁使用，因此可以多用一个二维表表示起点和终点来记录区间是为回文。

【状态表示】

dp[i] 表示 s[1..i] 的最少划分次数。

【转移方程】

$$
dp[i] = \min_{0 \le j < i}
\begin{cases}
dp[j] + 1, & \text{if } s[j+1..i] \text{ 是回文串} \\
dp[i], & \text{otherwise}
\end{cases}
$$


【代码实现】

```java
class Solution {
    public int minCut(String s) {
        int n = s.length();
        s = " " + s;
        
        boolean[][] isPal = new boolean[n+1][n+1];

        int[] dp = new int[n + 1];
        for (int i = 0; i <= n; i++) dp[i] = i - 1;

        for (int i = 1; i <= n; i++) {
            for (int j = 0; j < i; j++) {
                if (s.charAt(i) == s.charAt(j + 1) && (i - j < 3 || isPal[j + 1][i - 1])) {
                    isPal[j][i] = true;
                    dp[i] = Math.min(dp[i], dp[j] + 1);
                }
            }
        }

        return dp[n];
    }
}
```



## 网格 DP

### 最大正方形

【问题描述】

```text
给定一个由 '0' 和 '1' 组成的二维矩阵，找出只包含 '1' 的最大正方形，并返回其面积。
```

【原理分析】

如果一个点 (i,j) 为右下角点正方形的边长为 a，那么其 (i-1, j)、(i, j-1)、(i-1, j-1) 为右下角的正方形边长一定为 a - 1。

【状态表示】

dp\[i][j] 表示以 (i, j) 为右下角的最大正方形边长。

【转移方程】

$$
dp[i][j] =
\begin{cases}
0, & \text{if } matrix[i][j] = 0 \
\\
\min(dp[i-1][j],\ dp[i][j-1],\ dp[i-1][j-1]) + 1, & \text{if } matrix[i][j] = 1
\end{cases}
$$

【代码实现】

```java
class Solution {
    public int maximalSquare(char[][] matrix) {
        int rows = matrix.length;
        int cols = matrix[0].length;
        
      	int[][] dp = new int[rows][cols];
        int max = 0;

        for (int i = 0; i < rows; i++) {
            for (int j = 0; j < cols; j++) {
                if (matrix[i][j] == '1') {
                    if (i == 0 || j == 0) {
                        dp[i][j] = 1;
                    } else {
                        dp[i][j] = Math.min(Math.min(dp[i-1][j], dp[i][j-1]),dp[i-1][j-1]) + 1;
                    }
                    max = Math.max(max, dp[i][j]);
                }
            }
        }

        return max * max;
    }
}
```

### 不同路径

【问题描述】

```text
一个机器人位于一个网格左上角，每次只能向下或向右移动一步，网格中有障碍物（obstacleGrid[i][j] == 1 表示障碍），请计算有多少条路径可以到达右下角。
```

【原理分析】

每个格子的路径数等于其上方和左方格子路径数之和。但若该格子存在障碍，则无法通行，对应路径数为 0。

【状态表示】

dp\[i][j] 表示从起点 (0,0) 到达位置 (i,j) 的路径总数。

【转移方程】

$$
dp[i][j] =
\begin{cases}
0, & \text{if } obstacleGrid[i][j] = 1 \\
dp[i-1][j] + dp[i][j-1], & \text{otherwise}
\end{cases}
$$

【代码实现】

```java
class Solution {
    public int uniquePathsWithObstacles(int[][] obstacleGrid) {
        int m = obstacleGrid.length;
        int n = obstacleGrid[0].length;

        int[][] dp = new int[m+1][n+1];
        for (int i = 1; i <= m; i++) {
            for (int j = 1; j <= n; j++) {
                if (obstacleGrid[i-1][j-1] == 1) dp[i][j] = 0;
                else if (i == 1 && j == 1)  dp[i][j] = 1;
                else dp[i][j] = dp[i-1][j] + dp[i][j-1];
            }
        }

        return dp[m][n];
    }
}
```



## 树形 DP

### 树形抢劫

【问题描述】

```text
在二叉树中，每个节点具有一个金额，相连接的节点（父子节点）不能同时偷，求最大金额。
```

【原理分析】

对于每个节点，可以选择偷或不偷，若偷则不能偷其子节点，若不偷则可以取左右子树最大值中的较大值。

【状态表示】

dp\[u][0] 表示不偷当前节点的最大值，dp\[u][1] 表示偷当前节点的最大值，dp\[u][2] 表示当前节点可以获得的最大值。

【状态转移】

$$
\begin{aligned}
dp[u][0] &= dp[l][2] + dp[r][2] \\
dp[u][1] &= val + dp[l][0] + dp[r][0] \\
dp[u][2] &= \max(dp[u][0], dp[u][1])
\end{aligned}
$$

【代码实现】

```java
class Solution {
    public int rob(TreeNode root) {
        return dp(root)[2];
    }

    private int[] dp(TreeNode node) {
        if (node == null) return new int[]{0, 0, 0};

        int[] left = dp(node.left);
        int[] right = dp(node.right);

        int notRob = left[2] + right[2]; 					// 不打劫价值 
        int rob = node.val + left[0] + right[0];	// 打劫价值
        int maxVal = Math.max(notRob, rob);				// 最大价值

        return new int[]{notRob, rob, maxVal};
    }
}
```

### 二叉树中的最大路径和

【问题描述】

```text
给定一个二叉树的根节点 root，返回其最大路径和。路径可以从任意节点开始和结束，但必须沿着父子节点连接。
```

【原理分析】

对于每个节点，最大值（max）要么来自于 enable，要么来自于 unable

- 可以传递给父节点使用（enable）
    - 使用当前节点，但不使用左子节点和右子节点：val
    - 使用当前节点，但只使用其中一个子节点：val + left.enable 或 val + right.enable
- 不能传递给父节点使用（unable）
    - 使用当前节点、左子节点和右子节点：val + left.enable + right.enable
    - 不使用当前节点，但使用其中一个子节点：left.max 或 right.max

所以为了父节点的更新，需要把 enable 和 max 传递给父节点，而空节点则可令 enbale 是节点最小值，令 max 是整数最小值

【状态表示】

dp(node)[0] 表示可以传递给父节点的最大值，dp(node)[1] 表示当前节点计算得到的最大值。

【转移方程】

$$
\begin{aligned}
dp[u][0] &= \max\bigl( val,\; val + dp[l][0],\; val + dp[r][0] \bigr) \\
dp[u][1] &= \max\bigl( val + dp[l][0] + dp[r][0],\; dp[l][1],\; dp[r][1] \bigr)
\end{aligned}
$$


【代码实现】

```java
class Solution {
    public int maxPathSum(TreeNode root) {
        return dp(root)[1];
    }

    public int[] dp(TreeNode node) {
        if (node == null) return new int[]{-1000, Integer.MIN_VALUE};

        int[] left = dp(node.left);
        int[] right = dp(node.right);

        // 可传递
        int enable = Math.max(
            node.val + left[0], Math.max(
            node.val + right[0],
            node.val
        ));

        // 不可传递
        int unable = Math.max(
            node.val + left[0] + right[0], Math.max(
            left[1], 
            right[1]
        ));

        int max = Math.max(enable, unable);

        return new int[]{enable, max};
    }
}
```



## 区间 DP

### 回文子串个数

【问题描述】

```text
给定字符串 s，求其中回文子串的总数。
```

【原理分析】

若字符串的两端字符相等且中间子串也是回文串，则该字符串也是回文串。

- 平凡情况：当字符串的长度为 0 或 1 的时候是回文串；
- 特殊情况：当字符串长度为 2 或 3 且两端字符相等的时候，中间子串的长度是 0 或 1，因此肯定是回文串；
- 一般情况：当字符串长度 >= 3 且两端字符相等的时候，只需要看中间子串是否是回文。

【状态表示】

dp\[i][j] 表示 s[i..j] 是否为回文子串。

【转移方程】

$$
dp[i][j] = (s[i] = s[j])\ \text{and}\ (j - i <= 2\ \text{or}\ dp[i+1][j-1])
$$

【代码实现】

```java
class Solution {
    public int countSubstrings(String s) {
        int n = s.length();

        boolean[][] dp = new boolean[n][n];
        int count = 0;

        for (int len = 1; len <= n; len++) {
            for (int i = 0, j = i + len - 1; j < n; i++, j++) {
                if (s.charAt(i) == s.charAt(j)) {
                    if (len <= 3 || dp[i+1][j-1]) {
                        dp[i][j] = true;
                        count++;
                    }
                }
            }
        }
        
        return count;
    }
}
```

### 最长回文序列

【问题描述】

```text
给定一个字符串 s，找到其中最长的回文子序列的长度。
```

【原理分析】

对于字符串区间 [i, j]，如果两端字符相等，那么最长回文子序列长度 = 内部子串的最长回文子序列长度 + 2，否则则为去掉左端或去掉右端两种情况的最大值

【状态表示】

dp[i][j] 表示字符串 s 在区间 [i, j] 内的最长回文子序列长度

【转移方程】

$$
dp[i][j] = 
\begin{cases}
dp[i+1][j-1] + 2, & \text{if } s[i] = s[j] \\
\max(dp[i+1][j], dp[i][j-1]), & \text{otherwise}
\end{cases}
$$

【代码实现】

```java
class Solution {
    public int longestPalindromeSubseq(String s) {
        int n = s.length();
        char[] str = s.toCharArray();

        int[][] dp = new int[n][n];
        for (int i = 0; i < n; i++) dp[i][i] = 1;

        for (int len = 2; len <= n; len++) {
            for (int i = 0, j = i + len - 1; j < n; i++, j++) {
                if (str[i] == str[j]) {
                    dp[i][j] = dp[i+1][j-1] + 2;
                } else {
                    dp[i][j] = Math.max(dp[i+1][j], dp[i][j-1]);
                }
            }
        }

        return dp[0][n-1];
    }
}
```

### 戳气球

【问题描述】

```text
有 n 个气球，每个气球上都标有一个数字。每当你戳破一个气球 i，你会得到 nums[i-1] * nums[i] * nums[i+1] 的硬币。戳破后，气球会消失，左右气球相邻。请返回戳破所有气球所能获得的最大硬币数。
```

【原理分析】

对于气球区间 (i, j)，如果除了两端气球，最后戳破的气球是中间的某个 k，那戳破的得分一定为 arr[i] * arr[k] * arr[j]。此时区间 (i, k) 与区间 (k, j) 的气球已经全部戳完，所以问题自然分解为两个独立子区间的子问题，即 (i, j) 的最大分数 = (i, k) 的最大分数 * (k, j) 的最大分数 * 乘上最后戳破气球 k 的分数。但由于 i 和 j 的气球尚未戳破，它们可以看作“边界墙”，只需要在原数组的两侧补上 1 即可。

【状态表示】

dp\[i][j] 表示戳完开区间 (i, j) 内的所有气球能获得的最大金币数。

【转移方程】

$$
dp[i][j] = \max_{i < k < j}\big( dp[i][k] + dp[k][j] + arr[i] \times arr[k] \times arr[j] \big)
$$

【代码实现】

```java
class Solution {
    public int maxCoins(int[] nums) {
        int n = nums.length;

        int[] arr = new int[n+2];
        for (int i = 0; i < n; i++) arr[i+1] = nums[i];
        arr[0] = arr[n+1] = 1;
        n = n + 2;

        int[][] dp = new int[n][n];
        for (int len = 3; len <= n; len++) {
            for (int i = 0, j = i + len - 1; j < n; i++, j++) {
                for (int k = i + 1; k < j; k++) {
                    dp[i][j] = Math.max(dp[i][j], dp[i][k] + dp[k][j] + arr[i] * arr[k] * arr[j]);
                }
            }
        }

        return dp[0][n-1];
    }
}
```



## 背包 DP

### 分割等和子集

【问题描述】

```text
判断一个只包含正整数的数组是否能分成和相等的两个子集。
```

【原理分析】

问题等价于在数组中选择一些数，使其和为总和的一半。在之前的所有数字能达到的可达状态下，如果加上当前数字，判断可达状态是否会更新。为了防止覆盖，应该倒序遍历，确保不会影响上一迭代的可达结果。由于每个数只能使用一次，所以这属于零一背包。

【状态描述】

dp[j] 表示是否能恰好取出若干数使和为 j。

【转移方程】

$$
dp[j] = dp[j]\ \text{or}\ dp[j - nums[i]]
$$

【代码实现】

```java
class Solution {
    public boolean canPartition(int[] nums) {
        int n = nums.length;

        int sum = 0;
        for (int i = 0; i < n; i++) sum += nums[i];
        if (sum % 2 != 0) return false;
        
        int target = sum / 2;
        boolean[] dp = new boolean[target + 1];
        dp[0] = true;

        for (int num : nums) {
            for (int i = target; i >= num; i--) {
                dp[i] = dp[i] || dp[i - num];
            }
        }

        return dp[target];
    }
}
```

### 二进制串凑数

【问题描述】

```text
给定一个仅包含 0 和 1 的字符串数组 strs，以及两个整数 m 和 n。请你找出并返回最多有多少个字符串，其所包含的 0 的数量不超过 m，1 的数量不超过 n。
```

【原理分析】

每个字符串相当于一个物品，而一个物品具有两个容量，分别是 0 的数量和 1 的数量，所以应该从两个维度来遍历。因为每个字符串只能选一次，所以这属于零一背包。

【状态描述】

dp[i][j] 表示在最多使用 i 个 ‘0’ 和 j 个 ‘1’ 的限制下，能选择的字符串最大数量。

【转移方程】

$$
dp[i][j] = \max(dp[i][j], dp[i - zeros][j - ones] + 1)
$$

【代码实现】

```java
class Solution {
    public int findMaxForm(String[] strs, int m, int n) {
        int[][] dp = new int[m+1][n+1];

        for (String s : strs) {
            int zeros = 0, ones = 0;
            
            for (char c : s.toCharArray()) {
                if (c == '0') zeros++;
                else ones++;
            }

            for (int i = m; i >= zeros; i--) {
                for (int j = n; j >= ones; j--) {
                    dp[i][j] = Math.max(dp[i][j], dp[i - zeros][j - ones] + 1);
                }
            }
        }

        return dp[m][n];
    }
}
```

### 零钱兑换

【问题描述】

```text
给定硬币面额数组 coins 和目标金额 amount，求凑成该金额的最少硬币数，不可凑出则返回 -1，每种硬币可以重复使用或不使用。
```

【原理分析】

对于每一种硬币 coin，按顺序每个金额 i，只要 coin 不大于 i，那么 i 所需的最少硬币数要么是原先的硬币数（不使用），要么是 i - coin 所需的最少硬币加上 coin 这单个硬币（使用）。由于 coin 可以无限使用，所以这属于完全背包。

【状态表示】

dp[i] 表示凑成金额 i 所需的最少硬币数。

【转移方程】

$$
dp[i] = \min_{coin \in coins}(dp[i],\ dp[i - coin] + 1)
$$

【代码实现】

```java
class Solution {
    public int coinChange(int[] coins, int amount) {
        int[] dp = new int[amount + 1];
        Arrays.fill(dp, amount + 1); // 填充 amount + 1，因为最坏的情况就是使用全部 1 即 amount
        dp[0] = 0;

        for (int coin : coins) {
            for (int i = coin; i <= amount; i++) {
                dp[i] = Math.min(dp[i], dp[i - coin] + 1);
            }
        }

        return dp[amount] > amount ? -1 : dp[amount];
    }
}
```

### 完全平方和

【问题描述】

```text
给定一个正整数 n，求最少由多少个完全平方数（如 1, 4, 9, 16, …）之和组成 n。
```

【原理分析】

对于每个可以使用完全平方数 square，按顺序遍历每个数 i，只要 square 不大于 i，那么 i 所需的最少完全平方数数量要么是原先的数量（不使用），要么是 i - square 所需的最少数量加上 square 这单个数量（使用）。由于 square 可以无限使用，所以这属于完全背包。

【状态表示】

dp[i] 表示组成整数 i 所需的最少完全平方数数量。

【转移方程】

$$
dp[i] = \min_{1 \le j^2 \le i}(dp[i],\ dp[i - j^2] + 1)
$$

【代码实现】

```java
class Solution {
    public int numSquares(int n) {
        int[] dp = new int[n+1];
        Arrays.fill(dp, n);
        dp[0] = 0;

        for (int j = 1; j * j <= n; j++) {
            int square = j * j;
            for (int i = square; i <= n; i++) {
                dp[i] = Math.min(dp[i], dp[i - square] + 1);
            }
        }

        return dp[n];
    }
}
```



## 状态机 DP

### 股票买卖含手续费

【问题描述】

```text
给定一个整数数组 prices，其中第 i 天的价格为 prices[i]，以及一个手续费 fee。你可以多次买卖股票，但每次卖出都需要支付固定手续费 fee，求可以获得的最大利润。
```

【原理分析】

可以一开始令利润为 0，买股票利润需要扣减股票价格，卖股票利润需要增加股票价格，每天结束时的状态完全取决于昨天状态：

- 持仓：要么昨天也持仓，要么昨天空仓但在今天买入；
- 空仓：要么昨天也空仓，要么昨天持仓但在今天卖出。

【状态表示】

dp\[i][0] 表示第 i 天持仓的最大利润；dp\[i][1] 表示第 i 天空仓的最大利润。

【转移方程】

$$
\begin{aligned}
dp[i][0] &= \max(dp[i-1][0],\ dp[i-1][1] - prices[i]) \\
dp[i][1] &= \max(dp[i-1][1],\ dp[i-1][0] + prices[i] - fee) \\
\end{aligned}
$$

【代码实现】

```java
class Solution {
    public int maxProfit(int[] prices, int fee) {
        int n = prices.length;

        int[][] dp = new int[n][2];
        dp[0][0] = -prices[0];
        dp[0][1] = 0;

        for (int i = 1; i < n; i++) {
            dp[i][0] = Math.max(dp[i - 1][0], dp[i - 1][1] - prices[i]);
            dp[i][1] = Math.max(dp[i - 1][1], dp[i - 1][0] + prices[i] - fee);
        }

        // 最后一天的最大利润肯定是没持有股票，否则一定会卖出
        return dp[n - 1][1];
    }
}
```

### 股票买卖含冷冻期

【问题描述】

```text
给定一个整数数组 prices，其中第 i 天的价格为 prices[i]。你可以多次买卖股票，但卖出股票后有一天冷冻期，在冷冻期内不能买入，求最大利润。
```

【原理分析】

可以一开始令利润为 0，买股票利润需要扣减股票价格，卖股票利润需要增加股票价格，每天结束时的状态完全取决于昨天状态：

- 持仓：要么昨天也持仓，要么昨天空仓但在今天买入；
- 平仓：昨天持仓且今天卖出；
- 空仓：要么昨天平仓，要么昨天空仓。

【状态表示】

dp\[i][0] 表示第 i 天持仓的最大利润；dp\[i][1] 表示第 i 天平仓的最大利润；dp\[i][2] 表示第 i 天空仓的最大利润。

【转移方程】

$$
\begin{aligned}
dp[i][0] &= \max(dp[i-1][0],\ dp[i-1][2] - prices[i]) \\
dp[i][1] &= dp[i-1][0] + prices[i] \\
dp[i][2] &= \max(dp[i-1][1],\ dp[i-1][2])
\end{aligned}
$$

【代码实现】

```java
class Solution {
    public int maxProfit(int[] prices) {
        int n = prices.length;
        if (n == 0) return 0;
        
        dp[0][0] = -prices[0];
        dp[0][1] = 0;
        dp[0][2] = 0;

        for (int i = 1; i < n; i++) {
            dp[i][0] = Math.max(dp[i - 1][0], dp[i - 1][2] - prices[i]);
            dp[i][1] = dp[i - 1][0] + prices[i];
            dp[i][2] = Math.max(dp[i - 1][1], dp[i - 1][2]);
        }

        // 最后一天的最大利润肯定是没持有股票，否则一定会卖出
        return dp[n - 1][1];
    }
}
```

### 股票买卖含上限次数

【问题描述】

```text
给定一个整数数组 prices，第 i 天的股票价格为 prices[i]。最多可以完成 k 笔交易（买入和卖出为一笔交易），请计算你所能获得的最大利润。
```

【原理分析】

由于存在最多 k 次交易的限制，同时一次只能持有一份股票，所以必须在状态中显式记录交易次数：

- 第 j 次持仓：昨天的第 j 次持仓，昨天第 j - 1 次空仓但今天买入
- 第 j 次空仓：昨天的第 j 次空仓，昨天第 j 次持仓但今天卖出

【状态表示】

dp\[i]\[k][0] 表示第 i 天最多进行 k 次交易且当前持仓的最大利润；dp\[i]\[k][0] 表示第 i 天最多进行 k 次交易且当前空仓的最大利润。

【转移方程】

$$
\begin{aligned}
dp[i][k][0] &= \max(dp[i-1][k][0],\ dp[i-1][k-1][1] - prices[i]) \\
dp[i][k][1] &= \max(dp[i-1][k][1],\ dp[i-1][k][0] + prices[i]) \\
\end{aligned}
$$

【代码实现】

```java
class Solution {
    public int maxProfit(int k, int[] prices) {
        int n = prices.length;

        int[][][] dp = new int[n+1][k+1][2];
        for (int j = 0; j <= k; j++) dp[0][j][0] = -prices[0];

        for (int i = 1; i < n; i++) {
            for (int j = 1; j <= k; j++) {
                dp[i][j][0] = Math.max(dp[i - 1][j][0], dp[i - 1][j - 1][1] - prices[i]);
                dp[i][j][1] = Math.max(dp[i - 1][j][1], dp[i - 1][j][0] + prices[i]);
            }
        }
        
        return dp[n-1][k][1];
    }
}
```



## 双序列 DP

### 编辑距离

【问题描述】

```text
给定两个字符串 word1 和 word2，求将 word1 转换为 word2 所需的最少操作次数。你可以进行以下三种操作：1. 插入一个字符 2. 删除一个字符 3. 替换一个字符。
```

【原理分析】

由于无后效性，所有可能的历史编辑路径都已包含在较小的子问题中，因此当前最优解只与更短前缀的最优解有关。如果已经知道相邻状态的最短编辑距离，那么对于当前字符 i 和字符 j，如果相同则为不需要额外操作，否则只有可能是相邻状态执行删除/插入/替换中的一个：

- 删除：从 word1[0, i-1] 已经可以得到 word2[0, j]，所以删除 word1[i]；
- 插入：从 word1[0, i] 已经可以得到 word2[0, j-1]，所以插入 word2[j]；
- 替换：从 word1[0, i-1] 已经可以得到 word2[0, j-1]，所以替换 word1[i] 为 word2[j]。

【状态表示】

dp\[i][j] 表示将 word1 的前 i 个字符转换为 word2 的前 j 个字符所需的最少操作次数。

【转移方程】

$$
dp[i][j] =
\begin{cases}
dp[i-1][j-1], & \text{if } word1[i] = word2[j] \\
\min(dp[i-1][j] + 1,\ dp[i][j-1] + 1,\ dp[i-1][j-1] + 1), & \text{otherwise}
\end{cases}
$$

【代码实现】

```java
class Solution {
    public int minDistance(String word1, String word2) {
        int len1 = word1.length();
        int len2 = word2.length();
        word1 = " " + word1;
        word2 = " " + word2;

        int[][] dp = new int[len1 + 1][len2 + 1];
        for (int i = 0; i <= len1; i++) dp[i][0] = i; // 全删除
        for (int j = 0; j <= len2; j++) dp[0][j] = j; // 全插入

        for (int i = 1; i <= len1; i++) {
            for (int j = 1; j <= len2; j++) {
                if (word1.charAt(i) == word2.charAt(j)) {
                    dp[i][j] = dp[i-1][j-1];
                } else {
                    dp[i][j] = 1 + Math.min(
                        /* 删除 */ dp[i-1][j], Math.min(
                        /* 插入 */ dp[i][j-1],
                        /* 替换 */ dp[i-1][j-1]
                    ));
                }
            }
        }

        return dp[len1][len2];
    }
}
```

### 最长公共子序列

【问题描述】

```text
给定两个字符串 text1 和 text2，返回它们的最长公共子序列的长度。
```

【原理分析】

如果两个字符串的最后一个字符相等，那么它们的最长公共子序列一定是前一个状态的长度 + 1；否则，最长公共子序列一定是跳过其中一个字符后得到的两个可能结果中的较大值。

【状态表示】

dp\[i][j] 表示 text1 的前 i 个字符和 text2 的前 j 个字符的最长公共子序列长度。

【转移方程】

$$
dp[i][j] =
\begin{cases}
dp[i-1][j-1] + 1, & \text{if } text1[i] = text2[j] \\
\max(dp[i-1][j],\ dp[i][j-1]), & \text{otherwise}
\end{cases}
$$

【代码实现】

```java
class Solution {
    public int longestCommonSubsequence(String text1, String text2) {
        int len1 = text1.length();
        int len2 = text2.length();
        text1 = " " + text1;
        text2 = " " + text2;

        int[][] dp = new int[len1 + 1][len2 + 1];
        for (int i = 1; i <= len1; i++) {
            for (int j = 1; j <= len2; j++) {
                if (text1.charAt(i) == text2.charAt(j)) {
                    dp[i][j] = dp[i-1][j-1] + 1;
                } else {
                    dp[i][j] = Math.max(dp[i-1][j], dp[i][j-1]);
                }
            }
        }

        return dp[len1][len2];
    }
}
```

### 不同子序列个数

【问题描述】

```text
给定两个字符串 s 和 t，统计在 s 的所有子序列中，有多少个等于 t。
```

【原理分析】

如果 t[i] == s[j]，则子序列个数是先前已经有的子序列个数加上 t[i-1] 的子序列个数（这种情况只需要再补充当前字符即可）；否则只能是先前已经有的子序列个数。

【状态表示】

dp\[i][j] 表示使用 s 的前 j 个字符可以形成 t 的前 i 个字符的不同子序列个数。

【转移方程】

$$
dp[i][j] =
\begin{cases}
dp[i-1][j-1] + dp[i][j-1], & \text{if } t[i] = s[j] \\
dp[i][j-1], & \text{otherwise}
\end{cases}
$$

【代码实现】

```java
class Solution {
    public int numDistinct(String s, String t) {
        int sLen = s.length();
        int tLen = t.length();
        s = " " + s;
        t = " " + t;

        int[][] dp = new int[tLen + 1][sLen + 1];
        for (int j = 0; j <= sLen; j++) dp[0][j] = 1;

        for (int i = 1; i <= tLen; i++) {
            for (int j = 1; j <= sLen; j++) {
                if (t.charAt(i) == s.charAt(j)) {
                    dp[i][j] = dp[i-1][j-1] + dp[i][j-1];
                } else {
                    dp[i][j] = dp[i][j-1];
                }
            }
        }

        return dp[tLen][sLen];
    }
}

```