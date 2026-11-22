---
id: py.exceptions.raise
title: 主动抛出异常
description: 发现问题时自己报错，别让坏数据继续往后走
language: python
category_id: programming.basics
module: builtins
origin: builtin
import: ""
qualname: "raise"

object:
  id: error.condition
  name: 异常
  aliases: [异常, 错误, 报错, 异常对象, exception, error]

action:
  id: create.new
  name: 创建
  aliases: [抛出, 抛异常, 主动报错, 中断, raise]

targets: []

utterances:
  direct:
    - 主动抛出异常
    - 自己报错
    - 抛出自定义异常
  questions:
    - 怎么主动抛异常
    - 自定义异常类怎么写
    - raise 和 return 报错有什么区别
  colloquial:
    - 参数不合法就直接报错算了
    - 别让它跑下去，丑话说在前面
  technical:
    - raise
    - raise ValueError
    - 自定义异常
    - raise ... from
  short_queries:
    - 抛出
    - raise
    - 自定义异常

status: tested
tested_versions: ["3.10", "3.11", "3.12", "3.13", "3.14"]
min_version: "3.0"
version_note: raise / raise ... from 语法各版本一致
sources:
  - Python 官方教程 raise 语句
---

# 主动抛出异常

## 功能描述

输入一个异常对象，输出「立刻中断当前函数」；调用方要么接住，要么继续往上抛。

## 推荐代码

```python
class ConfigError(ValueError):
    """配置不合法时抛这个。"""

def load(port: int) -> int:
    if not (0 < port < 65536):
        raise ConfigError(f"端口不合法: {port}")
    return port

print(load(8000))

try:
    load(70000)
except ConfigError as exc:
    print("接住了:", exc)
```

## 语句解释

### raise 异常对象

立刻中断，把异常往调用方抛。

### class ConfigError(ValueError)

自定义异常继承内置的 `ValueError`，这样「接 ValueError 的地方」也能接住它。

### raise ... from 原异常

在 `except` 里再抛时用它保留原始原因：`raise ConfigError("配置错") from exc`。

## 原理解释

**一句话：** 它当场喊停，把「出了什么事」打包好，交给上层决定怎么处理。

**执行逻辑：**

1. 造一个异常对象（带上说明信息）
2. 立刻终止当前函数的执行，后面的代码一句都不跑
3. 沿着调用栈往上找能接住这个类型的 `except`
4. 找到 → 从那一段继续；找不到 → 一直冒到最外层，程序打印堆栈后退出

**机器层（可跳过）：** 抛异常会展开栈帧，比正常 `return` 慢，但它只发生在错误路径上。

**边界（从逻辑推出来）：**

- 第 2 步「后面的代码不跑」，所以 `raise` 之后的清理代码必须放到 `finally` 里
- 第 3 步按类型匹配，所以自定义异常继承哪个基类，决定了哪些 `except` 能接住它
- 第 4 步「没接住就退出」说明异常不是错误信息，是控制流
- 用 `raise` 还是 `return None` 表示失败：前者强制调用方处理，后者容易被忽略

## 注意事项

- `raise` 后面别再写代码，那是死代码（除非在 `try` 里被 `finally` 需要）。
- 自定义异常别继承 `BaseException`，继承 `Exception` 或其子类。
- 在 `except` 里重新抛要保留原因：`raise X from exc`，否则原始堆栈就丢了。
- 报错信息要写清**具体值**（`端口不合法: 70000`），不要只写「参数错误」。

## 使用场景

- 校验入参，不合法就当场拒绝。
- 库函数里明确「这个错误该由调用方处理」。
- 把底层异常翻译成自己领域的错误类型。
