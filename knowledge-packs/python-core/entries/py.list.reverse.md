---
id: py.list.reverse
title: 反转列表
description: 把顺序倒过来，注意有两种写法、结果不一样
language: python
category_id: programming.basics
module: list
origin: builtin
import: ""
qualname: "list.reverse() / reversed()"
signature: "items.reverse() / reversed(items) / items[::-1]"
args:
  - name: "items"
    required: true
    accepts: "列表（reverse 要求可变序列；reversed 只要求可迭代）"
    nesting: "可以"
returns: "reverse 返回 None（原地改）；reversed 返回迭代器；[::-1] 返回新列表"
object:
  id: list.element
  name: 列表元素
  aliases: [列表, 顺序, 反转, 倒序, items]
action:
  id: modify.change
  name: 修改
  aliases: [反转, 倒过来, 倒序, 逆序, reverse]
targets: []
utterances:
  direct:
    - 反转列表
    - 把列表顺序倒过来
    - 列表倒序
  questions:
    - 怎么反转一个列表
    - reverse 和 [::-1] 有什么区别
    - 反转之后原列表会变吗
  colloquial:
    - 想从后往前排
    - 倒着处理一遍
  technical:
    - list.reverse
    - reversed
    - 负数步长切片
  short_queries:
    - 反转
    - 倒序
    - reverse
status: tested
tested_versions: ["3.10", "3.11", "3.12", "3.13", "3.14"]
min_version: "3.0"
version_note: "reverse / reversed / 切片三种写法各版本一致"
sources:
  - Python 官方文档 list.reverse
---

# 反转列表

## 功能描述

把元素顺序颠倒。三种写法：`list.reverse()` 原地改、`reversed()` 返回迭代器、`[::-1]` 返回新列表。

## 推荐代码

```python
a = [1, 2, 3]

a.reverse()          # 原地改，返回 None
print(a)             # [3, 2, 1]

b = [1, 2, 3]
c = list(reversed(b))
print(b, c)          # [1, 2, 3] [3, 2, 1]  ← b 没变

d = [1, 2, 3][::-1]
print(d)             # [3, 2, 1]
```

## 语句解释

### list.reverse()

**原地改，返回 None**。写成 `a = a.reverse()` 会得到 None。

### reversed(items)

返回**迭代器**，不建新列表；要列表就 `list(...)`。能用于任何可迭代对象。

### items[::-1]

切片造一个新列表，最短的写法。

## 原理解释

**一句话：** `reverse` 是把首尾两两交换、往中间收；`reversed` 是「倒着走」的视角，不搬数据。

**执行逻辑（reverse）：**

1. 两个指针：一个指头、一个指尾
2. 交换这两个位置的元素
3. 头指针往后、尾指针往前
4. 两个指针相遇就停
5. 返回 None

**执行逻辑（reversed）：**

1. 记下序列，从最后一个元素开始
2. 每次往前挪一个交给你
3. 全程不复制，所以很快

**机器层（可跳过）：** `reverse` 是 O(n) 的交换；`reversed` 几乎零开销，但只能走一遍。

**边界（从逻辑推出来）：**

- `reverse` 第 5 步返回 None，所以不能赋值接收
- `reversed` 第 3 步不复制，所以原列表改了它看到的也变
- `reversed` 返回迭代器，遍历一次就空
- 只想「从后往前遍历」直接用 `for x in reversed(items)`，不必造新列表

## 注意事项

- `a = a.reverse()` 是经典错误，得到 None。
- 需要保留原顺序就用 `reversed` 或 `[::-1]`。
- `reversed` 对字符串、元组也能用。
- 反转不等于排序，别和 `sorted(..., reverse=True)` 搞混。

## 使用场景

- 最新记录排前面（日志倒序展示）。
- 撤销栈的遍历。
- 从后往前处理列表而不想改原列表。
