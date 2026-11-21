---
id: py.collections.counter
title: 统计每个元素出现几次
description: 一行算出频次表，找最高频也在里面
language: python
category_id: programming.basics
module: collections

object:
  id: dict.value
  name: 字典值
  aliases: [频次, 计数, 出现次数, 统计结果, 字典, counter]

action:
  id: get.obtain
  name: 获取
  aliases: [统计, 计数, 算次数, 数一数, count]

targets: []

utterances:
  direct:
    - 统计元素出现次数
    - 算每个元素的频次
    - 找出现最多的元素
  questions:
    - 怎么统计列表里每个元素出现几次
    - 如何找出出现次数最多的
    - 怎么算字符频率
  colloquial:
    - 这个列表里哪个值最多，出现几次
    - 想数一数每样有几个
  technical:
    - collections.Counter
    - most_common
    - 词频统计
  short_queries:
    - 统计
    - 频次
    - Counter

status: tested
tested_versions: ["3.10", "3.11", "3.12", "3.13", "3.14"]
min_version: "3.0"
version_note: Counter 从 2.7 起；3.10 起新增 total() 方法
sources:
  - Python 官方文档 collections.Counter
---

# 统计每个元素出现几次

## 功能描述

输入可迭代对象，输出一个“元素 → 次数”的字典，还带取 Top N 的方法。

## 推荐代码

```python
from collections import Counter

words = ["a", "b", "a", "c", "a", "b"]
c = Counter(words)

print(c)                      # Counter({'a': 3, 'b': 2, 'c': 1})
print(c["a"])                 # 3
print(c["不存在"])             # 0 —— 不抛 KeyError
print(c.most_common(2))       # [('a', 3), ('b', 2)]
print(sum(c.values()))        # 6
```

## 语句解释

### Counter(words)

一次性统计。它本身是 dict 的子类，能像字典一样用。

### c["不存在"] 返回 0

这点和普通字典不同——普通字典抛 `KeyError`，Counter 返回 0。

### most_common(n)

取出现次数最多的 n 个，返回 `(元素, 次数)` 列表。

## 原理解释

`Counter` 内部就是“用一个字典累计计数”，初始化时遍历一遍计数。
它额外实现了 `+`、`-` 等运算（合并/相减计数表），以及 `most_common` 的排序。

元素必须是可哈希的（字符串、数字、元组），列表和字典不行。

## 注意事项

- 元素必须可哈希，列表/字典当元素会抛 `TypeError`。
- `Counter` 的键不存在返回 0，别用这个特性去判断“有没有” —— 用 `in`。
- 只想要频次最高的一个，`most_common(1)[0]` 即可。
- 统计大量数据时它占内存，纯计数可以用 `dict.get(k, 0) + 1` 更省。

## 使用场景

- 词频统计、日志里错误码分布。
- 找出重复最多的记录。
- 统计选项投票结果。
