# Graph



## 广度优先搜索 BFS

**按“层次”逐步扩展节点，用队列保证先入先出，从起点向外一圈一圈搜索**

```java
public void BFS(List<List<Integer>> graph, int start) {
  	// 1. 用一个候选队列记录需要遍历的节点，用一个布尔数组记录每个节点是否已经遍历
    boolean[] visited = new boolean[graph.size()];
    Queue<Integer> queue = new LinkedList<>();

  	// 2. 将起点加入到候选队列，并标记为已访问
    queue.offer(start);
    visited[start] = true;

    while(!queue.isEmpty()) {
      	// 3. 如果候选队列不为空，取出第一个节点
        int cur = queue.poll();
      	
       	// 4. 遍历当前候选者的所有连接节点，输出连接关系
        for (int neighbor : graph.get(cur)) {
            System.out.println(cur + " -> " + neighbor);
          
          	// 5. 如果遍历节点是未访问，则先标记为已访问，然后加入候选队列
            if (!visited[neighbor]) {
                visited[neighbor] = true;
                queue.offer(neighbor);
            }
        }
      	// 6. 循环回到第 3 步，直到所有节点都是已访问
    }
}
```



## 深度优先搜索 DFS

**沿一条路径尽可能深入，用递归探索所有可能的分支**

```java
public void DFS(List<List<Integer>> graph, int cur, boolean[] visited) {
  	// 1. 标记当前节点为已访问
    visited[cur] = true;
  	
  	// 2. 遍历当前节点的所有连接节点，输出连接关系
    for (int neighbor : graph.get(cur)) {
        System.out.println(cur + " -> " + neighbor);
      
      	// 3. 如果连接节点没有被访问过，则接着探索连接节点
        if (!visited[neighbor]) {
            DFS(graph, neighbor, visited);
        }
    }
}
```



## 环检测

### DFS 三色标记法

将 visited 从布尔数组变为整数数组，用 0 表示未访问，1 表示正在访问，2 表示已经访问，如果 DFS 过程中，访问到了标记为 1 的节点，说明存在环

```java
public void findCycleDFS(List<List<Integer>> graph, int cur, int[] visited, List<Integer> path) {
  	// 1. 标记当前节点为正在访问，并添加到路径之中
    visited[cur] = 1;
    path.add(cur);
  
  	// 2. 遍历当前节点的所有连接节点
    for (int neighbor : graph.get(cur)) {
      	// 2.1 如果未访问则 DFS
        if (visited[neighbor] == 0) {
            findCycleDFS(graph, neighbor, visited, path);
        }
      	// 2.2 如果正在访问则输出环路径
        else if (visited[neighbor] == 1) {
            int i = path.indexOf(neighbor);
            String cycle = path.subList(i, path.size())
                    .stream()
                    .map(String::valueOf)
                    .collect(Collectors.joining(" -> "));
            System.out.println("find cycle: " + cycle + " -> " + neighbor);
        }
    }
  
  	// 3. 当前节点 DFS 完成，移出路径，并标记为已访问
    path.remove(path.size() - 1);
    visited[cur] = 2;
}
```

### 拓扑排序

```java
public boolean hasCycleTopo(List<List<Integer>> graph) {
    int n = graph.size();
    int[] indegree = new int[n];

    // 1. 统计每个节点的入度
    for (List<Integer> neighbors : graph) {
        for (int neighbor : neighbors) {
            indegree[neighbor]++;
        }
    }

    // 2. 将所有入度为 0 的节点入队
    Queue<Integer> queue = new LinkedList<>();
    for (int i = 0; i < indegree.length; i++) {
        if (indegree[i] == 0) {
            queue.offer(i);
        }
    }

    // 3. 遍历所有入度为 0 的节点并出队
    int count = 0;
    while (!queue.isEmpty()) {
        int cur = queue.poll();
        // 4. 遍历所有连接节点
        for (int neighbor : graph.get(cur)) {
            // 4.1 将连接节点的入度-1
            indegree[neighbor]--;
            // 4.2 如果连接节点的入度此时为 0，则入队
            if (indegree[neighbor] == 0) {
                queue.offer(neighbor);
            }
        }
        count++;
    }

    // 5. 如果没有处理所有节点，则代表存在环
    return count < n;
}
```



### 独立岛屿问题











