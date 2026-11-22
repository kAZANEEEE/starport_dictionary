---
id: py.set.ops
title: 集合运算（交并差）
description: 求两个集合的公共部分、合并、差集
language: python
category_id: programming.basics
module: set
origin: builtin
import: ""
qualname: "set 运算 & | -"

object:
  id: list.duplicate
  name: 列表重复元素
  aliases: [集合, 交集, 并集, 差集, set]

action:
  id: convert.transform
  name: 转换
  aliases: [求交, 求并, 求差, 去重, intersection, union]

targets: []

utterances:
  direct:
    - 求两个集合的交集
    - 求并集
    - 求差集
  questions:
    - 怎么找两个列表的共同元素
    - 如何求并集和差集
    - set 和 list 转换有什么代价
  colloquial:
    - 两边都有的那些给我挑出来
    - 有哪些是只在 A 里没有的
  technical:
    - "set 运算"
    - "& | - 运算符"
    - "frozenset"
    - "为什么 set 不能保序"
  short_queries:
    - 交集
    - 并集
    - 差集

status: tested
tested_versions: ["3.10", "3.11", "3.12", "3.13", "3.14"]
min_version: "3.0"
version_note: set 运算与运算符语法各版本一致
sources:
  - Python 官方文档 set
---

# 集合运算（交并差）

## 功能描述

输入两个集合（或能变成集合的序列），输出交、并、差的结果；**结果无序**。

## 推荐代码

```python
a = {"apple", "banana", "cherry"}
b = {"banana", "dragon"}

print(a & b)     # {'banana'}          交集
print(a | b)     # 并集
print(a - b)     # {'apple', 'cherry'} 只在 a 里
print(a ^ b)     # 对称差：只在一侧

# 列表也能直接算，会自动转换
print(set(["a", "b"]) & {"b", "c"})   # {'b'}
```

## 语句解释

### a & b

交集：两边都有的元素。

### a | b

并集：任一边有的都留下。

### a - b

差集：在 a 里但不在 b 里（**有方向**）。

### a ^ b

对称差：只在一侧出现的（等价于 `(a|b) - (a&b)`）。

## 原理解释

**一句话：** 它拿小的一方的元素去大的一方里查，查得到/查不到决定要不要留下。

**执行逻辑：**

1. 把两边的元素都放进哈希表（集合本身就是哈希表）
2. 遍历其中一个集合的每个元素
3. 去另一个集合里查它在不在（一步到位，不用逐个比）
4. 按运算规则决定留不留：交集留「都在」，差集留「只在这边」
5. 把留下的元素组成新集合

**机器层（可跳过）：** 每次查找是 O(1)，所以运算代价约等于元素个数。

**边界（从逻辑推出来）：**

- 第 1 步要建哈希表，所以元素必须可哈希（列表不能放进集合）
- 第 3 步是哈希查找而不是逐个比较，所以它比「双层循环找共同元素」快得多
- 因为哈希表本身不记顺序，所以结果**无序**；需要顺序就转回列表再排
- 差集有方向：`a - b` 和 `b - a` 不同，别记反
- 第 1 步会把重复元素合并，所以「去重」是集合的副产品

## 注意事项

- 结果无序，要稳定输出就 `sorted(...)`。
- 元素必须可哈希；要放列表/tuple 里的 list，得先转成 tuple。
- `a - b` 有方向。
- 只是想去重又需要保序，用 `dict.fromkeys` 而不是 `set`。

## 使用场景

- 找两个用户列表的共同好友。
- 找出「新增」和「消失」的数据（差集）。
- 快速判重、去重后再统计。
