---
id: py.collections.defaultdict
title: 带默认值的字典
description: 访问不存在的键时自动建一个，省掉判空
language: python
category_id: programming.basics
module: collections
origin: stdlib
import: "from collections import Counter, defaultdict"
qualname: "collections.defaultdict"

object:
  id: dict.value
  name: 字典值
  aliases: [字典, 键值, 计数表, 分组, defaultdict]

action:
  id: create.new
  name: 创建
  aliases: [自动创建默认值, 初始化, 分组, 建表, default]

targets: []

utterances:
  direct:
    - 带默认值的字典
    - 访问不到就自动创建
    - 用 defaultdict 分组
  questions:
    - 怎么让字典取值时不报错还自动建
    - 如何按条件把元素分组到字典
    - defaultdict 和 get 有什么区别
  colloquial:
    - 每次都要判断 key 在不在，太烦了
    - 想把数据按类型塞进不同的桶
  technical:
    - collections.defaultdict
    - default_factory
    - 分组 groupby 替代
  short_queries:
    - defaultdict
    - 默认值
    - 分组

status: tested
tested_versions: ["3.10", "3.11", "3.12", "3.13", "3.14"]
min_version: "3.0"
version_note: defaultdict 各版本稳定
sources:
  - Python 官方文档 collections.defaultdict
---

# 带默认值的字典

## 功能描述

输入「默认值工厂」，输出一个字典：读不存在的键时**自动建一个默认值并写回字典**，所以能直接 `d[k].append(x)`。

## 推荐代码

```python
from collections import defaultdict

groups = defaultdict(list)
for word in ["apple", "avocado", "banana"]:
    groups[word[0]].append(word)
print(dict(groups))     # {'a': ['apple', 'avocado'], 'b': ['banana']}

counts = defaultdict(int)
for ch in "hello":
    counts[ch] += 1
print(dict(counts))     # {'h': 1, 'e': 1, 'l': 2, 'o': 1}
```

## 语句解释

### defaultdict(list)

默认值工厂是 `list`，缺键时自动建一个**空列表**。

### defaultdict(int)

`int()` 返回 0，所以缺键时得 0，可以直接 `+= 1` 计数。

### dict(groups)

转成普通字典，打印和比较时更干净（否则显示成 `defaultdict(<class 'list'>, ...)`）。

## 原理解释

**一句话：** 它在「查不到」的那一刻，先按你给的工厂造一个默认值、顺手存进去，然后再把它交给你。

**执行逻辑：**

1. 用键去查
2. 查到 → 返回值
3. 查不到 → 调用「默认值工厂」造一个新值
4. **把这个新值写进字典**（所以下次就在了）
5. 返回它

**机器层（可跳过）：** 第 3 步就是调一次 `list()` / `int()` / `set()`，开销与工厂的代价相同。

**边界（从逻辑推出来）：**

- 第 4 步会**真的写入**，所以「只是读一下」也会让字典变大——这是它和 `get` 最本质的区别
- `get` 不写回，只返回默认值，所以 `d[k].append(x)` 用 `get` 会失败（拿到的是临时空列表）
- 工厂必须是**可调用对象**（`list`/`int`/`set`/`lambda: 0`），写 `defaultdict([])` 会报错
- 因为第 1 步是标准字典查找，性能与普通字典相同

## 注意事项

- 别用 `defaultdict(list)` 判「键在不在」——`k in d` 不会触发工厂，但 `d[k]` 会。
- 工厂写类名不写实例：`list` 不是 `list()`。
- 需要序列化/比较时转成普通 `dict`。
- 想「缺键时返回默认值但**不要**写回」，用 `get`。

## 使用场景

- 按首字母/类型把元素分组。
- 词频、字符频统计。
- 构建「节点 → 邻居列表」的图结构。
