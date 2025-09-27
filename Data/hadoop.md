# Hadoop



* [Hadoop](#hadoop)
   * [Hadoop 概念](#hadoop-概念)
   * [Hadoop 组成](#hadoop-组成)
      * [HDFS](#hdfs)
      * [Yarn](#yarn)
      * [MapReduce](#mapreduce)
      * [关系/整体流程](#关系整体流程)
   * [大数据技术生态体系](#大数据技术生态体系)
      * [数据来源层（Source）](#数据来源层source)
      * [数据传输层（Ingestion）](#数据传输层ingestion)
      * [数据存储层（Storage）](#数据存储层storage)
      * [资源管理层](#资源管理层)
      * [数据计算层](#数据计算层)
      * [任务调度层](#任务调度层)
      * [业务模型层](#业务模型层)



## Hadoop 概念

什么是hadoop：是分布式系统基础架构，是一个技术生态圈，主要解决海量数据的存储、分析和计算

hadoop优势
- 高可靠性：底层维护多个数据副本，即使某个计算元素或存储出现故障，也不会导致数据的丢失
- 高扩展性：在集群间分配任务数据，可动态地增加或减少节点
- 高效性：并行工作，加快任务处理
- 高容错性：能够自动将失败的任务重新分配

hadoop版本
- hadoop 1.x：Common 辅助工具 + HDFS 数据存储 + MapReduce 计算-资源调度 + JobTracker 资源管理
- hadoop 2.x：Common 辅助工具 + HDFS 数据存储 + Yarn 资源调度 + MapReduce 计算 + ResourceManager/NodeManager 资源管理
- hadoop 3.x：核心组件与 hadoop 2.x 近似，但是支持多个 NameNode，对环境要求更广泛



## Hadoop 组成

### HDFS

分布式文件系统（Hadoop Distributed File System, HDFS）：存储大规模数据它将大文件分割成多个数据块，然后分布式地存储在多台机器上
- NameNode：管家，记录文件的元数据，如文件名、文件目录结构、文件属性，以及每个文件的块列表和块所在的 DataNode
- DataNode：搬运工，在本地文件系统存储文件块数据，以及块数据的校验和，并定期向 NameNode 汇报状态
- Secondary NameNode：每隔一段时间对NameNode的关键部分进行备份，防止NameNode挂掉

### Yarn

又一个资源调度器（Yet Another Resource Negotiator, YARN）：统一管理集群资源，并调度分布式应用程序的运行
- ResourceManager：整个集群的老大，全局资源分配和调度的控制中心
- NodeManager：单个节点的老大，汇报本地资源使用并管理任务容器
- ApplicatinonMaster：单个任务/应用的老大，负责协调该应用在集群中的执行
- Container：资源容器，封装了任务运行的资源（内存、CPU、磁盘、宽带等），是Application执行的地方

需要说明的是
1. 集群可以支持多客户端访问
2. 集群上可以运行多个ApplicatinonMaster
3. 每个NodeManager可以有多个Container
4. ApplicatinonMaster可以利用其它节点的Container执行

### MapReduce

分发汇总（MapReduce）：是分布式计算模型，适用于大数据的批量处理
- Map：接收输入数据，应用用户定义的 map 函数，输出一组中间 <key, value> 对
- Shuffle：负责根据 key 进行聚合，把所有相同 key 的中间值发给同一个 Reduce 任务
- Sort：可选的操作，对 key 或者 key 组内的 value 进行排序
- Reduce：接收一个 key 和这个 key 对应的一组 value，应用用户定义的 reduce 函数，输出最终结果

### 关系/整体流程

1. 用户上传数据到集群，HDFS 的 NameNode 接收请求并决定将文件切分成若干数据块，并将每块数据复制三份，分配给不同的 DataNode 存储，DataNode 接收分配的数据块并写入本地磁盘
2. 客户端提交一个 MapReduce 作业到 YARN 集群，ResourceManager 接收任务，并先分配一个 Container 来运行 ApplicationMaster，ApplicationMaster 启动后会向 NameNode 查询数据块的位置，然后根据数据的物理分布，将 Map Task 安排在合适节点上
3. ApplicationMaster 根据任务需要向 ResourceManager 请求执行 Map 和 Reduce 任务所需的 Container，ResourceManager 决定在哪些节点上分配资源，并通知对应节点的 NodeManager 启动 Container 以运行实际任务
4. 每个节点的 NodeManager 会监听 ResourceManager 的请求，启动本机上的 Container，同时 NodeManager 会监控 Container 的运行情况，并向 ResourceManager 和 ApplicationMaster 定期心跳
5. Container 启动后执行具体的 Map 或 Reduce 任务Map Task 输出中间结果，Reduce Task 汇总处理后将最终结果通过 HDFS 写入系统此时，NameNode 会负责输出文件的块分配规划，具体数据则由对应的 DataNode 接收并写入磁盘
6. 最后 ApplicationMaster 向 ResourceManager 报告任务完成，自我终结，同时所有 Container 被关闭，NodeManager 回收资源



## 大数据技术生态体系

### 数据来源层（Source）

数据接入的起点，负责从各类业务系统、设备或外部渠道中采集原始数据

- **结构化数据**：具有固定模式和字段定义，适合建模与存储在关系型数据库中，例如 Excel 表格、MySQL 表
- **半结构化数据**：格式灵活但具备可识别标签，如 JSON、XML、日志文件，可通过解析转化为结构化数据
- **非结构化数据**：无固定格式，包含大量潜在信息，如文本、图像、音频、视频等，需借助 AI 技术提取特征
  
### 数据传输层（Ingestion）


数据的搬运工，负责将源数据稳定、高效地采集并传输至数据平台，支持批处理与实时处理场景

- **Sqoop**：用于结构化数据在关系型数据库与 HDFS/Hive 之间的批量同步
- **Flume**：擅长实时采集日志类数据，支持非结构化或半结构化数据流入
- **Kafka**：分布式高吞吐消息队列，广泛用于构建实时数据管道，支撑流处理架构

### 数据存储层（Storage）

数据的落脚点，负责对采集到的数据进行持久化存储，并根据使用场景进行分层管理

- **HDFS**：分布式文件系统，适用于海量数据的离线存储，支持大文件批处理
- **Hive**：基于 HDFS 构建的数据仓库，提供类 SQL 查询能力，适用于分析型处理
- **HBase**：分布式列式数据库，支持高并发访问和随机读写，适合实时数据存储场景

### 资源管理层

数据的管理者，负责统一协调 CPU、内存等资源的分配与监控，确保系统运行稳定高效

- **YARN**：Hadoop 生态的资源调度平台，支持 MapReduce、Spark 等任务框架调度
- **Kubernetes**：面向容器化部署的调度平台，支持自动伸缩、自愈和多框架并发运行

### 数据计算层

数据的打工人，负责对数据进行清洗、转换、建模与分析，是实现数据价值的核心环节

- **MapReduce**：Hadoop 原生批处理框架，容错性强，适用于离线数据处理
- **Flink**：原生流式计算框架，支持低延迟、高吞吐的数据处理，适合实时分析与事件检测
- **Spark**：内存计算引擎，兼容批处理和流处理，支持 SQL 查询、机器学习与图计算等多样任务

### 任务调度层

数据的沟通员，负责作业的定时调度、依赖控制、失败重试等流程管理，保障作业链的自动化运行

- **Oozie**：Hadoop 原生调度器，支持复杂作业流和时间窗口控制
- **Azkaban**：轻量级调度工具，支持任务依赖与失败恢复，配置简单
- **Cron**：用于单机或轻量环境中的定时任务管理，适用于基础调度需求

### 业务模型层

数据的利用者，负责将计算层输出的分析结果、指标数据、预测模型等进行业务化封装与服务化呈现，驱动其它项目落地

![alt text](image.png)











推荐系统案例：

环境准备
1. 虚拟机
2. 克隆
3. JDK+Hadoop

生产集群搭建
1. 本地模式
2. 完全分布式集群

常见错误的解决方案