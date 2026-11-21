---
id: py.os.listdir
title: 列出目录里的东西
description: 看一眼某个目录下有哪些文件和子目录
language: python
category_id: programming.filesystem
module: os

object:
  id: dir.list
  name: 目录内容
  aliases: [目录, 文件夹, 目录列表, 文件夹里有什么, listdir]

action:
  id: get.obtain
  name: 获取
  aliases: [列出, 拿到, 查看, 读取, list]

targets: []

utterances:
  direct:
    - 列出目录内容
    - 获取文件夹里的文件列表
    - 查看目录下有什么
  questions:
    - 怎么列出一个目录下的文件
    - 如何获取文件夹里所有文件名
    - Python 怎么知道文件夹里有几个文件
  colloquial:
    - 这个文件夹里都有些啥
    - 想把目录里的名字都拿出来
  technical:
    - os.listdir
    - os.scandir
    - pathlib iterdir
  short_queries:
    - 列出
    - listdir
    - 目录

status: tested
tested_versions: ["3.10", "3.11", "3.12", "3.13", "3.14"]
min_version: "3.0"
version_note: os.listdir / os.scandir 接口稳定；Path.iterdir 是 3.4 起
sources:
  - Python 官方文档 os.listdir
  - Python 官方文档 os.scandir
---

# 列出目录里的东西

## 功能描述

拿到一个目录下的所有条目名（文件和子目录混在一起，**不含子目录里的内容**）。

## 推荐代码

```python
import os
from pathlib import Path

print(os.listdir(".")[:5])          # 只有名字，字符串

for entry in os.scandir("."):        # 带类型信息，效率更好
    print(entry.name, entry.is_file())
    break

print([p.name for p in Path(".").iterdir()][:5])   # pathlib 风格
```

## 语句解释

### os.listdir(path)

返回名字列表，**不带路径**。想要完整路径得自己 `os.path.join(path, name)`。

### os.scandir(path)

返回条目对象，可以问 `is_file()` / `is_dir()`，而且类型信息是系统顺带给的，
比 `listdir` 再逐个 `stat` 快。

### Path(".").iterdir()

pathlib 写法，返回 `Path` 对象，能直接接 `.suffix`、`.stat()` 这些方法。

## 原理解释

`os.listdir` 底层是一次目录读取系统调用，只给出名字和（部分系统的）inode 信息，
类型得再查。`os.scandir` 把系统返回的目录项类型缓存下来，所以循环里判断
文件还是目录时不会每次都去问磁盘——这就是它比 `listdir` 快的原因。

**`listdir` 不递归**：它只给第一层，要看子目录里的东西得自己递归或用 `walk`。

## 注意事项

- 返回顺序是文件系统的顺序，**不保证有序**，要稳定输出就自己 `sorted()`。
- 只有名字没有路径，拼路径别用字符串加法。
- 目录里有隐藏文件也会返回（Linux 上以点开头的那些）。
- 目录很大时 `listdir` 会一次生成整个列表，占内存；遍历用 `scandir` 或 `iterdir`。

## 使用场景

- 扫描目录做批量处理。
- 统计文件数量、按类型分组。
- 做简单的文件浏览器。
