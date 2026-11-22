---
id: py.sqlite.executescript
title: 一次执行多条 SQL
description: 建表、插数据、建索引写在一个脚本里跑完
language: python
category_id: programming.database
module: sqlite3
origin: stdlib
import: "import sqlite3"
qualname: "sqlite3.Cursor.executescript()"
signature: "cur.executescript(多语句 SQL 文本)"
args:
  - name: "SQL 文本"
    required: true
    accepts: "包含多条语句的字符串，语句之间用分号分隔"
    nesting: "可以，常见从 .sql 文件读进来"
returns: "游标：没有返回值；副作用是里面每条语句都执行了（多条语句自动 commit）"
object:
  id: db.record
  name: 数据库记录
  aliases: [表结构, 多条语句, 建表脚本, 初始化, script]
action:
  id: run.execute
  name: 执行
  aliases: [执行, 一次跑完, 运行脚本, 初始化, script]
targets: []
utterances:
  direct:
    - 一次执行多条 SQL
    - 运行建表脚本
    - executescript 怎么用
  questions:
    - 怎么一次执行好几条语句
    - 从 sql 文件读出来怎么跑
    - executescript 会自动提交吗
  colloquial:
    - 手上一堆建表语句，想一次跑完
    - 初始化数据库的脚本怎么执行
  technical:
    - executescript
    - 多条语句
    - 自动 commit
    - 初始化 schema
  short_queries:
    - 多条 SQL
    - executescript
    - 建表脚本
status: tested
tested_versions: ["3.10", "3.11", "3.12", "3.13", "3.14"]
min_version: "3.0"
version_note: "executescript 各版本一致；它会在执行前先提交挂起的事务"
sources:
  - Python 官方文档 sqlite3.Cursor.executescript
---

# 一次执行多条 SQL

## 功能描述

输入一段含多条语句的 SQL 文本，逐条执行；**语句之间用分号分隔**。

## 推荐代码

```python
import sqlite3

con = sqlite3.connect(":memory:")
cur = con.cursor()

cur.executescript("""
CREATE TABLE IF NOT EXISTS user (id INTEGER PRIMARY KEY, name TEXT);
CREATE INDEX IF NOT EXISTS idx_user_name ON user(name);
INSERT INTO user (name) VALUES ('张三');
INSERT INTO user (name) VALUES ('李四');
""")

print(cur.execute("SELECT COUNT(*) FROM user").fetchone()[0])   # 2
con.close()
```

## 语句解释

### executescript(SQL 文本)

把整段文本交给数据库，按分号逐条执行。

### 适合初始化

建表、建索引、插初始数据，一个脚本就是一套 schema。

### 和 executemany 的区别

`executemany` 是「同一条语句跑很多组参数」；`executescript` 是「多条不同语句各跑一次」。

## 原理解释

**一句话：** 它把整段文本按分号切开，一条条交给数据库执行。

**执行逻辑：**

1. 先把当前挂起的事务提交掉
2. 按分号把文本切成多条语句
3. 逐条执行
4. 全部跑完

**机器层（可跳过）：** 每条语句一次解析执行，开销比单条循环小（省了多次 Python 层调用）。

**边界（从逻辑推出来）：**

- 第 1 步会**先提交**，所以之前没提交的改动会立刻落盘，回滚不了
- 第 2 步只按分号切，所以 SQL 字符串里含分号会切错（比如文本值里有 `;`）
- 第 3 步中途报错会停下，前面的语句**已经执行**（且已提交）
- 它不能用 `?` 占位符——脚本里没法传参

## 注意事项

- 要传参数就别用 `executescript`，改用 `execute` 循环。
- 它会先提交事务，别指望和之前的操作一起回滚。
- 文本值里有分号时要小心切分。
- 初始化脚本建议写成 `.sql` 文件，读进来执行。

## 使用场景

- 程序启动时初始化数据库结构。
- 执行升级/迁移脚本。
- 快速造测试库。
