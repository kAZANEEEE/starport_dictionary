---
id: py.logging.basic
title: 输出日志（比 print 规范）
description: 用 logging 打带级别和时间的信息
language: python
category_id: programming.basics
module: logging

object:
  id: log.record
  name: 日志
  aliases: [日志, 记录, 输出信息, 调试信息, log]

action:
  id: create.new
  name: 创建
  aliases: [输出, 打印, 记录, 打日志, log, print]

targets: []

utterances:
  direct:
    - 输出日志
    - 打印日志信息
    - 用 logging 记录
  questions:
    - 怎么用 logging 打印日志
    - 日志和 print 有什么区别
    - 怎么让日志带时间
  colloquial:
    - 不想再用 print 调试了
    - 想给输出加时间和级别
  technical:
    - logging.basicConfig
    - logging.info
    - 日志格式 format
    - 日志级别
  short_queries:
    - 日志
    - logging
    - 打日志

status: tested
tested_versions: ["3.10", "3.11", "3.12", "3.13", "3.14"]
min_version: "3.0"
version_note: logging 各版本接口稳定；basicConfig 只在首次调用时生效
sources:
  - Python 官方文档 logging.basicConfig
---

# 输出日志（比 print 规范）

## 功能描述

输入一条消息 + 级别，输出到控制台（或文件）；低于设定级别的消息**直接丢弃不处理**。

## 推荐代码

```python
import logging

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
)

logging.debug("这条不会显示（低于 INFO）")
logging.info("程序启动")
logging.warning("配置项缺失，用默认值")
logging.error("请求失败")
```

## 语句解释

### basicConfig(level=, format=)

一次配置全局格式和最低级别。**只在第一次调用时生效**，后面再调会被忽略。

### logging.info(...) 等

五个常用级别从低到高：DEBUG < INFO < WARNING < ERROR < CRITICAL。

### format 里的占位

`%(asctime)s` 时间、`%(levelname)s` 级别、`%(message)s` 消息。

## 原理解释

**一句话：** 每条日志要过一道「级别闸门」，够高才放行，放行后按模板拼好再输出。

**执行逻辑：**

1. 调用 `info("xx")` 时，先造一条日志记录（带级别、时间、消息）
2. 拿它的级别和设定的最低级别比：不够高 → 直接丢弃，**后面的格式化都省了**
3. 够高 → 交给处理器（控制台或文件）
4. 处理器按 `format` 模板把各字段拼成一行
5. 写到目标位置

**机器层（可跳过）：** 级别判断在拼接之前，所以关掉 debug 几乎零开销。

**边界（从逻辑推出来）：**

- 第 2 步是「低于就丢」，所以 `level=INFO` 时 `debug` 的消息永远看不到——不是没打，是没进来
- 第 4 步靠模板，所以不配 `format` 就只有干巴巴一句 message
- `basicConfig` 只在第一次生效：模块被 import 多次时第二次调会被忽略，这是「我改了格式没生效」的真实原因
- 因为第 2 步在拼接之前，用 `log.debug("%s", 大对象)` 的写法比 f-string 更省——后者会先拼好再丢

## 注意事项

- 别用 f-string 拼日志参数（会先计算），用 `logging.info("x=%s", x)` 的惰性写法。
- `basicConfig` 只生效一次；要改格式得先 `logging.getLogger().handlers.clear()`。
- 生产环境默认级别设 INFO，调试时临时设 DEBUG。
- 多线程/多进程写同一文件要配 `FileHandler`，否则可能串行错乱。

## 使用场景

- 替换散落各处的 print。
- 记录程序流程和错误上下文。
- 线上排查问题（级别控制输出量）。
