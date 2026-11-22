---
id: py.list.flatten
title: 展平嵌套列表
description: 二维列表压成一维，别用错写法
language: python
category_id: programming.basics
module: list
origin: builtin
import: ""
qualname: "列表推导式 [x for row in m for x in row]"
signature: "[x for row in matrix for x in row]"
args:
  - name: "matrix"
    required: true
    accepts: "嵌套的列表（二维或更多层）"
    nesting: "可以，多层要多写几个 for"
returns: "列表：压平一层后的元素；只压一层，深层还是嵌套"
object:
  id: list.element
  name: 列表元素
  aliases: [列表, 嵌套列表, 二维列表, 展平, items]
action:
  id: convert.transform
  name: 转换
  aliases: [展平, 压平, 拍平, 变成一维, flatten]
targets: []
utterances:
  direct:
    - 展平嵌套列表
    - 二维列表变一维
    - 把列表的列表压平
  questions:
    - 怎么把嵌套列表展平
    - 两个 for 的推导式怎么写
    - 多层嵌套怎么完全展平
  colloquial:
    - 一堆小列表想合成一个大列表
    - 外面套了一层 list，想拆掉那层
  technical:
    - 列表展平
    - 嵌套推导式
    - itertools.chain
    - 递归展平
  short_queries:
    - 展平
    - flatten
    - 压平
status: tested
tested_versions: ["3.10", "3.11", "3.12", "3.13", "3.14"]
min_version: "3.0"
version_note: "嵌套推导式与 chain 各版本一致"
sources:
  - Python 官方教程 列表推导式
  - Python 官方文档 itertools.chain
---

# 展平嵌套列表

## 功能描述

输入「列表的列表」，输出把它们接起来的一维列表；**只压一层**。

## 推荐代码

```python
matrix = [[1, 2], [3], [4, 5]]

print([x for row in matrix for x in row])      # [1, 2, 3, 4, 5]

from itertools import chain
print(list(chain.from_iterable(matrix)))       # [1, 2, 3, 4, 5]

# 反例：这样只得到原样的子列表
print([row for row in matrix])                 # [[1,2],[3],[4,5]]
```

## 语句解释

### [x for row in matrix for x in row]

两个 `for` 从左往右读：先外层（取每个子列表），再内层（取子列表里的元素）。

### chain.from_iterable(matrix)

把每个子列表当一条流水依次取完，不建中间列表。

### 为什么容易写错

`[x for x in matrix]` 里的 `x` 是**子列表**，不是元素。

## 原理解释

**一句话：** 它先走外层拿一个子列表，再走内层把子列表里的每个元素吐出来。

**执行逻辑：**

1. 从外层取第一个子列表
2. 从子列表取第一个元素，放进结果
3. 子列表取完，换下一个子列表
4. 全部取完，返回结果列表

**机器层（可跳过）：** 一趟遍历，元素总数 n 次操作。

**边界（从逻辑推出来）：**

- 第 2 步只取一层，所以 `[[[1]]]` 展平后还是 `[[1]]`
- 元素必须都是可迭代的，混进数字会抛 TypeError
- 它按顺序吐出，所以顺序与原嵌套结构一致
- 数据大时用 `chain`（惰性）比推导式（一次建成）省内存

## 注意事项

- 只能压一层，多层要递归或写多个 `for`。
- 列表里有非列表元素（如数字）会报错，先过滤。
- 想保留原结构别展平，注意别把 `[x for x in matrix]` 当展平。
- 展平是浅拷贝，内层元素还是原对象。

## 使用场景

- 合并多个批次的结果。
- 把矩阵压成一行做统计。
- 处理 `[[(k,v)], ...]` 这类嵌套结果。
