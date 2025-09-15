# Vue

## 概述

### Vue 框架

Vue 是渐进式 JavaScript 框架，专注于构建视图层，可以按照需要逐步引入模块
- 声明式渲染：用模板语法绑定数据到视图，声明“想看到什么”，而 Vue 会自动最小化地更新 DOM，无需手动操作
- SFC 模式（Single File Component）：单文件组件模式把一个组件的模板、逻辑和样式都写在同一个 .vue 文件里
- 响应性数据：模板使用的数据变化时，视图会自动同步更新，避免手动更新 DOM

### 组件

组件（Component）是一个小的、封装的、可重用的 .vue 实例文件，本质上就是一块 HTML，只不过加一点 JS 逻辑，再撒了点 CSS 样式，通常代表 UI 的一部分，小到按钮、输入框，大到页眉、页脚甚至整个页面

> .vue 文件和 vue 组件是等价的叫法

组件文件结构
- \<template>：组件视图，存 html 代码
- \<script>：组件逻辑，存 js 代码
- \<style scoped>：组件样式，存 css 代码

组件的元数据：描述组件结构和行为的幕后信息
- name：组件的名字
- props：组件可以接受的外部参数
- emits：组件可以发出哪些事件
- components：用到的子组件
- directives：用到的自定义指令

### 工作流程

Vue 的工作流程
1. 开发阶段：编写 .vue 文件
2. 构建阶段：Vite/Webpack 会把 .vue 文件分离为模板、脚本、样式三部分供后续处理
3. 编译阶段：模板部分被编译为 JS 渲染函数，脚本逻辑被封装为 JS 组件对象，样式则被提取并作用域处理
4. 部署阶段：所有组件被打包为浏览器可执行的静态资源文件（HTML、JS、CSS）
5. 运行阶段：浏览器加载应用入口，Vue 实例挂载组件到 DOM 上，启动响应式系统并动态更新 DOM

使用其他 .vue 文件的底层逻辑
1. 在 App.vue 的 script 中 `import xxx from "/path/to/xxx.vue"`
2. 在 App.vue 的 template 中，利用标签使用导入的组件 `<xxx></xxx>`
3. Vue 的编译器在构建阶段会把 `<xxx></xxx>` 转换成 JS 函数 `createVNode(Header)`
4. Vue 把这个虚拟节点 VNode 渲染成真正的 DOM，并绑定上组件逻辑，最后挂载到页面的 DOM 树

## Vite

Vite 是一个现代前端构建工具，目标是提供更快、更轻量的开发体验
- 极速冷启动：直接加载 .js / .ts 文件，模块按需加载
- 超快热更新：只重新加载变更模块，不影响其他代码，也不刷新整个页面
- 内置支持 Vue、React 等主流框架
- 简单配置：使用 vite.config.js 进行高效快速配置，同时默认配置已经足够好

常用 api
- npm create vite：创建项目，会提示你输入项目名、选择框架
- npn rum dev：启动本地开发服务器，默认在 localhost:5173
- npm run build：打包构建生产环境代码，构建出优化后的静态资源，默认输出到 dist/ 目录
- npm run preview：启动一个本地服务，预览 npm run build 打包出来的页面效果

目录结构
- public/：存放一些公共资源，不会被打包处理，如favicon、字体等，这些会直接复制到构建出的 dist/ 下
- src/：存放项目的源代码
  - assets/：存放项目中需要引入的静态资源，如 img、svg、css、js 等
  - components/：存放可复用的小型 UI 组件，是最小功能单元，如按钮、输入框、Modal 等
  - main.js：应用的入口文件，负责创建 Vue 实例并挂载根组件 App.vue 
  - App.vue：根组件，负责渲染页面的主结构，是所有组件的起点容器
  - 可选的目录，用于细粒度区分文件
    - layouts/：存放项目布局容器组件，负责应用程序的整体布局，如头部、底部、导航菜单等
    - pages/：存放页面级别的组件
    - utils/：工具函数库，封装常用逻辑
    - plugins/：存放插件相关文件
    - router/：放置路由配置相关的文件
    - store/：存放状态管理相关的文件
