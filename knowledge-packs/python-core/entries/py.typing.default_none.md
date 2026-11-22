---
id: py.typing.default_none
title: 参数默认写 None 的套路
description: 可变默认值的坑，以及 Optional 该怎么写
language: python
category_id: programming.basics
module: typing
origin: stdlib
import: "from typing import Optional"
qualname: "X | None / typing.Optional"
signature: "def 函数(参数: 类型 | None = None)"
args:
  - name: "参数"
    required: false
    default: "None"
    accepts: "默认值写 None，函数里再 if x is None: x = []"
    nesting: "可以，但别把 [] 直接当默认值（会所有调用共享）"
returns: "无返回值：这是写法约定；判断「传没传」要用 is None，不是 not x"

object:
  id: type.annotation
  name: 类型标注
  aliases: [类型标注, 默认值, 可选参数, 类型提示, typing]

action:
  id: modify.change
  name: 修改
  aliases: [标注, 设置默认值, 声明可选, 改成可选, annotate]

targets: []

utterances:
  direct:
    - 参数默认值写 None
    - 可变默认值的坑
    - 可选参数怎么标注
  questions:
    - 为什么不能用空列表当默认参数
    - Optional 怎么写
    - 参数默认 None 之后怎么处理
  colloquial:
    - 函数默认参数是空列表，结果所有调用共享了
    - 想表示这个参数可以不传
  technical:
    - 可变默认参数
    - Optional
    - "None 哨兵"
    - "x: int | None = None"
  short_queries:
    - 默认参数
    - Optional
    - None

status: tested
tested_versions: ["3.10", "3.11", "3.12", "3.13", "3.14"]
min_version: "3.10"
version_note: "X | None 写法从 3.10 起；老版本用 typing.Optional[X]"
sources:
  - Python 官方教程 默认参数值
  - Python 官方文档 typing.Optional
---

# 参数默认写 None 的套路

## 功能描述

输入「参数名 + 类型 + 默认 None」，输出一个可选参数；函数体里再用 `if x is None` 换成真正的默认值。

## 推荐代码

```python
def collect(items=None, name: str | None = None) -> list:
    if items is None:
        items = []          # 每次调用都新建，互不影响
    items.append(1)
    return items

print(collect(), collect())     # [1] [1]  ← 互不影响

def bad(items=[]):              # 反例：所有调用共享同一个列表
    items.append(1)
    return items

print(bad(), bad())             # [1, 1]  ← 越来越长
```

## 语句解释

### `items: list | None = None`

类型说明「可能是列表，也可能是 None」，默认给 None。

### `if items is None: items = []`

在函数**内部**造默认值，所以每次调用都是新的。

### `if x is None` 而不是 `if not x`

空列表、0、空字符串都为假，用 `not x` 会把「显式传了空列表」也当成没传。

## 原理解释

**一句话：** 默认值只在**定义函数时**算一次，之后每次调用都复用同一个对象。

**执行逻辑：**

1. 定义函数时，Python 求值所有默认参数，把结果存进函数对象里
2. 每次调用，没传的参数就用存着的那个对象
3. 所以可变对象（列表、字典）被所有调用**共享**
4. 而 `None` 是不可变的，共享也无害——于是有了「默认 None，函数内再造」的套路

**机器层（可跳过）：** 默认值存放在 `函数.__defaults__` 里，可以打印出来看。

**边界（从逻辑推出来）：**

- 第 3 步共享是「可变默认参数」所有怪象的总根：`bad()` 越调越长
- 第 4 步说明 `None` 是安全的哨兵，因为它不可变
- 因为第 1 步只求值一次，`def f(x=now())` 里的 `now()` 也只在定义时执行一次
- 判断「传没传」要用 `is None`，因为空列表会被 `not` 判成假

## 注意事项

- 默认值别写 `[]`、`{}`、`set()`，写 `None` 再在函数里建。
- 判空用 `is None`，别用 `not x`（会把空容器也当没传）。
- `def f(x: int = None)` 类型是错的，要写 `int | None`。
- 想看默认值到底存了什么，`print(func.__defaults__)`。

## 使用场景

- 可选列表/字典参数。
- 需要区分「没传」和「传了空值」的场景。
- 想给默认值做一次性的重计算（每次调用都要新的）。
