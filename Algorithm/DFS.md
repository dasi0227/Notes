# DFS



   * [目标和](#目标和)
   * [除法求值](#除法求值)
   * [括号生成](#括号生成)



## 目标和

【问题描述】

```text
给定一个整数数组 nums 和一个目标值 target。每个元素都可以被赋值为 + 或 -。计算有多少种不同的符号组合，使得这些数字的和等于 target。
```

【状态定义】

(index, sum)：index 表示当前深度搜索到的数组位置，sum 表示当前累计的和

- 起始状态：(0, 0)
- 终止状态：(nums.length, target)

【搜索分支】

对状态 (index, sum)

- 给 nums[i] 加上正号：状态转移为 (i + 1, sum + nums[i])
- 给 nums[i] 加上负号：状态转移为 (i + 1, sum - nums[i])

【代码实现】

```java
class Solution {
    private Map<String, Integer> memo = new HashMap<>();

    public int findTargetSumWays(int[] nums, int target) {
        return dfs(nums, 0, 0, target);
    }

    private int dfs(int[] nums, int index, int sum, int target) {
        // 是否接受
        if (index == nums.length) {
            return sum == target ? 1 : 0;
        }

        // 构造 key
        String key = index + "," + sum;
      
      	// 剪枝
        if (memo.containsKey(key)) {
            return memo.get(key);
        }

        // 搜索加减分支
        int add = dfs(nums, index + 1, sum + nums[index], target);
        int sub = dfs(nums, index + 1, sum - nums[index], target);
        int total = add + sub;
      
      	// 记忆
        memo.put(key, total);
        return total;
    }
}
```



## 除法求值

【问题描述】

```text
给定一组等式 equations 和对应的值 values，表示 equations[i][0] / equations[i][1] = values[i]。
对于一些查询 queries，返回每个 query 的结果。如果无法确定结果，返回 -1.0。
```

【状态定义】

(var1, var2, val)：表示当前推导出的关系 var1 / var2 = val

- 起始状态：以 query\[i][0] 作为被除数
- 终止状态：以 query\[i][1] 作为除数

【搜索分支】

对于状态 (var1, var2, x)，搜索分支是以 var2 作为被除数的算式 (var2, var3, y)，状态转移为 (var1, var3, x * y)

```java
class Solution {
    private Map<String, Map<String, Double>> graph = new HashMap<>();
    private Map<String, Double> memo = new HashMap<>();

    public double[] calcEquation(List<List<String>> equations, double[] values, List<List<String>> queries) {
        // 1. 建图
        for (int i = 0; i < equations.size(); i++) {
            String a = equations.get(i).get(0);
            String b = equations.get(i).get(1);
            double val = values[i];
            graph.putIfAbsent(a, new HashMap<>());
            graph.putIfAbsent(b, new HashMap<>());
            graph.get(a).put(b, val);
            graph.get(b).put(a, 1.0 / val);
        }

        // 2. 查询
        double[] res = new double[queries.size()];
        for (int i = 0; i < queries.size(); i++) {
            String start = queries.get(i).get(0);
            String end = queries.get(i).get(1);
            res[i] = dfs(start, end, new HashSet<>(), 1.0);
        }
        return res;
    }

    private double dfs(String cur, String target, Set<String> visited, double product) {
        // 剪枝 1：不存在该节点
        if (!graph.containsKey(cur) || !graph.containsKey(target)) return -1.0;

        // 剪枝 2：到达目标
        if (cur.equals(target)) return product;

        // 剪枝 3：记忆化查找
        String key = cur + "->" + target;
        if (memo.containsKey(key)) return product * memo.get(key);

        visited.add(cur);
        for (Map.Entry<String, Double> entry : graph.get(cur).entrySet()) {
            String next = entry.getKey();
            if (visited.contains(next)) continue;

            double res = dfs(next, target, visited, product * entry.getValue());
          	// 剪枝 4：找到目标，早停
            if (res != -1.0) {
                memo.put(key, res / product);
                return res;
            }
        }
        return -1.0;
    }
}
```



## 括号生成

【问题描述】

```text
给定一个正整数 n 表示生成括号的对数，生成所有可能且有效的括号组合。
```

【状态定义】

(left, right, path)：left 表示已使用的左括号数量，right 表示已使用的右括号数量，path 表示当前构建的括号字符串

- 起始状态：(0, 0, "")
- 终止状态：(n, n, path)，此时 path 是一个有效的括号组合

【搜索分支】

对当前状态 (left, right, path)

- 如果 left < n，则可以加入左括号，状态转移为 (left + 1, right, path + "(")
- 如果 right < left，则可以加入右括号，状态转移为 (left, right + 1, path + ")")

【代码实现】

```java
class Solution {
    public List<String> generateParenthesis(int n) {
        List<String> res = new ArrayList<>();
        dfs(n, 0, 0, "", res);
        return res;
    }

    private void dfs(int n, int left, int right, String path, List<String> res) {
        // 终止状态
        if (left == n && right == n) {
            res.add(path);
            return;
        }

        // 搜索分支
        if (left < n) {
            dfs(n, left + 1, right, path + "(", res); // 加 '('
        }

        if (right < left) {
            dfs(n, left, right + 1, path + ")", res); // 加 ')'
        }
    }
}
```









