# DFS



   * [加减目标和](#加减目标和)
   * [括号生成](#括号生成)
   * [全排列](#全排列)
   * [组合目标和](#组合目标和)
   * [正则表达式匹配](#正则表达式匹配)
   * [幂集](#幂集)
   * [除法求值](#除法求值)
   * [单词搜索](#单词搜索)



## 加减目标和

【问题描述】

```text
给定一个整数数组 nums 和一个目标值 target。每个元素都可以被赋值为 + 或 -。计算有多少种不同的符号组合，使得这些数字的和等于 target。
```

【状态定义】

(index, sum)：index 表示当前搜索到的数组下标位置，sum 表示当前累计的和

- 起始状态：(0, 0)
- 接受状态：index == nums.length 且 sum == target，表示所有数字均已选择且刚好满足目标和
- 剪枝状态：用一张记忆表存储 index 下到达 sum 的路径数量，下次遇到时直接获取

【搜索分支】

对状态 (index, sum)

- 给 nums[index] 加上正号：状态转移为 (index + 1, sum + nums[index])
- 给 nums[index] 加上负号：状态转移为 (index + 1, sum - nums[index])

【代码实现】

```java
class Solution {
    private Map<String, Integer> memo = new HashMap<>();

    public int findTargetSumWays(int[] nums, int target) {
        return dfs(nums, 0, 0, target);
    }

    private int dfs(int[] nums, int index, int sum, int target) {
        // 接受
        if (index == nums.length) {
            return sum == target ? 1 : 0;
        }

      	// 剪枝
        String key = index + "," + sum;
        if (memo.containsKey(key)) {
            return memo.get(key);
        }
	
        int add = dfs(nums, index + 1, sum + nums[index], target);
        int sub = dfs(nums, index + 1, sum - nums[index], target);
        int total = add + sub;
      
        memo.put(key, total);
        return total;
    }
}
```



## 括号生成

【问题描述】

```text
给定一个正整数 n 表示生成括号的对数，生成所有可能且有效的括号组合。
```

【状态定义】

(left, right, path)：left 表示已使用的左括号数量，right 表示已使用的右括号数量，path 表示当前构造的括号字符串

- 起始状态：(0, 0, "")
- 接受状态：left + right == 2n，表示左右括号均已使用完
- 剪枝状态：right > left，表示右括号数量超过左括号，不可能合法

【搜索分支】

对状态 (left, right, path)

- 如果 left < n，则可以加入左括号，状态转移为 (left + 1, right, path + "(")
- 如果 right < left，则可以加入右括号，状态转移为 (left, right + 1, path + ")")

【代码实现】

```java
class Solution {
    public List<String> generateParenthesis(int n) {
        List<String> res = new ArrayList<>();
        StringBuilder path = new StringBuilder();
        dfs(res, n, 0, 0, path);
        return res;
    }

    private void dfs(List<String> res, int n, int left, int right, StringBuilder path) {
        // 接受
        if (left + right == 2 * n) {
            res.add(path.toString());
            return;
        }
      
        // 剪枝
        if (right > left) {
          	return ;
        }
      				
        if (left < n) {
          	// 转移
            path.append('(');
          	// 递归
            dfs(res, n, left + 1, right, path);
          	// 回溯
            path.deleteCharAt(path.length() - 1);
        }
     
        if (right < left) {
            path.append(')');
            dfs(res, n, left, right + 1, path);
            path.deleteCharAt(path.length() - 1);
        }
    }
}
```



## 全排列

【问题描述】

```text
给定一个不含重复数字的整数数组 nums，返回所有可能的全排列。
```

【状态定义】

(numbers, path)：numbers 是当前可以使用的数字，path 是当前已经构成的组合数

- 起始状态：(nums, [])
- 接受状态：当 numbers == [] 时，即数字都使用完时

【搜索分支】

对当前状态 (number, path)，遍历 number 中的所有数字 num，状态转移为 (number - num, path + num)

【代码实现】

```java
class Solution {
    public List<List<Integer>> permute(int[] nums) {
        List<List<Integer>> ans = new ArrayList<>();
        boolean[] used = new boolean[nums.length];
        dfs(nums, used, new ArrayList<>(), ans);
        return ans;
    }

    private void dfs(int[] nums, boolean[] used, List<Integer> path, List<List<Integer>> ans) {
      	// 接受
        if (path.size() == nums.length) {
            ans.add(new ArrayList<>(path));
            return;
        }

        for (int i = 0; i < nums.length; i++) {
          	// 剪枝
            if (used[i]) continue;
          	// 转移
            used[i] = true;
            path.add(nums[i]);
          	// 递归
            dfs(nums, used, path, ans);
          	// 回溯
            path.remove(path.size() - 1);
            used[i] = false;
        }
    }
}
```



## 组合目标和

【问题描述】

```text
给定一个无重复元素的正整数数组 candidates 和一个目标数 target，找出 candidates 中所有可以使数字和为 target 的组合。同一个数字可以被重复选取。
```

【状态定义】

(index, target, path)：index 表示当前搜索起点，target 表示当前剩余目标和，path 表示当前组合

- 起始状态：(0, target, [])
- 接受状态：target == 0，表示当前 path 的和恰好等于目标值
- 剪枝状态：可以对 candidate 排序，然后按照升序遍历 candidate，如果 target - candidates[i] < 0，表示加上当前的数会溢出，那么加上比它大的数肯定也会溢出

【搜索分支】

对状态 (index, target, path) 和每个 i ∈ [index, n)，状态转移为 (index, target - candidates[index], path + candidates[index])，由于同一个数可以重复使用，因此仍从 index 开始。

【代码实现】

```java
class Solution {
    public List<List<Integer>> combinationSum(int[] candidates, int target) {
        List<List<Integer>> ans = new ArrayList<>();
        List<Integer> path = new ArrayList<>();
        Arrays.sort(candidates);
        dfs(ans, candidates, target, 0, path);
        return ans;
    }

    private void dfs(List<List<Integer>> ans, int[] candidates, int target, int begin, List<Integer> path) {
        // 接受
        if (target == 0) {
            ans.add(new ArrayList<>(path));
            return;
        }

        for (int i = begin; i < candidates.length; i++) {
            // 剪枝
            if (target - candidates[i] < 0) break;

            // 转移
            path.add(candidates[i]);
            // 递归
            dfs(ans, candidates, target - candidates[i], i, path);
            // 回溯
            path.remove(path.size() - 1);
        }
    }
}
```



## 正则表达式匹配

【问题描述】

```text
给定一个字符串 s 和一个模式 p，实现支持 '.' 和 '*' 的正则表达式匹配。
'.' 匹配任意单个字符；'*' 匹配前一个元素零次或多次。匹配要求覆盖整个字符串，判断是否匹配成功。
```

【状态定义】

(sIndex, pIndex)：sIndex 表示当前匹配到字符串 s 的位置，pIndex 表示当前匹配到模式串 p 的位置

- 起始状态：(0, 0)
- 接受状态：pIndex == pLen 且 sIndex == sLen，表示两者同时匹配完成
- 剪枝状态
    - pIndex == pLen 且 sIndex < sLen，表示模式串已匹配完而字符串未匹配完，返回 false
    - sIndex == sLen 且 pIndex < pLen，表示模式串没有匹配完但字符串已经匹配完，模式串剩余必须为 `x*` 的形式，否则无法匹配空串
    - 先前已经得到 pIndex 和 sIndex 下的匹配情况


【搜索分支】

对状态 (sIndex, pIndex)：

- 若下一个字符为 *：
    - 匹配零次：转移为 (sIndex, pIndex + 2)
    - 匹配一次：转移为 (sIndex + 1, pIndex)
- 若下一个字符不是 *：
    - 当前字符是否匹配：转移为 (sIndex + 1, pIndex + 1)
    - 当前字符无法匹配：直接得到 false

【代码实现】

```java
class Solution {
    Map<String, Boolean> memo = new HashMap<>();

    public boolean isMatch(String s, String p) {
        return dfs(s, 0, p, 0);
    }

    private boolean dfs(String s, int sIndex, String p, int pIndex) {
        int sLen = s.length();
        int pLen = p.length();
        String key = sIndex + "," + pIndex;
        
        boolean flag;

        // 剪枝：已有记忆
        if (memo.containsKey(key)) {
            return memo.get(key);
        }

        // 剪枝：p 到末尾
        if (pIndex == pLen) {
            flag = (sIndex == sLen);
            memo.put(key, flag);
            return flag;
        }

        // 剪枝：s 到末尾
        if (sIndex == sLen) {
            for (int k = pIndex; k + 1 < pLen; k += 2) {
                if (p.charAt(k + 1) != '*') {
                    memo.put(key, false);
                    return false;
                }
            }
            flag = ((pLen - pIndex) % 2 == 0);
            memo.put(key, flag);
            return flag;
        }

        // 当前字符是否匹配
        boolean firstMatch = p.charAt(pIndex) == s.charAt(sIndex) || p.charAt(pIndex) == '.';

        // 下一个字符是否是 '*'
        boolean hasStar = (pIndex + 1 < pLen && p.charAt(pIndex + 1) == '*');

        // 可以不消耗当前字符，也可以只消耗当前字符
        if (hasStar) {
            flag = dfs(s, sIndex, p, pIndex + 2) || (firstMatch && dfs(s, sIndex + 1, p, pIndex));
        }
        // 消耗当前字符，递增 1 后递归
        else {
            flag = firstMatch && dfs(s, sIndex + 1, p, pIndex + 1);
        }

        memo.put(key, flag);
        return flag;
    }
}
```



## 幂集

【问题描述】

```text
给你一个整数数组 nums，数组中的元素互不相同，返回该数组所有可能的子集。
```

【代码实现】

```java
class Solution {
    public List<List<Integer>> subsets(int[] nums) {
        List<List<Integer>> ans = new ArrayList<>();
        dfs(ans, nums, 0, new ArrayList<>());
        return ans;
    }

    public void dfs(List<List<Integer>> ans, int[] nums, int begin, List<Integer> path) {
        ans.add(new ArrayList(path));
        while (begin < nums.length) {
            path.add(nums[begin]);
            dfs(ans, nums, ++begin, path);
            path.remove(path.size() - 1);
        }
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
- 接受状态：以 query\[i][1] 作为除数

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



## 单词搜索

【问题描述】

```text
给定一个二维字符网格 board 和一个字符串 word，判断 word 是否存在于网格中。单词必须按照字母顺序，通过相邻的上下左右单元格连接形成。同一个单元格内的字母不能被重复使用。
```

【状态定义】

(row, col, index)：row、col 表示当前搜索到网格中的坐标位置，index 表示当前匹配到单词 word 的第 index 个字符。

- 起始状态：(i, j, 0)，i 和 j 是 board 任意位置
- 接受状态：index == word.length()，表示所有字符已匹配成功
- 剪枝状态：
    - row 或 col 超出边界
    - board\[row][col] != word[index]
    - 当前格子已被访问过


【搜索分支】

对于状态 (row, col, index)

- 上：(row - 1, col, index + 1)
- 下：(row + 1, col, index + 1)
- 左：(row, col - 1, index + 1)
- 右：(row, col + 1, index + 1)

【代码实现】

```java
class Solution {
    public boolean exist(char[][] board, String word) {
        int rows = board.length, cols = board[0].length;
        boolean[][] visited = new boolean[rows][cols];

        for (int row = 0; row < rows; row++) {
            for (int col = 0; col < cols; col++) {
                if (dfs(board, word, row, col, 0, visited)) {
                    return true;
                }
            }
        }
        return false;
    }

    private boolean dfs(char[][] board, String word, int row, int col, int index, boolean[][] visited) {
        if (index == word.length()) return true;
        if (row < 0 || row >= board.length || col < 0 || col >= board[0].length) return false;
        if (visited[row][col]) return false;
        if (board[row][col] != word.charAt(index)) return false;

        visited[row][col] = true;

        boolean found =
            dfs(board, word, row + 1, col, index + 1, visited) ||
            dfs(board, word, row - 1, col, index + 1, visited) ||
            dfs(board, word, row, col + 1, index + 1, visited) ||
            dfs(board, word, row, col - 1, index + 1, visited);

        visited[row][col] = false;
        return found;
    }
}
```

> 不应该先判断合法状态才 dfs，而是把非法状态作为剪枝状态置于最顶层，每次都直接 dfs