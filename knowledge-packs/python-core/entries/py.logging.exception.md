---
id: py.logging.exception
title: 记录异常堆栈到日志
description: 出错时把完整报错写进日志，而不是只写一句
language: python
category_id: programming.basics
module: logging
origin: stdlib
import: "import logging"
qualname: "logging.exception()"
signature: "logging.exception(消息)"
args:
  - name: "消息"
    required: true
    accepts: "一句说明，堆栈会自动附在后面"
    nesting: "可以，但建议用 logging.exception(\"x=%s\", x) 的惰性写法"
returns: "None：写一条 ERROR 日志并带上当前异常的堆栈；只在 except 块里有效"

object:
  id: log.record
  name: 日志
  aliases: [日志, 报错记录, 堆栈, 错误信息, log]

action:
  id: create.new
  name: 创建
  aliases: [记录, 输出, 写入, 打日志, log]

targets: []

utterances:
  direct:
    - 把异常记录到日志
    - 日志里打印堆栈
    - except 里怎么打日志
  questions:
    - 怎么在日志里输出 traceback
    - logging.exception 和 error 有什么区别
    - 出错日志缺堆栈怎么办
  colloquial:
    - 线上出错了只看到一句话，找不到哪行
    - 想把完整报错留在日志里
  technical:
    - logging.exception
    - exc_info
    - traceback
    - 只在 except 里用
  short_queries:
    - 堆栈
    - exception
    - 报错日志

status: tested
tested_versions: ["3.10", "3.11", "3.12", "3.13", "3.14"]
min_version: "3.0"
version_note: "logging.exception 等价于 error(..., exc_info=True)，各版本一致"
sources:
  - Python 官方文档 logging.exception
---

# 记录异常堆栈到日志

## 功能描述

输入一条说明，输出日志行 + **完整异常堆栈**；必须在 `except` 块里调用才有效。

## 推荐代码

```python
import logging

logging.basicConfig(level=logging.INFO, format="%(levelname)s %(message)s")

try:
    int("abc")
except ValueError:
    logging.exception("转换失败")   # 日志里带 traceback

# 不在 except 里时用 error + exc_info
logging.error("没有异常上下文", exc_info=True)
```

## 语句解释

### logging.exception(消息)

等价于 `logging.error(消息, exc_info=True)`，会自动附上当前正在处理的异常堆栈。

### 只能在 except 里用

它靠「当前异常」这个上下文，出了 `except` 就取不到，堆栈会是 `NoneType: None`。

### exc_info=True

显式要求「把异常信息一起记下来」，在 `except` 外用也行（但得自己把异常传进去才准）。

## 原理解释

**一句话：** 它把日志和「当前正在处理的异常」关联起来，写日志时顺带把那串堆栈也写进去。

**执行逻辑：**

1. 从当前执行上下文取出「正在处理的异常」信息
2. 生成一条 ERROR 级别日志记录，附带这个异常
3. 处理器格式化时，把堆栈追加在消息后面
4. 输出到文件或控制台

**机器层（可跳过）：** 堆栈信息来自异常对象自带的 traceback，不额外回溯。

**边界（从逻辑推出来）：**

- 第 1 步依赖上下文，所以只能在 `except` 块里用；否则记下的是「没有异常」
- 第 3 步堆栈是追加的，所以日志会多好几行——查问题时正是要这个
- 因为级别是 ERROR，把日志级别设成 CRITICAL 时它也不会输出
- 它**不吞异常**，记完日志异常仍然继续往上抛

## 注意事项

- 只在 `except` 里用 `logging.exception`。
- 记完日志要决定：继续抛（`raise`）还是吞掉——别默默吞。
- 日志里不要写密码、令牌，堆栈里也可能带参数值。
- 生产环境用文件+轮转，别只打控制台。

## 使用场景

- 服务端捕获异常后留现场。
- 批处理任务里记录「哪一条数据出错」。
- 桌面程序把报错写进日志，让用户发过来。
