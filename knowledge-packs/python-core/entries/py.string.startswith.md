---
id: py.string.startswith
title: 判断开头或结尾
description: 看字符串是不是以某段内容开始或结束
language: python
category_id: programming.basics
module: str
origin: builtin
import: ""
qualname: "str.startswith() / str.endswith()"

object:
  id: string.text
  name: 字符串
  aliases: [文本, 字串, 开头, 结尾, 前缀后缀, string]

action:
  id: inspect.check
  name: 判断
  aliases: [判断, 检查, 看是否, 以什么开头, 是不是, startswith]

targets: []

utterances:
  direct:
    - 判断字符串开头
    - 检查是否以某个词开头
    - 判断字符串结尾
  questions:
    - 怎么判断字符串以什么开头
    - 如何检查文件名是不是以 log 开头
    - Python 怎么判断结尾是什么
  colloquial:
    - 想知道这行是不是以 http 开头
    - 这串是不是以 .py 结尾
  technical:
    - str.startswith
    - str.endswith
    - python string prefix check
  short_queries:
    - 开头
    - 结尾
    - startswith
    - endswith

status: tested
tested_versions: ["3.10", "3.11", "3.12", "3.13", "3.14"]
min_version: "3.0"
version_note: startswith / endswith 支持元组参数，各版本一致
sources:
  - Python 官方文档 str.startswith
  - Python 官方文档 str.endswith
---

# 判断开头或结尾

## 功能描述

输入字符串 + 一个或多个候选，输出 `True/False`：是不是以它们开头（或结尾）。

## 推荐代码

```python
line = "http://example.com/a.py"

print(line.startswith("http"))        # True
print(line.endswith(".py"))           # True

# 一次给多个候选，命中任意一个就 True
print(line.startswith(("http://", "https://")))   # True
print(line.endswith((".py", ".pyw")))             # True
```

## 语句解释

### .startswith(prefix)

判断开头，返回布尔值。区分大小写。

### .endswith(suffix)

判断结尾。注意它判断的是**字符串结尾**，不是“文件后缀”——路径带查询串时会误判。

### 传元组 `("http://", "https://")`

一次判断多种可能，比写 `or` 更清楚也更快。

## 原理解释

**一句话：** 拿开头那几个字符和目标比一比，一样就是 True。

**执行逻辑：**

1. 从字符串开头取前 N 个字符（N = 目标的长度）
2. 和目标逐字符比较
3. 全一样 → 返回 True；有一个不一样 → 返回 False
4. 传元组时，对每个候选重复 1–3，任意一个成功即 True
5. `endswith` 完全对称，只是从末尾往前取

**机器层（可跳过）：** 只比较目标长度那么几个字符，和原串多长无关。

**边界（从逻辑推出来）：**

- 第 1 步取的是固定长度，所以原串比目标短时直接 False，不会报错
- 逐字符比较区分大小写：`"Py".startswith("py")` 是 False
- `endswith` 比的是**字符串末尾**，所以带查询串的 URL（`a.py?x=1`）会判错——那要先拆 URL
- 用 `endswith` 判断后缀不安全（`"notpy".endswith("py")` 为真），文件后缀该用 `Path().suffix`
## 注意事项

- 区分大小写：`"Py".startswith("py")` 是 False。
- `endswith(".py")` 对 `"a.py?x=1"` 会返回 False，URL 场景要先用 `urlparse`。
- 别用 `startswith` 判断后缀，`"notpy".endswith("py")` 会误判。
- 判断“是哪种文件”时 `Path(p).suffix` 与 `endswith` 二选一，别混用。

## 使用场景

- 过滤日志行（找以 ERROR 开头的）。
- 判断 URL 协议。
- 快速筛文件名前缀，比如批量处理 `2026-` 开头的归档。
