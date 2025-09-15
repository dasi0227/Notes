## 前端工程化

工程化 = 用工具、规范、接口让开发变得规范和专业
- 模块化：代码拆分、职责清晰，避免“一个 JS 文件统治世界”
- 自动化：由框架实现打包、压缩、转译、热更新，而不是手搓
- 组件化：UI 组件封装复用
- 规范化：Lint、Prettier、Git 提交规范、接口文档标准、分支策略等

前后端分离模式：前端只做视图渲染和交互逻辑，后端只提供接口和业务处理，彼此靠接口通信，互不嵌套、互不部署
- 开发分离
    - 前端项目使用 Vue/React 开发，启动在 localhost:3000
    - 后端项目使用 SpringBoot/Django/Node.js，启动在 localhost:8080
- 部署分离
    - 前端部署在 CDN、Nginx、OSS、GitHub 等
    - 后端部署到服务器上，跑 API 服务

技术栈
1. ECMAScript 6：Vue3 代码的语法规范
2. Node.js：前端项目的运行时环境
3. npm：依赖管理工具，用来安装组件库、工具库
4. vite：前端构建工具，启动快、热更新快
5. vue3：前端主框架，轻量、响应式、支持组合式 API
6. router：通过路由来切换不同页面
7. pinia：状态管理工具，专门处理组件之间的数据共享
8. axios：封装了 ajax 技术，实现前后端交互
9. Element Plus：UI 组件库，用来快速构建界面

## Node.js

Node.js 是基于 Chrome 的 V8 引擎构建的运行时环境，就像 Java 有 JVM，JS 就有 Node.js
- 让 JS 代码脱离浏览器，直接跑在服务器上
- 是 Vue/React 框架的运行环境
- 统一语言栈，做全栈开发更简单

## npm

npm（Node Package Manager）是 Node.js 的包管理工具，职责是下载、安装、更新和卸载 JavaScript 依赖库和工具包
- 下载、安装和更新别人写好的库：`npm install axios`
- 管理项目依赖：`npm install` 可以一键装好项目中 package.json 文件声明的所有包
- 提供项目运行脚本：`npm run dev` 可以执行 package.json 里配置自定义命令
- 发布自己的库：`npm publish` 可以让其他人使用你自己写的包

包（package）是 npm 的最小单位，一切都可以称为包，具体可以区分为：
- 库（library）：一组功能模块的集合，用户代码主动调用它
- 工具（tool）：用来辅助开发流程的，比如构建、格式化、测试、打包、启动服务器
- 框架（framework）：提供一整套开发结构、约定和运行流程，用户代码被它调用
- 插件（plugin）：为工具或框架提供扩展功能，要被宿主加载使用

包仓库系统（registry）：与 Github 不同，Github 存储的是源代码，而 npm 仓库存储的是压缩包
- 官方仓库地址是 https://registry.npmjs.org/ ，不作为网页使用，而是作为网络接口，接收 HTTP 请求，响应请求的压缩包
- 官方可视化网站是 https://www.npmjs.com/ ，在这查找包的元信息
- 镜像仓库地址是 https://registry.npmmirror.com/ ，是对官方仓库的一个代理，常用于国内加速

常见命令
- npm init：让你输入项目信息，用于在当前目录下创建一个新的 package.json 文件，-y 选项可以自动填入默认值
- npm install：安装 package.json 里声明的所有依赖，没有参数时，默认安装的是生产依赖（dependencies 和 devDependencies）
- npm install 包名：安装单个包，默认装到 dependencies
- npm uninstall 包名：卸载单个包
- npm update：按照 package.json 的版本规则去更新依赖
- npm ls：查看当前项目的全部依赖
- npm run 脚本名：运行定义在 package.json 的 "scripts" 字段中
- npm config get registry：获取仓库地址
- npm config set registry 地址：设置仓库地址
- npm login：登陆 npm 账号
- npm publish：发布包到 npm
- npm unpublish：删除自己发布的包

依赖（dependency）：项目运行时所需要的外部包
- package.json 中的 dependencies 字段：记录了项目运行时需要的包，会打包进最终项目中，每次运行 `npm install xxx`，都会自动添加一个记录，也可以自己手动添加
- package.json 中的 devDependencies 字段：记录了项目开发时需要的包，通常是构建工具、测试框架、格式化器、打包器等，不会上传部署，每次运行 `npm install xxx包名 --save-dev`，都会自动添加一个记录
- node_modules 目录：是依赖的实际存储位置，通常不上传到 Git 仓库，只上传 package.json
