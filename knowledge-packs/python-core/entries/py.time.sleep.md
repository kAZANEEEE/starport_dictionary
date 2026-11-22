---
id: py.time.sleep
title: 让程序等一会儿
description: 暂停几秒再继续，常用于重试和限速
language: python
category_id: programming.basics
module: time
origin: stdlib
import: "import time"
qualname: "time.sleep"

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

**一句话：** 告诉操作系统「我这个线程先歇 N 秒，到点再叫我」。

**执行逻辑：**

1. 把秒数交给操作系统的定时机制
2. 当前线程被挂起，让出 CPU（别的程序照跑）
3. 时间到了，系统把线程唤醒
4. 从下一行继续执行

**机器层（可跳过）：** 是真正的挂起，不是空转，所以几乎不占 CPU。

**边界（从逻辑推出来）：**

- 第 3 步是系统唤醒，精度受调度影响，实际可能比指定时间略长
- 第 2 步挂起的是**整个线程**，GUI 主线程被挂起 = 界面卡死
- 异步代码里用它会把整个事件循环堵住，要用 `await asyncio.sleep()`
- 想「等到某个条件」不能靠 sleep 猜时间，那是轮询，间隔会决定反应速度
## 注意事项

- 会阻塞整个线程，GUI 主线程里千万别用。
- 精度不保证，实际可能比指定时间略长。
- 异步代码里用 `await asyncio.sleep()`，不是 `time.sleep`。
- 重试等待建议指数退避（1、2、4 秒），别固定间隔死磕。

## 使用场景

- 爬虫/接口调用限速。
- 轮询等待某个条件成立。
- 重试之间退避。
