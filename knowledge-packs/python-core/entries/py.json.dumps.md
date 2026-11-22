---
id: py.json.dumps
title: 转成 JSON 字符串
description: 把字典或列表变成 JSON 文本
language: python
category_id: programming.filesystem
module: json
origin: stdlib
import: "import json"
qualname: "json.dumps"

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

**一句话：** 把 Python 的字典/列表翻译成一段文本，方便存或者传。

**执行逻辑：**

1. 看对象类型：字典 → 输出 `{}` 结构，列表 → 输出 `[]`
2. 逐个处理里面的值：字符串加引号并转义、数字原样、True/False/None → `true`/`false`/`null`
3. 遇到不认识的对象类型就停下并报错（除非你提供了转换函数）
4. 按 `indent` 决定要不要换行缩进
5. 拼成一整段字符串返回

**机器层（可跳过）：** 纯字符串拼接，不联网、不写文件。

**边界（从逻辑推出来）：**

- 第 2 步对中文默认做 `\uXXXX` 转义，所以要 `ensure_ascii=False` 才保持原样
- 第 3 步说明 `datetime`、`set`、自定义对象都不能直接转，得先自己换成字符串/列表
- 因为结果是一段文本，`dumps` 后再 `loads` 会得到**新对象**，和原来没有关联
- 循环引用的结构在第 2 步会无限递归，Python 会检测并报错
## 注意事项

- 中文必须 `ensure_ascii=False`，否则全是转义序列。
- `datetime` 不能直接序列化，先 `.isoformat()`。
- 循环引用会抛 `ValueError: Circular reference detected`。
- 浮点数精度、NaN 在 JSON 里是非法值，要处理成 null。

## 使用场景

- 接口返回前把数据转 JSON。
- 写配置文件。
- 打印调试信息时格式化输出。
