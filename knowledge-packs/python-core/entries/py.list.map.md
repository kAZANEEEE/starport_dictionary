---
id: py.list.map
title: 批量转换列表元素
description: 对每个元素做同一个操作，得到新列表
language: python
category_id: programming.basics
module: list
origin: builtin
import: ""
qualname: "map() / 列表推导式"
signature: "[对每个元素做什么 for x in items]；map(函数, items)"
args:
  - name: "函数 / 表达式"
    required: true
    accepts: "对单个元素做的转换：str、int、lambda 或任意表达式"
    nesting: "可以，map 可传 lambda，推导式可写任意表达式"
returns: "列表（推导式）或迭代器（map）：元素个数和原来一样"

object:
  id: list.element
  name: 列表元素
  aliases: [列表, 元素, 每个元素, items]

action:
  id: convert.transform
  name: 转换
  aliases: [转换, 映射, 批量处理, 逐个处理, map]

targets: []

utterances:
  direct:
    - 批量转换列表元素
    - 列表里每个元素都转成字符串
    - 对列表每个元素做处理
  questions:
    - 怎么把列表里所有元素转成字符串
    - 如何对列表每个元素调用同一个函数
    - Python 怎么批量处理列表
  colloquial:
    - 这一列数字想全部变成字符串
    - 每个元素都要加 1
  technical:
    - map 函数
    - 列表推导式映射
    - lambda 配合 map
  short_queries:
    - 映射
    - map

status: tested
tested_versions: ["3.10", "3.11", "3.12", "3.13", "3.14"]
min_version: "3.0"
version_note: map 返回迭代器；列表推导式各版本一致
sources:
  - Python 官方文档 map
---

# 批量转换列表元素

## 功能描述

输入列表 + 一个转换操作，输出**每个元素都被转换过的新列表**，元素个数不变。

## 推荐代码

```python
nums = [1, 2, 3]

strs = [str(n) for n in nums]
print(strs)                        # ['1', '2', '3']

plus_one = list(map(lambda n: n + 1, nums))
print(plus_one)                    # [2, 3, 4]

raw = [" 10 ", "20 "]
print([int(x) for x in raw])       # [10, 20]  int 会自动处理首尾空白
```

## 语句解释

### [str(n) for n in nums]

列表推导式，最常用。左边是“对每个元素做什么”。

### map(函数, 可迭代)

把函数逐个应用到元素上，返回**迭代器**，要 `list()` 才是列表。

### 两者的区别

`map` 只是“应用函数”；推导式还能顺便筛选（加 `if`），也能做更复杂表达式。

## 原理解释

**一句话：** 挨个把元素丢进同一个函数，把每次的返回值收集起来。

**执行逻辑：**

1. 准备一个空的结果列表（推导式）或一个惰性迭代器（`map`）
2. 取一个元素，交给转换函数
3. 拿到返回值，放进结果
4. 重复 2–3 直到取完
5. 交给你结果；元素个数和原来一样

**机器层（可跳过）：** 一趟遍历 + 每元素一次函数调用，O(n)。

**边界（从逻辑推出来）：**

- 第 5 步「个数不变」是它的定义——要减少个数得换成筛选
- `map` 是惰性的：不消费就算一次都没调用，所以调试时打印看不到结果
- 每元素都要调一次函数，函数本身写得很重时会明显变慢，简单运算用推导式内联更快
- 转换函数抛异常会中断整个流程，批量处理时最好在函数里自己兜住
## 注意事项

- `map` 返回迭代器，`print` 出来是 `<map object at 0x...>`。
- 迭代器只能消费一次。
- 需要同时处理两个列表用 `map(f, a, b)` 或 `zip`。
- 元素类型不一致时先统一，否则后面处理会各类报错。

## 使用场景

- 把字符串列表转成数字列表。
- 给一批文件名统一加前缀。
- 对抓取到的数据做统一清洗。
