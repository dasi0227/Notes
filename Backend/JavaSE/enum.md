# ENUM

枚举是用来表示一组固定常量的类型，比如星期、颜色、状态、方向这种就特别适合用枚举，因为它们的取值是固定且有限的

## 底层

枚举本质上是类型为 public static final 的 ENUM 类的实例

```java
enum Color {
    RED, GREEN, BLUE;
}
// 等价于
final class Color extends Enum<Color> {
    public static final Color RED = new Color("RED", 0);
    public static final Color GREEN = new Color("GREEN", 1);
    public static final Color BLUE = new Color("BLUE", 2);
}
```

如果是自己实现的 enum 类
```java
enum Season {
    Spring("春天", "潮湿"),
    Summer("夏天", "炎热"),
    Autumn("秋天", "温和"),
    Winter("冬天", "寒冷");

    private final String name;
    private final String desc;

    Season(String name, String desc) {
        this.name = name;
        this.desc = desc;
    }

    public String getName() {
        return name;
    }

    public String getDesc() {
        return desc;
    }
}
```

## 使用

- enum 关键字创建的类默认继承 java.lang.Enum，不能再继承其他类
- enum 创建的类是一个 final 类，也就是不可被继承（因为枚举值不希望被更改），但是可以实现接口
- JVM 会把每个枚举值变成当前类的**静态常量实例**，即 public static final，本质是对象
- 枚举构造函数必须是 private，不能被外部实例化
- 枚举值必须写在最前面/最上面，后面才能定义字段和方法
- 枚举值可以没有字段，此时使用的是默认的无参构造函数
- 枚举值也可以自定义字段，用有参构函数赋值
- 自定义字段不能与枚举值重名
- 构造函数得到的枚举对象必须放在第一行

## ENUM 类方法

- name()：返回枚举值
- toString()：返回枚举值
- ordinal()：返回枚举值的位置，按照声明顺序，从 0 开始
- values()：返回所有枚举值，是一个 Enum[] 数组
- valueOf(String name)：将字符串转化为对应的枚举值，大小写敏感
- equals(Object o)：判断是否为同一个枚举实例
- compareTo(Enum e)：返回当前枚举对象的编号 - 传递的枚举对象的编号
  


