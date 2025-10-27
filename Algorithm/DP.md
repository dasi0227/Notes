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
   * [序列 DP](#序列-dp)
      * [编辑距离](#编辑距离)
   * [划分 DP](#划分-dp)
      * [单词拆分](#单词拆分)
   * [网格 DP](#网格-dp)
      * [最大正方形](#最大正方形)
   * [树形 DP](#树形-dp)
      * [打家劫舍](#打家劫舍)
   * [区间 DP](#区间-dp)
      * [回文子串](#回文子串)
      * [戳气球](#戳气球)
   * [背包 DP](#背包-dp)
      * [分割等和子集](#分割等和子集)
      * [零钱兑换](#零钱兑换)
      * [完全平方和](#完全平方和)
   * [状态机 DP](#状态机-dp)
      * [股票买卖](#股票买卖)



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

| **类型** | **状态含义** | **转移特征** | **经典问题** |
| --------- | ------------------------------------------------------------ | ---------------------------------------------- | -------------- |
| **线性 DP** | dp\[i] 表示按顺序遍历到第 i 个元素的最优解 | 依赖于前几个状态 | 最长上升子序列 |
| **网格 DP** | dp\[i][j] 表示按行序 / 列序遍历到 (i, j) 位置的最优解 | 依赖于当前位置的左方，上方或左上方 | 最小路径和 |
| **树形 DP** | dp\[u] 表示以节点 u 为根时的最优解 | 依赖于树的子节点 | 打家劫舍 |
| **区间 DP** | dp\[i][j] 表示区间 [i, j] 的最优解 | 依赖于长度更小的区间 | 矩阵连乘 |
| **背包 DP** | dp\[i][j] 表示前 i 个物品，容量为 j 时的最优解 | 依赖于“取”或“不取” | 分割等和子集 |
| **划分 DP** | dp[i] 表示前 i 个元素的最优解 | 依赖于从 0 到 i 的不同划分点 | 单词拆分 |
| **状态机 DP** | dp\[i][state] 表示第 i 个阶段、状态为 state 的最优解 | 依赖于前一个阶段的不同状态 | 股票买卖 |
| **双序列 DP** | dp\[i][j] 表示序列 A 的前 i 个元素和序列 B 的前 j 个元素下的最优解 | 依赖于序列 A 的前几个状态和序列 B 的前几个状态 | 编辑距离 |



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



## 序列 DP

### 编辑距离

【问题描述】

```text

```

【代码实现】

```java
```



## 划分 DP

### 单词拆分

【问题描述】

```text
给定字符串 s 和字典 wordDict，判断 s 能否由字典中单词拼接组成。
```

【原理分析】

遍历字符串的每个前缀，若存在某个划分点使前段可达且后段在字典中，则整个前缀可达。

【状态表示】

dp[i] 表示 s[0..i-1] 是否能被拆分。

【转移方程】

$$
dp[i] = \exists j < i,\ dp[j]\ \text{and}\ (s[j..i-1] \in wordDict)
$$

【代码实现】

```java
class Solution {
    public boolean wordBreak(String s, List<String> wordDict) {
        int len = s.length();
      	Set<String> dict = new HashSet<>(wordDict);
        boolean[] dp = new boolean[len + 1];
        dp[0] = true;

        for (int end2 = 1; end2 <= len; end2++) {
            for (int end1 = 0; end1 < end2; end1++) {
                String substr = s.substring(end1, end2);
                if (dp[end1] && dict.contains(substr)) {
                    dp[end2] = true;
                    break;
                }
            }
        }

        return dp[len];
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

每个点能构成的正方形边长取决于其上方、左方和左上方的最小正方形边长，若当前位置为 1，则可在三者最小值基础上加一。

<img src="https://dasi-blog.oss-cn-guangzhou.aliyuncs.com/Java/202510111501374.png" alt="image-20251011150109847" style="zoom: 50%;" />

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



## 树形 DP

### 打家劫舍

【问题描述】

```text
在二叉树中，每个节点具有一个金额，相连接的节点即父子节点不能同时偷，求最大金额。
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

    // 返回 [不打劫价值, 打劫价值, 最大价值]
    private int[] dp(TreeNode node) {
        // 空节点的三个价值都是 0
        if (node == null) return new int[]{0, 0, 0};

        int[] left = dp(node.left);
        int[] right = dp(node.right);

        // 【不打劫价值】 = Max {【左最大价值】, 【右最大价值】}
        int notRob = left[2] + right[2];

        // 【打劫价值】 = 【自身价值】 + 【左不打劫价值】 + 【右不打劫价值】
        int rob = node.val + left[0] + right[0];

        // 【最大价值】 = Max {【打劫价值】, 【不打劫价值】}
        int maxVal = Math.max(notRob, rob);

        return new int[]{notRob, rob, maxVal};
    }
}
```



## 区间 DP

### 回文子串

【问题描述】

```text
给定字符串 s，求其中回文子串的总数。
```

【原理分析】

若两端字符相等且中间部分是回文，则该区间也是回文。同时，当字符串长度为 1 的时候一定是回文，当字符串长度为 2 且两端字符相等的时候也一定是回文。

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

        // 区间长度从 1 开始枚举
        for (int len = 1; len <= n; len++) {
            for (int start = 0, end = start + len - 1; end < n; start++, end++) {
                if (s.charAt(start) == s.charAt(end)) {
                    // 长度 ≤ 2 直接为回文，否则取决于内部子区间
                    if (len <= 2 || dp[start + 1][end - 1]) {
                        dp[start][end] = true;
                        count++;
                    }
                }
            }
        }

        return count;
    }
}
```

### 戳气球

【问题描述】

```text
给你 n 个气球，每个气球上写着一个数字 nums[i]。你可以选择一个气球 i 戳破，得到的硬币数为 nums[left] * nums[i] * nums[right]，如果左右两边不存在气球，则数值可以看作为 1。戳破后，只有气球 i 会消失。
求出能获得的最多硬币数。
```

【原理分析】

对于气球区间 (i, j)，如果最后戳破的气球是其中的 k，那么戳破的得分为 arr[i] * arr[k] * arr[j]，并且此时 (i, k) 与 (k, j) 区间的气球已经全部戳完。所以问题自然分解为两个独立子区间的子问题，即 (i, j) 的最大分数 = (i, k) 的最大分数 * (k, j) 的最大分数 * 乘上最后戳破气球 k 的分数。

【状态表示】

dp\[i][j] 表示在开区间 (i, j) 内，戳破所有气球能获得的最大金币数。

【转移方程】

$$
dp[i][j] = \max_{i < k < j}\big( dp[i][k] + dp[k][j] + arr[i] \times arr[k] \times arr[j] \big)
$$

【代码实现】

```java
class Solution {
    public int maxCoins(int[] nums) {
        int n = nums.length;

        // 引入虚拟气球，防止索引溢出
        int[] arr = new int[n + 2];
        for (int i = 0; i <= n + 1; i++) {
            // 最左/右侧引入值为 1 的虚拟气球
            if (i == 0 || i == n+1) {
                arr[i] = 1;
            } else {
                arr[i] = nums[i - 1];
            }
        }
        n = arr.length;

        // dp[i][j] 表示戳破 (i, j) 之间所有气球所能获得的最大金币数
        int[][] dp = new int[n][n];
        // 区间长度
        for (int len = 1; len <= n; len++) {
            // 窗口：左端和右端
            for (int left = 0, right = len + 1; right < n; left++, right++) {
                // 分隔点
                for (int k = left + 1; k < right; k++) {
                    dp[left][right] = Math.max(
                        dp[left][right],
                        dp[left][k] + dp[k][right] + arr[left] * arr[k] * arr[right]
                    );
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

问题等价于在数组中选择一些数，使其和为总和的一半。在之前的所有数字能达到的可达状态下，如果加上当前数字，判断可达状态是否会更新。为了防止覆盖，应该倒序遍历，确保不会影响上一迭代的可达结果。

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
        int sum = 0;
        for (int i = 0; i < nums.length; i++) {
            sum += nums[i];
        }
      	// 不能分为两半，返回 false
        if (sum % 2 != 0) {
            return false;
        }
        sum /= 2;

        boolean[] dp = new boolean[sum + 1];
      	// 0 一定可达
        dp[0] = true;

        for (int num : nums) {
            for (int j = sum; j >= num; j--) {
                dp[j] = dp[j] || dp[j-num];
            }
        }

        return dp[sum];
    }
}
```

### 零钱兑换

【问题描述】

```text
给定硬币面额数组 coins 和目标金额 amount，求凑成该金额的最少硬币数，不可凑出则返回 -1，每种硬币可以重复使用或不使用。
```

【原理分析】

对于每个金额 i，我们尝试使用每一种硬币 coin，只要当前硬币不超过 i，那么 i 所需的最少硬币数就可能是 i - coin 所需的最少硬币加上 coin 这单个硬币。

【状态表示】

dp[i] 表示凑成金额 i 所需的最少硬币数。

【转移方程】

$$
dp[i] = \min_{coin \in coins}(dp[i - coin] + 1)
$$

【代码实现】

```java
class Solution {
    public int coinChange(int[] coins, int amount) {

        int[] dp = new int[amount + 1];
        Arrays.fill(dp, amount + 1);
        dp[0] = 0;

        for (int i = 1; i <= amount; i++) {
            for (int coin : coins) {
                if (coin <= i) {
                    dp[i] = Math.min(dp[i], dp[i - coin] + 1);
                }
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

类似零钱兑换，只不过对于 num，可以使用完全平方数限制在 $1 ～ \sqrt{num}$，先得到较小数的结果，尝试使用每个完全平方数，结果为剩余数的结果 + 1。

【状态表示】

dp[i] 表示组成整数 i 所需的最少完全平方数数量。

【转移方程】

$$
dp[i] = \min_{1 \le j^2 \le i}(dp[i - j^2] + 1)
$$

【代码实现】

```java
class Solution {
    public int numSquares(int num) {
        int[] dp = new int[num + 1];
        
        for (int i = 1; i <= num; i++) {
            dp[i] = i;
            for (int j = 1; j * j <= i; j++) {
                dp[i] = Math.min(dp[i], dp[i - j * j] + 1);
            }
        }

        return dp[num];
    }
}
```



## 状态机 DP

### 股票买卖

【问题描述】

```text
给定一个整数数组 prices，其中第 i 天的价格为 prices[i]。你可以多次买卖股票，但卖出股票后有一天冷冻期，在冷冻期内不能买入，求最大利润。
```

【原理分析】

可以一开始令利润为 0，买股票利润需要扣减股票价格，卖股票利润需要增加股票价格，每天结束时的状态可以区分为三种状况，而每种状况的更新完全取决于昨天状态的三种情况：

- 持仓：可以是昨天持有的没卖，也可以是昨天没有但今天刚开仓；
- 平仓：昨天持有且今天卖出；
- 空仓：要么昨天平仓了，要么昨天也是空仓。

【状态表示】

dp\[i][0] 表示第 i 天持有的最大利润；

dp\[i][1] 表示第 i 天刚卖出的最大利润；

dp\[i][2] 表示第 i 天没持有的最大利润。

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
            // 今天持有的最大利润 = 昨天持有的最大利润 or 昨天没持有但今天买入的最大利润
            dp[i][0] = Math.max(dp[i - 1][0], dp[i - 1][2] - prices[i]);
            // 今天卖出的最大利润 = 昨天持有的最大利润 + 卖出价格
            dp[i][1] = dp[i - 1][0] + prices[i];
            // 今天没持有的最大利润 = 昨天卖出的最大利润 or 昨天没持有的最大利润
            dp[i][2] = Math.max(dp[i - 1][1], dp[i - 1][2]);
        }

        // 最后一天的最大利润肯定是没持有股票，否则一定会卖出
        return Math.max(dp[n - 1][1], dp[n - 1][2]);
    }
}
```