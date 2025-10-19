# List



## 快速排序

### 二向划分

快速排序（quick sort）会首先随机选择一个位置的元素作为基准值，然后将小于基准值的数放到左侧，将所有大于等于基准值的数放到右侧，最后将基准值放到正中间，这样一次分区（partition）就可以确定一个基准值的位置是最后排序好的位置。

不需要对左右两边的子数组排序，而是对两个子数组递归地重复同样的分区过程，每次分区都能确保一个元素/基准值排好序，当子数组只有一个元素时，递归就可以终止了

在平均情况下，快速排序的时间复杂度为 O(n log n)，然而如果数组存在大量重复元素，并且基准值选取得不好，那么可能退化为 O(n²)

```java
public void quickSort2(int[] arr, int left, int right) {
    if (left >= right) {
        return;
    }

    // 获取基准值
    int pivotIndex = rand.nextInt(right - left + 1) + left;
    int pivotValue = arr[pivotIndex];

    // 将基准值放到最右边
    swap(arr, pivotIndex, right);

    // 遍历所有元素，维护一个小指针，如果元素小于基准值，就移动到小指针的位置
    int swapIndex = left;
    for (int i = left; i < right; i++) {
        if (arr[i] < pivotValue) {
            swap(arr, i, swapIndex);
            swapIndex++;
        }
    }

    // 将基准值放到小指针的位置，即正中间的位置
    swap(arr, swapIndex, right);

    // 递归遍历左子数组和右子数组
    quickSort2(arr, left, swapIndex - 1);
    quickSort2(arr, swapIndex + 1, right);
}
```

### 三向划分

为了解决数组中存在大量相等元素时快速排序性能退化的问题，可以将数组划分为三个区间：小于基准值区间、大于基准值区间、等于基准值区间。这样就需要维护一个小指针，一个大指针，然后将所有等于基准值的值放到小指针和大指针之间

分区结束后，等于基准值的区间 [lt, gt] 已经自然有序，因此只需递归地对“小于基准值区间”和“大于基准值区间”继续分区即可，等于基准值区间就全部排好序了。相当于，每一次分区都可以确定一个区间（如果没有重复值，这个区间就是单值）

```java
public void quickSort3(int[] arr, int left, int right) {
    if (left >= right) {
        return;
    }

    // 获取基准值
    int pivotIndex = rand.nextInt(right - left + 1) + left;
    int pivotValue = arr[pivotIndex];

    // 遍历所有元素，维护一个小指针、一个大指针、一个遍历指针
    int lt = left;
    int gt = right;
    int i = left;
    while (i <= gt) {
        // 小于：递增小指针，递增遍历指针
        if (arr[i] < pivotValue) swap(arr, i++, lt++);
        // 大于：递增大指针
        else if (arr[i] > pivotValue) swap(arr, i, gt--);
        // 等于：递增遍历指针
        else i++;
    }

    // 递归分区小于子数组和大于子数组
    quickSort3(arr, left, lt- 1);
    quickSort3(arr, gt + 1, right);
}
```

### 快速选择

为了选择第 k 小元素，本质上还是要排序，但是不需要全排，因为我们只是为了找到位置为 k-1 的这个元素即可，而三向划分的快速排序每次分区都可以确定一个区间，所以只需要根据区间位置和位置 k-1，选择某一个分区递归查找即可，如果运气好，甚至第一次分区就可以找到

```java
public int findKthSmallest(int[] arr, int left, int right, int k) {
    int pivotIndex = rand.nextInt(right - left + 1) + left;
    int pivotValue = arr[pivotIndex];

    int lt = left;
    int gt = right;
    int i = left;
    while (i <= gt) {
        if (arr[i] < pivotValue) swap(arr, i++, lt++);
        else if (arr[i] > pivotValue) swap(arr, i, gt--);
        else i++;
    }

    if (k < lt) return findKthSmallest(arr, left, lt - 1, k);
    else if (k > gt) return findKthSmallest(arr, gt + 1, right, k);
    else return arr[k];
}
```



## 链表排序

### 原地排序

