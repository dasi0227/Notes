# 集合框架



   * [前置知识](#前置知识)
      * [类关系图](#类关系图)
      * [比较器](#比较器)
   * [Collection](#collection)
      * [关键 API](#关键-api)
         * [toArray](#toarray)
         * [stream](#stream)
         * [iterator](#iterator)
      * [List](#list)
         * [定义](#定义)
         * [ArrayList](#arraylist)
            * [定义](#定义)
            * [构造函数](#构造函数)
            * [扩容机制](#扩容机制)
         * [LinkedList](#linkedlist)
            * [定义](#定义)
            * [区别](#区别)
            * [链接机制](#链接机制)
      * [Set](#set)
         * [定义](#定义)
         * [实现类](#实现类)
      * [Queue](#queue)
         * [定义](#定义)
         * [实现类](#实现类)
         * [阻塞队列](#阻塞队列)
         * [ArrayBlockingQueue](#arrayblockingqueue)
   * [Map](#map)
      * [关键 API](#关键-api)
         * [Entry](#entry)
         * [遍历](#遍历)
      * [实现类区别](#实现类区别)
      * [HashMap](#hashmap)
         * [结构](#结构)
            * [Node](#node)
            * [bucket](#bucket)
         * [计算原理](#计算原理)
            * [槽位计算](#槽位计算)
            * [哈希计算](#哈希计算)
            * [迁移计算](#迁移计算)
         * [源码分析](#源码分析)
            * [字段](#字段)
            * [hash](#hash)
            * [putVal](#putval)
            * [getNode](#getnode)
            * [resize 方法](#resize-方法)
      * [ConcurrentHashMap](#concurrenthashmap)
         * [线程安全原理](#线程安全原理)
         * [协助迁移](#协助迁移)
         * [源码分析](#源码分析)
            * [tabAt / casTabAt / setTabAt](#tabat-castabat-settabat)
            * [putVal](#putval)
            * [get](#get)
   * [使用规范](#使用规范)
      * [集合判空](#集合判空)
      * [集合去重](#集合去重)
      * [集合转 Map](#集合转-map)
      * [集合转数组](#集合转数组)
      * [数组转集合](#数组转集合)



## 前置知识

### 类关系图

![918bdc2b0fd7be877965381ac34bbec0](https://dasi-blog.oss-cn-guangzhou.aliyuncs.com/Java/202509221449411.png)

### 比较器

比较器是**用来比较两个相同类的对象“谁先谁后”的一种机制，不能简单理解为“谁大谁小”**，因为排序规则完全可以不依赖于数值，而是任何自定义逻辑

| **接口** | **方法** | **实现** | **数量** | **场景** |
| ------------------ | ------------------------ | ------ | ------------ | ------------------------------------------ |
| **Comparable\<T>** | int compareTo(T o); | 当前类 | 只能实现一个 | 让一个类自己具备比较内部元素的能力 |
| **Comparator\<T>** | int compare(T o1, T o2); | 外部类 | 可以实现多个 | 让一个类使用外部定义的比较器来比较内部元素 |

**Java 的所有包装类（Integer、Double、Long、Float、Short、Byte、Character、Boolean）都已经实现了 Comparable\<T> 接口**，因此它们自带 compareTo(T other) 方法

不过需要注意的是，**部分包装类中的 compare 方法不是实现 Comparator 接口重写的，而是自定义的静态方法**

```java
// 年龄比较：低于 18 一档，18-40 一档，40-60 一档，60 以上一档
public class AgeComparator implements Comparator<Employee> {
    @Override
    public int compare(Employee e1, Employee e2) {
      	int age1 = getAgeGroup(e1.getAge();
				int age2 = getAgeGroup(e2.getAge();
        return Integer.compare(age1, age2);
    }
  
    private int getAgeGroup(int age) {
        if (age < 18) return 0;
        else if (age < 40) return 1;
        else if (age < 60) return 2;
        else return 3;
    }
}

// 薪水比较：超过 10000 的扣 10%，低于 10000 的扣 5%
public class SalaryComparator implements Comparator<Employee> {
    @Override
    public int compare(Employee e1, Employee e2) {
      	double salary1 = getSalaryDeduct(e1.salary);
        double salary2 = getSalaryDeduct(e2.salary);
        return Double.compare(salary1, salary2);
    }
  
    private double getSalaryDeduct(double salary) {
        if (salary > 10000) {
            return salary * 0.9;
        } else {
            return salary * 0.95;
        }
    }
}

public class Employee implements Comparable<Employee> {
  	public String name;
  	public int age;
  	public Double salary;
  
  	// 引入外部比较器类
  	private AgeComparator ageComparator = new AgeComparator();
    private SalaryComparator salaryComparator = new SalaryComparator();
  
  	// 实现自己的比较器
    @Override
    public int compareTo(Employee other) {
        int ageCmp = ageComparator.compare(this, other);
      	if (ageCmp != 0) return ageCmp;
      	
       	int nameCmp = this.name.compareTo(other.name);
      	if (nameCmp != 0) return nameCmp;
      
      	return salaryComparator.compare(this, other);
    }	
}
```



## Collection

### 关键 API

#### toArray

**Array 是 Java 的一种基础数据结构，不是一个类**，用来存放固定长度、相同类型的数组，插入和删除需要手动移动元素，通过 `Type[] array = new Type[length]` 创建。

Collection 提供了 toArray 函数，将集合元素重新封装为 Array 基础数据结构返回

- `Object[] toArray()`：把集合中的所有元素复制到一个新的 Object[] 数组中，需要手动强转才能得到具体类型
- `<T> T[] toArray(T[] a)`：把集合中的所有元素复制到一个指定类型的数组中，如果数组 a 不够大会新建一个和 a 类型相同、大小刚好的数组并返回

#### stream

stream() 是 Java8 引入的新特性，**可以把 Collection 对象转换成 Stream 对象**，而 Stream 是一种特殊的结构，它主要负责对数据执行链式、声明式操作，它不存储数据，只用于操作数据，也就是说数据只能被消费一次，用完需要重新生成

Stream 操作的核心就是**让元素排列好，一个接一个地像流水线一样执行中间操作，而且每次中间操作的结果都是一个新的流，直到遇到终止操作才得到成品**

> 链式调用的中间操作不会立即执行，而是做到终结操作才会触发执行

假设有 nums = {1,2,3,4,5}

- 过滤 filter（中间）：依次把元素传给 Predicate 函数，返回 true 的才保留到流

    ```java
    List<Integer> even = nums.stream()
        .filter(n -> n % 2 == 0)
        .collect(Collectors.toList());   // [2, 4]
    ```

- 映射 map（中间）：依次把元素传给 Function 函数，返回结果填充到流

    ```java
    List<Integer> double = nums.stream()
        .map(n -> n * 2)
        .collect(Collectors.toList());   // [2, 4, 6, 8, 10]
    ```

- 排序 sorted（中间）：传入一个 Comparator 对象，返回排序好的结果作为流

    ```java
    List<Integer> desc = nums.stream()
        .sorted(Comparator.reverseOrder())
        .collect(Collectors.toList());   // [5, 4, 3, 2, 1]
    ```

- 聚合 reduce（终结）：把初始值/上个值和当前值传给 BinaryOperator 函数，直到最后得到一个结果

    ```java
    // 求和：15
    int sum = nums.stream().reduce(0, Integer::sum);
    
    // 求最大值：5
    int max = nums.stream().reduce(Integer.MIN_VALUE, Integer::max);
    
    // 求最小值：1
    int min = nums.stream().reduce(Integer.MAX_VALUE, Integer::min);
    
    // 求乘积：120
    int product = nums.stream().reduce(1, (a, b) -> a * b);
    ```

- 收集 collect（终结）：把流中的元素收集为一个新集合，如果是 toMap 还需要传入两个 Function 表示如何生成键和值

    ```java
    // ArrayList([1, 2, 3, 4, 5])
    List<Integer> list = nums.stream().collect(Collectors.toList());
    
    // HashSet([1, 2, 3, 4, 5])
    Set<Integer> set = nums.stream().collect(Collectors.toSet());
    
    // HashMap({1=1, 2=2, 3=3, 4=4, 5=5})
    Map<String, Integer> map = nums.stream().collect(Collectors.toMap(n -> n + "", n -> n));
    ```

- 遍历 forEach（终结）：对流中的每个数据执行 Consumer 函数

    ```java
    nums.stream().forEach(n -> System.out.println("元素: " + n));
    ```

#### iterator

Iterator 是 Java 集合框架中的迭代器接口，用来遍历集合中的元素，所有继承了 Collection 接口的集合类（List、Set、Queue 等）都提供了 iterator() 方法，可以返回已经实现了 Iterator 接口的对象

- `boolean hasNext()`：判断是否还有元素未遍历
- `E next()`：返回下一个元素，并将指针向后移动
- `void remove()`：在迭代过程中，安全地删除上一次由 next() 方法返回的元素
- `default void forEachRemaining(Consumer<? super E> action)`：从当前位置开始，对剩余的每个元素执行指定操作

由于迭代器不保证线程安全，因此当线程正在使用迭代器遍历集合时，集合可能会被其他线程**结构性修改（add / remove / clear 等）**，所以 Java 提供了一个 fail-fast 机制，在集合对象底层会维护一个 modCount 来记录修改的次数

1. 当调用 iterator() 创建迭代器时，会把 modCount 的当前值保存到 expectedModCount
2. 在迭代过程中都会检查 expectedModCount 是否等于 modCount
3. 如果不一致说明集合在迭代期间被结构性修改，立刻抛出 **ConcurrentModificationException** 异常

### List

#### 定义

**List 存储一个元素数组，强调连续性，可以通过索引访问元素，也可以放入重复元素，典型操作有：get、add、remove**

#### ArrayList

##### 定义

为了提供比 Array 更方便的数组使用，Java 在集合框架提供了 ArrayList 类

- 根据实际存储的元素**动态地扩容**，创建时允许不指定容量，默认容量为 10，每次扩容 1.5 倍
- 只能**存储对象**，如果是基本数据类型需要**包装类**，同时允许使用**泛型**来确保类型安全
- **线程不安全**，多线程同时对同一个 ArrayList 对象操作可能会导致数据不一致
- ArrayList **在底层维护了一个 Array 数组 `Object[] elementData`** 表示存放的元素和一个整型 `int size` 表示存放元素的个数

##### 构造函数

如果使用无参构造或者容量为 0 的有参构造，实际上都是**初始化了一个空数组**，只有在真正添加元素的时候才会分配内存

```java
transient Object[] elementData; 
private int size;

private static final int 			DEFAULT_CAPACITY = 10;
private static final Object[] DEFAULTCAPACITY_EMPTY_ELEMENTDATA = {};
private static final Object[] EMPTY_ELEMENTDATA = {};

// 无参构造
public ArrayList() {
    this.elementData = DEFAULTCAPACITY_EMPTY_ELEMENTDATA;
}

// 有参构造
public ArrayList(int initialCapacity) {
    if (initialCapacity > 0) {
        this.elementData = new Object[initialCapacity];
    } else if (initialCapacity == 0) {
        this.elementData = EMPTY_ELEMENTDATA;
    } else {
        throw new IllegalArgumentException("Illegal Capacity: " + initialCapacity);
    }
}
```

##### 扩容机制 

扩容是在添加元素时触发的，它**在添加元素到数组之前必须确保容量足够**

```java
// 添加元素
public boolean add(E e) {
    ensureCapacityInternal(size + 1);
    elementData[size++] = e;
    return true;
}

// 确保内部容量足够
private void ensureCapacityInternal(int minCapacity) {
    ensureExplicitCapacity(calculateCapacity(elementData, minCapacity));
}

// 计算所需容量：如果数组未初始化，则所需容量为默认容量
private static int calculateCapacity(Object[] elementData, int minCapacity) {
    if (elementData == DEFAULTCAPACITY_EMPTY_ELEMENTDATA) {
        return Math.max(DEFAULT_CAPACITY, minCapacity);
    }
    return minCapacity;
}

// 判断是否需要扩容：所需容量 > 数组长度
private void ensureExplicitCapacity(int minCapacity) {
    modCount++;
    if (minCapacity - elementData.length > 0)
        grow(minCapacity);
}

// 扩大容量：先扩大为之前的 1.5 倍，不够则直接扩容为所需容量
private void grow(int minCapacity) {
    int oldCapacity = elementData.length;
    int newCapacity = oldCapacity + (oldCapacity >> 1);
    if (newCapacity - minCapacity < 0)
        newCapacity = minCapacity;
    if (newCapacity - MAX_ARRAY_SIZE > 0)
        newCapacity = hugeCapacity(minCapacity);
    elementData = Arrays.copyOf(elementData, newCapacity);
}
```

可以发现最后执行扩容的，实际是 **Arrays 工具类的静态方法 copyOf()**

```java
public static Object[] copyOf(Object[] original, int newLength) {
    // 1. 创建一个扩大容量后的全新数组
    Object[] copy = new Object[newLength];

    // 2. 把原数组的数据复制到新数组中
    System.arraycopy(original, 0, copy, 0, Math.min(original.length, newLength));

    // 3. 返回拷贝后的新数组
    return copy;
}
```

还没完，最后的最后执行扩容的，是 **System 类的 arraycopy 方法，而这是一个 native 方法，底层由 C/C++ 直接实现，只需要指定源数组的拷贝位置、目标数组的粘贴位置和拷贝粘贴的元素数量**

```java
public static native void arraycopy(
    Object src,       // 源数组
    int srcPos,       // 源数组的起始位置
    Object dest,      // 目标数组
    int destPos,      // 目标数组的起始位置
    int length        // 复制的长度
);
```

#### LinkedList

##### 定义

LinkedList 是 Java 集合框架中基于双向链表实现的 List

- 同时实现了 **List 和 Deque** 接口，既可以作为顺序存储的列表，也可以作为双端队列使用
- 元素被包装在**内部静态类 Node** 之中
- LinkedList 对象本身只记录头节点、尾节点和链表长度

```java
transient int size = 0;          // 链表长度
transient Node<E> first;         // 头节点
transient Node<E> last;          // 尾节点

private static class Node<E> {
    E item;                      // 当前节点的数据
    Node<E> next;                // 后继节点
    Node<E> prev;                // 前驱节点
    Node(Node<E> prev, E element, Node<E> next) {
        this.item = element;
        this.next = next;
        this.prev = prev;
    }
}
```

##### 区别

| **特性** | **ArrayList** | **LinkedList** |
| ----------------- | ---------------------- | -------------------------------- |
| **底层结构** | Object[] elementData | Node{prev,item,next} |
| **随机访问效率** | O(1)，直接通过下标访问 | O(n)，必须遍历链表 |
| **插入/删除效率** | O(n)，需要移动大量元素 | O(1)，只需修改前后指针 |
| **空间占用** | 紧凑存储 | 分散存储，多了 next 和 prev 引用 |
| **线程安全性** | 非线程安全 | 非线程安全 |
| **适用场景** | 读多写少，频繁随机访问 | 写多读少，频繁插入删除 |

##### 链接机制

当调用 add(element) 时，不指定插入位置默认插入到链表尾部，执行的是 linkLast 方法

```java
void linkLast(E e) {
  	// 保存当前链表的尾节点引用
    final Node<E> l = last;
  
  	// 创建新节点，前驱指向 l，元素值为 e，后继为 null
    final Node<E> newNode = new Node<>(l, e, null);
    
  	// 更新 LinkedList 的尾节点指针指向最新的尾节点
    last = newNode;
	  
  	// 如果是第一次添加，那么头节点和尾节点都要指向 newNode
    if (l == null)
        first = newNode;
  	// 如果不是第一次添加，只需要把旧尾节点的 next 指针指向新节点
    else
        l.next = newNode;
  	
  	// 元素数量 + 1
    size++;
  	// 修改次数 + 1
    modCount++;
}
```

当调用 add(index, element) 时，会先执行 node 获取到 index 位置的节点，然后执行 linkBefore 方法

```java
Node<E> node(int index) {
    // 如果 index 小于链表长度的一半，从前往后找
    if (index < (size >> 1)) {
        Node<E> x = first;
        for (int i = 0; i < index; i++)
            x = x.next;
        return x;
    } 
	  // 否则，从后往前找
  	else {
        Node<E> x = last;
        for (int i = size - 1; i > index; i--)
            x = x.prev;
        return x;
    }
}

void linkBefore(E e, Node<E> succ) {
  	// 获取 succ 的前驱节点 pred
    final Node<E> pred = succ.prev;
  	
    // 创建新节点，前驱指向 pred，元素值为 e，后继指向 succ
    final Node<E> newNode = new Node<>(pred, e, succ);
    
  	// 将 succ 的前驱引用更新为新节点
    succ.prev = newNode;
  
    // 如果 succ 是第一个节点，则需要更新头节点
    if (pred == null)
        first = newNode;
  	// 如果 succ 不是第一个节点，则把 pred 的后继引用更新为新节点
    else
        pred.next = newNode;
  
  	// 元素数量 + 1
    size++;
  	// 修改次数 + 1
    modCount++;
}
```

当调用 remove 或 clear 方法，执行的都是 unlink 方法

```java
E unlink(Node<E> x) {
    // 获取当前节点的前驱节点、后继节点和元素
    final Node<E> prev = x.prev;
    final Node<E> next = x.next;
    final E element = x.item;

    // 如果当前节点是头节点，直接让链表头指向当前节点的下一个节点
    if (prev == null) {
        first = next;
    } 
  	// 如果当前节点不是头节点，则将前一个节点的 next 指针指向当前节点的下一个节点
  	else {
        prev.next = next;
        x.prev = null;
    }

    // 如果当前节点是尾节点，直接让链表尾指向当前节点的前一个节点
    if (next == null) {
        last = prev;
    } 
  	// 如果当前节点不是尾节点，则将下一个节点的 prev 指针指向当前节点的前一个节点
  	else {
        next.prev = prev;
        x.next = null;
    }

    // 将当前节点元素置为 null
    x.item = null;
  
    // 元素数量 - 1
    size--;
    // 修改次数 + 1
    modCount++;
    return element;
}
```

### Set

#### 定义

**Set 存储一个元素集合，强调唯一性和无序性，不能通过索引访问元素，不允许放入重复元素，典型操作有：contains、add、remove**

#### 实现类

| **特性** | **HashSet** | **LinkedHashSet** | **TreeSet** |
| ----------------- | ---------------------- | ---------------------- | ------------------------ |
| **底层结构** | HashMap | LinkedHashMap | TreeMap |
| **元素顺序** | 无序 | 有序 | 有序 |
| **允许 null** | 允许 1 个 null 元素 | 允许 1 个 null 元素 | 不允许 null |
| **查找/插入效率** | O(1) | O(1) | O(log n) |
| **去重依据** | hashCode() + equals() | hashCode() + equals() | Comparable / Comparator |
| **适用场景** | 只关心去重，不关心顺序 | 需要去重且保持插入顺序 | 需要去重且保持自定义顺序 |

### Queue

#### 定义

**Queue 存储一个元素序列，强调有序性和首尾操作，不能通过索引访问元素，但允许放入重复元素，典型操作有 offer、poll、peek**

#### 实现类

| **实现类** | **底层结构** | **线程安全** | **是否有界** | **出队顺序** |
| --------------------- | --------------- | ------------ | ------------ | -------- |
| **LinkedList** | 双向链表 | ❌ | ❌ | 插入 |
| **ArrayDeque** | 循环数组 | ❌ | ❌ | 插入 |
| **PriorityQueue** | 二叉堆 | ❌ | ❌ | 比较 |
| **ConcurrentLinkedQueue** | 单向链表 + CAS | ✅ | ❌ | 插入 |
| **LinkedBlockingQueue** | 双向链表 + 双锁 | ✅ | ✅ | 插入 |
| **ArrayBlockingQueue** | 循环数组 + 单锁 | ✅ | ✅ | 插入 |
| **PriorityBlockingQueue** | 二叉堆 + 单锁 | ✅ | ❌ | 比较 |

#### 阻塞队列

BlockingQueue 继承自 Queue，是 JUC 提供的接口，内部通过锁或 CAS 保证线程安全，最常用的就是生产者-消费者模型

- 插入 put：当队列满时，阻塞直到有空位
- 移除 take：当队列空时，阻塞直到有新元素
- 超时 offer/poll ：允许设置 timeout

| **操作类型** | **抛异常** | **返回值** | **限时** | **条件变量** |
| ---------- | --------- | -------- | ----------------------- | -------- |
| **添加** | add(e) | offer(e) | offer(e, timeout, unit) | put(e) |
| **获取并删除** | remove() | poll() | poll(timeout, unit) | take() |
| **获取不删除** | element() | peek() | - | - |

#### ArrayBlockingQueue

字段

```java
// 底层用数组存放队列元素
final Object[] items;

// 下一个取出元素的位置，随着消费移动
int takeIndex;

// 下一个放入元素的位置，随着生产移动
int putIndex;

// 当前队列中已有元素的数量
int count;

// 负责阻塞消费
private final Condition notEmpty;

// 负责阻塞生产
private final Condition notFull;
```

构造函数

```java
public ArrayBlockingQueue(int capacity, boolean fair) {
  // 必须有容量
  if (capacity <= 0)
      throw new IllegalArgumentException();
  // 创建数组
  this.items = new Object[capacity];
  // 创建 ReentrantLock
  lock = new ReentrantLock(fair);
  // 用 ReentrantLock 创建两个条件变量
  notEmpty = lock.newCondition();
  notFull =  lock.newCondition();
}
```

put 方法

```java
public void put(E e) throws InterruptedException {
    // 确保插入的元素不为空
    checkNotNull(e);
    
  	// 获取锁
    final ReentrantLock lock = this.lock;
  	
  	// 加锁
    lock.lockInterruptibly();
    try {
      	// 如果当前存在元素数量=容量，则线程被阻塞到条件变量中
        while (count == items.length)
            notFull.await();
	      // 否则元素入队
        enqueue(e);
    } finally {
        // 解锁
        lock.unlock();
    }
}

private void enqueue(E x) {
   	// 获取数组
    final Object[] items = this.items;
    
  	// 往 putindex 位置添加元素
    items[putIndex] = x;
    
  	// 更新 putindex 和 count
    if (++putIndex == items.length)
        putIndex = 0;
    count++;
    
  	// 通知队列非空
    notEmpty.signal();
}
```

take 方法

```java
public E take() throws InterruptedException {
    // 获取锁
    final ReentrantLock lock = this.lock;

    // 加锁
    lock.lockInterruptibly();
    try {
      	// 如果当前存在元素数量=0，则线程被阻塞到条件变量中
				while (count == 0)
						notEmpty.await();
      	// 否则元素出队
      	return dequeue();
    } finally {
        // 解锁
        lock.unlock();
    }
}

private E dequeue() {
    // 获取数组
    final Object[] items = this.items;
  
    // 从 takeIndex 位置取出元素并置空
    @SuppressWarnings("unchecked")
    E x = (E) items[takeIndex];
    items[takeIndex] = null;
  
    // 更新 putindex 和 count
    if (++takeIndex == items.length)
        takeIndex = 0;
    count--;
  
    if (itrs != null)
        itrs.elementDequeued();
    
  	// 通知队列非满
    notFull.signal();
    return x;
}
```



## Map

### 关键 API

#### Entry

Entry<K, V> 是 Map 的一个内部嵌套接口，用来表示 Map 中的一个键值对

```java
interface Entry<K, V> {
  	// 返回 key
    K getKey();
  
  	// 返回 value
    V getValue();
  	
  	// 修改 value 并返回旧值
    V setValue(V value);
  
  	// 按 key 的自然顺序返回一个比较器
    public static <K extends Comparable<? super K>, V> Comparator<Map.Entry<K, V>> comparingByKey() {
        return (Comparator<Map.Entry<K, V>> & Serializable)
            (c1, c2) -> c1.getKey().compareTo(c2.getKey());
    }
  
	  // 按 value 的自然顺序返回一个比较器
    public static <K, V extends Comparable<? super V>> Comparator<Map.Entry<K, V>> comparingByValue() {
        return (Comparator<Map.Entry<K, V>> & Serializable)
            (c1, c2) -> c1.getValue().compareTo(c2.getValue());
  }

  	// 根据 key 使用自定义比较器返回一个比较器
    public static <K extends Comparable<? super K>, V> Comparator<Map.Entry<K, V>> comparingByKey() {
        return (Comparator<Map.Entry<K, V>> & Serializable)
            (c1, c2) -> c1.getKey().compareTo(c2.getKey());
    }

  	// 根据 value 使用自定义比较器返回一个比较器
    public static <K, V> Comparator<Map.Entry<K, V>> comparingByValue(Comparator<? super V> cmp) {
        Objects.requireNonNull(cmp);
        return (Comparator<Map.Entry<K, V>> & Serializable)
            (c1, c2) -> cmp.compare(c1.getValue(), c2.getValue());
    }
}
```

#### 遍历

Map 虽然没有 iterator() 方法来获得迭代器，但是有三种方法可以先获取到 Collection，再通过 iterator() / get() 来遍历

- **entrySet()**：可以获得所有键值对的集合 `Set<Map.Entry<K,V>>`
- **keySet()**：可以获取所有键的集合 `Set<K>`
- **values()**：可以获取所有值的集合 `Collection<V>`

### 实现类区别

| **实现类** | **底层结构** | **是否有序** | **线程安全** | **null 支持** | **适用场景** |
| --------------------- | ------------------ | ----------------- | ------------ | --------------------------------- | -------------------------- |
| **HashMap** | 数组 + 链表/红黑树 | 无序 | ❌ | 允许 1 个 null key，多 null value | 单线程 |
| **Hashtable** | 数组 + 链表 | 无序 | ✅ | 不允许 null key / value | 已经过时 |
| **TreeMap** | 红黑树 | 按 key 自定义排序 | ❌ | 不允许 null key，允许 null value | 需要排序和搜索 |
| **LinkedHashMap** | 数组 + 双向链表 | 保持插入顺序 | ❌ | 允许 1 个 null key，多 null value | 需要保持插入顺序和按序遍历 |
| **ConcurrentHashMap** | 数组 + 链表/红黑树 | 无序 | ✅ | 不允许 null key / value | 高并发 |

### HashMap

#### 结构

##### Node

在 HashMap 中，每个键值对都是 Map.Entry<K,V> 的实现类 Node<K,V> 对象，它们被收集到了 **Node<K,V>[] table** 中

- key / value：存放键和值
- hash：保存 key 的哈希值
- next：**指向桶/槽位中同一链表的下一个节点**

```java
static class Node<K,V> implements Map.Entry<K,V> {
    final int hash;
    final K key;
    V value;
    Node<K,V> next;

    Node(int hash, K key, V value, Node<K,V> next) {
        this.hash = hash;
        this.key = key;
        this.value = value;
        this.next = next;
    }

    public final K getKey()        { return key; }
    public final V getValue()      { return value; }
    public final String toString() { return key + "=" + value; }

    public final int hashCode() {
        return Objects.hashCode(key) ^ Objects.hashCode(value);
    }

    public final V setValue(V newValue) {
        V oldValue = value;
        value = newValue;
        return oldValue;
    }

    public final boolean equals(Object o) {
        if (o == this)
            return true;

        return o instanceof Map.Entry<?, ?> e
                && Objects.equals(key, e.getKey())
                && Objects.equals(value, e.getValue());
    }
}
```

##### bucket

可以把 table 的每个索引位置都看作为一个哈希桶 bucket，之所以叫哈希桶是因为它不只存一个元素，而是可能存放多个哈希值一样的元素，**这些在同一个桶的多个元素用链表/红黑树的方式连接起来，而 table 每个索引位置实际只存储该链表的头节点或红黑树的根节点**

- **capacity：是 table 的数组长度，即哈希桶的数量**
- **length：是 bucket 中的元素个数，即链表/红黑树的大小**
- **size：是 HashMap 的节点个数，即实际存储的键值对数量**

其中红黑树是一种高效增删改查的数据结构，它保证操作的**时间复杂度都是 O(logn)**，只不过红黑树会比链表占据更多内存空间，所以**一开始默认使用链表，随着元素添加，根据阈值来决定是对链表进行扩容还是进行树化**

- **length >= TREEIFY_THRESHOLD && capacity < MIN_TREEIFY_CAPACITY：扩容 resize，把所有元素重新分配到新桶中**
- **length >= TREEIFY_THRESHOLD && capacity >= MIN_TREEIFY_CAPACITY：树化 treeify，只把该桶的 Node 转换为 TreeNode**

![image-20250923114637792](https://dasi-blog.oss-cn-guangzhou.aliyuncs.com/Java/202509231146853.png)

#### 计算原理

##### 槽位计算

由于 hash 是一个 int 值，有 40 多亿个不同值，显然无法直接作为索引，因此预先创建好一定长度的 table，将 hash 再次映射到槽位号

- `index = hash % capacity`：传统方法是进行取余运算，得到的余数就是槽位号，但是 % 运算很慢
- `index = (capacity - 1) & hash`：规定 capacity 是 2 的幂，那么 capacity - 1 的低位就全是 1，高位就全是 0，直接与 hash 值进行与运算，得到的值就是槽位号

> 比如 32 =  0...0100000，那么 32 - 1 = 0...011111，与任何数做与运算的值都可以映射在 00000 到 11111 之间

##### 哈希计算

根据上面的分析，可以发现**计算槽位的时候实际只用到了 hash 的低位信息**，因此为了尽可能地避免哈希冲突，不能只用单纯的 hashCode，还需要把高位的信息也融合进低位

1. `h = key.hashCode()`：这个方法是在顶层 Object 类里定义的本地方法，由 JVM 的 C/C++ 代码实现，会计算返回一个 32 位 int 整数
2. `h' = h >>> 16`：把高 16 位移动到低 16 位的位置
3. `hash = h ^ h'`：高 16 位保持不变，但是低 16 位会被扰动

##### 迁移计算

观察源码可以发现，**每次扩容都是原来的两倍，并且不支持自定义**，这是因为要保持容量是 2 的幂这个特性，把上面两个公式结合 `index = (capacity - 1) & (hashCode ^ (hashCode >>> 16))`，可以发现与运算的右操作数不会改变的，而与运算的左操作数的下一个高位从 0 变为 1，所以**与操作的结果只有一位可能会改变，而改变与否的依据则是 hash & oldCap 是否等于 0**，因此**要么 newIndex = oldIndex，要么 newIndex = oldIndex + oldCap**

> oldCap = 16 = 00010000，16 - 1 = 00001111
>
> newCap = 32 = 00100000，32 - 1 = 00011111
>
> 对于 hash = 7 = 00000111
>
> ​	是否改变：00010000 & 00000111 = 00000000 == 0 -> false
>
> ​	扩容前 index = 00001111 & 00000111 = 7
>
> ​	扩容后 index = 00001111 & 00010111 = 7
>
> 对于 hash = 22 = 00010110
>
> ​	是否改变：00010000 & 00010110 = 00010000 != 0 -> true
>
> ​	扩容前 index = 00001111 & 00010110 = 6
>
> ​	扩容后 index = 00001111 & 00010110 = 22 = 6 + 16

#### 源码分析

##### 字段

```java
// 默认初始容量是 16
static final int DEFAULT_INITIAL_CAPACITY = 1 << 4;

// 最大容量是 10 亿
static final int MAXIMUM_CAPACITY = 1 << 30;

// 桶大小触发树化/扩容的阈值
static final int TREEIFY_THRESHOLD = 8;

// 容量触发树化的阈值
static final int MIN_TREEIFY_CAPACITY = 64;

// 反树化阈值
static final int UNTREEIFY_THRESHOLD = 6;

// 默认的负载因子
static final float DEFAULT_LOAD_FACTOR = 0.75f;

// 负载因子，用于控制装填密度
final float loadFactor;

// 扩容的阈值 = 容量 × 负载因子
int threshold;

// 实际存储的键值对数量
transient int size;

// 结构性修改的次数
transient int modCount;
```

##### hash

```java
static final int hash(Object key) {
    int h;
    return (key == null) ? 0 : (h = key.hashCode()) ^ (h >>> 16);
}
```

##### putVal

```java
final V putVal(int hash, K key, V value, boolean onlyIfAbsent, boolean evict) {
    Node<K,V>[] tab; Node<K,V> p; int n, i;
    
    // 1. 如果 table 为空则初始化
    if ((tab = table) == null || (n = tab.length) == 0)
        n = (tab = resize()).length;
    
    // 2. 定位桶索引，如果该位置为空，直接插入新节点
    if ((p = tab[i = (n - 1) & hash]) == null)
        tab[i] = newNode(hash, key, value, null);
    
    else {
        Node<K,V> e; K k;
        // 3. 桶中已有节点，判断是否为同一个 key
        if (p.hash == hash && ((k = p.key) == key || (key != null && key.equals(k))))
            e = p;
        
        // 4. 如果是红黑树节点，走红黑树的 putTreeVal
        else if (p instanceof TreeNode)
            e = ((TreeNode<K,V>)p).putTreeVal(this, tab, hash, key, value);
        
        // 5. 否则走链表的尾插法
        else {
            for (int binCount = 0; ; ++binCount) {
                if ((e = p.next) == null) {
                    p.next = newNode(hash, key, value, null);
                    // 如果链表长度达到阈值，树化
                    if (binCount >= TREEIFY_THRESHOLD - 1)
                        treeifyBin(tab, hash);
                    break;
                }
                if (e.hash == hash && ((k = e.key) == key || (key != null && key.equals(k))))
                    break;
                p = e;
            }
        }
        
        // 6. 如果找到了已有节点 e，覆盖其 value（不属于结构性变化）
        if (e != null) {
            V oldValue = e.value;
            if (!onlyIfAbsent || oldValue == null)
                e.value = value;
            return oldValue;
        }
    }
    
    // 7. modCount+1，元素数量+1
    ++modCount;
    if (++size > threshold)
        resize();   // 扩容
    return null;
}
```

##### getNode

```java
final Node<K,V> getNode(int hash, Object key) {
    Node<K,V>[] tab; Node<K,V> first, e; int n; K k;
    
    // 1. table 不为空且容量大于 0，定位桶索引，并取出桶的第一个节点
    if ((tab = table) != null && (n = tab.length) > 0 && (first = tab[(n - 1) & hash]) != null) {
        
        // 2. 检查桶的第一个节点
        if (first.hash == hash && ((k = first.key) == key || (key != null && key.equals(k))))
            return first;
        
        // 3. 如果桶里不止一个节点（链表/红黑树）
        if ((e = first.next) != null) {
            // 3.1 红黑树：调用树的查找逻辑
            if (first instanceof TreeNode)
                return ((TreeNode<K,V>)first).getTreeNode(hash, key);
            // 3.2 链表：遍历查找
            do {
                if (e.hash == hash &&
                    ((k = e.key) == key || (key != null && key.equals(k))))
                    return e;
            } while ((e = e.next) != null);
        }
    }
    return null;
}
```

##### resize 方法



```java
final Node<K,V>[] resize() {
    Node<K,V>[] oldTab = table;             // 原数组
    int oldCap = (oldTab == null) ? 0 : oldTab.length;
    int oldThr = threshold;                 // 扩容阈值
    int newCap, newThr = 0;

    // 1. 计算新容量
  	
  	// 1.1 如果已有容量
    if (oldCap > 0) {
      	// 到达最大不能扩容
        if (oldCap >= MAXIMUM_CAPACITY) {
            threshold = Integer.MAX_VALUE;
            return oldTab;
        }
      	// 超过初始容量则阈值翻倍
        else if ((newCap = oldCap << 1) < MAXIMUM_CAPACITY &&
                 oldCap >= DEFAULT_INITIAL_CAPACITY)
            newThr = oldThr << 1;
    }
    // 1.2 如果在构造函数中指定了的初始容量大小（暂存到 threshold 中）
    else if (oldThr > 0)
        newCap = oldThr;
  	// 1.3 如果构造函数没有指定，使用默认值
    else {
        newCap = DEFAULT_INITIAL_CAPACITY;
        newThr = (int)(DEFAULT_LOAD_FACTOR * DEFAULT_INITIAL_CAPACITY);
    }

  	// 2. 计算新阈值
    if (newThr == 0) {
        float ft = (float)newCap * loadFactor;
        newThr = (newCap < MAXIMUM_CAPACITY && ft < (float)MAXIMUM_CAPACITY ? (int)ft : Integer.MAX_VALUE);
    }
    threshold = newThr;

    // 3. 创建新数组
    @SuppressWarnings({"rawtypes","unchecked"})
    Node<K,V>[] newTab = (Node<K,V>[])new Node[newCap];
    table = newTab;

    // 4. 把老数组数据迁移到新数组
    if (oldTab != null) {
        for (int j = 0; j < oldCap; ++j) {
            Node<K,V> e;
            if ((e = oldTab[j]) != null) {
                oldTab[j] = null;
              	// 4.1 只有一个节点
                if (e.next == null)
                    newTab[e.hash & (newCap - 1)] = e;
              	// 4.2 红黑树节点
                else if (e instanceof TreeNode)
                    ((TreeNode<K,V>)e).split(this, newTab, j, oldCap);
	              // 4.3 链表节点
                else {
                    Node<K,V> loHead = null, loTail = null;
                    Node<K,V> hiHead = null, hiTail = null;
                    Node<K,V> next;
                    do {
                        next = e.next;
                        if ((e.hash & oldCap) == 0) {
                            if (loTail == null)
                                loHead = e;
                            else
                                loTail.next = e;
                            loTail = e;
                        } else {
                            if (hiTail == null)
                                hiHead = e;
                            else
                                hiTail.next = e;
                            hiTail = e;
                        }
                    } while ((e = next) != null);
                    if (loTail != null) {
                        loTail.next = null;
                        newTab[j] = loHead;
                    }
                    if (hiTail != null) {
                        hiTail.next = null;
                        newTab[j + oldCap] = hiHead;
                    }
                }
            }
        }
    }
    return newTab;
}
```

### ConcurrentHashMap

#### 线程安全原理

Hashtable 是早期实现并发安全的一个手段，它通过**在所有关键方法上加 synchronized 关键字**来保证线程安全，这样只要一个线程执行了这些方法，其他线程必须等待，因此 Hashtable 相当于是**方法级别的锁**，即使两个线程操作不同的 bucket，也会互斥等待，大大降低了并发性能 

相比之下，ConcurrentHashMap 通过以下机制保障了线程安全

- **使用 Unsafe 和 CAS**：提供了原子的获取值和更新值操作
- **对 table 加上 volatile 关键字**：保证了任何线程都 table 的修改都可以被其他线程立马看到
- **对 bucket 的头节点/根节点使用 synchronized**：桶级别的锁，不会干扰线程对其他桶的操作
- 提供了 **putIfAbsent、computeIfAbsent、computeIfPresent** 等原子性的复合操作

#### 协助迁移

1. 当 size > threshold 时会触发扩容，线程会先创建一个 nextTable，容量为 table 的 2 倍
2. 共享变量 transferIndex 保存了还未搬迁的最大下标，线程会从 transferIndex 里领取一个区间，然后负责该区间的桶迁移
3. 线程会把负责区间的桶的头节点的 hash 设置为 MOVED(-1)
4. 线程遍历桶内的链表或红黑树，根据规则将节点重新分配到 nextTable 中
5. 此时如果别的线程获取到时间片，并且发现桶的头节点是 MOVED，它会调用 helpTransfer() 方法，领取新的区间，继续迁移
6. 当一个桶迁移完成，会放置一个 ForwardingNode 占位，内部持有 nextTable 的引用，之后访问该桶的线程，会暂时去 nextTable 查找
7. 当所有区间迁移完毕，会清空原先的 table，并把 nextTable 赋值给 table

#### 源码分析

##### tabAt / casTabAt / setTabAt

ConcurrentHashMap 具有一个静态 Unsafe 对象，底层封装了 CPU 的原子指令，通过**本地方法 getReferenceAcquire、putReferenceRelease 和 compareAndSetReference 实现获取、插入和更新键值对**

在 tabAt / casTabAt / setTabAt 中传入的只是槽位的编号，而 Unsafe 方法需要传入槽位的内存偏移量，因此首先需要得到每个 Node 的大小 scale

- 传统：`address = base + index * scale`
- 改进：address `= base + index << shift`，这是因为 scale 是 2 的幂，**乘法运算可以直接变为左移位运算**，而 shift 就是 scale 中 1 后面 0 的个数，也就是 31 减去前导 0 的个数

> 比如 2^5 = 32 = 0...0100000，1 后面有 几个 0 就是 2 的几次幂

```java
private static final Unsafe U = Unsafe.getUnsafe();
private static final int ABASE = U.arrayBaseOffset(Node[].class);
private static final int ASHIFT;

static {
    int scale = U.arrayIndexScale(Node[].class);
    if ((scale & (scale - 1)) != 0)
        throw new ExceptionInInitializerError("array index scale not a power of two");
    ASHIFT = 31 - Integer.numberOfLeadingZeros(scale);

    // Reduce the risk of rare disastrous classloading in first call to
    // LockSupport.park: https://bugs.openjdk.java.net/browse/JDK-8074773
    Class<?> ensureLoaded = LockSupport.class;

    // Eager class load observed to help JIT during startup
    ensureLoaded = ReservationNode.class;
}

static final <K,V> Node<K,V> tabAt(Node<K,V>[] tab, int i) {
    return (Node<K,V>)U.getReferenceAcquire(tab, ((long)i << ASHIFT) + ABASE);
}

static final <K,V> boolean casTabAt(Node<K,V>[] tab, int i, Node<K,V> c, Node<K,V> v) {
    return U.compareAndSetReference(tab, ((long)i << ASHIFT) + ABASE, c, v);
}

static final <K,V> void setTabAt(Node<K,V>[] tab, int i, Node<K,V> v) {
    U.putReferenceRelease(tab, ((long)i << ASHIFT) + ABASE, v);
}
```

##### putVal

```java
final V putVal(K key, V value, boolean onlyIfAbsent) {
    // ConcurrentHashMap 不允许 key 或 value 为 null
    if (key == null || value == null) throw new NullPointerException();
  
  	// 计算哈希值
    int hash = spread(key.hashCode());
  
  	// 无限循环实现自旋
    int binCount = 0;
    for (Node<K,V>[] tab = table;;) {
        Node<K,V> f; int n, i, fh;
      	// 初始化 table
        if (tab == null || (n = tab.length) == 0)
            tab = initTable();
      	// 如果桶为空，则直接 CAS
        else if ((f = tabAt(tab, i = (n - 1) & hash)) == null) {
            if (casTabAt(tab, i, null, new Node<K,V>(hash, key, value, null)))
                break;
        }
      	// 如果桶正在扩容，则协助扩容
        else if ((fh = f.hash) == MOVED)
            tab = helpTransfer(tab, f);
      	// 如果桶此前有值
        else {
            V oldVal = null;
            // 使用 synchronized 锁住当前桶的头节点/根节点
            synchronized (f) {
                if (tabAt(tab, i) == f) {
                    // 链表
                    if (fh >= 0) {
                        binCount = 1;
                      	// 尾插法
                        for (Node<K,V> e = f;; ++binCount) {
                            K ek;
                          	// 存在键
                            if (e.hash == hash &&
                                ((ek = e.key) == key ||
                                 (ek != null && key.equals(ek)))) {
                                oldVal = e.val;
                              	// 保持旧值
                                if (!onlyIfAbsent)
                                    e.val = value;
                                break;
                            }
                            Node<K,V> pred = e;
                          	// 不存在键
                            if ((e = e.next) == null) {
                                pred.next = new Node<K,V>(hash, key, value, null);
                                break;
                            }
                        }
                    }
                  	// 红黑树
                    else if (f instanceof TreeBin) {
                        Node<K,V> p;
                        binCount = 2;
                        if ((p = ((TreeBin<K,V>)f).putTreeVal(hash, key, value)) != null) {
                            oldVal = p.val;
                            if (!onlyIfAbsent)
                                p.val = value;
                        }
                    }
                }
            }
            if (binCount != 0) {
                if (binCount >= TREEIFY_THRESHOLD)
                    treeifyBin(tab, i);
                if (oldVal != null)
                    return oldVal;
              	// 跳出自旋
                break;
            }
        }
    }
    addCount(1L, binCount);
    return null;
}
```

##### get

```java
public V get(Object key) {
    Node<K,V>[] tab; Node<K,V> e, p; int n, eh; K ek;
  	// 计算哈希值
    int h = spread(key.hashCode());
  
  	// 槽位有元素
    if ((tab = table) != null && (n = tab.length) > 0 &&
        (e = tabAt(tab, (n - 1) & h)) != null) {
        // 如果头节点就是目标，则直接返回值
        if ((eh = e.hash) == h) {
            if ((ek = e.key) == key || (ek != null && key.equals(ek)))
                return e.val;
        }
      	// 如果头节点 hash < 0，说明正在扩容或者是红黑树，find 查找
        else if (eh < 0)
            return (p = e.find(h, key)) != null ? p.val : null;
      	// 如果头节点 hash >= 0，说明是链表，遍历查找
        while ((e = e.next) != null) {
            if (e.hash == h &&
                ((ek = e.key) == key || (ek != null && key.equals(ek))))
                return e.val;
        }
    }
  	// 槽位无元素
    return null;
}
```



## 使用规范

### 集合判空

使用 isEmpty() 方法，而不是 size()==0 的方式，并且需要避免 NPE

```java
if (list == null || list.isEmpty()) { ... }
```

### 集合去重

利用 Set 的唯一性，而不是循环判断添加

```java
List<Integer> distinctList = new ArrayList<>(new LinkedHashSet<>(list));
```

### 集合转 Map

必须传入 mergeFunction 来处理 key 冲突

```java
Map<Integer, String> map = list.stream()
    .collect(Collectors.toMap(
        n -> n,                 // key
        n -> "val" + n,         // value
        (v1, v2) -> v1)					// 保留前者
    );
```

### 集合转数组

使用集合的 toArray 方法，传入类型一致，长度为 0 的数组

```java
String[] array = list.toArray(new String[0]);
```

### 数组转集合

使用 Arrays.asList() 返回是  java.util.Arrays.ArrayList，是一个长度固定的数组，不允许 add、remove 和 clear，在底层是直接引用了传入的数组，set 会影响原始数组

```java
List list = Arrays.asList(array);
```

使用 ArrayList 的有参构造函数

```java
List<Integer> list = new ArrayList<>(Arrays.asList(array));
```

使用  Java8 提供的 Arrays.stream()，收集得到的是 ArrayList 类型

```java
List<Integer> list = Arrays.stream(array).collect(Collectors.toList());
```

使用 Java9 提供的 List.of() 返回的是 java.util.ImmutableCollections.ListN，是一个不可变数组，不允许 add、remove、clear 和 set

```java
List<Integer> list = List.of(array);
```