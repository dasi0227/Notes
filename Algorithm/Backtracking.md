# Backtracking



> **回溯算法本质上是一种深度优先的搜索过程，它通过构造一棵状态树，从根节点开始，沿着每一条可能的路径递归探索，当遇到不满足条件的分支时，就回退到上一个状态，尝试其他分支。**



## 目标和

如果每个状态都有 x 个搜素方向（即每个节点都有 x 个子节点），并且问题深度为 n，那时间复杂度就为 O(x^n)，指数级增长，代价极高。

在目标和问题中，**状态的表示为 (index, rest)，根状态为 (length - 1, target)，终结状态为 (-1, 0)**。从根状态开始，可能会有不同的路径反复到达同一个状态，虽然该状态向上的所有路径可能是不一样的，但是向下的所有路径是完全相同的。如果我们之前已经计算过状态 (index, target) 能达到终结状态的路径数为 n，那么再次遇到相同状态时就可以直接复用结果，而无需重新递归搜索。

```java
class Solution {
    public Map<String, Integer> memory = new HashMap<>();

    public int findTargetSumWays(int[] nums, int target) {
        return dfs(nums, nums.length - 1, target);
    }
  	
    public int dfs(int[] nums, int index, int target) {
        if (index == -1) {
            return target == 0 ? 1 : 0;
        }

        String key = index + "," + target;
        if (memory.containsKey(key)) {
            return memory.get(key);
        }

        int plus = dfs(nums, index - 1, target - nums[index]);
        int minus = dfs(nums, index - 1, target + nums[index]);
        int sum = plus + minus;

        memory.put(key, sum);

        return sum;
    }
}
```



## 除法求值

```text
给你一个变量对数组 equations，一个实数值数组 values，其中 equations[i] = [Ai, Bi] 和 values[i] 表示等式 Ai / Bi = values[i]。

再给定一个变量对数组 queries 表示的问题，其中 queries[j] = [Cj, Dj] 表示问题 Cj / Dj。

返回一个 double 数组，double[i] 表示 queries[j] 的答案，如果无法根据已知条件得到，则用 -1.0 替代。
```

根据除法的性质：如果有 a / b = x 和 b / c = y，那么就可以使用 (a / b) * (b / c) 得到 a / c = x * y；转化为数据结构，那就是**如果有 a --x-->b 和 b --y-->c，则有 a --x*y--> c**。

同时，如果可知 a / b，那么自然可知 b / a；转化为数据结构，得到的图是一个无向图。

除此之外，如果我们在深度搜索的时候发现了 a 通过某条路径可以到达 c，则可以直接将 a 与 c 相连并记录结果，那么下次再遇到 c 就可以直接返回结果，不需要重新深度搜索！

```java
class Solution {
    Map<String, Map<String, Double>> graph = new HashMap<>();

    public double[] calcEquation(List<List<String>> equations, double[] values, List<List<String>> queries) {
        double[] ans = new double[queries.size()];

        // 建图
        for (int i = 0; i < equations.size(); i++) {
            String var1 = equations.get(i).get(0);
            String var2 = equations.get(i).get(1);
            double val = values[i];
            graph.putIfAbsent(var1, new HashMap<>());
            graph.putIfAbsent(var2, new HashMap<>());
            graph.get(var1).put(var2, val);
            graph.get(var2).put(var1, 1.0 / val);
        }

        // 查询
        for (int i = 0; i < queries.size(); i++) {
            String var1 = queries.get(i).get(0);
            String var2 = queries.get(i).get(1);
            if (!graph.containsKey(var1) || !graph.containsKey(var2)) {
                ans[i] = -1.0;
            } else if (var1.equals(var2)) {
                ans[i] = 1.0;
            } else {
                ans[i] = dfs(var1, var2, new HashSet<>());
            }
        }

        return ans;
    }

    public double dfs(String current, String target, Set<String> visited) {
        // current 标记为已访问
        visited.add(current);

        // 如果 current 和 target 有连接，直接返回记录的值
        Map<String, Double> neighbors = graph.get(current);
        if (neighbors.containsKey(target)) {
            return neighbors.get(target);
        }

        // 否则遍历邻居来深度搜索
        for (Map.Entry<String, Double> map : neighbors.entrySet()) {
            String neighbor = map.getKey();
            // 如果没有访问过
            if (!visited.contains(neighbor)) {
                double subResult = dfs(neighbor, target, visited);
                // 如果 neighbor 和 target 有连接，则 current 和 target 也可以建立连接
                if (subResult != -1.0) {
                    double total = map.getValue() * subResult;
                    graph.get(current).putIfAbsent(target, total);
                    graph.get(target).putIfAbsent(current, 1.0 / total);
                    return total;
                }
            }
        }

        // 如果遍历邻居来深度搜索都找不到 target，那么就返回 -1.0
        return -1.0;
    }
}
```



