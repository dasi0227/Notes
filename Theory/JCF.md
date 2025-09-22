# Collection



![918bdc2b0fd7be877965381ac34bbec0](https://dasi-blog.oss-cn-guangzhou.aliyuncs.com/Java/202509221449411.png)



## 前置知识

### 迭代器



### 比较器

比较器是**用来比较两个相同类的对象“谁先谁后”，不能简单理解为“谁大谁小”**，因为排序规则完全可以不依赖于数值，而是任何自定义逻辑

| 接口               | 方法                     | 实现   | 数量         | 场景                                       |
| ------------------ | ------------------------ | ------ | ------------ | ------------------------------------------ |
| **Comparable\<T>** | int compareTo(T o);      | 当前类 | 只能实现一个 | 让一个类自己具备比较内部元素的能力         |
| **Comparator\<T>** | int compare(T o1, T o2); | 外部类 | 可以实现多个 | 让一个类使用外部定义的比较器来比较内部元素 |

**Java 的所有包装类（Integer、Double、Long、Float、Short、Byte、Character、Boolean）都已经实现了Comparable\<T> 接口**，因此它们自带 compareTo(T other) 方法

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

### fail-fast

由于部分集合框架是不支持线程安全的，因此为了能够提前发现并发操作导致线程安全风险，底层会维护一个 modCount 来记录修改的次数

1. 当调用 **iterator()** 创建迭代器时，会把 modCount 的当前值保存到 expectedModCoun
2. 在迭代过程中都会检查 **expectedModCount == modCount**
3. 如果不一致说明集合在迭代期间被**结构性修改**，立刻抛出 **ConcurrentModificationException** 异常



## List

### 定义

**List 存储一个元素数组，强调连续性，可以通过索引访问元素，也可以放入重复元素，典型操作有：get、add、remove**

### ArrayList

#### 定义

**Array 是 Java 的一种基础数据结构，不是一个类**，用来存放固定长度、相同类型的数组，插入和删除需要手动移动元素，通过 `Type[] array = new Type[length]` 创建。

因此为了提供更方便的数组使用，Java 在集合框架提供了 ArrayList 类

- 根据实际存储的元素**动态地扩容**，创建时允许不指定容量，默认容量为 10，每次扩容 1.5 倍
- 只能**存储对象**，如果是基本数据类型需要**包装类**，同时允许使用**泛型**来确保类型安全
- **线程不安全**，多线程同时对同一个 ArrayList 对象操作可能会导致数据不一致
- ArrayList **在底层维护了一个 Array 数组 `Object[] elementData`** 表示存放的元素和一个整型 `int size` 表示存放元素的个数

#### 构造函数

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

#### 扩容机制 

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

### LinkedList

#### 定义

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

#### 区别

| **特性**          | ArrayList              | LinkedList                       |
| ----------------- | ---------------------- | -------------------------------- |
| **底层结构**      | Object[] elementData   | Node{prev,item,next}             |
| **随机访问效率**  | O(1)，直接通过下标访问 | O(n)，必须遍历链表               |
| **插入/删除效率** | O(n)，需要移动大量元素 | O(1)，只需修改前后指针           |
| **空间占用**      | 紧凑存储               | 分散存储，多了 next 和 prev 引用 |
| **线程安全性**    | 非线程安全             | 非线程安全                       |
| **适用场景**      | 读多写少，频繁随机访问 | 写多读少，频繁插入删除           |

#### 链接机制

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



## Set

### 定义

**Set 存储一个元素集合，强调唯一性和无序性，不能通过索引访问元素，不允许放入重复元素，典型操作有：contains、add、remove**

### 实现类

| **特性**          | **HashSet**            | **LinkedHashSet**      | **TreeSet**              |
| ----------------- | ---------------------- | ---------------------- | ------------------------ |
| **底层结构**      | HashMap                | LinkedHashMap          | TreeMap                  |
| **元素顺序**      | 无序                   | 有序                   | 有序                     |
| **允许 null**     | 允许 1 个 null 元素    | 允许 1 个 null 元素    | 不允许 null              |
| **查找/插入效率** | O(1)                   | O(1)                   | O(log n)                 |
| **去重依据**      | hashCode() + equals()  | hashCode() + equals()  | Comparable / Comparator  |
| **适用场景**      | 只关心去重，不关心顺序 | 需要去重且保持插入顺序 | 需要去重且保持自定义顺序 |



## Queue

### 定义

**Queue 存储一个元素序列，强调有序性和首尾操作，不能通过索引访问元素，但允许放入重复元素，典型操作有 offer、poll、peek、remove、element**

### 实现类

| **实现类**            | **底层结构**    | **线程安全** | **是否有界** | 出队顺序 |
| --------------------- | --------------- | ------------ | ------------ | -------- |
| LinkedList            | 双向链表        | ❌            | ❌            | 插入     |
| ArrayDeque            | 循环数组        | ❌            | ❌            | 插入     |
| PriorityQueue         | 二叉堆          | ❌            | ❌            | 比较     |
| ConcurrentLinkedQueue | 单向链表 + CAS  | ✅            | ❌            | 插入     |
| LinkedBlockingQueue   | 双向链表 + 双锁 | ✅            | ✅            | 插入     |
| ArrayBlockingQueue    | 数组 + 单锁     | ✅            | ✅            | 插入     |
| PriorityBlockingQueue | 二叉堆 + 单锁   | ✅            | ❌            | 比较     |

### 阻塞队列

BlockingQueue 继承自 Queue，是 JUC 提供的接口，内部通过锁或 CAS 保证线程安全，主要拓展了：

- 插入 put：当队列满时，阻塞直到有空位
- 移除 take：当队列空时，阻塞直到有新元素
- 超时机制：允许 offer 和 poll 设置 timeout

阻塞队列最常用的就是生产者-消费者模型，这里主要分析 ArrayBlockingQueue

- 构造函数

  ```java
  // capacity 表示队列初始容量，fair 表示 锁的公平性
  public ArrayBlockingQueue(int capacity, boolean fair) {
    //如果设置的队列大小小于0，则直接抛出IllegalArgumentException
    if (capacity <= 0)
        throw new IllegalArgumentException();
    //初始化一个数组用于存放队列的元素
    this.items = new Object[capacity];
    //创建阻塞队列流程控制的锁
    lock = new ReentrantLock(fair);
    //用lock锁创建两个条件控制队列生产和消费
    notEmpty = lock.newCondition();
    notFull =  lock.newCondition();
  }
  ```





































































# Map





