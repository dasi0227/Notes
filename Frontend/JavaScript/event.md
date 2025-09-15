## 概述

事件：是浏览器或用户交互触发的行为
- 利用元素的属性绑定：onXXX，如 onclick, onchange 等
- 通过 DOM 编程动态绑定：DOM0，DOM2

事件对象 event，承载了本次交互事件的所有上下文信息，常用属性／方法包括
- type：事件类型
- target：触发事件的最初元素
- currentTarget：当前执行处理函数的元素
- clientX/clientY：如果是鼠标事件，可以获取鼠标的视口坐标
- button：如果是鼠标事件，可以获取按键编号
- key：如果是键盘事件，可以获取按键值
- code：如果是键盘事件，可以获取按键编码
- timeStamp：事件发生的时间戳（毫秒）
- preventDefault()：阻止浏览器默认行为，如链接跳转和表单提交
- stopPropagation()：阻止事件继续冒泡／捕获

## 常见事件类型

鼠标事件
- click：在目标元素上按下并释放主按钮时触发
- dblclick：在系统双击阈值内连续两次触发 click 后触发
- mousedown：按下任意鼠标按钮时即时触发
- mouseup：释放鼠标按钮时触发
- mousemove：鼠标指针在元素内移动时持续触发，频率高
- contextmenu：在目标元素上点击次按钮或触发上下文菜单快捷键时触发

键盘事件
- keydown：按下任意键时立即触发，可用于检测按键开始
- keyup：释放按键时触发，可用于检测按键结束

表单事件
- input：用户每次修改 \<input>、\<textarea> 或可编辑区域的值时即时触发
- change：元素值更改并失去焦点后触发，常用于选项或文本框的最终确认
- focus：元素获得焦点时触发，可用于高亮或校验前准备
- blur：元素失去焦点时触发，可用于即时校验或样式恢复
- submit：表单提交时触发，常用 event.preventDefault() 阻止默认提交行为
- reset：表单重置时触发，可用于恢复自定义状态或清理副作用

## DOM0 事件模型

通过元素的事件属性直接指定事件处理函数
- 不支持捕获
- 每个元素的每种事件只能绑定一个函数，后一个会覆盖前一个

流程
1. 获取目标元素：const btn = document.getElementById('myButton')
2. 绑定处理函数：btn.onclick = function(event) {}
3. 每次用户交互都会隐式执行处理函数，也可以在脚本显式调用 btn.onclick()
4. 移除绑定：btn.onclick = null

this：在非严格模式下，处理函数的 this 指向绑定该事件属性的元素

window.onload：在所有资源（HTML、CSS、图片、脚本）加载完毕后触发一次，用于初始化全局逻辑