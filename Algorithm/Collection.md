# List



## LRU

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

