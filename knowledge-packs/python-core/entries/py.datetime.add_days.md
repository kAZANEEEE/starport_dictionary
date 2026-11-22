---
id: py.datetime.add_days
title: 日期加减几天
description: 算「三天后」「两周前」是哪一天
language: python
category_id: programming.basics
module: datetime
origin: stdlib
import: "from datetime import datetime, timedelta"
qualname: "datetime + timedelta"
signature: "dt + timedelta(days=7) / dt - timedelta(hours=2)"
args:
  - name: "dt"
    required: true
    accepts: "一个 datetime（或 date）"
    nesting: "可以，可以是 datetime.now()"
  - name: "timedelta"
    required: true
    accepts: "间隔：days=7、hours=2、minutes=30 可以组合写"
    nesting: "可以，两个 timedelta 也能相加"
returns: "新的 datetime：日期变了但原对象不变（datetime 不可变）"
object:
  id: datetime.time
  name: 时间
  aliases: [时间, 日期, 几天后, 加减, timedelta]
action:
  id: convert.transform
  name: 转换
  aliases: [加, 减, 往后推, 往前推, add]
targets: []
utterances:
  direct:
    - 日期加几天
    - 算三天后是哪天
    - 时间往前推一周
  questions:
    - 怎么在当前时间上加七天
    - timedelta 怎么用
    - 加一个月怎么写
  colloquial:
    - 想算出下周同日
    - 会员还剩几天怎么算
  technical:
    - timedelta
    - date + days
    - relativedelta 加月
  short_queries:
    - 日期加减
    - timedelta
    - 几天后
status: tested
tested_versions: ["3.10", "3.11", "3.12", "3.13", "3.14"]
min_version: "3.0"
version_note: "timedelta 各版本一致；按「月」加减需要第三方 dateutil.relativedelta"
sources:
  - Python 官方文档 datetime.timedelta
---

# 日期加减几天

## 功能描述

输入一个时间 + 一个间隔，输出新的时间；原对象不变，返回的是新对象。

## 推荐代码

```python
from datetime import datetime, timedelta

now = datetime(2026, 1, 30, 10, 0, 0)

print(now + timedelta(days=3))       # 2026-02-02 10:00:00（自动进位）
print(now - timedelta(weeks=2))      # 2026-01-16 10:00:00
print(now + timedelta(hours=5, minutes=30))

today = now.date()
print(today + timedelta(days=1))     # 只对 date 也能加
```

## 语句解释

### timedelta(days=, hours=, weeks=)

表示一段时长。多个单位可以一起写，会自动换算成「天 + 秒」。

### dt + timedelta

返回**新对象**。跨越月份、年份会自动算对（不会出现 1 月 32 日）。

### dt - timedelta

同理，往前推。

## 原理解释

**一句话：** 它先把时间换算成「从某个起点算起的总秒数」，加上间隔，再换回年月日。

**执行逻辑：**

1. 把 datetime 换算成内部的「天数 + 当天秒数」
2. 把 timedelta 也换算成「天数 + 秒数」
3. 两个相加；秒数溢出了就往天上进位
4. 再把天数还原成年月日（自动处理每月多少天、闰年）
5. 返回新对象，原对象不动

**机器层（可跳过）：** 内部全是整数运算，不涉及时区换算（除非对象本身带时区）。

**边界（从逻辑推出来）：**

- 第 4 步负责日历换算，所以 1 月 30 日加 3 天得到 2 月 2 日，不会出错
- 因为 timedelta 只认「天/秒」，**不能加「一个月」**——每月长度不同
- 第 5 步不可变，所以要接返回值：`now = now + timedelta(...)`
- 带时区的对象加 timedelta 仍保持时区，不会帮你换算成别的时区

## 注意事项

- 加「一个月」不能用 timedelta；用第三方 `dateutil.relativedelta(months=1)`。
- 记住接返回值（不可变对象）。
- `date` 和 `datetime` 别混着加（会抛类型错误）。
- 算「还剩几天」用相减得 `timedelta`，再取 `.days`。

## 使用场景

- 会员到期日、试用期结束日。
- 生成「最近 7 天」的日期列表。
- 定时任务里算下次执行时间。
