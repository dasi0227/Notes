# Dynamic Planning



## 线性 DP

### 打家劫舍

```text
给定一个代表每个房屋存放金额的非负整数数组，要求在不触动相邻房屋警报的前提下，计算能够偷取的最大金额。
```

经典的动态规划问题，由于价值始终是累加的，不会出现减少的情况，所以对于当前房屋，利益最大只有两个选项：

- 打劫上上个房屋 + 打劫当前房屋：dp[i] = dp[i-2] + nums[i]
- 打劫上个房屋，不打劫当前房屋：dp[i] = dp[i-1]

综上，转移方程为 `dp[i] = Math.max(dp[i-1], dp[i-2] + nums[i]);`，但是需要先确保具有至少两个元素，并且需要给 dp[0] 和 dp[1] 赋初值

```java
class Solution {
    public int rob(int[] nums) {
        int n = nums.length;
        if (n == 0) return 0;
        if (n == 1) return nums[0];

        int[] dp = new int[n];
        dp[0] = nums[0];
        dp[1] = Math.max(nums[0], nums[1]);
        for (int i = 2; i < n; i++) {
            dp[i] = Math.max(dp[i-1], dp[i-2] + nums[i]);
        }

        return dp[n - 1];
    }
}
```

### 最大连续乘积

```text
给你一个整数数组 nums，请你找出数组中乘积最大的非空连续子数组，并返回该子数组所对应的乘积。
```

如果数组中所有数都是正数，那么显然乘的数越多，乘积越大；当出现负数时，符号会反转，使得当前最大值变最小值、最小值变最大值。特别地，如果负数出现偶数次，负负得正，整体乘积依然可能变大。因此，包含当前数的连续子数组乘积的最大或最小值，只可能来源于三种情况：

- 当前数
- 当前数 * 上一个最小数（可能负负得正）
- 当前数 * 上一个最大数（可能正正得正）

所以我们需要两个数组，一个记录最小数，一个记录最大数，结果就是最大数数组中的最大值

```java
class Solution {
    public int maxProduct(int[] nums) {
        int length = nums.length;

        int max_dp[] = new int[length];
        int min_dp[] = new int[length];

        max_dp[0] = nums[0];
        min_dp[0] = nums[0];

        for (int i = 1; i < length; i++) {
            max_dp[i] = Math.max(max_dp[i - 1] * nums[i], Math.max(nums[i], min_dp[i - 1] * nums[i]));
            min_dp[i] = Math.min(max_dp[i - 1] * nums[i], Math.min(nums[i], min_dp[i - 1] * nums[i]));
        }

        int result = max_dp[0];
        for (int i = 1; i < length; i++) {
            result = Math.max(result, max_dp[i]);
        }
        return result;
    }
}
```



## 网格 DP

### 最大正方形

```text
给定一个由 '0' 和 '1' 组成的二维矩阵，找出只包含 '1' 的最大正方形，并返回其面积。
```

动态规划的核心思想是“**当前状态依赖于历史状态**”，因此在本题应该以以“正方形的右下角”为状态基准，即 dp[i][j] 表示以 (i, j) 为右下角的最大正方形边长

注意到：只有当左、上、左上三个方向都能支撑一个边长至少为 n 的正方形时，我们才能在当前格扩展出一个边长为 n+1 的更大正方形，满足的条件为：

- 当前格 matrix[i][j] 自身为 '1'
- 以 (i-1, j-1) 为右下角的正方形边长为 n
- 以 (i-1, j) 为右下角的正方形边长 ≥ n
- 以 (i, j-1) 为右下角的正方形边长 ≥ n

又注意到：如果以 (a, b) 为右下角，能够构成边长为 c 的正方形，那么以 (a, b) 为右下角的更小边长的正方形也必然存在，因此当前格能扩展的最大边长是左边、上边、左上角的正方形边长的最小值再加一

<img src="https://dasi-blog.oss-cn-guangzhou.aliyuncs.com/Java/202510111501374.png" alt="image-20251011150109847" style="zoom: 50%;" />

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

```text
每个房屋都存放一定金额的钱，并且除了根节点外，每个房屋都有唯一的父节点。
如果同一晚间偷了两个直接相连的房屋（即父子关系），警察就会被惊动。
给定这棵二叉树的根节点 root，返回小偷在不惊动警察的前提下，所能偷取的最大金额。
```

对于当前节点，最直观的看只有两个选择方式：

- 打劫当前节点：最大价值 = 当前节点价值 + 左边的两个孙子的最大价值 + 右边的两个孙子的最大价值
- 不打劫当前节点：最大价值 = 左儿子的最大价值 + 右儿子的最大价值

但是这样子来分析的话，不仅要考虑父子关系，还要考虑爷孙关系，过于复杂。实际上，每个节点都可以存储四个价值：【自身价值】、【打劫价值】、【不打劫价值】、【最大价值】

- 【最大价值】 = Max {【打劫价值】, 【不打劫价值】}
- 【打劫价值】 = 【自身价值】 + 【左不打劫价值】 + 【右不打劫价值】
- 【不打劫价值】 = Max {【左最大价值】, 【右最大价值】}

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

