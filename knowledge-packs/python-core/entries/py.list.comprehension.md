---
id: py.list.comprehension
title: 用推导式生成列表
description: 一行写清「对每个元素做什么」，还能带条件
language: python
category_id: programming.basics
module: list

object:
  id: list.element
  name: 列表元素
  aliases: [列表, 元素, 新列表, 数据, items]

action:
  id: convert.transform
  name: 转换
  aliases: [推导式, 生成列表, 一行生成, 转成列表, comprehension]

targets: []

utterances:
  direct:
    - 用推导式生成列表
    - 一行生成列表
    - 列表推导式怎么写
  questions:
    - 怎么用一行代码生成列表
    - 推导式和 for 循环有什么区别
    - 怎么在推导式里加条件
  colloquial:
    - 想少写几行 for 循环
    - 这个 for 循环能不能写短一点
  technical:
    - 列表推导式
    - list comprehension
    - 生成器表达式
    - 嵌套推导式
  short_queries:
    - 推导式
    - comprehension

status: tested
tested_versions: ["3.10", "3.11", "3.12", "3.13", "3.14"]
min_version: "3.0"
version_note: 推导式语法各版本一致；海象运算符 := 需 3.8+
sources:
  - Python 官方教程 列表推导式
---

# 用推导式生成列表

## 功能描述

输入“表达式 + 遍历 + 可选条件”，输出一个新列表，等价于 `for` 循环 + `append`。

## 推荐代码

```python
nums = [1, 2, 3, 4]

print([n * 2 for n in nums])                  # [2, 4, 6, 8]
print([n for n in nums if n % 2 == 0])        # [2, 4]
print([[n, n * n] for n in nums])             # 嵌套结构

# 嵌套推导式：展平二维列表
matrix = [[1, 2], [3, 4]]
print([x for row in matrix for x in row])     # [1, 2, 3, 4]
```

## 语句解释

### [表达式 for 变量 in 可迭代对象]

左边是“对每个元素做什么”，右边是“从哪儿来”。

### 后面加 if

只保留满足条件的元素，等价于循环里的 `continue`。

### 两个 for 连写

从左往右读：先外层后内层，所以能展平二维列表。

## 原理解释

**一句话：** 它一边造列表一边往里塞，比 `for` 循环少做两件事。

**执行逻辑：**

1. 先造一个空列表（你看不见，但它已经在那儿了）
2. 从来源里取出第一个元素
3. 对它求值，比如算出 `i * 2`
4. 把结果塞进那个列表的末尾
5. 回到第 2 步，直到来源取完
6. 把整个列表交给你

**和 `for` 差在哪：** `for` 在「求值」和「塞进去」之间要多做两步——先找 `append` 在哪、再调用它。推导式把这两步合成固定动作。省的是「元素个数 × 两次小动作」，实测一百万个元素：103 毫秒 → 73 毫秒。

**机器层（可跳过）：** CPython 编成一条专用指令直接追加，不经过函数调用。

**边界（从逻辑推出来）：**

- 第 1 步就建了列表且全程只有一个，所以**元素全部同时待在内存里**，长度=内存占用
- 数据大就改用生成器表达式（圆括号），它不建列表，边算边用
- 加的 `if` 是在第 2 步之后判断的：不合格的元素不进入第 3 步，所以结果个数可能变少
- 别在第 3 步里做副作用（写文件、打印），那会让逻辑难以推断
## 注意事项

- 太复杂就该拆成普通循环，超过两行的推导式不可读。
- 推导式会**立刻生成整个列表**；只需要迭代一次、数据又大，用生成器表达式 `(x for x in ...)`。
- 别在推导式里做副作用（写文件、打印），那是 for 循环的活。
- 嵌套超过两层就该考虑函数了。

## 使用场景

- 批量转换或筛选数据。
- 展平嵌套列表。
- 从字典列表里抽取某个字段。
