---
id: py.json.dumps
title: 转成 JSON 字符串
description: 把字典或列表变成 JSON 文本
language: python
category_id: programming.filesystem
module: json

object:
  id: json.object
  name: JSON 数据
  aliases: [json, 字典, 数据结构, json 文本, json data]

action:
  id: convert.transform
  name: 转换
  aliases: [转成 json, 序列化, 变成字符串, 输出 json, dumps, serialize]

targets: []

utterances:
  direct:
    - 转成 JSON 字符串
    - 字典转 JSON
    - 序列化数据
  questions:
    - 怎么把字典转成 json 字符串
    - 如何输出中文不乱码的 json
    - dumps 和 dump 有什么区别
  colloquial:
    - 想把结果拼成 json 发给别人
    - 存成 json 文本，中文别变乱码
  technical:
    - json.dumps
    - ensure_ascii
    - indent
    - sort_keys
  short_queries:
    - 序列化
    - dumps
    - 转 json

status: tested
tested_versions: ["3.10", "3.11", "3.12", "3.13", "3.14"]
min_version: "3.0"
version_note: json.dumps 参数稳定
sources:
  - Python 官方文档 json.dumps
---

# 转成 JSON 字符串

## 功能描述

输入字典/列表，输出 JSON 文本；要写文件用 `json.dump`（不带 s）。

## 推荐代码

```python
import json

data = {"name": "星港", "nums": [1, 2], "ok": True}

print(json.dumps(data, ensure_ascii=False))
print(json.dumps(data, ensure_ascii=False, indent=2))
print(json.dumps(data, ensure_ascii=False, sort_keys=True))
```

## 语句解释

### json.dumps(obj)

`dumps` = dump string，返回字符串。`dump` 是写到文件对象。

### ensure_ascii=False

**不加这个，中文会变成 `\u661f\u6e2f`**。人读的输出一定要加。

### indent=2

缩进美化，便于人看；机器传输一般不要，浪费字节。

### sort_keys=True

按键排序，方便对比两份 JSON 的差异。

## 原理解释

JSON 只支持有限的类型：对象、数组、字符串、数字、布尔、null。
`dumps` 会把 Python 的 dict/list/str/int/float/bool/None 映射过去；
遇到 `datetime`、`set`、自定义对象会抛 `TypeError`，需要 `default=` 提供转换函数。

## 注意事项

- 中文必须 `ensure_ascii=False`，否则全是转义序列。
- `datetime` 不能直接序列化，先 `.isoformat()`。
- 循环引用会抛 `ValueError: Circular reference detected`。
- 浮点数精度、NaN 在 JSON 里是非法值，要处理成 null。

## 使用场景

- 接口返回前把数据转 JSON。
- 写配置文件。
- 打印调试信息时格式化输出。
