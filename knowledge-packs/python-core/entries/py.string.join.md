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

**一句话：** 拿着分隔符当「胶水」，把一堆字符串按顺序粘成一条。

**执行逻辑：**

1. 先看要粘的东西有多少个，算出总长度（要留多少位置）
2. 一次性申请好这么大的一块地方
3. 放进第一个字符串
4. 放进胶水（分隔符），再放下一个字符串
5. 重复第 4 步，直到放完
6. 收成一条字符串返回

**机器层（可跳过）：** 因为第 1 步先算总长，全程只分配一次内存。

**边界（从逻辑推出来）：**

- 第 3–5 步依次做，所以胶水**只在元素之间**出现，开头结尾都不会有
- 只接受字符串：列表里有数字会在第 3 步失败（要自己先 `str()`）
- 因为第 1 步要算总长，可迭代对象会被先遍历一次——传生成器也能用，但会被消费
- 循环里用 `+` 拼接等价于每次都重新算长度、重新分配，所以次数多了慢得多
## 注意事项

- 元素必须全是字符串，有数字要先 `str()` 或 `map(str, ...)`。
- 分隔符写前面：`",".join(list)`，不是 `list.join(",")`。
- 少量拼接用 `+` 也行，循环里大量拼接必须用 `join`，否则 O(n²)。
- 元素本身含逗号时，拼出来再拆会出错，这种情况用 `csv` 模块。

## 使用场景

- 把一行字段拼成 csv 文本。
- 生成 SQL 的 `IN (...)` 列表。
- 拼路径片段（路径还是建议用 `Path`）。
