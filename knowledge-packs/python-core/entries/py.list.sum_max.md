---
id: py.list.sum_max
title: 求和 / 最大 / 最小
description: 一行算出总和、最大值、最小值
language: python
category_id: programming.basics
module: builtins

object:
  id: list.element
  name: 列表元素
  aliases: [列表, 数字, 元素, 一组数, items]

action:
  id: get.obtain
  name: 获取
  aliases: [求和, 求最大, 求最小, 算总和, sum, max, min]

targets: []

utterances:
  direct:
    - 求列表的和
    - 找最大值最小值
    - 计算总和
  questions:
    - 怎么求列表所有元素的和
    - 如何找最大值的下标
    - 空列表求最大值会怎样
  colloquial:
    - 这一列数加起来是多少
    - 哪个最大，排第几
  technical:
    - sum
    - max
    - min
    - index of max
    - 空序列 ValueError
  short_queries:
    - 求和
    - 最大
    - 最小
    - sum

status: tested
tested_versions: ["3.10", "3.11", "3.12", "3.13", "3.14"]
min_version: "3.0"
version_note: sum 的 start 参数、max/min 的 key 参数各版本一致
sources:
  - Python 官方文档 sum
  - Python 官方文档 max
---

# 求和 / 最大 / 最小

## 功能描述

输入一组数，输出总和 / 最大值 / 最小值；**空序列求 sum 得 0，求 max/min 抛 `ValueError`**。

## 推荐代码

```python
nums = [3, 1, 4, 1, 5]

print(sum(nums))            # 14
print(max(nums), min(nums)) # 5 1

print(sum(nums, 100))       # 带初始值：114

# 找最大值的下标
print(nums.index(max(nums)))    # 4

# 按某个字段找最大的那个对象
people = [{"name": "李", "age": 30}, {"name": "王", "age": 22}]
print(max(people, key=lambda p: p["age"])["name"])   # 李
```

## 语句解释

### sum(序列)

从头累加。第二个参数是初始值，默认 0。

### max / min

直接给数值序列就能比。传 `key=` 则按函数返回值比，返回的是**元素本身**。

### nums.index(max(nums))

找最大值的下标：先求最大值，再回列表里查它第一次出现的位置。

## 原理解释

**一句话：** 它从一个起点开始，把每个元素都「并」进当前结果里——sum 是加，max 是谁大留谁。

**执行逻辑：**

1. 取初始值（sum 默认 0；max/min 取第一个元素当擂主）
2. 取下一个元素
3. 和当前结果合并：sum 相加；max 比较，更大就替换擂主
4. 重复 2–3 直到取完
5. 返回最终结果

**机器层（可跳过）：** 一趟线性遍历，不额外占内存（不需要新列表）。

**边界（从逻辑推出来）：**

- 第 1 步 `max` 要拿第一个元素当擂主，所以**空序列时它没有起点**，只能抛 `ValueError`
- `sum` 有默认起点 0，所以空序列返回 0（不报错）
- 第 3 步是逐个比较，所以元素必须能互相比较；混着数字和字符串会抛 `TypeError`
- `.index(max(...))` 要找两次：一次求值一遍遍历，一次查位置——数据大时改成 `max(enumerate(...))`

## 注意事项

- 空列表：`sum` 得 0，`max`/`min` 抛 `ValueError`，要么判空要么给 `default=`。
- `max(nums, default=0)` 是 3.4+ 的写法，空序列也能安全返回。
- 求平均别写 `sum/len`，空列表会除零；用 `statistics.mean` 或先判空。
- 浮点求和有精度误差，金额场景用 `Decimal` 或先转成分。

## 使用场景

- 统计总价、总时长。
- 找最高分、最低价。
- 按字段从对象列表里挑最大/最小的那个。
