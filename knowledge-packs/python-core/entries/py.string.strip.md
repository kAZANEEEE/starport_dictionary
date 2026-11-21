---
id: py.string.strip
title: 去掉首尾空白
description: 清掉字符串两端的空格、换行、制表符
language: python
category_id: programming.basics
module: str

object:
  id: string.text
  name: 字符串
  aliases: [文本, 字串, 空白, 多余空格, string]

action:
  id: modify.change
  name: 修改
  aliases: [去掉, 清除, 清理, 删除, 去除, strip]

targets: []

utterances:
  direct:
    - 去掉首尾空格
    - 清除字符串两端的空白
    - 删除换行符
  questions:
    - 怎么去掉字符串前后的空格
    - 如何清理读进来的那一行的换行
    - Python 怎么去掉多余空白
  colloquial:
    - 读进来的每行后面带个换行，想去掉
    - 用户输入前后老是多空格
  technical:
    - str.strip
    - str.lstrip
    - str.rstrip
    - python trim string
  short_queries:
    - 去空格
    - 空白
    - strip

status: tested
tested_versions: ["3.10", "3.11", "3.12", "3.13", "3.14"]
min_version: "3.0"
version_note: strip / lstrip / rstrip 行为稳定
sources:
  - Python 官方文档 str.strip
---

# 去掉首尾空白

## 功能描述

输入一个字符串，输出**首尾**空白被删掉的版本（中间的空格保留），返回新字符串。

## 推荐代码

```python
line = "  你好，世界  \n"
print(repr(line.strip()))    # '你好，世界'

print(repr("  a  ".lstrip()))  # 'a  '  只去左边
print(repr("  a  ".rstrip()))  # '  a'  只去右边

print(repr("xxhixx".strip("x")))  # 'hi'  去掉指定的字符
```

## 语句解释

### .strip()

不带参数时，去掉首尾所有空白字符：空格、`\t`、`\n`、`\r`。

### .lstrip() / .rstrip()

只处理左边或右边。读文件时用 `rstrip("\n")` 去行尾换行最常见。

### .strip("x")

带参数时，参数是“字符集合”，**不是子串**：`strip("xy")` 会去掉首尾所有的 x 和 y。

## 原理解释

`strip` 从两端往中间扫描，遇到第一个“不属于要删的字符集”就停。
它返回**新字符串**，原字符串不变（字符串不可变）。

不带参数时判断的是 `str.isspace()`，所以中文全角空格（`\u3000`）也会被去掉。

## 注意事项

- 只去首尾，中间的空格不动；要把中间多空格压成一个用 `" ".join(s.split())`。
- `strip("ab")` 会删掉首尾所有 a 和 b，不是删掉子串 "ab"——这是常见误解。
- 字符串不可变，必须重新赋值：`s = s.strip()`。
- 读 csv 时先去空白再分割，比切完再挨个 strip 麻烦少。

## 使用场景

- 清理用户输入。
- 处理文件的每一行（去掉行尾换行）。
- 解析配置值时去掉多余空白。
