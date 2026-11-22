---
id: py.functools.lru_cache
title: 缓存函数结果
description: 同样的参数只算一次，后面直接拿缓存
language: python
category_id: programming.basics
module: functools
origin: stdlib
import: "from functools import lru_cache"
qualname: "functools.lru_cache"
signature: "@lru_cache(maxsize=None)"
args:
  - name: "maxsize"
    required: false
    default: "128"
    accepts: "最多缓存几条；None = 不限"
    nesting: "一般直接写 None 或数字"
returns: "装饰后的函数：参数相同直接返回上次结果；cache_info() 看命中情况"

object:
  id: cache.result
  name: 缓存
  aliases: [缓存, 计算结果, 中间结果, 记忆化, cache]

action:
  id: modify.change
  name: 修改
  aliases: [缓存, 记住结果, 加速, 加缓存, cache, memoize]

targets: []

utterances:
  direct:
    - 缓存函数结果
    - 给函数加缓存
    - 记忆化函数
  questions:
    - 怎么让函数记住算过的结果
    - 递归太慢怎么用缓存加速
    - lru_cache 和手写字典有什么区别
  colloquial:
    - 这个函数参数一样却算了很多遍
    - 想省掉重复计算
  technical:
    - functools.lru_cache
    - maxsize 参数
    - cache 装饰器
    - 缓存不命中
  short_queries:
    - 缓存
    - lru_cache
    - 记忆化

status: tested
tested_versions: ["3.10", "3.11", "3.12", "3.13", "3.14"]
min_version: "3.2"
version_note: lru_cache 从 3.2 起；3.9 起可直接用 @cache（无大小限制）
sources:
  - Python 官方文档 functools.lru_cache
---

# 缓存函数结果

## 功能描述

输入一个函数，输出「带记忆的同款函数」：参数相同就直接返回上次结果，不重新执行；`cache_info()` 能看到命中情况。

## 推荐代码

```python
from functools import lru_cache

@lru_cache(maxsize=None)
def fib(n: int) -> int:
    return n if n < 2 else fib(n - 1) + fib(n - 2)

print(fib(30))
print(fib.cache_info())   # hits 有值，说明缓存起作用了
```

## 语句解释

### @lru_cache(maxsize=None)

装饰器。`maxsize=None` = 不限条数；给数字（如 128）就是只保留最近用的 N 条。

### 装饰器做了什么

把原函数包起来：先查缓存，命中就返回，没命中才算并写入。原函数本身还在。

### cache_info()

返回 `hits`（命中次数）、`misses`（未命中）、`currsize`（当前缓存条数）。

## 原理解释

**一句话：** 它给函数配了一个小本子，调用前先翻本子，记过就直接给，没记过就真算一遍再记上。

**执行逻辑：**

1. 把这次调用的参数拼成「缓存键」
2. 去缓存里查这个键
3. 命中 → 直接返回存下的结果，**原函数体一行都不执行**
4. 没命中 → 真的调用原函数，拿到结果
5. 把「键 → 结果」写进缓存（超过上限就丢掉最久没用的），返回结果

**机器层（可跳过）：** 缓存就是一个字典 + 一条淘汰队列，查找 O(1)。

**边界（从逻辑推出来）：**

- 第 1 步要拼键，所以**参数必须能哈希**：传 list、dict 会直接报错
- 第 3 步返回的是**上次那个对象**，如果它是可变对象，被改过下次拿到的就是改后的样子
- 因为「参数相同就命中」，所以函数必须**纯**（只依赖参数）——依赖时间、文件、随机数会拿到过期结果
- 第 5 步有上限时会淘汰，所以不设 `maxsize` 在参数空间大时可能吃满内存
- 命中不执行函数体，所以里面的副作用（打印、写日志）也会被跳过

## 注意事项

- 参数必须可哈希；列表先转 `tuple`。
- 只给纯函数加缓存，别给「读文件/发请求」的函数加。
- 内存敏感时设 `maxsize`；`maxsize=None` 等于无限增长。
- 需要手动清空用 `func.cache_clear()`。

## 使用场景

- 递归的斐波那契、动态规划类计算。
- 解析同一个小文件的重复调用。
- 计算代价高、参数空间有限的函数。