- index.html：项目的主入口页面，开发阶段就是浏览器打开的页面
- vite.config.js：Vite 的配置文件
- package.json：npm 的配置文件

## .vue 文件

### script 风格

Options API 风格：分别声明提供的变量和方法
```html
<script>
    export default{
        // 提供变量：会被放在组件的实例对象上
        data() {
            return {}
        },
        // 提供方法：this 指向实例对象
        methods: {
            method1() {},
            method2() {}
        }
    };
</script>
```

Composition API 风格：相当于构造函数
```html
<script>
    import { ref } from 'vue';
    export default {
        setup() {
            // 声明变量：返回的是响应式包装对象，通过 .value 访问值，不提供则为 undefined
            const var1 = ref();
            const var2 = ref({ name: 'dasi', age: 21 });
            // 声明方法
            function method1(){}
            function method2(){}
            // 声明要提供的变量和方法
            return { var1, var2, method1, method2 };
        }
    };
</script>
```

setup 语法糖：不需要写 setup()、return 和 export default，默认将顶层声明的东西全 return，只能使用一次
```html
<script setup>
    import { ref } from 'vue';
    const var1 = ref();
    const var2 = ref({ name: 'dasi', age: 21 });
    function method1(){}
    function method2(){}
</script>
```

### 响应式数据

响应式数据：不需要手动更新 DOM，当数据变化时，页面会自动刷新

ref(初始值)：用于原始数据类型，如数字、字符串和布尔值，在 script 中操作需要通过 .value，在 template 中操作不需要 .value
```js
import { ref } from 'vue';
const count = ref(0); 
count.value++;
```

reactive(初始值)：用于对象或数组，不需要 .value，直接 .属性名 即可
```js
import { reactive } from 'vue';
const user = reactive({
  name: 'Alice',
  age: 21
});
user.age++; 
```

toRef(对象名, 属性名)：从一个响应式对象中，提取某个属性，把它变成一个独立的 ref，但它仍然和原对象保持响应式绑定
```js
import { reactive, toRef } from 'vue';

const state = reactive({
  count: 0,
  name: 'Vue'
});

// 提取 count 字段为 ref
const countRef = toRef(state, 'count');
// 修改 countRef，会同步更新 state.count
countRef.value++;
console.log(state.count); // 输出：1
// 修改原对象，也会同步影响 ref
state.count++;
console.log(countRef.value); // 输出：2
```

toRefs(对象名)：把一个响应式对象的每个属性都转换为 ref，并保持响应性
```js
import { reactive, toRefs } from 'vue';

const state = reactive({
  count: 0,
  name: 'Vue'
});

// 一次性提取所有字段为 ref
const { count, name } = toRefs(state);
// 修改 ref，原对象同步变化
count.value += 5;
name.value = 'React Who?';
console.log(state.count); // 输出：5
console.log(state.name);  // 输出：React Who?
```

计算属性：`computed()` 根据已有响应式数据计算得出的值，并且会自动缓存，只有相关数据真的变了才重新计算
```js
import { ref, computed } from 'vue';
const firstName = ref('Vue');
const lastName = ref('3');
const fullName = computed(() => {
  return firstName.value + ' ' + lastName.value;
});
```

数据监听：`watch(data, (newVal, oldVal))` 监听一个或多个响应式数据的变化，在变化时触发你定义的回调函数
```js
import { ref, watch } from 'vue';
const count = ref(0);
watch(count, (newVal, oldVal) => {
  console.log(`count 从 ${oldVal} 变成了 ${newVal}`);
});
```

> `watchEffect()` 自动追踪依赖的副作用函数，在函数体内使用监听的响应式变量，系统就会在这些变量变化时重新执行整个函数