```java
class Solution {
    public ListNode sortList(ListNode head) {
        if (head == null || head.next == null) {
            return head;
        }
      
      	// 哨兵节点
        ListNode dummy = new ListNode(-1);
        dummy.next = head;
      
      	// 尾节点
        ListNode tail = head;
      
      	// 遍历当前节点
      	ListNode curr = head.next;
        while (curr != null) {
          	// 当前节点就在尾巴，无需插入
            if (tail.val <= curr.val) {
                tail = curr;
            } 
           	// 寻找插入位置
          	else {
              	// 得到前驱节点
	             	ListNode prev = dummy;
              	while (prev.next.val <= curr.val) {
                  	prev = prev.next;
                }
              	// 得到后继节点
              	tail.next = curr.next;
              	curr.next = prev.next;
              	prev.next = curr;
            }
          	curr = tail.next;
        }
        return dummy.next;
    }
}
```

### 归并排序

归并排序就是对左半边和右半边分别排序，然后将左半边和右半边合并起来，同时当半边只剩 0/1 个元素的时候天然有序，而链表找中点是利用快慢指针

```java
class Solution {
    public ListNode sortList(ListNode head) {
      	// 平凡情况
        if (head == null || head.next == null) {
            return head;
        }
	
      	// 得到左半边和右半边
        ListNode middle = findMiddle(head);
        ListNode right = middle.next;
        middle.next = null;
        ListNode left = head;

      	// 对左半边和右半边排序
        left = sortList(left);
        right = sortList(right);
        
      	// 合并
        return merge(left, right);
    }

  	// 寻找链表中点：快慢指针法
    public ListNode findMiddle(ListNode head) {
        ListNode slow = head;
        ListNode fast = head.next;
        while (fast != null && fast.next != null) {
            slow = slow.next;
            fast = fast.next.next;
        }
        return slow;
    }

  	// 合并两个链表
    public ListNode merge(ListNode left, ListNode right) {
      	// 哨兵节点
        ListNode dummy = new ListNode(-1);
      	// 尾节点
        ListNode tail = dummy;
        while (left != null && right != null) {
          	// 将较小的节点插入
            if (left.val <= right.val) {
                tail.next = left;
                left = left.next;
            } else {
                tail.next = right;
                right = right.next;
            }
            tail = tail.next;
        }
      	// 将剩下的节点直接插入后方
        tail.next = (left != null) ? left : right;
      
      	// 返回头节点
        return dummy.next;
    }
}
```



## 快慢指针

### 链表中点

用快慢指针法，初始令 fast = slow = head，让慢指针一次走一步，快指针一次走两步，终止条件都是 `fast != null || fast.next != null`，最后的 mid = slow

不过需要根据任务来确定 mid 究竟是属于左半部分和右半部分，即是左闭还是右闭，一般是希望谁最后结束，就把 mid 归于哪边

如果把 mid 归于左半部分，那么就有

- 偶数个节点：左半部分和右半部分长度一样
- 奇数个节点：左半部分比右半部分多一

```java
ListNode slow = head, fast = head;
while (fast != null && fast.next != null) {
    slow = slow.next;
    fast = fast.next.next;
}
ListNode mid = fast;
```

### 环检测

一开始令快指针 fast 和慢指针 slow 都位于头部，然后快指针每次走 2 步，慢指针每次走 1 步，因此快指针走的步数始终等于快指针的 2 倍。

假设从头到环入口的距离为 a，环长度为 b，相遇的时候 a 在环内走了 x，b 比 a 多走了 n 环（n 为正整数），那么有

- a 走的距离：a + x
- b 走的距离：a + x + nb
- 距离关系：2(a + x) = a + x + nb

可以得到： a + x = nb，也就是说，慢指针再往前走 a，在环内走的总距离就是 nb 即整数圈，慢指针就回到了环入口

而 a 是从头到环入口的距离为 a，所以我们再新建一个指针 ptr，ptr 和 slow 每次同时走 1 步，当 ptr 走了 a 步到环入口的时候，slow 也正好达到环入口，而由于速度一样，它们只有可能在环入口相遇，所以相遇的位置就是环入口位置

```java
public class Solution {
    public ListNode detectCycle(ListNode head) {
        if (head == null || head.next == null) {
            return null;
        }

        ListNode slow = head, fast = head;
        while (fast != null) {
            slow = slow.next;
            if (fast.next == null) {
                return null;
            } else {
                fast = fast.next.next;
            }
            if (slow == fast) {
                ListNode ptr = head;
                while (ptr != slow) {
                    ptr = ptr.next;
                    slow = slow.next;
                }
                return ptr;
            }
        }
        return null;
    }
}
```



