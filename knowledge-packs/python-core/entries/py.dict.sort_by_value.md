---
id: py.dict.sort_by_value
title: 按值排序字典
description: 字典本身无序，排完要转成列表才能保持顺序
language: python
category_id: programming.basics
module: dict
origin: builtin
import: ""
qualname: "sorted(d.items(), key=lambda kv: kv[1])"
signature: "sorted(d.items(), key=lambda kv: kv[1], reverse=True)"
args:
  - name: "d.items()"
    required: true
    accepts: "把字典变成 (键, 值) 对，才能排序"
    nesting: "可以，也可以直接 sorted(d, key=d.get) 只拿键"
  - name: "key"
    required: true
    accepts: "kv[1] 表示按值排；kv[0] 表示按键排"
    nesting: "可以，值是复合结构时写 kv[1][\"score\"]"
returns: "列表（不是字典）：[(键, 值), ...] 或键的列表；字典本身不保留排序"
object:
  id: dict.value
  name: 字典值
  aliases: [字典, 值, 排序, 排名, dict]
action:
  id: sort.order
  name: 排序
  aliases: [排序, 按值排, 排名, 降序, sort]
targets: []
utterances:
  direct:
    - 按值排序字典
    - 字典按值降序
    - 给字典排序
  questions:
    - 怎么按值给字典排序
    - sorted(d.items()) 的 key 怎么写
    - 排完为什么变列表了
  colloquial:
    - 想按次数从多到少排出来
    - 字典排完还是字典吗
  technical:
    - sorted items key
    - dict 顺序
    - operator.itemgetter
  short_queries:
    - 按值排序
    - 字典排序
    - 排名
status: tested
tested_versions: ["3.10", "3.11", "3.12", "3.13", "3.14"]
min_version: "3.0"
version_note: "sorted + items 各版本一致；3.7 起字典本身保插入顺序"
sources:
  - Python 官方文档 sorted
  - Python 官方文档 dict.items
---

# 按值排序字典

## 功能描述

输入字典，输出按值排好的**列表**（`(键, 值)` 对）；字典本身不会被排序。

## 推荐代码

```python
scores = {"张三": 90, "李四": 95, "王五": 88}

print(sorted(scores.items(), key=lambda kv: kv[1]))              # 升序
print(sorted(scores.items(), key=lambda kv: kv[1], reverse=True)) # 降序

# 只要键
print(sorted(scores, key=scores.get, reverse=True))   # ['李四', '张三', '王五']

# 用 operator.itemgetter 更短
from operator import itemgetter
print(sorted(scores.items(), key=itemgetter(1), reverse=True))
```

## 语句解释

### d.items()

变成 `(键, 值)` 对的集合，才能按值排。

### key=lambda kv: kv[1]

`kv[1]` 是值，`kv[0]` 是键。

### 为什么结果是列表

字典没有「排序状态」，`sorted` 返回的是列表；要字典只能 `dict(...)` 重建（但那就是插入顺序了）。

### key=scores.get

只排键时用：对每个键取它的值当依据。

## 原理解释

**一句话：** 先把字典变成一串「键值对」，按你指定的字段排这串对，返回排好的列表。

**执行逻辑：**

1. `items()` 产出 (键, 值) 对
2. 对每一对调 key 函数，算出排序依据
3. 按依据排序
4. 返回排好的列表

**机器层（可跳过）：** 一次排序 O(n log n)，依据只算一次（不是每次比较都算）。

**边界（从逻辑推出来）：**

- 第 1 步变成序列，所以结果不再是字典
- 第 4 步返回列表，想变回字典用 `dict(...)`，但那时顺序只是"插入顺序"恰好等于排好的顺序
- 用 `dict(...)` 重建后如果再增删键，顺序还是会跟着插入顺序变
- 值相同的情况下按原顺序（稳定排序）

## 注意事项

- 结果是列表，不是字典；要字典就 `dict(sorted(...))`，但别指望它以后一直有序。
- 值相同会保持原顺序（稳定）。
- 值是复合结构时 `kv[1]["score"]`，写清楚层级。
- 只要前 N 名用 `[:N]`，别全排（数据大时可考虑 `heapq.nlargest`）。

## 使用场景

- 排行榜（词频、成绩）。
- 统计结果按数量排序展示。
- 找最大的几个键。