### 生命周期

钩子（hook）是组件生命周期的某些时刻，在这里可以调用你注册的回调函数
- 挂载（mount）：把组件渲染成真实的 DOM，然后插入到页面中的 DOM 树中
- 卸载（unmount）：把组件的 DOM 元素从页面中移除，同时清理相关的数据、监听器、定时器等资源
- 更新（update）：当组件依赖的响应式数据发生变化时，Vue 会重新渲染虚拟 DOM 并更新真实 DOM

|API|时机|作用|
|-|-|-|
|onBeforeMount|模板还没挂上 DOM 前|初始化一些数据、日志|
|onMounted|模板渲染并挂上 DOM 后|操作 DOM、发请求、开定时器|
|onBeforeUpdate|响应式数据更新触发 DOM 变更前|对旧数据做最后处理|
|onUpdated|DOM 更新完成后|检查新视图，更新依赖数据等|
|onBeforeUnmount|组件准备被卸载前|清除副作用（定时器、监听器）|
|onUnmounted|组件已从 DOM 移除后|彻底清扫垃圾，日志输出|


## 模板语法

### {{}}

插值表达式：使用双大括号 {{}} 插入响应式数据
```html
<p>当前用户为：{{ message }}</p>
```

### v-text

文本绑定：`v-text` 绑定响应式数据作为标签内的文本，原标签内的文字会被覆盖，如果需要拼接字符串需要在 v-text 中利用模板字符串
```html
<p v-text="`当前用户为：${message}`"></p>
```

### v-html

内容绑定：`v-html` 绑定响应式数据作为标签内的 HTML 标签
```html
<div v-html="rawHtml"></div>
```

### v-bind

属性绑定：`v-bind` 绑定响应式数据作为标签的属性
```html
<img v-bind:src="avatarUrl" alt="头像">
<!-- 简写为 :prop -->
<img :src="faviconUrl" alt="图标">
```

### v-on

事件绑定：`v-on` 绑定响应式数据作为事件的触发方法
```html
<button v-on:click="handleClickReset">点击重置</button>
<!-- 简写为 @event -->
<button @click="handleClickSubmit">点击提交</button>
```

### v-if/v-else

条件绑定：`v-if 和 v-else` 绑定响应式数据作为条件，决定是否插入 DOM 元素，`v-else` 自动和前一个 `v-if` 形成配对
```html
<p v-if="isLoggedIn">已登录</p>
<p v-else>请登录</p>
```

### v-show

条件显示：`v-show` 绑定响应式数据作为条件，决定 display 属性的 display 属性是否为 none
```html
<p v-show="isLoggedIn">你已登陆</p>
```

### v-for

列表渲染：`v-for="(item, index) in items" v-bind:key="item.id"` 遍历可迭代对象，动态生成元素列表
```html
<ul>
    <li v-for="(todo, i) in todos" :key="todo.id">
        {{ i+1 }}. {{ todo.text }} ({{ todo.done ? '已完成' : '未完成' }})
    </li>
</ul>

<tbody>
    <tr v-for="(todo, i) in todos" :key="todo.id">
        <td>{{ i + 1 }}</td>
        <td>{{ todo.text }}</td>
        <td>{{ todo.done ? '已完成' : '未完成' }}</td>
    </tr>
</tbody>
```

### v-model

双向绑定：`v-model` 在用户更改 DOM 树中表单上的值，会同步反映到响应式数据
```html
<input v-model="form.username" placeholder="用户名" />
```

### v-once

单次渲染：`v-once` 将元素及其子组件只渲染一次，后续数据变化不再更新，用于静态内容优化
```html
<p v-once>初始化时间：{{ now }}</p>
```

### v-pre

跳过编译：`v-pre` 告诉 Vue 不去编译该元素及其所有子节点，直接原样输出
```html
<p v-pre>原始模板串为：{{ rawTemplate }}</p>
```

### 挂载