## 双指针

### 反转链表

其实很类似交换位置，先用一个节点存储 next，然后将 curr.next 指向 prev 即可，最后需要注意的是新的头节点是 prev 而不是 curr！

```java
ListNode prev = null;
ListNode curr = head;
while (curr != null) {
    ListNode next = curr.next;
    curr.next = prev;
    prev = curr;
    curr = next;
}
head = prev;
```



### 反转单词

```text
不仅要反转单词，还要处理前后空格，以及单词中间的多余空格
- 输入：s = "  a good   example   "
- 输出："example good a"
```

由于 String 字符串对象是不可变的，所以可以利用 `tocharArray()` 先转换为 `char[]` 字符数组，在最后用 `new String(char[] chars, int begin, int end)` 变回字符串对象

本题主要考验的是双指针法

- 头尾指针：一个指针指向开头，一个指针指向结尾，符合左闭右开原则，一旦发现头指针或尾指针超过数组大小则退出
    1. 头指针找到第一个非空格字符
    2. 令尾指针为头指针
    3. 尾指针找到第一个空格字符，此时 [begin, end) 就是一个单词
    4. 令头指针为尾指针

- 快慢指针：一个指针指向插入位置，一个指针指向字符位置，也就是把字符全部向前移，压缩空格，
    1. 快指针找到第一个非空格字符
    2. 将快指针指向字符放入慢指针指向的位置，然后递增快指针和慢指针，直到快指针遇到空格字符
    3. 快指针再找到第一个非空格字符，此时如果没到尾，说明还有单词，则需要加一个空格字符，递增慢指针

```java
class Solution {
    public String reverseWords(String s) {
        char[] chars = s.toCharArray();
        int len = chars.length;

        // 先整体反转
        reverse(chars, 0, len - 1);

        // 然后逐单词反转
        int begin = 0, end = 0;
        while (begin < len) {
            while (begin < len && chars[begin] == ' ')  begin++;
          	if (begin == len) break;
            end = begin;
            while (end < len && chars[end] != ' ') end++;
            reverse(chars, begin, end - 1);
            begin = end;
        }

        // 最后处理空格
        int slow = 0, fast = 0;
        while (fast < len) {
            while (fast < len && chars[fast] == ' ') fast++;
            while (fast < len && chars[fast] != ' ') chars[slow++] = chars[fast++];
            while (fast < len && chars[fast] == ' ') fast++;
            if (fast < len) chars[slow++] = ' ';
        }

        return new String(chars, 0, slow);
    }


    public void reverse(char[] chars, int begin, int end) {
        while (begin <= end) {
            char tmp = chars[begin];
            chars[begin] = chars[end];
            chars[end] = tmp;
            begin++;
            end--;
        }
    }
}
```



## 特殊数据结构

### LRU

LRU 需要配合 Map 和 LinkedList 实现，Map 负责检查是否命中缓存，而 LinkedList 负责维护最近关系

- 最近使用的节点在链表越靠前
- 当命中缓存的时候，需要将节点移动到最前
- 当缓存满的时候，需要删除最后的节点

由于涉及移除中间节点、尾移除和头插入这类对链表**增删改**的操作，因此使用双向链表结构，同时维护一个头和尾哨兵节点，可以避免空指针的干扰

```java
class LRUCache {
    private static class Node {
        int key, value;
        Node prev, next;
        Node(int k, int v) {
            key = k;
            value = v;
        }
    }

    private final Map<Integer, Node> cache;
    private final int capacity;
    private int size;
    private final Node head, tail;

    public LRUCache(int capacity) {
        this.capacity = capacity;
        this.cache = new HashMap<>();
        this.size = 0;

        // 哨兵节点：避免空指针判断
        head = new Node(-1, -1);
        tail = new Node(-1, -1);
        head.next = tail;
        tail.prev = head;
    }

    public int get(int key) {
        Node node = cache.get(key);
        if (node == null) return -1;
        moveToHead(node);
        return node.value;
    }

    public void put(int key, int value) {
        Node node = cache.get(key);
        if (node != null) {
            node.value = value;
            moveToHead(node);
        } else {
            Node newNode = new Node(key, value);
            cache.put(key, newNode);
            addToHead(newNode);
            size++;
            if (size > capacity) {
                Node removed = removeTail();
                cache.remove(removed.key);
                size--;
            }
        }
    }

    /** 添加到链表头 */
    private void addToHead(Node node) {
        node.next = head.next;
        node.prev = head;
        head.next.prev = node;
        head.next = node;
    }

    /** 移除一个节点 */
    private void removeNode(Node node) {
        node.prev.next = node.next;
        node.next.prev = node.prev;
    }

    /** 将节点移动到头部 */
    private void moveToHead(Node node) {
        removeNode(node);
        addToHead(node);
    }

    /** 移除尾节点 */
    private Node removeTail() {
        Node node = tail.prev;
        removeNode(node);
        return node;
    }
}
```

