---
id: py.fs.exists
title: 判断文件或目录是否存在
description: 看一个路径到底有没有东西
language: python
category_id: programming.filesystem

object:
  id: file.exists
  name: 文件是否存在
  aliases: [在不在, 有没有这个文件, 存在, 存在性, exist, exists]

action:
  id: inspect.check
  name: 判断
  aliases: [检查, 判断是否, 确认, 看看, 验证, check]

targets: []

utterances:
  direct:
    - 判断文件是否存在
    - 检查路径在不在
    - 判断目录是否存在
    - 检查文件有没有
  questions:
    - 怎么判断文件存不存在
    - 如何检查一个路径是不是存在
    - Python 怎么知道文件在不在
    - 怎么区分文件还是目录
  colloquial:
    - 这个文件到底有没有
    - 不确定那个 txt 在不在
    - 程序跑之前想先看看文件在不在
  goal_based:
    - 读文件前先判断存在
    - 存在就覆盖不存在就新建
  technical:
    - pathlib exists
    - os.path.exists
    - os.path.isfile
    - python check file exists
  short_queries:
    - 存在
    - 在不在
    - exists
    - isfile

status: tested
tested_versions: ["3.10", "3.11", "3.12", "3.13", "3.14"]
min_version: "3.4"
version_note: Path.exists / is_file / is_dir 从 3.4 起，行为稳定
sources:
  - Python 官方文档 pathlib.Path.exists
  - Python 官方文档 pathlib.Path.is_file
---

# 判断文件或目录是否存在

## 功能描述

问一个路径到底有没有东西，以及它是文件还是目录。

## 推荐代码

```python
from pathlib import Path

p = Path("maybe.txt")

print(p.exists())   # 有没有东西（文件或目录都算）
print(p.is_file())  # 是不是文件
print(p.is_dir())   # 是不是目录
```

## 语句解释

### .exists()

路径指向的任何东西存在就返回 True。**文件和目录都算**，不区分。

### .is_file() / .is_dir()

区分类型。`is_file()` 为真时 `is_dir()` 一定为假，反之亦然。

### p

只是路径对象，`exists()` 才真的去问操作系统。

## 原理解释

这几个方法底层都是调操作系统的 `stat`：向文件系统询问“这个路径有对应条目吗、是什么类型”。

**所以它是一次真实的磁盘查询**，不是读缓存——放在循环里检查几万个路径会明显变慢。

## 注意事项

- `exists()` 只回答“存在”，不回答“可读”。文件存在但没权限，读的时候照样报错。
- 目录也算存在。要确认“是个文件”必须用 `is_file()`。
- 路径里有拼写错误、用了相对路径但工作目录不对，都会得到 False——**False 不一定等于文件不存在**。
- 判断完再操作之间存在时间窗口（TOCTOU），对并发环境不严格；稳妥做法是直接操作并捕获异常。
- 断开的网络盘/权限不足的路径可能返回 False 而不是报错。

## 使用场景

- 读配置前先判断文件在不在，给出更友好的提示。
- 决定“存在就覆盖、不存在就新建”。
- 扫描结果去重时过滤掉目录。
