---
id: py.dict.fromkeys
title: 批量造一个字典
description: 给一批键，全部配上同一个初值
language: python
category_id: programming.basics
module: dict
origin: builtin
import: ""
qualname: "dict.fromkeys()"
signature: "dict.fromkeys(keys, value=None)"
args:
  - name: "keys"
    required: true
    accepts: "键序列，元素必须可哈希"
    nesting: "可以"
  - name: "value"
    required: false
    default: "None"
    accepts: "所有键共用的初始值"
    nesting: "可以，但传可变对象会被所有键共享"
returns: "新字典：每个键都对应同一个 value"

object:
  id: dict.value
  name: 字典值
  aliases: [字典, 键, 初始值, 批量创建, dict]

action:
  id: create.new
  name: 创建
  aliases: [批量创建, 初始化, 造字典, 批量生成, fromkeys]

targets: []

utterances:
  direct:
    - 批量创建字典
    - 给一批键加上同一个初值
    - 用 fromkeys 初始化字典
  questions:
    - 怎么一次性创建多个键的字典
    - fromkeys 的默认值能改吗
    - 为什么用 fromkeys 建列表会共享
  colloquial:
    - 有一堆键，想先都设成 0
    - 用 fromkeys 建完列表，改一个全变了
  technical:
    - dict.fromkeys
    - 可变默认值共享
    - 计数表初始化
  short_queries:
    - fromkeys
    - 批量创建
    - 初始值

status: tested
tested_versions: ["3.10", "3.11", "3.12", "3.13", "3.14"]
min_version: "3.0"
version_note: "dict.fromkeys 各版本一致；注意可变默认值会被共享"
sources:
  - Python 官方文档 dict.fromkeys
---

# 批量造一个字典

## 功能描述

输入一批键 + 一个初值，输出字典：每个键都对应**同一个**初值对象；不传初值则都是 `None`。

## 推荐代码

```python
keys = ["a", "b", "c"]

print(dict.fromkeys(keys))              # {'a': None, 'b': None, 'c': None}
print(dict.fromkeys(keys, 0))           # {'a': 0, 'b': 0, 'c': 0}

# 危险用法：所有键共享同一个列表
bad = dict.fromkeys(keys, [])
bad["a"].append(1)
print(bad)          # {'a': [1], 'b': [1], 'c': [1]}  ← 全变了

# 正确做法：字典推导式，每个键单独造
good = {k: [] for k in keys}
good["a"].append(1)
print(good)         # {'a': [1], 'b': [], 'c': []}
```

## 语句解释

### fromkeys(键序列, 初值)

每个键都指向**同一个**初值对象。不可变初值（0、None、字符串）没问题。

### 为什么列表会共享

因为「初值」只求值一次，所有键都指向它，改一个就是改全部。

### 字典推导式代替

`{k: [] for k in keys}` 每次迭代都新建列表，互不影响。

## 原理解释

**一句话：** 它挨个把键放进字典，值统一填你给的**那一个**对象（不是每次新造一个）。

**执行逻辑：**

1. 创建一个空字典
2. 从键序列取一个键
3. 把「你给的那个初值」填给这个键（引用，不复制）
4. 重复 2–3 直到取完
5. 返回字典

**机器层（可跳过）：** 每个键一次插入，O(n)；值只是引用赋值。

**边界（从逻辑推出来）：**

- 第 3 步填的是同一个引用，所以可变初值（列表/字典）会被所有键共享
- 不可变初值（数字、字符串、None）共享无害，因为改不了
- 键必须可哈希，且重复键会被合并（只保留一个）
- 因为第 2 步按顺序插入，3.7+ 顺序与键序列一致，所以也常用来「保序去重」

## 注意事项

- **别用 `fromkeys(k, [])` 或 `{}`** 造可变初值，改一个会全变。
- 要可变初值就用字典推导式或 `defaultdict`。
- 重复键会自动合并，正好可以当保序去重用。
- 键必须可哈希。

## 使用场景

- 初始化计数表（`fromkeys(keys, 0)`）。
- 保序去重（`list(dict.fromkeys(items))`）。
- 造「标志位」字典（全是 False）。
