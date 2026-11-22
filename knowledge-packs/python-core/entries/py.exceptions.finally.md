---
id: py.exceptions.finally
title: 无论如何都要执行的清理
description: 出不出错都要关文件、断开连接
language: python
category_id: programming.basics
module: builtins
origin: builtin
import: ""
qualname: "try / finally"
signature: "try: ... finally: 收尾"
args: []
returns: "无返回值：finally 里的代码一定会执行（return/异常/正常结束都一样）"

object:
  id: error.condition
  name: 异常
  aliases: [异常, 错误, 清理, 收尾, exception]

action:
  id: run.execute
  name: 执行
  aliases: [确保执行, 一定执行, 收尾, 清理, finally]

targets: []

utterances:
  direct:
    - 无论是否出错都要执行
    - 用 finally 做清理
    - 保证资源被释放
  questions:
    - finally 什么时候执行
    - 怎么保证文件一定关闭
    - return 之后 finally 还执行吗
  colloquial:
    - 出错也要把连接关掉
    - 不想因为异常漏掉收尾
  technical:
    - finally
    - try finally
    - 资源释放
    - with 与 finally
  short_queries:
    - finally
    - 清理
    - 收尾

status: tested
tested_versions: ["3.10", "3.11", "3.12", "3.13", "3.14"]
min_version: "3.0"
version_note: try/finally 语义各版本一致
sources:
  - Python 官方教程 定义清理行为
---

# 无论如何都要执行的清理

## 功能描述

输入一段代码 + 一段收尾代码，输出「收尾代码一定会跑」；即使中间 `return`、抛异常也都跑。

## 推荐代码

```python
def read_first_line(path: str) -> str | None:
    f = open(path, encoding="utf-8")
    try:
        return f.readline().strip()
    finally:
        f.close()          # 无论上面 return 还是抛异常，都会关

print(read_first_line("probe.txt") if False else "跳过演示")

try:
    read_first_line("不存在的文件.txt")
except FileNotFoundError:
    print("文件不存在被接住了")
```

## 语句解释

### try / finally

`finally` 里的代码在离开 `try` 时**一定会执行**：正常结束、`return`、抛异常，都一样。

### 和 with 的关系

`with open(...)` 就是「try/finally + close」的封装，能用 `with` 就别手写。

### return 在 try 里

返回值会先被记住，然后执行 `finally`，最后才真的返回。

## 原理解释

**一句话：** 它给这段代码挂了个「出门必做」，不管从哪个门出去，都要先做一遍。

**执行逻辑：**

1. 进入 `try`，执行里面的代码
2. 遇到 `return` / 异常 / 正常走完，都先**记住当前的结局**
3. 立刻跳到 `finally` 块执行
4. `finally` 跑完，再按第 2 步记住的结局继续：返回、或把异常往上抛

**机器层（可跳过）：** 由解释器在栈帧退出路径上统一处理，不依赖任何库。

**边界（从逻辑推出来）：**

- 第 2 步「记住结局」说明 `return` 的值在 `finally` 之前就定了；但如果在 `finally` 里再 `return`，会**覆盖**原结局
- 第 3 步无条件执行，所以清理代码放这里最靠谱——放 `try` 末尾会被异常跳过
- 第 4 步异常仍会继续往上抛，`finally` 不吞异常
- 进程被强杀（`kill -9`）不会走 `finally`，这不是它的保证范围

## 注意事项

- 别在 `finally` 里写 `return`，会吞掉异常和原返回值。
- 能 `with` 就 `with`，手写 `finally` 容易漏。
- `finally` 里也可能抛异常，会把原异常覆盖掉（可 `raise ... from` 保留）。
- 它保证「会执行」，不保证「执行成功」。

## 使用场景

- 关闭文件、断开数据库/网络连接。
- 释放锁。
- 记录「任务结束」日志（无论成败）。
