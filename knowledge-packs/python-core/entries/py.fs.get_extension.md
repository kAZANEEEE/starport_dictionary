---
id: py.fs.get_extension
title: 获取文件后缀
description: 把文件名最后那一截后缀取出来
language: python
category_id: programming.filesystem
module: pathlib

object:
  id: file.extension
  name: 文件后缀
  aliases: [后缀, 扩展名, 文件扩展名, 文件名后缀, suffix, extension]

action:
  id: get.obtain
  name: 获取
  aliases: [取, 拿到, 得到, 读取, 提取, get, obtain]

targets: []

utterances:
  direct:
    - 获取文件后缀
    - 取出文件扩展名
    - 得到文件的后缀名
  questions:
    - 怎么获取文件后缀
    - 如何取出文件的扩展名
    - Python 怎么拿文件后缀
  colloquial:
    - 想把最后那个 .py 取出来
    - 文件名后面那串怎么单独拿到
  short_queries:
    - 后缀
    - 扩展名
    - suffix

status: tested
tested_versions: ["3.10", "3.11", "3.12", "3.13", "3.14"]
min_version: "3.4"
version_note: pathlib 从 3.4 就有，suffix 的行为一直没变
sources:
  - Python 官方文档 pathlib.Path.suffix
---

# 获取文件后缀

## 功能描述

从路径里取出最后一个后缀，返回带点号的字符串，比如 `".py"`。

## 推荐代码

```python
from pathlib import Path

file_path = Path("report.2026.tar.gz")
print(file_path.suffix)   # .gz
```

## 语句解释

### Path(...)

把字符串变成路径对象，只是为了能用 `.suffix` 这种写法。不会去磁盘上找这个文件。

### .suffix

返回最后一个后缀，**带点号**。没有后缀时返回空字符串，不是 `None`。

### print(...)

只是把结果打出来看，实际使用时直接拿 `.suffix` 的值去比较就行。

## 原理解释

`pathlib` 把路径拆成 `name`（最后一段）和 `suffix`（name 里最后一个点之后的部分）。

`report.2026.tar.gz` 的名字里有两个点，`.suffix` 只取最后一个，所以是 `.gz`。

## 注意事项

- 只要最后一个后缀，`tar.gz` 时拿不到 `.tar.gz`，要用 `.suffixes`。
- 以点开头的文件（`.bashrc`）会被认为没有后缀，返回空串。
- 返回值可能带大写（`.PY`），比较前通常要 `.lower()`。
- 后缀不代表文件真实类型，改个名字就能骗过它。

## 使用场景

- 按格式给文件分组。
- 决定用哪个解析器读取文件。
- 生成同名但不同格式的输出文件。