### 并查集

如果最直观的实现并查集，那么是为每个元素维护一个集合 Set，组成一个列表 List\<Set>，然后每遇到两个符合题意的元素，就从列表中取出这两个元素所在的集合，做一次并集操作再放回。

但是并集操作太耗时了，而且如果无法合并的集合太多，空间浪费也很大。

实际上，我们可以**根据某种原则选举集合中的某个元素作为代表元素，只需要记录当前元素所属集合的代表元素是谁即可**。这样原先并集的操作就可以简化为，**根据规则从两个集合的代表元素中决出一个代表元素，然后更新两个元素的代表元素即可**。

而代表元素如何定义，如何查找当前集合的代表元素，以及如何从两个集合的代表元素中决出一个，就是并查集实现的关键

- 定义：每个集合用一棵树来表示，代表元素就是树的根节点
- 查找：用一个 parent 数组存储当前元素的父节点，根节点的父节点是自己，一直向上找直到根节点
- 合并：为了让查找操作更快，树的高度越小越好，因此对于两颗树，应该让小树挂在到大树的根节点下，这样**只有小部分节点查找时需要多一步，而大部分节点查找步数不变**

```java
class UnionFind {吃一下
    Map<Integer, Integer> parent = new HashMap<>();
    Map<Integer, Integer> size = new HashMap<>();
  
  	// 初始化：每个节点都是根节点，大小为 1
    public UnionFind(int n) {
        parent = new int[n];
        size = new int[n];
        for (int i = 0; i < n; i++) {
            parent[i] = i;
            size[i] = 1;
        }
    }

  	// 查找：不断找父节点直到根节点
    public int find(int curr) {
        int next = parent.get(curr);
        while (curr != next) {
            curr = next;
            next = parent.get(curr);
        }
        return curr;
    }

  	// 合并：如果两个树不一样，则小树挂大树
    public void union(int num1, int num2) {
        int root1 = find(parent, num1);
        int root2 = find(parent, num2);

      	// 已经属于同一个集合
        if (root1 == root2) {
            return;
        }

        int size1 = size.get(root1);
        int size2 = size.get(root2);

        if (size1 < size2) {
            parent.put(root1, root2);
            size.put(root2, size1 + size2);
        } else {
            parent.put(root2, root1);
            size.put(root1, size1 + size2); 
        }
    }
}
```

### TopK

当我们需要找最大的 K 个元素时，实际上可以维护一个大小为 K 的最小堆（注意不是最大堆），当有新元素需要进来时，只需要比较堆头元素和新元素

- 如果新元素 < 堆头元素，则新元素一定小于最小堆所有元素，拒绝添加
- 如果新元素 > 堆头元素，且堆未满，则放到堆尾，然后执行 heapify_up
- 如果新元素 > 堆头元素，且堆已满，则先把堆尾元素放到堆头，执行 heapify_down，然后再把新元素放到堆尾，执行 heapify_up

heapify_up：从堆尾开始一直向上，如果父元素大于当前元素，则交换，否则停止

heapify_down：从堆头开始一直向下，选取两个子元素中存在且较小的那个，如果当前元素大于子元素，则交换，否则停止

