---
title: Git基本操作
tags:
  - Git
categories:
  - 笔记
cover: /image/git.png
description: 介绍git的基本操作以及对git指令的理解
abbrlink: f11dbe61
swiper_index: 4
date: 2024-09-13 14:41:58
---
<meta name="referrer" content="no-referrer"/>

## 1. 什么是Git？

Git是一种**分布式版本控制系统**，广泛用于协作开发、版本管理和分支管理
- **协作开发**：每个开发者在本地都有完整的仓库，可以从远程仓库拉取最新更新到本地仓库，也可以提交本地仓库的修改到远程仓库
- **版本管理**：Git记录了项目的每一次更改，并可以通过查看历史记录比较差异和文件恢复
- **分支管理**：Git支持开创多个独立的工作线，运行开发者在分支进行开发、测试和修复，将项目发布在主分支（master或main）

{% note info flat %}
Git本义其实是饭桶、傻瓜的意思，创始人林纳斯·托瓦兹（Linus Torvalds）想说哪怕是傻瓜都可以使用git实现分布式版本控制
后人将“Git” 解释为 “Global Information Tracker” ，即全球信息追踪器，一定程度上蕴含了Git的功能，但这并不是命名的真实意图
{% endnote %}

## 2. Git原理

【Git仓库（Repository）】
- **远程仓库**：托管在网络服务器上的Git仓库（Github或Gitee），用于开源共享和协作开发
- **本地仓库**：托管在开发者个人计算机上的Git仓库，包含项目的所有文件及其版本历史记录

【Git的四个区】
- **工作区/本地库**：存放项目的本地副本，是编辑文件的地方
- **暂存区**：暂时存放你准备提交的修改
- **版本库**：保存了项目的所有提交记录，即项目的所有版本历史
- **远程库**：托管在网络服务器上的Git仓库

