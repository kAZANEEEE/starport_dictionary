---
id: py.json.write
title: 把数据写成 JSON 文件
description: 字典存成 .json，中文不乱码
language: python
category_id: programming.filesystem
module: json
origin: stdlib
import: "import json"
qualname: "json.dump()"
signature: "json.dump(obj, 文件对象, ensure_ascii=False, indent=2)"
args:
  - name: "obj"
    required: true
    accepts: "字典、列表、数字、字符串、True/False/None"
    nesting: "可以，嵌套结构也支持"
  - name: "文件对象"
    required: true
    accepts: "用 open 打开的文件对象（不是路径）"
    nesting: "可以，常见写成 with open(p, \"w\", encoding=\"utf-8\") as f: json.dump(...)"
  - name: "ensure_ascii"
    required: false
    default: "True"
    accepts: "False = 中文原样写入（强烈建议）"
    nesting: "一般直接写 False"
  - name: "indent"
    required: false
    default: "None"
    accepts: "缩进空格数，给人看用 2"
    nesting: "一般直接写数字"
returns: "None：没有返回值；副作用是把 JSON 文本写进文件（会覆盖原内容）"
object:
  id: json.object
  name: JSON 数据
  aliases: [json, 配置文件, 数据文件, 写 json, json data]
action:
  id: create.new
  name: 创建
  aliases: [写入, 保存, 生成文件, 输出, dump]
targets: []
utterances:
  direct:
    - 把字典写成 JSON 文件
    - 保存配置成 json
    - 输出 json 文件
  questions:
    - 怎么把字典存成 json 文件
    - json.dump 和 dumps 有什么区别
    - 写出来的中文为什么是转义
  colloquial:
    - 想把配置存下来，下次读
    - 写出来的文件里中文变成 \u 了
  technical:
    - json.dump
    - ensure_ascii
    - indent
    - with open 写 json
  short_queries:
    - 写 json
    - dump
    - 保存配置
status: tested
tested_versions: ["3.10", "3.11", "3.12", "3.13", "3.14"]
min_version: "3.0"
version_note: "json.dump 各版本一致"
sources:
  - Python 官方文档 json.dump
---

# 把数据写成 JSON 文件

## 功能描述

输入 Python 对象 + 文件对象，把 JSON 文本写进文件；**`ensure_ascii=False` 才能保住中文**。

## 推荐代码

```python
import json
from pathlib import Path

config = {"名字": "星港", "版本": 1, "开启": True}

with open("config.json", "w", encoding="utf-8") as f:
    json.dump(config, f, ensure_ascii=False, indent=2)

print(Path("config.json").read_text(encoding="utf-8"))
```

## 语句解释

### json.dump(obj, 文件对象)

`dump` 吃**文件对象**（和 `dumps` 吃字符串的区别）。

### ensure_ascii=False

不加就写成 `\u661f\u6e2f`，人能看懂但不好读。

### with open(..., "w", encoding="utf-8")

`"w"` 是覆盖写；编码必须写，否则 Windows 上是 GBK。

## 原理解释

**一句话：** 它把对象转成 JSON 文本，边转边往文件里写，不先拼成一个大字符串。

**执行逻辑：**

1. 打开文件（`"w"` 模式，先清空）
2. 从对象最外层开始转：字典 → `{}`，列表 → `[]`
3. 逐个键值转成 JSON 片段写进文件
4. 中文看 `ensure_ascii`，决定原样写还是转义
5. 全部写完，关闭文件

**机器层（可跳过）：** 边转边写，所以对象很大也不至于拼出一整个巨字符串。

**边界（从逻辑推出来）：**

- 第 1 步 `"w"` 会先清空文件，所以写失败可能留下半个文件
- 第 2 步遇到 `datetime`、`set` 会报错，得自己先转成字符串/列表
- 第 4 步决定中文写法；**读回来时两种都能解析**，只是人看着不一样
- 因为吃文件对象，所以不能直接传路径：`json.dump(data, "a.json")` 会报错

## 注意事项

- 传的是文件对象，不是路径。
- `ensure_ascii=False` + `encoding="utf-8"` 两个一起写，中文才正常。
- 想生成紧凑文件（给机器读）就别加 `indent`。
- 写配置建议先写临时文件再替换，避免写坏后配置丢失。

## 使用场景

- 存用户配置、缓存结果。
- 导出数据给别的程序或人看。
- 程序重启后恢复状态。
