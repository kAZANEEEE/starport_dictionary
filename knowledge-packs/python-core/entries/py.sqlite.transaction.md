---
id: py.sqlite.transaction
title: 事务处理
description: 一批操作要么全成功要么全回滚
language: python
category_id: programming.database
module: sqlite3

object:
  id: db.record
  name: 数据库记录
  aliases: [多条操作, 一批写入, 事务, 记录, record]

action:
  id: run.execute
  name: 执行
  aliases: [提交, 回滚, 执行事务, 一起执行, commit, rollback]

targets: []

utterances:
  direct:
    - 事务处理
    - 一批操作一起提交
    - 出错就全部回滚
  questions:
    - 怎么用事务保证要么全成功要么全失败
    - 多条插入怎么一起提交
    - Python sqlite 怎么回滚
  colloquial:
    - 中间出错前面那些也别留下
    - 想一次写很多条，成功才算数
  technical:
    - BEGIN
    - COMMIT
    - ROLLBACK
    - with connection
  short_queries:
    - 事务
    - commit
    - rollback

status: tested
tested_versions: ["3.10", "3.11", "3.12", "3.13", "3.14"]
min_version: "3.0"
version_note: sqlite3 的 with 语法在 3.6 前后语义有变化（3.12 起不再自动开事务），以显式 commit 为准
sources:
  - Python 官方文档 sqlite3 事务控制
---

# 事务处理

## 功能描述

把多条写操作打包：全部成功才 `commit()`，中途出错就 `rollback()`，数据库回到操作前。

## 推荐代码

```python
import sqlite3

con = sqlite3.connect(":memory:")
cur = con.cursor()
cur.execute("CREATE TABLE t (id INTEGER PRIMARY KEY, name TEXT)")
con.commit()

try:
    cur.execute("INSERT INTO t (name) VALUES (?)", ("a",))
    cur.execute("INSERT INTO t (name) VALUES (?)", ("b",))
    con.commit()          # 两条一起生效
except sqlite3.Error:
    con.rollback()        # 一起作废
    raise

print(cur.execute("SELECT name FROM t").fetchall())
con.close()
```

## 语句解释

### con.commit()

把当前事务里所有改动一次性落盘。

### con.rollback()

丢弃事务里所有改动，回到事务开始前。

### try / except 包住

这是手写事务的标准形状：中间任何一步抛错都走到 `rollback`，不会留下半截数据。

## 原理解释

SQLite 默认在第一条写语句时自动开事务，`commit` 结束它。事务保证**原子性**：
要么全部生效，要么全部无效——靠的是写前日志（journal/wal），崩溃后也能还原。

批量的好处不只是安全，还更快：一次提交 = 一次磁盘同步，
逐条 `commit` 等于反复刷盘，批量插入会慢十倍以上。

## 注意事项

- 批量写**不要逐条 commit**，包在一个事务里快得多。
- 出错一定要 `rollback()`，否则连接里会留着未提交的脏状态。
- 长事务会锁库，别人写不进去；导入大量数据时分批提交。
- 3.12 起 `with con:` 不再自动开事务，别依赖旧语义，显式 commit 最稳。

## 使用场景

- 批量导入数据。
- 转账式操作（扣一个、加一个）。
- 任何“要么全对要么全不算”的写操作。
