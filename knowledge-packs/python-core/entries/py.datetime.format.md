---
id: py.datetime.format
title: 把时间格式化成字符串
description: 时间对象转成 2026-11-22 10:30:00 这样的文本
language: python
category_id: programming.basics
module: datetime

object:
  id: datetime.time
  name: 时间
  aliases: [时间, 日期, 日期时间, 时间对象, datetime]

action:
  id: convert.transform
  name: 转换
  aliases: [格式化, 转成字符串, 变成文本, 输出格式, format, strftime]

targets: []

utterances:
  direct:
    - 格式化时间
    - 时间转成字符串
    - 按格式输出日期
  questions:
    - 怎么把时间格式化成字符串
    - 如何输出 yyyy-mm-dd 格式
    - Python 怎么打印好看的时间
  colloquial:
    - 想要 2026年11月22日 这种写法
    - 日志里的时间格式怎么弄
  technical:
    - strftime
    - isoformat
    - f-string 时间格式
  short_queries:
    - 格式化
    - strftime

status: tested
tested_versions: ["3.10", "3.11", "3.12", "3.13", "3.14"]
min_version: "3.0"
version_note: strftime 的指令集各版本一致；isoformat 是 3.6 起的标准写法
sources:
  - Python 官方文档 datetime.strftime
---

# 把时间格式化成字符串

## 功能描述

输入一个时间对象 + 格式串，输出字符串；反过来解析用 `strptime`。

## 推荐代码

```python
from datetime import datetime

now = datetime(2026, 11, 22, 10, 30, 45)
print(now.strftime("%Y-%m-%d %H:%M:%S"))   # 2026-11-22 10:30:45
print(now.strftime("%Y年%m月%d日"))          # 2026年11月22日
print(now.isoformat())                      # 2026-11-22T10:30:45
```

## 语句解释

### strftime(格式)

`%Y` 四位年、`%m` 月、`%d` 日、`%H` 时、`%M` 分、`%S` 秒。**`%m` 是月，`%M` 是分**。

### isoformat()

标准 ISO 8601 格式，机器之间传输用它，不用记格式串。

## 原理解释

`strftime` 是把时间字段按模板拼字符串，本质是字符串替换，不涉及时区换算——
`datetime` 里存的是什么就输出什么。要转时区得先 `astimezone()`。

## 注意事项

- `%m`（月）和 `%M`（分）极易写反。
- 本地化名称（星期、月份英文）受系统 locale 影响，跨机器可能不一致。
- 传输/存库用 `isoformat()`，给人看再用 `strftime`。
- 文件名里用 `%Y%m%d_%H%M%S`，别带冒号（Windows 文件名不允许）。

## 使用场景

- 日志每行带时间。
- 生成带时间的文件名或目录名。
- 报表里输出人类可读日期。
