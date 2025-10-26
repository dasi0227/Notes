


## 单调栈

### 柱状图中最大矩形

【问题描述】

```text
给定 n 个非负整数，用来表示柱状图中各个柱子的高度。每个柱子彼此相邻，且宽度为 1。求在该柱状图中，能够勾勒出来的矩形的最大面积。
```

<img src="https://dasi-blog.oss-cn-guangzhou.aliyuncs.com/Java/202510261702768.png" alt="ef8219241b776fecb5cba2f2bdfd256a" style="zoom:50%;" />

【原理分析】



【代码实现】

```java
class Solution {
    public int largestRectangleArea(int[] heights) {
        int n = heights.length;
        Deque<Integer> stack = new ArrayDeque<>();
        int ans = 0;

        for (int i = 0; i <= n; i++) {
            int curHeight = (i == n ? 0 : heights[i]);
            while (!stack.isEmpty() && curHeight < heights[stack.peek()]) {
                int index = stack.pop();
                int height = heights[index];
                int width = stack.isEmpty() ? i : i - stack.peek() - 1;
                ans = Math.max(ans, height * width);
            }
            stack.push(i);
        }

        return ans;
    }
}
```

### 接雨水

【问题描述】

```text
给定 n 个非负整数表示每个宽度为 1 的柱子的高度图，计算按此排列的柱子，下雨之后能接多少雨水。
```

<img src="https://dasi-blog.oss-cn-guangzhou.aliyuncs.com/Java/202510261702323.png" alt="73a6fe8114e8cfaa6a7830cc21321117" style="zoom:50%;" />

【原理分析】

对于容积，本质上只需要确定宽和高，左右边界的较小者限制了最高水位，底限制了最低水位，最高水位 - 最低水位就是容积的高，而左右边界的差就是容积的宽。可以维护一个单调递减栈，如果发现每个元素值大于栈顶元素值，则当前元素值可以作为右边界，能够处理所有元素值小于等于它的左边界

【代码实现】

```java
class Solution {
    public int trap(int[] height) {
        Deque<Integer> stack = new ArrayDeque<>();
        int n = height.length, ans = 0;

        for (int i = 0; i < n; i++) {
            while (!stack.isEmpty() && height[i] > height[stack.peek()]) {
                int bottom = stack.pop();
                if (stack.isEmpty()) break;

                int left = stack.peek();
                int right = i;
                int width = right - left - 1;
                int heightDiff = Math.min(height[left], height[right]) - height[bottom];

                ans += width * heightDiff;
            }
            stack.push(i);
        }
        return ans;
    }
}
```

### 