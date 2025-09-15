# ECMAScript 6

ECMAScript 实际上就是 JavaScript 的一次重大更新，提升了 JS 开发体验

## let 和 const

var 的局限性
- 只有全局作用域或函数作用域，不能在块内限定生命周期，易引发重名和覆盖
- var 声明会“提升”到函数或全局最顶端，导致在声明前就能访问到 undefined，增加调试难度

新增变量声明符
- let：块级作用域，声明后值与类型均可改变
- const：块级作用域，声明时必须初始化，声明后值与类型都不可变，但如果它引用的是对象或数组，对象内部仍可被修改

暂时性死区（TDZ, Temporal Dead Zone）：声明会自动提升到块级作用域顶部，但是在初始化前访问会抛出 ReferenceError

## 模板字符串

传统拼接：用双引号或单引号包裹，通过 + 拼接，需要 \\n 来实现换行
```js
let name = "dasi";
let msg = "hello " + name + "!\nWelcome";
```

模板字符串：用反撇号包裹，通过 ${...} 嵌入变量、方法或任意表达式，可以直接换行 
```js
let name = "dasi";
let msg = `hello ${name}!
Welcome`
```

## 解构赋值

使用一种声明式的语法，一次性从数组或对象中提取出多个值，并赋给相应的变量
- 简化变量声明
- 直接提取函数返回值和函数参数
- 交换变量值：[a, b] = [b, a]

数组解构
```js
// 传统方式
const arr = [1, 2, 3];
const a = arr[0];
const b = arr[1];

// 解构赋值：变量必须对应位置，若被解构的值数量不足变量数量，则多出的变量值为 undefined；
const [x, y, z] = [1, 2, 3];
console.log(x, y, z); // 1 2 3

// 跳过元素：使用逗号跳过，不占用变量
const [first, , third] = [10, 20, 30];
console.log(first, third); // 10 30

// 设置默认值：当对应元素为 undefined 时才使用默认值，而 null 等其他值不会触发默认
const [m = 5, n = 7] = [undefined, 2];
console.log(m, n);  // 5 2
```

对象解构
```js
// 传统方式
const user = { name: 'dasi', age: 21 };
const name1 = user.name;
const age1  = user.age;

// 解构赋值：名称必须相同，如果属性不存在，则为 undefined
const { name, age } = { name: 'dasi', age: 21 };
console.log(name, age); // dasi 21

// 解构赋值：重命名
const { name: uname, gender = 'male' } = { name: 'dasi' };
console.log(uname, gender); // dasi male
```

函数参数解构
```js
// 数组参数
function sum([a, b]) {
    return a + b;
}
console.log(sum([3, 4])); // 7

// 对象参数
function greet({ name, age = 21 }) {
    console.log(`你好，${name}，${age} 岁`);
}
greet({ name: 'dasi' }); // 你好，dasi，18 岁
```

## 箭头函数

箭头函数旨在提供一种更简洁、更安全、更符合现代开发习惯的函数写法

基本语法
```js
// 传统函数
function sum(a, b) {
    return a + b;
}

// 单条表达式无需大括号，默认返回该值
const sum = (a, b) => a + b;

// 单个参数可以省略小括号
const sq = x => x * x;

// 没有参数却不可以省略小括号
const sayHi = () => console.log('Hi');

// 多条表达式需要大括号
const cmp = (a, b) => {
    if (a > b) return 1;
    if (a < b) return -1;
    return 0;
};
```

this 绑定：箭头函数不有自己的 this，它的 this 始终指向定义时所在的外层作用域，适合在回调里保持上下文
```js
<button id="btn" value="abc">点我查看值</button>

<script>
    const widget = {
        value: 123,
    
        // 传统方式：this 指向触发事件的 DOM 元素，输出 abc
        bindWithFunction() {
        document.getElementById('btn').addEventListener('click', function() {
                console.log(this);
                console.log('function this.value =', this.value);
            });
        },

        // 箭头函数方式：this 指向 widget 对象，输出 123
        bindWithArrow() {
        document.getElementById('btn').addEventListener('click', () => {
            console.log(this)
            console.log('arrow this.value =', this.value);
            });
        }
    };

    // 选择一个方式
    widget.bindWithFunction();
    widget.bindWithArrow();
</script>
```

## rest 和 spread

rest：可以通过 ...rest 放在参数列表的最后，将剩余参数收集到一个数组里面
```js
function sum(...nums) {
    return nums.reduce((total, n) => total + n, 0);
}
console.log(sum(1, 2, 3));    // 6
```

spread：可以通过 ...spread 将一个可迭代对象展开成一列单独的值或属性
```js
// 数组展开
const nums = [1, 2, 3];
console.log(Math.max(...nums)); // 等同于 Math.max(1, 2, 3) → 3
const a = [1, 2];
const b = [3, 4];
const c = [...a, ...b]; // [1, 2, 3, 4]

// 对象展开：后面属性会覆盖前面
const o1 = { x: 1, y: 2 };
const o2 = { y: 3, z: 4 };
const o3 = { ...o1, ...o2 }; // { x:1, y:3, z:4 }
```

> spread 通常用于深拷贝：object_copy = [...object]

## 模块化

模块化：将代码按功能拆分到独立模块中的设计思想
- 高内聚、低耦合：每个模块只关注自己的一部分功能，暴露必要接口，其它细节对外隐藏
- 可维护性：模块代码独立、易读、易测、易复用
- 依赖管理：显式声明模块间依赖关系，避免全局变量冲突

模块实现
- 导出：通过 export 标记哪些属性和功能是对外可用的，明确“我能提供什么”
- 导入：通过 import 引入外部文件的哪些属性和功能，明确“我需要什么”
- 导出导入内容都是作为对象进行处理

导出方式
- 分别导出：每个要导出的绑定都单独加上 export 关键字
- 统一导出：先在模块内部定义，然后在底部一次性集中导出
- 默认导出：模块只能有一个默认导出，适用于该模块的主功能

导入方式
- 分别导入：使用 {} 括起需要导入的属性或功能，名称必须与导出时的名称一致，可以使用 as 进行 重命名
- 统一导入：可以利用通配符 * 导入，但是必须使用 as 进行重命名作为对象使用
- 默认导入：直接随意给定一个名称导入之前默认导出的东西，不需要与导出时的名称一致