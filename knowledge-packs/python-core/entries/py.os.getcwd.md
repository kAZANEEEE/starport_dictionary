---
id: py.os.getcwd
title: 获取当前工作目录
description: 程序现在站在哪个目录里
language: python
category_id: programming.filesystem
module: os

object:
  id: file.path
  name: 文件路径
  aliases: [路径, 当前目录, 当前路径, 工作目录, 所在目录, cwd]

action:
  id: get.obtain
  name: 获取
  aliases: [取, 拿到, 查看, 读到, get]

targets: []

utterances:
  direct:
    - 获取当前工作目录
    - 查看当前路径
    - 拿到程序所在的目录
  questions:
    - 怎么获取当前工作目录
    - 如何知道程序现在在哪个目录
    - Python 怎么打印当前路径
  colloquial:
    - 现在是在哪个文件夹里跑的
    - 相对路径到底相对哪儿
  technical:
    - os.getcwd
    - pathlib cwd
    - os.chdir
  short_queries:
    - 当前目录
    - cwd
    - getcwd

status: tested
tested_versions: ["3.10", "3.11", "3.12", "3.13", "3.14"]
min_version: "3.0"
version_note: os.getcwd 一直没变；pathlib 的 Path.cwd() 是 3.4 起
sources:
  - Python 官方文档 os.getcwd
---

# 获取当前工作目录

## 功能描述

问程序“我现在站在哪个目录”。相对路径都是相对它算的。

## 推荐代码

```python
import os
from pathlib import Path

print(os.getcwd())
print(Path.cwd())      # 效果一样，返回 Path 对象
```

## 语句解释

### os.getcwd()

返回字符串形式的当前工作目录。cwd = current working directory。

### Path.cwd()

同样的事，但返回 `Path` 对象，后面接 `.joinpath()` 这些方法更方便。

## 原理解释

“当前工作目录”是**进程级**的状态，不是文件所在的位置。它由启动进程时的目录决定
（双击运行通常是程序所在目录，从命令行运行就是命令提示符所在目录），
之后可以被 `os.chdir()` 改掉。

所以同一个相对路径 `"data.txt"`，在不同启动方式下指向的文件可能完全不同——
这是“明明文件在，却报 FileNotFoundError”最常见的原因。

## 注意事项

- 工作目录 ≠ 脚本所在目录。要拿脚本自己的目录用 `Path(__file__).parent`。
- `os.chdir()` 是全局副作用，改完之后所有相对路径都变，慎用。
- 打包成 exe 后工作目录常常不是 exe 所在目录。
- 路径拼接别用字符串相加，用 `Path(...) / "sub"` 或 `os.path.join`。

## 使用场景

- 报错时把工作目录打出来，便于定位路径问题。
- 启动时把工作目录切到数据目录。
- 拼绝对路径之前先确认基准目录。
