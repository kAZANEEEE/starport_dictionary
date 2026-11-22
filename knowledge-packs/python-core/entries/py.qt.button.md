---
id: py.qt.button
title: 按钮点击后做一件事
description: 点一下触发函数，界面程序最基础的交互
language: python
category_id: programming.filesystem
module: PySide6
origin: thirdparty
import: "from PySide6.QtWidgets import QPushButton"
qualname: "QPushButton.clicked.connect()"
signature: "btn = QPushButton(\"文字\")  btn.clicked.connect(函数)"
args:
  - name: "按钮文字"
    required: true
    accepts: "显示在按钮上的字符串"
    nesting: "可以，可以是变量"
  - name: "回调函数"
    required: true
    accepts: "点击时被调用的函数（不要加括号！）"
    nesting: "可以，常用 lambda 传参"
returns: "无返回值：connect 只是登记「点了我该叫谁」"
object:
  id: gui.button
  name: 按钮
  aliases: [按钮, 点击, 按键, 控件, button]
action:
  id: run.execute
  name: 执行
  aliases: [点击, 触发, 响应, 绑定, click]
targets: []
utterances:
  direct:
    - 按钮点击绑定函数
    - 点了按钮执行代码
    - 按钮怎么加事件
  questions:
    - PySide6 按钮点击怎么绑定
    - connect 里的函数为什么不能加括号
    - 点击后怎么传参数
  colloquial:
    - 点了按钮没反应
    - 想点一下就跑我的函数
  technical:
    - clicked.connect
    - 信号槽
    - lambda 传参
    - 按钮没反应
  short_queries:
    - 按钮
    - 点击
    - connect
status: tested
tested_versions: ["3.10", "3.11", "3.12", "3.13", "3.14"]
min_version: "3.9"
version_note: "PySide6 信号槽语法稳定；本机已装 6.12"
sources:
  - PySide6 官方文档 QPushButton
---

# 按钮点击后做一件事

## 功能描述

输入按钮文字 + 一个函数，输出绑定好的按钮：点击时那个函数被调用。

## 推荐代码

```python
from PySide6.QtWidgets import QApplication, QPushButton

app = QApplication([])

def on_click():
    print("被点了")

btn = QPushButton("点我")
btn.clicked.connect(on_click)     # 注意：传函数本身，不加括号
btn.click()                        # 模拟一次点击，验证绑定成功
print("按钮文字:", btn.text())
```

## 语句解释

### clicked.connect(函数)

把「被点击」这个信号连到函数上。这就是 Qt 的**信号槽**机制。

### 为什么不能写 `on_click()`

加括号是**立刻调用**并把返回值（None）连上去——点击时什么都不会发生。**这是「点了没反应」的第一大原因。**

### lambda 传参

`btn.clicked.connect(lambda: do(1))`，因为签名必须是无参函数。

## 原理解释

**一句话：** `connect` 只是在按钮身上登记「点了我该叫谁」，点击时才真的去叫它。

**执行逻辑：**

1. 创建按钮，内部维护一个「信号 → 回调列表」
2. `connect(f)` 把 f 加到这个列表里
3. 用户点击 → 按钮发出 `clicked` 信号
4. Qt 遍历回调列表，逐个调用
5. 回调里改界面，界面自动重绘

**机器层（可跳过）：** 信号发出后由事件循环分发，回调在**主线程**执行。

**边界（从逻辑推出来）：**

- 第 2 步是「登记」，所以可以给同一个信号连多个回调（都会执行）
- 第 4 步在主线程执行，所以回调里做耗时会**卡住整个界面**
- 因为第 1 步列表可增，重复 connect 会导致回调被调多次
- `clicked` 还给一个「是否选中」参数，需要时函数可以接收它

## 注意事项

- 传函数本身，不加括号。
- 需要参数用 `lambda`，注意别在 lambda 里写耗时逻辑。
- 回调里别做网络请求/大循环，会卡界面。
- 解绑用 `disconnect()`，否则重复连接会触发多次。

## 使用场景

- 点「开始」执行任务。
- 点「清空」重置表单。
- 点「保存」把界面数据写文件。
