---
id: py.list.any_all
title: 判断有没有 / 是不是全都满足
description: 一批条件里，任意一个成立、或者全部成立
language: python
category_id: programming.basics
module: list

object:
  id: list.element
  name: 列表元素
  aliases: [列表, 元素, 一批条件, 全部, items]

action:
  id: inspect.check
  name: 判断
  aliases: [判断, 检查, 有没有, 是不是都, any, all]

targets: []

utterances:
  direct:
    - 判断列表里有没有符合条件的
    - 检查是不是全部都满足
    - 判断是否存在某个元素
  questions:
    - 怎么判断列表里有没有大于 10 的
    - 如何检查所有元素都符合条件
    - any 和 all 有什么区别
  colloquial:
    - 有一个满足就算过
    - 必须全部满足才行
  technical:
    - any
    - all
    - 短路求值
  short_queries:
    - 有没有
    - 全部
    - any
    - all

status: tested
tested_versions: ["3.10", "3.11", "3.12", "3.13", "3.14"]
min_version: "3.0"
version_note: any / all 各版本一致；都是短路求值
sources:
  - Python 官方文档 any
  - Python 官方文档 all
---

# 判断有没有 / 是不是全都满足

## 功能描述

输入一批真假值，输出一个布尔：`any` = 至少一个真，`all` = 全为真。**空列表时 any 为假、all 为真**。

## 推荐代码

```python
nums = [1, 5, 8, 12]

print(any(n > 10 for n in nums))     # True
print(all(n > 0 for n in nums))      # True
print(all(n > 10 for n in nums))     # False

print(any([]))    # False
print(all([]))    # True（空集合里没有反例）
```

## 语句解释

### any(可迭代)

只要有一个元素为真就返回 True，**遇到第一个真就停**。

### all(可迭代)

只要有一个为假就返回 False，遇到第一个假就停。

### 传生成器而不是列表

`(n > 10 for n in nums)` 边算边判、判到就停，不浪费计算。

## 原理解释

**一句话：** 它挨个看条件成立不成立，一旦结论定了就立刻收工。

**执行逻辑：**

1. 从可迭代对象里取一个值
2. 判断它是真还是假
3. `any` 看到真 → 立刻返回 True；`all` 看到假 → 立刻返回 False
4. 否则取下一个，重复 2–3
5. 全都取完了还没定论：`any` 返回 False（一个真的都没有），`all` 返回 True（一个反例都没有）

**机器层（可跳过）：** 因为会中途停，最坏才走完全程——这叫短路求值。

**边界（从逻辑推出来）：**

- 第 3 步「立刻返回」意味着后面的元素**根本不会被计算**，所以传生成器能省掉大量计算
- 第 5 步对空集合的结论不同：`any([])==False`、`all([])==True`，这是「没有反例」的逻辑后果
- 因为第 3 步随时可能提前返回，函数参数里有副作用时不能指望它全执行
- 判断「有没有某个元素」用 `in` 更直接，`any` 适合带条件的判断

## 注意事项

- 空列表：`any` 假、`all` 真——这个组合最容易被想反。
- 传生成器时不要求先建成列表，省内存。
- 别在生成器表达式里写打印/写文件这类副作用，短路会让它们只执行一部分。
- 判断元素存在性用 `x in lst`，不要换成 `any(v == x for v in lst)`。

## 使用场景

- 校验表单：所有必填项都非空（`all`）。
- 快速失败：任何一个检查项报错就停（`any`）。
- 替代一串 `or` / `and` 条件判断。
