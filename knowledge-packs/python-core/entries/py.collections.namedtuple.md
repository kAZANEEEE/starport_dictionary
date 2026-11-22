---
id: py.collections.namedtuple
title: 具名元组
description: 带字段名的轻量结构，比字典省、比普通元组好读
language: python
category_id: programming.basics
module: collections
origin: stdlib
import: "from collections import namedtuple"
qualname: "collections.namedtuple"

object:
  id: type.annotation
  name: 类型标注
  aliases: [结构体, 数据对象, 具名元组, 字段, namedtuple]

action:
  id: create.new
  name: 创建
  aliases: [定义, 创建, 声明, 生成, define]

targets: []

utterances:
  direct:
    - 定义具名元组
    - 用 namedtuple 建结构
    - 带字段名的元组
  questions:
    - namedtuple 和 dataclass 有什么区别
    - 怎么用字段名访问元组
    - namedtuple 能改吗
  colloquial:
    - 想用一个类装几个字段，又不想写一堆代码
    - 元组取值的下标记不住
  technical:
    - collections.namedtuple
    - _asdict
    - _replace
    - 不可变结构
  short_queries:
    - namedtuple
    - 具名元组
    - 结构体

status: tested
tested_versions: ["3.10", "3.11", "3.12", "3.13", "3.14"]
min_version: "3.0"
version_note: "namedtuple 从 2.6 起；3.6 起支持 defaults 参数"
sources:
  - Python 官方文档 collections.namedtuple
---

# 具名元组

## 功能描述

输入「类型名 + 字段名列表」，输出一个类：实例既能按下标取，也能按字段名取；**不可变**。

## 推荐代码

```python
from collections import namedtuple

Point = namedtuple("Point", "x y")
p = Point(3, 4)

print(p.x, p[0])       # 3 3
print(p)               # Point(x=3, y=4)
print(p._asdict())     # {'x': 3, 'y': 4}

q = p._replace(x=10)   # 返回新的，原对象不变
print(p, q)            # Point(x=3, y=4) Point(x=10, y=4)
```

## 语句解释

### namedtuple("Point", "x y")

第一个参数是类型名，第二个是字段名（空格或逗号分隔，也能传列表）。

### p.x / p[0]

两种访问方式都行，所以既能自解释、又能像普通元组那样解包。

### _replace(...)

因为不可变，改字段得生成新对象。方法名带下划线是刻意的，避免和字段名冲突。

## 原理解释

**一句话：** 它生成一个「元组的子类」，给每个位置绑定一个名字，别的行为和元组一样。

**执行逻辑：**

1. 定义时按字段名列表生成一个类，内部记录「字段名 → 下标」的映射
2. 创建实例时，按位置把值存进元组的槽位（和普通元组一样）
3. 访问 `p.x` 时，把名字换成下标，再去元组里取
4. `_replace` 复制所有槽位、换掉指定那个，生成新实例

**机器层（可跳过）：** 实例就是一个元组，字段名是类级别的映射，不占每个实例的内存。

**边界（从逻辑推出来）：**

- 第 2 步按位置存，所以**字段顺序必须和定义一致**，不能按名字传（3.6+ 可用 `_make` 或 defaults）
- 第 3 步只是名字换下标，所以它仍然是元组：能解包、能比较、能当字典键
- 第 4 步生成新实例，所以「改字段」不会影响原对象（不可变）
- 字段名不能是 Python 关键字或以下划线开头（那会和内部方法冲突）

## 注意事项

- 不可变，改字段用 `_replace`，不是赋值。
- 字段太多（>6）时 dataclass 更好读，namedtuple 适合两三个字段的小结构。
- 需要方法/校验时用 dataclass，namedtuple 只能装数据。
- `_asdict()` 返回的是普通 dict，可以直接转 JSON。

## 使用场景

- 表示坐标、尺寸、起止范围这类小结构。
- 从数据库行/CSV 行转成带名字的对象。
- 函数返回多个值时，用一个具名元组代替裸元组。
