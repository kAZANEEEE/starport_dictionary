---
id: py.sqlite.create_index
title: 给字段建索引
description: 让按这个字段查询变快，代价是写入变慢一点
language: python
category_id: programming.database
module: sqlite3
origin: stdlib
import: "import sqlite3"
qualname: "CREATE INDEX"
signature: 'cur.execute("CREATE INDEX IF NOT EXISTS 名字 ON 表(列)")'
args:
  - name: "名字"
    required: true
    accepts: "索引名，自己起，一般 idx_表_列"
    nesting: "不能参数化，必须写进 SQL"
  - name: "表(列)"
    required: true
    accepts: "在哪个表的哪个列上建索引；多列用逗号"
    nesting: "可以有多个列（复合索引，顺序有意义）"
returns: "游标：没有返回值；副作用是之后按这一列查询会快很多（要 commit）"
object:
  id: db.record
  name: 数据库记录
  aliases: [索引, 表, 字段, 查询加速, index]
action:
  id: create.new
  name: 创建
  aliases: [建索引, 加索引, 创建索引, index]
targets: []
utterances:
  direct:
    - 给字段建索引
    - 创建数据库索引
    - 让查询变快
  questions:
    - sqlite 怎么建索引
    - 索引为什么能让查询变快
    - 索引会影响写入速度吗
  colloquial:
    - 查询越来越慢了，是不是该加索引
    - 每次查 name 都要扫全表
  technical:
    - CREATE INDEX
    - 复合索引
    - EXPLAIN QUERY PLAN
  short_queries:
    - 索引
    - create index
    - 加速
status: tested
tested_versions: ["3.10", "3.11", "3.12", "3.13", "3.14"]
min_version: "3.0"
version_note: "CREATE INDEX 是 SQLite 语法，随 SQLite 版本走；IF NOT EXISTS 一直支持"
sources:
  - Python 官方文档 sqlite3
  - SQLite 官方文档 CREATE INDEX
---

# 给字段建索引

## 功能描述

输入表名 + 列名，建立一个「值的排好序的对照表」，之后按这列查询不用扫全表。

## 推荐代码

```python
import sqlite3

con = sqlite3.connect(":memory:")
cur = con.cursor()
cur.execute("CREATE TABLE user (id INTEGER PRIMARY KEY, name TEXT, city TEXT)")

cur.execute("CREATE INDEX IF NOT EXISTS idx_user_city ON user(city)")
cur.executemany("INSERT INTO user (name, city) VALUES (?, ?)",
                [("张三", "沧州"), ("李四", "北京"), ("王五", "沧州")])

print(cur.execute("SELECT name FROM user WHERE city = ?", ("沧州",)).fetchall())
print(cur.execute("EXPLAIN QUERY PLAN SELECT name FROM user WHERE city = ?", ("沧州",)).fetchall())
con.close()
```

## 语句解释

### CREATE INDEX 名字 ON 表(列)

建立索引。`IF NOT EXISTS` 让语句可以重复执行。

### EXPLAIN QUERY PLAN

看数据库**打算怎么执行**这条查询：用了索引会写 `USING INDEX`。

### 复合索引 (a, b)

两列一起建索引，对「a = ? AND b = ?」和「a = ?」有效，但对「只要 b」帮助不大。

## 原理解释

**一句话：** 索引就是按这一列的值排好序、并记着每行在哪的一张「目录」，查的时候先去目录找。

**执行逻辑（查询时）：**

1. 看到 `WHERE city = ?`
2. 有索引 → 在索引里二分查找这个值，拿到对应行的位置
3. 按位置把行取出来
4. 没索引 → 从表头开始一行行比对，直到扫完

**机器层（可跳过）：** 索引本身是一棵 B 树（一种排好序的多叉树），查找是 O(log n)。

**边界（从逻辑推出来）：**

- 第 2 步靠「排好序」才能二分，所以索引在**写入时要维护顺序**——插入/更新会变慢一点
- 因为索引存的是「值 → 行位置」，所以它占额外空间
- 复合索引的顺序有意义：`(a, b)` 不能替代 `(b)` 单独查询
- 对很小的表，扫全表可能比走索引还快，数据库自己会判断

## 注意事项

- 索引不是越多越好：每个索引都让写入更慢、占更多空间。
- 只在**经常用它查询/排序**的列上建。
- 建完索引要 `commit()`。
- 用 `EXPLAIN QUERY PLAN` 验证真的走了索引，别凭感觉。

## 使用场景

- 经常按某字段查（用户名、城市、状态）。
- 大表按时间范围查询。
- 频繁排序的字段。
