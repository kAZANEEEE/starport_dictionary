---
id: py.list.chunk
title: 把列表分批
description: 一次处理 N 个，分页和限流常用
language: python
category_id: programming.basics
module: list
origin: builtin
import: ""
qualname: "分批切片 items[i:i+n]"
signature: "[items[i:i + n] for i in range(0, len(items), n)]"
args:
  - name: "items"
    required: true
    accepts: "要分组的列表（或任何可切片的序列）"
    nesting: "可以"
  - name: "n"
    required: true
    accepts: "每批几个；最后一组可能不足 n"
    nesting: "一般直接写数字"
returns: "列表的列表：每项是一批；元素总数不变，最后一组可能短一些"
object:
  id: list.element
  name: 列表元素
  aliases: [列表, 分批, 分组, 每批, items]
action:
  id: convert.transform
  name: 转换
  aliases: [分批, 切成组, 分组, chunk]
targets: []
utterances:
  direct:
    - 把列表分批
    - 列表按 N 个一组
    - 分组处理列表
  questions:
    - 怎么把列表每 100 个分一组
    - 分批处理怎么写
    - 最后一组不足怎么办
  colloquial:
    - 一次处理太多会超时，想分批
    - 接口一次最多传 50 个，怎么拆
  technical:
    - 列表分批
    - range step
    - 切片分组
  short_queries:
    - 分批
    - 分组
    - chunk
status: tested
tested_versions: ["3.10", "3.11", "3.12", "3.13", "3.14"]
min_version: "3.0"
version_note: "切片 + range 步长写法各版本通用；3.12 起可用 itertools.batched"
sources:
  - Python 官方教程 range
  - Python 官方文档 itertools.batched
---

# 把列表分批

## 功能描述

输入列表 + 每批大小，输出一个「列表的列表」；最后一组不足时就是短的。

## 推荐代码

```python
items = list(range(7))
n = 3

chunks = [items[i:i + n] for i in range(0, len(items), n)]
print(chunks)      # [[0,1,2], [3,4,5], [6]]

for batch in chunks:
    print("处理一批:", batch)
```

## 语句解释

### range(0, len(items), n)

产生 0、3、6……这些起始下标。步长就是「每批几个」。

### items[i:i + n]

切片：从 i 开始取 n 个。**超出范围会自动截断**，所以最后一组不会报错。

### 3.12+ 的简写

`from itertools import batched`，然后 `batched(items, n)` 直接给分批。

## 原理解释

**一句话：** 用步长等于批大小的起点序列，每次从起点往后切一刀。

**执行逻辑：**

1. 算出列表长度
2. 起点从 0 开始，每次加 n
3. 用 `[起点, 起点+n)` 切片取出一批（越界自动截断）
4. 起点超过长度就停
5. 所有批次组成一个列表返回

**机器层（可跳过）：** 每批一次切片拷贝，总元素量不变，所以内存约等于原列表（是拷贝）。

**边界（从逻辑推出来）：**

- 第 3 步切片不越界报错，所以最后一组短一截也不会出错
- 第 5 步会拷贝出新列表，数据大时内存翻倍；只想遍历不建副本就用生成器写法
- 因为第 2 步用整数步长，`n` 必须是正整数，0 会死循环
- 它按**位置**分批，不按内容分组

## 注意事项

- `n` 必须 ≥ 1，写 0 会无限循环。
- 要省内存把方括号去掉，变成生成器表达式。
- 分批提交数据库/接口时，记得每批处理完再看是否需要停顿。
- 按内容分组不是这个，用 `defaultdict(list)` 或 `itertools.groupby`。

## 使用场景

- 批量调接口（每批 50 条）。
- 分批写数据库、分批上传。
- 分页展示数据。
