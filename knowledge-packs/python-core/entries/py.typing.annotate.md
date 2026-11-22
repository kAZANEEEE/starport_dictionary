---
id: py.typing.annotate
title: 类型标注
description: 给函数和变量写上类型，方便人看和工具检查
language: python
category_id: programming.basics
module: typing
origin: stdlib
import: "from typing import Optional"
qualname: "typing 类型标注"

object:
  id: type.annotation
  name: 类型标注
  aliases: [类型标注, 类型提示, 注解, 类型说明, typing]

action:
  id: modify.change
  name: 修改
  aliases: [标注, 声明类型, 加上类型, 注明, annotate]

targets: []

utterances:
  direct:
    - 给函数加类型标注
    - 声明变量类型
    - 写类型提示
  questions:
    - 怎么给函数参数标类型
    - 类型标注会影响性能吗
    - 返回值类型怎么写
    - Optional 是什么意思
  colloquial:
    - 想让人一眼看出参数是什么类型
    - 编辑器老提示类型，怎么标清楚
  technical:
    - type hints
    - Optional
    - Union
    - list[int]
    - -> 返回值
  short_queries:
    - 类型标注
    - type hints
    - 注解

status: tested
tested_versions: ["3.10", "3.11", "3.12", "3.13", "3.14"]
min_version: "3.9"
version_note: 3.9 起可用 list[int] 这种内置泛型；3.10 起可用 X | None，不必写 Optional
sources:
  - Python 官方文档 类型提示
---

# 类型标注

## 功能描述

输入函数/变量的声明，输出带类型说明的代码；**运行时不做检查**，只是给人和工具看的说明。

## 推荐代码

```python
def total(prices: list[float], discount: float = 0.0) -> float:
    return sum(prices) * (1 - discount)

def find(name: str) -> str | None:
    return None if name != "a" else "找到了"

print(total([10.0, 20.0], 0.5))
print(find("a"), find("b"))
```

## 语句解释

### prices: list[float]

参数名后面的冒号写类型。3.9+ 可以直接写 `list[float]`。

### -> float

箭头后面是返回值类型。

### str | None

表示「可能是字符串，也可能是 None」。3.10+ 的写法，老版本写 `Optional[str]`。

### 默认值放最后

有默认值的参数必须写在没默认值的后面。

## 原理解释

**一句话：** 标注只是**记在函数身上的说明文字**，Python 执行时不会因此检查或转换类型。

**执行逻辑：**

1. 定义函数时，Python 把标注存进 `函数.__annotations__` 这个字典
2. 真调用时，它按普通方式绑定参数——**完全不看标注**
3. 传错类型照样能跑，直到那行代码真的用错才报错
4. 编辑器/类型检查器（mypy）在**写代码阶段**读第 1 步那份记录，提前报警

**机器层（可跳过）：** 标注求值发生在定义时，对调用没有运行开销。

**边界（从逻辑推出来）：**

- 第 2 步说明标注**不是运行时约束**：传 `"abc"` 给 `list[float]` 参数不会当场报错
- 第 1 步存的是对象，所以写了复杂表达式会在定义时求值——想延后得用字符串写法
- 第 4 步的价值全在工具链：没有 mypy/编辑器，标注就是纯文档
- `str | None` 里的 `None` 是类型不是值，别写成 `"None"`

## 注意事项

- 标注不改变运行时行为，别指望它替你校验入参。
- 真正想校验用 `isinstance` 或 `pydantic`。
- `def f(x: int = None)` 是类型错的（None 不是 int），要写 `int | None`。
- 泛型容器写 `list[int]` 而不是 `list`，`dict[str, int]` 两个参数都要给。

## 使用场景

- 给公共函数写清入参和返回类型。
- 让编辑器给出更准的补全和报错。
- 多人协作时当契约用。
