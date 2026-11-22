---
id: py.sqlite.drop_table
title: 删除表
description: 连结构带数据一起删掉，不可撤销
language: python
category_id: programming.database
module: sqlite3
origin: stdlib
import: "import sqlite3"
qualname: "DROP TABLE"
signature: 'cur.execute("DROP TABLE IF EXISTS 表名")'
args:
  - name: "表名"
    required: true
    accepts: "要删的表名；不能参数化，必须写进 SQL"
    nesting: "一般直接写字面量"
returns: "游标：没有返回值；副作用是整张表（结构和数据）消失，要 commit"
object:
  id: db.record
  name: 数据库记录
  aliases: [表, 表结构, 数据库表, 记录, table]
action:
  id: delete.remove
  name: 删除
  aliases: [删表, 删除表, 清空表, drop]
targets: []
utterances:
  direct:
    - 删除数据库表
    - 把表整个删掉
    - drop table 怎么用
  questions:
    - 怎么删除一张表
    - 删除表和清空表有什么区别
    - 表不存在会报错吗
  colloquial:
    - 这张表不要了，连结构一起删
    - 只是清空数据不删表怎么写
  technical:
    - DROP TABLE
    - DELETE FROM
    - IF EXISTS
  short_queries:
    - 删表
    - drop
    - 清空表
status: tested
tested_versions: ["3.10", "3.11", "3.12", "3.13", "3.14"]
min_version: "3.0"
version_note: "DROP TABLE 是 SQLite 语法，随 SQLite 版本走"
sources:
  - Python 官方文档 sqlite3
  - SQLite 官方文档 DROP TABLE
---

# 删除表

## 功能描述

输入表名，把整张表（结构 + 所有数据）从数据库删掉；只想清数据不删表用 `DELETE FROM 表`。

## 推荐代码

```python
import sqlite3

con = sqlite3.connect(":memory:")
cur = con.cursor()

cur.execute("CREATE TABLE tmp (id INTEGER PRIMARY KEY, name TEXT)")
cur.execute("INSERT INTO tmp (name) VALUES (?)", ("a",))
con.commit()

cur.execute("DROP TABLE IF EXISTS tmp")
con.commit()

# 表没了，再查会报错
try:
    cur.execute("SELECT * FROM tmp")
except sqlite3.OperationalError as exc:
    print("表已经不在了:", exc)
con.close()
```

## 语句解释

### DROP TABLE 表名

删除表结构 + 全部数据。

### IF EXISTS

表不存在时不报错，适合放在初始化脚本里反复执行。

### 和 DELETE FROM 的区别

`DELETE FROM t` 只清数据，表还在；`DROP TABLE t` 连表一起没。

## 原理解释

**一句话：** 它把这张表在数据库里的登记和所有数据页一起标记为可回收。

**执行逻辑：**

1. 在数据库元数据里找到这张表
2. 找不到 → 有 `IF EXISTS` 就跳过，没有就报错
3. 找到 → 把它的数据页全部标记为可复用
4. 删除表的定义（列、索引、约束一起没）
5. `commit()` 之后别的连接才看不到

**机器层（可跳过）：** 只改元数据 + 标记页面，所以很快；文件不会因此立刻变小。

**边界（从逻辑推出来）：**

- 第 4 步「索引、约束一起没」，所以建过的索引要重建
- 第 5 步之前可回滚，`commit` 之后不可撤销
- 因为只标记页面，删表后文件大小不变，需要 `VACUUM` 才回收
- 有外键引用它时会失败（如果开了外键约束）

## 注意事项

- `DROP TABLE` 不可撤销，重要数据先备份。
- 只想清空数据用 `DELETE FROM`（还能保留自增 id 的连续性和表结构）。
- 养成写 `IF EXISTS` 的习惯，脚本能重复执行。
- 删表后文件不变小是正常的。

## 使用场景

- 临时表用完清理。
- 迁移脚本里重建表结构（先 drop 再 create）。
- 测试用内存库，每次重建。
