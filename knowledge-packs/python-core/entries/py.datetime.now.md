---
id: py.datetime.now
title: 获取当前时间
description: 拿到现在的时间，并格式化成字符串
language: python
category_id: programming.basics
module: datetime

object:
  id: datetime.time
  name: 时间
  aliases: [时间, 当前时间, 现在, 时间戳, 日期时间, datetime]

action:
  id: get.obtain
  name: 获取
  aliases: [获取, 拿到, 取得, now]

targets: []

utterances:
  direct:
    - 获取当前时间
    - 取得现在的时间
    - 打印当前日期时间
    - 拿到系统时间
  questions:
    - 怎么获取当前时间
    - 如何把时间格式化成年月日
    - Python 怎么生成时间字符串
    - 怎么算程序跑了多久
  colloquial:
    - 想在日志里带上时间
    - 文件名里加个时间戳
    - 现在几点了，代码里怎么拿
  goal_based:
    - 记录任务开始和结束时间
    - 按日期给文件分类命名
  technical:
    - datetime.now
    - strftime
    - time.time
    - isoformat
  short_queries:
    - 时间
    - 当前时间
    - now
    - 时间戳

status: tested
tested_versions: ["3.10", "3.11", "3.12", "3.13", "3.14"]
min_version: "3.0"
version_note: datetime 是标准库老模块；3.12 加入 datetime.UTC 常量，本条目用不到
sources:
  - Python 官方文档 datetime.datetime.now
  - Python 官方文档 datetime.datetime.strftime
---

# 获取当前时间

## 功能描述

拿到当前时间，并能格式化成字符串、算出两段代码之间的耗时。

## 推荐代码

```python
from datetime import datetime
import time

now = datetime.now()
print(now)                                  # 2026-11-22 01:20:33.123456

print(now.strftime("%Y-%m-%d %H:%M:%S"))    # 2026-11-22 01:20:33
print(now.year, now.month, now.day)         # 拆开取

start = time.perf_counter()
time.sleep(0.01)
print(f"耗时 {time.perf_counter() - start:.3f} 秒")
```

## 语句解释

### datetime.now()

返回本机的当前时间（**不带时区**），精确到微秒。

### .strftime("%Y-%m-%d %H:%M:%S")

把时间格式化成字符串。`%Y` 四位年、`%m` 月、`%d` 日、`%H` 时分秒。
常用 `%Y%m%d_%H%M%S` 做文件名里的时间戳。

### time.perf_counter()

测耗时专用计时器，单调递增，不受系统时间被改动影响。**测耗时就该用它，不是 datetime.now()**。

## 原理解释

**一句话：** 向系统问一句「现在几点」，拿回一个能拆分、能加减的时间对象。

**执行逻辑：**

1. 读系统时钟（年月日时分秒微秒）
2. 用它构造一个 `datetime` 对象（**不带时区信息**）
3. `.strftime(...)` 把它按模板拼成文本；`.year/.month/...` 直接取某一项
4. 两个时间相减得到 `timedelta`，再取 `.days` / `.total_seconds()`

**机器层（可跳过）：** 读的是系统时钟，会被校时影响。

**边界（从逻辑推出来）：**

- 第 1 步读系统时钟，如果期间系统同步了时间，差值可能异常——**测耗时要用 `perf_counter`**
- 第 2 步不带时区，跨时区比较会错，要带时区得用 `now(timezone.utc)`
- 第 3 步的模板里 `%m` 是月、`%M` 是分，写反了不报错但结果全错
- 相减只对同类型对象有效（都带时区或都不带），混着会抛异常
## 注意事项

- `datetime.now()` 不带时区；要带时区用 `datetime.now(timezone.utc)` 或 `astimezone()`。
- 测耗时用 `perf_counter()`，不要用 `datetime.now()`。
- `strftime` 里的 `%m` 是月、`%M` 是分，写反了很难发现。
- 时间戳（秒）用 `time.time()`，和 `datetime` 是两个体系，转换用 `fromtimestamp`。

## 使用场景

- 日志每行带时间戳。
- 文件名加时间，避免覆盖。
- 统计某段代码、某个任务跑了多久。
