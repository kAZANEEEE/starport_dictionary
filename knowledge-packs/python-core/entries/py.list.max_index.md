---
id: py.list.max_index
title: 找最大值在第几个
description: 知道最大值还不够，还想知道它的位置
language: python
category_id: programming.basics
module: list
origin: builtin
import: ""
qualname: "items.index(max(items))"
signature: "items.index(max(items)) / max(range(len(items)), key=items.__getitem__)"
args:
  - name: "items"
    required: true
    accepts: "要比较的列表（元素要能比大小）"
    nesting: "可以，可以配合 key 用表达式比较"
returns: "整数下标：最大值第一次出现的位置；空列表抛 ValueError"
object:
  id: list.element
  name: 列表元素
  aliases: [列表, 最大值, 位置, 下标, items]
action:
  id: search.find
  name: 查找
  aliases: [找位置, 定位, 找下标, 查位置, index]
targets: []
utterances:
  direct:
    - 找最大值的位置
    - 最大值排第几
    - 取最大值的下标
  questions:
    - 怎么找到最大值所在的下标
    - max 只能给值，怎么知道位置
    - 列表里有重复最大值取哪个
  colloquial:
    - 知道最高分，想知道是谁
    - 想找最大的那个在第几个
  technical:
    - list.index
    - max with index
    - argmax
    - 重复最大值
  short_queries:
    - 最大值位置
    - 下标
    - index
status: tested
tested_versions: ["3.10", "3.11", "3.12", "3.13", "3.14"]
min_version: "3.0"
version_note: "index / max 各版本一致；没有内置的 argmax"
sources:
  - Python 官方文档 list.index
  - Python 官方文档 max
---

# 找最大值在第几个

## 功能描述

输入一个列表，输出最大值的下标；Python **没有内置的 argmax**，所以要用 `index(max(...))` 组合。

## 推荐代码

```python
scores = [72, 95, 88, 95]

print(max(scores))                     # 95
print(scores.index(max(scores)))       # 1  ← 第一个 95 的位置

# 一次遍历，同时拿到位置和值
best_i, best_v = max(enumerate(scores), key=lambda t: t[1])
print(best_i, best_v)                  # 1 95
```

## 语句解释

### max(scores)

只给最大值，不给位置。

### scores.index(max(scores))

先求最大值，再回列表里找它第一次出现的位置——**两趟遍历**。

### max(enumerate(...), key=...)

`enumerate` 给出 `(下标, 值)`，`key` 指定按「值」比大小，一次遍历同时拿到位置和值。

## 原理解释

**一句话：** 要么「先找最大值、再回列表查它在哪」，要么「边遍历边记下当前最大的位置」。

**执行逻辑（index + max）：**

1. 第一趟：比较所有元素，找到最大值
2. 第二趟：从头找第一个等于这个最大值的下标
3. 返回这个下标

**执行逻辑（enumerate + max）：**

1. 边遍历边产出 (下标, 值)
2. 每次和当前擂主比较，更大就替换擂主
3. 遍历完，擂主就是 (最大值下标, 最大值)

**机器层（可跳过）：** 第一种两趟 O(n)，第二种一趟 O(n)。

**边界（从逻辑推出来）：**

- 第一种要第 2 步「找第一个相等」，所以**有重复最大值时返回最靠前的那个**
- 第二种在第 2 步用「更大才替换」，所以持平不替换——同样返回第一个最大
- 空列表时 `max` 抛 `ValueError`，先判空
- 元素不能比大小时（如混合类型）会在比较处抛 `TypeError`

## 注意事项

- 有重复最大值时取第一个，想要最后一个用 `len - 1 - reversed(...)` 或倒着找。
- 空列表先判空，否则 `ValueError`。
- 只要位置不要值，`enumerate` 写法更省一次遍历。
- 按「某个字段」比大小就写 `key=lambda x: x["score"]`。

## 使用场景

- 排行榜取第一名是谁。
- 找图像里最亮的像素位置。
- 选出「分数最高」的那条记录。
