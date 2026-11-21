---
id: py.json.read
title: 读取 JSON 文件
description: 把 JSON 文件读成字典或列表
language: python
category_id: programming.filesystem
module: json

object:
  id: json.object
  name: JSON 数据
  aliases: [json, json 对象, json 文件, 配置数据, json data]

action:
  id: get.obtain
  name: 获取
  aliases: [读取, 解析, 加载, 取, load, parse]

targets: []

utterances:
  direct:
    - 读取 JSON 文件
    - 解析 json
    - 把 json 读成字典
  questions:
    - 怎么读取 json 文件
    - 如何把 json 解析成字典
    - Python 怎么加载 json
  colloquial:
    - 那个 json 文件怎么弄进程序里
    - 想读配置文件的那些值
  short_queries:
    - json
    - 解析
    - json.load

status: tested
tested_versions: ["3.10", "3.11", "3.12", "3.13", "3.14"]
min_version: "3.0"
version_note: json 模块从 2.6 就有，3.x 一直是同一套接口
sources:
  - Python 官方文档 json.load
---

# 读取 JSON 文件

## 功能描述

把 JSON 文件解析成 Python 的字典或列表。

## 推荐代码

```python
import json
from pathlib import Path

# 演示用：先造一个文件，实际使用时这两行删掉
Path("config.json").write_text('{"name": "starport", "version": 1}', encoding="utf-8")

with open("config.json", encoding="utf-8") as f:
    data = json.load(f)

print(data["name"])      # starport
print(data["version"])   # 1
print(type(data).__name__)
```

## 语句解释

### open(..., encoding="utf-8")

读取 JSON 必须显式指定编码，Windows 默认 GBK 会把中文读坏。

### json.load(f)

从**文件对象**里读并解析。注意不是 `json.loads`——那个接收的是字符串。

### data["name"]

解析结果就是普通字典（对象）或列表（数组），照平时的方式取值。

## 原理解释

**一句话：** 把 JSON 文本翻译成 Python 能直接用的字典或列表。

**执行逻辑：**

1. 打开文件，把文本读进来（这一步只拿到一串字符）
2. 从第一个字符开始解析：见到 `{` 就开始读一个对象，见到 `[` 就开始读一个数组
3. 遇到字符串/数字/`true`/`false`/`null`，分别转成 `str`/`int` 或 `float`/`bool`/`None`
4. 按括号层级一层层收口，直到整个结构结束
5. 把解析结果返回（顶层是对象就是 dict，是数组就是 list）

**机器层（可跳过）：** 纯文本解析，不联网、不看原文件以外的东西。

**边界（从逻辑推出来）：**

- 第 2 步对格式极其严格：多一个逗号、写了注释都会抛 `JSONDecodeError`——JSON 不是 Python 字典
- 解析出来是**新的** dict/list，和原文件没有任何关联，改它不会回写文件
- 编码要在第 1 步指定，否则中文可能在读的时候就坏掉
- 因为是纯解析，文件里写了 `"nan"` 这类非标准值，行为取决于实现，别依赖
## 注意事项

- `json.load` 吃文件对象，`json.loads` 吃字符串，混用是最常见的报错。
- 文件不是合法 JSON 会抛 `json.JSONDecodeError`，报错里有位置提示。
- JSON 不允许注释和结尾多余的逗号，写的时候别当成 Python 字典。
- 中文想不被转义成 `\uXXXX`，写文件时加 `ensure_ascii=False`。

## 使用场景

- 读程序的配置文件。
- 处理接口返回的数据。
- 读取、修改、再写回结构化数据。
