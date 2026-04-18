# 部署 ECS



## 1. 配置 ECS

### 1.1 选购套餐

- 云服务器推荐：https://docs.qq.com/document/DV0RCS0lGeHdMTFFV?tab=000003
- 实际采购地址：https://cloud.tencent.com/act/pro/double12-2025

![](https://dasi-blog.oss-cn-guangzhou.aliyuncs.com/Casual/202602151424487.png)

### 1.2 选择系统

- Linux：Ubuntu 22.04 LTS
- Docker：Docker 26.1.3

### 1.3 重新设置登录密码

- 登陆腾讯云的控制台：https://console.cloud.tencent.com/lighthouse/instance/index
- 点击右上角三个点重置密码

<img src="https://dasi-blog.oss-cn-guangzhou.aliyuncs.com/Casual/202602151424488.png" style="zoom: 50%;" />

### 1.4 添加 SSH 密钥

```shell
ssh-keygen -t ed25519 -a 64 -C "ecs"
```

![](https://dasi-blog.oss-cn-guangzhou.aliyuncs.com/Casual/202602151424489.png)



## 2. 配置 Docker

### 2.1 配置镜像地址

```shell
# 是否安装
docker --version
docker compose version
# 是否运行：active / running
systemctl status docker
# 配置仓库镜像地址：registry-mirrors
sudo nano /etc/docker/daemon.json
```

### 2.2 启动 Portainer

Portainer 可以提供 docker 管理的 Web 页面，使得主机可以通过浏览器配置云服务器的 docker

```shell
# 创建数据卷，用于持久化数据到路径：/var/lib/docker/volumes/portainer_data/_data
docker volume create portainer_data
# 拉取镜像
docker pull portainer/portainer-ce:2.19.5
# 创建容器
docker run -d \
  --name portainer \
  --restart=always \
  -p 9000:9000 \
  -p 9443:9443 \
  -v /var/run/docker.sock:/var/run/docker.sock \
  -v portainer_data:/data \
  portainer/portainer-ce:2.19.5
```

### 2.3 登陆 Portainer

- 在控制台的【防火墙】配置规则，允许访问 9443 端口
- 浏览器输入网址：https://ip-address:9443，设置初始用户名和登录密码

![](https://dasi-blog.oss-cn-guangzhou.aliyuncs.com/Casual/202602151424490.png)



## 3. 配置数据库

### 3.1 Docker 拉取镜像

```shell
# 创建外部网络
docker network create infra_net
# 创建数据卷
docker volume create mysql_data
docker volume create redis_data
# 拉取镜像
docker pull mysql:8.4.8
docker pull redis:7.4.7
```

### 3.2 编写 conf 文件

```cnf
# sudo nano /home/ubuntu/docker/conf/mysql/my.cnf
[client]
default-character-set = utf8mb4

[mysql]
default-character-set = utf8mb4

[mysqld]
# 基础网络
bind-address = 0.0.0.0
port = 3306

# 跳过 DNS 反查
skip-name-resolve

# 字符集
character-set-server = utf8mb4
collation-server = utf8mb4_0900_ai_ci

# 时区
default-time-zone = '+08:00'

# 连接
max_connections = 200
max_allowed_packet = 64M

# InnoDB
innodb_file_per_table = 1
innodb_buffer_pool_size = 1G
innodb_flush_log_at_trx_commit = 2

# 临时表
tmp_table_size = 64M
max_heap_table_size = 64M

# SQL 模式
sql_mode = STRICT_TRANS_TABLES,ERROR_FOR_DIVISION_BY_ZERO,NO_ENGINE_SUBSTITUTION

# 慢查询
slow_query_log = ON
long_query_time = 1
log_queries_not_using_indexes = OFF

# 数据目录
datadir = /var/lib/mysql
```

```conf
# sudo nano /home/ubuntu/docker/conf/redis/redis.conf
# 监听地址/端口
bind 0.0.0.0
port 6379

# 保护模式
protected-mode yes

# 密码
requirepass xxxxxxx

# 连接与超时
timeout 0
tcp-keepalive 300

# 数据库数量
databases 16

# 持久化：RDB
save 900 1
save 300 10
save 60 10000
stop-writes-on-bgsave-error yes

# 持久化：AOF
appendonly yes
appendfilename "appendonly.aof"
appendfsync everysec
no-appendfsync-on-rewrite no
auto-aof-rewrite-percentage 100
auto-aof-rewrite-min-size 64mb

# 数据目录
dir /data

# 最大内存策略
maxmemory 512mb
maxmemory-policy allkeys-lru

# 日志不写文件
loglevel notice
logfile ""

# 容器不在后台运行
daemonize no
supervised no
```

### 3.3 编写 compose 文件

```yaml
services:
  # ===================== MySQL =====================
  mysql:
    image: mysql:8.0.40
    container_name: mysql
    restart: unless-stopped
    ports:
      - "3306:3306"
    environment:
      MYSQL_USER: ${USERNAME}
      MYSQL_PASSWORD: ${PASSWORD}
      MYSQL_ROOT_PASSWORD: ${PASSWORD}
      TZ: ${TZ}
    volumes:
      - mysql_data:/var/lib/mysql
      - ./mysql/my.cnf:/etc/mysql/conf.d/my.cnf:ro
      - ./mysql/init.sql:/docker-entrypoint-initdb.d/init.sql:ro
    depends_on:
      - pgvector
    healthcheck:
      test: ["CMD-SHELL", "mysqladmin ping -h localhost -p${PASSWORD} --silent"]
      interval: 5s
      timeout: 10s
      retries: 10
    networks:
      - ai-agent

  # ===================== Redis =====================
  redis:
    image: redis:8.0.1
    container_name: redis
    restart: unless-stopped
    ports:
      - "6379:6379"
    command:
      - redis-server
      - /usr/local/etc/redis/redis.conf
      - --appendonly
      - "yes"
      - --requirepass
      - ${PASSWORD}
    volumes:
      - redis_data:/data
      - ./redis/redis.conf:/usr/local/etc/redis/redis.conf:ro
    healthcheck:
      test: [ "CMD", "redis-cli", "-a", "${PASSWORD}", "ping" ]
      interval: 5s
      timeout: 10s
      retries: 10
    networks:
      - ai-agent
```



## 4. 配置程序环境

### 4.1 安装 git/jdk/maven/nginx/npm/nodejs

```shell
sudo apt update
# git
sudo apt install -y git
git --version
# jdk
sudo apt install -y openjdk-17-jdk
java -version
javac -version
# maven
sudo apt install -y maven
mvn -v
# nginx
sudo apt install -y nginx
nginx -v
# npm
sudo apt install -y npm
npm -v
# nodejs
sudo apt-get install -y ca-certificates curl gnupg
curl -fsSL https://deb.nodesource.com/setup_20.x | sudo -E bash -
sudo apt-get remove -y libnode-dev
sudo apt-get install -y nodejs
node -v
```

### 4.2 配置 Nginx

```conf
server {
    listen 80;
    server_name your.domain.com;   # 示例域名

    # /app -> /app/
    location = /app {
        return 301 /app/;
    }

    # Backend API under /app/api/*
    location /app/api/ {
        proxy_pass http://127.0.0.1:PORT/api/;   # 后端服务端口

        proxy_http_version 1.1;

        # Stream / SSE support
        proxy_buffering off;
        proxy_cache off;
        gzip off;
        proxy_read_timeout 3600s;
        proxy_send_timeout 3600s;

        proxy_set_header Connection "";
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
    }

    # Frontend under /app/*
    location /app/ {
        alias /path/to/frontend/dist/;   # 前端构建产物目录
        try_files $uri $uri/ /app/index.html;
    }
}
```

### 4.3 授予权限

```shell
# 1) 让 nginx(www-data)能穿透进入上级目录（只给执行权限，不开放目录列表）
sudo chmod o+x /home
sudo chmod o+x /home/ubuntu
sudo chmod o+x /home/ubuntu/Agent
sudo chmod o+x /home/ubuntu/Agent/frontend

# 2) dist 目录授权给 www-data 读取
sudo chown -R ubuntu:www-data /home/ubuntu/Agent/frontend/dist
sudo find /home/ubuntu/Agent/frontend/dist -type d -exec chmod 755 {} \;
sudo find /home/ubuntu/Agent/frontend/dist -type f -exec chmod 644 {} \;

# 3) 重载 nginx 并验证
sudo nginx -t
sudo systemctl reload nginx
curl -I http://127.0.0.1/
```



## 5. 域名

### 5.1 解析

在对应厂商的控制台添加解析记录，A 记录用于将域名解析为 IPv4 地址

![](https://dasi-blog.oss-cn-guangzhou.aliyuncs.com/Casual/202602151424491.png)

### 5.2 备案（ICP + 公安）

1. 填写个人基本信息：需要身份证拍照和人脸拍照（不能用照片）
2. 填写网站基本信息：备注需要写清楚不涉及企业信息，项目名称写个人学习项目测试（AI 即可）
3. 填写互联网信息服务备案承诺书：签名 + 手印 + 拍照上传
4. 接受电话进行客服验证：会问姓名、身份证后6位、项目名称，最后进行项目信息的确认
5. 进入工信部网站对校验短信进行核验：注意手机短信，还需要填写手机号和身份证后 6 位
6. 等待管局审核后，进行公安备案：需要主体申请和网站申请
7. 将备案信息的 HTML 代码放到网页底部

<img src="https://dasi-blog.oss-cn-guangzhou.aliyuncs.com/Casual/202602151424492.png" style="zoom:67%;" />

![](https://dasi-blog.oss-cn-guangzhou.aliyuncs.com/Casual/202602151424494.png)

![/](https://dasi-blog.oss-cn-guangzhou.aliyuncs.com/Casual/202602151424495.png)

### 5.3 签发证书

```sh
# 1. 开放端口
sudo ufw allow 80/tcp && sudo ufw allow 443/tcp && sudo ufw reload
# 2. 验证 DNS 生效
dig +short example.com
dig +short www.example.com
# 3. 安装 Certbot
sudo apt install -y certbot python3-certbot-nginx
# 4. 检查是否启用站点
sudo nginx -T | grep -n "server_name"
# 5. 自动配置 SSL 证书
sudo certbot --nginx -d example.com -d www.example.com
# 6. 自动把 HTTP 自动 301 到 HTTPS
sudo certbot --nginx -d example.com --redirect
# 7. 检查是否签发成功
sudo certbot certificates
curl -I http://example.com
curl -I https://example.com
# 7. 重启 Nginx
sudo nginx -t && sudo systemctl reload nginx
```



## 6. 运行项目

### 6.1 拉取Git

```sh
cd ~/Agent
git pull
```

### 6.2 构建前端

```sh
cd ~/Agent/frontend
npm ci
npm run build
```

### 6.3 启动 Docker 容器

```sh
cd ~/Agent/backend/docs/docker
docker compose -f docker-compose.yml up -d
```

### 6.4 初始化数据

```sh
docker exec -i mysql mysql -uroot -pxxxxxx < dump.sql
```

### 6.5 构建后端

```sh
cd ~/Agent/backend
mvn -DskipTests clean package
java -jar ~/Agent/backend/ai-agent-app/target/*.jar --server.address=127.0.0.1 --server.port=8066
```



## 7. 添加基本防护

```sh
# 1. 更改 ssh 配置
sudo tee -a /etc/ssh/sshd_config >/dev/null <<'EOF'
Port xxxxx
PermitRootLogin no
PubkeyAuthentication yes
PasswordAuthentication no
KbdInteractiveAuthentication no
EOF
sudo sshd -t
sudo systemctl restart ssh

# 2. 防火墙放行
sudo ufw default deny incoming
sudo ufw default allow outgoing
sudo ufw allow 80/tcp
sudo ufw allow 443/tcp
sudo ufw allow xxxxx/tcp
sudo ufw delete allow 22/tcp
sudo ufw enable
sudo ufw status verbose

# 3. 装 fail2ban 防爆破
sudo apt update && sudo apt install -y fail2ban
sudo systemctl enable --now fail2ban
sudo tee /etc/fail2ban/jail.local >/dev/null <<'EOF'
[DEFAULT]
bantime = 1h
findtime = 10m
maxretry = 5
backend = systemd
banaction = ufw
ignoreip = 127.0.0.1/8 ::1

[sshd]
enabled = true
port = xxxxx
logpath = %(sshd_log)s
EOF
sudo systemctl restart fail2ban
sudo fail2ban-client status
sudo fail2ban-client status sshd
```







