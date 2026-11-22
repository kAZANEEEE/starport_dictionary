---
id: py.itertools.chain
title: 串联多个列表一起处理
description: 把几个列表接成一条流水，挨个处理
language: python
category_id: programming.basics
module: itertools
origin: stdlib
import: "from itertools import chain"
qualname: "itertools.chain"

object:
  id: list.element
  name: 列表元素
  aliases: [列表, 多个列表, 元素, 序列, items]

action:
  id: traverse.walk
  name: 遍历
  aliases: [串联, 连接后遍历, 合并遍历, 串起来, chain]

targets: []

utterances:
  direct:
    - 串联多个列表
    - 把几个列表接起来遍历
    - 合并多个列表
  questions:
    - 怎么把多个列表连成一个
    - 如何遍历几个列表的所有元素
    - chain 和 + 拼接有什么区别
  colloquial:
    - 手上好几个列表，想一次全过一遍
    - 不想先拼成一个大列表再循环
  technical:
    - itertools.chain
    - chain.from_iterable
    - 拼接列表代价
  short_queries:
    - 串联
    - chain
    - 合并列表

status: tested
tested_versions: ["3.10", "3.11", "3.12", "3.13", "3.14"]
min_version: "3.0"
version_note: chain 与 chain.from_iterable 各版本稳定
sources:
  - Python 官方文档 itertools.chain
---

# 串联多个列表一起处理

## 功能描述

输入若干个可迭代对象，输出一条「依次取完所有元素」的流水线；**不复制数据**。

## 推荐代码

```python
from itertools import chain

a = [1, 2]
b = [3, 4]

print(list(chain(a, b)))              # [1, 2, 3, 4]
print(sum(chain(a, b)))               # 10

groups = [[1, 2], [3], [4, 5]]
print(list(chain.from_iterable(groups)))   # [1, 2, 3, 4, 5]
```

## 语句解释

### chain(a, b)

把 a 和 b 串起来，先取完 a 再取 b。

### chain.from_iterable(嵌套结构)

输入「列表的列表」，一层展开——等价于把每一层当参数传给 `chain`。

### list(...)

`chain` 返回迭代器，要列表才 `list()`，要求和直接传给 `sum()` 更省内存。

## 原理解释

**一句话：** 它记着「现在在第几个列表」，取完一个就换成下一个，从头到尾没拼过新列表。

**执行逻辑：**

1. 记住第一个来源，从它开始取元素
2. 取完第一个 → 切到第二个来源，从头取
3. 依次类推，直到最后一个也取完
4. 整个过程只在需要时元素才被产出（惰性）

**机器层（可跳过）：** 不分配新的容器，只保存「当前在第几个来源」。

**边界（从逻辑推出来）：**

- 第 4 步是惰性，所以可以串接无限长的生成器（比如读文件的行）
- 因为没复制数据，原始的列表改了会影响遍历结果（它不是快照）
- 和 `a + b` 的区别：`+` 会真的复制出一个新列表，数据大时内存翻倍
- `chain` 返回迭代器，只能遍历一次

## 注意事项

- 只遍历一次，需要多次就得 `list()` 存下来（但那又变回占内存）。
- 需要「串联后去重/排序」的，先 `chain` 再交给 `set`/`sorted`。
- `chain(a)` 和不加参数的区别：`chain()` 是空序列。
- 想拼接字符串列表并加分隔符，用 `"".join(...)` 不是 `chain`。

## 使用场景

- 多批数据统一处理（分页结果、多个文件的行）。
- 展平一层嵌套列表。
- 把多个来源塞进 `sum` / `max` / `any` 这种聚合函数。
