---
id: py.sqlite.select
title: 查询数据库记录
description: 从表里按条件读出数据
language: python
category_id: programming.database
module: sqlite3

object:
  id: db.record
  name: 数据库记录
  aliases: [记录, 查询结果, 表数据, 行, record]

action:
  id: get.obtain
  name: 获取
  aliases: [查询, 读取, 取出, 查出, select, fetch]

targets: []

utterances:
  direct:
    - 查询数据库记录
    - 从表里读数据
    - 按条件查记录
  questions:
    - 怎么查询 sqlite 表里的数据
    - 如何按条件筛选记录
    - fetchall 和 fetchone 有什么区别
  colloquial:
    - 想把这个表里的东西读出来
    - 查一下符合条件的那些行
  technical:
    - SELECT
    - fetchall
    - fetchone
    - cursor execute
  short_queries:
    - 查询
    - select
    - fetchall

status: tested
tested_versions: ["3.10", "3.11", "3.12", "3.13", "3.14"]
min_version: "3.0"
version_note: sqlite3 查询接口稳定
sources:
  - Python 官方文档 sqlite3 查询
---

# 查询数据库记录

## 功能描述

输入 SQL + 参数，输出结果集；`fetchall` 全取、`fetchone` 取一条、`fetchmany(n)` 取 n 条。

## 推荐代码

```python
import sqlite3

con = sqlite3.connect(":memory:")
cur = con.cursor()
cur.execute("CREATE TABLE t (id INTEGER PRIMARY KEY, name TEXT)")
cur.executemany("INSERT INTO t (name) VALUES (?)", [("张三",), ("李四",)])
con.commit()

cur.execute("SELECT id, name FROM t WHERE name = ?", ("张三",))
print(cur.fetchone())

cur.execute("SELECT id, name FROM t ORDER BY id")
print(cur.fetchall())

con.close()
```

## 语句解释

### execute(SQL, 参数)

执行查询，结果留在游标里，需要 fetch 才拿到。

### fetchone()

取一条，返回元组；没有更多返回 `None`。

### fetchall()

取剩下全部，返回元组列表。数据大时占内存，循环里用 `for row in cur` 更好。

## 原理解释

游标是“结果集上的指针”：`execute` 之后结果集就绪，`fetch` 每次往前挪。
所以 `fetchone()` 连着调两次会拿到两条，不是同一条。

`for row in cur` 直接迭代游标，内部按行取，不会一次把结果全读进内存。

## 注意事项

- 在同一个游标上再 `execute` 会丢掉未取完的结果。
- `fetchall()` 对百万行会爆内存，用迭代或 `fetchmany`。
- 条件值用 `?` 占位，别拼字符串（防注入）。
- 结果默认是元组；要按列名取，设 `con.row_factory = sqlite3.Row`。

## 使用场景

- 展示列表数据。
- 按条件统计/导出。
- 读配置或缓存到内存里用。
