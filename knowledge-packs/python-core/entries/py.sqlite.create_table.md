---
id: py.sqlite.create_table
title: 建表
description: 定义一张表的字段和类型，不存在就创建
language: python
category_id: programming.database
module: sqlite3
origin: stdlib
import: "import sqlite3"
qualname: "sqlite.create_table"

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

**一句话：** 在数据库里登记一张新表：有哪些列、每列装什么类型、哪列是主键。

**执行逻辑：**

1. 检查这张表是否已存在（用了 `IF NOT EXISTS` 才会检查）
2. 不存在 → 把表结构写进数据库的元数据里
3. 已存在 → 什么都不做（没有 `IF NOT EXISTS` 就直接报错）
4. 表建好后还没有任何数据，只是个空壳

**机器层（可跳过）：** 改的是数据库文件里的结构信息，和写数据一样要提交。

**边界（从逻辑推出来）：**

- 第 1 步的检查是可选的，所以建表语句能不能重复执行，取决于你写没写 `IF NOT EXISTS`
- `INTEGER PRIMARY KEY` 是 SQLite 的特例：它绑定内部行号，插入时自动填，所以能当自增
- SQLite 的类型约束比较宽松，写了 `TEXT` 也能塞数字——别指望它帮你把关
- 建完表要 `commit()`（DDL 也在事务里）
## 注意事项

- 不加 `IF NOT EXISTS`，第二次运行就抛 `OperationalError: table already exists`。
- 建表要 `commit()` 才算完（DDL 也是事务）。
- 改表结构比建表麻烦，字段尽量一次想清楚；后面加列用 `ALTER TABLE ... ADD COLUMN`。
- 主键用 `INTEGER PRIMARY KEY`，别用 `VARCHAR` 自增。

## 使用场景

- 程序启动时初始化 schema。
- 测试里建临时内存表。
- 迁移脚本里补新表。
