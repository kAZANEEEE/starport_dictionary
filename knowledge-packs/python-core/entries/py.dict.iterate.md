---
id: py.dict.iterate
title: 遍历字典
description: 逐个拿到字典里的键、值或键值对
language: python
category_id: programming.basics
module: dict
origin: builtin
import: ""
qualname: "dict.items()"
signature: "for k, v in d.items()"
args:
  - name: "d"
    required: true
    accepts: "要遍历的字典"
    nesting: "可以"
returns: "迭代器：items 给 (键, 值)；keys 给键；values 给值。遍历中不能改字典"

object:
  id: dict.value
  name: 字典值
  aliases: [字典, 键值对, 每一项, 键和值, dict]

action:
  id: traverse.walk
  name: 遍历
  aliases: [遍历, 循环, 逐个, 走一遍, 迭代, iterate]

targets: []

utterances:
  direct:
    - 遍历字典
    - 循环字典的每一项
    - 同时拿到键和值
  questions:
    - 怎么遍历字典
    - 如何同时取出字典的键和值
    - Python 怎么循环字典取 key 和 value
  colloquial:
    - 想把字典里每一项都处理一遍
    - 字典里的东西怎么一个个拿出来
  technical:
    - dict.items
    - dict.keys
    - dict.values
    - for k v in dict
  short_queries:
    - 遍历字典
    - items
    - keys

status: tested
tested_versions: ["3.10", "3.11", "3.12", "3.13", "3.14"]
min_version: "3.7"
version_note: 3.7 起字典保证插入顺序，遍历顺序才可依赖
sources:
  - Python 官方文档 dict.items
---

# 遍历字典

## 功能描述

输入字典，逐个访问它的键、值或键值对；顺序等于插入顺序（3.7+）。

## 推荐代码

```python
scores = {"语文": 90, "数学": 85}

for k, v in scores.items():
    print(k, v)

for k in scores:                 # 直接遍历拿到的是键
    print(k)

for v in scores.values():
    print(v)
```

## 语句解释

### scores.items()

返回 `(键, 值)` 对，配合 `for k, v in` 一次拿两个。

### for k in scores

直接遍历字典，拿到的**是键**，不是键值对。这一点和 `.items()` 最容易混。

### scores.values()

只拿值。想同时要下标可以套 `enumerate`。

## 原理解释

**一句话：** 把字典里的东西一件一件交到你手上，你可以选择拿钥匙、拿货、或者两样一起拿。

**执行逻辑：**

1. Python 按内部存放顺序取出一个「键」
2. 你要键 → 交给你；你要值 → 先用键找到值再交给你；你要一对 → 同时给键和值
3. 从下一个位置继续（字典不是按顺序存的，但它额外记着插入次序）
4. 取完为止

**机器层（可跳过）：** 遍历的其实是哈希表的槽位，顺序来自插入记录，不是排序。

**边界（从逻辑推出来）：**

- 第 1 步只交键，所以 `for k in d` 拿到的是键不是值（最常见的误用）
- 第 3 步的「插入次序」是 3.7 起才保证的，想按 key 排序仍要 `sorted()`
- 遍历途中增删键会让「当前位置」失效，Python 直接抛 `RuntimeError`
- `.items()` 给的是视图不是拷贝，遍历期间字典变了它也会跟着变
## 注意事项

- 遍历时改字典会抛 `RuntimeError: dictionary changed size during iteration`；
  要改就先 `list(d.keys())` 复制一份键再遍历。
- `for k in d` 拿到的是键，别当成值用。
- 想按 key 排序遍历：`for k in sorted(d)`。
- `items()` 返回的是视图，不是列表；要列表用 `list(d.items())`。

## 使用场景

- 把配置字典逐项处理。
- 统计/聚合时遍历键值对。
- 输出表格前先排序遍历，保证每次都一样。
