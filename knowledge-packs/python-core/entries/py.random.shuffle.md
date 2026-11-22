---
id: py.random.shuffle
title: 打乱列表顺序
description: 把列表里元素顺序随机重排
language: python
category_id: programming.basics
module: random
origin: stdlib
import: "import random"
qualname: "random.shuffle"

object:
  id: list.element
  name: 列表元素
  aliases: [列表, 元素, 顺序, 排列, items]

action:
  id: modify.change
  name: 修改
  aliases: [打乱, 洗牌, 重排, 随机排序, shuffle]

targets: []

utterances:
  direct:
    - 打乱列表顺序
    - 洗牌
    - 随机重排列表
  questions:
    - 怎么打乱一个列表
    - 如何随机排序列表
    - Python 怎么洗牌
  colloquial:
    - 想让顺序随机一点
    - 把这几项随机打散
  technical:
    - random.shuffle
    - random.sample
    - random.sample shuffled
  short_queries:
    - 打乱
    - shuffle
    - 洗牌

status: tested
tested_versions: ["3.10", "3.11", "3.12", "3.13", "3.14"]
min_version: "3.0"
version_note: random.shuffle 接口稳定，3.11 起增加 random 参数的用法
sources:
  - Python 官方文档 random.shuffle
  - Python 官方文档 random.sample
---

# 打乱列表顺序

## 功能描述

把列表里元素的顺序随机重排。**原地修改**，返回 `None`。

## 推荐代码

```python
import random

items = [1, 2, 3, 4, 5]
random.shuffle(items)
print(items)                       # 顺序变了，还是这五个数

# 想要"打乱后的副本"、不动原列表：
original = [1, 2, 3, 4, 5]
shuffled = random.sample(original, k=len(original))
print(original, shuffled)
```

## 语句解释

### random.shuffle(list)

原地洗牌，**返回 None**。写成 `items = random.shuffle(items)` 会得到 None，这是经典坑。

### random.sample(seq, k)

从中取 k 个不重复元素。`k = len(seq)` 就等于“打乱后的副本”，原列表不动。

## 原理解释

**一句话：** 从最后一个位置开始，每个位置和前面某个随机位置交换一下，交换完整串就乱了。

**执行逻辑：**

1. 从最后一个位置 i 开始
2. 在 0..i 里摇一个随机位置 j
3. 交换 i 和 j 两个位置上的元素
4. i 往前挪一位，重复 2–3
5. 走到第 1 个位置就结束——**原地改，不返回新列表**

**机器层（可跳过）：** 线性时间；每一步只做一次交换。

**边界（从逻辑推出来）：**

- 第 3 步是「和已经处理过的区间以外的位置」交换，所以每种排列出现概率相同；用 `sorted(key=random)` 做不到这点，分布会不均
- 第 5 步原地改，所以 `items = random.shuffle(items)` 会得到 None
- 想要「打乱后的副本」用 `random.sample(items, len(items))`，原列表不动
- 元素本身没被复制，列表里是可变对象时还是同一批对象
## 注意事项

- `shuffle` 原地改，返回 None；要副本用 `sample`。
- 别用 `sorted(key=random.random())` 洗牌，分布不对。
- 元素本身不会被复制，列表里是可变对象时仍是同一批对象。
- 需要可复现就 `random.seed(...)` 先固定。

## 使用场景

- 抽签、发牌、随机分组。
- 打乱训练数据顺序。
- 生成随机顺序的测试用例。
