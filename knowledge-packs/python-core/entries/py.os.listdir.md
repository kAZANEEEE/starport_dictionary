---
id: py.os.listdir
title: 列出目录里的东西
description: 看一眼某个目录下有哪些文件和子目录
language: python
category_id: programming.filesystem
module: os
origin: stdlib
import: "import os"
qualname: "os.listdir"
signature: "os.listdir(path=\".\")"
args:
  - name: "path"
    required: false
    default: "\".\""
    accepts: "目录路径；默认当前目录"
    nesting: "可以，可以是变量"
returns: "列表：里面的文件和子目录名（只有名字、不含路径，且不递归）"

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

**一句话：** 拿到一个目录里所有东西的名字，只给名字、不给路径。

**执行逻辑：**

1. 打开指定目录，读出它里面的目录项
2. 每一项取出名字（不含上级路径）
3. 全部收集成列表返回
4. 只做这一层，**不会钻进子目录**

**机器层（可跳过）：** 一次目录读取，名字直接来自目录表，不需要打开文件。

**边界（从逻辑推出来）：**

- 第 2 步只给名字，所以想拼完整路径得自己 `os.path.join`（或改用 `Path` 的方法）
- 第 4 步不递归，子目录里的东西看不到——要递归用 `walk` 或 `rglob`
- 返回顺序是文件系统给的顺序，**不保证稳定**，要可比就 `sorted()`
- 目录很大时列表会一次性占内存，遍历用 `os.scandir` 更省
## 注意事项

- 返回顺序是文件系统的顺序，**不保证有序**，要稳定输出就自己 `sorted()`。
- 只有名字没有路径，拼路径别用字符串加法。
- 目录里有隐藏文件也会返回（Linux 上以点开头的那些）。
- 目录很大时 `listdir` 会一次生成整个列表，占内存；遍历用 `scandir` 或 `iterdir`。

## 使用场景

- 扫描目录做批量处理。
- 统计文件数量、按类型分组。
- 做简单的文件浏览器。
