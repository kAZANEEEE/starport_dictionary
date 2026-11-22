---
id: py.itertools.product
title: 生成所有组合（笛卡尔积）
description: 两个列表的所有搭配，一个不漏
language: python
category_id: programming.basics
module: itertools
origin: stdlib
import: "from itertools import product"
qualname: "itertools.product"

object:
  id: list.element
  name: 列表元素
  aliases: [列表, 组合, 所有搭配, 元素, items]

action:
  id: create.new
  name: 创建
  aliases: [生成组合, 枚举所有, 笛卡尔积, 全排列组合, product]

targets: []

utterances:
  direct:
    - 生成所有组合
    - 两个列表的所有搭配
    - 求笛卡尔积
  questions:
    - 怎么列出两个列表的所有组合
    - 如何生成所有可能的搭配
    - product 和 zip 有什么区别
  colloquial:
    - 所有搭配都想试一遍
    - 颜色和尺寸的所有组合
  technical:
    - itertools.product
    - repeat 参数
    - 排列组合 permutations combinations
  short_queries:
    - 组合
    - 笛卡尔积
    - product

status: tested
tested_versions: ["3.10", "3.11", "3.12", "3.13", "3.14"]
min_version: "3.0"
version_note: "product 各版本一致；repeat 参数也是 3.x 全支持"
sources:
  - Python 官方文档 itertools.product
---

# 生成所有组合（笛卡尔积）

## 功能描述

输入两个（或多个）可迭代对象，输出「每种搭配都出现一次」的元组序列；总数 = 各列表长度的乘积。

## 推荐代码

```python
from itertools import product

colors = ["红", "蓝"]
sizes = ["S", "M"]

for c, s in product(colors, sizes):
    print(c, s)          # 4 种搭配

print(list(product([0, 1], repeat=2)))   # [(0,0),(0,1),(1,0),(1,1)]
```

## 语句解释

### product(a, b)

返回所有 `(a 的元素, b 的元素)` 组合，顺序是「后面的变化最快」。

### repeat=2

同一个序列自己和自己组合，等价于 `product(x, x)`。

### 和 zip 的区别

`zip` 是**一一对应**（成对往下走），`product` 是**每种都配一遍**。

## 原理解释

**一句话：** 它像里程表——最后一位先转完一圈，再进一位，把所有读数都列一遍。

**执行逻辑：**

1. 固定第一个列表的第一个元素
2. 把第二个列表的元素依次配一遍，全部输出
3. 第二个列表转完 → 第一个列表换下一个元素，回到第 2 步
4. 第一个列表也走完 → 结束

**机器层（可跳过）：** 惰性生成，一个算一个；总数多时内存不会一次爆，但**遍历总耗时**是各长度的乘积。

**边界（从逻辑推出来）：**

- 第 2 步「后面的变化最快」决定了输出顺序，要和别的库对上顺序时注意
- 总数是乘积，所以 3 个 10 元素列表 = 1000 组，4 个就是 1 万——**组合爆炸要提前估**
- 因为惰性，`product(...)` 本身不占内存，`list(product(...))` 才占
- 它不做去重也不排序，输入有重复元素就会有重复组合

## 注意事项

- 总数是乘积，别在大列表上直接 `list(...)`。
- 只要成对往下走用 `zip`，要所有搭配才用 `product`。
- 需要「不重复的排列/组合」用 `permutations` / `combinations`。
- 结果顺序固定但依赖输入顺序，测试时注意。

## 使用场景

- 参数网格（颜色 × 尺寸 × 面料）。
- 穷举测试用例组合。
- 双循环的替代（`for a in A: for b in B` 可写成 `product`）。
