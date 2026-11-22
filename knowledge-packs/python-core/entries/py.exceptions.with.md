---
id: py.exceptions.with
title: 用 with 自动收尾
description: 进块时拿资源，出块时自动还，别漏
language: python
category_id: programming.basics
module: builtins
origin: builtin
import: ""
qualname: "with ... as（上下文管理器）"
signature: "with 管理器 as 变量: ..."
args:
  - name: "管理器"
    required: true
    accepts: "实现 __enter__ / __exit__ 的对象，如 open(...)、锁"
    nesting: "可以，多个资源可用逗号并列"
  - name: "as 变量"
    required: false
    default: "无"
    accepts: "接住 __enter__ 的返回值（常用的是文件对象）"
    nesting: "一般直接写 f"
returns: "无返回值：语法结构。离开代码块时自动收尾，异常照常往外抛"

object:
  id: error.condition
  name: 异常
  aliases: [资源, 清理, 上下文, 收尾, with]

action:
  id: run.execute
  name: 执行
  aliases: [自动关闭, 自动释放, 收尾, 托管, with]

targets: []

utterances:
  direct:
    - 用 with 自动关闭文件
    - 上下文管理器怎么用
    - 自动释放资源
  questions:
    - with 为什么能自动关闭
    - 自己能写上下文管理器吗
    - with 里出异常会关闭吗
  colloquial:
    - 老忘记 close，有没有自动的
    - 想自己造一个能 with 的东西
  technical:
    - with 语句
    - __enter__ __exit__
    - contextlib.contextmanager
  short_queries:
    - with
    - 上下文管理器
    - 自动关闭

status: tested
tested_versions: ["3.10", "3.11", "3.12", "3.13", "3.14"]
min_version: "3.0"
version_note: "with 从 2.5 起；3.10 起括号写法支持多行"
sources:
  - Python 官方文档 with 语句
  - Python 官方文档 contextlib.contextmanager
---

# 用 with 自动收尾

## 功能描述

输入一个「上下文管理器」，输出它的资源对象，并在离开代码块时**自动执行收尾**（即使抛异常）。

## 推荐代码

```python
from pathlib import Path

Path("demo.txt").write_text("一行\n", encoding="utf-8")

with open("demo.txt", encoding="utf-8") as f:
    print(f.readline().strip())      # 出块后 f 自动关闭

# 自己写一个：进出都要打印
class Step:
    def __init__(self, name): self.name = name
    def __enter__(self):
        print("进入", self.name); return self
    def __exit__(self, *exc):
        print("离开", self.name); return False   # False = 不吞异常

with Step("a"):
    print("干活")
```

## 语句解释

### with 表达式 as 变量

进入时调用 `__enter__`（返回值给 `as` 变量），离开时调用 `__exit__`。

### `__exit__` 返回 False

表示「异常不吞掉」，让它继续往上抛；返回 True 才会把异常压掉。

### `__exit__` 的三个参数

`exc_type, exc_value, traceback`——没异常时都是 None。

## 原理解释

**一句话：** 它把「拿资源」和「还资源」绑成一件事：进块调一次，出块无论怎么出都调一次。

**执行逻辑：**

1. 求值 `with` 后面的表达式，拿到上下文管理器
2. 调用它的 `__enter__()`，返回值绑给 `as` 变量
3. 执行 `with` 块里的代码
4. 无论正常结束、`return` 还是抛异常，都调用 `__exit__(...)`
5. `__exit__` 返回 False（或 None）→ 异常继续抛；返回 True → 异常被吞

**机器层（可跳过）：** 纯语法层展开，不是库功能，也没有额外开销。

**边界（从逻辑推出来）：**

- 第 4 步「无论怎么出都调用」就是它比手写 try/finally 更可靠的原因
- 第 5 步决定异常去向，所以写 `__exit__` 时**默认要返回 False**，别无意中吞掉错误
- 因为第 2 步能返回值，`as` 拿到的不一定是管理器本身（文件对象就是这样）
- `__exit__` 自己也抛异常时，会覆盖原异常

## 注意事项

- 别在 `__exit__` 里 `return True`，除非你明确要吞异常。
- 需要一堆资源时，`with` 可以用逗号并列，或嵌套。
- 只是包个函数体做前后处理，用 `contextlib.contextmanager` 装饰生成器更省事。
- `with` 结束不代表「没出错」，异常可能还在往上走。

## 使用场景

- 文件、数据库连接、锁、网络会话。
- 临时切换工作目录、环境变量。
- 计时块（进入记时间、离开打印耗时）。
