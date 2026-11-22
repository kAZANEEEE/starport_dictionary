---
id: py.datetime.weekday
title: 判断星期几
description: 这个日期是周几，怎么输出「星期三」
language: python
category_id: programming.basics
module: datetime
origin: stdlib
import: "from datetime import datetime"
qualname: "datetime.weekday() / isoweekday()"
signature: "dt.weekday() / dt.isoweekday() / dt.strftime(\"%A\")"
args:
  - name: "dt"
    required: true
    accepts: "一个 datetime（或 date）"
    nesting: "可以，可以是 datetime.now()"
returns: "weekday() 给 0~6（周一=0）；isoweekday() 给 1~7（周一=1，周日=7）"
object:
  id: datetime.time
  name: 时间
  aliases: [时间, 日期, 星期, 周几, datetime]
action:
  id: get.obtain
  name: 获取
  aliases: [判断, 获取, 计算, 查, weekday]
targets: []
utterances:
  direct:
    - 判断星期几
    - 获取日期对应的星期
    - 算某天是周几
  questions:
    - 怎么知道一个日期是星期几
    - weekday 和 isoweekday 有什么区别
    - 怎么输出中文的星期几
  colloquial:
    - 想知道这天是周几
    - 想在界面上显示「星期三」
  technical:
    - datetime.weekday
    - isoweekday
    - strftime %A
    - 星期映射
  short_queries:
    - 星期
    - 周几
    - weekday
status: tested
tested_versions: ["3.10", "3.11", "3.12", "3.13", "3.14"]
min_version: "3.0"
version_note: "weekday / isoweekday 各版本一致"
sources:
  - Python 官方文档 datetime.weekday
---

# 判断星期几

## 功能描述

输入一个日期，输出它是周几的数字；中文名字要自己映射（标准库不内置中文星期）。

## 推荐代码

```python
from datetime import datetime

d = datetime(2026, 11, 22)

print(d.weekday())        # 6  ← 周一=0，所以 6 是周日
print(d.isoweekday())     # 7  ← 周一=1，所以 7 是周日

names = ["周一", "周二", "周三", "周四", "周五", "周六", "周日"]
print(names[d.weekday()]) # 周日
```

## 语句解释

### weekday()

返回 0~6，**周一 = 0**，周日 = 6。

### isoweekday()

返回 1~7，**周一 = 1**，周日 = 7（国际标准 ISO 的编号）。

### 中文要自己映射

用列表按下标取就行；`strftime("%A")` 输出的是英文星期名，还受系统语言影响。

## 原理解释

**一句话：** 它把日期换算成「距某个基准日过了几天」，再对 7 取余得到星期。

**执行逻辑：**

1. 把日期换算成从基准日算起的第几天
2. 对 7 取余
3. `weekday()` 让余数 0 对应周一；`isoweekday()` 把结果 +1 让周一变成 1
4. 返回这个数字

**机器层（可跳过）：** 纯算术，无 I/O。

**边界（从逻辑推出来）：**

- 两套编号差 1，混用会整体错一天，这是最常见的错
- 中文名不在标准库里，必须自己建表（或用第三方库）
- `strftime("%A")` 的输出受系统语言影响，同一段代码在别人机器上可能是中文/英文
- 它只认日期，不认时间；同一时刻不同时区可能是不同的星期

## 注意事项

- `weekday()` 周一=0，`isoweekday()` 周一=1，**别混**。
- 中文星期自己映射，别依赖 `%A`。
- 跨时区判断「周几」要先把时间转成目标时区。
- 只要日期不要时间时用 `.date()`。

## 使用场景

- 日历、排班表显示「周三」。
- 判断是不是周末（`weekday() >= 5`）。
- 统计「每周几的数据量」。
