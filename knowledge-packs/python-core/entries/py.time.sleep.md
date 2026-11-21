---
id: py.time.sleep
title: 让程序等一会儿
description: 暂停几秒再继续，常用于重试和限速
language: python
category_id: programming.basics
module: time

object:
  id: datetime.time
  name: 时间
  aliases: [时间, 等待, 延时, 暂停, 间隔, sleep]

action:
  id: run.execute
  name: 执行
  aliases: [等待, 暂停, 休眠, 延时, 等一下, sleep, wait]

targets: []

utterances:
  direct:
    - 让程序等一会儿
    - 延时几秒
    - 暂停执行
  questions:
    - 怎么让程序停顿两秒
    - 如何实现延时
    - Python 怎么等待一段时间
  colloquial:
    - 请求太快了，中间歇一下
    - 想隔一秒再发下一个
  technical:
    - time.sleep
    - asyncio.sleep
    - 限速 sleep
  short_queries:
    - 等待
    - 延时
    - sleep

status: tested
tested_versions: ["3.10", "3.11", "3.12", "3.13", "3.14"]
min_version: "3.0"
version_note: time.sleep 可接受 float；3.5 起更精细
sources:
  - Python 官方文档 time.sleep
---

# 让程序等一会儿

## 功能描述

输入秒数（可以是小数），让当前线程暂停那么久，没有返回值。

## 推荐代码

```python
import time

time.sleep(0.5)          # 停 0.5 秒
for i in range(3):
    print(i)
    time.sleep(0.2)      # 隔 0.2 秒打一个
```

## 语句解释

### time.sleep(秒)

阻塞当前线程。`0.5` 这种小数也可以，精度受系统调度影响，不保证毫秒级精确。

### 循环里的 sleep

做限速的标准写法：每处理一条，停一小会儿，避免把对方服务打崩。

## 原理解释

`sleep` 会让出 CPU，让操作系统把线程挂起，到时再唤醒——**不是空转等待**，
所以不占 CPU。但它是**阻塞**的：这段时间里这个线程什么都干不了。

在 GUI 程序里用它会让界面卡住（事件循环被阻塞），要换成 `QTimer` 或放进工作线程。

## 注意事项

- 会阻塞整个线程，GUI 主线程里千万别用。
- 精度不保证，实际可能比指定时间略长。
- 异步代码里用 `await asyncio.sleep()`，不是 `time.sleep`。
- 重试等待建议指数退避（1、2、4 秒），别固定间隔死磕。

## 使用场景

- 爬虫/接口调用限速。
- 轮询等待某个条件成立。
- 重试之间退避。
