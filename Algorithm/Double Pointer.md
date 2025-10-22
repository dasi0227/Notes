# Double Pointer



   * [快慢指针](#快慢指针)
      * [链表中点](#链表中点)
      * [环检测](#环检测)
   * [双指针](#双指针)
      * [反转链表](#反转链表)
      * [反转单词](#反转单词)



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

其实很类似交换位置，先用一个节点存储 next，然后将 curr.next 指向 prev 即可，最后需要注意的是新的头节点是 prev 而不是 curr

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