---
id: py.qt.window
title: 打开一个窗口
description: PySide6 的最小可运行程序
language: python
category_id: programming.filesystem
module: PySide6
origin: thirdparty
install: "pip install PySide6"
import: "from PySide6.QtWidgets import QApplication, QMainWindow"
qualname: "QApplication + QMainWindow"
signature: "app = QApplication([])  →  win = QMainWindow()  →  app.exec()"
args:
  - name: "QApplication"
    required: true
    accepts: "一个程序只能有一个，必须最先创建；参数传 sys.argv 或 []"
    nesting: "不能嵌套创建第二个"
  - name: "窗口对象"
    required: true
    accepts: "QMainWindow（带菜单状态栏）或 QWidget（最简单）"
    nesting: "可以，一个窗口里可以放很多控件"
returns: "app.exec() 会阻塞运行事件循环（直到窗口关闭）；不调用 exec 就只是个对象，不显示"
object:
  id: gui.window
  name: 窗口
  aliases: [窗口, 界面, 主窗口, 窗体, window]
action:
  id: create.new
  name: 创建
  aliases: [创建, 打开, 显示窗口, 新建, window]
targets: []
utterances:
  direct:
    - 打开一个窗口
    - 创建 PySide6 窗口
    - 写个最小的界面程序
  questions:
    - PySide6 怎么开窗口
    - QApplication 是干什么的
    - 为什么程序一闪就退
  colloquial:
    - 想做个桌面程序，先弹个窗口
    - 按钮还没写，先把界面立起来
  technical:
    - QApplication
    - QMainWindow
    - exec 事件循环
    - 一闪而过
  short_queries:
    - 窗口
    - QMainWindow
    - 界面
status: tested
tested_versions: ["3.10", "3.11", "3.12", "3.13", "3.14"]
min_version: "3.9"
version_note: "PySide6 需 pip install；本机已装 6.12"
sources:
  - PySide6 官方文档 QApplication
  - PySide6 官方文档 QMainWindow
---

# 打开一个窗口

## 功能描述

输入无（或命令行参数），输出一个窗口；**必须调 `app.exec()` 才会真正进入界面循环并停在屏幕上**。

## 推荐代码

```python
import sys
from PySide6.QtWidgets import QApplication, QMainWindow

app = QApplication([])          # 一个程序只能有一个，最先创建

win = QMainWindow()
win.setWindowTitle("星港词典")
win.resize(800, 600)

print(win.windowTitle(), win.size().width())   # 不调用 exec 也能操作对象

# 真正显示并进入事件循环（会阻塞在这里，直到关窗口）
# win.show()
# sys.exit(app.exec())
```

## 语句解释

### QApplication([])

整个程序的事件循环载体。没有它，任何控件创建都会崩。

### win.show()

把窗口显示出来。

### app.exec()

进入事件循环：等待鼠标、键盘事件并分发。不调用它就等于「窗口创建完程序立刻结束」，也就是**一闪而过**。

## 原理解释

**一句话：** 控件只是内存里的对象，`app.exec()` 才把它们真正摆到屏幕上并开始"听"用户操作。

**执行逻辑：**

1. 创建 `QApplication`，准备好事件循环
2. 创建窗口和控件对象，设置属性
3. `show()` 把窗口标记为可见
4. `exec()` 进入循环：不断取事件（点击、输入、重绘）并分发给对应控件
5. 窗口关闭时循环退出，程序结束

**机器层（可跳过）：** 事件循环是一个阻塞的 while，靠操作系统把事件送进来唤醒它。

**边界（从逻辑推出来）：**

- 第 1 步必须在所有控件之前，且**只能一个**——重复创建会崩
- 第 4 步会阻塞，所以 `exec()` 之后的代码要等窗口关闭才执行
- 不调 `show()` 窗口不显示；不调 `exec()` 程序立刻退出（两个「一闪而过」的原因不同）
- 长任务直接写在 exec 之前或控件回调里会卡住界面——那是线程的活

## 注意事项

- `QApplication` 只能创建一个，且在控件之前。
- `exec()` 是阻塞的，不要指望它返回后继续干活。
- 打包成 exe 时要把 Qt 的插件一起打进去，否则运行时缺库。
- 界面卡死基本都是「在主线程里做了耗时操作」。

## 使用场景

- 桌面工具的主界面。
- 给脚本套一个简单操作界面。
- 学习 Qt 的第一步。
