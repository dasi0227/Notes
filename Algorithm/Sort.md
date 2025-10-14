# Sort



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

### 快速选择第 k 小元素

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


