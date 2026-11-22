---
id: py.json.loads
title: 从字符串解析 JSON
description: 接口返回的一串 JSON 文本，直接变成字典
language: python
category_id: programming.filesystem
module: json
origin: stdlib
import: "import json"
qualname: "json.loads"
signature: "json.loads(字符串)"
args:
  - name: "字符串"
    required: true
    accepts: "一段 JSON 文本（单引号/注释都非法）"
    nesting: "可以，常见是接口返回的文本"
returns: "dict / list / 数字 / 字符串：解析结果；格式不对抛 JSONDecodeError"

object:
  id: json.object
  name: JSON 数据
  aliases: [json, json 文本, 接口返回, 字符串, json data]

action:
  id: convert.transform
  name: 转换
  aliases: [解析, 转成字典, 反序列化, 变成对象, loads, parse]

targets: []

utterances:
  direct:
    - 从字符串解析 JSON
    - JSON 文本转字典
    - 把接口返回的 json 解析出来
  questions:
    - 怎么把 json 字符串变成字典
    - loads 和 load 有什么区别
    - 解析失败报什么错
  colloquial:
    - 请求回来的那串文本怎么用
    - 这串花括号怎么变成能取值的对象
  technical:
    - json.loads
    - JSONDecodeError
    - json 与 dict 区别
  short_queries:
    - 解析
    - loads
    - json 解析

status: tested
tested_versions: ["3.10", "3.11", "3.12", "3.13", "3.14"]
min_version: "3.0"
version_note: json.loads 各版本一致；错误类型 3.5 起是 JSONDecodeError
sources:
  - Python 官方文档 json.loads
---

# 从字符串解析 JSON

## 功能描述

输入一段 JSON 文本，输出对应的 Python 对象（dict / list）；格式不合法抛 `JSONDecodeError`。

## 推荐代码

```python
import json

text = '{"name": "starport", "nums": [1, 2], "ok": true}'
data = json.loads(text)

print(data["name"])       # starport
print(data["nums"][1])    # 2
print(data["ok"] is True) # True —— JSON 的 true 变成了 Python 的 True

print(json.loads("123"))       # 123
print(json.loads('"hi"'))      # hi
```

## 语句解释

### json.loads(字符串)

`s` = string。吃字符串，返回 Python 对象。

### 与 json.load 的区别

`load` 吃**文件对象**（配合 `open`），`loads` 吃**字符串**。

### 类型映射

JSON 对象 → dict，数组 → list，`true/false` → `True/False`，`null` → `None`。

## 原理解释

**一句话：** 它从第一个字符开始读，看到什么结构就造什么 Python 对象，一层层套起来。

**执行逻辑：**

1. 跳过空白，读第一个非空字符
2. 是 `{` → 开始读一个字典：读键（字符串）、冒号、值，遇到 `}` 结束
3. 是 `[` → 开始读列表：逐个读值，遇到 `]` 结束
4. 遇到数字/字符串/`true`/`false`/`null` → 直接转成对应的 Python 值
5. 顶层读完还剩下别的字符（除空白）→ 报错

**机器层（可跳过）：** 纯文本解析，不联网、不读其他文件。

**边界（从逻辑推出来）：**

- 第 2、3 步要求严格配对，多一个逗号、少一个括号都会失败
- 第 5 步说明它允许开头结尾有空白，但**不允许正文里多出内容**（比如两段 JSON 拼在一起）
- JSON 里没有注释，写了 `//` 会解析失败——这是「我手写的配置怎么报错」的常见原因
- 解析出来的都是**新对象**，和原字符串无关，改了不会回写
- 单引号不是合法 JSON：`{'a': 1}` 会失败，必须双引号

## 注意事项

- 单引号、尾逗号、注释都不是合法 JSON——那是 Python 字面量的习惯。
- 解析外部数据一定包 `try`，别假设对方格式永远对。
- 中文一般没问题（`loads` 接受 `\uXXXX` 也能读原文）；写的时候才需要注意 `ensure_ascii`。
- 大数字会变 `int`，但精度敏感的（金额、ID 超过 2^53）建议当字符串传。

## 使用场景

- 解析 HTTP 接口返回的 JSON。
- 读命令行传进来的一段 JSON。
- 处理消息队列里的 JSON 消息。
