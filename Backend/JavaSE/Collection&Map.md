## Collection & Map



## 定义

### 数组与集合

| 维度     | 数组(Array)          | 集合(Collection)       |
| -------- | -------------------- | ---------------------- |
| 存储长度 | 固定                 | 可变                   |
| 存储类型 | 只能存同一类型       | 可以存不同类型         |
| 存储内容 | 基本类型或对象       | 只能存对象             |
| 下标访问 | 支持                 | 部分支持直接下标访问   |
| 增删元素 | 不支持               | 支持                   |
| 常见实现 | int[], String[]      | List、Set、Map         |
| 使用场景 | 数据量固定、访问频繁 | 数据动态变化、增删频繁 |

### 框架体系

- Collection：存放单值
    - List：有序、可重复元素
        - ArrayList：动态数组，查询快，增删慢
        - LinkedList：双向链表，查询慢，增删快
    - Set：无序、不重复元素
        - HashSet：基于哈希表，查询快
        - LinkedHashSet：有插入顺序的 HashSet
        - TreeSet：基于红黑树，元素自动排序（必须实现 Comparable 或传 Comparator）
    - Queue：有序、可重复元素，先进先出
        - PriorityQueue：优先队列，元素有优先级
        - ArrayDeque：双端队列，可替代 Stack 和 Queue
- Map：存放键值对
    - HashMap：无序
    - LinkedHashMap：有插入顺序的 HashMap
    - TreeMap：自动按键排序（基于红黑树）
    - ConcurrentHashMap：线程安全，适合并发场景

### 业务选择

| 业务特点                 | 优先选择集合                                    | 理由                            |
| ------------------------ | ----------------------------------------------- | ------------------------------- |
| 需要快速查找、插入、删除 | HashMap、HashSet                                | 基于哈希表，时间复杂度接近O(1)  |
| 需要元素有序             | LinkedHashMap、LinkedHashSet、ArrayList         | 保留插入顺序，遍历顺序稳定      |
| 需要排序                 | TreeMap、TreeSet                                | 基于红黑树，自动按key或元素排序 |
| 需要频繁插入/删除        | LinkedList                                      | 链表结构，插入删除效率高        |
| 需要频繁随机访问         | ArrayList                                       | 底层数组，按索引访问快          |
| 要求线程安全             | ConcurrentHashMap、Collections.synchronizedList | 支持并发读写或同步操作          |
| 键值对存储               | Map相关（HashMap、TreeMap）                     | 专门用于键值对映射              |
| 允许重复元素             | ArrayList、LinkedList                           | List 允许重复                   |
| 不允许重复元素           | HashSet、TreeSet                                | Set 自动去重                    |
| 先进先出队列结构         | Queue、LinkedList、ArrayDeque                   | 用于队列或缓冲场景              |



## Collection

### 接口方法

- boolean add(E e)：添加元素到集合中
- boolean addAll(Collection<? extends E> c)：把另一个集合的所有元素加入当前集合
- boolean remove(Object o)：移除指定元素（按 equals 匹配）
- boolean removeAll(Collection<?> c)：移除与参数集合中相同的所有元素
- void clear()：清空集合中所有元素
- boolean contains(Object o)：判断集合中是否包含指定元素
- boolean containsAll(Collection<?> c)：判断是否包含参数集合的全部元素
- int size()：返回集合中元素数量
- boolean isEmpty()：判断集合是否为空
- Iterator<E> iterator()：返回迭代器，用于遍历
- Object[] toArray() / <T> T[] toArray(T[] a)：转为 Object[] 数组
- boolean retainAll(Collection<?> c)：保留参数集合中也存在的元素（求交集）
- boolean equals(Object o)：判断两个集合是否相等（元素完全一致）
- int hashCode()：返回集合的哈希码（重写 equals 必须重写它）

### 遍历手段

Iterator

- hasNext()：是否还有下一个元素
- next()：返回下一个元素，并跳转到下一个元素的位置
- remove()：删除当前元素
- 迭代器一开始指向的是集合开头之前的位置，而不是第一个元素的位置！
- 如果想要从头遍历，需要再次利用 iterator() 重置迭代器
- Iterator 只有 hasNext()，也就是说它是单向的，只能单调往前，不能倒退

```java
Iterator<String> it = list.iterator();
while (it.hasNext()) {
    String element = it.next();
    System.out.println(element);
}
```

for-each

- 不能在 for-each 里面删除元素
- for-each 也可以在数组上使用
- for-each 在底层仍然是迭代器

```java
for (String element : list) {
    System.out.println(element);
}
```

### List 方法

- E get(int index)：获取指定位置元素
- E set(int index, E element)：设置指定位置元素
- void add(int index, E element)：在指定位置插入元素
- E remove(int index)：按索引删除元素
- int indexOf(Object o)：返回第一次出现的位置，找不到返回 -1
- int lastIndexOf(Object o)：返回最后一次出现的位置，找不到返回 -1
- ListIterator<E> listIterator() / listIterator(int index)：获取 ListIterator，用于双向遍历
- List<E> subList(int fromIndex, int toIndex)：获取子列表（from 包含，to 不含）

