---
id: py.collections.counter
title: 统计每个元素出现几次
description: 一行算出频次表，找最高频也在里面
language: python
category_id: programming.basics
module: collections
origin: stdlib
import: "from collections import Counter, defaultdict"
qualname: "collections.counter"
signature: "Counter(可迭代对象)"
args:
  - name: "可迭代对象"
    required: true
    accepts: "任何可迭代对象；元素必须可哈希"
    nesting: "可以，常见是列表或字符串"
returns: "Counter（字典子类）：元素 → 次数；most_common(n) 取前 n 名"

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

**一句话：** 拿一本小本子挨个过一遍，见到谁就在谁名下加一笔。

**执行逻辑：**

1. 准备一个空的计数表（本质是字典）
2. 取一个元素，去表里查「这个名字记过没有」
3. 没记过 → 记成 1；记过了 → 原来的数加 1
4. 重复 2–3 直到取完
5. 表本身就是结果；`most_common(n)` 再按次数从大到小排一遍取前 n

**机器层（可跳过）：** 每个元素一次哈希查找 + 自增，O(n)。

**边界（从逻辑推出来）：**

- 第 2 步要拿元素当键，所以元素必须能哈希——列表、字典当元素直接报错
- 第 3 步「没记过就记成 1」意味着**不存在的键查出来是 0**，这是它和普通字典唯一的手感差异
- 第 5 步要排序，所以 `most_common` 比单纯统计慢
- 因为它是 dict 的子类，`c["不存在的"]` 不报错但也不写入，别用它判断「有没有」
## 注意事项

- 元素必须可哈希，列表/字典当元素会抛 `TypeError`。
- `Counter` 的键不存在返回 0，别用这个特性去判断“有没有” —— 用 `in`。
- 只想要频次最高的一个，`most_common(1)[0]` 即可。
- 统计大量数据时它占内存，纯计数可以用 `dict.get(k, 0) + 1` 更省。

## 使用场景

- 词频统计、日志里错误码分布。
- 找出重复最多的记录。
- 统计选项投票结果。
