---
id: py.datetime.ts_to_str
title: 时间戳转成可读时间
description: 拿到一串数字（1795…）怎么变成年月日
language: python
category_id: programming.basics
module: datetime
origin: stdlib
import: "from datetime import datetime"
qualname: "datetime.fromtimestamp()"
signature: "datetime.fromtimestamp(时间戳)"
args:
  - name: "时间戳"
    required: true
    accepts: "从 1970 年起的秒数（浮点或整数）"
    nesting: "可以，常来自 time.time() 或数据库"
returns: "datetime 对象（按**本地时区**解释）；再 .strftime 才是字符串"
object:
  id: datetime.time
  name: 时间
  aliases: [时间, 时间戳, 可读时间, 日期时间, datetime]
action:
  id: convert.transform
  name: 转换
  aliases: [转换, 变成时间, 格式化, fromtimestamp]
targets: []
utterances:
  direct:
    - 时间戳转成时间
    - 把秒数变成日期
    - 时间戳格式化
  questions:
    - 怎么把时间戳转成可读时间
    - fromtimestamp 用的是哪个时区
    - 数据库里的时间戳怎么显示
  colloquial:
    - 拿到一串 1795 开头的数字，看不懂
    - 日志里时间是数字，想变成年月日
  technical:
    - fromtimestamp
    - utcfromtimestamp
    - 时区
    - 时间戳转换
  short_queries:
    - 时间戳转换
    - fromtimestamp
    - 转时间
status: tested
tested_versions: ["3.10", "3.11", "3.12", "3.13", "3.14"]
min_version: "3.0"
version_note: "fromtimestamp 各版本一致；utcfromtimestamp 在 3.12 起被标为不推荐"
sources:
  - Python 官方文档 datetime.fromtimestamp
---

# 时间戳转成可读时间

## 功能描述

输入秒数（浮点），输出本地的 `datetime` 对象；要字符串还得再 `.strftime()`。

## 推荐代码

```python
from datetime import datetime
import time

ts = time.time()
print(ts)                                    # 1795xxxxxx.123

dt = datetime.fromtimestamp(ts)
print(dt)                                    # 2026-11-22 13:20:45.123456
print(dt.strftime("%Y-%m-%d %H:%M:%S"))       # 2026-11-22 13:20:45

# 按 UTC 解释（和本地差几个时区）
print(datetime.fromtimestamp(ts).astimezone())
```

## 语句解释

### fromtimestamp(秒)

把时间戳解释成**本地时间**。

### 结果还是 datetime

要人能看的字符串必须再 `strftime`。

### UTC 与本地

同一时间戳在 UTC 和本地差一个时区偏移；`astimezone()` 能看带时区的版本。

## 原理解释

**一句话：** 它把「距 1970 年多少秒」加上时区偏移，换成年月日时分秒。

**执行逻辑：**

1. 拿到秒数
2. 加上本机时区偏移（比如东八区 +8 小时）
3. 把总秒数换算成「第几天 + 当天多少秒」
4. 再从天数反推年月日（自动处理闰年、每月天数）
5. 返回 datetime 对象

**机器层（可跳过）：** 纯算术，不查网络也不查磁盘。

**边界（从逻辑推出来）：**

- 第 2 步加偏移，所以**同一时间戳在不同时区的机器上显示不同**
- 第 4 步要处理日历，所以 2 月 29 日这类边界不会出错
- 输入是浮点时，小数部分变成微秒
- 时间戳超出范围（很大或负数）可能抛 `OSError`/`ValueError`

## 注意事项

- 它是本地时区；跨机器比较时要统一用 UTC。
- 转换完还是对象，要字符串得 `strftime`。
- 数据库里存时间戳比存字符串更省事、也便于比较。
- 别用已弃用的 `utcfromtimestamp`，用 `fromtimestamp(ts, timezone.utc)`。

## 使用场景

- 显示后端返回的时间戳。
- 日志时间数字转成可读。
- 把旧数据的时间戳批量格式化导出。
