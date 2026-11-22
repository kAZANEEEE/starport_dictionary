---
id: py.json.get_nested
title: 安全地取嵌套字段
description: 接口返回层级很深，中间缺一层也不崩
language: python
category_id: programming.filesystem
module: json
origin: stdlib
import: "import json"
qualname: "链式 .get() 取嵌套字段"
signature: "d.get(\"a\", {}).get(\"b\", {}).get(\"c\", 默认值)"
args:
  - name: "字段名链"
    required: true
    accepts: "一层一层往里写的键名"
    nesting: "可以，任意深度，每层都配一个 .get(..., {}) 兜底"
returns: "取到的值；中间任一环缺失就一路返回默认值，不抛 KeyError"
object:
  id: json.object
  name: JSON 数据
  aliases: [json, 嵌套字段, 接口返回, 层级, json data]
action:
  id: get.obtain
  name: 获取
  aliases: [取, 安全取值, 逐层取, 读字段, get]
targets: []
utterances:
  direct:
    - 安全取嵌套字段
    - 取深层 json 字段
    - 中间缺字段也不报错
  questions:
    - 怎么取嵌套很深的 json 字段
    - 接口字段缺失怎么避免 KeyError
    - 链式 get 怎么写
  colloquial:
    - 接口有时候不返回那一层，直接取就崩了
    - 想取 a 里 b 里 c，某层没有就返回空
  technical:
    - 链式 get
    - 嵌套字典
    - 缺字段
    - 默认值兜底
  short_queries:
    - 嵌套取值
    - 安全取值
    - get 链
status: tested
tested_versions: ["3.10", "3.11", "3.12", "3.13", "3.14"]
min_version: "3.0"
version_note: "dict.get 各版本一致；写法只是组合调用"
sources:
  - Python 官方文档 dict.get
---

# 安全地取嵌套字段

## 功能描述

输入一串字段名，逐层往下取；**中间缺任何一层就返回兜底值，而不是抛异常**。

## 推荐代码

```python
resp = {"user": {"profile": {"city": "沧州"}}}

city = resp.get("user", {}).get("profile", {}).get("city", "未知")
print(city)     # 沧州

missing = resp.get("user", {}).get("nope", {}).get("city", "未知")
print(missing)  # 未知  ← 中间缺一层也不崩
```

## 语句解释

### 每层都要 `.get(..., {})`

兜底写 `{}`（空字典）而不是 `None`，因为下一层还要继续 `.get`，`None.get` 会崩。

### 最后一层给真正的默认值

`"未知"` 这种人类可读的兜底。

### 链式写法的代价

每层都调一次方法；层数多时不好读，可以考虑写个小函数递归取。

## 原理解释

**一句话：** 每一层都问「有这个键吗，没有就给我一个空字典继续问」，所以链不会断。

**执行逻辑：**

1. 在最外层字典里找第一个键
2. 找到 → 拿到值，继续第 3 步
3. 没找到 → 返回兜底的 `{}`，这时后面的 `.get` 都是空字典在应答
4. 一层层往下，直到最后一层取到值或触发兜底
5. 返回结果

**机器层（可跳过）：** 每层一次哈希查找，层数 × O(1)。

**边界（从逻辑推出来）：**

- 第 3 步兜底必须是**空字典**，写 `None` 会让下一步 `None.get` 抛 AttributeError
- 中间某一层的值是列表时不能继续 `.get`，需要先判断类型
- 它没法区分「键不存在」和「值是 None」，都在兜底里失效
- 深层嵌套多时链式写法可读性差，层数超过 3 建议写函数

## 注意事项

- 兜底写 `{}` 不是 `None`，否则下一层会崩。
- 遇到列表要另外处理（`[{...}]` 得先取 `[0]`）。
- 层数太多就写个 `deep_get(d, ["a", "b", "c"], default)` 函数。
- 调试时把中间结果打印出来，别一步到底。

## 使用场景

- 解析第三方接口返回（字段可能缺）。
- 读配置文件的分层设置。
- 处理爬到的结构不稳定的数据。
