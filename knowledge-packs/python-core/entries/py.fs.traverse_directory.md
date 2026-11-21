---
id: py.fs.traverse_directory
title: 遍历文件夹里所有文件
description: 递归找出一个目录下的全部文件
language: python
category_id: programming.filesystem

object:
  id: dir.list
  name: 目录内容
  aliases: [目录, 文件夹, 文件夹里有什么, 目录列表, listdir, directory]

action:
  id: traverse.walk
  name: 遍历
  aliases: [循环, 递归, 逐个处理, 走一遍, walk, iterate]

targets: []

utterances:
  direct:
    - 遍历文件夹
    - 递归遍历目录
    - 把目录下所有文件列出来
  questions:
    - 怎么遍历文件夹里所有文件
    - 如何递归列出目录下所有文件
    - Python 怎么走一遍整个目录
  colloquial:
    - 我想把一个文件夹里的东西全找出来
    - 文件夹里面还有文件夹，怎么全扫一遍
  goal_based:
    - 统计某个目录下有多少个文件
  short_queries:
    - 遍历
    - 目录
    - rglob

status: tested
tested_versions: ["3.10", "3.11", "3.12", "3.13", "3.14"]
min_version: "3.5"
version_note: rglob 从 3.5 起就有；3.12 加入了 walk()，但这里用的写法兼容更广
sources:
  - Python 官方文档 pathlib.Path.rglob
---

# 遍历文件夹里所有文件

## 功能描述

递归列出目录下的所有文件，包括子目录里的。

## 推荐代码

```python
from pathlib import Path

root = Path(".")
files = [p for p in root.rglob("*") if p.is_file()]

print(len(files))
for p in files[:5]:
    print(p)
```

## 语句解释

### Path(".")

当前目录。换成任意目录路径都行。

### .rglob("*")

递归匹配所有条目，把子目录里的也带出来。只想看一层用 `.glob("*")`。

### if p.is_file()

`rglob` 连目录也会一起返回，这个判断只留下文件。

### 列表推导式

把结果一次性收集成列表。文件特别多时改成生成器（去掉方括号），省内存。

## 原理解释

`rglob` 等价于“在每层目录上都展开一次 `glob`”，遇到子目录就继续往下走，
本质是广度/深度优先的目录树遍历，由标准库实现，不用自己写递归。

## 注意事项

- 目录里如果有几万文件，先 `len()` 再遍历，避免一次占满内存。
- 会跟随符号链接，可能绕成环；要排除可以用 `Path.walk()`（3.12+）或自己判断。
- 权限不足的子目录会直接抛 `PermissionError`，需要 `try/except` 跳过。
- 想按后缀筛，配合 `p.suffix == ".py"`，别用字符串 `endswith` 拼路径。

## 使用场景

- 批量处理某个项目里的所有源码。
- 统计目录规模和文件类型分布。
- 做索引、备份、搜索前的文件收集。
