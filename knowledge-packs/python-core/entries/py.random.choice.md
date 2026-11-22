---
id: py.random.choice
title: 随机选一个
description: 从列表里随机挑一个元素
language: python
category_id: programming.basics
module: random
origin: stdlib
import: "import random"
qualname: "random.choice"

object:
  id: random.number
  name: 随机数
  aliases: [随机, 随机数, 随机值, 抽样, random]

action:
  id: get.obtain
  name: 获取
  aliases: [选, 挑, 抽, 取, 随机取, choice]

targets: []

utterances:
  direct:
    - 随机选一个
    - 从列表里随机取一个
    - 随机抽一个元素
  questions:
    - 怎么从列表里随机选一个
    - 如何随机抽取一个元素
    - Python 怎么生成随机整数
  colloquial:
    - 想随便挑一个出来
    - 抽奖那种，随机抽一个
  technical:
    - random.choice
    - random.randint
    - random.seed
  short_queries:
    - 随机
    - choice
    - 抽取

status: tested
tested_versions: ["3.10", "3.11", "3.12", "3.13", "3.14"]
min_version: "3.0"
version_note: random.choice / randint 接口稳定；3.11 起 random 模块算法实现有调整，行为不变
sources:
  - Python 官方文档 random.choice
  - Python 官方文档 random.randint
---

# 随机选一个

## 功能描述

从序列里随机挑一个元素，或者生成一个随机整数。

## 推荐代码

```python
import random

colors = ["红", "绿", "蓝"]
print(random.choice(colors))        # 随机一个颜色

print(random.randint(1, 6))         # 1 到 6，含两端（掷骰子）
print(random.randrange(1, 6))       # 1 到 5，不含右端

random.seed(42)                     # 固定种子 → 结果可复现
print(random.choice(colors))
```

## 语句解释

### random.choice(seq)

从序列里随机取一个元素，序列不能是空的。字符串也行，取出来是单个字符。

### random.randint(a, b)

随机整数，**包含 a 和 b 两端**。掷骰子就是 `randint(1, 6)`。

### random.randrange(start, stop)

和 `range` 一样**不含右端**。这两个差一位，是常见错误来源。

### random.seed(n)

固定种子后，随机序列固定，方便复现和写测试。

## 原理解释

**一句话：** 先摇一个「第几个」的随机数，再按这个数从序列里取出来。

**执行逻辑：**

1. 摇一个 0 到「长度-1」之间的整数（伪随机）
2. 用这个下标从序列里取出元素返回
3. 序列为空时，第 1 步就没有合法的下标可摇 → 抛 `IndexError`

**机器层（可跳过）：** 伪随机数由种子决定，同一种子必然得到同一串结果。

**边界（从逻辑推出来）：**

- 第 1 步的上界包含两端吗？`choice` 内部用的是「0 到 len-1」，所以不会越界；但 `randint(1,6)` 是**含两端**，`randrange(1,6)` **不含右端**，这两个差一位
- 因为结果是伪随机，`random.seed(n)` 之后序列固定，可以复现和写测试
- 伪随机**不可预测性不足**，生成密码/token 必须用 `secrets`
- 第 3 步空序列直接报错，调用前要判空
## 注意事项

- `randint` 含两端，`randrange` 不含，选错会差一位。
- 空序列调用 `choice` 会抛 `IndexError`。
- 不要用 `random` 生成密码、token —— 用 `secrets`。
- 多进程/多线程里共用同一个随机状态可能拿到相同结果，各自 seed 或换 `random.Random()` 实例。

## 使用场景

- 抽奖、摇骰子、随机点名。
- 造测试数据。
- 随机打乱后取前 N 个做样本。
