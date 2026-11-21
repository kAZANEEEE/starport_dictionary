---
id: py.dict.get
title: 取字典里的值
description: 安全地按键取值，键不存在时给默认值
language: python
category_id: programming.basics
module: dict

object:
  id: dict.value
  name: 字典值
  aliases: [字典, 键值, 某个键的值, 配置项, dict, key value]

action:
  id: get.obtain
  name: 获取
  aliases: [取, 拿到, 读取, 取值, 查, get]

targets: []

utterances:
  direct:
    - 取字典里的值
    - 按 key 取值
    - 从字典里拿数据
    - 安全地取字典值
  questions:
    - 怎么从字典里取一个值
    - 如何避免字典取值报 KeyError
    - 键不存在的时候怎么返回默认值
    - Python 怎么读字典里的某一项
  colloquial:
    - 这个 key 可能没有，别让它崩
    - 配置里取不到就用默认的
    - 想看看字典里那个字段是啥
  goal_based:
    - 读配置项时给默认值
    - 遍历一堆字典统计某个字段
  technical:
    - dict.get
    - dict[key]
    - KeyError
    - python dict default value
  short_queries:
    - 字典
    - 取值
    - get
    - key

status: tested
tested_versions: ["3.10", "3.11", "3.12", "3.13", "3.14"]
min_version: "3.0"
version_note: dict.get 的 (key, default) 参数各版本一致
sources:
  - Python 官方文档 dict.get
---

# 取字典里的值

## 功能描述

按键取值。`d[key]` 键不存在会报错，`d.get(key, 默认值)` 不会。

## 推荐代码

```python
config = {"name": "starport", "version": 1}

print(config["name"])              # starport
print(config.get("version"))       # 1
print(config.get("missing"))       # None
print(config.get("missing", 0))    # 0
print(config.get("name", "默认"))   # starport —— 键存在就用真实值
```

## 语句解释

### config["key"]

直接下标取值。**键不存在抛 `KeyError`**，程序会中断。

### .get("key")

键不存在返回 `None`，不报错。

### .get("key", 默认值)

第二个参数是兜底值。只有键**真的不存在**时才用，键存在但值是 `None` 时不生效。

## 原理解释

字典是哈希表：用键算哈希 → 找到槽位 → 比较键。平均 O(1)，和字典大小无关。
`d[k]` 找不到槽位就抛异常；`get` 是“找不到就返回兜底值”的同一个查找，
所以在性能上两者没有区别，差别只在失败时的行为。

## 注意事项

- `get` 的默认值只在**键缺席**时生效；值是 `None` 时不会替换成默认值。
- 想区分“没有这个键”和“值是 None”，用 `key in d` 先判断，或 `d.get(k, 哨兵)`。
- 嵌套字典要一层层取：`d.get("a", {}).get("b")`，直接 `d["a"]["b"]` 容易连挂两次。
- 取到的是引用：字典里存的可变对象被改了，原字典里的也会变。
- 遍历字典时不要增删键，会抛 `RuntimeError`。

## 使用场景

- 读配置、读接口返回的 JSON，字段可能缺。
- 聚合统计时给计数一个初值 0。
- 做参数默认值，避免一堆 if 判空。
