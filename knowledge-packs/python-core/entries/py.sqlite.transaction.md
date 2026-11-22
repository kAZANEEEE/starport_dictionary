---
id: py.sqlite.transaction
title: 事务处理
description: 一批操作要么全成功要么全回滚
language: python
category_id: programming.database
module: sqlite3
origin: stdlib
import: "import sqlite3"
qualname: "sqlite.transaction"

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

**一句话：** 先记账、后统一生效——中间任何一笔出错，前面记的全都作废。

**执行逻辑：**

1. 开始一个事务（第一句写操作时自动开启）
2. 每写一行，先写进「变更日志」，同时改内存里的数据
3. 如果中途出错 → `rollback()`：按日志把内存里的改动撤回，日志清掉
4. 如果全部成功 → `commit()`：把日志标记为已生效，改动正式落盘
5. 崩溃重启时，数据库会读日志，未提交的自动作废（这叫 WAL 恢复）

**机器层（可跳过）：** 一次提交只做一次磁盘同步，所以批量写比逐条提交快很多。

**边界（从逻辑推出来）：**

- 第 2、4 步之间有「未提交」的中间态，所以别人看不到你的改动
- 第 3 步能撤回的前提是有日志，所以事务期间磁盘不能用尽
- 第 4 步一次同步，逐条 `commit` 就是反复同步——慢十倍不夸张
- 事务开着会锁库，别人写不进去；长事务要拆
## 注意事项

- 批量写**不要逐条 commit**，包在一个事务里快得多。
- 出错一定要 `rollback()`，否则连接里会留着未提交的脏状态。
- 长事务会锁库，别人写不进去；导入大量数据时分批提交。
- 3.12 起 `with con:` 不再自动开事务，别依赖旧语义，显式 commit 最稳。

## 使用场景

- 批量导入数据。
- 转账式操作（扣一个、加一个）。
- 任何“要么全对要么全不算”的写操作。
