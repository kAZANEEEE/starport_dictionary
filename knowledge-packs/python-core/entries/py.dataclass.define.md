---
id: py.dataclass.define
title: 用 dataclass 定义数据结构
description: 少写样板代码的数据类，自动生成初始化、打印、比较
language: python
category_id: programming.basics
module: dataclasses
origin: stdlib
import: "from dataclasses import dataclass, field"
qualname: "dataclasses.dataclass"

object:
  id: type.annotation
  name: 类型标注
  aliases: [数据类, 类, 结构体, 数据对象, dataclass]

action:
  id: create.new
  name: 创建
  aliases: [定义, 创建, 声明, 生成, define]

targets: []

utterances:
  direct:
    - 用 dataclass 定义类
    - 定义数据类
    - 写一个只装数据的类
  questions:
    - dataclass 怎么用
    - 为什么用它比手写 __init__ 好
    - 字段默认值和可变默认值的坑
  colloquial:
    - 一堆字段的类，手写 init 太累了
    - 只想装数据，不想要一堆样板
  technical:
    - "@dataclass 装饰器"
    - "field(default_factory=)"
    - "frozen=True"
    - "dataclasses.asdict"
  short_queries:
    - dataclass
    - 数据类
    - 定义类

status: tested
tested_versions: ["3.10", "3.11", "3.12", "3.13", "3.14"]
min_version: "3.7"
version_note: "dataclass 装饰器从 3.7 起；frozen / slots 参数在 3.10 起可用"
sources:
  - Python 官方文档 dataclasses
---

# 用 dataclass 定义数据结构

## 功能描述

输入「字段名 + 类型（+ 默认值）」，输出一个类：自动生成 `__init__`、`__repr__`、`__eq__`。

## 推荐代码

```python
from dataclasses import dataclass, field

@dataclass
class Entry:
    id: str
    title: str
    tags: list[str] = field(default_factory=list)

e = Entry("py.x", "示例")
print(e)                      # Entry(id='py.x', title='示例', tags=[])
print(e == Entry("py.x", "示例"))   # True
e.tags.append("a")
print(e.tags)                 # ['a']
```

## 语句解释

### @dataclass

装饰器，按类里写的字段声明生成方法。

### 字段写法和普通类属性一样

`id: str` 表示这个字段叫 id、类型是 str，**必须传**。

### field(default_factory=list)

可变默认值（列表/字典）要用 `default_factory`，直接写 `= []` 会报错。

## 原理解释

**一句话：** 它读一遍你写的字段清单，替你把这些样板方法生成出来。

**执行逻辑：**

1. 装饰器扫描类体里的「带类型标注的属性」，记下字段名、类型、默认值
2. 按顺序生成 `__init__(self, id, title, tags=...)`，里面逐个赋值
3. 生成 `__repr__`，把字段名和值拼成可读字符串
4. 生成 `__eq__`，逐个字段比较
5. 生成完把类还给你，之后 `Entry(...)` 就是在走第 2 步的初始化

**机器层（可跳过）：** 生成发生在「定义类」那一刻，运行时没有额外开销。

**边界（从逻辑推出来）：**

- 第 1 步只认带类型标注的字段，所以漏写 `: str` 的不会成为参数
- 第 2 步按声明顺序给参数，所以**有默认值的字段必须写在后面**
- 第 3 步的 `__repr__` 依赖第 1 步的字段清单，加字段自动出现在打印里
- 可变默认值必须用 `default_factory`：否则所有实例共享同一个列表（Python 的默认值只求值一次）
- 想不可变用 `frozen=True`，之后赋值会抛异常

## 注意事项

- 有默认值的字段要排在没默认值的后面，否则定义时就报错。
- 列表/字典默认值必须 `field(default_factory=list)`。
- `frozen=True` 之后不能改字段，也不能再当「可变状态」用。
- 需要 JSON 序列化用 `dataclasses.asdict(e)`。

## 使用场景

- 表示解析出来的数据（配置项、抓取结果、API 响应）。
- 替代「一堆字段的字典」，让编辑器能补全和检查。
- 作为函数的返回值，比 tuple 可读。
