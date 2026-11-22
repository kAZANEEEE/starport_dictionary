---
id: py.os.chdir
title: 切换工作目录
description: 让后面的相对路径都以新目录为基准
language: python
category_id: programming.filesystem
module: os
origin: stdlib
import: "import os"
qualname: "os.chdir()"
signature: "os.chdir(path)"
args:
  - name: "path"
    required: true
    accepts: "要切换到的目录路径（相对或绝对都行）"
    nesting: "可以，常配合 Path(__file__).parent 用"
returns: "None：没有返回值；副作用是**整个进程**的相对路径基准都变了"
object:
  id: file.path
  name: 文件路径
  aliases: [路径, 工作目录, 当前目录, 切换, cwd]
action:
  id: modify.change
  name: 修改
  aliases: [切换, 改目录, 进入目录, 设置工作目录, chdir]
targets: []
utterances:
  direct:
    - 切换工作目录
    - 进入某个目录
    - 改变当前路径
  questions:
    - 怎么切换到别的目录
    - chdir 之后相对路径怎么变
    - 切换目录会影响别的代码吗
  colloquial:
    - 想把工作目录挪到数据文件夹
    - 每次都要写长路径，想先切进去
  technical:
    - os.chdir
    - 工作目录
    - 相对路径基准
  short_queries:
    - 切换目录
    - chdir
    - 工作目录
status: tested
tested_versions: ["3.10", "3.11", "3.12", "3.13", "3.14"]
min_version: "3.0"
version_note: "os.chdir 各版本一致"
sources:
  - Python 官方文档 os.chdir
---

# 切换工作目录

## 功能描述

输入一个目录路径，把它设成当前工作目录；之后的相对路径都以它为基准。

## 推荐代码

```python
import os
from pathlib import Path

Path("work/inner").mkdir(parents=True, exist_ok=True)
Path("work/inner/a.txt").write_text("x", encoding="utf-8")

before = os.getcwd()
os.chdir("work/inner")
print(Path("a.txt").exists())     # True —— 相对路径换基准了
os.chdir(before)                  # 记得切回去
print(Path("a.txt").exists())     # False
```

## 语句解释

### os.chdir(路径)

切换当前进程的工作目录。目录不存在抛 `FileNotFoundError`。

### 先用 getcwd 存一份

因为是全局状态，改完要能回来。忘记切回是常见 bug。

### 更安全的替代

用 `Path(...)` 拼绝对路径，就不用切目录了——**大多数情况这不是必须的**。

## 原理解释

**一句话：** 它改的是「这个进程认为自己在哪个目录」，不是一个局部变量。

**执行逻辑：**

1. 检查目标路径是否存在、是不是目录
2. 把进程的工作目录字段改成它
3. 之后所有相对路径解析，都从这个新目录开始算

**机器层（可跳过）：** 内核里每个进程有一个当前目录指针，切换就是改这个指针。

**边界（从逻辑推出来）：**

- 第 2 步改的是**进程级**状态，所以别处代码的相对路径也会跟着变——这是它危险的根源
- 第 3 步说明「先 chdir 再写相对路径」能省事，但会让函数有隐藏的全局依赖
- 多线程里 chdir 会影响所有线程，不是一个线程一个目录
- 因为第 1 步要校验，目录不存在会直接抛错

## 注意事项

- 少用。用绝对路径拼 `Path` 更安全，函数也不会偷偷依赖全局状态。
- 如果必须用，先 `before = os.getcwd()`，用完切回去。
- 多线程里别用 chdir。
- 切目录不改变 `__file__` 指向的脚本位置。

## 使用场景

- 运行一个「必须在特定目录下跑」的外部命令前临时切换。
- 处理别人写的脚本（它假定工作目录固定）。
- 交互式环境里偷懒少写路径。
