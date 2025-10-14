# Dynamic Planning



## 最大正方形

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



## 打家劫舍

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



## 最大连续乘积

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

