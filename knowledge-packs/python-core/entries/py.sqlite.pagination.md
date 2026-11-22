---
id: py.sqlite.pagination
title: 分页查询
description: 一次只取一页，数据再多页不卡
language: python
category_id: programming.database
module: sqlite3
origin: stdlib
import: "import sqlite3"
qualname: "SELECT ... LIMIT ? OFFSET ?"
signature: 'cur.execute("SELECT * FROM t ORDER BY id LIMIT ? OFFSET ?", (每页几条, 跳过几条))'
args:
  - name: "LIMIT"
    required: true
    accepts: "这一页取几条"
    nesting: "可以，用 ? 占位传参数"
  - name: "OFFSET"
    required: true
    accepts: "跳过前面几条，公式 = (页码 - 1) × 每页条数"
    nesting: "可以，常写成变量"
returns: "游标：这一页的行；总页数要另算（用 COUNT(*) 除以每页条数）"
object:
  id: db.record
  name: 数据库记录
  aliases: [记录, 分页, 一页数据, 条数, record]
action:
  id: get.obtain
  name: 获取
  aliases: [查询, 分页查询, 取一页, 获取, paginate]
targets: []
utterances:
  direct:
    - 分页查询
    - 一次取一页
    - 查询第二页数据
  questions:
    - 怎么实现分页查询
    - LIMIT 和 OFFSET 怎么算
    - 分页为什么必须加 ORDER BY
  colloquial:
    - 数据太多，想一页页看
    - 翻页效果怎么用 SQL 做出来
  technical:
    - LIMIT OFFSET
    - 分页
    - ORDER BY
    - 深分页变慢
  short_queries:
    - 分页
    - limit
    - offset
status: tested
tested_versions: ["3.10", "3.11", "3.12", "3.13", "3.14"]
min_version: "3.0"
version_note: "LIMIT/OFFSET 是 SQLite 语法，各版本支持"
sources:
  - Python 官方文档 sqlite3
  - SQLite 官方文档 LIMIT
---

# 分页查询

## 功能描述

输入「每页几条 + 跳过几条」，输出这一页的数据；**必须配 `ORDER BY`**，否则每次翻页顺序都可能变。

## 推荐代码

```python
import sqlite3

con = sqlite3.connect(":memory:")
cur = con.cursor()
cur.execute("CREATE TABLE t (id INTEGER PRIMARY KEY, name TEXT)")
cur.executemany("INSERT INTO t (name) VALUES (?)", [(f"第{i}条",) for i in range(1, 8)])
con.commit()

page, size = 2, 3
offset = (page - 1) * size
rows = cur.execute(
    "SELECT id, name FROM t ORDER BY id LIMIT ? OFFSET ?", (size, offset)
).fetchall()
print(rows)          # 第 2 页：4、5、6
con.close()
```

## 语句解释

### LIMIT 每页条数

这一页最多给几条。

### OFFSET 跳过几条

公式：(页码 - 1) × 每页条数。第 1 页 offset 是 0。

### 必须写 ORDER BY

没有明确排序，数据库可以按任意顺序返回，翻页会重复或漏数据。

## 原理解释

**一句话：** 数据库按顺序数到第 offset 条，然后往后取 limit 条给你。

**执行逻辑：**

1. 按 `ORDER BY` 排好序
2. 从头数，跳过前 offset 条
3. 从第 offset + 1 条开始，取 limit 条
4. 返回这 limit 条

**机器层（可跳过）：** 跳过的行也要真的数一遍，所以 offset 很大时慢。

**边界（从逻辑推出来）：**

- 第 2 步「真要数一遍」解释了为什么**深分页（第 1 万页）很慢**——不是取慢，是跳慢
- 没有第 1 步的排序，第 2 步跳过的可能是任意行 → 翻页会重复/漏
- 最后一页可能不足 limit 条，这不算错
- 总页数要另算，SQL 不会告诉你

## 注意事项

- **一定写 ORDER BY**，且排序字段要唯一（否则并列时顺序不稳）。
- 深分页慢是结构性的，几万页时改用「记住上一页最后一个 id」的方式（`WHERE id > ? LIMIT ?`）。
- 总数用 `SELECT COUNT(*)` 单独查，别每次都取全表数。
- `OFFSET` 和 `LIMIT` 都能用 `?` 传参，别拼字符串。

## 使用场景

- 列表页翻页（第 N 页）。
- 分批导出数据。
- 大表按页展示，避免一次加载全部。
