---
id: py.fs.check_extension
title: 判断文件后缀
description: 只看文件名后缀，判断是不是某一种格式
language: python
category_id: programming.filesystem

object:
  id: file.extension
  name: 文件后缀
  aliases: [后缀, 扩展名, 文件扩展名, 文件名后缀, suffix, extension]

action:
  id: inspect.check
  name: 判断
  aliases: [检查, 验证, 确认, 判断是否, 看看是不是, 检测, check]

targets: [".py", ".txt", ".jpg", ".png"]

constraints:
  - key: case_sensitive
    values: ["true", "false"]
    default: "false"

utterances:
  direct:
    - 判断文件后缀
    - 检查文件扩展名
    - 判断文件扩展名
    - 验证文件后缀
  questions:
    - 怎么判断文件后缀
    - 如何检查文件扩展名
    - 怎么知道文件是什么后缀
    - Python 如何判断文件是否以 .py 结尾
  colloquial:
    - 看看是不是 py 文件
    - 这个文件是什么格式
    - 我想知道文件名最后面是什么
  goal_based:
    - 只处理 Python 文件
    - 按后缀筛选文件
    - 根据文件类型执行不同操作
  technical:
    - pathlib suffix
    - Path.suffix
    - check file extension
    - Python extension validation
  short_queries:
    - 后缀
    - 扩展名
    - suffix
    - .py

ambiguity:
  - note: 如果用户要的是“这个文件到底是什么格式”，光看后缀不够，得读文件头
    candidate_ids: [py.fs.real_type]

related_ids:
  - py.fs.get_extension
  - py.fs.get_suffixes
  - py.fs.traverse_directory

status: tested
tested_versions: ["3.10", "3.11", "3.12", "3.13", "3.14"]
min_version: "3.10"
version_note: 3.9 没实测过；写法本身通用
sources:
  - Python 官方文档 pathlib.Path.suffix
---

# 判断文件后缀

## 功能描述

取出文件名的最后一个后缀，统一转成小写再比较，判断它是不是 `.py` 文件。

## 推荐代码

```python
from pathlib import Path

file_path = Path("example.PY")

if file_path.suffix.lower() == ".py":
    print("这是一个 Python 文件")
```

## 语句解释

### Path()

创建一个路径对象，让后面的操作都走 pathlib 的接口，而不是手工拼字符串。

### .suffix

取路径最后一个后缀，返回值带点号（`".PY"`）。没有后缀时返回空字符串，不会报错。

### .lower()

把 `".PY"` 转成 `".py"`。Windows 上文件名大小写不敏感，不转会把大写的 `.PY` 误判成别的文件。

### ==

字符串相等比较。`suffix` 返回的一定带点，所以右边也要写 `.py` 而不是 `py`。

## 原理解释

`Path.suffix` 拿的是路径最后一段（`name`），从**最后一个点**往后切。所以：

- `a/b.py` → `.py`
- `a/archive.tar.gz` → `.gz`
- `a/Makefile` → `""`
- `a/.bashrc` → `""`

以点开头的文件被当作「没有后缀」，因为那个点是隐藏文件标记，不是后缀分隔符。

## 注意事项

- 只取最后一个后缀，`archive.tar.gz` 得到 `.gz`；要全部用 `.suffixes`。
- 后缀不代表真实格式。把 `a.txt` 改名成 `a.jpg`，`suffix` 照样返回 `.jpg`。
- 要不要忽略大小写取决于业务，别默认 `.lower()` 就完事。
- 路径对象没有后缀时 `.suffix` 是空字符串，判断不会抛异常，但要留意这个边界。

## 使用场景

- 扫描目录时只挑某一种格式的文件。
- 上传文件前做一次粗略校验。
- 按后缀分流，交给不同的处理函数。
