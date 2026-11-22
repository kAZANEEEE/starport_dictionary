---
id: py.list.count
title: 数某个值出现几次
description: 列表里这个值有几个（列表自带的简单计数）
language: python
category_id: programming.basics
module: list
origin: builtin
import: ""
qualname: "list.count()"
signature: "items.count(值)"
args:
  - name: "值"
    required: true
    accepts: "任何值；比较用的是 ==（所以 1 和 True 会被当成同一个）"
    nesting: "可以，可以是变量"
returns: "整数：出现了几次；值不存在返回 0（不报错）"
object:
  id: list.element
  name: 列表元素
  aliases: [列表, 元素, 某个值, 出现次数, items]
action:
  id: get.obtain
  name: 获取
  aliases: [数, 统计, 计数, 出现几次, count]
targets: []
utterances:
  direct:
    - 数列表里某个值出现几次
    - 统计元素出现次数
    - list.count 怎么用
  questions:
    - 怎么数列表里某个值有几个
    - count 和 Counter 有什么区别
    - 统计多个值的次数怎么写
  colloquial:
    - 想知道这个值出现了几次
    - 要统计每个元素的次数，一个个 count 太慢
  technical:
    - list.count
    - collections.Counter
    - 计数复杂度
  short_queries:
    - 计数
    - count
    - 出现几次
status: tested
tested_versions: ["3.10", "3.11", "3.12", "3.13", "3.14"]
min_version: "3.0"
version_note: "list.count 各版本一致；每次调用都是一趟遍历"
sources:
  - Python 官方文档 list.count
---

# 数某个值出现几次

## 功能描述

输入一个值，输出它在列表里出现了几次；找不到返回 0，不报错。

## 推荐代码

```python
items = [1, 2, 2, 3, 2]

print(items.count(2))     # 3
print(items.count(99))    # 0

# 要统计「每个元素」各几次，别循环 count
from collections import Counter
print(Counter(items))     # Counter({2: 3, 1: 1, 3: 1})
```

## 语句解释

### list.count(值)

每调一次就从头扫一遍，所以只适合「偶尔数一个值」。

### 为什么不要循环 count

对每个不同的值调一次 count，就是 N 次全表扫描，数据一多就慢。

### Counter 的定位

一次遍历统计所有元素，是多值统计的正确工具。

## 原理解释

**一句话：** 它从头到尾走一遍，每次遇到相等的就 +1。

**执行逻辑：**

1. 计数器从 0 开始
2. 取一个元素，和你给的值用 `==` 比
3. 相等就 +1
4. 走完全部元素，返回计数

**机器层（可跳过）：** 一趟遍历，O(n)；调用多次就是多次 O(n)。

**边界（从逻辑推出来）：**

- 第 2 步用 `==` 比较，所以 `1` 与 `True`、`1` 与 `1.0` 都算相等
- 每次调用都重新扫一遍，所以「统计所有值」是 O(n×不同值个数)
- 找不到返回 0，不抛异常——所以不能靠它判断「有没有这个值」（那用 `in` 更清楚）
- 它只处理列表这一层，嵌套列表里的元素不会被统计

## 注意事项

- 统计多个值的次数用 `Counter`，不要循环 `count`。
- `count` 不报错，找「有没有」请用 `in`。
- 浮点数比较有精度问题，别用 count 判等。
- 巨大的列表里频繁 count 会明显变慢。

## 使用场景

- 数某个标记出现了几次。
- 检查数据里有没有重复过多（配合阈值判断）。
- 简单的出现次数断言（测试里）。
