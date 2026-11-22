---
id: py.datetime.diff
title: 算两个时间差多少
description: 两个时间相减，得到多少天、多少秒
language: python
category_id: programming.basics
module: datetime
origin: stdlib
import: "from datetime import datetime"
qualname: "datetime.diff"
signature: "dt_a - dt_b"
args:
  - name: "两个时间"
    required: true
    accepts: "两个 datetime（时区要一致）"
    nesting: "可以，可以和 timedelta 一起参与运算"
returns: "timedelta：间隔。用 .days 取整天、.total_seconds() 取总秒数"

object:
  id: datetime.time
  name: 时间
  aliases: [时间, 两个时间, 时间差, 间隔, datetime]

action:
  id: compare.diff
  name: 比较
  aliases: [相减, 算差, 差多少, 间隔多久, diff]

targets: []

utterances:
  direct:
    - 算两个时间的时间差
    - 两个日期相差几天
    - 计算时间间隔
  questions:
    - 怎么算两个时间相差多少天
    - 如何计算程序运行了多久
    - timedelta 怎么取小时和分钟
  colloquial:
    - 这事发生到现在多少天了
    - 差了两个小时还是两天
  technical:
    - timedelta
    - total_seconds
    - days
    - 时间相减
  short_queries:
    - 时间差
    - 相差
    - timedelta

status: tested
tested_versions: ["3.10", "3.11", "3.12", "3.13", "3.14"]
min_version: "3.0"
version_note: timedelta 各版本一致；total_seconds 从 2.7 起
sources:
  - Python 官方文档 datetime.timedelta
---

# 算两个时间差多少

## 功能描述

输入两个时间对象，输出一个 `timedelta`（天数 + 秒数）；用 `.days` / `.total_seconds()` 取具体数值。

## 推荐代码

```python
from datetime import datetime

a = datetime(2026, 11, 22, 10, 0, 0)
b = datetime(2026, 11, 20, 8, 30, 0)

delta = a - b
print(delta)                     # 2 days, 1:30:00
print(delta.days)                # 2（只取整天数）
print(delta.total_seconds())     # 176400.0
print(delta.total_seconds() / 3600)   # 49.0 小时
```

## 语句解释

### a - b

两个时间相减得到 `timedelta`，表示「从 b 到 a 的间隔」。

### .days

只取**整天**部分，不是「总天数」。`2 days, 1:30:00` 的 `.days` 是 2。

### .total_seconds()

换算成总秒数（浮点），之后自己除以 3600 得小时、除以 86400 得天。

### 反过来 b - a

得到负数间隔，`.days` 会是 -1 这类值（不是 0），因为它按「天 + 剩余秒」表示。

## 原理解释

**一句话：** 把两个时刻都换算到同一个计数轴上，相减就得到中间隔了多少。

**执行逻辑：**

1. 两个时间各自换算成「距某个基准点的天数 + 时分秒」
2. 相减得到天数差和秒数差
3. 如果秒数差是负数，就向天数借 1（借 86400 秒）
4. 结果规范化成「整天 + 0~24 小时的余数」再交给你

**机器层（可跳过）：** timedelta 内部就是「天、秒、微秒」三个整数。

**边界（从逻辑推出来）：**

- 第 3 步「借一天」让负差值看起来奇怪：`-1 day, 23:00:00` 其实是「负 1 小时」
- 第 4 步的规范化说明 `.days` 只是整天部分，要总时长必须用 `total_seconds()`
- 带时区和不带时区的对象不能相减，会抛 `TypeError`
- 只想知道「是不是超过 30 天」用 `delta > timedelta(days=30)`，比换算成秒清楚

## 注意事项

- `.days` 是整天部分，不是总天数——超过 24 小时但不满一天的部分不会算进去。
- 负间隔的 `.days` 会向下取整，看数字容易误判，直接用 `total_seconds()` 判断正负。
- 时区必须一致才能相减。
- 只比较日期不管时间，可以用 `.date()` 先截断。

## 使用场景

- 计算任务耗时、会员剩余天数。
- 判断「多久没登录」。
- 按间隔做限流或过期清理。
