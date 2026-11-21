---
id: py.list.map
title: 批量转换列表元素
description: 对每个元素做同一个操作，得到新列表
language: python
category_id: programming.basics
module: list

object:
  id: list.element
  name: 列表元素
  aliases: [列表, 元素, 每个元素, items]

action:
  id: convert.transform
  name: 转换
  aliases: [转换, 映射, 批量处理, 逐个处理, map]

targets: []

utterances:
  direct:
    - 批量转换列表元素
    - 列表里每个元素都转成字符串
    - 对列表每个元素做处理
  questions:
    - 怎么把列表里所有元素转成字符串
    - 如何对列表每个元素调用同一个函数
    - Python 怎么批量处理列表
  colloquial:
    - 这一列数字想全部变成字符串
    - 每个元素都要加 1
  technical:
    - map 函数
    - 列表推导式映射
    - lambda 配合 map
  short_queries:
    - 映射
    - map

status: tested
tested_versions: ["3.10", "3.11", "3.12", "3.13", "3.14"]
min_version: "3.0"
version_note: map 返回迭代器；列表推导式各版本一致
sources:
  - Python 官方文档 map
---

# 批量转换列表元素

## 功能描述

输入列表 + 一个转换操作，输出**每个元素都被转换过的新列表**，元素个数不变。

## 推荐代码

```python
nums = [1, 2, 3]

strs = [str(n) for n in nums]
print(strs)                        # ['1', '2', '3']

plus_one = list(map(lambda n: n + 1, nums))
print(plus_one)                    # [2, 3, 4]

raw = [" 10 ", "20 "]
print([int(x) for x in raw])       # [10, 20]  int 会自动处理首尾空白
```

## 语句解释

### [str(n) for n in nums]

列表推导式，最常用。左边是“对每个元素做什么”。

### map(函数, 可迭代)

把函数逐个应用到元素上，返回**迭代器**，要 `list()` 才是列表。

### 两者的区别

`map` 只是“应用函数”；推导式还能顺便筛选（加 `if`），也能做更复杂表达式。

## 原理解释

`map` 是惰性的：不 `list()` 就一次都没算。所以 `map(...)` 之后直接 `sum()` 也很省内存。

列表推导式会**立刻**把结果全建出来，占用等于结果的长度。数据量大时这是主要区别。

## 注意事项

- `map` 返回迭代器，`print` 出来是 `<map object at 0x...>`。
- 迭代器只能消费一次。
- 需要同时处理两个列表用 `map(f, a, b)` 或 `zip`。
- 元素类型不一致时先统一，否则后面处理会各类报错。

## 使用场景

- 把字符串列表转成数字列表。
- 给一批文件名统一加前缀。
- 对抓取到的数据做统一清洗。
