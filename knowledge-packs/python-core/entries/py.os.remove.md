---
id: py.os.remove
title: 删除文件
description: 把一个文件从磁盘上删掉
language: python
category_id: programming.filesystem
module: os
origin: stdlib
import: "import os"
qualname: "os.remove() / os.unlink()"
signature: "os.remove(path) / Path(path).unlink(missing_ok=False)"
args:
  - name: "path"
    required: true
    accepts: "要删的文件路径（不能是目录）"
    nesting: "可以"
  - name: "missing_ok"
    required: false
    default: "False"
    accepts: "True = 文件本来不在也不报错（仅 Path.unlink 支持）"
    nesting: "一般直接写 True"
returns: "None：没有返回值；副作用是文件被删除（进不了回收站）"

object:
  id: file.path
  name: 文件路径
  aliases: [文件, 路径, 文件名, 目标文件, file]

action:
  id: delete.remove
  name: 删除
  aliases: [删除, 删掉, 移除, 清掉, remove, unlink]

targets: []

utterances:
  direct:
    - 删除文件
    - 删掉指定文件
    - 移除文件
  questions:
    - 怎么删除一个文件
    - 文件不存在会报错吗
    - 如何删除整个文件夹
  colloquial:
    - 处理完的文件想删掉
    - 临时文件要清理
  technical:
    - os.remove
    - os.unlink
    - os.rmdir
    - shutil.rmtree
  short_queries:
    - 删文件
    - remove
    - rmtree

status: tested
tested_versions: ["3.10", "3.11", "3.12", "3.13", "3.14"]
min_version: "3.0"
version_note: "os.remove 与 os.unlink 是同一个函数；shutil.rmtree 删目录树"
sources:
  - Python 官方文档 os.remove
  - Python 官方文档 shutil.rmtree
---

# 删除文件

## 功能描述

输入文件路径，把它从磁盘上移除；文件不存在抛 `FileNotFoundError`，路径是目录则抛 `IsADirectoryError`。

## 推荐代码

```python
import os
from pathlib import Path

Path("temp.txt").write_text("x", encoding="utf-8")
os.remove("temp.txt")

Path("temp2.txt").write_text("y", encoding="utf-8")
Path("temp2.txt").unlink(missing_ok=True)   # 不存在也不报错

# 删整个目录树要小心
import shutil
Path("dir_a").mkdir(exist_ok=True)
shutil.rmtree("dir_a")
print("删完了")
```

## 语句解释

### os.remove(路径)

删文件。`os.unlink` 是同一个函数的别名。

### Path(...).unlink(missing_ok=True)

pathlib 写法，`missing_ok=True` 让「文件本来就不在」不报错。

### shutil.rmtree(目录)

递归删整个目录（含里面的文件）。**它只认目录**，删文件要用 `remove`。

## 原理解释

**一句话：** 它只是把目录里这个文件名摘掉；真正的数据块等没人引用之后才被系统回收。

**执行逻辑：**

1. 按路径在目录里找到这个名字
2. 检查它是不是文件（是目录就报错）
3. 把这个目录项从目录里摘掉
4. 如果这个文件的链接数为 0、也没程序打开它，数据块标记为可复用

**机器层（可跳过）：** 删除只是改元数据，所以瞬间完成；数据是否真的被擦除取决于文件系统。

**边界（从逻辑推出来）：**

- 第 3 步只摘名字，所以文件被别的程序打开着时，Windows 会直接拒绝删除
- 因为只改元数据，删除不可撤销——**没有回收站**
- 第 2 步说明它不删目录，删目录要 `rmdir`（空目录）或 `rmtree`（整棵树）
- 文件不存在时第 1 步就失败，所以批量删除要自己判存在或 `missing_ok=True`

## 注意事项

- 删了就没了，没有回收站；批量删之前先打印一遍要删的路径。
- `rmtree` 极其危险，路径变量拼错可能删掉工作目录——**执行前把绝对路径打出来确认**。
- 正在被打开的文件在 Windows 删不掉（`PermissionError`）。
- 想「移到回收站」得用第三方库 `send2trash`，标准库做不到。

## 使用场景

- 清理临时文件和中间产物。
- 处理完的源文件归档后删除。
- 测试结束后清理造出来的文件。