挂载（mount）就是把写好的组件塞进页面上的某个 DOM 元素里，让 Vue 接管它的内容和更新
```js
// 引入 Vue 框架中的 createApp 方法
import { createApp } from 'vue';

// 引入自定义的 Vue 组件对象
import MyApp from './MyApp.vue';

// 创建上述对象的 Vue 组件实例
const myApp = createApp(MyApp)

// 将 Vue 组件实例挂载到页面指定的 DOM 元素上
myApp.mount('#app');
```

## 参数传递

### 子传父：emit

1. 子组件定义新事件 `emit = defineEmits(["myEvent"])`
2. 子组件发出事件 `emit("myEvent", "para1", "para2")`
3. 父组件在子组件的标签中监听处理事件 `<Child @myEvent="handleMyEvent"></Child>`
4. 父组件声明回调函数处理子组件传递的参数 `function handleMyEvent(para1, para2)`

> handleMyEvent 不需要给出 (参数列表)，默认就是子组件传递的参数

### 父传子：prop

1. 子组件定义新属性 `defineProps({myProp: String})`
2. 父组件在子组件标签上传递参数 `<Child v-bind:myProp="parentVar"></Child>`

> props 是响应式的，父组件数据更新时，子组件会自动同步更新。但是对于子组件来说是只读的，父组件可以更改，但是子组件不能更改

### 父子互传

1. 父组件：`v-model:childProp="parentProp"`
2. 子组件：
   1. `defineProps({ childProp: String })`
   2. `defineEmits(['update:childProp'])`
   3. `emit('update:childProp', newValue)`

### 兄弟互传

必须由子组件 A 传给父组件，再由父组件传给子组件 B

## 路由

### 定义

单页应用模式（SPA，Single Page Application）只用一页来实现具体应用，通过点击按钮来切换链接，从而实现页面跳转的功能，但实际上只是切换组件

路由（Route）：根据网址的路径，决定页面的显示，即 App.vue 挂载哪个组件

### 路由配置

需要引入依赖 `vue-router`
- createRouter()：创建路由对象的工厂函数，配合 history 和 routes 一起使用
- createWebHistory()：设置为 HTML5 History 模式，需要服务端支持
- createWebHashHistory()：设置为 Hash 模式，URL 会包含前缀 #，无需服务端支持

定义路由规则 routes 数组，每个元素是对象，代表一个路由项
- path：访问路径
- component：该路径渲染哪个组件
- redirect：重定向到哪个路径

```js
// src/routers/router.js
import { createRouter, createWebHistory } from 'vue-router'
import Home from '../components/Home.vue'
import About from '../components/About.vue'

const routes = [
  { path: '/', redirect: '/home' },
  { path: '/home', component: Home },
  { path: '/about', component: About }
]

const router = createRouter({
  history: createWebHashHistory(), // 或 createWebHistory()
  routes
})

export default router
```

注册路由
1. 在 router.js 中默认导出路由器
2. 在 main.js 中导入路由器
3. 在 main.js 中注册路由系统，否则 router-view 无效

```js
// main.js
import { createApp } from 'vue'
import App from './App.vue'
import router from './router'
const app = createApp(App)
app.use(router)
app.mount('#app')
```

### 路由展示

Vue Router 会将当前路由对应的组件渲染到 `<router-view />` 标签所在的位置，并且实际应用中 App.vue 只有一个该 `<router-view />`，作为主视图展示区域

> 虽然理论上可以有多个 `<router-view />`，但是这样不符合 SPA 模式

嵌套路由：在 routes 中定义路由对象/路由项时，声明 children 属性来定义子路由
```js
const routes = [
  {
    path: '/admin',
    component: AdminLayout,
    children: [
      { path: 'user', component: UserList },
      { path: 'setting', component: Settings }
    ]
  }
]
```

