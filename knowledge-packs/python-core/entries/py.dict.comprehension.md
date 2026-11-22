---
id: py.dict.comprehension
title: 用推导式生成字典
description: 一行把两个列表配成字典，或筛选转换字典
language: python
category_id: programming.basics
module: dict
origin: builtin
import: ""
qualname: "dict 推导式 {k: v for ...}"
signature: "{键表达式: 值表达式 for 变量 in 来源 if 条件}"
args:
  - name: "键表达式"
    required: true
    accepts: "算出来当键的东西，必须可哈希"
    nesting: "可以，可以是切片、函数调用"
  - name: "值表达式"
    required: true
    accepts: "算出来当值的东西，什么类型都行"
    nesting: "可以，可以嵌套另一个推导式"
  - name: "条件"
    required: false
    default: "无"
    accepts: "只保留满足条件的项"
    nesting: "可以，可多个条件用 and"
returns: "字典：立刻构造好的完整字典；键重复时后面的覆盖前面的"
object:
  id: dict.value
  name: 字典值
  aliases: [字典, 键值对, 推导式, 生成字典, dict]
action:
  id: create.new
  name: 创建
  aliases: [生成字典, 批量创建, 推导, comprehension]
targets: []
utterances:
  direct:
    - 用推导式生成字典
    - 一行生成字典
    - 字典推导式怎么写
  questions:
    - 怎么用一行代码生成字典
    - 两个列表怎么变成一个字典
    - 字典推导式怎么加条件
  colloquial:
    - 想少写几行 for 循环建字典
    - 有一个名字列表和一个值列表，怎么配起来
  technical:
    - dict comprehension
    - 推导式
    - dict(zip(...))
  short_queries:
    - 字典推导式
    - 生成字典
    - comprehension
status: tested
tested_versions: ["3.10", "3.11", "3.12", "3.13", "3.14"]
min_version: "3.0"
version_note: "字典推导式从 2.7/3.0 起就有"
sources:
  - Python 官方教程 字典推导式
---

# 用推导式生成字典

## 功能描述

输入「键表达式 + 值表达式 + 来源」，输出一个新字典；可加条件筛掉不要的项。

## 推荐代码

```python
nums = [1, 2, 3]

print({n: n * n for n in nums})          # {1: 1, 2: 4, 3: 9}
print({n: n * n for n in nums if n > 1}) # {2: 4, 3: 9}

names = ["a", "b"]
ages = [1, 2]
print({k: v for k, v in zip(names, ages)})   # {'a': 1, 'b': 2}
print(dict(zip(names, ages)))                # 同样结果，更短
```

## 语句解释

### `{键: 值 for x in 来源}`

冒号左边算键、右边算值。整体结果是一个字典。

### 加 `if`

写在 `for` 后面，只保留满足条件的项。

### zip 配两个列表

`zip` 把两个列表配成对，再交给推导式或 `dict()` 直接变字典。

## 原理解释

**一句话：** 它一边遍历来源，一边算出「这一项的键和值」，塞进新字典。

**执行逻辑：**

1. 造一个空字典
2. 从来源取一个元素
3. 算键表达式、算值表达式
4. 把这对塞进字典（键已存在就**覆盖**旧值）
5. 重复 2–4 直到取完，返回字典

**机器层（可跳过）：** 每一项一次哈希插入，总开销与来源长度成正比。

**边界（从逻辑推出来）：**

- 第 4 步「键已存在就覆盖」，所以**后面的项赢**——这决定了重复键的处理结果
- 键必须可哈希，值无所谓
- 因为第 2 步按来源顺序走，3.7+ 结果字典的顺序与来源一致
- 它立刻建完整个字典，数据大时内存峰值等于结果大小

## 注意事项

- 键重复时保留最后一个，不是第一个。
- 键必须可哈希（列表不行）。
- 只是「两个等长列表配字典」用 `dict(zip(a, b))` 更短。
- 太复杂的推导式拆成循环更易读。

## 使用场景

- 建「名字 → 分数」的映射表。
- 从列表里挑出符合条件的项做索引。
- 把列表转成字典以便 O(1) 查找。
