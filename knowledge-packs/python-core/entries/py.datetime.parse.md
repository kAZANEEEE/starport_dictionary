---
id: py.datetime.parse
title: 把字符串解析成时间
description: 「2026-11-22 10:30」这样的文本转成时间对象
language: python
category_id: programming.basics
module: datetime

object:
  id: datetime.time
  name: 时间
  aliases: [时间, 日期, 时间字符串, 日期文本, datetime]

action:
  id: convert.transform
  name: 转换
  aliases: [解析, 转成时间, 变成时间对象, 读成时间, parse, strptime]

targets: []

utterances:
  direct:
    - 字符串转时间
    - 解析日期字符串
    - 把时间文本变成时间对象
  questions:
    - 怎么把字符串解析成时间
    - 如何把 2026-11-22 转成 datetime
    - Python 怎么比较两个时间字符串
  colloquial:
    - 用户输入的日期怎么变成时间
    - 这串日期文本怎么拿来算差值
  technical:
    - strptime
    - fromisoformat
    - datetime parse
  short_queries:
    - 解析时间
    - strptime

status: tested
tested_versions: ["3.10", "3.11", "3.12", "3.13", "3.14"]
min_version: "3.7"
version_note: fromisoformat 从 3.7 起；3.11 起对更多 ISO 变体宽容
sources:
  - Python 官方文档 datetime.strptime
  - Python 官方文档 datetime.fromisoformat
---

# 把字符串解析成时间

## 功能描述

输入日期时间字符串 + 格式串，输出 `datetime` 对象；格式对不上就抛 `ValueError`。

## 推荐代码

```python
from datetime import datetime

t = datetime.strptime("2026-11-22 10:30:00", "%Y-%m-%d %H:%M:%S")
print(t.year, t.month, t.day)

print(datetime.fromisoformat("2026-11-22T10:30:00"))

a = datetime.strptime("2026-11-22", "%Y-%m-%d")
b = datetime.strptime("2026-11-20", "%Y-%m-%d")
print((a - b).days)          # 2
```

## 语句解释

### strptime(字符串, 格式)

`p` 是 parse。格式串必须和输入**严格对应**，空格数量也要一致。

### fromisoformat()

解析 ISO 格式，省得写格式串；格式不标准时会报错（3.11 起宽容度提高）。

### 相减得到 timedelta

两个 `datetime` 相减得 `timedelta`，用 `.days` / `.total_seconds()` 取值。

## 原理解释

**一句话：** 反过来——按你给的模板，把一段文本一个字段一个字段地读成时间。

**执行逻辑：**

1. 从字符串开头开始，按模板逐段匹配
2. 遇到 `%Y` 就读 4 位数字当年，遇到 `%m` 就读 2 位当月……每段都要对得上
3. 全部字段都读出来 → 组装成 `datetime` 对象返回
4. 任何一段对不上（少个零、多个空格）→ 直接抛 `ValueError`

**机器层（可跳过）：** 纯字符串匹配 + 数字转换，不查系统时间。

**边界（从逻辑推出来）：**

- 第 2 步是**严格匹配**，所以模板和文本必须一字不差，多一个空格都失败
- 第 4 步直接抛错，所以解析用户输入必须包 `try`
- 文本带时区（`+08:00`）时模板要写 `%z`，否则末尾那段匹配不上
- 因为结果是新对象，与原字符串没有任何关联
## 注意事项

- 格式串和输入必须一一对应，多一个空格都失败。
- 解析失败抛 `ValueError`，要紧的地方包 `try`。
- 带时区的字符串（`+08:00`）要用 `fromisoformat` 或 `%z`。
- 中文日期（“2026年11月22日”）要自定义格式：`"%Y年%m月%d日"`。

## 使用场景

- 读日志文件里的时间戳做统计。
- 处理用户输入的日期。
- 计算两个事件相差几天。
