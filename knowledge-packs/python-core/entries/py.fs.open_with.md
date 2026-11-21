---
id: py.fs.open_with
title: 逐行读取大文件
description: 一行一行处理，不把整个文件读进内存
language: python
category_id: programming.filesystem
module: builtins

object:
  id: file.content
  name: 文件内容
  aliases: [文件内容, 每一行, 文本行, 大文件, file lines]

action:
  id: get.obtain
  name: 获取
  aliases: [逐行读, 一行一行读, 读取, 遍历行, readline, readlines]

targets: []

utterances:
  direct:
    - 逐行读取文件
    - 一行一行处理文件
    - 读取大文件
  questions:
    - 怎么逐行读一个大文件
    - 如何边读边处理不占内存
    - readlines 和 for line in f 的区别
  colloquial:
    - 文件太大不能一次读进来
    - 想一行行处理日志
  technical:
    - with open
    - for line in f
    - readlines
    - 迭代文件对象
  short_queries:
    - 逐行
    - open
    - 大文件

status: tested
tested_versions: ["3.10", "3.11", "3.12", "3.13", "3.14"]
min_version: "3.0"
version_note: 文件对象迭代与 with 语法各版本一致
sources:
  - Python 官方文档 open
  - Python 官方教程 文件读写
---

# 逐行读取大文件

## 功能描述

输入文件路径，逐行产出内容（含行尾换行符），内存占用与文件大小无关。

## 推荐代码

```python
# 演示用：先造一个文件，实际使用时删掉这两行
from pathlib import Path
Path("logs.txt").write_text("line1\nline2\nline3\n", encoding="utf-8")

count = 0
with open("logs.txt", encoding="utf-8") as f:
    for line in f:
        text = line.rstrip("\n")
        if text.startswith("line"):
            count += 1

print("匹配行数:", count)
```

## 语句解释

### with open(...) as f

`with` 保证文件一定被关闭，即使中途抛异常。

### for line in f

文件对象本身可迭代，每行一次，**惰性读取**——这是处理大文件的正解。

### line.rstrip("\n")

每行末尾带换行符，比较前通常要去掉。用 `rstrip("\n")` 而不是 `strip()`，避免误删行首空格。

## 原理解释

`for line in f` 内部用缓冲区分块读（通常几 KB），再按行切给你，
所以内存里同时只有一个缓冲区 + 当前行。而 `f.read()` / `f.readlines()`
会把整个文件（或全部行）装进内存——大文件直接爆。

## 注意事项

- 必须写 `encoding="utf-8"`，否则 Windows 默认编码会把中文读坏。
- 行尾带 `\n`，比较前要处理。
- `readlines()` 一次性返回所有行，只适合小文件。
- 迭代文件对象时不要在循环里对该文件做别的读操作，位置会乱。

## 使用场景

- 处理几百 MB 的日志。
- 边读边过滤、边统计。
- 大文件转格式（读一行、处理、写一行）。