命名路由：在 routes 中定义路由对象/路由项时，通过将 components 属性设置为对象，为不同名称的 `<router-view name="xxx"/>` 渲染不同的组件
```js
const routes = [
  {
    path: '/dashboard',
    components: {
      default: MainView, // 没有 name 属性时默认显示的组件
      sidebar: SidePanel,
      footer: FooterView
    }
  }
]

/* 模板中使用命名
<router-view />
<router-view name="sidebar" />
<router-view name="footer" />
*/
```

### 路由方式

声明式路由：通过模板中的 `<router-link to=""></router-link>` 实现页面跳转，适合静态导航栏、菜单等固定跳转结构
- 如果目标地址是静态字符串，则不需要 `:`
- 如果目标地址是模板字符串，需要 `:` 告诉 Vue 去解析表达式
```html
<router-link to="/home">首页</router-link>
<router-link :to="`/user/${userId}`">用户中心</router-link>
```

编程式路由：通过 JS 代码操作 Vue Router 实例，实现页面跳转，适用于用户交互、逻辑判断、权限控制等动态场景，而不依赖静态标签
```js
import { useRouter } from 'vue-router'
// 使用前需调用 useRouter() 获取路由器实例
const router = useRouter()
// 基本操作
router.push('/path')       // 正常跳转到指定路径，记录在历史栈中
router.replace('/path')    // 替换当前路径，不会留下历史记录
router.back()              // 返回上一页
router.forward()           // 前进一页
```

### 路由传参

路径传参：参数直接嵌在路径中，常用于资源 ID、语言、用户 ID 等
- 路由配置：需要通过 `:` 声明动态参数
```js
{
  path: '/profile/:id/:username',
  name: 'profile'
  component: Profile
}
```
- 跳转方式：可以传递模板字符串，也可以声明 params 属性传递对象（必须使用名称，参数名必须一致）
```js
router.push(`/profile/0001/dasi`)
router.push({
    name: 'profile',
    params: {
        id: 0001,
        username: dasi
    }
})
```
- 接收方式：位于 route 实例的 params 属性中
```js
import { useRoute } from 'vue-router'
const route = useRoute()
console.log(route.params.id)
console.log(route.params.username)
```

键值对传参：参数写在 URL 的 ? 后面，适合用于搜索、分页、筛选等需求
- 路由配置：不需要特殊配置
```js
{
  path: '/search',
  component: Search
}
```
- 跳转方式：跳转方式：可以传递模板字符串，也可以声明 query 属性传递对象（可以不使用名称，但参数名必须一致）
```js
router.push("/search?keyword=vue&page=2")
router.push({
  path: '/search',
  query: {
    keyword: 'vue',
    page: 2
  }
})
```
- 接收方式：位于 route 实例的 query 属性中
```js
import { useRoute } from 'vue-router'
const route = useRoute()
console.log(route.query.keyword)
console.log(route.query.page)
```

### 路由守卫

路由守卫是 Vue Router 提供的钩子函数，用于在路由发生变化前后执行逻辑

|类型|作用范围|常见用途|
|-|-|-|
|全局守卫|全局有效|权限验证、登录跳转、打点统计|
|路由守卫|单个路由项上|特定路由的权限限制或拦截逻辑|
|组件守卫|当前激活组件|离开前提示、进入后初始化、数据校验|

执行顺序
1. 用户发起导航行为
2. 全局前置守卫：router.beforeEach()
3. 新页面的路由前置守卫：beforeEnter()
5. 组件挂载
6. 原页面的组件离开守卫：beforeRouteLeave()
7. 全局后置守卫：router.afterEach()

参数
- to：将要进入的目标路由
- from：当前导航正要离开的路由
- next：守卫函数里必须调用的回调函数
  - next()：放行，继续路由跳转
  - next(false)：中断跳转，停在当前页面
  - next('/login')：重定向到指定路径


全局前置守卫：定义在 router.js 中，页面跳转完成前触发
```js
router.beforeEach((to, from, next) => {})
```

