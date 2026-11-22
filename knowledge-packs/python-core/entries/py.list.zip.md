---
id: py.list.zip
title: 同时遍历两个列表
description: 按下标把两个列表成对取出来
language: python
category_id: programming.basics
module: builtins
origin: builtin
import: ""
qualname: "zip"
signature: "zip(a, b, ..., strict=False)"
args:
  - name: "a, b, ..."
    required: true
    accepts: "两个或多个可迭代对象"
    nesting: "可以，可以是生成器、字典的键"
  - name: "strict"
    required: false
    default: "False"
    accepts: "True = 长度不一致直接报错；False = 按最短的截断"
    nesting: "一般直接写 True/False"
returns: "迭代器：每次给一组配对的元素；长度不同默认静默截断"

object:
  id: list.element
  name: 列表元素
  aliases: [列表, 元素, 两个列表, 成对, items]

action:
  id: traverse.walk
  name: 遍历
  aliases: [同时遍历, 配对, 并行循环, 一起遍历, zip]

targets: []

utterances:
  direct:
    - 同时遍历两个列表
    - 把两个列表配对
    - 并行循环两个列表
  questions:
    - 怎么同时遍历两个列表
    - 如何把两个列表组成字典
    - zip 长度不一样会怎样
  colloquial:
    - 一个名字列表一个年龄列表，想配对处理
    - 想两个一起循环，不想用下标
  technical:
    - zip
    - zip 转 dict
    - zip_longest
    - 长度不同截断
  short_queries:
    - 配对
    - zip
    - 同时遍历

status: tested
tested_versions: ["3.10", "3.11", "3.12", "3.13", "3.14"]
min_version: "3.0"
version_note: zip 各版本一致；zip 的 strict 参数是 3.10 新增
sources:
  - Python 官方文档 zip
---

# 同时遍历两个列表

## 功能描述

输入两个（或多个）可迭代对象，输出「(第一个的第 i 个, 第二个的第 i 个)」这样的元组；**长度不同时按最短的截断**。

## 推荐代码

```python
names = ["张三", "李四", "王五"]
ages = [28, 31]

for name, age in zip(names, ages):
    print(name, age)      # 只输出两组，第三个人被截掉

print(dict(zip(names, ages)))     # 顺便组成字典

# 不想截断：短的补 None
from itertools import zip_longest
print(list(zip_longest(names, ages, fillvalue="未知")))
```

## 语句解释

### zip(a, b)

每次从两个里各取一个，配成元组。取完就停。

### dict(zip(键列表, 值列表))

最常用的组合：两个等长列表直接变字典。

### zip_longest(..., fillvalue=)

短的用 `fillvalue` 补齐，不丢数据。

## 原理解释

**一句话：** 它每个元素都从几个来源各拿一个，凑成一对交给你，谁先取完就收工。

**执行逻辑：**

1. 从第一个列表取一个，从第二个取一个，组成元组
2. 交给循环体处理
3. 再各取下一个，重复
4. 只要**任何一个**来源取完了 → 立刻停止（多余的元素被丢弃）

**机器层（可跳过）：** 惰性迭代器，取一对算一对，不预先造列表。

**边界（从逻辑推出来）：**

- 第 4 步「谁先完就停」是**静默截断**，不会报错——这是最常见的丢数据原因
- 3.10 起可以写 `zip(a, b, strict=True)`，长度不一致时直接抛错，适合「本该等长」的场景
- 因为第 1 步各取一个，所以两个列表不需要有下标（生成器、文件对象也能配）
- `zip` 返回迭代器，用一次就空，想再用得 `list(zip(...))`

## 注意事项

- 长度不一致会**静默丢数据**，要么自己 `len` 校验，要么 `strict=True`。
- `zip` 是迭代器，`print(zip(...))` 看不到内容，要 `list()`。
- 三个以上列表也能配，但可读性会下降，考虑用字典或具名元组。
- 想要「笛卡尔积」不是 `zip`，那是 `itertools.product`。

## 使用场景

- 姓名和年龄/成绩配对处理。
- 两个等长列表拼成字典。
- 批量对比两组数据的对应项。