![](https://dasi-blog.oss-cn-guangzhou.aliyuncs.com/Gitee/202409181327357.png)

## 3. Git操作

### 3.1 Git安装

git安装网上很多教程，这里推荐这个链接
{% link Git安装教程（超详细）,Fun_Rock,https://blog.csdn.net/qq_45281589/article/details/134650456 %}

### 3.2 SSH

**SSH（Secure Shell）**：安全外壳协议，提供了对计算机的加密连接，确保数据在传输过程中的机密性和完整性，主要用于**远程登录、文件传输和命令执行**

【SSH的认证】

|方法|方式|适用|性质|
|-|-|-|-|
|密码（password）|用户提供用户名和密码给服务器来验证身份|临时访问|每次都需要输入，麻烦|
|密钥（secret key）|私钥存储在本地，公钥存储在服务器|长期访问|配置好之后免密登录，私钥不容易泄露|

【SSH的认证流程】

1. **生成SSH密钥对**：`-t rsa`指定密钥类型为RSA，`b 4096`指定密钥长度为4096位，`-C your_email`为密钥添加邮箱参数
```bash
ssh-keygen -t rsa -b 4096 -C your_email
```
{% note warning flat %}
your_email是在github或gitee注册时用的邮箱！
{% endnote %}

2. **按提示操作**
   1. 输入文件保存位置：可以自己设置路径，默认是保存在`c/Users/DELL/.ssh`
   2. 输入私钥访问密码
   3. 确认私钥访问密码

3. **复制公钥**：切换到路径下的目录，复制公钥文件`id_rsa.pub`内容

4. **添加公钥**：在github或gitee中的个人设置中添加公钥（标题可以写笔记本电脑的名字，用于标识此电脑）
![](https://dasi-blog.oss-cn-guangzhou.aliyuncs.com/Gitee/202409111429264.png)

5. **测试SSH连接**
```bash
ssh -T git@gitee.com
ssh -T git@github.com
```

### 3.3 配置

1. **配置本地的用户名和邮箱**：帮助客户端身份被Gitee/Github服务器正确识别
```bash
git config --global user.name your_name
git config --global user.email your_email
```
{% note success flat %}使用命令`git config --list`可以查看配置信息{% endnote %}

2. **初始化Git仓库**
```bash
cd path_to_your_project
git init
```
{% note success flat %}
会创建一个名为`.git`的子目录，需要设置`显示隐藏的项目`才能看到
{% endnote %}

3. **连接到远程仓库**：引用名是可选的，默认是origin，哪怕自定义了远程仓库引用名，origin依然保留
```bash
git remote add 引用名 远程仓库URL
```
{% note success flat %}
可以通过`git remote -v`或`git remote show`来查看连接信息
{% endnote %}

### 3.4 获取

#### 3.4.1 获取整个仓库

**克隆仓库**：将远程仓库完整地克隆到本地，如果本地存在同名文件或文件夹会报错，因此这个方法适用于**最初在空文件夹中获取远程仓库**
```bash
git clone 远程URL
```

{% note warning flat %}
后台会自定建立一个本地仓库和远程仓库的连接！不再需要先前的手动连接！
{% endnote %}

#### 3.4.2 获取最新更改

**拉取仓库**：从远程仓库的分支拉取最新的更改到本地仓库（注意**合并冲突**）
```bash
git pull 引用名 分支名
```

{% note warning flat %}
本地仓库和远程仓库必须存在连接才能使用该命令
{% endnote %}

### 3.5 发布

1. **修改**：在本地添加、删除和编辑文件

2. **上传**：将工作区的修改上传到暂存区（第一个针对全部文件，第二个是指定文件或文件夹）
```bash
git add .
git add path-to-file
```

3. **提交**：将暂存区的修改提交到到版本库
```bash
git commit -m 声明内容
```
{% note warning flat %}`-m 声明内容`是必须的！这符合协作开发时每个人都清楚知道文件更改详情的原则！如果不使用`-m`选项会自动进入Vim编辑器，十分不好用{% endnote %}

4. **推送**：将分支版本库的修改推送到远程仓库的分支
```bash
git push 引用名 分支名
```
{% note warning flat %}分支名是远程仓库的分支名，不是本地仓库的{% endnote %}

### 3.6 撤销

**软撤销**：撤销最近n次提交，但是**保留更改在工作区**，以便**修改提交声明**
```bash
git reset --soft HEAD~n
```

**硬撤销**：撤销最近n次提交，并且**丢弃工作区的所有更改**，以便**回到历史版本，重新修改文件**
```bash
git reset --hard HEAD~n
```

**撤销推送**：撤销已经推送的提交，回到之前版本，以便**回到本地仓库的历史版本进行新一次的工作流**
```bash
git revert commit-hash -m 声明内容
```
{% note success flat %}
虽然只使用`git revert`不会撤销远程仓库的修改，但会自动**创建一个撤销的提交**，此时使用`git push`即可实现撤销对远程仓库的修改
**commit-hash**提交的哈希值可以通过`git log`指令查看
{% endnote %}

### 3.7 分支操作

**查看本地分支**
```bash
git branch
```

**查看远程分支**
```bash
git branch -r
```

**新建分支**
```bash
git branch name
```
{% note warning flat %}
在本地新建的分支，跟远程的分支一点关系都没有！
{% endnote %}

**分支重命名**
```bash
git branch -m old-name new-name
```

切换分支
```bash
git switch name
git checkout name
```
{% note warning flat %}
switch只有2.23或更高版本的Git才可以使用，可以使用`git --version`查看当前git版本
{% endnote %}

**删除分支**
```bash
git branch -d name
```
{% note warning flat %}
不能删除当前分支
{% endnote %}

### 3.8 引用名操作

**添加引用名**
```bash
git rmeote add name 远程库URL
```

**修改引用名**
```bash
git remote rename old-name new-name
```

**删除引用名**
```bash
git remote remove name
```

**查看全部引用名**
```bash
git remote show
```

**查看引用名的具体信息**
```bash
git remote show name
```

### 3.9 四个区的操作（进阶）

**查看版本库的提交信息**：提交的哈希值，作者信息，提交日期和提交的简短说明
```bash
git log
```

**查看暂存区状态**：列出了有几个本地提交尚未推送到远程仓库，并显示哪些更改已被添加到暂存区，哪些更改还在工作区
```bash
git status
```

**查看暂存区和版本库的差异**：每次使用`git add`都会**更新暂存区**的修改，而版本库只保留**最后一次提交**的修改，使用以下指令可以审查和比较代码的变化
```bash
git diff --cached
git diff --staged
```
{% note info flat %}实际上，diff的用法还有很多，既可以比较指定版本的差异，还可以比较分支的差异，甚至可以通过选项来设置比较手段，可以查阅相关资料{% endnote %}

**拉取远程库到版本库**：从远程仓库下载最新更改到版本库，但**不合并这些更改到当前工作分支**
```bash
git fetch 引用名 分支名
```

**拉取版本库到本地库**：合并指定分支到当前分支
```bash
git merge 引用名/分支名 -m 声明内容
```
{% note danger flat %}在合并之前，不允许对本地库进行未提交的更改，否则会造成合并冲突{% endnote %}

### 3.10 通用

实际上，如果只是单纯的获取和提交，使用到的指令可能只有这几个：
1. 获取更新：`git pull 引用名 master`
2. 上传修改：`git add .`
3. 提交修改：`git commit -m 声明`
4. 推送修改：`git push 引用名 master`

## 4. Pull Request

待更

## 5. 参考链接

{% link Git,极客教程,https://geek-docs.com/git %}