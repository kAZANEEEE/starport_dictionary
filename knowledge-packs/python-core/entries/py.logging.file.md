---
id: py.logging.file
title: 把日志写进文件
description: 输出同时进控制台和文件，方便事后查
language: python
category_id: programming.basics
module: logging

object:
  id: log.record
  name: 日志
  aliases: [日志, 日志文件, 记录文件, log file]

action:
  id: create.new
  name: 创建
  aliases: [写入文件, 保存日志, 输出到文件, 落盘, write]

targets: []

utterances:
  direct:
    - 日志写入文件
    - 把日志保存到文件
    - 日志同时输出到控制台和文件
  questions:
    - 怎么把日志存成文件
    - 日志文件怎么按天切分
    - 日志太多怎么自动轮转
  colloquial:
    - 出问题了想看之前的记录
    - 程序关了日志还在吗
  technical:
    - FileHandler
    - RotatingFileHandler
    - logging.basicConfig filename
  short_queries:
    - 日志文件
    - FileHandler
    - RotatingFileHandler

status: tested
tested_versions: ["3.10", "3.11", "3.12", "3.13", "3.14"]
min_version: "3.0"
version_note: RotatingFileHandler / TimedRotatingFileHandler 各版本稳定
sources:
  - Python 官方文档 logging.handlers.RotatingFileHandler
---

# 把日志写进文件

## 功能描述

输入日志消息，输出到文件（可同时输出到控制台）；文件超过大小会自动切分。

## 推荐代码

```python
import logging
from logging.handlers import RotatingFileHandler

logger = logging.getLogger("demo")
logger.setLevel(logging.INFO)

# 文件处理器：单个文件最大 1MB，保留 3 个备份
fh = RotatingFileHandler("app.log", maxBytes=1_000_000, backupCount=3, encoding="utf-8")
fh.setFormatter(logging.Formatter("%(asctime)s [%(levelname)s] %(message)s"))

# 控制台处理器
sh = logging.StreamHandler()
sh.setFormatter(logging.Formatter("%(message)s"))

logger.addHandler(fh)
logger.addHandler(sh)

logger.info("这条会同时进文件和控制台")
print(open("app.log", encoding="utf-8").read().strip().splitlines()[-1])
```

## 语句解释

### RotatingFileHandler(文件, maxBytes=, backupCount=)

写文件，超过 `maxBytes` 就把当前文件改名成 `.1`，新的继续写，最多留 `backupCount` 个。

### addHandler(...)

一个 logger 可以挂多个处理器，每个处理器各管一个去处。

### Formatter(模板)

每个处理器可以有自己的格式——控制台简洁、文件详细很常见。

## 原理解释

**一句话：** 一条日志会沿着 logger 上挂的处理器挨个走一遍，每个处理器自己决定怎么落地。

**执行逻辑：**

1. 日志记录先过 logger 的级别闸门
2. 够高 → 复制给每一个挂着的处理器
3. 文件处理器：把这一行写进文件缓冲区
4. 写入前检查文件是不是超了 `maxBytes`：超了就关掉当前文件、改名、开新文件
5. 控制台处理器：把这一行打到标准输出

**机器层（可跳过）：** 写文件是追加模式打开，每次写一行；轮转时是改名 + 新建。

**边界（从逻辑推出来）：**

- 第 2 步是「给每个处理器」，所以挂了两个处理器就会输出两次——这是「日志重复」的真正原因
- 第 4 步在写之前检查，所以单个文件可能略超 `maxBytes`（超出一条的长度）
- 因为第 3 步有缓冲区，程序崩溃时最后几行可能还没落盘（`flush()` 可强制刷）
- `basicConfig(filename=...)` 也能写文件，但没法做轮转，长期跑会撑爆磁盘

## 注意事项

- 挂多个处理器时注意「日志重复」；`propagate=False` 可以阻止往上冒泡。
- 记着 `encoding="utf-8"`，否则中文日志在 Windows 上会乱。
- 长期运行的服务一定要用轮转处理器，别让日志把磁盘吃满。
- logger 名建议用 `__name__`，方便按模块调级别。

## 使用场景

- 长时间运行的服务留现场。
- 桌面程序出问题后让用户把 log 发过来。
- 把调试信息留在文件里，控制台只打关键几行。
