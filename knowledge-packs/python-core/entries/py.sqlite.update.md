---
id: py.sqlite.update
title: 更新数据库记录
description: 改表里已有行的字段值
language: python
category_id: programming.database
module: sqlite3

object:
  id: db.record
  name: 数据库记录
  aliases: [记录, 行, 字段值, 数据, record]

action:
  id: modify.change
  name: 修改
  aliases: [更新, 改, 修改, 设置新值, update]

targets: []

utterances:
  direct:
    - 更新数据库记录
    - 修改表里的数据
    - 改某一行的字段
  questions:
    - 怎么更新 sqlite 表里的数据
    - 如何按条件改一条记录
    - 更新了但没生效是怎么回事
  colloquial:
    - 想把这条记录改一下
    - 数据错了，怎么改回来
  technical:
    - UPDATE SET WHERE
    - rowcount
    - 忘了 commit
  short_queries:
    - 更新
    - update

status: tested
tested_versions: ["3.10", "3.11", "3.12", "3.13", "3.14"]
min_version: "3.0"
version_note: sqlite3 UPDATE 与 rowcount 行为稳定
sources:
  - Python 官方文档 sqlite3 Cursor.rowcount
---

# 更新数据库记录

## 功能描述

输入表名、要改的字段、条件，更新匹配的行；返回没值，但 `cur.rowcount` 告诉你改了几行。

## 推荐代码

```python
import sqlite3

con = sqlite3.connect(":memory:")
cur = con.cursor()
cur.execute("CREATE TABLE t (id INTEGER PRIMARY KEY, name TEXT)")
cur.execute("INSERT INTO t (name) VALUES ('旧名字')")
con.commit()

cur.execute("UPDATE t SET name = ? WHERE id = ?", ("新名字", 1))
print("改了", cur.rowcount, "行")
con.commit()

print(cur.execute("SELECT name FROM t").fetchall())
con.close()
```

## 语句解释

### UPDATE t SET 字段 = ? WHERE 条件

`SET` 是要改成什么，`WHERE` 是改哪些行。**只用 `?`，不拼字符串**。

### cur.rowcount

受影响的行数。用来确认“到底改没改到”，改成 0 行通常意味着 `WHERE` 写错了。

### commit()

必须提交，否则改动只在当前连接事务里，别人看不到，关了可能丢。

## 原理解释

`UPDATE` 是逐行匹配 `WHERE` 再改字段。SQLite 支持事务：一条 `UPDATE` 改多行时，
要么全成功，要么全回滚——这正是事务的意义。

`rowcount` 是执行后由驱动报告的，对 `UPDATE`/`DELETE` 有效，对 `SELECT` 不可靠。

## 注意事项

- **忘记 `WHERE` 会改全表**，这是最危险的一类事故。
- 更新完不 `commit()`，数据等于没改。
- `rowcount == 0` 要当成异常信号排查，别默默放过。
- 字段名不能用 `?` 占位，只能放在 SQL 里（需要动态字段时用白名单校验）。

## 使用场景

- 修改用户资料、状态位。
- 批量修正某类数据。
- 标记已处理/已读。
