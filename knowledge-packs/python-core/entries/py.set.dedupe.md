---
id: py.set.dedupe
title: 用集合去重
description: 最快去重的写法，代价是不保序
language: python
category_id: programming.basics
module: set

object:
  id: list.duplicate
  name: 列表重复元素
  aliases: [重复项, 重复值, 去重, 重复元素, duplicate]

action:
  id: delete.remove
  name: 删除
  aliases: [去重, 去掉重复, 剔除重复, 去重, dedupe]

targets: []

utterances:
  direct:
    - 用集合去重
    - 列表去重最快写法
    - set 去重
  questions:
    - 怎么用 set 快速去重
    - set 去重后顺序变了吗
    - 去重还要保持原顺序怎么办
  colloquial:
    - 只想要不重复的那些
    - 去重之后顺序乱了，怎么办
  technical:
    - set()
    - dict.fromkeys 保序去重
    - 可哈希
  short_queries:
    - set 去重
    - 去重最快

status: tested
tested_versions: ["3.10", "3.11", "3.12", "3.13", "3.14"]
min_version: "3.0"
version_note: set 各版本一致；3.7 起 set 的内存布局有调整，行为不变
sources:
  - Python 官方文档 set
---

# 用集合去重

## 功能描述

输入可迭代对象，输出一个**元素唯一**的集合；顺序不保证。

## 推荐代码

```python
nums = [3, 1, 3, 2, 1]

unique = set(nums)
print(unique)            # {1, 2, 3}  顺序不保证
print(len(unique))       # 3

# 要保序：先按插入顺序建字典键
print(list(dict.fromkeys(nums)))   # [3, 1, 2]
```

## 语句解释

### set(可迭代)

每个元素算哈希存进去，同一个值只留一份。

### len(set(...))

顺便就得到「有多少种不同的值」。

### dict.fromkeys(可迭代)

3.7+ 的保序去重写法：字典键唯一且保序。

## 原理解释

**一句话：** 它把每个元素按哈希值放进不同的格子，同一个值一定落进同一个格子，所以重复的自然被挤掉。

**执行逻辑：**

1. 建一张空的哈希表
2. 取一个元素，算它的哈希值
3. 按哈希值定位到某个格子：格子里已经有相等的值 → 丢弃；没有 → 放进去
4. 重复 2–3 直到取完
5. 把表里的元素给你（顺序取决于哈希值，不是插入顺序）

**机器层（可跳过）：** 每次插入/查找平均 O(1)，所以整体 O(n)。

**边界（从逻辑推出来）：**

- 第 3 步靠哈希定位，所以元素必须**可哈希**——列表、字典不能直接放进去
- 第 5 步输出顺序由哈希决定，所以**顺序不保证**，多次运行也可能不同
- 因为第 3 步比较的是「哈希 + 相等」，`1` 和 `True` 会被认为同一个元素
- 要保序就得换成「按插入顺序记录」的结构，也就是 `dict.fromkeys`

## 注意事项

- 不能保序，需要顺序就用 `dict.fromkeys`。
- 元素必须可哈希；嵌套列表先转成 tuple。
- `1` 和 `True`、`1` 和 `1.0` 会被当成重复。
- 只要「不重复」且数量大时，`set` 最快；`dict.fromkeys` 稍慢但保序。

## 使用场景

- 快速去重、统计不同值的个数。
- 判断两个列表是否有交集（转成 set 再算）。
- 做白名单/黑名单查找（`in` 是 O(1)）。
