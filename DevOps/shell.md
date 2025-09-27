# shell



   * [shell 简介](#shell-简介)
   * [Shell 变量](#shell-变量)
      * [使用](#使用)
      * [数据结构](#数据结构)
      * [环境变量](#环境变量)
      * [字符串](#字符串)
      * [数组](#数组)



## shell 简介

Shell 本义外壳，是一种命令行解释器，可以将用户输入的文本命令转化为操作系统内核能够执行的机器指令，常见的有 bash、sh、zsh，每个运行中的 Shell 实例都是一个独立的进程

终端（Terminal）通常跟命令解释器（Shell）是绑定在一起的，实际上终端指的是一个图形化的窗口，用于接收用户输入命令，并传递给 Shell，最后显示 Shell 输出，每打开一个终端都会自动启动并绑定一个独立的 Shell 进程，每个 Terminal/Shell 都拥有自己独立的命令环境、环境变量及上下文，它们之间的操作互不干扰

但是在本篇文章中 Shell 指的是 Shell Script 即脚本语言，是一种程序设计语言，但是在开始正式开始写脚本之前，先要了解一些前置知识：
- 脚本文件的后缀设置为 `.sh`：实际上任意后缀名都无所谓，因为 Shell 只读取字符来解释运行，不需要编译
- 起始标记 `#! /bin/bash`：通常作为脚本文件的第一行，又叫作 shebang，本义是工作，用于告诉系统这个脚本需要用什么解释器来执行
- 单行注释：使用 `#` 开始的行
- 执行方式
  - `./script.sh`：创建一个新的 Shell 实例，根据 shebang 决定解释器，需要授予脚本执行权限，`chmod +x ./script.sh`
  - `bash script.sh`：创建一个新的 Shell 实例，直接指定解释器，无需给予脚本执行权限
  - `source script.sh` 或 `. script.sh`：在当前 Shell 执行，直接使用当前 Shell 环境的解释器，能直接影响当前环境的变量和设置



## Shell 变量

### 使用

- 创建变量：在 shell 中声明和定义是同时进行的，命名规则和 C 语言一样，因为 Shell 在解析命令时会根据空格将输入分成多个独立的单词或参数，因此赋值等号之间不能加空格
    ```shell
    var1="123"
    ```
- 使用变量：只需要在变量名前面加美元符号 `$` 即可
    ```shell
    var="123"
    echo $var
    ```
- 只读变量：在创建变量之后，可以通过命令 `readonly` 设置只读属性
    ```shell
    var="123"
    readonly var
    ```
- 删除变量：在创建变量之后，可以通过命令 `unset` 删除变量，删除后无法使用
    ```shell
    var="123"
    unset var
    ```

### 数据结构

- 字符串：是 shell 唯一的数据类型，可以用也可以不用引号，在数学运算中 shell 会自动将数值字符串当作数字进行计算
    ```shell
    var1="apple"
    var2='banana'
    var3=123
    ```
- 整数：可以使用命令 `declare -i` 创建类似 int 的整数变量
    ```shell
    declare -i integer=42
    ```
- 索引数组：用括号 `()` 声明，元素之间用空格隔开，允许用数字下标访问，默认从 0 开始递增
    ```shell
    array=(apple banana cherry)
    echo ${array[0]}
    ```
- 关联数组：可以使用命令 `declare -A` 创建使用字符串作为键的字典
    ```shell
    declare -A dict
    dict["name"]="dasi"
    dict["age"]=21
    ```

> 如果有特殊字符，比如空格或$，则必须使用引号

### 环境变量

环境变量是以键值对的形式存在的数据，存储着系统和应用程序所需的信息
- `export [var]`：导出变量，使其成为环境变量并能传递给子进程
- `env`：显示当前环境中的所有变量
- `env [$env_var]="value" [command]`：临时设置环境变量执行命令

常见的环境变量
|环境变量|说明|
|---|---|
|PATH|命令搜索路径，用于定位可执行程序|
|HOME|当前用户的家目录|
|USER|当前登录用户的用户名|
|LOGNAME|当前登录用户的用户名|
|HOSTNAME|当前主机的名称|
|SHELL|默认的 Shell 程序路径，如 `/bin/bash`|
|PWD|当前工作目录|
|OLDPWD|上一次的工作目录，用于 `cd -` 操作|
|LANG|系统语言及区域设置，如 `en_US.UTF-8`|
|TERM|终端类型，如 `xterm-256color`|
|EDITOR|默认的文本编辑器|
|VISUAL|默认的可视化文本编辑器|

### 字符串

引号的区别
- 单引号：所有字符都被视为字面量，因此不能传递变量，也不能转义
- 双引号：可以有变量，也可以出现转义字符
```shell
str1="hello"
str2="world"
str3="$str1 $str2"
echo $str3
```

字符串的一些操作
- 拼接：可以直接将变量和字符串并排写在一起
    ```shell
    str1="hello"
    str2="world"
    str3=$str1", ""$str2!"
    echo $str3
    ```
- 长度：利用 `${#var}` 获取字符串的长度
    ```shell
    str="123456789"
    length=${#str}
    echo $length
    ```
- 截取：使用 `${var:position:length}` 从 position 开始提取长度为 length 的字符串
    ```shell
    str="0123456789"
    substr=${str:3:3}
    echo $substr
    ```
- 替换：使用 `${var/pattern/replacement}` 对字符串中匹配 pattern 部分替换为 replacement
    ```shell
    str="apppe orange banana"
    newstr=${str/apppe/apple}
    echo $newstr
    ```

### 数组

在 shell 中，索引数组的索引不是连续的，更多的像一种数值作为键的字典方式，可以使用 `@` 或 `*` 表示获取全部元素
```shell
str=(apple orange banana)
echo ${str[@]}  # 输出数组内容：apple orange banana
echo ${str[*]}  # 输出数组内容：apple orange banana
echo ${#str[@]} # 输出数组长度：3
str[5]=grape    # 
echo ${str[5]}  # 输出不连续索引：grape
echo ${#str[2]} # 输出索引对应元素的长度：6
```

关联数组可以通过 `!` 获取所有键，如果不加则获得所有值，但是注意输出顺序与定义顺序不一致，输出顺序是不确定的
```shell
declare -A dict
dict["name"]="dasi"
dict["age"]=21
echo ${dict["name"]}    # 输出键对应的值：dasi  
echo ${!dict[@]}        # 输出全部键：age name
echo ${dict[@]}         # 输出全部值：21 dasi
```