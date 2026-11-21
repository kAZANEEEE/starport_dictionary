---
id: py.time.timestamp
title: 获取时间戳
description: 拿到从 1970 年到现在过了多少秒
language: python
category_id: programming.basics
module: time

object:
  id: datetime.time
  name: 时间
  aliases: [时间, 时间戳, 秒数, 当前时间, timestamp]

action:
  id: get.obtain
  name: 获取
  aliases: [取, 获取, 拿到, 算, get]

targets: []

utterances:
  direct:
    - 获取时间戳
    - 拿到当前时间戳
    - 取现在的秒数
  questions:
    - 怎么获取当前时间戳
    - 如何把时间转成时间戳
    - Python 怎么拿到毫秒级时间
  colloquial:
    - 想给文件加个数字时间当名字
    - 算两个时间差多少秒
  technical:
    - time.time
    - time.time_ns
    - datetime timestamp
  short_queries:
    - 时间戳
    - timestamp
    - time

status: tested
tested_versions: ["3.10", "3.11", "3.12", "3.13", "3.14"]
min_version: "3.3"
version_note: time.time 一直有；time.time_ns 从 3.7 起
sources:
  - Python 官方文档 time.time
  - Python 官方文档 time.time_ns
---

# 获取时间戳

## 功能描述

拿到“从 1970-01-01 UTC 到现在过了多少秒”的浮点数，常用来做文件名或算耗时。

## 推荐代码

```python
import time
from datetime import datetime

ts = time.time()
print(f"{ts:.0f}")                       # 例如 1795281234
print(int(ts * 1000))                    # 毫秒
print(time.time_ns())                    # 纳秒，3.7+

print(datetime.fromtimestamp(ts))        # 还原成本地时间
```

## 语句解释

### time.time()

返回浮点秒数，带小数部分（小数就是不足一秒的零头）。

### int(ts * 1000)

要毫秒就乘 1000 再取整。**别用 round**，取整更稳。

### datetime.fromtimestamp(ts)

把时间戳还原成可读时间。注意它按**本地时区**解释。

## 原理解释

时间戳是“Unix 纪元以来的秒数”，与时区无关——它记录的是同一个绝对时刻。
时区只在“显示成人看的年月日”时才介入，所以 `fromtimestamp` 需要知道你所在时区。

`time.time()` 读系统时钟，会被校时影响；测耗时应该用 `time.perf_counter()`。

## 注意事项

- 时间戳是 UTC 基准，跨时区比较是安全的；格式化成本地时间才会带时区。
- 秒级精度做文件名可能重复（同一秒内多次），加个序号或毫秒。
- `time.time()` 不适合测耗时（系统校时会让差值异常）。
- 32 位环境下 2038 年会有溢出问题，Python 的 int 本身不受限，但底层接口可能。

## 使用场景

- 文件名加唯一时间后缀。
- 记录事件发生时刻（日志、数据库）。
- 和 `datetime` 互转，做时间计算。
