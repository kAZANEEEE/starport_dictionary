---
id: py.list.insert
title: 在指定位置插入元素
description: 插到某个下标前面，不是替换
language: python
category_id: programming.basics
module: list
origin: builtin
import: ""
qualname: "list.insert()"

object:
  id: list.element
  name: 列表元素
  aliases: [列表, 元素, 位置, 下标, items]

action:
  id: modify.change
  name: 修改
  aliases: [插入, 插到前面, 添加, 放到指定位置, insert]

targets: []

utterances:
  direct:
    - 在指定位置插入元素
    - 往列表中间插一个
    - 插入到某个下标
  questions:
    - 怎么在列表中间插入元素
    - insert 和 append 有什么区别
    - 下标越界会怎样
  colloquial:
    - 想插到第一个位置
    - 插进去之后后面的都往后挪了吗
  technical:
    - list.insert
    - list.append
    - 负下标插入
    - 插入代价
  short_queries:
    - 插入
    - insert
    - 中间插入

status: tested
tested_versions: ["3.10", "3.11", "3.12", "3.13", "3.14"]
min_version: "3.0"
version_note: "list.insert 各版本一致；越界时按 append 处理"
sources:
  - Python 官方文档 list.insert
---

# 在指定位置插入元素

## 功能描述

输入下标 + 元素，把元素插到该下标**之前**（原元素和后面全部后移）；原地修改，返回 None。

## 推荐代码

```python
nums = [1, 2, 3]

nums.insert(1, 99)
print(nums)       # [1, 99, 2, 3]  ← 插在 2 前面

nums.insert(0, 0)
print(nums)       # [0, 1, 99, 2, 3]  ← 插到最前

nums.insert(-1, 88)
print(nums)       # [0, 1, 99, 2, 88, 3]  ← 插在最后一个之前

nums.insert(100, 7)
print(nums[-1])   # 7  ← 越界等价于 append
```

## 语句解释

### insert(下标, 元素)

把元素放到这个下标位置，原来的元素往后挪。

### 负下标

`-1` 表示「插在最后一个元素之前」，不是插到最后。

### 越界不报错

超过长度就等同于追加到末尾——这点和 `pop`/`索引` 不一样，**insert 不抛越界异常**。

## 原理解释

**一句话：** 它在那个位置腾出一个格子，把后面的元素全部往后挪一格，再把新元素放进去。

**执行逻辑：**

1. 把下标换算成合法位置（负数从末尾算，越界就夹到末尾）
2. 从列表末尾开始，把 `i` 及之后的元素逐个往后挪一格
3. 把新元素放到位置 `i`
4. 长度加 1，返回 None

**机器层（可跳过）：** 挪动是内存拷贝，所以插在前面比插在后面贵，O(n)。

**边界（从逻辑推出来）：**

- 第 1 步把越界夹到末尾，所以 `insert(100, x)` 等于 `append(x)`，**不报错**
- 第 2 步要挪动，所以列表很大又频繁在头部插入时会明显变慢
- `insert(-1, x)` 插在「最后一个之前」，因为 -1 指向最后那个元素的位置
- 它原地改并返回 None，所以 `nums = nums.insert(...)` 会得到 None

## 注意事项

- `insert(-1, x)` 不是「插到最后」，那是 `append`。
- 频繁头部插入用 `collections.deque`（`appendleft` 是 O(1)）。
- 越界不报错，所以下标算错时不容易发现。
- 返回 None，别赋值接收。

## 使用场景

- 把元素插到指定顺序里（保持有序）。
- 在列表头部插入（少量数据）。
- 构造特定排列的测试数据。
