---
id: py.fs.get_extension
title: 获取文件后缀
description: 把文件名最后那一截后缀取出来
language: python
category_id: programming.filesystem
module: pathlib
origin: stdlib
import: "from pathlib import Path"
qualname: "pathlib.Path.suffix"
signature: "Path(path).suffix"
args:
  - name: "path"
    required: true
    accepts: "文件路径，字符串或 Path"
    nesting: "可以，可以是变量或函数返回值"
returns: "字符串：带点的后缀，如 \".gz\"；没有后缀时返回空字符串"

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

**一句话：** 和白拿一样简单——从路径里切出最后一个后缀，返回带点的那一串。

**执行逻辑：**

1. 把路径字符串变成路径对象（只是解析，不读磁盘）
2. 从后往前找最后一个 `.`，切下它后面的部分
3. 把这一截原样返回（**不改大小写、不去空格**）

**机器层（可跳过）：** 一次从右往左的字符串扫描，找到点就停。

**边界（从逻辑推出来）：**

- 只切一次，所以 `a.tar.gz` 得到 `.gz`，不是 `.tar.gz`
- 找不到点就返回空字符串 `""`（不是 None，也不是报错）
- 以点开头的文件名（`.env`）会被当成「没有后缀」——因为那个点被当作隐藏文件标记
- 返回值可能带大写，调用方需要自己决定要不要 `.lower()`
## 注意事项

- 只要最后一个后缀，`tar.gz` 时拿不到 `.tar.gz`，要用 `.suffixes`。
- 以点开头的文件（`.bashrc`）会被认为没有后缀，返回空串。
- 返回值可能带大写（`.PY`），比较前通常要 `.lower()`。
- 后缀不代表文件真实类型，改个名字就能骗过它。

## 使用场景

- 按格式给文件分组。
- 决定用哪个解析器读取文件。
- 生成同名但不同格式的输出文件。
