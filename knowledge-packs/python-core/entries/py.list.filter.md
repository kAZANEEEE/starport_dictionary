---
id: py.list.filter
title: 按条件筛选列表
description: 留下满足条件的元素，组成新列表
language: python
category_id: programming.basics
module: list

object:
  id: list.element
  name: 列表元素
  aliases: [列表, 元素, 数据项, items]

action:
  id: filter.select
  name: 筛选
  aliases: [筛选, 过滤, 挑出, 只留, 保留, filter]

targets: []

utterances:
  direct:
    - 筛选列表
    - 按条件过滤列表
    - 只保留符合条件的元素
  questions:
    - 怎么筛选出列表里大于 10 的数
    - 如何过滤掉空字符串
    - Python 怎么按条件取子集
  colloquial:
    - 只想要偶数那几个
    - 把不合格的去掉
  technical:
    - filter 函数
    - 列表推导式过滤
    - if 条件 推导式
  short_queries:
    - 筛选
    - 过滤
    - filter

status: tested
tested_versions: ["3.10", "3.11", "3.12", "3.13", "3.14"]
min_version: "3.0"
version_note: filter 内置函数与列表推导式各版本一致
sources:
  - Python 官方文档 filter
  - Python 官方教程 列表推导式
---

# 按条件筛选列表

## 功能描述

输入列表 + 一个判断条件，输出**只包含通过条件的元素的新列表**，原列表不变。

## 推荐代码

```python
nums = [1, 5, 8, 12, 3]

evens = [n for n in nums if n % 2 == 0]
print(evens)                       # [8, 12]

big = list(filter(lambda n: n > 5, nums))
print(big)                         # [8, 12]

words = ["a", "", "b", None]
print([w for w in words if w])     # ['a', 'b']
```

## 语句解释

### [n for n in nums if n % 2 == 0]

列表推导式：`for` 后面加 `if` 就是筛选。最直观，也最快。

### filter(函数, 可迭代)

返回**迭代器**，外面套 `list()` 才是列表。不套的话只能遍历一次。

### if w 这种写法

`if w` 用的是“真值判断”：空字符串、0、None、空列表都算假，会被筛掉。

## 原理解释

**一句话：** 挨个问每个元素「你要不要留下」，要的放进新列表。

**执行逻辑：**

1. 准备一个空的结果列表
2. 取一个元素，交给条件判断
3. 判断为真 → 放进结果；为假 → 丢掉
4. 重复 2–3 直到取完
5. 返回结果列表（`filter` 版本是边问边给，不一次给完）

**机器层（可跳过）：** 一趟遍历，O(n)；条件函数每个元素调用一次。

**边界（从逻辑推出来）：**

- 第 5 步的差别很重要：推导式**立刻建完**整个列表，`filter` 返回的是**迭代器**，不 `list()` 就一次都没算
- 迭代器被消费一次就空了，第二次遍历拿不到东西
- 第 3 步判断的是「真假值」，不是严格布尔：空字符串、0、None 都算假
- 结果永远是**新对象**，原列表不动，元素本身还是同一批引用
## 注意事项

- `filter` 返回迭代器，打印出来是 `<filter object>`，要看结果得 `list(...)`。
- 迭代器用一次就空了，第二次遍历拿不到东西。
- 复杂条件优先用推导式，写成一句话更易读；只有现成的判断函数（如 `str.isdigit`）才用 `filter`。
- 筛选大量数据又只取前几个，用生成器表达式 + `islice`，别全建成列表。

## 使用场景

- 从扫描结果里挑出某类型文件。
- 过滤掉空值和无效记录。
- 按阈值筛数据（大于、小于、区间）。
