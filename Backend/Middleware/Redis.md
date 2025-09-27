# Redis



   * [概述](#概述)
      * [定义](#定义)
      * [使用流程](#使用流程)
      * [基本命令](#基本命令)
   * [数据类型](#数据类型)
      * [String](#string)
      * [List](#list)
      * [Hash](#hash)
      * [Set](#set)
      * [ZSet](#zset)
      * [BitMap](#bitmap)
      * [HyperLogLog](#hyperloglog)
      * [GEO](#geo)
      * [Stream](#stream)
   * [持久化 Persistence](#持久化-persistence)
      * [意义](#意义)
      * [RDB](#rdb)
      * [AOF](#aof)
      * [修复文件](#修复文件)
   * [事务 Transaction](#事务-transaction)
      * [定义](#定义)
      * [命令](#命令)
      * [错误处理](#错误处理)
   * [管道 Pipeline](#管道-pipeline)
      * [Redis 通信服务](#redis-通信服务)
      * [定义](#定义)
      * [批量执行区分](#批量执行区分)
   * [复制 Replication](#复制-replication)
      * [定义](#定义)
      * [节点信息](#节点信息)
      * [命令](#命令)
      * [工作流程](#工作流程)
      * [缺陷](#缺陷)
   * [哨兵 Sentinel](#哨兵-sentinel)
      * [定义](#定义)
      * [配置](#配置)
      * [实践](#实践)
      * [原理](#原理)
      * [缺陷](#缺陷)
   * [集群 Cluster](#集群-cluster)
      * [定义](#定义)
      * [优势](#优势)
      * [哈希分区策略](#哈希分区策略)
      * [Gossip 协议](#gossip-协议)
      * [配置](#配置)
      * [命令](#命令)
         * [命令行工具](#命令行工具)
         * [集群管理](#集群管理)
         * [节点管理](#节点管理)
         * [槽管理](#槽管理)
   * [SpringBoot 集成](#springboot-集成)
      * [RedisTemplate](#redistemplate)
      * [序列化问题](#序列化问题)
      * [配置](#配置)
   * [BigKey](#bigkey)
      * [概念](#概念)
      * [SCAN](#scan)
      * [发现](#发现)
      * [处理](#处理)
   * [双写一致性](#双写一致性)
      * [策略](#策略)
      * [Canal](#canal)
   * [高级数据结构实践](#高级数据结构实践)
      * [统计类型](#统计类型)
      * [HyperLogLog](#hyperloglog)
      * [BitMap](#bitmap)
      * [Geo](#geo)
      * [Bloom Filter](#bloom-filter)
   * [Lua](#lua)
      * [定义](#定义)
      * [语法](#语法)
      * [使用](#使用)
   * [分布式锁](#分布式锁)
      * [定义](#定义)
      * [测试框架](#测试框架)
      * [本地锁](#本地锁)
      * [Redis 简易锁](#redis-简易锁)
      * [Redis 进阶锁](#redis-进阶锁)
      * [RedLock](#redlock)
      * [Redisson](#redisson)
   * [三大问题与三大方案](#三大问题与三大方案)
      * [穿透 Penetration](#穿透-penetration)
      * [击穿 Breakdown](#击穿-breakdown)
      * [雪崩 Avalanche](#雪崩-avalanche)
      * [限流 Rate Limiting](#限流-rate-limiting)
      * [熔断 Circuit Breaker](#熔断-circuit-breaker)
      * [降级 Degrade](#降级-degrade)
   * [过期策略](#过期策略)
      * [内存](#内存)
      * [删除策略](#删除策略)
      * [淘汰策略](#淘汰策略)
   * [Redis 为什么这么快](#redis-为什么这么快)
      * [1. 内存 + 数据结构](#1-内存-数据结构)
      * [2. 单线程](#2-单线程)
      * [3. I/O 多路复用](#3-io-多路复用)
         * [定义与瓶颈](#定义与瓶颈)
         * [Unix 的 I/O 模型](#unix-的-io-模型)
         * [epoll](#epoll)



## 概述

### 定义

Redis（Remote Dictionary Server）是一个开源的内存数据结构存储系统，是一种基于 key-value 类型的数据库，常用于缓存、分布式锁、消息队列和排行榜等，由 **Antirez** 在 2009 年开发，核心特点为：

- **内存存储**：速度极快，不用读写磁盘，每秒可以处理十万次读写
- **丰富数据类型**：字符串（String）、列表（List）、集合（Set）、有序集合（ZSet）、哈希（Hash）、基数统计（HyperLogLog）、地理空间（GEO）、位图（BitMap）、流（Stream）
- **持久化**：利用 RDB 提供快照，利用 AOF 追加写日志
- **高可用**：提供主从复制和哨兵模式
- **分布式**：提供分片集群

### 使用流程

1. 下载：默认位置在 /usr/local/bin（相当于 Windows C 盘下的 ProgramFiles）

    - **redis-cli**：客户端

    - **redis-server**：服务端

    - **redis-benchmark**：压力测试工具

    - **redis-sentinel**：集群功能，高可用哨兵进程

    - **redis-check-rdb**：RDB 文件检查/修复工具

    - **redis-check-aof**：AOF 文件检查/修复工具
2. 配置：拷贝 redis.conf 到 etc/redis/ 下

    - `daemonize = true`：以守护进程方式运行，即可以在后台运行

    - `protected-mode no`：关闭保护模式，接受远程连接

    - `bind 0.0.0.0`：监听所有网卡

    - `requirepass xxxxx`：设置密码
3. 启动：`redis-server /etc/redis/redis.conf`
4. 登录：`redis-cli -a xxxx`
5. 测试：`ping`（回复 PONG）
6. 关闭：`shutdown`
7. 断开：`quit`

### 基本命令

【数据库与服务器】

| 命令               | 功能                                  | 返回值                                  |
| ------------------ | ------------------------------------- | --------------------------------------- |
| **dbsize**         | 获取当前数据库中 key 的数量           | key 数量                                |
| **flushdb**        | 删除当前数据库的所有 key              | "OK"                                    |
| **flushall**       | 删除所有数据库的所有 key              | "OK"                                    |
| **time**           | 返回当前服务器时间                    | UNIX 时间戳和微秒数                     |
| **info**           | 获取 Redis 服务器的各种信息和统计数值 | 多行字符串，每行都是 `field:value` 形式 |
| **select** dbindex | 切换到指定数据库                      | "OK"                                    |
| **ping**           | 查看服务是否运行                      | PONG                                    |

【Key】

| 命令                    | 功能                                                | 返回值                 |
| ----------------------- | --------------------------------------------------- | ---------------------- |
| **KEYS** pattern        | 查找所有匹配给定模式 pattern 的 key                 | key 数组               |
| **TYPE** key            | 查看 key 对应数据的类型                             | 类型名称               |
| **RENAME** key newkey   | 用于修改 key 的名字为 newkey                        | "OK"                   |
| **EXIST** key [keys...] | 判断指定单个或多个 key 是否存在                     | 存在个数               |
| **DEL** key [keys...]   | 删除指定单个或多个 key 的数据                       | 删除个数               |
| **DUMP** key            | 获取 key 对应 value 的序列化值                      | 多行字符串             |
| **TTL** key             | 查看 key 还有多少秒过期                             | -1 永不过期；-2 不存在 |
| **PERSIST** key         | 设置 key 永不过期                                   | 1 成功；0 失败         |
| **EXPIRE** key          | 给 key 设置过期时间（-1 是永不过期，-2 是已经过期） | 1 成功；0 失败         |
| **MOVE** key dbindex    | 将当前数据库的 key 移动到指定数据库                 | 1 成功；0 失败         |



## 数据类型

### String

存储：二进制安全的字符串，如文字、JSON、序列化对象、二进制文件等

适用：缓存、计数器、分布式锁

实践：短信验证码缓存、抖音短视频播放量统计

| 命令                              | 功能                                 |
| --------------------------------- | ------------------------------------ |
| **SET** key value                 | 设置指定 key 的值                    |
| **SETRANGE** key offset value     | 从 offset 开始用 value 覆盖 key 的值 |
| **MSET** key value [key value...] | 设置所有给定 key 的值                |
| **GET** key                       | 获取指定 key 的 value                |
| **GETRANGE** key start end        | 获取从 start 到 end 的 value 子串    |
| **MGET** key [key...]             | 获取所有给定 key 的值                |
| **STRLEN** key                    | 返回 key 所储存的字符串值的长度      |
| **APPEND** key str                | 将 str 加到 key 原来的 value 末尾    |
| **INCR** key                      | 将 key 存储的 value 加 1             |
| **INCRBY** key increment          | 将 key 存储的 value 加 increment     |
| **DECR** key                      | 将 key 存储的 value 减 1             |
| **DECRBY** key decrement          | 将 key 存储的 value 减 decrement     |

### List

存储：双向链表，可以在头部和尾部高效插入/弹出

适用：消息队列、时间线、异步任务流

实践：微信的消息队列、美团外卖的订单队列

| 命令                                            | 功能                                                  |
| ----------------------------------------------- | ----------------------------------------------------- |
| **LSET** key index element                      | 通过索引设置列表元素的值                              |
| **LINDEX** key index                            | 通过索引获取列表中的元素                              |
| **LRANGE** key start stop                       | 获取列表指定范围内的元素                              |
| **LINSERT** key **BEFORE\|AFTER** pivot element | 把 element 插入到列表 key 中参考值 pivot 的前面或后面 |
| **LTRIM** key start stop                        | 裁剪从 start 到 stop 的列表                           |
| **LREM** key count element                      | 从列表 key 中删除前 count 个值等于 element 的元素     |
| **LPUSH** key element [element...]              | 将一个或多个值插入到列表头部                          |
| **RPUSH** key element [element...]              | 将一个或多个值插入到列表尾部                          |
| **LPOP** key                                    | 移出并获取列表的第一个元素                            |
| **RPOP** key                                    | 移出并获取列表的最后一个元素                          |

### Hash

存储：field-value 字典

适用：结构化数据存储、对象属性信息、配置中心

产品：CF 操作配置记录、淘宝商品详情页信息

| 命令                                       | 功能                                    |
| ------------------------------------------ | --------------------------------------- |
| **HSET** key field value [field value ...] | 为哈希表的 field 字段赋值 value         |
| **HGET** key field                         | 获取哈希表 field 字段的值               |
| **HGETALL** key                            | 获取哈希表所有 field 和 value           |
| **HKEYS** key                              | 获取哈希表所有 field                    |
| **HVALS** key                              | 获取哈希表所有 value                    |
| **HLEN** key                               | 获取哈希表的字段数量                    |
| **HEXISTS** key field                      | 判断哈希表 field 字段是否存在           |
| **HINCRBY** key field increment            | 为哈希表的 field 字段加上增量 increment |
| **HDEL** key field [field ...]             | 删除哈希表一个或多个指定字段            |

### Set

存储：无序且唯一的元素集合，支持交集、并集、差集运算

适用：关系计算、标签系统、去重

实践：QQ 共同好友、豆瓣兴趣标签集合

| 命令                                | 功能                                    |
| :---------------------------------- | :-------------------------------------- |
| **SADD** key member [member ...]    | 向集合添加一个或多个成员                |
| **SREM** key member [member ...]    | 删除集合中一个或多个成员                |
| **SINTER** key [key ...]            | 取集合的交集                            |
| **SUNION** key [key ...]            | 取集合的并集                            |
| **SDIFF** key [key ...]             | 取集合的差集                            |
| **SCARD** key                       | 获取集合的成员数量                      |
| **SMEMBERS** key                    | 获取集合的所有成员                      |
| **SISMEMBER** key member            | 判断 member 是否是集合的成员            |
| **SMOVE** source destination member | 将 member 从 source 移动到  destination |
| **SPOP** key                        | 移除并随机获取一个成员                  |

### ZSet

存储：带分数的集合，成员唯一且按分数排序

适用：排行榜、任务调度、优先队列

实践：网易云音乐热歌榜、王者荣耀巅峰排行榜、微博热搜榜、12306 候补购票

| 命令                                         | 功能                                     |
| :------------------------------------------- | :--------------------------------------- |
| **ZADD** key score member [score member ...] | 将一个或多个成员及其分数加入到有序集合中 |
| **ZREM** key member [member ...]             | 将一个或多个成员从有序集合中移除         |
| **ZINCRBY** key increment member             | 将成员的分数加上增量                     |
| **ZCARD** key                                | 获取有序集的成员个数                     |
| **ZSCORE** key member                        | 获取成员的分数                           |
| **ZCOUNT** key min max                       | 获取分数在指定区间内的成员个数           |
| **ZRANK** key member [WITHSCORE]             | 获取成员从小到大的排名                   |
| **ZREVRANK** key member [WITHSCORE]          | 获取成员从大到小的排名                   |
| **ZRANGE** key start stop [WITHSCORE]        | 从小到大获取指定排名区间的成员           |
| **ZRANGEBYSCORE** key min man [WITHSCORE]    | 从小到大获取指定分数区间的成员           |
| **ZREVRANGE** key start stop [WITHSCORE]     | 从大到小获取指定排名区间的成员           |
| **ZREVRANGEBYSCORE** key min man [WITHSCORE] | 从大到小获取指定分数区间的成员           |

### BitMap

存储：基于 String 的二进制位，每个 bit 表示一个布尔状态

适用：签到统计、状态标记

实践：小红书用户在线状态、贴吧连续签到统计、B 站视频是否观看

| **命令**                                | **功能**                                           |
| --------------------------------------- | -------------------------------------------------- |
| **SETBIT** key offset value             | 将位图第 offset 位设置为 value                     |
| **GETBIT** key offset                   | 获取位图的第 offset 位的值                         |
| **STRLEN** key                          | 获取位图占据的字节长度                             |
| **BITCOUNT** key [start end]            | 统计位图指定区间内值为 1 的 bit 数                 |
| **BITPOS** key bit [start end]          | 查找位图指定区间内第一个值为 bit 的位的偏移量      |
| **BITOP** operation destkey key [key …] | 对一个或多个 BitMap 执行按位操作（AND/OR/XOR/NOT） |

### HyperLogLog

存储：不同元素的估计数量，**无论如何都只需要 12 KB，误差仅约为 0.81%**

适用：用户访客统计、大规模去重计数

实践：淘宝的日活用户数、微博话题的浏览量

| **命令**                                      | **功能**                                         |
| --------------------------------------------- | ------------------------------------------------ |
| **PFMERGE** destkey sourcekey [sourcekey ...] | 将多个 HyperLogLog 合并到一个新的 HyperLogLog 中 |
| **PFADD** key element [element...]            | 将所有元素添加到 HyperLogLog 中                  |
| **PFCOUNT** key [key...]                      | 返回给定集合（并集）的基数估计值                 |

### GEO

存储：基于 ZSet 的地理位置，保存经纬度

适用：范围覆盖、距离计算

实践：美团的附近餐馆、滴滴出行的附近司机

| **命令**                                                     | **功能**                                         |
| ------------------------------------------------------------ | ------------------------------------------------ |
| **GEOADD** key longitude latitude member [longitude latitude member ...] | 将给定经纬度的位置成员加入到集合                 |
| **GEOPOS** key member [member ...]                           | 获取成员的经纬度信息                             |
| **GEOHASH** key member [member ...]                          | 获取经纬度的 hash 映射表示                       |
| **GEODIST** key member1 member2                              | 获取两个给定位置之间的距离（指定单位）           |
| **GEORADIUS** key longitude latitude radius                  | 获取以给定经纬度为中心，在方 radius 内的所有成员 |
| **GEORADIUSBYMEMBER** key member radius                      | 获取以成员为中心，在方 radius 内的所有成员       |

### Stream

存储：消息流，每条消息都有一个唯一 ID 和多个 field-value 记录

适用：消息队列、事件溯源、日志收集

实践：爱奇艺的弹幕系统、饿了么外卖订单系统

| **命令**                                                     | **功能**                                                     |
| ------------------------------------------------------------ | ------------------------------------------------------------ |
| **XADD** key ID field value [field value …]                  | 向流中追加一条消息（ID 为 * 表示主键由 redis 自动生成）       |
| **XLEN** key                                                 | 获取流中的消息数量                                           |
| **XRANGE** key start end [COUNT count]                       | 按 ID 正序获取消息（-/+ 表示最大和最小）                     |
| **XREVRANGE** key end start [COUNT count]                    | 按 ID 倒序获取消息（-/+ 表示最大和最小）                     |
| **XDEL** key id [id …]                                       | 删除指定 ID 的消息                                           |
| **XTRIM** key MAXLEN count                                   | 截取 ID 大的 count 条消息                                    |
| **XTRIM** key MINID id                                       | 截取比 ID 小的消息                                           |
| **XREAD** [COUNT count] [BLOCK ms] **STREAMS** key [key …] ID [ID …] | 从一个或多个流中（阻塞）读取（指定数量）消息                 |
| **XGROUP CREATE** key group id                               | 创建消费组，从指定 ID 开始消费（$ 表示最后一条消息）         |
| **XGROUP** DESTROY key group                                 | 删除指定消费组                                               |
| **XINFO** GROUPS mystream                                    | 获取消费组信息                                               |
| **XREADGROUP GROUP** group consumer [COUNT count] [BLOCK ms] **STREAMS** key [key …] ID [ID …] | 使用消费组 group 中的消费者 consumer 来消费消息（ID 用 > 表示读取下一个未被消费的消息） |
| **XPENDING** key group [start end count [consumer]]          | 查看消费组中待确认的消息                                     |
| **XACK** key group id [id …]                                 | 确认消息已被成功处理，标记为已消费                           |



## 持久化 Persistence

### 意义

因为 Redis 的数据是存储在内存的，**如果系统断电或宕机，那么内存中的数据很有可能会丢失**，因此需要将数据写到磁盘，保证重启时能够恢复数据。

### RDB

【定义】

RDB（Redis DataBase） 会把内存里某一时刻的**数据快照**保存到磁盘的 **dump.rdb** 文件

【优点】

- 二进制快照，读取和加载速度快
- 可以自动定时备份，不需要手动操作
- 每次保存的都是完整数据快照，方便全量恢复

【缺点】

- 可能会存在 RDB 空窗期，系统突然宕机会有丢失数据风险
- 如果内存数据很大，那么 fork 操作会有秒级阻塞
- 全量同步会大大增加 I/O 压力

【配置】

- `dbfilename`：RDB 文件存储的名称
- `stop-writes-on-bgsave-error`：如果 RDB 操作失败，是否停止写操作
- `rdbcompression`：是否对 RDB 文件进行 LZF 压缩
- `rdbchecksum`：是否在 RDB 文件末尾加上校验和，但是在保存/加载时造成一定的 CPU 额外消耗
- `rdb-del-sync-files`：是否在加载完成后删除文件

【自动触发】

- 默认规则

    - 在 3600 秒 / 1 小时内至少有 1 次写操作

    - 在 300 秒 / 5 分钟内至少有 100 次写操作

    - 在 60 秒 / 1 分钟内至少有 10000 次写操作

- 手动设置：`save 秒数 写操作数 [秒数 写操作数...]`（手动设置会覆盖默认规则）

- 禁用：`save ""`（手动触发仍然生效）

- 触发命令：**flushdb、flushall、shutdown**

【手动触发】

- **SAVE**：立即在主线程执行 RDB，在持久化完成之前阻塞其他请求，生产环境不可使用
- **BGSAVE**：主线程会 fork 一个子线程执行 RDB，主线程仍然可以处理请求
- **LASTSAVE**：获取上一次 RDB 的时间戳

### AOF

【定义】

AOF（Append Only File）会把所有**写命令**记录到一个 **appendonly.aof** 日志文件

【优点】

- 只会逐条追加写命令，丢数据的窗口最多秒级，数据更安全
- 内容不是二进制的，可以直接读取命令
- 如果不小心执行了 flushdb 和 flushall，完全可以通过手动编辑 AOF 文件来撤销

【缺点】

- 重启相当于一条条执行 AOF 命令，速度很慢
- 记录命令会比记录数据占用更多内存

【流程】

1. 用户发出写命令
2. Redis 根据写命令执行写操作，同时把写命令写入到 AOF 缓冲区
3. Redis 根据配置的 appendfsync 策略，把缓冲区的数据写到 AOF 文件
4. 随着时间推移，AOF 文件会越来越大，一定程度下 Redis 会触发 AOF 重写，使用等价但体积更小的命令来替换原来的 AOF 文件
5. 当 Redis 重启的时候，会加载 AOF 文件，顺序执行写命令恢复数据

![image-20250824172004958](https://dasi-blog.oss-cn-guangzhou.aliyuncs.com/Java/SpringMVC202508241720454.png)

【配置】

- `appendonly`：是否开启 AOF 持久化，开启后会优先使用 AOF 而不是 RDB
- `appenddirname`：AOF 文件存储的路径（相对于 RDB 的路径 dir）
- `appendfilename`：AOF 文件存储的名称，但是在 Redis7 之后不再使用，而是默认使用以下三个
    - `base.rdb`：保存基准快照
    - `incr.aof`：保存增量日志
    - `manifest`：保存文件清单，指导 Redis 如何使用 base.aof 和 incr.aof
- `appendfsync`：AOF 缓冲区的写入磁盘策略
    - `always`：每次写命令都同步到磁盘，最安全但是最慢
    - `everysec`：每秒写一次，数据丢失在秒级
    - `no`：交给操作系统来控制，性能最好，但是可能会丢失较多数据
- `no-appendfsync-on-rewrite`：在 AOF 重写期间是否禁止 fsync
- `auto-aof-rewrite-percentage`：AOF 文件大小增长比例触发重写（100 表示增长一倍后触发）
- `auto-aof-rewrite-min-size`：触发 AOF 重写的最小文件大小
- `aof-load-truncated`：当 AOF 文件因异常时，是否继续加载
- `aof-use-rdb-preamble`：是否启用 AOF 混合持久化，当 Redis 在执行 AOF 重写时，会先把当前内存快照存储到 base.rdb，然后把这之后的写命令存储到 incr.aof

### 修复文件

意义：如果只是一个或两个 key 或写命令损坏，仍然会使得整个 dump.rdb 或 appendonly.aof 文件无法被 Redis 解析，导致重启失败

校验：只会反馈检查信息

-  `redis-check-rdb /path/to/dump.rdb` 
-  `redis-check-aof /path/to/appendonly.aof`

修复：丢失损坏的 key 或命令

- `redis-check-rdb --fix /path/to/dump.rdb`：
- `redis-check-aof --fix /path/to/dump.rdb`



## 事务 Transaction

### 定义

事务是一组按顺序执行的命令集合，这些命令会被 Redis 一次性且串行地执行，执行过程中不会被其他命令插入

| **特性**             | **MySQL 事务**                                   | **Redis 事务**                                               |
| -------------------- | ------------------------------------------------ | ------------------------------------------------------------ |
| 原子性 (Atomicity)   | 支持完整的回滚，保证要么全部执行，要么全部不执行 | 不支持回滚，执行错误不会撤销，只能保证一组命令按顺序执行     |
| 一致性 (Consistency) | 严格保证数据一致性                               | 通过 WATCH 实现乐观锁，保证事务期间 key 没被修改，否则事务失败 |
| 隔离性 (Isolation)   | 可以设置不同的隔离级别                           | 事务内的命令在 EXEC 之前不会执行，而一旦执行不会被打断       |
| 持久性 (Durability)  | InnoDB 日志（redo/undo）确保提交的数据不会丢失   | 依赖于 RDB/AOF，事务本身不提供持久性保证                     |
| 错误处理             | 可以用 ROLLBACK 命令撤销事务命令                 | 只能用 DISCARD 丢弃事务还没执行的命令                        |
| 适用场景             | 金融、订单、库存，追求强一致性                   | 排行榜、抢票，追求高性能和低延迟                             |

### 命令

- **MULTI**：开启一个事务，之后的命令会进入事务队列
- **EXEC**：一次性执行先前事务队列里的所有命令，顺序执行不会被打断
- **DISCARD**：取消事务，清空事务队列里的所有命令，但无法撤销已经执行的操作
- **WATCH**：开始对 key 对监视，用于实现**乐观锁**，即在提交事物时如果检测到正在监视的 key 被其他客户端修改了，那么 EXEC 会返回 nil，事务失败
- **UNWATCH**：取消对所有 key 对监视

### 错误处理

| 错误类型     | 处理                                     | 理解                               | 例子       |
| ------------ | ---------------------------------------- | ---------------------------------- | ---------- |
| 入队阶段错误 | 整个事务内的命令都会被放弃               | 编译期错误，如命令不存在、语法错误 | SET k1     |
| 执行阶段错误 | 只有错误的命令会失败，其他命令仍然会执行 | 运行期错误，如命令与数据结构不对应 | INCR email |



## 管道 Pipeline

### Redis 通信服务

Redis 是一种**基于客户端-服务端和请求-响应的 TCP 服务**

- 客户端发送命令到服务端，服务端执行命令并返回结果到客户端，客户端以阻塞模式监听 Socket 来等待服务端的响应
- 数据包往返于两端到时间被称为 **RTT（Round Trip Time）**

一条一条命令地发送的弊端

- **RTT 延迟累积**：每条命令都要经历一次请求 + 响应的完整 RTT
- **频繁 I/O 调用**：网路交互需要通过网卡实现发送和接收数据包
- **严重 CPU 开销**：频繁调用多次 read() 和 write() 会导致操作系统在用户态和内核台之间来回切换

### 定义

管道是一种**批量发送命令**的机制

- 客户端会将多条命令打包，通过单次网络请求一次性将命令发送给服务端，服务端会按顺序执行这些命令，然后将所有结果一次性返回给客户端
- 无论多少条命令都只需要一次 RTT
- 大大提升吞吐量，Redis 服务端可以按顺序连续处理请求，效率更高

![5cf333bd-6679-4bc9-8c23-93e5c8ab2983](https://dasi-blog.oss-cn-guangzhou.aliyuncs.com/Java/SpringMVC202508271625537.png)

```bash
cat batch.txt | redis-cli -a password --pipe
```

- `cat batch.txt`：显示文件的内容到标注输出
- `|`：linux 管道符，会把前一个命令的输出作为后一个命令的输入
- `--pipe`：开启 Redis 的管道模式，一次性读取标准输入里的所有命令，然后批量发送给 Redis

### 批量执行区分

| 特性     | 管道                                                     | 事务                                                       | 命令                                               |
| -------- | -------------------------------------------------------- | ---------------------------------------------------------- | -------------------------------------------------- |
| 定义     | 一次性发送多条命令到 Redis，并一次性接收命令结果         | 把多条命令打包，顺序执行并保证不被打断                     | Redis 内置支持的一次性操作多个 key 的命令          |
| 目的     | 提高性能，减少 RTT、I/O 开销                             | 保证逻辑一致性，控制并发冲突                               | 简化操作逻辑                                       |
| 错误处理 | 某条命令失败不影响其他命令，本质上还是一条一条命令的执行 | 入队时报错会导致整个事务取消，执行时错误只会影响错误的命令 | 命令层面执行，某些子操作可能失败但不会影响其他 key |
| 事务属性 | 没有原子性                                               | 批量原子性                                                 | 命令原子性                                         |
| 典型用法 | 追求性能：批量写入、批量查询、大数据初始化               | 追求一致：扣库存、转账、订单生成                           | 追求方便：批量设置缓存、批量删除数据               |



## 复制 Replication

### 定义

将一个 Redis 实例的数据同步到其他多个 Redis 实例，前者称为主节点 Master，后者称为从节点 Slave

- **Master 主要负责处理写请求，Slave 主要负责处理读请求**
- **同步请求 Slave → Master**：在 redis.conf 中，Slave 的 masterauth 需要与 Master 的 requirepass 一致
- **数据传输 Master → Slave**：保持主从一致
- Master 和 Slave 是相对的，**所有节点在一开始都是 Master**，同步请求后才会变成 Slave
- **一个节点可以同时作为 Master 和 Slave**，形成链式关系，但数据会始终同步自最前 o 的 Master

<img src="https://dasi-blog.oss-cn-guangzhou.aliyuncs.com/Java/SpringMVC202508271625637.png" alt="04f28596-3eac-4659-b605-c60ea7f836d1" style="zoom:33%;" />

### 节点信息

可以利用 `info replication` 查看

- Master
    - **connected_slaves**：已经连接的 Slave 数量
    - **slavex**：按顺序连接的第 x 个 Slave 的信息，包括 ip，port，state，offset，lag
    - **master_replid**：主节点的复制 ID
    - **master_repl_offset**：Master 当前的复制偏移量
    - **repl_backlog_active**：是否开启复制 backlog
    - **repl_backlog_histlen**：backlog 中已有的数据长度

- Slave
    - **master_host**：Master 运行 ip
    - **master_port**：Master 运行 port
    - **master_link_status**：是否连接上 Master
    - **master_last_io_seconds_ago**：最近一次和 Master 交互的秒数
    - **master_sync_in_progress**：是否正在做全量同步
    - **slave_repl_offset**：当前 Slave 已经复制到的偏移量
    - **slave_priority**：用于 Sentinel 选主时的优先级
    - **slave_read_only**：是否只读

### 命令

| 命令                                    | 功能                                       |
| --------------------------------------- | ------------------------------------------ |
| **REPLICAOF <master_ip> <master_port>** | 设置当前 Redis 实例为某个 Master 的 Slave  |
| **REPLICAOF NO ONE**                    | 取消复制关系，恢复当前 Redis 实例为 Master |

### 工作流程

1. Slave 主动申请与 Master 建立连接，发起 PSYNC 请求
2. Master 收到 PSYNC 请求后，会立刻执行 BGSAVE，生成 RDB 快照，同时在这期间把写命令写入 backlog
3. Master 把 RDB 文件 + backlog 命令发送给 Slave
4. Slave 收到后会清空自己的数据，再加载文件到内存，完成数据初始化
5. Master 会周期性地发 PING 到 Slave，检测连接是否存活
6. Slave 会周期性地发 REPLCONF ACK 到 Master，报告自己复制进度 offset
7. Master 每次都是先执行写命令作用到本地内存，然后再追加到 backlog
8. Master 会根据每个 Slave 报告的 offset，决定从 backlog 哪个位置开始推送写命令

### 缺陷

- 延迟高：在高并发和网络抖动时，Slave 数据可能会远远落后于 Master，导致客户端读取到旧数据
- 单点故障：Master 挂掉后，不会有 Slave 自动上位，也不会主动取消 Slave 角色
- 数据丢失：如果 Master 的 backlog 出错，会导致整个系统数据丢失
- 开销大：如果有多个 Slave 与 Master 建立新的连接，全量复制会加剧 Master 压力



## 哨兵 Sentinel

### 定义

哨兵本质上是一个特殊模式的 Redis 实例，它本身不用于存储数据，而是专门用于**主从复制结构**

- **监控**：持续检测 Master 和 Slave 是否正常运行
- **转移**：当 Master 挂掉后，会自动选举一个 Slave 升级为新的 Master，并更新其他 Slave 的 Master
- **通知**：可以把故障情况和转移情况通知到客户端，并且会自动更新客户端保存的 Master 地址
- **恢复**：当原来的 Master 恢复上线时，哨兵会将它自动降级为 Slave 并重新加入主从复制结构

<img src="https://dasi-blog.oss-cn-guangzhou.aliyuncs.com/Java/SpringMVC202508271624414.png" alt="78c46ac2-694d-4c01-be14-fa1b4db140b8" style="zoom:33%;" />

### 配置

启动命令：`redis-server /etc/redis/sentinel.conf --sentinel`

```conf
# 实例配置
bind 0.0.0.0
daemonize yes
protected-mode no
port 26379
logfile "/var/log/sentinel_26379.log"
pidfile "/var/run/sentinel_26379.pid"
dir "/var/lib/redis"

# 哨兵配置
sentinel monitor mymaster 127.0.0.1 6379 2
sentinel auth-pass mymaster <password>
```

### 实践

1. 开启主从实例

    ```redis
    redis-server /etc/redis/redis_6379.conf
    redis-server /etc/redis/redis_6380.conf
    redis-server /etc/redis/redis_6381.conf
    ```

2. 开启哨兵实例

    ```redis
    redis-server /etc/redis/sentinel_26379.conf --sentinel
    redis-server /etc/redis/sentinel_26380.conf --sentinel
    redis-server /etc/redis/sentinel_26381.conf --sentinel
    ```

3. 设置主从关系

    ```redis
    127.0.0.1:6380> REPLICAOF 127.0.0.1 6379
    127.0.0.1:6381> REPLICAOF 127.0.0.1 6379
    ```

4. 关闭 Redis-6379：存在延迟，哨兵正在执行转移，会发出 `Error: Server closed the connection` 异常，然后哨兵会选举 6380 作为新的 Master，并更新 6381 为 6380 的 Slave

5. 重启 Redis-6379：存在延迟，哨兵正在执行恢复，仍然认为自己是 Master 角色，然后哨兵会将 6379 降级为 6380 的 Slave

### 原理

1. **监控过程**
    1. **主观下线（SDOWN）**：一个 Sentinel 发送心跳命令到 Master，发现 Master 超过 down-after-milliseconds 没响应，就**自认为** Master 挂了
    2. **客观下线（ODOWN）**：多个 Sentinel 也检测到相同情况，当确认数超过 quorum 时，会**统一认定** Master 挂了，进入故障转移流程
2. **选举过程**
    1. 集群会进入一个 epoch，每个 Sentinel 会请求其他所有 Sentinel 给自己投票
    2. Sentinel 会给自己收到的最先请求的 Sentinel 投票，并且每个 epoch 只能投票一次，投票完会忽略之后的请求
    3. 如果某个 Sentinel 检测到自己获得的票数已经超过 majority 时，会成为 Leader
    4. 如果没有 Sentinel 当选 Leader，那么会进入下一轮 epoch，重复上述过程
3. **挑选过程**
    1. `replica-priority`：**值越小越会被选择**，由开发员在 redis.conf 中直接配置，但是 0 表示永远不可能成为 Master
    2. `replication offset`：**值越大越会被选择**，复制偏移量越大说明数据越完整越新
    3. `runid`：**值越小越会被选择**，是 Redis 启动时随机生成的不重复 ID，因此可以保证该过程能确定一个 Slave
4. **转移过程**
    1. 给之前挑选好的 Slave 发送 `SLAVEOF NO ONE` 提升其为新的 Master
    2. 找到剩下的 Slaves 发送 `SLAVEOF` 让他们与新的 Master 建立连接
    3. Leader 会把新的 Master 信息广播给其他 Sentinel，然后所有 Sentinel 都会更新自己的配置文件
5. **恢复过程**
    1. 当有新节点加入进来，哨兵会发 `PING` 和 `INFO replication` 获取节点原先保存的信息
    2. 这个新节点可能是纯新的，也有可能是先前挂掉的 Master 或 Slave，无论如何 所有 Sentinel 都会向它发送 `SLAVEOF`，让它去同步当前的 Master

### 缺陷

- 故障转移期间，最新写入的数据可能还没同步到 Slave，因此新 Master 也不会有这部分数据，**做不到强一致性，只能做到最终一致性**
- 从故障检测到转移完成，这期间 Redis 服务是不可用的，可能会导致业务服务直接终端
- 如果发生网络错误，Sentinel 可能把仍然存活的 Master 判为下线，提升另一个 Slave 为 Master，导致系统出现了两个 Master



## 集群 Cluster

### 定义

Redis 集群是官方提供的**分布式部署方案**

- **分片（shard）**：把一整个数据集拆分为多个子集，分别存储在不同的节点上
- **哈希槽（hash slot）**：集群会根据键的哈希值映射到到具体的槽位
- **分片是真实的物理分区，哈希槽是虚拟的逻辑分区**
- **槽分配给分片，分片负责多个槽**

![6224a5021340a8c79df5c0eb1e33f6dc](https://dasi-blog.oss-cn-guangzhou.aliyuncs.com/Java/202508271629527.png)

Redis Cluster 定义了 **16384 个哈希槽**（编号 0–16383），假设 Master1 管理槽 0–5460，Master2 管理槽 5461–10922，Master3 管理槽 10923–16383，那么键 "name" 经过哈希后得到 slot=7365，检查得到槽位在 Master2，那么就会把这个命令发到 Master2 执行

- Redis 不会在内存里专门建一个 slot[0..16383] 的数组去存 key，实际上 **key 还是照常存储在 Redis 节点自己的哈希表里**
- Redis Cluster 使用 `CRC16(key) mod slots` 计算槽位，16384 = $2^{14}$ 可以很方便地用位运算
- 16384 可以很平均地把 key 打散，负载均衡效果好
- 槽数太少迁移不灵活，槽数太多会增加内存和通信开销，16384 是实践验证的最佳平衡点

<img src="https://dasi-blog.oss-cn-guangzhou.aliyuncs.com/Java/SpringMVC202508262258956.png" alt="image-20250826225856274" style="zoom:33%;" />

### 优势

- **性能高**：写入和查询请求根据精心设计的哈希算法会被均分分散到不同节点，每个节点只处理部分数据，整体吞吐量成倍提升
- **高可用**：内置哨兵功能，每个 Master 节点都有一个或多个 Slave 节点作为副本，当 Master 宕机时，Cluster 会自动把某个 Slave 提升为 Master，实现自动故障转移
- **可扩展**：集群采用 16384 个槽位分片，新增节点时只需把部分槽迁移过去即可，支持在线扩容或缩容，容量和性能几乎可以线性增长
- **去中心化**：Cluster 没有中心节点，每个节点都保存槽分配信息，并通过 Gossip 协议交换状态，避免单点故障

### 哈希分区策略

| 策略                | 原理                                                         | 优点                       | 缺点                                  |
| ------------------- | ------------------------------------------------------------ | -------------------------- | ------------------------------------- |
| hash(key) mod nodes | 直接将哈希值对节点数取余，余数就是节点编号                   | 实现最简单                 | 节点一旦变化，所有 key 都要被重新分配 |
| hash(key) mod slots | 先将哈希值对槽数取余，余数就是槽位编号，再映射到节点编号     | 兼顾均匀性和可扩展性       | 需要多一步槽位到节点的映射            |
| consistent hash     | 把哈希空间组成一个环，节点和 key 都会映射到环上，key 属于按顺时针查找最近的节点 | 节点增减时只影响附近的 key | 无法保证均衡性                        |

### Gossip 协议

Gossip 协议时一种**分布式系统中去中心化传播节点状态和元信息**的协议

- 传播信息：存活、下线、加入、移除、故障、槽位分配、数据分布、配置变更
- 传播方式：节点周期性选择一个随机节点通信，交换彼此最新状态
- 传播特征：不是瞬时一致，而是随着 Gossip 轮次逐渐全网收敛，收敛速度约 O(log N)

Redis 使用

- 节点通过**集群总线端口（服务端口 + 10000）**进行 Gossip 消息交换
- 每个节点周期性地向其他节点发送 PING 消息，并附带自己对集群状态的部分认知，接收方返回 PONG，附带自己的状态信息
- 如果一个节点在一定时间内未收到某节点的 PONG，则会把该节点标记为 **PFAIL（疑似下线）**，若多个节点通过 Gossip 达成共识 → 标记为 **FAIL（确认下线）**并广播

### 配置

```conf
# 实例配置
bind 0.0.0.0
daemonize yes
protected-mode no
port 7000
pidfile /var/run/redis_7000.pid
logfile "/var/log/redis_7000.log"
dir /var/lib/redis/7000

# 开启集群
cluster-enabled yes
cluster-config-file nodes_7000.conf
cluster-node-timeout 5000

# 持久化
appendonly yes
```

### 命令

#### 命令行工具

| 命令                                                         | 功能                                                         |
| ------------------------------------------------------------ | ------------------------------------------------------------ |
| redis-cli **-c** -p port                                     | -c 会开启集群模式，当操作落在其他节点的槽，会自动重定向到其他节点，不需要手动 exit 和重连接，否则会抛出 `(error) MOVED` 错误 |
| redis-cli --cluster **create** ip\:port … [**–cluster-replicas n**] | 创建集群，一次性添加多个节点，通过 n 指定每个 Master 对应多少个 Slave |
| redis-cli --cluster check ip\:port                           | 检查集群整体状态                                             |
| redis-cli --cluster **rebalance** ip:port                    | 自动均衡所有 Master 的槽分布                                 |
| redis-cli --cluster **reshard** ip\:port                     | 将槽重新分配给其他节点，ip:port 是任意一个已存在集群中的节点即可，提示步骤为：<br />1. 输入迁移的槽数量<br />2. 输入迁移对象的节点 ID<br />3. 输入从哪些节点迁出槽<br />4. 输入 yes 开始迁移 |
| redis-cli --cluster **add-node** ip\:port ip\:port [--cluster-slave] | 加节点到集群之中，默认是 Master，Slave 需要添加额外参数，第二个 ip\:port 是已经存在的节点作为“引荐人”提供集群入口 |
| redis-cli --cluster **del-node** ip\:port node-id            | 从集群之中删节点，如果是 Master 需要先把槽分配出去，Slave 可以直接删 |

#### 集群管理

| 命令                             | 功能                                                    |
| -------------------------------- | ------------------------------------------------------- |
| **CLUSTER INFO**                 | 查看集群整体状态（槽数量、节点数量、轮次...）           |
| **CLUSTER NODES**                | 查看所有节点的详细信息（ID、角色、槽范围、连接状态）    |
| **CLUSTER SLOTS**                | 查看槽分配情况（槽区间属于哪个 Master 和其 Slave）      |
| **CLUSTER KEYSLOT** key          | 查看 key 属于哪个槽号（key 不需要存在，只是查询哈希值） |
| **CLUSTER COUNTKEYSINSLOT** slot | 查询 slot 已经存了多少个 key                            |
| **CLUSTER GETKEYSINSLOT** count  | 查询 slot 中 count 个 key                               |

#### 节点管理

| 命令                          | 功能                                                         |
| ----------------------------- | ------------------------------------------------------------ |
| **CLUSTER MEET** ip port      | 手动让一个新节点与当前节点建立联系，从而加入集群（但此时没有任何角色） |
| **CLUSTER FORGET** node-id    | 手动让一个节点从集群中脱离                                   |
| **CLUSTER REPLICATE** node-id | 把当前节点设置为某个 Master 的 Slave                         |
| **CLUSTER RESET**             | 重置节点信息                                                 |
| **CLUSTER FAILOVER**          | 强制让某个 Slave 执行主从切换，提升为 Master                 |
| **CLUSTER SAVECONFIG**        | 强制保存集群配置到 nodes.conf                                |
| **CLUSTER MYID**              | 查看当前节点的唯一 ID                                        |

#### 槽管理

| 命令                                           | 功能                                                         |
| ---------------------------------------------- | ------------------------------------------------------------ |
| **CLUSTER ADDSLOTS** slot                      | 给当前节点分配槽（只能是 Master）                            |
| **CLUSTER DELSLOTS** slot                      | 删除当前节点的槽（只能是 Master，槽会处于悬空状态，必须手动重新分配） |
| **CLUSTER SETSLOT** slot **NODE** node-id      | 把某个槽指派给指定节点（只能是 Master）                      |
| **CLUSTER SETSLOT** slot **IMPORTING** node-id | 让当前节点从另一个节点导入槽（成对使用）                     |
| **CLUSTER SETSLOT** slot **MIGRATING** node-id | 让当前节点向另一个节点导出槽（成对使用）                     |



## SpringBoot 集成

### RedisTemplate

RedisTemplate 是 Spring Data Redis 提供一个操作 Redis 的工具类，**它把 Redis 的各种命令封装成 Java 方法**，从而可以用面向对象的方式操作 Redis，内部调用 Jedis 或 Lettuce

| 对比       | Jedis                    | Lettuce                        |
| ---------- | ------------------------ | ------------------------------ |
| I/O 模型   | 阻塞                     | 基于 Netty，非阻塞             |
| 线程安全性 | 非线程安全，需要连接池   | 线程安全，可多线程复用一个连接 |
| 连接管理   | 依赖 commons-pool2       | 默认单连接，支持连接池，可复用 |
| 调用方式   | 只支持同步               | 同步 / 异步 / 响应式           |
| 性能       | 中等，连接池可能成为瓶颈 | 高，适合高并发                 |

Lettuce 是 Redis 真正的客户端，因为 **Redis 本质上是客户端-服务端的 TCP 通信**，RedisTemplate 在底层使用 Lettuce 发送命令请求和返回数据响应

```text
代码：业务逻辑
 ↓
RedisTemplate：核心 API 封装类
 ↓
RedisConnectionFactory：连接工厂接口，封装底层实现，向上提供 RedisConnection
 ↓
LettuceConnectionFactory：连接工厂实现类，调用 Lettuce 客户端来管理 Redis 连接
 ↓
Lettuce：作为 Redis 客户端，负责底层 TCP 通信，把命令序列化为 Redis 协议
 ↓
Redis：接收命令，在内存中执行，返回结果
```

### 序列化问题

Redis 处理：统一存**二进制字节数组**，redis-cli 在显示数据时会尝试用 UTF-8 解码字节数组

- 如果是 ASCII 字符，可以直接显示
- 如果有特殊字符如中文，就会显示成 \x?? 转义形式
- 可以通过启动 CLI 时加参数 --raw，不进行转义直接原样展示

Java 处理：对于 String、Integer 和自定义实体类都需要将对象序列化为字节数组

- **JdkSerializationRedisSerializer**：默认，会把整个对象序列化，包括了类名、serialVersionUID 等元数据，只能 Java 读，跨语言不友好，在 CLI 看到的全是乱码
- **StringRedisSerializer**：只是把字符串的值本身序列化
- **Jackson2JsonRedisSerializer**：先把对象转换成 JSON 格式的字符串，然后再进行序列化

配置：可以将 key 和 value 分别设置不同的序列化和反序列化方式

```java
@Configuration
public class RedisConfig {
    @Bean
    public RedisTemplate<String, Object> redisTemplate(RedisConnectionFactory factory) {
        RedisTemplate<String, Object> template = new RedisTemplate<>();
        template.setConnectionFactory(factory);

        // key 序列化为字符串
        StringRedisSerializer stringSerializer = new StringRedisSerializer();
        template.setKeySerializer(stringSerializer);
        template.setHashKeySerializer(stringSerializer);
      	
      	// value 序列化为 JSON
        Jackson2JsonRedisSerializer<Object> jsonSerializer = new Jackson2JsonRedisSerializer<>(Object.class);
        template.setHashValueSerializer(jsonSerializer);
       	template.setValueSerializer(jsonSerializer);

        template.afterPropertiesSet();
        return template;
    }
}
```

### 配置

1. 关闭虚拟机防火墙

    ```bash
    sudo systemctl stop firewalld
    ```

2. Redis 配置

    ```conf
    bind 0.0.0.0
    protected-mode no
    cluster-announce-ip 172.16.140.128
    cluster-announce-port 7000
    cluster-announce-bus-port 17000
    ```

3. 添加依赖

    ```xml
    <dependency>
        <groupId>org.springframework.boot</groupId>
        <artifactId>spring-boot-starter-data-redis</artifactId>
    </dependency>
    ```

4. SpringBoot 配置

    ```yml
    spring:
      data:
        redis:
        	# 基础配置
          host: 172.16.140.128
          port: 6379
          password: 123456
          # 集群配置
          cluster:
            nodes:
              - 172.16.140.128:7000
              - 172.16.140.128:7001
              - 172.16.140.128:7002
              - 172.16.140.128:7003
              - 172.16.140.128:7004
              - 172.16.140.128:7005
          # 连接池配置
          lettuce:
            pool:
            	# 最大活跃连接数
              max-active: 8
              # 最大空闲连接数
              max-idle: 8
              # 最小空闲连接数
              min-idle: 1
              # 最大等待时间
              max-wait: 1000ms
            refresh:
            	# 开启自适应拓扑刷新
            	adaptive: true
            	# 自动刷新间隔
            	period: 60s
    ```



## BigKey

### 概念

【定义】

BigKey 指的是**单个 key 的 value 内容过大**或者**单个 key 的 value 数量过多**

【原因】

- **数据存储设计不当**：日志内容作为超大 String 直接存入
- **数据清理不及时**：消息队列没有作过期控制，导致 List 堆积百万条数据
- **数据规模考虑不周到**：统计类 Hash 不断增长，没有分库分表

【危害】

- **网络阻塞**：每次获取 BigKey 会返回超大数据包，网络带宽被占满
- **客户端阻塞**：Redis 执行命令是单线程处理，对 BigKey 的操作会经过很久才能有响应
- **工作线程阻塞**：如果使用 del 删除 BigKey 时，会阻塞工作线程，没办法处理后续的命令
- **内存碎片**：过大的对象会导致内存分配和回收不均匀

### SCAN

```redis
keys pattern
```

一次性返回所有匹配的 key，会阻塞 Redis，严重时会直接导致 Redis 服务卡死挂掉，生产环境不可使用

```redis
SCAN / HSCAN / SSCAN / ZSCAN key cursor [pattern] [count]
```

可以按照游标位置，根据自定义的匹配模式和数量分批次获取 key

- SCAN 遍历全局 key，HSCAN 遍历 value 中的 field，SSCAN 和 ZSCAN 遍历所有 member
- List 没有 LSCAN，但可以通过 LRANGE 分段获取
- 一般从 cursor = 0 开始遍历，如果返回值是 0 表示遍历完毕

### 发现

- redis-cli **--bigkeys**：找出每种类型的最大 key，并且给出每种类型的键个数和平均大小
- 先用 SCAN 分批获取 key，然后根据对应数据类型逐个使用 **STRLEN、HLEN、LLEN、SCARD、ZCARD** 获取其长度或成员数量
- **MEMORY USAGE** key：精确查询某个 key 的内存占用
- 借助**开源工具**分析 RDB 文件
- **公有云**的 Redis 服务的话提供了 key 分析功能

### 处理

- **UNLINK**：先解除 Redis 对 BigKey 的引用，由后台线程异步删除，可以避免阻塞主工作线程
- **lazy-free**：在配置文件中开启懒释放，当内部触发自动删除的时候，会 fork 子线程异步清理，同样可以避免阻塞主工作线程
- **采用合适数据结构**
    - 大文件应该持久化存储，Redis 只保存文件路径
    - 海量计数不要用 Set 而是用 HyperLogLog
    - 布尔状态不要用 Hash 而是用 BitMap
    - 日志流不要用 List 而是用 Stream



## 双写一致性

### 策略

在写数据库和写缓存期间出现的脏数据，**不可能做到强一致性，目标是保证最终一致性和高可用**

- 先更新数据库，再删除缓存（✅）：不会出现脏数据，删除缓存的开销相对较小，只有下一次读的时候再写入缓存
- 先更新数据库，再更新缓存（⚠️）：不会出现脏数据，但是新数据不一定会被用到，而更新缓存的开销相对较大，会耗费资源
- 先更新缓存，再更新数据库（❌）：如果更新数据库失败了，那么会出现脏数据，而且原则上是缓存追求与数据库一致，而不是数据库追求与缓存一致
- 先删除缓存，再更新数据库（❌）：存在空窗期，此时不仅缓存 miss，所有请求直接打到数据库，并且读到的还是脏数据

![image-20250827220756743](https://dasi-blog.oss-cn-guangzhou.aliyuncs.com/Java/202508272207378.png)

### Canal

Canal 是阿里巴巴开源的 MySQL binlog 增量订阅 & 消费组件，核心功能是把 MySQL 的 binlog 解析为可读数据，分发给下游系统（Redis、RocketMQ）进行更新

1. Canal 会实现 MySQL 的 replication 协议来模拟 MySQL Slave
2. Canal 会主动向 MySQL Master 发送 dump 请求
3. MySQL Master 收到 dump 请求后，会推送 binlog 给伪装成 MySQL Slave 的 Canal
4. Canal 会把二进制 binlog 解析成结构化数据，并把增量变化推送到 Redis 实现缓存更新

流程

1. 配置 Canal Server：`root/conf/example/instance.properties`

    ```properties
    # MySQL 连接信息
    canal.instance.master.address=127.0.0.1:3306
    canal.instance.dbUsername=root
    canal.instance.dbPassword=123456
    canal.instance.connectionCharset = UTF-8
    # 订阅规则（正则）：所有库所有表
    canal.instance.filter.regex=.*\\..*
    ```

2. 配置 MySQL：`/etc/my.cnf`

    ```cnf
    [mysqld]
    server-id=1
    log-bin=mysql-bin
    binlog-format=ROW
    ```

3. 配置 Redis：`/etc/redis/redis_6379.conf`，还需要关闭防火墙 `systemctl stop firewalld`

    ```conf
    bind 0.0.0.0
    protected-mode no
    port 6379
    requirepass 123456
    ```

4. 配置 SpringBoot：`application.yml`

    ```yml
    spring:
      data:
        redis:
          host: 172.16.140.128
          port: 6379
          password: 123456
    ```

5. 配置 Canal Client

    ```java
    public class CanalClient {
    
        // Canal Server 的配置
        private static final String CANAL_SERVER_HOST = "127.0.0.1";
        private static final Integer CANAL_PORT = 11111;
        private static final String DESTINATION = "example";
        private static final String USERNAME = "";
        private static final String PASSWORD = "";
    
        // 注入 Redis
        @Autowired
        private StringRedisTemplate redisTemplate;
    
        // 配置 Canal 连接
        private CanalConnector connector;
    
        // 在 Spring 容器启动后自动执行
        @PostConstruct
        public void init() {
            connector = CanalConnectors.newSingleConnector(
                    new InetSocketAddress(CANAL_SERVER_HOST, CANAL_PORT),
                    DESTINATION,
                    USERNAME,
                    PASSWORD);
            // 开启一个线程执行监听方法
            new Thread(this::listen).start();
        }
    
    
        // 监听方法
        public void listen() {
            try {
                connector.connect();
                // 需要监听传来的所有库表信息
                connector.subscribe(".*\\..*");
                connector.rollback();
    
                // 无限循环，一直监听并调用解析方法
                while (true) {
                    Message message = connector.getWithoutAck(100);
                    long batchId = message.getId();
                    int size = message.getEntries().size();
                    if (batchId != -1 && size > 0) {
                        handleMessage(message.getEntries());
                    }
                    connector.ack(batchId);
                }
            } finally {
                connector.disconnect();
            }
        }
    
        // 解析方法
        private void handleMessage(List<CanalEntry.Entry> entries) {
            try {
                for (CanalEntry.Entry entry : entries) {
                    if (entry.getEntryType() == CanalEntry.EntryType.ROWDATA) {
                        CanalEntry.RowChange rowChange = CanalEntry.RowChange.parseFrom(entry.getStoreValue());
                        CanalEntry.EventType eventType = rowChange.getEventType();
    
                        String tableName = entry.getHeader().getTableName();
                        System.out.println("=== 捕获到变更 ===");
                        System.out.println("表：" + tableName + " | 操作：" + eventType);
    
                        // 简单示例：把更新后的数据写入 Redis
                        ObjectMapper objectMapper = new ObjectMapper();
                        rowChange.getRowDatasList().forEach(rowData -> {
    
                            // 把每一列拼到一个 Map，然后序列化为 JSON 作为 Redis Value
                            java.util.Map<String, String> rowMap = new java.util.HashMap<>();
                            rowData.getAfterColumnsList().forEach(column ->
                                rowMap.put(column.getName(), column.getValue())
                            );
    
                            // 取 id 当作 Redis Key
                            String id = rowMap.get("id");
                            if (id != null) {
                                String redisKey = tableName + ":" + id;
                                String redisValue = null;
                                try {
                                    redisValue = objectMapper.writeValueAsString(rowMap);
                                } catch (JsonProcessingException e) {
                                    throw new RuntimeException(e);
                                }
                                redisTemplate.opsForValue().set(redisKey, redisValue);
                                System.out.println("写入 Redis -> " + redisKey + " = " + redisValue);
                            }
                        });
                    }
                }
            } catch (Exception e) {
                e.printStackTrace();
            }
        }
    }
    ```

![212f49eedbee598b89f60d171142b1b4](https://dasi-blog.oss-cn-guangzhou.aliyuncs.com/Java/202508272315399.png)



## 高级数据结构实践

### 统计类型

| 类型     | 定义                                                   | 场景                   | 指标 |
| -------- | ------------------------------------------------------ | ---------------------- | ---- |
| 聚合统计 | 对数据进行求和、计数、平均值、最大值、最小值等归约操作 | 总交易额、平均交易额   | PV   |
| 排序统计 | 对一组数据按某个指标排序                               | 热搜榜、热卖榜、打赏榜 | TopN |
| 二值统计 | 对数据进行二分类                                       | 签到打卡、每日登陆     | UV   |
| 基数统计 | 统计不同元素的个数                                     | 浏览量、用户数         | DAU  |

### HyperLogLog

HyperLogLog 就**只用来存储一个基数统计结果，而不是存储任何数据**，底层核心是：**基数越大 → 哈希值越稀疏 → 前导 0 越多 → 随机深度越大**

1. 每个元素先通过哈希函数映射为一个 64 位的二进制串
2. Redis 把哈希值的前 14 位作为桶编号，将元素分别落在 $2^{14}=16384$ 个桶中
3. 对元素剩下的 50 位从左往右找到第一个 1 出现的位置，称作随机深度，将该位置记录在桶中
4. 每个桶只会保留一个值，即所有落在该桶中元素的最大随机深度
5. 利用调和平均的方法归约所有桶的值来计算总基数

> 随机深度最大为 50，因此每个桶都只需要 6bit 的长度，一共有 16384 个桶，一共就需要 98304bit = 12288byte = 12KB

### BitMap

BitMap 的底层实际上是 String，这是因为 **String 的本质是字节数组，一个字符对应一个字节即 8bit 来存储**，同时 BitMap 是二进制安全的，它不会去解析这些二进制码究竟是不是字符

- 11111111 即 OxFF 在 ASCII 和 UTF-8 都是不可打印字符，只是显示会乱码，不会报错
- BitMap 的指令可以直接对 String 某个字节的某个位直接操作
- 字节和位都是从 0 开始计数：**offset = byteIndex * 8 + bitIndex**
    - byteIndex = offset / 8
    - bitIndex = offset % 8
- String 可以存 512MB 的数据，也就是 42.9 亿个 bit / 布尔值，如果用 int 则需要 17.2GB，相差了接近 34 倍

### Geo

Geo 的底层**实际上是 ZSET，其中 Member 是地理对象名称，Score 是经纬度经过处理过后的值**，而范围查询实际上是利用 ZSET 的 **ZRANGEBYSCORE** 过滤掉不在指定范围内的点

【插入】

1. 通过 **交替二分法**将经纬度变为 52 位二进制串 GeoHash（奇数位是纬度，偶数位是经度）
2. 计算这个二进制串的**整数值作为 Score**（ 是 double 类型的有 64 位，足够放下）

【查询】

1. 粗略筛选
    1. 根据指定的半径大小选择合适的前缀位长度：**半径越大，精度越低，前缀位越短**
    2. 将 Score 变换回 GeoHash，然后根据前缀位提取出经纬度各自的二进制子串
    3. **将二进制子串 ±1, ±0，先排列组合再拼接**，就得到 9 个 GeoHash 前缀
    4. **在前缀后面补上全 1/0**，然后转换回 Score，就可以得到各自的范围区间 [min, max]
    5. 每个区间都使用 ZRANGEBYSCORE 查询一次
2. 精确筛选
    1. 将这些候选点的 Score 解码回经纬度
    2. **利用 Haversine 公式计算候选点到目标点距离**

> GEO 存在空间失真，不可能做到精确，会出现多查但不会出现少查，而且很快，误差只在米级

### Bloom Filter

【定义】

Bloom Filter 是一种概率型数据结构，底层是一个长度为 m 的 BitMap，主要用于**判断某个元素是否在一个集合中**，常用于黑名单过滤、重复事件过滤

- 布隆过滤器判断在集合里，但其实有可能是不在的
- 布隆过滤器判断不在集合里，那么一定是不在的

【原理】

**哈希的重复性导致了假阳性**

1. 初始时 BitMap 全是 0
2. 存在多个哈希函数 h1,h2,...,hk，每个函数都会把元素映射到 [0, m-1] 的某个索引
3. 将这些索引的位都置为 1
4. 查询的时候，**只要这些索引位都是 1，那么可能存在，但只要存在一个 0，就一定不存在**

> 如果 m 是位数，k 是哈希数，n 是元素数，那么误差近似为 $(1−e^{-\frac{kn}{m}})^k$

【优点】

- 用 bit 数组存储，远小于用 Hash 或 Set
- 插入和查询时间都是 O(k)，而不是 O(n)
- 位数组很适合分布式存储，多机合并时只需要按位操作即可

【缺点】

- 不支持删除，因为一个 bit 可能绑定了很多元素，删除当前元素的同时会影响其他元素
- 必须提前确定预计存储数量才能确定 k 和 m 值，否则元素数量超过预期会大大提升误判率
- 像 HyperLogLog 一样只是存储了一个统计信息，不存储数据本身

【命令】

需要在 Github 下载 RedisBloom 模块，然后在配置文件中导入 `loadmodule xxx.so`

| 命令                       | 功能                                                      |
| -------------------------- | --------------------------------------------------------- |
| BF.RESERVE key rate amount | 创建一个名为 key 的布隆过滤器，并事先指定误判率和元素数量 |
| BF.ADD key value           | 加入元素                                                  |
| BF.EXISTS key value        | 检查元素是否存在                                          |



## Lua

### 定义

Lua 脚本是一种轻量级脚本语言，语法简洁，常用作嵌入式脚本，它可以**将多个 Redis 命令会一次性、原子性执行，避免分布式并发下的竞态条件**

### 语法

```lua
-- 变量
local a = 10
local b = "hello"

-- 条件

if (a > 5) then
    return "大于 5"
else
    return "小于等于 5"
end

-- 循环
for i = 1, 5 do
    a = a + 1
end

-- 命令
redis.call('set', KEYS[1], ARGV[1])
local name = redis.call('get', 'name')

-- 返回
return name
```

### 使用

```redis
EVAL script numkeys key [key ...] arg [arg ...]
```

- script：Lua 代码字符串
- numkeys：表示有多少个 key（用于解析后面的 key 和 arg，防止搞混）
- key [key...]：传入的 key 列表
- arg [arg...]：传入的参数

```redis
SCRIPT LOAD script
```

- 把脚本存到脚本缓存里
- 返回一个 SHA1 校验和，可以看作为脚本的哈希值

```redis
EVALSHA sha1 numkeys key [key ...] arg [arg ...]
```

- 不用再传完整脚本，减少带宽和解析开销
- 必须先执行 `SCRIPT LOAD`



## 分布式锁

### 定义

分布式锁是一种跨进程、跨节点的锁，用来保证在分布式系统中同一资源在同一时间只会被一个节点操作

- **缓存击穿**：只允许一个线程去数据库，其他线程原地等待
- **秒杀库存**：防止多个并发请求导致超卖
- **幂等控制**：防止请求在并发场景下重复执行

分布式锁的要求

| 特性     | 定义                                                 | 否则会导致的问题                               |
| -------- | ---------------------------------------------------- | ---------------------------------------------- |
| 互斥性   | 同一时间只有一个客户端获得锁                         | 并发冲突，数据不一致                           |
| 防死锁   | 锁最终必须被释放                                     | 所有客户端阻塞，资源永远不可访问               |
| 解锁安全 | 只有持有锁的客户端才能释放锁                         | 锁彻底失去意义，任何人都能释放别人的锁         |
| 可重入   | 持有锁的客户端可以再次获取锁，不会被自己阻塞         | 同一个业务流程内部多次调用会被卡死             |
| 可续期   | 在锁快要过期且业务还没执行完毕时，自动延长锁的有效期 | 锁提前释放，其他线程插入进来，导致并发安全失效 |

### 测试框架

>  以下锁都将在这个框架基础上测试

【流程】

1. 在 Mac 上使用 Jmeter 模拟请求洪流，发送到 VM 的 80 端口
2. 在虚拟机上使用 Nginx 将 80 端口的请求转发到 Mac 上的 8080 和 8081 端口
3. 在 Mac 上使用 Terminal 分别在端口 8080 和 8081 启动打包好的 jar 包
4. Java 程序收到请求，对 VM 上的 Redis 进行操作

【虚拟机配置】

```bash
# 关闭防火墙
sudo systemctl disable firewalld
# 允许 Nginx 主动建立网络连接（否则会 502 错误）
sudo setsebool -P httpd_can_network_connect true
```

【Nginx 配置】

```conf
# 命名转发对象为 inventory，并指定其包含的 ip、port、weight
upstream inventory {
    server 192.168.31.174:8080 weight=1;
    server 192.168.31.174:8081 weight=1;
}

# 配置 Nginx 服务
server {
		# 监听 localhost 的 80 端口
    listen 80 default_server;
    server_name localhost;
		
		# 对 /inventory 的请求转发到配置好的 inventory
    location /inventory {
        proxy_pass http://inventory;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
    }
}
```

【application 配置】

```yml
server:
  port: 8080 # 另一个改为 8081

spring:
  data:
    redis:
      host: 172.16.140.128
      port: 6379
      password: jason2004
      lettuce:
        pool:
          max-active: 8
          max-idle: 8
          min-idle: 0
          max-wait: -1ms
```

【JMeter 配置】

![image-20250829090523209](https://dasi-blog.oss-cn-guangzhou.aliyuncs.com/Java/202508290905917.png)

业务方法

```java
private String Sale() {
  	// 获取 Redis 操作对象
    String messgae = "";
    ValueOperations<String, String> ops = stringRedisTemplate.opsForValue();
    // 查询库存
    String result = ops.get(KEY_INVENTORY);
    int last = result == null ? 0 : Integer.parseInt(result);
    // 扣减库存
    if (last > 0) {
        ops.set(KEY_INVENTORY, String.valueOf(--last));
        messgae = port + ": " + "卖出一个商品，库存剩余 " + last + "\n";
    } else{
        messgae = port + ": " + "商品卖完了，库存剩余 " + last + "\n";
    }
    return messgae;
}
```



### 本地锁

只对单机单实例起作用，无法防止多个线程同时进入临界区，做不到全局互斥

- **超卖**：同一个商品卖给了两个客户
- **少卖**：库存扣减与实际请求数量完全不一致

| 方法          | 使用方式                                                     | 特点                                               |
| ------------- | ------------------------------------------------------------ | -------------------------------------------------- |
| synchronized  | 关键字修饰方法或代码块，进入时自动加锁，退出时自动释放       | 简单，但是粒度较粗，无法中断和设置超时，灵活性不足 |
| ReentrantLock | 获取 ReentrantLock 对象 lock，显式调用 lock() 和 unlock() 函数 | 更加灵活，可重入，但需要手动管理                   |

```java
private final Lock reentrantLock = new ReentrantLock();
public String saleByLocalLock() {
    String message = "";
    try {
        reentrantLock.lock();
        message = Sale();
    } catch (Exception e) {
        System.out.println(e.getMessage());
    } finally {
        reentrantLock.unlock();
    }
    System.out.println(message);
    return message;
}
```

### Redis 简易锁

基于 **SET key value NX EX/PX expire** 和 **Lua** 脚本实现

- NX：只有当 key 不存在的时候，才会设置 key 的值，因此只要有一个线程设置了 KEY_LOCK，那么其他现场再去设置就会返回错误，根据这个原理可以设置自旋锁
- EX/PX：设置 key 的过期时间，当持有锁的挂掉时仍然可以通过 Redis 的机制来自动释放锁
- value：需要设置为唯一 id 值，用于在删除 key 的时候判断是否是自己加的锁，因为当业务时间大于过期时间时，锁会被自动释放
- Lua：应该将判断 key 的 value 是否与自己一致和删除 key 的命令合并为一个原子操作，否则高并发下仍然会有窗口期导致键被删除

![8409dd37450b315876775dff8188c6a4](https://dasi-blog.oss-cn-guangzhou.aliyuncs.com/Java/202508291005070.png)

```java
public String saleBySimpleRedisLock() {
    String message = "";
    ValueOperations<String, String> ops = stringRedisTemplate.opsForValue();
    String id = IdUtil.simpleUUID() + ":" + Thread.currentThread().getId();
    try {
        while (!ops.setIfAbsent(KEY_LOCK, id, 1L, TimeUnit.SECONDS)) {
            try {
                TimeUnit.MILLISECONDS.sleep(50);
            } catch (InterruptedException e) {
                Thread.currentThread().interrupt();
            }
        }
        message = Sale();
    } catch (Exception e) {
        System.out.println(e.getMessage());
    } finally {
        if (id.equals(ops.get(KEY_LOCK))) {
            stringRedisTemplate.delete(KEY_LOCK);
        }
    }
    System.out.println(message);
    return message;
}
```

### Redis 进阶锁

- 可重入：如果同一个线程要多次获得锁，那么就需要用一个计数器来统计获得的锁数量，显然 Hash 的 field-value 结构很适合，其中 **field 是线程的唯一标识，value 是线程获得的锁数量**
    1. 先执行 `EXISTS key` 和 `HEXISTS key clientId`  判断线程是否加锁
    2. 如果没锁，才执行 `HSET key clientId` 加锁
    3. 每次获得锁，就执行 `HINCRBY key clientId 1`
    4. 每次释放锁，就执行 `HINCRBY key clientId -1`
    5. 当且仅当释放锁后的返回值为 0，才执行 `DEL key` 解锁

- 可续期：可以在当前线程开启一个后台定时任务
    1. 每隔 `expireTime/3` 执行 `HEXISTS key clientId`，检查是否还持有锁
    2. 如果锁还在当前客户端手里，则执行 `EXPIRE key exp`  续期
    3. 如果锁已经不在自己手里，则停止续期
- 可阻塞：创建自定义类实现 Java 的 Lock 接口，将加锁、解锁机制进行封装，需要重写以下方法
    - `void lock()`：阻塞式加锁，如果拿不到锁会一直等
    - `boolean tryLock()`：非阻塞式加锁，当下拿不到锁立即返回 false
    - `boolean tryLock(long time, TimeUnit unit)`：非阻塞式加锁，规定时间内拿不到锁会返回 false，拿到了返回 true
    - `void unlock()`：解锁

```java
public class RedisLock implements Lock {

    private static final String KEY_LOCK = "lock";              // KEYS[1]
    private final String id;																		// ARGV[1]
    private static final Long expireTime = 30L;                 // ARGV[2]
    private final StringRedisTemplate stringRedisTemplate;

    public RedisLock(StringRedisTemplate stringRedisTemplate, String id) {
        this.stringRedisTemplate = stringRedisTemplate;
        this.id = id;
    }

    @Override
    public void lock() {
        String lockScript =
            "if redis.call('EXISTS', KEYS[1]) == 0 " +
            "or redis.call('HEXISTS', KEYS[1], ARGV[1]) == 1 " +
            "then " +
                "redis.call('HINCRBY', KEYS[1], ARGV[1], 1) " +
                "redis.call('EXPIRE', KEYS[1], ARGV[2]) " +
                "return 1 " +
            "else " +
                "return 0 " +
            "end";
        try {
            while (!stringRedisTemplate.execute(new DefaultRedisScript<>(lockScript, Boolean.class), List.of(KEY_LOCK), id, String.valueOf(expireTime))) {
                TimeUnit.MILLISECONDS.sleep(50);
            }
        } catch (Exception e) {
            e.printStackTrace();
        }

        renewExpire();
    }

    @Override
    public void unlock() {
        String script =
            "if redis.call('HEXISTS', KEYS[1], ARGV[1]) == 0 " +
                "then " +
                "return nil " +
            "elseif " +
                "redis.call('HINCRBY', KEYS[1], ARGV[1], -1) == 0 then " +
                "return redis.call('DEL', KEYS[1]) " +
            "else " +
                "return 0 " +
            "end";

        Long result = stringRedisTemplate.execute(new DefaultRedisScript<>(script, Long.class), List.of(KEY_LOCK), id, String.valueOf(expireTime));
        if (result == null) {
            throw new RuntimeException("Lock Doesn't EXIST");
        }
    }

    private void renewExpire() {
        String script =
            "if redis.call('HEXISTS', KEYS[1], ARGV[1]) == 1 then " +
                "return redis.call('EXPIRE', KEYS[1], ARGV[2]) " +
            "else " +
                "return 0 " +
            "end";

        new Timer().schedule(new TimerTask() {
            @Override
            public void run() {
                if (stringRedisTemplate.execute(new DefaultRedisScript<>(script, Boolean.class), List.of(KEY_LOCK), id, String.valueOf(expireTime))) {
                    renewExpire();
                }
            }
        },(expireTime * 1000) / 3);
    }

    @Override
    public boolean tryLock() {
        throw new UnsupportedOperationException("tryLock not supported");
    }

    @Override
    public boolean tryLock(long time, TimeUnit unit) {
        throw new UnsupportedOperationException("tryLock not supported");
    }

    @Override
    public void lockInterruptibly() throws InterruptedException {
        throw new UnsupportedOperationException("tryLock not supported");
    }

    @Override
    public Condition newCondition() {
        throw new UnsupportedOperationException("tryLock not supported");
    }
}
```

### RedLock

以上的分布式锁足够应付单节点情况，但是如果放到集群之中，存在以下隐患

1. 节点 A 一开始拿到集群的锁 `lock: (idA, 1)`，并写入了 Master
2. Master 突然宕机，锁信息并没有同步到 Slave，某个 Slave 被提升为新的 Master
3. 节点 B 访问 Master，此时发现不存在键 `lock`，因此可以对集群加锁 `lock: (idB, 1)`
4. **节点 A 在执行业务的时候，不会对锁是否存在进行验证，而且它也感知不到提供 Redis 服务的节点是否变化**
5. **节点 A 和节点 B 都认为自己持有锁进行各自的业务，互斥性失效，会导致数据不一致**
6. 节点 A 执行完业务之后尝试解锁会抛出异常

因此 Redis 官方提供了 RedLock 算法来解决这个问题：不依赖于 Redis 的主从复制，而是在 N 个独立的节点上尝试加锁，同时**允许节点残留锁，依靠过期时间来释放锁，即牺牲可用性来保证安全性**

1. 加锁的时候，客户端会向所有 Redis 节点发起加锁请求 `SET key value NX PX exp`，而不是只是向 Master 节点，并且会生成一个全局唯一的随机值作为锁的 value
2. 如果 Redis 统计到加锁成功的节点数多于一半，并且当前耗时小于锁的过期时间，则认为加锁成功，否则会释放已经加锁的节点
3. 解锁的时候，客户端会向所有 Redis 节点发起解锁请求，利用 Lua 脚本来原子地检查 value his 否一致并删除锁
4. 解锁不要求 Redis 统计解锁结果，如果失败将不作任何处理，而是等待锁自然过期释放

### Redisson

Redisson 是一个基于 Redis 的分布式工具框架，是 Redis 的 Java 客户端之一，提供了很多**分布式可重用组件**，包括分布式锁、限流器、计数器等

| 类型                    | 功能                                                  | 适用                       |
| ----------------------- | ----------------------------------------------------- | -------------------------- |
| RLock（可重入锁）       | 类似 ReentrantLock，同一线程可多次加锁                | 单机（实例/集群）          |
| RedLock（红锁）         | 基于多个独立 Redis 节点，需多数节点成功               | 跨机房                     |
| FairLock（公平锁）      | 保证获取锁的顺序与请求顺序一致                        | 排队任务调度               |
| ReadWriteLock（读写锁） | 提供读写分离，多线程可同时读，但写时独占              | 配置中心                   |
| MultiLock（联锁）       | 将多个 RLock 绑定成一个整体，必须全部加锁成功才算成功 | 多资源使用                 |
| Semaphore（信号量）     | 控制同时访问某资源的线程数量                          | 限流、连接池               |
| CountDownLatch（闭锁）  | 等待其他线程完成后再继续执行                          | 并行任务汇总、任务依赖控制 |

```java
public String saleByRedLock() {
    RLock lock1 = r1.getLock(KEY_LOCK);
    RLock lock2 = r2.getLock(KEY_LOCK);
    RLock lock3 = r3.getLock(KEY_LOCK);
    RedissonRedLock redLock = new RedissonRedLock(lock1, lock2, lock3);
    String message = "";
    try {
        redLock.lock(10, TimeUnit.SECONDS);
        message = Sale();
    } catch (Exception ex) {
        ex.printStackTrace();
    } finally {
        redLock.unlock();
    }
    System.out.println(message);
    return message;
}
```



## 三大问题与三大方案

### 穿透 Penetration

**请求查询的数据不在缓存也不在数据库，但是请求会一直绕过缓存打到数据库上，高并发下可能会压垮数据库**

| 方案       | 说明                                                         | 缺陷                                     |
| ---------- | ------------------------------------------------------------ | ---------------------------------------- |
| 布隆过滤器 | 加入存在的 key 到布隆过滤器中，查询前先判断 key 是否可能存在 | 存在误判，而且不支持删除                 |
| 缓存空对象 | 将查询结果为空的数据也写入缓存，赋予一个特殊值 null 并设置短 TTL | 可能导致缓存中存在大量无效数据，占用空间 |

### 击穿 Breakdown

**某个热点 HotKey 在失效的瞬间，大量并发请求同时打到数据库导致崩溃**

| 方案              | 说明                                             | 缺陷                                     |
| ----------------- | ------------------------------------------------ | ---------------------------------------- |
| 热点 key 永不过期 | 物理上不设置过期，由应用管理层控制逻辑过期       | 可能导致缓存和数据库不一致               |
| 定期刷新          | 设置触发器，在 TTL 到期前提前异步刷新缓存        | 需要合理设置刷新频率                     |
| 分布式锁          | 只放一个请求去 DB 加载，其他请求原地等待缓存刷新 | 延迟增加，锁机制复杂，可能会造成额外问题 |

### 雪崩 Avalanche

**大量 key 在同一时间集中失效，或者 Redis 集群整体宕机，导致请求洪峰直接打到数据库导致崩溃**

| 方案     | 说明                                    | 缺陷                                  |
| -------- | --------------------------------------- | ------------------------------------- |
| 随机过期 | 设置 TTL 时加上随机值，错峰过期         | 对 TTL 失去控制，而且仍有概率发生雪崩 |
| 多级缓存 | 本地缓存（Guava） + 第三方缓存（Redis） | 增加开发和运维复杂度                  |

### 限流 Rate Limiting

【定义】强制限制单位时间内的请求数，保护下游数据库不会被击垮

【缺陷】用户需要反复请求来挤入数据库（抢票、查成绩）

### 熔断 Circuit Breaker

【定义】检测下游数据库异常率高时，快速切断当前请求并关闭入口，从而提供恢复时间

【缺陷】用户不得不等待服务恢复（餐厅爆单）

### 降级 Degrade

【定义】在无法提供完整服务时，返回默认数据或旧数据

【缺陷】用户拿到的数据不完整/不实时（双十一显示销量）

> 上述三个方法，都是**当缓存没有办法及时处理和恢复，且请求洪流将要到达下游数据库的情况下**，后端应该做的兜底操作，本质上都是**牺牲一部分用户体验或数据精度，来确保核心功能可用，而不是直接挂掉！**



## 过期策略

### 内存

不设置最大内存大小或者设置为 0 都表示不限制内存大小，理论上可以使用机器的全部物理内存

- 从 Redis 角度看自己使用的内存**只包括实际存储数据、元信息和运行时开销**
- 从操作系统角度看 Redis 使用的内存除了上述的内容，还包括**内存碎片、缓冲区、临时数据结构**等，往往会比前者大，被称为**常驻集大小（RSS，Resident Set Size）**

| 命令                    | 功能                                                         |
| ----------------------- | ------------------------------------------------------------ |
| **INFO MEMORY**         | 查看内存信息，关键字段有<br />- **used_memory_human**：Redis 认为自己正在使用的总内存<br />- **maxmemory_human**：Redis 认为自己可以使用的内存<br />- **used_memory_rss_human**：操作系统实际分配的内存<br />- **mem_fragmentation_ratio**：内存碎片率 |
| **MEMORY DOCTOR**       | 内存健康诊断报告，比如内存不够使用、内存碎片过多             |
| **MEMORY MALLOC-STATS** | 内存分配器的底层统计（操作系统层面）                         |
| **MEMORY PURGE**        | 强制清理脏页，把内存还给 OS                                  |
| **MEMORY STATS**        | 全面内存统计（JSON 格式）                                    |
| **MEMORY USAGE key**    | 返回当前 key 及其 value 所占用的内存字节数                   |

### 删除策略

| 策略               | 定义                                         | 优点         | 缺点                                         |
| ------------------ | -------------------------------------------- | ------------ | -------------------------------------------- |
| 立即删除 immediate | key 一过期就立刻删除                         | 拿时间换空间 | 会阻塞主线程，**对处理器压力最大**           |
| 惰性删除 lazy      | 只有访问的时候发现过期才删除，并返回 null    | 拿空间换时间 | 如果没有被访问则不会删除，**对内存压力最大** |
| 定期删除 periodic  | 周期性地随机抽取一些 key，检查是否过期并删除 | 两者中和     | 需要确定删除的**数量、时长和频率**           |

### 淘汰策略

| 策略 | LRU, Least Recently Used          | LFU, Least Frequently Used        | TTL                             | Random                   |
| ---- | --------------------------------- | --------------------------------- | ------------------------------- | ------------------------ |
| 定义 | 淘汰使用最久的 key                | 淘汰使用最少的 key                | 淘汰存活时间最短的 key          | 随机淘汰 key             |
| 实现 | 给每个 key 维护一个**访问时间戳** | 给每个 key 维护一个**访问计数器** | 给每个 key 维护一个**过期时间** | 调用哈希表的随机采样函数 |
| 性质 | 适合短期热点数据                  | 适合长期热点数据                  | 和业务更贴合                    | 最简单                   |

> 存在三个版本：noeviction（不做任何处理）、volatile（针对有过期时间的 key）、allkeys（针对所有的 key）



## Redis 为什么这么快

### 1. 内存 + 数据结构

Redis 的所有数据都存储在内存，内存读写速度（纳秒级别）远快于磁盘读写（毫秒级别）

Redis 底层不是直接使用 C 语言原生的字符串、数组、链表等，而是根据不同场景量身定做了一套优化数据结构：**SDS、dict、skiplist、listpack、quicklist** 

### 2. 单线程

**核心操作（命令解析+命令执行）都是由一个线程完成**，避免了多线程带来的锁竞争、数据不一致和上下问切换开销，而且在现代 CPU 和内存架构下，单线程足以支撑十万级的 QPS。但实际上，对于整个 Redis 服务是多线程的，主要有**网络 I/O、持久化、惰性删除、内存碎片整理、集群管理**等

![9360babd7ae3e5534688174b6855f8af](https://dasi-blog.oss-cn-guangzhou.aliyuncs.com/Java/202508302356345.png)

### 3. I/O 多路复用

#### 定义与瓶颈

Redis 的 I/O 不是指对硬盘的写入数据与写出数据，而是指**应用程序对网卡的套接字 socket 进行接收请求（read）和发送响应（write）**

I/O 的多路复用指的是**只用一个线程就可以管理成千上万个连接，处理多个 I/O 事件**，性能瓶颈来源于

- **数据拷贝**：读取的网络数据是先到内核缓冲区，应用程序必须通过调用 read() 才能把数据拷贝到用户缓冲区，这就涉及一次内存拷贝和一次上下文切换
- **等待就绪**：如果调用 read() 的时候数据还没到，阻塞 I/O 使得应用程序原地等待数据就绪，非阻塞 I/O 使得应用程序周期性地询问是否到达
- **管理连接**：每个 socket 都对应一个 file descriptor，操作系统需要判断哪个 socket 是可读/可写的

#### Unix 的 I/O 模型

| 模型         | 定义                                                         | 性质                                 |
| ------------ | ------------------------------------------------------------ | ------------------------------------ |
| 阻塞 I/O     | 如果数据没就绪，read() 会一直阻塞，直到数据到达并复制到用户缓冲区 | 最简单，但是效率最低                 |
| 非阻塞 I/O   | 如果数据没就绪，read() 会立刻返回 EAGIAN，应用程序需要不断轮询检查数据是否就绪 | CPU 消耗高                           |
| I/O 多路复用 | 使用系统调用检查套接字/文件描述符，只有可读的才会去 read()   | 能处理大量连接                       |
| 信号驱动 I/O | 当数据就绪时，内核主动通过信号通知应用程序，再由应用程序调用 read() | 信号机制的复杂度非常高，信号可能丢失 |
| 异步 I/O     | 应用程序向内核发起读请求，内核完成 read 工作后通知应用程序直接使用 | 效率最高，但是 Linux 不适用          |

![9b445b475903dd017e4fc72489a00668](https://dasi-blog.oss-cn-guangzhou.aliyuncs.com/Java/202508310028138.png)

#### epoll

【Linux 系统调用】

- epoll_create()：内核会创建一个 epoll 实例，包含一颗存储了所有被监控 fd 的红黑树和一个保存所有已经就绪 fd 的队列，函数会返回当前 epoll 的 epfd
- epoll_ctl(epfd, op, fd, event)：控制 epfd 对应的 epoll 实例，根据传入的 op、fd、event 管理（添加/修改/删除）需要被监控的 fd 及其事件（读、写、异常）
- epoll_wait(epfd, events, maxevents, timeout)：内核会检查 epoll 的就绪队列，如果有事件，就会把 fd 的事件信息存储到 events 数组，没有的话就根据 timeout 阻塞等待（0 立即返回、-1 无限等待）

【Redis 使用流程】

1. 启动初始化
    1. 调用 `epoll_create()` 创建 epoll 实例，得到 epfd
    2. 创建一个监听 socket，得到 listenfd
    3. 调用 `epoll_ctl(epfd, EPOLL_CTL_ADD, listenfd, EPOLLIN)` 注册连接事件
2. 建立连接
    1. 调用 `epoll_wait()` 返回可连接 listenfd
    2. 调用 `accept(listenfd)` 拿到连接
    3. 创建一个服务 socket，得到 clientfd
    4. 调用 `epoll_ctl(epfd, EPOLL_CTL_ADD, clientfd, EPOLLIN)` 注册读事件
3. 处理请求
    1. 调用 `epoll_wait()` 返回可读 clientfd
    2. 调用 `read(clientfd)` 读请求数据
4. 处理响应
    1. 调用 `epoll_ctl(epfd, EPOLL_CTL_MOD, clientfd, EPOLLOUT)` 改为写事件
    2. 调用 `epoll_wait()` 返回可写 clientfd
    3. 调用 `write(clientfd)` 写响应数据
    4. 调用 ``epoll_ctl(epfd, EPOLL_CTL_MOD, clientfd, EPOLLIN)` 改回读事件
5. 断开连接
    1. 调用 `epoll_ctl(epfd, EPOLL_CTL_DEL, clientfd, NULL)` 注销事件
    2. 调用 `close(clientfd)` 释放资源

【底层原理】

- epoll 的红黑树结构能够保证所有增删改查都是 **O(logN)**，特别适合大数据
- epoll 会监控其所有 fd 的状态，**只要某个 fd 发生了变化，epoll 就会把它放入就绪队列**
- redis 在底层会一直循环调用 `epoll_wait` 来获取可以使用的 socket
- 水平触发（**Level Triggered, LT**）：只要 fd 还是“就绪状态”，epoll_wait() 每次都会返回它
- 边缘触发（**Edge Triggered, ET**）：只有当 fd 状态从不可用到可用时，epoll_wait() 才会返回它

```c
// 伪代码
while (!stop) {
    int n = epoll_wait(epfd, events, MAX_EVENTS, timeout);
    for (i = 0; i < n; i++) {
        if (events[i].mask & EPOLLIN) {
            handleRead(events[i].fd);
        }
        if (events[i].mask & EPOLLOUT) {
            handleWrite(events[i].fd);
        }
    }
}
```

【实现对比】

| **特性**        | **select**                                 | **poll**                                   | **epoll**                                    |
| --------------- | ------------------------------------------ | ------------------------------------------ | -------------------------------------------- |
| **数据结构**    | 位图                                       | 数组                                       | 红黑树                                       |
| **最大连接数**  | 1024/2048                                  | 无上限                                     | 无上限                                       |
| **最大支持 fd** | 1024/2048                                  | 65535                                      | 65535                                        |
| **fd 拷贝**     | 每次调用都要把 fd 集合从用户态拷贝到内核态 | 每次调用都要把 fd 集合从用户态拷贝到内核态 | 提前调用 epoll_ctl 拷贝，epoll_wait 不再拷贝 |
| **工作效率**    | O(n) ，每次都要遍历所有 fd                 | O(n) ，每次都要遍历所有 fd                 | O(1) ，直接获取回调到就绪队列的所有 fd       |