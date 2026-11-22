---
id: py.dict.keys_values
title: 拿字典的键或值列表
description: 把键、值单独抽出来当列表用
language: python
category_id: programming.basics
module: dict
origin: builtin
import: ""
qualname: "dict.keys() / dict.values() / dict.items()"

object:
  id: dict.value
  name: 字典值
  aliases: [字典, 键, 值, 所有键, dict]

action:
  id: get.obtain
  name: 获取
  aliases: [获取, 取出, 拿, 列出, keys, values, items]

targets: []

utterances:
  direct:
    - 获取字典所有键
    - 拿到字典的值列表
    - 把键拿出来当列表
  questions:
    - 怎么把字典的键变成列表
    - keys 返回的是什么类型
    - 怎么按值排序取出键
  colloquial:
    - 想把字典里的名字都列出来
    - keys 加索引为什么报错
  technical:
    - dict.keys
    - dict.values
    - dict.items
    - 视图对象
  short_queries:
    - 键
    - 键列表
    - values

status: tested
tested_versions: ["3.10", "3.11", "3.12", "3.13", "3.14"]
min_version: "3.0"
version_note: "keys/values/items 返回视图，3.x 全部一致"
sources:
  - Python 官方文档 dict.keys
---

# 拿字典的键或值列表

## 功能描述

输入字典，输出键视图 / 值视图 / 键值对视图；**要真列表得 `list(...)` 套一层**。

## 推荐代码

```python
d = {"a": 1, "b": 2}

print(list(d.keys()))      # ['a', 'b']
print(list(d.values()))    # [1, 2]
print(list(d.items()))     # [('a', 1), ('b', 2)]

print(sorted(d.values()))  # 视图能直接交给 sorted

# 按值排序后取键
print(sorted(d, key=d.get))    # ['a', 'b']
```

## 语句解释

### keys() / values() / items()

返回的是**视图对象**，不是列表——它实时反映字典内容，但不支持下标。

### 为什么要 list(...)

视图不支持 `[0]`，也不支持 `append`。当成序列用之前先转列表。

### sorted(d, key=d.get)

遍历字典得到键，`key=d.get` 表示「按对应的值来排序」。

## 原理解释

**一句话：** 它不复制数据，只给你一个「能遍历这堆键」的窗口。

**执行逻辑：**

1. 调用 `keys()` 时不复制任何东西，只是返回一个指向原字典的视图对象
2. 遍历这个视图时，逐个去字典里取键
3. 如果你在遍历期间改了字典，视图反映的是**最新的**内容
4. `list(...)` 才会真的把当前内容抄出来

**机器层（可跳过）：** 视图本身只有几个字节，开销在遍历时才产生。

**边界（从逻辑推出来）：**

- 第 1 步不复制，所以 `ks = d.keys()` 之后改字典，`ks` 看到的也是新的
- 第 3 步「实时反映」意味着遍历时增删键会抛 `RuntimeError`
- 因为它不是列表，`d.keys()[0]` 会报 `TypeError`
- 需要一份稳定快照就必须 `list(d.keys())`

## 注意事项

- 视图不能下标，先 `list()`。
- 遍历时别改字典。
- 只判断键存在用 `in d`，不需要 `d.keys()`。
- 想按值排序取键：`sorted(d, key=d.get)`。

## 使用场景

- 把字典的键导出去做配置项列表。
- 统计值的分布（先 `list(d.values())`）。
- 排序输出、转成 CSV 的一行。
