---
id: py.sqlite.count_rows
title: 统计表里有多少行
description: 不用把数据全取出来就知道条数
language: python
category_id: programming.database
module: sqlite3
origin: stdlib
import: "import sqlite3"
qualname: "SELECT COUNT(*)"
signature: 'cur.execute("SELECT COUNT(*) FROM 表 WHERE 条件")'
args:
  - name: "表名 / 条件"
    required: false
    default: "整表"
    accepts: "表名必填；WHERE 条件可选，填了就只数符合条件的"
    nesting: "条件值用 ? 占位，不能把值拼进去"
returns: "游标：fetchone()[0] 就是行数（整数）；结果永远只有一行一列"
object:
  id: db.record
  name: 数据库记录
  aliases: [记录, 行数, 条数, 数量, record]
action:
  id: get.obtain
  name: 获取
  aliases: [统计, 数, 查询数量, 算条数, count]
targets: []
utterances:
  direct:
    - 统计表里有多少行
    - 查询记录条数
    - 数一下有多少条数据
  questions:
    - 怎么知道表里有多少条记录
    - COUNT(*) 会不会很慢
    - 怎么统计符合条件的有几条
  colloquial:
    - 想知道库里存了多少条
    - 只想看数量，不想把数据全取出来
  technical:
    - SELECT COUNT
    - fetchone
    - 带条件的计数
  short_queries:
    - 行数
    - count
    - 条数
status: tested
tested_versions: ["3.10", "3.11", "3.12", "3.13", "3.14"]
min_version: "3.0"
version_note: "COUNT 是 SQLite 语法；Python 侧只是 execute + fetchone"
sources:
  - Python 官方文档 sqlite3
  - SQLite 官方文档 聚合函数
---

# 统计表里有多少行

## 功能描述

输入表名（可带条件），输出行数；只返回一个数字，不把数据取出来。

## 推荐代码

```python
import sqlite3

con = sqlite3.connect(":memory:")
cur = con.cursor()
cur.execute("CREATE TABLE t (id INTEGER PRIMARY KEY, city TEXT)")
cur.executemany("INSERT INTO t (city) VALUES (?)", [("沧州",), ("北京",), ("沧州",)])
con.commit()

print(cur.execute("SELECT COUNT(*) FROM t").fetchone()[0])              # 3
print(cur.execute("SELECT COUNT(*) FROM t WHERE city = ?", ("沧州",)).fetchone()[0])  # 2
con.close()
```

## 语句解释

### SELECT COUNT(*)

数行数。`COUNT(*)` 数所有行，`COUNT(列)` 会跳过该列为 NULL 的行。

### fetchone()[0]

结果永远是一行一列，取第一个元素就是数字。

### 带 WHERE 的条件计数

只数符合条件的行；条件值仍然用 `?` 占位。

## 原理解释

**一句话：** 数据库自己数完行数，只把「几行」这一个数字给你，不把数据搬出来。

**执行逻辑：**

1. 解析 SQL，确定范围和条件
2. 逐行判断条件（没条件就每行都算）
3. 每通过一行就 +1
4. 扫完把总数作为一行一列返回

**机器层（可跳过）：** 没条件的 `COUNT(*)` SQLite 会走表结构信息，很快；带 WHERE 就要扫。

**边界（从逻辑推出来）：**

- 第 2 步带条件时要逐行判断，所以没索引的条件照样慢
- 第 4 步只返回一个数字，所以它比 `fetchall()` 再 `len()` 省内存——**别把整表取出来数**
- `COUNT(列)` 跳过 NULL，`COUNT(*)` 不跳，两者结果可能不同
- 结果是元组，必须 `[0]` 取值

## 注意事项

- 别用 `len(fetchall())` 数行数，数据大时内存会爆。
- `COUNT(*)` 和 `COUNT(某列)` 结果可能不一样（NULL 的行）。
- 带条件的计数要确信索引情况，否则大表会很慢。
- 空表返回 0，不是报错。

## 使用场景

- 分页时先拿总数算页数。
- 判断表空不空（`== 0`）。
- 统计某类数据的占比（两个 count 相除）。