全局后置守卫：定义在 router.js 中，页面跳转完成后触发
```js
router.afterEach((to, from) => {})
```

路由前置守卫：配置在 routes 数组的某个路由项内，进入该路径时生效
```js
{
  path: '/admin',
  component: AdminPage,
  beforeEnter: (to, from, next) => {}
}
```

组件离开守卫：定义在页面组件中，组件离开时生效
```js
import { onBeforeRouteLeave } from 'vue-router'
onBeforeRouteLeave(to, from, next) {}
```

## 异步编程

### Promise

Promise 是 JS 异步编程的一种解决方案，每个 Promise 对象代表一个异步操作
- 具有三种状态：pending（进行中）、resolved（成功）、rejected（失败）
- 一旦状态从 pending 变成 resolved 或 rejected，就不能再变了
- 只有 resolve() 和 reject() 可以改变状态，其他任何操作都不行

使用流程
1. 创建 Promise 实例，传递一个函数，函数题中根据需求调用 resolve(value) 或 reject(value)，或者 throw 出一个错误
2. 定义 Promise 实例的 then 方法，表示成功后的回调操作
3. 定义 Promise 实例的 catch 方法，表示失败后的回调操作

```js
let promise = new Promise(function (resolve, reject) {
    flag = ... // 业务逻辑
    if (flag) {
      resolve("成功执行1")
    } else {
      reject("失败执行")
    }
})

console.log("异步执行1")

promise.then(
  result => {
    console.log(result)
    return "成功执行2"
  }
).then(
  result => {
    console.log(result)
  }
).catch(
  error => {
    console.log(erroe)
  }
)

console.log("异步执行2")
```

### async 和 await

async 是一个 语法糖，用来标记一个函数为异步函数，从而可以在这个函数里用 await 等待一个 Promise 结果
```js
// 用 then：
function getData() {
  fetch(url) // 本身就返回一个 Promise 对象，不需要显式创建
    .then(res => {
      res.json()
    })
    .then(data => {
      console.log(data)
    })
    .catch(err => {
      console.error(err)
    })
}

// 用 async/await：
async function getData() {
  try {
    const res = await fetch(url)
    const data = await res.json()
    console.log(data)
  } catch (err) {
    console.error(err)
  }
}
```

### Axios 请求

Axios 是一个基于 Promise 的 HTTP 客户端，用来发送 AJAX 异步请求和获取响应的库

get 请求
```js
import axios from 'axios'
axios({
  method: "get",
  url: "https://example.com",
  // 放入 url 后
  params: {
    keyword: 'vue',
    page: 2
  }
}).then(res => console.log(res))
.catch(error => console.log(error))

// 也可以简写成
axios.get("https://example.com", {
  params: {
    keyword: 'vue',
    page: 2
  }
})
```

post 请求
```js
import axios from 'axios'
axios({
  method: "post",
  url: "https://example.com",
  // 放入请求体
  data: {
    username: "dasi",
    age: "21"
  }
}).then(res => console.log(res))
.catch(error => console.log(error))

// 也可以简写成
axios.post("https://example.com", {
  username: "dasi",
  age: 21
})
```

### Axios 实例

可以新建一个文件 src/axios.js，在其中创建实例并默认返回，从而让所有组件都可以使用这个 axios 实例

axios.create() 创建实例并配置属性
- baseURL：设置所有请求的基础路径前缀
- timeout：设置请求超时时间（毫秒），超过时间会抛出错误
- headers：设置默认的请求头

拦截器（Interceptor）
- 请求拦截器：在请求发送前执行，常用于加 token、日志、Loading 效果等
  - config：请求配置对象，可以修改后返回
  - error：处理失败请求，必须响应一个失败的 Promise

- 响应拦截器：在响应回来后执行，常用于统一处理响应、错误提示、token 失效重定向等
  - response：处理成功的响应对象，可以提取需要的信息返回
  - error：处理失败响应 error，必须响应一个失败的 Promise

