---
id: py.list.extend
title: 往列表里追加多个元素
description: 一次把另一个列表的内容接到末尾
language: python
category_id: programming.basics
module: list
origin: builtin
import: ""
qualname: "list.extend()"
signature: "items.extend(另一批)"
args:
  - name: "另一批"
    required: true
    accepts: "任何可迭代对象；字符串会被拆成单个字符"
    nesting: "可以，可以是另一个列表、生成器、字典的键"
returns: "None：原地把元素接到末尾（返回 None，别赋值接收）"

object:
  id: list.element
  name: 列表元素
  aliases: [列表, 元素, 多个元素, 一批数据, items]

action:
  id: modify.change
  name: 修改
  aliases: [追加, 添加, 扩展, 接到末尾, extend, append]

targets: []

utterances:
  direct:
    - 往列表追加多个元素
    - 把另一个列表接到末尾
    - 扩展列表
  questions:
    - extend 和 append 有什么区别
    - 怎么把一个列表加到另一个后面
    - 为什么 append 之后变成了嵌套列表
  colloquial:
    - 想一次加好几个，不要一个个加
    - 加完发现套了一层，不是我想要的
  technical:
    - list.extend
    - list.append
    - 加号拼接
    - 嵌套列表
  short_queries:
    - 追加
    - extend
    - 扩展

status: tested
tested_versions: ["3.10", "3.11", "3.12", "3.13", "3.14"]
min_version: "3.0"
version_note: extend / append / 加号拼接各版本一致
sources:
  - Python 官方文档 list.extend
---

# 往列表里追加多个元素

## 功能描述

输入可迭代对象，把它里面的元素**逐个**接到列表末尾；原地修改，返回 None。

## 推荐代码

```python
a = [1, 2]
a.extend([3, 4])
print(a)          # [1, 2, 3, 4]

b = [1, 2]
b.append([3, 4])
print(b)          # [1, 2, [3, 4]]  ← 套了一层

c = [1, 2] + [3, 4]
print(c)          # [1, 2, 3, 4]，但是新列表，a 没变

a.extend("xy")
print(a)          # [1, 2, 3, 4, 'x', 'y']  ← 字符串会被逐个字符加进去
```

## 语句解释

### extend(可迭代对象)

把里面的元素一个个接上，是「摊平」的加法。

### append(对象)

只加**一个**对象，整体加进去。所以传列表进去会变成嵌套。

### 加号 `a + b`

返回**新列表**，原列表不变；`extend` 是原地改。

## 原理解释

**一句话：** `extend` 是「把这一批元素挨个塞进去」，`append` 是「把这一整个东西塞进去」。

**执行逻辑（extend）：**

1. 取要追加的可迭代对象
2. 从里面取出第一个元素
3. 把它放到列表末尾，长度加 1
4. 取下一个，重复 3
5. 取完为止，返回 None

**机器层（可跳过）：** 因为它可能提前知道元素个数，会先扩容再逐个放，比循环 `append` 少几次扩容。

**边界（从逻辑推出来）：**

- 第 2 步是「取出元素」，所以传字符串会被拆成单个字符加进去（字符串也是可迭代对象）
- 第 3 步逐个放，所以传嵌套列表只会摊平**一层**
- 因为它原地改并返回 None，`a = a.extend([...])` 会得到 None
- 加号 `+` 是新建列表，数据大时内存翻倍，但不会改到原列表

## 注意事项

- 想「加一个整体」用 `append`，想「加一批」用 `extend`。
- 传字符串会逐字符加进去，通常不是你想要的。
- `extend` 返回 None，别赋值接收。
- 加号拼接创建新列表；循环里大量拼接应改用 `extend` 或先收集再一次性拼。

## 使用场景

- 合并多批结果。
- 循环里累积数据（比反复 `+` 高效）。
- 把文件读出的多行接到一起。
