---
id: py.list.sort
title: 给列表排序
description: 按数值、按字符串、或按自定义规则排列表
language: python
category_id: programming.algorithms
module: list

object:
  id: list.element
  name: 列表元素
  aliases: [元素, 列表项, 列表, 数据, items]

action:
  id: sort.order
  name: 排序
  aliases: [排, 排序, 从小到大, 从大到小, 重新排列, sort, order]

targets: []

utterances:
  direct:
    - 给列表排序
    - 列表从小到大排序
    - 按某个字段排序
  questions:
    - 怎么给列表排序
    - 如何按字典里的某个键排序
    - Python 怎么倒序排列列表
  colloquial:
    - 想让这些数字从小到大
    - 这个列表帮我按大小排一下
  short_queries:
    - 排序
    - 升序
    - sort
    - sorted

status: tested
tested_versions: ["3.10", "3.11", "3.12", "3.13", "3.14"]
min_version: "3.0"
version_note: sorted 和 list.sort 的 key / reverse 参数各版本一致
sources:
  - Python 官方文档 sorted
  - Python 官方文档 list.sort
---

# 给列表排序

## 功能描述

把列表排成升序或降序，也能按自定义规则（比如字典的某个键）排。

## 推荐代码

```python
nums = [3, 1, 4, 1, 5]
print(sorted(nums))                 # [1, 1, 3, 4, 5]
print(sorted(nums, reverse=True))   # [5, 4, 3, 1, 1]
print(nums)                         # [3, 1, 4, 1, 5] 原列表没变

people = [{"name": "李", "age": 30}, {"name": "王", "age": 22}]
by_age = sorted(people, key=lambda p: p["age"])
print([p["name"] for p in by_age])  # ['王', '李']
```

## 语句解释

### sorted(...)

返回**新列表**，原列表不动。拿返回值就是排好序的。

### reverse=True

降序。不是“反转”，是“按同一规则从大到小”。

### key=lambda p: p["age"]

`key` 接收一个函数，作用在**每个元素**上，排序比较的是这个函数的返回值。
所以这里比的是 age，不是整个字典。

### list.sort()

本地排序，原地改，返回 `None`。**写成 `nums = nums.sort()` 会得到 None**，这是经典坑。

## 原理解释

Python 用 Timsort，稳定排序：相等元素保持原来的相对顺序。
所以“先按 A 排、再按 B 排”可以拆成两次 `sorted`，后一次是主序，前一次是次序。

## 注意事项

- `sorted()` 返回新列表，`.sort()` 原地改并返回 None。
- 混合类型（数字和字符串）比较会抛 `TypeError`。
- 要按多个字段排，`key` 返回元组：`key=lambda x: (x["age"], x["name"])`。
- 排中文按 Unicode 码位，不是拼音；要按拼音得自己给 key 加映射。

## 使用场景

- 结果按分数、时间、名字排列。
- 取最大/最小的前 N 个（配合 `[:N]`，或直接用 `heapq.nlargest`）。
- 输出前统一顺序，方便对比和测试。
