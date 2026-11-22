---
id: py.sqlite.executemany
title: 批量插入数据
description: 一次插几百上千行，比循环 execute 快很多
language: python
category_id: programming.database
module: sqlite3
origin: stdlib
import: "import sqlite3"
qualname: "sqlite3.Cursor.executemany()"
signature: "cur.executemany(SQL, 参数序列)"
args:
  - name: "SQL"
    required: true
    accepts: '带 ? 占位符的插入语句，如 "INSERT INTO t (name) VALUES (?)"'
    nesting: "值不能拼进 SQL，只能占位"
  - name: "参数序列"
    required: true
    accepts: "一个可迭代对象，每项是一条记录对应的元组/列表；单值要写成 (v,)"
    nesting: "可以，常写成列表推导式或生成器"
returns: "游标：没有返回值可用；cur.rowcount 是插入了多少行（要 commit 才落盘）"
object:
  id: db.record
  name: 数据库记录
  aliases: [记录, 批量插入, 多条数据, 行, record]
action:
  id: create.new
  name: 创建
  aliases: [批量插入, 插入多条, 写入, 新增, executemany]
targets: []
utterances:
  direct:
    - 批量插入数据
    - 一次插入多行
    - executemany 怎么用
  questions:
    - 怎么一次性插入很多条
    - 循环 insert 太慢了怎么办
    - executemany 和 execute 区别
  colloquial:
    - 有一千条数据要存，一条条插太慢
    - 想批量写库
  technical:
    - executemany
    - 批量插入
    - 事务批量提交
  short_queries:
    - 批量
    - executemany
    - 插入多条
status: tested
tested_versions: ["3.10", "3.11", "3.12", "3.13", "3.14"]
min_version: "3.0"
version_note: "executemany 各版本一致"
sources:
  - Python 官方文档 sqlite3.Cursor.executemany
---

# 批量插入数据

## 功能描述

输入一条带占位符的 SQL + 一批参数，把每项参数各执行一次；**一次调用完成全部插入**。

## 推荐代码

```python
import sqlite3

con = sqlite3.connect(":memory:")
cur = con.cursor()
cur.execute("CREATE TABLE t (id INTEGER PRIMARY KEY, name TEXT)")

rows = [("张三",), ("李四",), ("王五",)]
cur.executemany("INSERT INTO t (name) VALUES (?)", rows)
con.commit()

print(cur.execute("SELECT COUNT(*) FROM t").fetchone()[0])   # 3
con.close()
```

## 语句解释

### executemany(SQL, 参数序列)

SQL 只解析一次，参数换着跑 N 次。这就是它比循环 `execute` 快的原因。

### rows 里每项是一个元组

单列记录也要写成 `("张三",)`，外面再套一层列表。

### 一次 commit

整批在一个事务里提交，等于只刷一次盘。

## 原理解释

**一句话：** 它把 SQL 先「编译」好，然后拿着这一份编译结果，把每条参数各填一遍。

**执行逻辑：**

1. 解析 SQL，编译成数据库能直接执行的形式（只做一次）
2. 从参数序列取第一条
3. 把值填进占位符，执行
4. 取下一条，重复 3
5. 全部执行完返回；这时还没落盘，要 `commit()`

**机器层（可跳过）：** 省掉的是「重复解析 SQL」和「重复开事务」两份开销。

**边界（从逻辑推出来）：**

- 第 1 步只解析一次，所以批量越大，相对循环 execute 的优势越明显
- 第 3 步逐条执行，**不是一条语句插 N 行**，所以中途某条违反约束会在此处抛错
- 第 5 步之前都在事务里，所以 `commit` 之前别人看不到
- 参数序列会被遍历一次，传生成器也能用（但用完就空了）

## 注意事项

- 一批别太大：几千条一次通常没问题，几十万条建议分批 commit。
- 单值元组的逗号不能少：`("张三",)`。
- 中途出错整批未提交，需要 `rollback()` 或直接放弃连接。
- 只是「多行数值一次插」还可以用多值语法 `VALUES (?),(?)`，但 executemany 更通用。

## 使用场景

- 导入 CSV/Excel 数据。
- 爬取结果批量落库。
- 造测试数据。
