# RabbitMQ



   * [概述](#概述)
      * [MQ](#mq)
      * [消息中间件](#消息中间件)
      * [Docker](#docker)
   * [体系架构](#体系架构)
      * [交互流程](#交互流程)
      * [交换机模式](#交换机模式)
      * [高可用方式](#高可用方式)
   * [SpringBoot 集成](#springboot-集成)
      * [pom.xml](#pomxml)
      * [application.yml](#applicationyml)
      * [RabbitConfig](#rabbitconfig)
      * [MessageConverter](#messageconverter)
      * [RabbitTemplate](#rabbittemplate)
      * [@RabbitListener](#rabbitlistener)
      * [@QueueBinding](#queuebinding)
   * [消息可靠性](#消息可靠性)
      * [生产者可靠性](#生产者可靠性)
         * [重试连接](#重试连接)
         * [生产者确认](#生产者确认)
         * [备份交换机](#备份交换机)
      * [消息队列可靠性](#消息队列可靠性)
         * [持久化](#持久化)
         * [惰性队列](#惰性队列)
      * [消费者可靠性](#消费者可靠性)
         * [消费者确认](#消费者确认)
         * [失败消息处理](#失败消息处理)
         * [业务幂等性](#业务幂等性)
         * [限流](#限流)
   * [延迟消息](#延迟消息)
      * [死信交换机](#死信交换机)
      * [延迟插件](#延迟插件)
      * [拆分延迟](#拆分延迟)
   * [优先级队列](#优先级队列)
      * [定义](#定义)
      * [队列优先级](#队列优先级)
      * [消息优先级](#消息优先级)



## 概述

### MQ

**消息队列（MQ, Message Queue）是一种异步通信机制，它可以充当系统中的消息缓冲区，允许不同微服务之间通过消息中间件来交互**，核心思想是**利用生产者（Producer）把消息放入队列，利用消费者（Consumer）从队列中取消息**

- **解耦**：生产者和消费者不必直接依赖，可以放在完全不同的微服务和主机，只要约定好消息的格式即可
- **扩展**：可以灵活地增加、修改和删除生产者和消费者，不需要对整个系统框架进行改动
- **异步**：微服务不需要阻塞等待结果，而是直接交给消息中间件来处理
- **削峰**：在高并发场景下，MQ 可以暂存请求，避免数据库和下游服务被流量压垮
- **填谷**：在低并发场景下，MQ 可以处理积压的请求，利用闲置资源，提高整体吞吐率
- **可靠**：MQ 提供持久化和确认机制，保证消息不丢失不重复

![image-20250831111316501](https://dasi-blog.oss-cn-guangzhou.aliyuncs.com/Java/202508311113566.png)

![image-20250831111713832](https://dasi-blog.oss-cn-guangzhou.aliyuncs.com/Java/202508311117880.png)

### 消息中间件

| **对比项** | **RabbitMQ**         | ActiveMQ     | **RocketMQ** | **Kafka**                      |
| ---------- | -------------------- | ------------ | ------------ | ------------------------------ |
| 开发公司   | Pivotal              | Apache       | Alibaba      | Apache                         |
| 开发语言   | Erlang               | Java         | Java         | Java                           |
| 吞吐率     | 中                   | 中           | 高           | 极高                           |
| 延迟       | 微妙                 | 毫秒         | 毫秒         | 毫秒以内                       |
| 典型场景   | 通知、订单、业务解耦 | 传统企业集成 | 金融、电商   | 日志采集、流式计算、大数据处理 |

### Docker

Docker 是一个开源的容器化平台，它本身不是容器，而是**容器引擎和容器运行平台，负责容器的生命周期管理和镜像构建与分发，同时还提供了网络、日志、存储等容器周边服务的支持**

Docker 的核心意义：**从 Docker Hub、私有库、开源网站上直接获取软件的镜像，然后放到 Docker 上自定义运行**，Docker 相当于手机上的 AppStore

- **镜像（Image）**：是一个只读的应用模版，包含了应用程序、依赖库、配置、环境，描述了如何运行这个应用
- **容器（Container）**：是镜像运行起来的实例，本质是一个与外部进程互不影响的隔离进程，但共享宿主内核

| 对比项   | Docker                                                | Virtual Machine                                      |
| -------- | ----------------------------------------------------- | ---------------------------------------------------- |
| 运行对象 | 应用容器 Container                                    | 操作系统 OS                                          |
| 隔离级别 | 进程级隔离，依靠 Namespace + Cgroups 有独立的分配资源 | 硬件级隔离，依靠 Hypervisor 有独立的 CPU、内存和磁盘 |
| 性能     | 启动秒级，轻量                                        | 启动分钟级，重量                                     |
| 典型用途 | 微服务部署                                            | 公有云的多租户                                       |

```dockerfile
# 安装
docker pull rabbitmq:3.13-management

# 开启
docker run \
  -d \                               # 后台运行
  --name rabbitmq \                  # 容器名称
  --hostname rabbitmq \              # 容器主机名
  -v mq-plugins:/plugins \           # 插件目录挂载
  -p 5672:5672 \                     # AMQP 协议端口
  -p 15672:15672 \                   # 管理控制台端口
  -e RABBITMQ_DEFAULT_USER=dasi \    # 设置用户名
  -e RABBITMQ_DEFAULT_PASS=jason \ 	 # 设置密码
  rabbitmq:3.13-management           # 镜像版本
```



## 体系架构

 ### 核心组件

- **Producer**：创建并发送消息（寄信人）
- **Connection**：发送渠道和接收渠道（邮车，一个邮车可以坐多个邮差）
- **Channel**： 发送信道和接收信道（邮差，一个邮差可以负责多个寄信人和收信人）
- **Broker**：消息代理（邮政，集中管理邮局和分拣员）
- **VirtualHost**：消息处理（邮局，分拣工作）
    - **Exchange**：消息路由（邮件分拣员，根据分拣规则把信放入对应收件箱）
    - **Binding**：消息绑定（分拣规则）
    - **Queue**：消息队列（收件箱，可以存储多个收件人的信）
- **Consumer**：接收并解析消息（收信人）

![image-20250831113739240](https://dasi-blog.oss-cn-guangzhou.aliyuncs.com/Java/202508311137314.png)

### 交互流程

1. Producer 和 Consumer 先与 Broker 建立 Connection，并指定 Virtual Host
2. Producer 和 Consumer 都在与 Broker 的 Connection 上创建各自的 Channel
3. Producer 通过 Channel 发送一条 Message 到 Exchange
4. Exchange 根据 Type 和 Binding 决定 Message 应该进入哪个 Queue
5. Consumer 主动从 Queue 中获取 Message，或者 Queue 主动推送 Message 到 Consumer
6. Consumer 确认消息后会发送 ACK 到 Broker

### 交换机模式

**Producer 发送消息到交换机的时候需要指定 RoutingKey，Queue 绑定 Exchange 的时候需要指定 BingdingKey，当且仅当 RoutingKey 和 BingdingKey 匹配，MQ 才会把消息放到匹配的队列中**

| 模式    | 规则                              |
| ------- | --------------------------------- |
| Direct  | 根据 Routing Key 精确匹配         |
| Fanout  | 把消息广播到所有绑定的队列        |
| Topic   | 根据 Routing Key + 通配符模糊匹配 |
| Headers | 根据 Headers 属性匹配             |

### 高可用方式

| 对比   | 集群 Cluster                                                 | 联邦 Federation                                  |
| ------ | ------------------------------------------------------------ | ------------------------------------------------ |
| 范围   | 同机房，同网域                                               | 跨机房，跨网域                                   |
| 同步   | 同步交换机/队列/绑定，但不同步消息内容                       | 同步消息内容，但不同步交换机/队列/绑定           |
| 可用性 | 如果主节点挂了，其他节点可以快速根据元数据恢复 MQ 结构来重启服务 | 如果上游集群挂了，下游集群保存的消息还可以被消费 |
| 缺陷   | 消息会丢失                                                   | 消息有延迟和重复                                 |



## SpringBoot 集成

### pom.xml

```xml
<!-- Spring AMQP + Spring RabbitMQ -->
<dependency>
    <groupId>org.springframework.boot</groupId>
    <artifactId>spring-boot-starter-amqp</artifactId>
</dependency>
```

### application.yml

```yml
spring:
  rabbitmq:
    host: localhost
    port: 5672
    username: dasi
    password: jason2004
    virtual-host: /wyw
```

### RabbitConfig

```java
@Configuration
public class RabbitConfig {
    @Bean
    public Queue queue(){
        return new Queue("queue", true, false, false);
    }

    @Bean
    public DirectExchange directExchange() {
        return new DirectExchange("direct.exchange", true, false);
    }

    @Bean
    public Binding binding() {
      return BindingBuilder
              .bind(queue())
              .to(directExchange())
              .with("direct.key");
    }
}
```

### MessageConverter

```java
@SpringBootApplication
public class Application {
    public static void main(String[] args) {
        SpringApplication.run(Application.class, args);
    }

    @Bean
    public MessageConverter messageConverter() {
        return new Jackson2JsonMessageConverter();
    }
}
```

### RabbitTemplate

```java
public class Producer {
    @Autowired
    private RabbitTemplate rabbitTemplate;

    public void send(String message) {
        rabbitTemplate.convertAndSend("queue", message);
    }
}
```

### @RabbitListener

```java
public class Consumer {
  	// 注入消息字符串
    @RabbitListener(queues = "queue")
    public void receiveString(String message) {
        System.out.println("Receive: " + message);
    }
  
  	// 注入消息对象
    @RabbitListener(queues = "queue")
    public void receiveString(Message message) {
        String body = new String(message.getBody());
				System.out.println("Receive: " + body);
    }
}
```

### @QueueBinding

```java
// 直接写在一起，没有就创建，有就直接使用
@RabbitListener(bindings = @QueueBinding(
    value = @Queue(value = "queue", durable = "true"),
    exchange = @Exchange(value = "direct.exchange", type = ExchangeTypes.DIRECT),
    key = "direct.key"
))
public void receive(String message) {
    System.out.println("Receive: " + message);
}
```



## 消息可靠性

### 生产者可靠性

#### 重试连接

【问题】**生产者和 MQ 之间可能因为网络波动导致连接失败，消息根本发不出去**

【解决】**利用 Spring 自带的 SpringRetry 模块，可以给任何方法和操作加重试机制**

> 需要注意的是重试是阻塞式的，**连接不上不会立马通知到客户端，而是全部重试都失败了才会抛出异常**

```yml
spring:
  rabbitmq:
  	# 连接 MQ 的时候最多等待 1 秒
  	connection-timeout: 1s
  	template:
  		# 重试机制
  		retry:
  			# 开启
  			enabled: true
      	# 初始重试间隔
  			initial-interval: 1000ms
  			# 间隔增长倍数
  			multiplier: 1
  			# 最大重试次数
  			max-attempts: 3
```

#### 生产者确认

【问题】**消息虽然发到 MQ 了，但是可能在 MQ 中出错了**

- 交换机不存在、交换机的类型与绑定的类型不一致、交换机找不到任何一个匹配的绑定
- 消息队列溢出、消息过期、Broker 宕机

【解决】**利用 SpringAMQP 提供的 Callback 确认回调机制，其中 Publisher Confirm 关注消息有没有到达交换机，以及 Publisher Return 关注消息有没有到达队列**

> ack 只是针对 confirm 而不是针对 return，因为 return 的时候消息已经进入了 Exchange，出现错误表明是 MQ 内部的错误，而不是 Producer 的错误

1. 配置 application.yml，开启确认回调机制，**其中 simple 表示同步阻塞等待回执，correlated 表示异步回调接收回执**

    ```yml
    spring:
      rabbitmq:
        publisher-confirm-type: correlated
        publisher-returns: true
    ```

2. 通过 @Bean 返回 RedisTemplate 对象，可以在其中设置对全部消息的全局 Callback

    ```java
    @Configuration
    public class RabbitConfig {
    
        @Bean
        public RabbitTemplate rabbitTemplate(ConnectionFactory connectionFactory) {
            RabbitTemplate rabbitTemplate = new RabbitTemplate(connectionFactory);
    
            // Confirm Callback
            rabbitTemplate.setConfirmCallback((correlationData, ack, cause) -> {
                if (ack) {
                    System.out.println("【全局回调】消息投递成功!");
                } else {
                    System.err.println("【全局回调】消息投递失败：" + cause);
                }
            });
    
            // Return Callback
          	rabbitTemplate.setMandatory(true); // 不丢弃消息
            rabbitTemplate.setReturnsCallback(returned -> {
                String msg = new String(returned.getMessage().getBody());
                Integer replyCode = returned.getReplyCode();
                String replyText = returned.getReplyText();
                String exchange = returned.getExchange();
                String routingKey = returned.getRoutingKey();
                System.err.printf("【全局回调】消息路由失败：" +
                    "msg=%s, replyCode=%d, replyText=%s, exchange=%s, routingKey=%s%n",
                    msg, replyCode, replyText, exchange, routingKey);
            });
    
    
            return rabbitTemplate;
        }
    }
    ```

3. 发送消息时，可以对每个消息关联一个局部 Callback

    ```java
    CorrelationData cd = new CorrelationData("msg-001");
    
    cd.getFuture().addCallback(result -> {
        if (result.isAck()) {
            System.out.println("【单条回调】msg-001 投递成功！");
        } else {
            System.err.println("【单条回调】msg-001 投递失败，原因：" + result.getReason());
        }
    }, ex -> {
        System.err.println("【单条回调】msg-001 出现异常: " + ex.getMessage());
    });
    
    rabbitTemplate.convertAndSend("my.direct", "my.key", "hello", cd);
    ```

#### 备份交换机

【问题】**消息投递到了 Exchange，但是没有任何 Queue 和它匹配，比如 RoutingKey 错误、没有 Binding**

【解决】**可以在声明 Exchange 的时候，指定一个 Alternate Exchange，让路由失败的消息投递到备份交换机**

```java
@Bean
public DirectExchange backupExchange() {
    return new DirectExchange("backup.exchange", true, false);
}

@Bean
public DirectExchange directExchange() {
    return ExchangeBuilder.directExchange("direct.exchange")
            .durable(true)
            .alternate("backup.exchange")
            .build();
}
```

### 消息队列可靠性

#### 持久化

【问题】**默认情况下，MQ 会把消息存在内存之中，如果主机宕机，那么内存中的数据会丢失**

【解决】**依靠创建交换机/队列/消息的时候都开启持久化**

```java
Message message = MessageBuilder
        .withBody("hello world".getBytes())
        .setDeliveryMode(MessageDeliveryMode.NON_PERSISTENT)
        .build();
```

#### 惰性队列

【问题】**如果队列中的消息数量太多，会把内存耗尽，导致内存溢出甚至 MQ 崩溃**

【解决】**MQ 提供 Page Out 机制，会自动把老旧数据加载到磁盘的临时文件中**

> 这些临时文件在 MQ 重启的时候会被删除，因此不等于持久化

```java
// 在配置类中创建
@Bean
public Queue lazyQueue() {
    return QueueBuilder.durable("lazy.queue")
            .withArgument("x-queue-mode", "lazy") // 开启惰性模式
            .build();
}

// 在消费者上创建
@RabbitListener(queuesToDeclare = @Queue(
        value = "lazy.queue",
        durable = "true",
        arguments = @Argument(name = "x-queue-mode", value = "lazy")
))
public void receive(String msg) {
    System.out.println("收到惰性队列消息：" + msg);
}
```

### 消费者可靠性

#### 消费者确认

【问题】**如果消息本身的内容错误、业务代码异常或消费者宕机，消费消息算失败**

【解决】**SpringAMQP 提供了三种配置模式来发送三种类型回执**

- 回执类型
    - ack：消费成功，可以从队列中删除消息
    - nack：消费失败，需要从队列中重新获取消息
    - reject：消费错误，直接从队列中删除消息
- 回执模式
    - none：只要到达消费者就 ack
    - manual：需要在代码中手动调用 API
    - auto：正常执行完毕返回 ack，业务异常返回 nack，消息错误返回 reject

```yml
spring:
	rabbitmq:
		# 消费者确认机制
    listener:
      simple:
        acknowledge-mode: auto				# 消费者确认模式：none/auto/manual
        prefetch: 1										# 每次预取一条消息
        retry:												# 利用 SpringRetry 模块
          enabled: true								# 开启重试机制
          initial-interval: 1000ms		# 重试间隔
          multiplier: 1								# 间隔增长倍数
          max-attempts: 3							# 最大重试次数
          stateless: true							# 是否需要事务回滚
```

#### 失败消息处理

【问题】**如果重试都失败了，那么需要对失败消息进行处理**

【解决】**SpringAMQP 提供了三种 MessageRecoverer 来处理失败消息**

- **RejectAndDontRequeueRecoverer**：直接 reject 消息，不再重新入队，或者投递到死信交换机，消息内容丢失（⚠️）
- **ImmediateRequeueMessageRecoverer**：立即 nack 消息，重新入队，可能导致无限重试（❌）
- **RebulishMessageRecoverer**：把消息发送到指定的交换机，然后由交换机发送到专门的错误队列（✅）

```java
@Configuration
public class ErrorRecoverer {
    @Autowired
    private RabbitTemplate rabbitTemplate;

    @Bean
    public Queue errorQueue() {
        return new Queue("error.queue", true, false, false);
    }

    @Bean
    public DirectExchange errorExchange() {
        return new DirectExchange("error.exchange", true, false);
    }

    @Bean
    public Binding errorBinding() {
        return BindingBuilder.bind(errorQueue()).to(errorExchange()).with("error.key");
    }

    @Bean
    public MessageRecoverer messageRecoverer() {
        return new RepublishMessageRecoverer(rabbitTemplate, "error.exchange", "error.key");
    }
}
```

#### 业务幂等性

【问题】同一个业务请求可能因为某些原因发送了多次，消费者应该只执行一次业务，对数据进行一次修改

【解决】给每条消息带上一个唯一业务 ID，然后维护一张幂等表来记录已经处理过的业务 ID，每次执行业务前先查表

```java
@Component
public class IdempotentChecker {
    @Autowired
    priavte StringRedisTemplate redisTemplate;

    public boolean check(String messageId) {
				Boolean exist = redisTemplate.opsForValue()
        		.setIfAbsent("msg:" + messageId, "1", 10, TimeInit.MINUTES);
      	return Boolean.TRUE.equals(exist);
    }
}
```

#### 限流

【问题】默认情况下，RabbitMQ 会尽可能地把队列里的所有消息都推送给消费者，而消费者的处理能力是有限的，可能会导致消息都堆积在内存中

【解决】SpringAMQP 提供了 `prefetch` 参数来配置消费者的预取数，即同一时刻消费者最多能处理的消息数量，当前仅当上一批消息全部都处理完毕后（ack/nack/reject 都算处理），才会分配下一批消息

```yml
spring:
  rabbitmq:
    listener:
      simple:
        prefetch: 1
      	acknowledge-mode: auto
```



## 延迟消息

### 死信交换机

死信：**在队列中因为某些原因没有被正常消费的消息**，而被 MQ 投递到死信交换机的消息

- 消费者调用 `basic.reject()` 或 `basic.nack()` 且参数 `requeue=false`
- 消息在队列中过期了仍没有被消费（可以给消息设置，也可以给队列设置，取决于谁更小）
- 如果队列满了，可能会导致最早的消息溢出

死信交换机（DLX, Dead Letter Exchange）本质上和普通交换机没有任何区别，只不过 **DLX 是在创建队列时需要被绑定的**，并且由 MQ 自动触发投递，**不是直接实现延迟，而是间接利用 TTL 实现延迟，可能与 TTL 的逻辑冲突**

```java
// 绑定 DLX 和 Queue
@Bean
public Queue queue() {
    return QueueBuilder.durable("normal.queue")
            // 指定死信交换机
            .withArgument("x-dead-letter-exchange", "dlx.exchange")
            // 指定死信路由键
            .withArgument("x-dead-letter-routing-key", "dlx.key")
      			// 指定过期时间（可选）
      			.withArgument("x-message-ttl", 5000)
            .build();
}

// 设置消息的 Expiration 属性
rabbitTemplate.convertAndSend("direct.exchange", "direct.key", message, processor-> {
    processor.getMessageProperties().setExpiration("5000");
    return processor;
});
```

### 延迟插件

RabbitMQ 官方提供了一个延迟插件 `rabbitmq_delayed_message_exchange`，**原理是创造一个延迟交换机，到达指定时间后才发送到队列**

1. 安装插件

    ```bash
    # 在宿主机下载插件
    wget https://github.com/rabbitmq/rabbitmq-delayed-message-exchange/releases/download/v3.13.0/rabbitmq_delayed_message_exchange-3.13.0.ez
    
    # 拷贝到容器的插件目录
    docker cp rabbitmq_delayed_message_exchange-3.13.0.ez rabbitmq:/opt/rabbitmq/plugins/
    
    # 在容器里启用插件
    docker exec -it rabbitmq rabbitmq-plugins enable rabbitmq_delayed_message_exchange
    
    # 重启容器
    docker restart rabbitmq
    
    # 观察插件列表，如果状态是 [E*] 表示成功
    docker exec -it rabbitmq rabbitmq-plugins list
    ```

2. 开启 Exchange 的 delayed 属性

    ```java
    @Bean
    public DirectExchange delayedExchange() {
        return ExchangeBuilder.directExchange("delayed.exchange")
                .delayed()
                .durable(true)
                .build();
    }
    ```

3. 设置消息的 DelayLong 属性

    ```java
    rabbitTemplate.convertAndSend("delayed.exchange", "delayed.key", message, processor -> {
        processor.getMessageProperties().setDelayLong(5000L);
        return processor;
    });
    ```

### 拆分延迟

| 情况         | 流程                                                         | 效果                                                         |
| ------------ | ------------------------------------------------------------ | ------------------------------------------------------------ |
| 单个延迟消息 | 下单时直接发送一条 30 min 的延迟消息 → 如果没有支付，则删除订单 | 如果短时间内有大量订单，那么交换机会积压很多延迟消息，可能导致内存溢出 |
| 拆分延迟消息 | 下单时先发送一条 5min 的延迟消息 → 如果没有支付，可以发送平台提醒到客户端，然后发送一条 5min 的延迟消息 → 如果没有支付，可以发送短信提醒到客户端，最后再发送一条 20 min 的延迟消息 → 如果没有支付，则删除订单 | 大部分订单在短时间内就被支付，后续延迟消息就不会再发，减少 MQ 长时间堆积，系统更高效 |



## 优先级队列

### 定义

**传统队列是遵循 FIFO 特性**，而在一特特定场景，消息比如告警通知应该被优先处理，RabbitMQ 给消息和队列都提供了优先级属性，值越大越优先，**允许消息在特定的队列中插队**

### 队列优先级

- 只有设定了大于 0 的值才算开启优先级队列，**否则哪怕消息有优先级也不生效**
- 设定的值表示允许的最大消息优先级值，**如果消息优先级超过该值会被截断到最大值**，因此所有超过该值的消息都属于同一优先级

```java
@Bean
public Queue priorityQueue() {
    return QueueBuilder.durable("priority.queue")
            .maxPriority(10)
            .build();
}
```

### 消息优先级

设置消息的 Priority 属性（0-255），官方推荐最大使用 5-10

```java
rabbitTemplate.convertAndSend("priority.exchange", "priority.key", message, processor -> { 
  	processor.getMessageProperties().setPriority(5);
    return processor;
});
```