---
id: py.list.dedupe
title: 列表去重
description: 去掉列表里重复的元素，保留原来的顺序
language: python
category_id: programming.algorithms
module: list

object:
  id: list.duplicate
  name: 列表重复元素
  aliases: [重复项, 重复值, 重复元素, duplicate, 重复数据]

action:
  id: delete.remove
  name: 删除
  aliases: [去掉, 移除, 清除, 去重, remove, dedupe]

targets: []

utterances:
  direct:
    - 列表去重
    - 去掉列表里的重复元素
    - 删除重复项
  questions:
    - 怎么给列表去重
    - 如何删除列表中的重复元素
    - 列表里重复的怎么去掉
  colloquial:
    - 这个列表里有重复的，怎么弄掉
    - 一堆重复的，只留一个
  goal_based:
    - 统计有多少种不同的值
    - 保证列表里的元素都不重复
  short_queries:
    - 去重
    - 重复
    - dedupe

related_ids:
  - py.list.find

status: tested
tested_versions: ["3.10", "3.11", "3.12", "3.13", "3.14"]
min_version: "3.7"
version_note: dict 保序从 3.7 起是语言保证，所以 3.7+ 都能用
---

# 列表去重

## 功能描述

把列表里重复的值去掉，只留第一次出现的位置，顺序不变。

## 推荐代码

```python
items = [3, 1, 3, 2, 1, 3]

unique = list(dict.fromkeys(items))
print(unique)  # [3, 1, 2]
```

## 语句解释

### dict.fromkeys(items)

把每个元素当成字典的键放进去。字典的键天然唯一，重复的会被覆盖。

### list(...)

`dict.fromkeys` 返回的是字典视图，外面套一层 `list` 才能拿回列表。

## 原理解释

**一句话：** 借字典「键不能重复」这个特性，把重复的挤掉，顺序还照旧。

**执行逻辑：**

1. `dict.fromkeys(列表)` 开始建字典——逐个元素当键往里放
2. 放进第一个 `3` 时，字典里新建一个键
3. 再遇到 `3` 时，键已经存在，**值被覆盖**（所以最后只剩一份）
4. 字典建完，它的**键集合**就是去重结果，且保持首次出现的顺序
5. `list(...)` 把键取出来变成列表

**机器层（可跳过）：** 字典是哈希表，查「键在不在」是 O(1)，所以整体是 O(n)。

**边界（从逻辑推出来）：**

- 第 1 步要求元素**能当字典键**（可哈希）——列表、字典当元素会抛 `TypeError`
- 保留的是「第一次出现」的位置，因为后续覆盖不改键的位置
- 顺序保证靠 3.7 起字典的插入有序特性，更老的版本不保证
- 只想「不重复」不在乎顺序，`set` 更快；一旦在乎顺序才用这条
## 注意事项

- 元素必须可哈希。列表、字典这类不能当键，会抛 `TypeError`。
- 该写法保留的是**第一次出现**的顺序，不是排序后的顺序。
- 想按值排序再去重，先 `sorted()` 再套这里，别反过来。
- 数据量大（十万以上）时 `set` + 列表推导通常更快，可以实测再决定。

## 使用场景

- 合并多个来源的 ID 列表后去重。
- 统计"有多少种不同的值"。
- 做配置合并时避免重复项。
