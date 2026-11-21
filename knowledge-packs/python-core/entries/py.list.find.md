---
id: py.list.find
title: 查找列表里的元素
description: 判断某个值在不在列表里，以及它第一次出现的位置
language: python
category_id: programming.basics
module: list

object:
  id: list.element
  name: 列表元素
  aliases: [元素, 列表项, 某一项, 某个值, item, element]

action:
  id: search.find
  name: 查找
  aliases: [找, 搜索, 定位, 查一下, 在不在, find, lookup]

targets: []

utterances:
  direct:
    - 查找列表中的元素
    - 判断元素在不在列表里
    - 找列表里某个值的位置
  questions:
    - 怎么判断一个值在不在列表里
    - 如何找到元素在列表的下标
    - Python 怎么查列表里有没有某个元素
  colloquial:
    - 这个东西在这个列表里吗
    - 想找一个值排第几个
  short_queries:
    - 查找
    - 列表查找
    - in
    - index

status: tested
tested_versions: ["3.10", "3.11", "3.12", "3.13", "3.14"]
min_version: "3.0"
version_note: in 和 list.index 是列表自带方法，各版本行为一致
sources:
  - Python 官方文档 list.index
---

# 查找列表里的元素

## 功能描述

判断某个值在不在列表里（`in`），或者取它第一次出现的下标（`index`）。

## 推荐代码

```python
items = ["apple", "banana", "cherry"]

print("banana" in items)      # True
print("grape" in items)       # False

if "cherry" in items:
    pos = items.index("cherry")
    print("下标:", pos)       # 下标: 2
```

## 语句解释

### "banana" in items

`in` 返回布尔值，直接从前往后找，找到就停。这是判断“在不在”的首选写法。

### items.index("cherry")

返回第一次出现的下标。**找不到会抛 ValueError**，所以要先判断或者包 try。

### if ... in ... 再 index

常见组合：先用 `in` 确认存在，再取下标；这样不会因为找不到而崩。

## 原理解释

列表是顺序结构，`in` 和 `index` 都是从第一个元素开始逐个比较，找完为止，
所以时间复杂度是 O(n)——列表越长越慢，这是它和字典最大的区别。

## 注意事项

- `index` 找不到抛 `ValueError`，不是返回 -1（那是字符串 `find` 的行为）。
- 只想判断存在性就用 `in`，别用 `index` 加 try，白绕一圈。
- 需要“取最后一个”或“所有位置”`in`/`index` 都不够，要么反转要么用列表推导。
- 数据量大且需要频繁查找，改用 `set` 或 `dict`，O(1)。

## 使用场景

- 去重或过滤前先判断某个 ID 是否已处理。
- 拆分逻辑：先判存在，再取位置做后续操作。
- 写测试时断言结果里有某个值。
