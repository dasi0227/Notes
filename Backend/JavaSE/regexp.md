# 正则表达式

## 语法

- 字符匹配：普通字符 a,b,c 或 Unicode \u4e2d
- 除了换行符的任意字符：. 
- 字符类：在方括号内的任一字符，如 [abc]、[123]
- 排除字符类：不在方括号内的任一字符，如 [^a]，[^4]
- 预定义字符类：\d 数字，\w 单词，\s 空白字符
- 连字符：[a-z]、[A-Z]、[0-9]
- 边界匹配：^ 行首，$ 行尾，\b 单词边界
- 量词：* 零词或多次，+ 一次或多次，？零次或一次，{m,n}至少m次至多n次，{n}匹配n次
- 或：a|b
- 分组：用括号 (...) 包裹起来的子表达式表示一个分组
- 捕获：对于每一个 (...) 从左到右都自动分配了一个编号，0 表示整个匹配结果，优先匹配括号内表达式
  md表格给我，给出正则表达式语法、含义和一个简单示例

## Pattern

Pattern 表示一个编译后的正则表达式模版，是不可变的
- static Pattern compile(String regex)：编译给定的正则表达式为一个 Pattern 对象，用于后续匹配
- static Pattern compile(String regex, int flags)：带标志位地编译正则表达式
- static boolean matches(String regex, CharSequence input)：对整个输入序列执行一次完整匹配
- String pattern()：返回编译此 Pattern 时用的正则表达式字符串
- int flags()：返回编译时使用的标志位
- Matcher matcher(String input)：返回 Matcher 对象实例 

标志位：
- Pattern.CASE_INSENSITIVE：忽略大小写
- Pattern.MULTILINE：多行模式，识别行首和行为，不仅限于输入的首尾
- Pattern.DOTALL：单行模式，. 会匹配换行符
- Pattern.UNICODE_CASE：启用 Unicode 方式的大小写折叠
- Pattern.COMMENTS：允许包含空白和注释
- Pattern.LITERAL：将整个模式当作字面文本
- Pattern.UNICODE_CHARACTER_CLASS：使预定义字符类采用 Unicode 而不是 ASCII

## Matcher

Matcher 表示一次“针对某个输入文本”的匹配会话，其绑定了唯一的 Pattern 正则表达式实例 和 String 输入字符串实例，内部维护了当前匹配的各种信息
- Matcher matcher(CharSequence input)：基于此 Pattern 创建一个作用于指定输入序列的 Matcher
- boolean matches()：尝试对整个输入序列进行完整匹配
- boolean find()：按顺序搜索下一个匹配子序列，每调用一次向后推进搜索位置
- boolean find(int start)：从指定索引位置开始搜索下一个匹配
- boolean lookingAt()：尝试从输入序列开始位置匹配，但不要求匹配到末尾
- String group(int group)：返回第 group 个捕获组匹配的子序列，不传则为 0
- int groupCount()：返回此 Pattern 中定义的捕获组数量
- int start(int group)：返回第 group 个捕获组匹配的起始索引，不传则为 0
- int end(int group)：返回第 group 个捕获组匹配结束的索引，不传则为 0
- Matcher reset()：重置 Matcher，将其状态恢复到最初
- String replaceAll(String replacement)：将所有匹配项替换为 replacement，并返回替换后的新字符串
- String replaceFirst(String replacement)：将第一个匹配项替换为 replacement，并返回替换后的新字符串

反向引用
- 在正则表达式里面：用 \1、\2… 等来引用第 1、第 2 … 个捕获组的文本
- 在替换模板里面：用 $1、$2… 等来代表第 1、第 2 … 个捕获组的文本

```java
public class JieBa {
    public static void main(String[] args) {
        String text = "我...现在在在在...在就...就要要要要..要..学学.学学学....JJJJavaaaaaa";
        System.out.println("最初的字符串：" + text);

        // 1. 去掉所有的 .
        Pattern pattern = Pattern.compile("[.]+");
        Matcher matcher = pattern.matcher(text);
        text = matcher.replaceAll("");
        System.out.println("去除 . 后的：" + text);

        // 2. 去除重复的字
        pattern = Pattern.compile("(.)\\1+");
        matcher = pattern.matcher(text);
        while (matcher.find()) {
            System.out.println("找到结巴的字：" + matcher.group(0));
        }
        text = matcher.replaceAll("$1");
        System.out.println("处理结巴字之后：" + text);
    }
}
```

不要被 //1 和 $1 迷惑了，他们不是每一组匹配，而是每一组匹配的子匹配，这里可以放在 while 循环外，就是对每一组匹配，替换为每一组匹配的第一个子匹配 