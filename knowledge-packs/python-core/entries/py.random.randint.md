---
id: py.random.randint
title: 生成随机整数
description: 在指定范围里随机取一个整数
language: python
category_id: programming.basics
module: random
origin: stdlib
import: "import random"
qualname: "random.randint()"
signature: "random.randint(a, b)"
args:
  - name: "a, b"
    required: true
    accepts: "整数范围，**包含两端**；要不含右端用 randrange"
    nesting: "可以，可以是变量"
returns: "整数：a 到 b 之间（含两端）的一个随机数"

object:
  id: random.number
  name: 随机数
  aliases: [随机数, 随机整数, 范围, 随机值, random]

action:
  id: get.obtain
  name: 获取
  aliases: [随机取, 生成, 抽取, 获得, randint]

targets: []

utterances:
  direct:
    - 生成随机整数
    - 取一个范围内的随机数
    - 随机一个整数
  questions:
    - 怎么生成指定范围的随机整数
    - randint 包含两端吗
    - 如何生成不重复的随机数
  colloquial:
    - 想随便取个 1 到 100 的数
    - 摇色子那种随机
  technical:
    - random.randint
    - random.randrange
    - random.sample 不重复
    - seed 可复现
  short_queries:
    - 随机数
    - randint
    - 范围

status: tested
tested_versions: ["3.10", "3.11", "3.12", "3.13", "3.14"]
min_version: "3.0"
version_note: "randint / randrange / sample 各版本一致"
sources:
  - Python 官方文档 random.randint
---

# 生成随机整数

## 功能描述

输入下界、上界，输出它们之间（**含两端**）的一个随机整数；要「不含右端」用 `randrange`。

## 推荐代码

```python
import random

random.seed(42)                     # 固定种子，结果可复现
print(random.randint(1, 6))         # 1..6 含两端，像骰子
print(random.randrange(1, 6))       # 1..5 不含右端
print(random.randrange(0, 100, 10)) # 0,10,...,90 带步长

print(random.sample(range(1, 46), 6))   # 不重复抽 6 个（彩票式）
```

## 语句解释

### randint(a, b)

**包含 a 和 b 两端**。`randint(1, 6)` 就是骰子。

### randrange(a, b[, step])

和 `range` 一致：**不含右端**，可带步长。

### sample(序列, k)

从里面抽 k 个**不重复**元素，返回列表。

## 原理解释

**一句话：** 它先在范围里算出「有多少个可能的整数」，摇一个下标，再加回起点。

**执行逻辑：**

1. 算出范围内整数个数 `n = b - a + 1`（`randint` 含两端所以 +1）
2. 摇一个 `0..n-1` 的伪随机整数 `r`
3. 返回 `a + r`
4. `randrange` 只是 `n` 的算法不同（不带 +1、支持步长）

**机器层（可跳过）：** 伪随机数由种子和内部状态决定，同种子必然同序列。

**边界（从逻辑推出来）：**

- 第 1 步的 `+1` 就是「含两端」的实现，`randrange` 不给这个 +1，所以差一位
- `a > b` 时抛 `ValueError`，空范围没有合法下标
- 因为第 2 步是伪随机，`random.seed(n)` 后序列固定——测试里要靠它
- 伪随机**不可预测性不足**，生成密码/令牌要用 `secrets.randbelow`

## 注意事项

- `randint` 含两端、`randrange` 不含，差一位最容易错。
- 要「不重复的多个随机数」用 `sample`，不要循环 `randint` 去重。
- 写测试先 `seed`，否则偶发失败查不出来。
- 别用 `random` 生成密钥。

## 使用场景

- 骰子、抽奖、随机步数。
- 造测试数据。
- 随机抽样做检查。