```js
import axios from 'axios'

const instance = axios.create({
    baseURL: 'https://',
    timeout: 5000,
    headers: {
        'Content-Type': 'application/json'
    }
})

instance.interceptors.request.use(
    config => {
        console.log("请求拦截")
        console.log(`要访问的URL：${config.baseURL + config.url}`)
        return config
    },
    error => {
        console.log(`错误信息：${error}`)
        return Promise.reject(error)
    }
)

instance.interceptors.response.use(
    response => {
        console.log("响应拦截")
        console.log(`消息来源于：${response.data.from}`)
        return response.data
    },
    error => {
        console.log(`错误信息：${error}`)
        return Promise.reject(error)
    }
)

export default instance
```


## CORS

### 浏览器行为

浏览器默认只能在同源/同域之间互相交互，要求两端必须**协议相同、域名相同、端口相同**

Vite 客户端运行在 http://localhost:5173/，而 Tomcat 服务端运行在 http://localhost:8080/，因此浏览器发现请求是从端口 5173 到端口 8080 的请求，产生了跨域问题，又称为跨域资源共享问题（Cross-Origin Resource Sharing，CORS）

浏览器首先会发送一个预检请求，即 OPTIONS 请求，来预先检查服务器是否允许这个实际请求，如果浏览器接收到的响应头中包含下述行
```
Access-Control-Allow-Origin: http://localhost:5173
```

那么浏览器则知道服务端允许来自跨域客户端的请求，所以放心的把原始的 POST/GET 请求发给服务端，但是如果没有找到上述行，则会产生报错信息
```
xxx has been blocked by CORS policy:
No 'Access-Control-Allow-Origin' header is present on the requested resource.
```

### 后端解决

```java
 // 设置 CORS 响应头
response.setHeader("Access-Control-Allow-Origin", "*");
response.setHeader("Access-Control-Allow-Methods", "POST, GET, OPTIONS, DELETE");
response.setHeader("Access-Control-Max-Age", "3600");
response.setHeader("Access-Control-Allow-Headers", "access-control-allow-origin, authority, content-type, version-info, X-Requested-With");
```

## Pinia

Pinia 是 Vue 官方推荐的状态管理库，使用流程如下

1. 安装
```bash
npm install pinia
```
2. 在入口文件注册（跟路由器一样）
```js
import { createApp } from 'vue'
import { createPinia } from 'pinia'
import App from './App.vue'

const app = createApp(App)
app.use(createPinia())
app.mount('#app')
```
3. 在 stores/user.js 中利用 defineStore 新建状态仓库：返回的是一个构造函数
|配置项|定义|使用|
|-|-|-|
|id|状态仓库的唯一 id|必需|
|state|要存储的状态数据|必需|
|getters|获取函数|可选，常用于对状态数据进行非更改性处理，比如组合数据、计算数据、格式化数据、筛选数据等|
|actions|方法函数|可选，常用于对状态数据进行更改性处理，不能用箭头函数，因为需要用 this 来访问状态数据|
```js
import { defineStore } from 'pinia'

export const definedUser = defineStore({
  id: 'user',
  state: () => ({
    username: "dasi",
    password: "123456",
    isLogin: false
  }),
  getters: {
    welcomeMessage: (state) => {
      return state.isLogin ? `欢迎回来，${state.username}！` : '请先登录'
    }
  }
  actions: {
    login(name) {
      this.username = name
      this.isLogin = true
    },
    logout() {
      this.username = ''
      this.isLogin = false
    }
  }
})
```
4. 组件中调用构造函数，获得状态仓库实例，从而允许多个组件中复用同一个 store 实例
```js
import { definedUser } from '../stores/user'
const userStore = definedUser()
userStore.login('Dasi')
console.log(userStore.username)
```

## Element-plus

Element Plus 是为 Vue 3 打造的桌面端组件库，是原来 Element UI 的升级版