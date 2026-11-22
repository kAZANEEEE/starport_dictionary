---
id: py.dict.setdefault
title: 缺键时给个默认值
description: 一次性完成「查、没有就建」，常用来分组和计数
language: python
category_id: programming.basics
module: dict
origin: builtin
import: ""
qualname: "dict.setdefault"

object:
  id: dict.value
  name: 字典值
  aliases: [字典, 键值, 默认值, 分组桶, dict]

action:
  id: modify.change
  name: 修改
  aliases: [设置默认值, 没有就建, 分组, 初始化, setdefault]

targets: []

utterances:
  direct:
    - 缺键时给默认值
    - 用 setdefault 分组
    - 一次查有就返回没有就建
  questions:
    - 怎么做到「有就取、没有就建」
    - 不用 defaultdict 怎么分组
    - setdefault 和 get 区别
  colloquial:
    - 每次都要先判断再插，太啰嗦
    - 想边查边建，不想写两遍 key
  technical:
    - dict.setdefault
    - defaultdict 替代
    - 分组写法
  short_queries:
    - setdefault
    - 默认值
    - 分组

status: tested
tested_versions: ["3.10", "3.11", "3.12", "3.13", "3.14"]
min_version: "3.0"
version_note: dict.setdefault 各版本一致
sources:
  - Python 官方文档 dict.setdefault
---

# 缺键时给个默认值

## 功能描述

输入键 + 默认值，输出这个键的值：键存在原样返回，不存在就**写入默认值再返回**。

## 推荐代码

```python
groups = {}
for word in ["apple", "avocado", "banana"]:
    groups.setdefault(word[0], []).append(word)
print(groups)      # {'a': ['apple', 'avocado'], 'b': ['banana']}

counts = {}
for ch in "hello":
    counts[ch] = counts.setdefault(ch, 0) + 1
print(counts)      # {'h': 1, 'e': 1, 'l': 2, 'o': 1}
```

## 语句解释

### setdefault(键, 默认值)

键不存在 → 把默认值写进去并返回它；键存在 → 直接返回已有的值。

### 为什么能 .append()

因为返回的是**字典里那个列表本身**（引用），所以直接 append 就改到了桶里。

### 计数那种写法

`counts.setdefault(ch, 0) + 1` 取出旧值（没有就 0）加一，再赋回去。

## 原理解释

**一句话：** 它分两路——有就给你原来的，没有就先造一个放进去再给你。

**执行逻辑：**

1. 用键查字典
2. 查到 → 直接返回那个值，**默认值根本不会被用**
3. 查不到 → 把传进来的默认值写进字典
4. 返回这个默认值

**机器层（可跳过）：** 一次查找 + 可能的写入，与普通字典操作同价。

**边界（从逻辑推出来）：**

- 第 2 步说明默认值只在缺键时才生效；键存在但值是 `None`，照样返回 `None`
- 第 3 步写的是**你传进去的那个对象**，所以 `setdefault(k, [])` 每次调用都会新建一个空列表，不会共享
- 第 2 步返回的是字典里的引用，所以对它 `.append()` 会真的改到字典
- 每次调用都要先构造默认值参数，所以 `setdefault(k, [])` 会白造一个空列表（有小开销）

## 注意事项

- 默认值传可变对象时注意：**每次调用都会新建**，反而安全；但有人误以为共享。
- 判断键在不在用 `in`，不要用 `setdefault`——后者会真的写入。
- 频繁分组用 `defaultdict(list)` 更省心，`setdefault` 更显式。
- 别在循环里用 `setdefault(k, expensive())`，参数会先求值。

## 使用场景

- 按分类把元素塞进不同的桶。
- 手工计数（不用 Counter 时）。
- 建邻接表、建索引。
