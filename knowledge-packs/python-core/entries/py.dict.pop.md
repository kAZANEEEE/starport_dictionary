---
id: py.dict.pop
title: 取出并删除字典里的项
description: 拿走一个键的值，同时把它从字典里删掉
language: python
category_id: programming.basics
module: dict

object:
  id: dict.value
  name: 字典值
  aliases: [字典, 键值, 某一项, 元素, dict]

action:
  id: delete.remove
  name: 删除
  aliases: [取出并删除, 弹出, 拿走, 删除, pop]

targets: []

utterances:
  direct:
    - 取出并删除字典元素
    - 弹出字典的某一项
    - 删除字典的键
  questions:
    - 怎么取出值的同时删掉这个键
    - pop 键不存在会怎样
    - 怎么安全地删除字典项
  colloquial:
    - 拿走一个值，顺便从字典里去掉
    - 删之前还想知道原来是多少
  technical:
    - dict.pop
    - pop 默认值
    - del 语句
    - popitem
  short_queries:
    - pop
    - 弹出
    - 删除字典

status: tested
tested_versions: ["3.10", "3.11", "3.12", "3.13", "3.14"]
min_version: "3.0"
version_note: dict.pop / popitem / del 各版本一致
sources:
  - Python 官方文档 dict.pop
---

# 取出并删除字典里的项

## 功能描述

输入键（+ 可选默认值），输出它的值并从字典移除；键不存在时：给了默认值就返回默认值，没给就抛 `KeyError`。

## 推荐代码

```python
config = {"host": "127.0.0.1", "port": 8000, "debug": True}

host = config.pop("host")
print(host, config)          # 127.0.0.1 {'port': 8000, 'debug': True}

missing = config.pop("nope", "默认值")
print(missing)               # 默认值

key, value = config.popitem()   # 弹出最后一对
print(key, value)            # debug True

del config["port"]           # 只删不取值
print(config)
```

## 语句解释

### pop(键)

取出值并删除这个键。键不存在直接抛 `KeyError`。

### pop(键, 默认值)

键不存在时返回默认值，**不报错也不插入**。

### popitem()

删掉并返回「最后一对」`(键, 值)`；字典空时抛 `KeyError`。

### del d[键]

只删不取，键不存在同样抛 `KeyError`。

## 原理解释

**一句话：** 它先把值记下来，再把这个键从字典里抹掉，最后把值交给你。

**执行逻辑：**

1. 用键去哈希表里定位
2. 找到 → 把对应的值先存到临时变量
3. 把这个键值对从表里移除（表长度减 1）
4. 返回第 2 步存下的值
5. 没找到 → 有默认值就返回默认值（不动字典），没有就抛 `KeyError`

**机器层（可跳过）：** 哈希表删除是 O(1)，不需要像列表那样挪动元素。

**边界（从逻辑推出来）：**

- 第 3 步真的删除了，所以**取和删是一个原子动作**，不能只取不删
- 第 5 步「有默认值是安全的」：`pop(k, None)` 是「删掉 KeyError 风险」的标准写法
- 因为第 2 步已经拿到值，所以 `del` 那种「只要删」的场景用不上它
- 遍历字典时 `pop` 会让迭代器失效，抛 `RuntimeError`

## 注意事项

- `pop(k)` 键不存在抛 `KeyError`，不确定就用 `pop(k, None)`。
- 遍历字典时别 pop，先把要删的键收集起来再删。
- 想要「取出来但不删」用 `get` 或 `d[k]`。
- `popitem()` 是 LIFO（最后插入的先出），但依赖这个顺序写业务逻辑要谨慎。

## 使用场景

- 从配置里取出某个键，避免它继续向下传递。
- 队列/栈式的任务表（配合 `popitem`）。
- 删除前先记录原值（审计、日志）。
