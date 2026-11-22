---
id: py.list.sort_multi
title: 按多个字段排序
description: 先按分数排，分数相同再按名字排
language: python
category_id: programming.algorithms
module: list
origin: builtin
import: ""
qualname: "sorted(key=lambda x: (字段1, 字段2))"
signature: "sorted(items, key=lambda x: (第一依据, 第二依据))"
args:
  - name: "items"
    required: true
    accepts: "要排序的列表（元素通常是字典或对象）"
    nesting: "可以"
  - name: "key"
    required: true
    accepts: "返回元组的函数：元组里靠前的字段优先级更高"
    nesting: "可以，元组里能写任意表达式"
returns: "新列表：按多个字段依次比较后的顺序；原列表不变"
object:
  id: list.element
  name: 列表元素
  aliases: [列表, 排序, 多个字段, 优先级, items]
action:
  id: sort.order
  name: 排序
  aliases: [排序, 多字段排序, 按优先级排, 二级排序, sort]
targets: []
utterances:
  direct:
    - 按多个字段排序
    - 多条件排序
    - 主要按分数，其次按名字
  questions:
    - 怎么按两个字段排序
    - 分数一样时怎么按名字排
    - 一个升序一个降序怎么写
  colloquial:
    - 先按分数排，分数一样再按名字
    - 排序有并列，想再定个规则
  technical:
    - sorted key tuple
    - 多级排序
    - sort 稳定性
    - 降序混排
  short_queries:
    - 多字段排序
    - 二级排序
    - key 元组
status: tested
tested_versions: ["3.10", "3.11", "3.12", "3.13", "3.14"]
min_version: "3.0"
version_note: "key 返回元组的写法各版本一致"
sources:
  - Python 官方文档 sorted
---

# 按多个字段排序

## 功能描述

输入列表 + 一个返回元组的 key 函数，输出按「元组里靠前字段优先」排好的新列表。

## 推荐代码

```python
people = [
    {"name": "张三", "score": 90},
    {"name": "李四", "score": 95},
    {"name": "王五", "score": 90},
]

by_score_name = sorted(people, key=lambda p: (p["score"], p["name"]))
print([p["name"] for p in by_score_name])   # ['张三', '王五', '李四']

# 一个升序一个降序：分数降序、名字升序
mixed = sorted(people, key=lambda p: (-p["score"], p["name"]))
print([(p["name"], p["score"]) for p in mixed])
```

## 语句解释

### key=lambda p: (p["score"], p["name"])

返回元组。Python 比元组是**从前往后逐个比**，前面相等才看后面。

### 降序用负号

`-p["score"]` 把数值取负，降序就变成升序——只对数字方便。

### 稳定性

排序是稳定的：key 完全相等的元素保持原顺序。

## 原理解释

**一句话：** 每个元素先被换成一个「比较用的元组」，然后按元组的字典序排队。

**执行逻辑：**

1. 对每个元素调一次 key，得到元组
2. 比较两个元组：先比第 1 个元素
3. 第 1 个相等 → 比第 2 个，以此类推
4. 全部相等 → 保持原顺序（稳定）
5. 按排好的顺序把原元素摆回去

**机器层（可跳过）：** 比较次数约 n log n，每次比较可能看多个字段。

**边界（从逻辑推出来）：**

- 第 2–3 步是元组的字典序，所以**字段顺序就是优先级**
- 想「一个升一个降」只能靠取负或分成两次排序（先按次要比，再按主次比，利用稳定性）
- 第 4 步的稳定性来自 Timsort，所以两次 `sorted` 能实现混排
- 元组里比较的类型必须一致，字符串和数字混着比会抛 TypeError

## 注意事项

- 字段顺序决定优先级，别写反。
- 混排（一升一降）要么取负，要么拆成两次 `sorted`（后一次是主序）。
- 字符串降序取负不行，得两次排序或自定义包装。
- 中文按码位比，不是拼音。

## 使用场景

- 排行榜：分数降序、同分按名字。
- 文件列表：先按类型、再按大小。
- 报表输出前统一排序。
