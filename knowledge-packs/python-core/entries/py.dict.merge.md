---
id: py.dict.merge
title: 合并两个字典
description: 把另一个字典的键值合进来，重复键谁覆盖
language: python
category_id: programming.basics
module: dict

object:
  id: dict.value
  name: 字典值
  aliases: [字典, 键值对, 两个字典, 配置, dict]

action:
  id: modify.change
  name: 修改
  aliases: [合并, 合起来, 叠加, 覆盖, merge, update]

targets: []

utterances:
  direct:
    - 合并两个字典
    - 字典合并
    - 把字典内容加进去
  questions:
    - 怎么把两个字典合并成一个
    - 重复的键以哪个为准
    - Python 3.9 之后字典怎么合并
  colloquial:
    - 两份配置想合成一份
    - 后写的那个想盖掉前面的
  technical:
    - "dict.update"
    - "管道运算符 |"
    - "{**a, **b} 解包合并"
  short_queries:
    - 合并
    - merge
    - update

status: tested
tested_versions: ["3.10", "3.11", "3.12", "3.13", "3.14"]
min_version: "3.9"
version_note: dict 的 | 和 |= 从 3.9 起可用；update 各版本都有
sources:
  - Python 官方文档 dict.update
  - Python 3.9 更新说明（PEP 584）
---

# 合并两个字典

## 功能描述

输入两个字典，输出合并后的字典；**重复键以右边为准**。

## 推荐代码

```python
defaults = {"host": "127.0.0.1", "port": 8000}
override = {"port": 9000}

print({**defaults, **override})     # port 变成 9000
print(defaults | override)          # 3.9+，同样结果
print(defaults)

merged = dict(defaults)
merged.update(override)             # 原地改 merged，不返回新字典
print(merged)
print(defaults | override | {"debug": True})
```

## 语句解释

### {**a, **b}

解包再重建，返回新字典。顺序决定优先级，后面的覆盖前面的。

### a | b

3.9+ 的合并运算符，返回新字典；`a |= b` 是原地合并。

### dict.update(b)

**原地修改且返回 None**。写成 `merged = a.update(b)` 会得到 None。

## 原理解释

**一句话：** 把第二个字典的每一对搬进第一个，撞上同名键时后者盖前者。

**执行逻辑：**

1. 复制一份第一个字典（`{**a, **b}` / `a | b` 会新建；`update` 直接改原字典）
2. 从第二个字典里取一对键值
3. 看这个键在结果里有没有：没有就新增，有就把值**替换**掉
4. 重复 2–3 直到第二个字典取完
5. 交给你合并后的字典

**机器层（可跳过）：** 逐个键做一次哈希查找 + 写入，总开销与第二个字典的大小成正比。

**边界（从逻辑推出来）：**

- 第 3 步「替换」意味着**右边的值优先**，所以默认配置放左边、用户配置放右边
- 只搬第一层的键值，值是字典的话整个被替换，不会递归合并
- `update` 是原地改且返回 None，`{**a, **b}` 和 `|` 返回新字典
- 值显式写成 None 也算「有值」，照样覆盖掉默认值
## 注意事项

- `update` 原地改并返回 None，别赋值接收。
- 只合并一层，嵌套要自己写递归或用 `collections.ChainMap`。
- `|` 需要 3.9+，兼容老版本用 `{**a, **b}`。
- 合并配置时注意“空值覆盖”：显式传 `None` 也会覆盖掉默认值。

## 使用场景

- 默认配置 + 用户配置叠加。
- 汇总多个来源的统计结果。
- 合并接口返回的多个字段块。
