---
id: py.sqlite.update_multi
title: 一次更新多列
description: 只发一条 SQL 就改好几个字段
language: python
category_id: programming.database
module: sqlite3
origin: stdlib
import: "import sqlite3"
qualname: "UPDATE ... SET a=?, b=?"
signature: 'cur.execute("UPDATE t SET a = ?, b = ? WHERE id = ?", (a, b, id))'
args:
  - name: "列和值"
    required: true
    accepts: "SET 后面写多组「列 = ?」，逗号分隔"
    nesting: "值全部用 ? 占位；列名不能占位"
  - name: "条件"
    required: true
    accepts: "WHERE 条件，通常按主键；忘写就是改全表"
    nesting: "条件值也用 ? 占位"
returns: "游标：cur.rowcount 是改了几行；要 commit 才落盘"
object:
  id: db.record
  name: 数据库记录
  aliases: [记录, 多列, 字段, 更新, record]
action:
  id: modify.change
  name: 修改
  aliases: [更新, 修改多列, 一起改, 批量更新, update]
targets: []
utterances:
  direct:
    - 一次更新多个字段
    - 同时改几列
    - update 多列怎么写
  questions:
    - 怎么用一条 SQL 更新多个字段
    - SET 后面多个列怎么写
    - 更新的值和条件一起传参怎么写
  colloquial:
    - 想一次把名字和城市都改了
    - 只改几个字段，其他别动
  technical:
    - UPDATE SET 多列
    - 参数顺序
    - 部分更新
  short_queries:
    - 更新多列
    - set
    - 部分更新
status: tested
tested_versions: ["3.10", "3.11", "3.12", "3.13", "3.14"]
min_version: "3.0"
version_note: "多列 UPDATE 是标准 SQL，SQLite 各版本支持"
sources:
  - Python 官方文档 sqlite3
  - SQLite 官方文档 UPDATE
---

# 一次更新多列

## 功能描述

输入「列 = ?」的多组赋值 + 条件，一条 SQL 改多个字段；**没写的列保持原值**。

## 推荐代码

```python
import sqlite3

con = sqlite3.connect(":memory:")
cur = con.cursor()
cur.execute("CREATE TABLE user (id INTEGER PRIMARY KEY, name TEXT, city TEXT, age INT)")
cur.execute("INSERT INTO user (name, city, age) VALUES (?, ?, ?)", ("张三", "沧州", 20))
con.commit()

cur.execute(
    "UPDATE user SET name = ?, city = ? WHERE id = ?",
    ("张三丰", "北京", 1),
)
print("改了", cur.rowcount, "行")
con.commit()
print(cur.execute("SELECT * FROM user").fetchone())   # age 还是 20
con.close()
```

## 语句解释

### SET name = ?, city = ?

多个赋值用逗号分隔，顺序必须和参数元组一致。

### 参数是一个扁平元组

`("张三丰", "北京", 1)` 按 `?` 出现的顺序一一对应。

### 没提的列不动

只写 name 和 city，`age` 保持原值——不是「整行覆盖」。

## 原理解释

**一句话：** 它按 `?` 出现的顺序，把参数一个个填进去，然后逐行判断条件再改指定列。

**执行逻辑：**

1. 解析 SQL，记下每个 `?` 的位置
2. 按顺序把参数填进这些位置
3. 逐行判断 `WHERE`：不满足跳过
4. 满足 → 只改 SET 里列出的列
5. 记下影响行数，等 `commit` 生效

**机器层（可跳过）：** 每改一行写一次日志，批量改比逐条改快。

**边界（从逻辑推出来）：**

- 第 2 步按出现顺序填，所以**参数顺序和 SET 顺序必须一致**，错位会静默改错值
- 第 4 步只改列出的列，所以它是「部分更新」，适合"只改用户改过的字段"
- 第 5 步之前可回滚
- 忘写 `WHERE` 就是改全表（第 3 步条件恒真）

## 注意事项

- 参数顺序必须和 `?` 顺序一致，错位不会报错、只会改错数据。
- 只改传进来的字段是特性，不要为了省事把所有列都写进 SET。
- 敏感字段（如更新时间）可以用 `CURRENT_TIMESTAMP` 让数据库填。
- 改完看 `rowcount` 确认真的改到了。

## 使用场景

- 表单只提交了部分字段（部分更新）。
- 批量修正同一类数据的几个字段。
- 更新状态 + 更新时间一起写。
