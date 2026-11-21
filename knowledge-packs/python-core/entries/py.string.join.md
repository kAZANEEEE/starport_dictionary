---
id: py.string.join
title: 把列表拼成字符串
description: 用分隔符把多个字符串连成一个
language: python
category_id: programming.basics
module: str

object:
  id: string.text
  name: 字符串
  aliases: [文本, 字串, 多个字符串, 一段文字, string]

action:
  id: create.new
  name: 创建
  aliases: [拼接, 连接, 合成, 合并, join]

targets: []

utterances:
  direct:
    - 把列表拼成字符串
    - 字符串拼接
    - 用逗号连接多个元素
  questions:
    - 怎么把列表里的字符串连成一个
    - 如何用分隔符拼接字符串
    - Python 怎么把多个字符串连起来
  colloquial:
    - 这些单词想连成一句
    - 中间加逗号拼起来
  technical:
    - str.join
    - join 分隔符
    - python concat list
  short_queries:
    - 拼接
    - join
    - 连接

status: tested
tested_versions: ["3.10", "3.11", "3.12", "3.13", "3.14"]
min_version: "3.0"
version_note: str.join 一直没变；注意它只能拼字符串，数字要先转换
sources:
  - Python 官方文档 str.join
---

# 把列表拼成字符串

## 功能描述

输入一个字符串列表 + 一个分隔符，输出把它们连起来的一个字符串（分隔符插在中间，不在末尾）。

## 推荐代码

```python
words = ["a", "b", "c"]
print(",".join(words))        # a,b,c
print("".join(words))         # abc
print(" - ".join(words))      # a - b - c

nums = [1, 2, 3]
print("-".join(str(n) for n in nums))   # 1-2-3
```

## 语句解释

### ",".join(words)

分隔符写在**前面**，被拼接的列表作为参数。这个顺序很多人第一次会写反。

### "".join(words)

空分隔符 = 直接连起来，不加任何东西。

### str(n) for n in nums

`join` 只吃字符串，列表里是数字时必须先转，否则抛 `TypeError`。

## 原理解释

`join` 是字符串的方法而不是列表的方法，因为分隔符才是“主语”——
它知道该用什么隔开，也知道要一次性算出总长度并分配内存，所以比循环 `+` 拼接快得多。

## 注意事项

- 元素必须全是字符串，有数字要先 `str()` 或 `map(str, ...)`。
- 分隔符写前面：`",".join(list)`，不是 `list.join(",")`。
- 少量拼接用 `+` 也行，循环里大量拼接必须用 `join`，否则 O(n²)。
- 元素本身含逗号时，拼出来再拆会出错，这种情况用 `csv` 模块。

## 使用场景

- 把一行字段拼成 csv 文本。
- 生成 SQL 的 `IN (...)` 列表。
- 拼路径片段（路径还是建议用 `Path`）。
