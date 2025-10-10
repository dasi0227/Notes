# Shell



   * [基本概念](#基本概念)
      * [Shell 命令行解释器](#shell-命令行解释器)
      * [Shell 脚本](#shell-脚本)
   * [脚本命令](#脚本命令)
      * [执行方式](#执行方式)
      * [内建命令](#内建命令)
      * [输入输出机制](#输入输出机制)
   * [变量](#变量)
      * [使用](#使用)
      * [替换机制](#替换机制)
      * [字符串操作](#字符串操作)
      * [算术运算](#算术运算)
   * [数组](#数组)
      * [定义](#定义)
      * [访问](#访问)
      * [修改](#修改)
      * [关联数组](#关联数组)
   * [运算符](#运算符)
      * [数值相关](#数值相关)
      * [字符串相关](#字符串相关)
      * [文件相关](#文件相关)
   * [流程控制](#流程控制)
      * [if](#if)
      * [case](#case)
      * [while](#while)
      * [for](#for)
   * [函数](#函数)
      * [定义](#定义)
      * [传参处理](#传参处理)
      * [返回值处理](#返回值处理)



## 基本概念

### Shell 命令行解释器

Shell 命令行解释器是用户和操作系统内核交互的接口，负责接收用户在终端输入的命令并解析，然后调用系统程序去执行命令，最后将执行结果返回给用户终端。

Shell 只是一个技术或者说是概念，本质上是一个可以执行的程序/在系统中运行的进程，具有多种实现

| **名称** | **所属系统** | **输出类型** | **核心定位** |
| ---------- | ------------ | ----------- | --------------------------- |
| **bash** | Linux | 字符串流 | 标准命令行与脚本解释器 |
| **zsh** | macOS | 字符串流 | bash 的增强版，交互体验更强 |
| **PowerShell** | Windows | .NET 对象流 | 面向对象的系统自动化平台 |

### Shell 脚本

Shell 脚本是一组命令的集合，既可以包含内建命令，也可以包含外部命令，都写在一个后缀为 `.sh` 的文本文件中，由 Shell 命令行解释器按顺序一次性批量执行

| **维度** | **脚本（Script）** | **程序（Program）** |
| ------------ | ------------------------- | ------------------------ |
| **执行方式** | 解释执行，逐行翻译执行 | 编译执行，生成可执行文件 |
| **运行效率** | 低 | 高 |
| **编写难度** | 简单灵活 | 相对复杂 |
| **典型语言** | Shell、Python、JavaScript | C、C++、Java、Go |



## 脚本执行

### 执行方式

- 显式调用解释器执行，会创建新进程

    ```bash
    bash script.sh
    ```

- 授予脚本执行权限后执行，会创建新进程，需要在脚本首行指明使用的解释器 `#!/bin/bash`

    ```bash
    chmod +x script.sh
    ./script.sh

- 利用内建命令 source 执行，不会创建新进程，而是在当前进程执行

    ```bash
    source script.sh
    ```

### 内建命令

| **命令** | **功能** | **示例** |
| -------- | ---------------------------------------------------------- | -------------------------------- |
| **alias** | 定义命令别名 | alias ll='ls -l' |
| **echo** | 打印文本 | echo "Hello World" |
| **printf** | 格式化输出 | printf "%s: %d\n" "age" 21 |
| **read** | 从标准输入读取数据并赋值给变量 | read name |
| **exit** | 退出当前 Shell 或脚本 | exit 0 |
| **eval** | 先对命令参数做一次变量与命令替换，再把结果当作命令重新执行 | cmd_ll="ls -l"<br />eval $cmd_ll |
| **exec** | 用新命令替换当前 Shell 进程，不再返回 | exec ls |



### 输入输出机制

Shell 中每个命令运行时，会自动关联 3 个文件描述符

| **描述符** | **名称** | **默认** | **作用** |
| ---------- | -------- | -------- | -------------- |
| **0** | stdin | 键盘 | 命令的输入来源 |
| **1** | stdout | 终端屏幕 | 命令的正常输出 |
| **2** | stderr | 终端屏幕 | 命令的错误输出 |

- `>`：将输出重定向并覆盖到指定文件

  ```bash
  echo "Hello" 1> hello.txt
  echo "Hello" 2> error.txt
  ```

- `>>`：将输出重定向并追加到指定文件

  ```bash
  echo "Hello" 1>> hello.txt
  echo "Hello" 2>> error.txt
  ```

- `<`：将输入重定向到指定文件

  ```bash
  cat 0< input.txt
  ```

- `|`：将前一个命令的 stdout 作为下一个命令的 stdin

  ```bash
  ls | grep ".sh"
  ```



## 变量

### 使用

Shell 变量就是一段字符串的引用，没有数据类型，所有数据都是字符串。变量赋值等号的两边不能有空格，而且变量名只能包含字母、数字、下划线，且不能以数字开头

- 普通变量：只在当前 Shell 有效

    ```bash
    name="dasi"
    ```

- 环境变量：通过 `export` 命令把变量提升为“环境变量”，使得子进程可以继承，从而实现脚本之间传递信息

    ```bash
    export name
    ```

- 只读变量：通过 `readonly` 命令设置只读属性，不能被修改和删除

    ```bash
    readonly name="dasi"
    ```

- 使用变量：用花括号和美元符号包括变量名
    ```shell
    echo "Name: ${name}"
    ```

- 删除变量：通过命令 `unset` 可以使局部变量失效
    ```shell
    unset name
    ```

### 替换机制

- 若变量没定义或为空字符串，则使用 default

    ```bash
    ${var:-default}
    ```

- 若变量没定义或为空字符串，则赋值为 default

    ```bash
    ${var:=default}
    ```

- 若变量没定义或为空字符串，则报错并输出 msg

    ```bash
    ${var:?default}
    ```

- 若变量定义且非空字符串，则使用 alt

    ```bash
    ${var:+default}
    ```

### 字符串操作

- 获取字符串长度

    ```bash
    echo ${#name}
    ```

- 字符串拼接

    ```bash
    c="${a}, ${b}!"
    ```

- 子串截取

    ```bash
    echo ${name:1:5} 	# 从 1 到 5
    echo ${name:2} 		# 从 2 到最后
    ```

- 字符串替换

    ```bash
    str="Hello_World_World"
    echo ${str/World/Earth}   # 替换第一个
    echo ${str//World/Earth}  # 替换所有
    ```

- 大小写转换

    ```bash
    echo ${str^}    # 首字母大写
    echo ${str^^}   # 全部大写
    echo ${str,}    # 首字母小写
    echo ${str,,}   # 全部小写
    ```

### 算术运算

- 整数运算：用两个括号和美元符号围起来

    ```bash
    $((a+b))
    $((a*b))
    $((a/b))
    $((a-b))
    ```

- 小数运算：写成字符串的形式，用 scale 指明位数，并借助 bc 计算

    ```bash
    echo "scale=1; ${a}/${b}" | bc
    ```



## 数组

### 定义

- 一次性定义

    ```bash
    arr=("apple" "banana" "cherry")
    ```

- 分步赋值

    ```bash
    arr[0]="apple"
    arr[1]="banana"
    arr[2]="cherry"
    ```

- 复制数组

    ```bash
    arr2=("${arr[@]}")
    ```

- 合并数组

    ```bash
    arr3=("${arr1[@]}" "${arr2[@]}")
    ```

### 访问

- 访问单个元素

    ```bash
    echo ${arr[0]} 
    ```

- 访问所有元素

    ```bash
    echo ${arr[@]}
    ```

- 获取数组长度

    ```bash
    echo ${#arr[@]}
    ```

- 获取数组有效索引

    ```bash
    echo ${!arr[@]} 
    ```

- 获取数组切片

    ```bash
    echo ${arr[@]:2:3}
    ```

### 修改

- 修改值

    ```bash
    arr[1]="orange"
    ```

- 追加元素

    ```bash
    arr+=("grape")
    ```

- 删除元素

    ```bash
    unset arr[1]
    ```

### 关联数组

其实上述数组并不是传统意义的 Array，因为它允许索引不连续，看作为键是位置索引的 Map 更合适，而通过 `declare` 命令可以让数组的键为字符串

```bashj
declare -A info
info[name]="Dasi"
info[age]="21"
info[school]="sysu"

echo ${info[name]}   # Dasi
echo ${info[age]}    # 21
echo ${!info[@]}     # 所有键
echo ${info[@]}      # 所有值
```



## 运算符

### 数值相关

| **运算符** | **功能** |
| ------ | ----------------------------- |
| **-eq** | 数值等于 equal |
| **-ne** | 数值不等于 not equal |
| **-gt** | 数值大于 greater than |
| **-lt** | 数值小于 less than |
| **-ge** | 数值大于等于 greater or equal |
| **-le** | 数值小于等于 less or equal |

### 字符串相关

| **运算符** | **功能** |
| ---------- | ---------- |
| **=** | 字符串相等 |
| **!=** | 字符串不等 |
| **-z** | 字符串为空 |
| **-n** | 字符串非空 |

### 文件相关

| **运算符** | **功能** |
| ------ | ------------------------- |
| **-f** | 文件是否是普通文件 file |
| **-d** | 文件是否是目录 directory |
| **-r** | 文件是否可读 readable |
| **-w** | 文件是否可写 writable |
| **-x** | 文件是否可执行 executable |
| **-s** | 文件是否有内容 size |
| **-e** | 文件是否存在 exist |



## 流程控制

### if

```bash
if [[ condition ]]; then
    commands
elif [[ condition2 ]]; then
    commands
else
    commands
fi
```

### case

```bash
case 变量 或 表达式 in
    pattern1)
        commands1
        ;;
    pattern2)
        commands2
        ;;
    *)
        default commands
        ;;
esac
```

### while

```bash
while [[conditio[[ condition ]]]
do
	  commands
done
```

### for

- 遍历数组

    ```bash
    for item in "${arr[@]}"
    do
    		commands
    done
    ```

- 遍历列表

    ```bash
    for num in 1 2 3 4 5
    do
      	commands
    done
    ```

- 遍历区间

    ```bash
    for num in {0..5..1}
    do
      	commands
    done
    ```

- 遍历文件

    ```bash
    for file in *.txt
    do
      	commands
    done
    ```



## 函数

### 定义

调用函数直接写函数名，不需要写括号，参数紧跟在函数后面，用空格分隔

```bash
func_name() {
    commands
}
```

### 传参处理

| **变量** | **含义** |
| -------- | ------------- |
| **$0** | 当前脚本名 |
| **$1~$9** | 第 1~9 个参数 |
| **$@** | 所有参数 |
| **$#** | 参数个数 |

### 返回值处理

- 如果是返回执行成功与否，可以直接命令 `return`，然后利用 ？捕获

    ```bash
    check_num() {
        if [ $1 -gt 0 ]; then
            return 0    # 表示“成功”
        else
            return 1    # 表示“失败”
        fi
    }
    
    check_num -5
    echo $?
    ```

- 如果是返回执行的具体结果，则用 `$()` 包围

    ```bash
    sum() {
        echo $(( $1 + $2 ))
    }
    
    result=$(sum 3 5)
    echo "结果是: $result"
    ```

    