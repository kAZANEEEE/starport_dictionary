---
id: py.fs.get_size
title: 获取文件大小
description: 一个文件占了多少字节
language: python
category_id: programming.filesystem
module: pathlib
origin: stdlib
import: "from pathlib import Path"
qualname: "pathlib.Path.stat().st_size"

object:
  id: file.size
  name: 文件大小
  aliases: [大小, 字节数, 体积, 占多少空间, size]

action:
  id: get.obtain
  name: 获取
  aliases: [取, 获取, 查, 算, getsize]

targets: []

utterances:
  direct:
    - 获取文件大小
    - 查看文件多少字节
    - 算文件体积
  questions:
    - 怎么获取文件大小
    - 如何把字节数转成 MB
    - 目录大小能直接取吗
  colloquial:
    - 想知道这个文件多大
    - 下载完看看有没有下全
  technical:
    - os.path.getsize
    - Path.stat().st_size
    - 格式化文件大小
  short_queries:
    - 文件大小
    - getsize
    - st_size

status: tested
tested_versions: ["3.10", "3.11", "3.12", "3.13", "3.14"]
min_version: "3.4"
version_note: "Path.stat 从 3.4 起；os.path.getsize 更老也一直能用"
sources:
  - Python 官方文档 os.path.getsize
  - Python 官方文档 pathlib.Path.stat
---

# 获取文件大小

## 功能描述

输入文件路径，输出它占的**字节数**（整数）；路径不存在抛 `FileNotFoundError`。

## 推荐代码

```python
import os
from pathlib import Path

Path("demo.bin").write_bytes(b"x" * 1500)

print(os.path.getsize("demo.bin"))          # 1500
print(Path("demo.bin").stat().st_size)      # 1500

def human(n: int) -> str:
    for unit in ("B", "KB", "MB", "GB"):
        if n < 1024:
            return f"{n:.1f} {unit}"
        n /= 1024
    return f"{n:.1f} TB"

print(human(os.path.getsize("demo.bin")))   # 1.5 KB
```

## 语句解释

### os.path.getsize(路径)

直接返回字节数，一步到位。

### Path(...).stat().st_size

`stat()` 拿到的是文件元数据（大小、时间、权限等），取 `st_size` 字段。要用其他字段时走这条路。

### 人读的格式化

自己按 1024 逐级换算。没有标准库函数直接给你 "1.5 MB"。

## 原理解释

**一句话：** 它只是问文件系统「这个文件登记的长度是多少」，不读文件内容。

**执行逻辑：**

1. 按路径找到目录项
2. 读出这条记录的元数据
3. 取其中的「长度」字段（字节数）
4. 返回这个整数

**机器层（可跳过）：** 一次 `stat` 系统调用，不碰文件内容，所以再大的文件也瞬间返回。

**边界（从逻辑推出来）：**

- 第 3 步拿的是**登记的字节数**，所以是磁盘上的逻辑大小，不代表实际占用的磁盘块（稀疏文件除外，`st_blocks` 才是占用）
- 第 1 步找不到文件就抛错，批量统计要自己跳过不存在的
- 目录也能 `stat`，但拿到的是目录项大小（几 KB），**不是里面所有文件之和**——要递归累加
- 因为只是查元数据，对网络盘/慢盘也可能卡一下，但没有读文件那么贵

## 注意事项

- 目录大小要递归累加，`getsize(目录)` 给的是目录本身的大小。
- 字节数转人读单位要自己写函数，1024 进制。
- 文件正被写入时读到的大小可能是旧值。
- 想按修改时间排序也用 `stat()` 的 `st_mtime`。

## 使用场景

- 下载/写入后校验大小是否一致。
- 批量统计目录体积。
- 按大小筛选或清理大文件。
