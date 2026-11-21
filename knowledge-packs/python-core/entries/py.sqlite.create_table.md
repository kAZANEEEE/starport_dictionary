---
id: py.sqlite.create_table
title: 建表
description: 定义一张表的字段和类型，不存在就创建
language: python
category_id: programming.database
module: sqlite3

object:
  id: db.record
  name: 数据库记录
  aliases: [表, 表结构, 字段, 建表, table]

action:
  id: create.new
  name: 创建
  aliases: [建表, 创建表, 新建, create, table]

targets: []

utterances:
  direct:
    - 创建数据库表
    - 建一张表
    - 定义表结构
  questions:
    - 怎么在 sqlite 里建表
    - 如何定义自增主键
    - 表已经存在会报错吗
  colloquial:
    - 想存数据，先得有个表
    - 建表语句怎么写才不重复报错
  technical:
    - CREATE TABLE
    - IF NOT EXISTS
    - AUTOINCREMENT
    - PRIMARY KEY
  short_queries:
    - 建表
    - create table

status: tested
tested_versions: ["3.10", "3.11", "3.12", "3.13", "3.14"]
min_version: "3.0"
version_note: sqlite3 支持的 SQL 方言随 SQLite 版本走，标准写法通用
sources:
  - Python 官方文档 sqlite3
  - SQLite 官方文档 CREATE TABLE
---

# 建表

## 功能描述

输入表名 + 字段定义，创建一张表；用 `IF NOT EXISTS` 可重复执行不报错。

## 推荐代码

```python
import sqlite3

con = sqlite3.connect(":memory:")
cur = con.cursor()

cur.execute("""
    CREATE TABLE IF NOT EXISTS notes (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        title TEXT NOT NULL,
        created TEXT DEFAULT CURRENT_TIMESTAMP
    )
""")
cur.execute("INSERT INTO notes (title) VALUES (?)", ("第一条",))
con.commit()

print(cur.execute("SELECT id, title FROM notes").fetchall())
con.close()
```

## 语句解释

### INTEGER PRIMARY KEY

`INTEGER PRIMARY KEY` 在 SQLite 里就是自增主键，插入时不用给值。

### NOT NULL / DEFAULT

列约束。`DEFAULT CURRENT_TIMESTAMP` 让插入时不写时间也有值。

### IF NOT EXISTS

表已存在时跳过，不报错——**这条让建表语句可以放在程序启动时无条件执行**。

## 原理解释

SQLite 的表结构存在数据库文件里，执行 `CREATE TABLE` 就是写入元数据。
类型声明被 SQLite 弱化处理（它更接近动态类型），但 `INTEGER PRIMARY KEY` 是特殊语法，
会绑定到 rowid，所以能自增。

## 注意事项

- 不加 `IF NOT EXISTS`，第二次运行就抛 `OperationalError: table already exists`。
- 建表要 `commit()` 才算完（DDL 也是事务）。
- 改表结构比建表麻烦，字段尽量一次想清楚；后面加列用 `ALTER TABLE ... ADD COLUMN`。
- 主键用 `INTEGER PRIMARY KEY`，别用 `VARCHAR` 自增。

## 使用场景

- 程序启动时初始化 schema。
- 测试里建临时内存表。
- 迁移脚本里补新表。
