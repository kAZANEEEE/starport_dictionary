---
id: py.sqlite.row_factory
title: 查询结果按列名取值
description: 让 sqlite 返回「能按字段名取」的行，而不是裸元组
language: python
category_id: programming.database
module: sqlite3
origin: stdlib
import: "import sqlite3"
qualname: "sqlite3.Row"

object:
  id: db.record
  name: 数据库记录
  aliases: [查询结果, 记录行, 字段名, 列名, row]

action:
  id: convert.transform
  name: 转换
  aliases: [改成字典, 按列名取值, 转换, 包装, row_factory]

targets: []

utterances:
  direct:
    - 让查询结果按列名取值
    - sqlite 返回字典
    - 用字段名访问查询结果
  questions:
    - row_factory 怎么用
    - 查询结果只有元组，怎么按名字取
    - sqlite3.Row 能转成字典吗
  colloquial:
    - 每次都要记住第几列，太容易错
    - 想用 row["name"] 这种写法
  technical:
    - sqlite3.Row
    - row_factory
    - dict(row)
    - 列名访问
  short_queries:
    - row_factory
    - 列名
    - sqlite 字典

status: tested
tested_versions: ["3.10", "3.11", "3.12", "3.13", "3.14"]
min_version: "3.0"
version_note: "sqlite3.Row 各版本一致"
sources:
  - Python 官方文档 sqlite3.Row
---

# 查询结果按列名取值

## 功能描述

输入连接（设置 `row_factory`），输出「既能下标、又能按列名取」的行对象；`dict(row)` 可转普通字典。

## 推荐代码

```python
import sqlite3

con = sqlite3.connect(":memory:")
con.row_factory = sqlite3.Row          # 关键这一行
cur = con.cursor()
cur.execute("CREATE TABLE t (id INTEGER PRIMARY KEY, name TEXT)")
cur.execute("INSERT INTO t (name) VALUES (?)", ("张三",))
con.commit()

row = cur.execute("SELECT id, name FROM t").fetchone()
print(row["name"])          # 张三 —— 按列名取
print(row[1])               # 张三 —— 还能按下标
print(dict(row))            # {'id': 1, 'name': '张三'}
print(row.keys())           # ['id', 'name']
con.close()
```

## 语句解释

### con.row_factory = sqlite3.Row

给连接设置「结果行工厂」，之后所有查询返回的行都变成 `Row` 对象。

### row["name"]

按列名取值；拼错列名会抛 `IndexError`（不是 `KeyError`，这点容易混）。

### dict(row)

转成普通字典，方便 `json.dumps` 或放进模板。

## 原理解释

**一句话：** 默认每行是裸元组，`Row` 给它加一张「列名→下标」的对照表，让名字也能取值。

**执行逻辑：**

1. 执行查询，数据库返回列名列表和每行的值
2. 默认工厂直接造元组；`Row` 工厂额外记下列名和它们的顺序
3. 取 `row["name"]` 时，先在列名里找到下标，再去元组里取值
4. `dict(row)` 逐列把「列名→值」拷成字典

**机器层（可跳过）：** 每行多存一份列名引用，几乎没有额外开销。

**边界（从逻辑推出来）：**

- 第 2 步依赖「列名列表」，所以 `SELECT *` 的字段顺序变化会让按名取值依然安全、按下标取值可能错位
- 第 3 步先找下标，所以列名拼错时报的是 `IndexError`
- `Row` 仍然支持下标和 `len()`，所以旧代码不会坏
- `dict(row)` 是拷贝，改字典不会影响行对象

## 注意事项

- `row["不存在"]` 抛 `IndexError`，不是 `KeyError`——写 try 时注意异常类型。
- 设了 `row_factory` 之后所有查询都变，别忘了这是连接级设置。
- 要直接序列化成 JSON，先 `dict(row)`。
- 用 `SELECT *` 时列顺序不稳定，按名取值最安全。

## 使用场景

- 查询结果字段多，按下标取容易错位。
- 把行直接塞进模板/JSON。
- 需要「列名 + 值」一起遍历时。
