---
id: py.sqlite.delete
title: 删除数据库记录
description: 按条件删掉表里的行
language: python
category_id: programming.database
module: sqlite3

object:
  id: db.record
  name: 数据库记录
  aliases: [记录, 行, 数据, 表记录, record]

action:
  id: delete.remove
  name: 删除
  aliases: [删除, 删掉, 清除, 移除, delete]

targets: []

utterances:
  direct:
    - 删除数据库记录
    - 删掉表里的某行
    - 按条件删除数据
  questions:
    - 怎么删除 sqlite 表里的数据
    - 如何按 id 删一条记录
    - 删除后能恢复吗
  colloquial:
    - 这条数据不要了，删掉
    - 想把过期的记录清掉
  technical:
    - DELETE FROM WHERE
    - TRUNCATE 替代
    - rowcount
  short_queries:
    - 删除
    - delete

status: tested
tested_versions: ["3.10", "3.11", "3.12", "3.13", "3.14"]
min_version: "3.0"
version_note: sqlite3 DELETE 行为稳定；VACUUM 需要单独执行
sources:
  - Python 官方文档 sqlite3
---

# 删除数据库记录

## 功能描述

输入表名 + 条件，删除匹配的行；删空整表用 `DELETE FROM t`（不加 WHERE）。

## 推荐代码

```python
import sqlite3

con = sqlite3.connect(":memory:")
cur = con.cursor()
cur.execute("CREATE TABLE t (id INTEGER PRIMARY KEY, name TEXT)")
cur.executemany("INSERT INTO t (name) VALUES (?)", [("a",), ("b",), ("c",)])
con.commit()

cur.execute("DELETE FROM t WHERE name = ?", ("b",))
print("删了", cur.rowcount, "行")
con.commit()

print(cur.execute("SELECT name FROM t").fetchall())
con.close()
```

## 语句解释

### DELETE FROM t WHERE 条件

删匹配行。`WHERE` 省略就是清空整张表。

### cur.rowcount

删掉的行数，0 表示没匹配到——用来确认条件对不对。

### DELETE 之后的空间

SQLite 不会自动还空间给系统，文件大小不会立刻变小。

## 原理解释

**一句话：** 按条件把行标成「不要了」，提交之后它们就查不到了。

**执行逻辑：**

1. 解析 SQL，确定表名和删除条件
2. 逐行判断 `WHERE`：不满足跳过
3. 满足 → 把这一行从表里去掉（数据文件里的空间暂时不还）
4. 记下删了几行（`rowcount`）
5. `commit()` 之后别的连接才看不到这些行

**机器层（可跳过）：** 删除只是把页面标记为可复用，文件大小不变；要还空间得 `VACUUM`。

**边界（从逻辑推出来）：**

- 第 2 步没写 `WHERE` 就是清空整表——最典型的误操作
- 第 3 步标记删除而非擦除，所以理论上还能从文件里被恢复，敏感数据要覆写
- 删除大量数据后文件不变小，这是第 3 步的后果
- 开着外键约束时，子表还引用着就删不掉（第 3 步会失败）
## 注意事项

- **忘了 `WHERE` 就是清空全表**，误操作前先 `SELECT` 验证一下条件。
- 删除不可撤销（没备份就没了），重要表建议软删除（加 `deleted_at` 字段）。
- 删大量数据后文件不变小，需要 `VACUUM`。
- 外键约束开启时删主表记录会被拦，先删子表。

## 使用场景

- 清理过期数据。
- 用户删除自己的记录。
- 测试结束后清表。
