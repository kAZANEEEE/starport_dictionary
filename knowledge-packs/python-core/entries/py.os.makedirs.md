---
id: py.os.makedirs
title: 创建目录（含上级）
description: 建目录，父目录不存在就一起建
language: python
category_id: programming.filesystem
module: os

object:
  id: dir.list
  name: 目录内容
  aliases: [目录, 文件夹, 上级目录, 目录层级, mkdir]

action:
  id: create.new
  name: 创建
  aliases: [建, 新建, 创建, 生成, mkdir, create]

targets: []

utterances:
  direct:
    - 创建目录
    - 递归创建文件夹
    - 新建多级目录
  questions:
    - 怎么创建目录
    - 如何一次性建好多层文件夹
    - 目录已存在时报错怎么办
  colloquial:
    - 想建个文件夹，但上级目录也没有
    - 写文件前先把目录准备好
  technical:
    - os.makedirs
    - os.mkdir
    - pathlib mkdir parents
    - exist_ok
  short_queries:
    - 建目录
    - mkdir
    - makedirs

status: tested
tested_versions: ["3.10", "3.11", "3.12", "3.13", "3.14"]
min_version: "3.2"
version_note: os.makedirs 的 exist_ok 参数从 3.2 起
sources:
  - Python 官方文档 os.makedirs
---

# 创建目录（含上级）

## 功能描述

建目录。用 `makedirs` 的话，中间缺的父目录会一起建出来。

## 推荐代码

```python
import os
from pathlib import Path

os.makedirs("a/b/c", exist_ok=True)      # a、b、c 一起建；已存在也不报错
print(os.path.isdir("a/b/c"))

Path("x/y").mkdir(parents=True, exist_ok=True)   # pathlib 写法
print(Path("x/y").is_dir())
```

## 语句解释

### os.makedirs(path, exist_ok=True)

递归建目录。**`exist_ok=True` 是关键**：目录已存在时不再抛 `FileExistsError`。

### os.mkdir(path)

只建一层。父目录不存在直接抛 `FileNotFoundError`。

### Path(...).mkdir(parents=True, exist_ok=True)

pathlib 等价写法。`parents=True` 相当于 makedirs 的递归行为。

## 原理解释

**一句话：** 建目录，中间缺的父目录它也帮你一起建。

**执行逻辑：**

1. 把路径拆成一段段（比如 `a/b/c` → `a`、`b`、`c`）
2. 从最前面开始，逐段检查：这一段存在吗
3. 不存在就建一个；存在就跳过
4. 一直到最末一段建完为止
5. 每一段都是一次独立的建目录动作

**机器层（可跳过）：** 底层是多次 `mkdir` 系统调用，不是一次原子操作。

**边界（从逻辑推出来）：**

- 第 3 步「跳过」是靠 `exist_ok=True` 实现的；不传这个参数，已存在时会抛 `FileExistsError`
- 第 5 步说明它是多步操作，两个进程同时建同一路径可能互相撞，`exist_ok` 能兜住
- 如果中间某段位置上已经是个**文件**，第 3 步之后的建目录必然失败
- 权限不足会停在某一层并抛 `PermissionError`，前面已建的目录会留着
## 注意事项

- 不加 `exist_ok=True`，目录已存在就抛 `FileExistsError`，这是最常见的坑。
- 路径里有文件占位（同名文件已存在）时，无论 `exist_ok` 都会报错。
- 权限不足抛 `PermissionError`，Windows 上还有路径过长的问题。
- 别在循环里反复 makedirs，先建一次再写文件。

## 使用场景

- 写文件前先保证输出目录存在。
- 按日期建归档目录。
- 程序首次运行初始化数据目录。