```java
public class MinHeap {
    private final int[] heap;
    private int size;

    public MinHeap(int capacity) {
        this.heap = new int[capacity];
        this.size = 0;
    }

    public void insert(int val) {
        // 堆未满：正常插入并上浮
        if (size < heap.length) {
            heap[size] = val;
            heapify_up(size);
            size++;
        }
        // 堆已满：如果新值更大，则替换堆顶并下沉
        else if (val > heap[0]) {
            heap[0] = val;
            heapify_down(0);
        }
        // 否则丢弃
    }

    private void heapify_up(int index) {
        int cur = index;
        while (cur > 0) {
            int parent = (cur - 1) / 2;
            if (heap[parent] > heap[cur]) {
                swap(parent, cur);
                cur = parent;
            } else {
                break;
            }
        }
    }

    private void heapify_down(int index) {
        int cur = index;
        while (cur * 2 + 1 < size) {
            int left = cur * 2 + 1;
            int right = cur * 2 + 2;

            int son = (right < size && heap[right] < heap[left]) ? right : left;

            if (heap[cur] > heap[son]) {
                swap(cur, son);
                cur = son;
            } else {
                break;
            }
        }
    }

    private void swap(int a, int b) {
        int temp = heap[a];
        heap[a] = heap[b];
        heap[b] = temp;
    }
}
```



## 找出消失数字

```text
给你一个含 n 个整数的数组 nums ，其中 nums[i] 在区间 [0, n] 内。请你找出所有在 [0, n] 范围内但没有出现在 nums 中的数字，并以数组的形式返回结果。
注意：要求时间复杂度 O(n)，空间复杂度 O(1)
```

这道题目的关键点就在于，值是 [1, n]，索引是 [0, n-1]，所以如果 value 存在，则把 value - 1当作索引，令 nums[value] 的值为负数，那么最后只要 nums[index] > 0，则该 index 就是没有出现在 nums 中的数字

1. 令 value = abs(nums[i])
2. 如果 nums[value] 是正数，则把其nums[value]
3. 如果 nums[value] 是负数，说明之前已经记录过

```java
class Solution {
    public List<Integer> findDisappearedNumbers(int[] nums) {
        int n = nums.length;
        List<Integer> list = new ArrayList<>();

        int i = 1, j;
        while (i <= n) {
            j = Math.abs(nums[i - 1]);
            if (nums[j - 1] > 0) {
                nums[j - 1] *= -1;
            }
            i++;
        }

        for (i = 0; i < n; i++) {
            if (nums[i] > 0) {
                list.add(i + 1);
            }
        }

        return list;
    }
}
```



## 字符串解码

```text
给定一个经过编码的字符串，返回它解码后的字符串。编码规则为: k[encoded_string]，表示其中方括号内部的 encoded_string 正好重复 k 次，可以保证输入字符串总是有效的。

输入：s = "3[a2[c]]"
输出："accaccacc"

输入：s = "2[abc]3[cd]ef"
输出："abcabccdcdcdef"
```

天然的递归：找到匹配的 []，那么里面的子字符串也可以得到一个解析结果，从而提供给上层的字符串使用。

1. 向下

    - 找到 str = `2[a2[b2[c]]]`
    - 找到 substr1 = `a2[b2[c]]`

    - 找到 substr2 = `b2[c]`

    - 找到 substr3 = `c`

2. 向上

    - 得到 substr3 的解析结果为 `c`

    - 得到 substr2 的解析结果为 `bcc`

    - 得到 substr1 的解析结果为 `abccbcc`

    - 得到 str 的解析结果为 `abccbccabccbcc`

实际上，由于递归总是往前走的，我们可以利用一个递增的全局 index 表示当前正在遍历的字符

- 如果是数字字符，则得到循环得到完整的重复次数，并且递归解析字符串
- 如果是字母字符，则加到字符串后面
- 如果是 ']'，则返回当前得到的字符串
- 如果到达最后，则返回当前得到的字符串

```java
class Solution {
    private int index = 0;

    public String decodeString(String s) {
        StringBuilder sb = new StringBuilder();
        int len = s.length();

        while (index < len) {
            char ch = s.charAt(index);

            // 数字字符
            if (Character.isDigit(ch)) {
                int num = 0;
                while (index < len && Character.isDigit(s.charAt(index))) {
                    num = num * 10 + (s.charAt(index) - '0');
                    index++;
                }

                // 跳过 '['
                index++;
                // 递归解析
                String inner = decodeString(s);
                sb.append(inner.repeat(num));
            }
            // 遇到 ']'，返回当前层结果
            else if (ch == ']') {
                index++;
                break;
            }
            // 普通字符
            else {
                sb.append(ch);
                index++;
            }
        }
        // 返回当前得到的字符串
        return sb.toString();
    }
}
```



