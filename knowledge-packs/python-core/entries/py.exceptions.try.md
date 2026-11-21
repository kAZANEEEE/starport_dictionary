---
id: py.exceptions.try
title: 捕获异常
description: 出错时不让程序崩，接住并处理
language: python
category_id: programming.basics
module: builtins

object:
  id: error.condition
  name: 异常
  aliases: [异常, 错误, 报错, 出错, exception, error]

action:
  id: inspect.check
  name: 判断
  aliases: [捕获, 接住, 处理, 忽略, 捕获异常, try]

targets: []

utterances:
  direct:
    - 捕获异常
    - 处理错误
    - 让程序别崩
  questions:
    - 怎么捕获异常
    - 如何忽略某个错误继续跑
    - try except 怎么写才不吞掉错误
  colloquial:
    - 这条报错了，想接住它别中断
    - 某个文件可能不在，别让它崩
  technical:
    - try except
    - except Exception
    - finally
    - raise 重新抛出
  short_queries:
    - try
    - except
    - 异常

status: tested
tested_versions: ["3.10", "3.11", "3.12", "3.13", "3.14"]
min_version: "3.0"
version_note: try/except/else/finally 语法各版本一致
sources:
  - Python 官方教程 错误与异常
---

# 捕获异常

## 功能描述

输入一段可能出错的代码 + 一个异常类型，出错时接住并执行处理分支；类型不匹配就照常抛出。

## 推荐代码

```python
try:
    value = int("abc")
except ValueError as exc:
    print("转换失败:", exc)
    value = 0
else:
    print("没出错才走这里")
finally:
    print("不管出不出错都走这里")

print("继续往下跑:", value)
```

## 语句解释

### try / except 类型 as 变量

`try` 里的代码出错时，异常会沿着类型匹配——匹配上就走 `except` 分支。

### else

`try` 里**没出错**时才执行。

### finally

**无论如何都执行**，用来释放资源。

### raise

在 `except` 里写 `raise` 表示「处理完再抛出去」，不吞掉错误。

## 原理解释

**一句话：** 出错的瞬间，Python 沿着调用栈往上找，找第一个「能接住这个类型」的 except，找到就跳过去继续跑。

**执行逻辑：**

1. `try` 里逐句执行
2. 某句抛异常 → 立刻跳出 `try`，跳过剩下的语句
3. 从上到下检查每个 `except` 的类型：是它的子类或本身 → 进去执行
4. `except` 执行完，程序从整个 `try` 语句之后继续
5. 一个都没匹配上 → 异常继续往上抛；到最外层还没人接，程序带堆栈退出

**机器层（可跳过）：** 抛异常会展开栈帧，比正常返回慢，但比崩溃可控。

**边界（从逻辑推出来）：**

- 第 2 步「跳过剩下的语句」意味着 `try` 块里出错点之后的代码不会执行
- 第 3 步按类型匹配、而且是**从上到下**，所以具体类型要写在宽泛类型前面
- 第 5 步说明不写 `except` 的异常会冒到最外层——不是消失
- `except Exception:` 会接住几乎所有错误（包括你自己的 bug），这是「错误被吞掉」的根源

## 注意事项

- 别裸写 `except:`，会让 Ctrl+C 都抓不住；至少写 `except Exception`。
- 捕获后要么处理，要么 `raise` 抛出去，别默默 pass。
- 只捕获你**知道怎么处理**的异常类型，其他让它们暴露。
- `finally` 里别写 `return`，会把异常和返回值一起吞掉。

## 使用场景

- 读可能不存在的文件。
- 解析用户输入（数字、JSON）。
- 网络请求这种外部依赖，失败要能继续。
