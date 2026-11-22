---
id: py.list.enumerate
title: 遍历时带上下标
description: 循环时同时拿到「第几个」和「元素」
language: python
category_id: programming.basics
module: builtins
origin: builtin
import: ""
qualname: "enumerate"
signature: "enumerate(items, start=0)"
args:
  - name: "items"
    required: true
    accepts: "任何可迭代对象"
    nesting: "可以"
  - name: "start"
    required: false
    default: "0"
    accepts: "序号从几开始；给人看的编号一般写 1"
    nesting: "一般直接写数字"
returns: "迭代器：每次给 (序号, 元素) 两个值"

object:
  id: list.element
  name: 列表元素
  aliases: [列表, 元素, 下标, 序号, items]

action:
  id: traverse.walk
  name: 遍历
  aliases: [遍历, 循环, 带下标遍历, 编号, enumerate]

targets: []

utterances:
  direct:
    - 遍历时带下标
    - 循环同时拿到序号
    - 给元素编号遍历
  questions:
    - 怎么在循环里同时拿到下标和元素
    - 如何从 1 开始编号
    - range(len(lst)) 和 enumerate 哪个好
  colloquial:
    - 想边循环边知道是第几个
    - 不想自己维护一个计数器
  technical:
    - enumerate
    - start 参数
    - 不要用 range(len)
  short_queries:
    - enumerate
    - 下标
    - 编号

status: tested
tested_versions: ["3.10", "3.11", "3.12", "3.13", "3.14"]
min_version: "3.0"
version_note: enumerate 的 start 参数各版本一致
sources:
  - Python 官方文档 enumerate
---

# 遍历时带上下标

## 功能描述

输入可迭代对象，输出「(序号, 元素)」对；序号默认从 0 开始，可用 `start=` 改。

## 推荐代码

```python
items = ["a", "b", "c"]

for i, item in enumerate(items):
    print(i, item)

for i, item in enumerate(items, start=1):
    print(f"第 {i} 个是 {item}")
```

## 语句解释

### enumerate(items)

每次产出 `(下标, 元素)` 两个值，用 `for i, item in` 一次接住。

### start=1

序号从 1 开始。只影响计数，不影响元素。

### 为什么不用 range(len(items))

那个写法要索引两次（`items[i]`），而且对生成器之类没有下标的东西根本不能用。

## 原理解释

**一句话：** 它一边遍历，一边自己数个数，每取一个就报「这是第几个」和「内容是什么」。

**执行逻辑：**

1. 准备一个计数器，初值 = `start`（默认 0）
2. 从可迭代对象里取一个元素
3. 产出 `(当前计数, 元素)`
4. 计数器加 1
5. 回到第 2 步，直到取完

**机器层（可跳过）：** 它本身是惰性迭代器，取一个算一个，不预先造列表。

**边界（从逻辑推出来）：**

- 第 3 步先产出后加 1，所以第一个元素的序号就是 `start`
- 因为第 2 步是「取一个」，所以它能用于生成器、文件对象这些没有下标的东西
- 它是惰性的，所以在循环中途 `break` 时后面根本没算过
- 想同时知道总数还得自己 `len()`（生成器没有长度）

## 注意事项

- 别在循环里对同一个 `enumerate` 对象再遍历一次，它已经被消费完了。
- 需要序号时优先 `enumerate`，`range(len(...))` 是可读性更差的写法。
- 序号只是计数，不代表数据的业务含义。
- 中文环境从 1 开始计数就显式写 `start=1`。

## 使用场景

- 输出带编号的列表。
- 批量处理时打印进度。
- 需要「第一个特殊处理」的逻辑。