###  HashSet 底层

- HashSet 本质上就是一个没有值的 HashMap，add 的元素都被当作 key，值是固定占位符
- 插入顺序不保证、查询速度飞快、允许存 null，但也只有一个
- 可以重写 hashCode 自定义哈希逻辑
- 不允许重复元素，核心在于 hashCode() + equals()
    1. 先调用 obj.hashCode()，算出哈希值，定位数组槽
    2. 如果这个位置没人 → 放进去
    3. 如果有冲突，会遍历数组槽对于链表里的对象
    4. 调用 equals() 判断是否“等于已有对象”
    5. 如果存在 equals 返回 true → 视为重复，不加
    6. 如果全部 equals 返回 false → 加入桶链尾部
    7. 如果链表超过最大阈值，那么链表会自动进化为树





## Map

### 接口方法

- V put(K key, V value)：将指定的键值对放入 Map 中（若键已存在会覆盖原值）
- void putAll(Map<? extends K, ? extends V> m)：将另一个 Map 中的所有键值对添加进来
- V get(Object key)：根据键获取对应的值，找不到返回 null
- V remove(Object key)：根据键移除对应的键值对
- boolean containsKey(Object key)：判断是否包含指定键
- boolean containsValue(Object value)：判断是否包含指定值
- int size()：返回 Map 中的键值对数量
- boolean isEmpty()：判断是否为空
- void clear()：清空所有键值对
- Set<K> keySet()：返回所有键的 Set 视图
- Collection<V> values()：返回所有值的 Collection 视图
- Set<Map.Entry<K, V>> entrySet()：返回所有键值对的 Set 视图（Map.Entry 是内部接口）
- boolean equals(Object o)：判断两个 Map 是否相等（键值完全相同）
- int hashCode()：返回 Map 的哈希码
- V getOrDefault(Object key, V defaultValue)：获取 key 对应的值，若不存在则返回默认值
- V putIfAbsent(K key, V value)：仅当 key 不存在时添加
- V replace(K key, V value)：仅当 key 存在时替换对应值
- boolean replace(K key, V oldValue, V newValue)：只有旧值匹配时才替换为新值
- void forEach(BiConsumer<? super K, ? super V> action)：对每个键值对执行操作

### 实现类对比

| 类名              | 是否线程安全 | 是否允许null键/值         | 是否有序       | 是否自动排序 | 底层结构         | 适用场景                  |
| ----------------- | ------------ | ------------------------- | -------------- | ------------ | ---------------- | ------------------------- |
| HashMap           | 否           | 允许1个null键，多个null值 | 否             | 否           | 数组+链表/红黑树 | 最常用的Map，快速查找插入 |
| LinkedHashMap     | 否           | 允许                      | 是（插入顺序） | 否           | HashMap+双向链表 | 保持插入顺序，遍历稳定    |
| TreeMap           | 否           | 键不能为null，值可为null  | 是（升序）     | 是（按key）  | 红黑树           | 需要有序的Map             |
| Hashtable         | 是           | 不允许                    | 否             | 否           | 哈希表（早期）   | 老代码遗留，不推荐        |
| ConcurrentHashMap | 是           | 不允许                    | 否             | 否           | 分段哈希+红黑树  | 并发安全场景推荐使用      |

### 遍历手段

Entry

- Map 里的所有元素，本质上就是一组 Entry 对象
- Entry 是一个 Set，因此可以利用 for-each 遍历
- 通过 getKet 和 getValue 可以获得当前元素的键值对

```java
for (Map.Entry<String, Integer> entry : map.entrySet()) {
    System.out.println(entry.getKey() + " = " + entry.getValue());
}
```

也可以单独遍历键和值

```java
for (String key : map.keySet()) {
    System.out.println(key + " = " + map.get(key));
}

for (Integer value : map.values()) {
    System.out.println(value);
}
```

### Properties

Properties 是 Java 提供的一个用于配置加载的类，继承自 Hashtable，线程安全

- String getProperty(String key)：根据键获取属性值
- String getProperty(String key, String defaultValue)：获取属性值，如果没有则返回默认值
- Object setProperty(String key, String value)：设置属性值（键值都为字符串）
- void load(InputStream inStream)：从字节输入流中加载 .properties 配置文件
- void load(Reader reader)：从字符输入流中加载 .properties 配置文件
- void store(OutputStream out, String comments)：将配置信息写入到文件（字节流）
- void store(Writer writer, String comments)：将配置信息写入到文件（字符流）
- Set<String> stringPropertyNames()：获取所有的键（只返回字符串键）
- Enumeration<?> propertyNames()：获取所有属性名（兼容旧写法）
- void list(PrintStream out)：将属性列表打印到输出流
- void list(PrintWriter out)：将属性列表打印到字符输出流