### 戳气球

【题目】

```text
给你 n 个气球，每个气球上写着一个数字 nums[i]。你可以选择一个气球 i 戳破，得到的硬币数为 nums[left] * nums[i] * nums[right]，如果左右两边不存在气球，则数值可以看作为 1。戳破后，只有气球 i 会消失。
求出能获得的最多硬币数。
```

【原理】

对于气球区间 (i, j)，如果最后戳破的气球是其中的 k，那么戳破的得分为 arr[i] * arr[k] * arr[j]，并且此时 (i, k) 与 (k, j) 区间的气球已经全部戳完。所以问题自然分解为两个独立子区间的最优子结构，即 (i, k) 与 (k, j) 得到的分数。

【状态表示】

dp\[i][j] 表示在开区间 (i, j) 内，戳破所有气球能获得的最大金币数

【转移方程】

撒
$$
dp[i][j] = \max_{i < k < j}\big( dp[i][k] + dp[k][j] + arr[i] \times arr[k] \times arr[j] \big)
$$




## 背包 DP

### 分割等和子集

```text
给你一个只包含正整数的非空数组 nums，请你判断是否可以将这个数组分割成两个子集，使得两个子集的元素和相等。
```

这道题的关键在于转换问题：分割成等和子集，就代表我们只要用数组中的部分数，能够得到总和的一半即可

- dp[i]：**表示当前迭代下目标和为 i 时是否可以利用数组得到**
- boolean dp[]：**当前迭代结束时，所有目标和的可达状态**
- 遍历 nums：**如果可以使用之前的所有数字加上当前数字，那么可达状态是否会发生变化**，而之前的所有数字的可达状态已经存储到了 dp 之中
    - 如果 dp[i] = true，则表示即使不加当前数字也可以得到目标和 i，所以 dp[i] 保持 true 不变
    - 否则，使用当前数字，看看剩下 dp[i - num] 是否可达
- 转移方程：`dp[j] = dp[j] || dp[j - num]`

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
          	// 倒序遍历，可以确保不会影响上一迭代的 dp 结果
            for (int j = sum; j >= num; j--) {
                dp[j] = dp[j] || dp[j-num];
            }
        }

        return dp[sum];
    }
}
```

### 零钱兑换

```text
给你一个整数数组 coins 表示不同面额的硬币，以及一个整数 amount 表示总金额，计算并返回可以凑成总金额所需的最少的硬币个数，如果没有任何一种硬币组合能组成总金额，返回 -1。
注意：硬币是可以重复使用的。
```

设 dp[i] 表示凑成金额 i 所需的最少硬币个数，如果无法凑成金额 i，我们让 dp[i] = amount + 1，这个值相当于“不可能”的上限。

对于每个金额 i，我们尝试使用每一种硬币 coin，只要当前硬币不超过 i，那么 i 所需的最少硬币数就可能是 i - coin 所需的最少硬币加上 coin 这单个硬币：`dp[i] = min(dp[i], dp[i - coin] + 1)`

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





## 划分 DP

### 回文子串

对于一个字符串 [i, j)，如果 [i+1, j-1) 是回文的，并且 char[i] == char[j]，那么说明 [i, j) 也是回文的

- end 的取值范围是 [1, length)；start 的取值范围是 [0, end)
- 当 start 和 end 相同的时候，也就是只有一个字符，必然是回文
- 当 start 和 end 差距为 1 的时候，也就是只有两个字符，只要 char[i] == char[j] 就是回文
- 转移方程：`dp[i][j] = (ch_end == ch_start) && (end - start < 3 || dp[start+1][end-1])`

```java
class Solution {
    public int countSubstrings(String s) {
        int n = s.length();
        boolean[][] dp = new boolean[n][n];
        int count = n;

        for (int end = 1; end < n; end++) {
            char ch_end = s.charAt(end);
            for (int start = 0; start < end; start++) {
                char ch_start = s.charAt(start);
                if (ch_end == ch_start && (end - start < 3 || dp[start+1][end-1])) {
                    dp[start][end] = true;
                    count++;
                }
            }
        }

        return count;
    }
}
```

### 单词拆分

```text
给你一个字符串 s 和一个字符串集合 wordDict，如果可以利用字典中出现的一个或多个单词拼接出 s 则返回 true。
注意：不要求字典中出现的单词全部都使用，并且字典中的单词可以重复使用。
```

对于一个字符串 [0, end2)，如果把它分成两部分 [0 ~ end1) 和 [end1~end2)，如果第一个部分能够被拼接出来，并且第二个部分在字典里面，那么 [0, end2) 就可以被拼接出来。所以，应该是先遍历 end，再里面遍历 end1

- end2 的取值范围是 [1, length]，end1 的取值范围是 [0, end2-1]
- 平凡情况 [0, 0] 是可以被拼接出来的
- 转移方程为 `dp[end2] = dp[end1] && dict.contains(str[end1, end2))`

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
