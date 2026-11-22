---
id: py.string.count_words
title: 统计有多少个词
description: 中文和英文要分开处理，不能都按空格切
language: python
category_id: programming.basics
module: str
origin: builtin
import: ""
qualname: "split() + len()"
signature: "len(text.split())"
args:
  - name: "text"
    required: true
    accepts: "要统计的文本"
    nesting: "可以"
returns: "整数：按空白切出来的段数；中文按空格切不出「词」，需要分词工具"
object:
  id: string.text
  name: 字符串
  aliases: [文本, 词数, 字数, 单词数, string]
action:
  id: get.obtain
  name: 获取
  aliases: [统计, 数, 计算, 得到, count]
targets: []
utterances:
  direct:
    - 统计有多少个词
    - 数一下单词数
    - 文本词数统计
  questions:
    - 怎么统计一段话有多少个单词
    - 中文字数怎么数
    - len(split) 和 len(文本) 有什么区别
  colloquial:
    - 想看看这段文字有多少词
    - 英文按空格切就行，中文怎么办
  technical:
    - 词数统计
    - split 长度
    - 中文分词 jieba
  short_queries:
    - 词数
    - 字数
    - 统计
status: tested
tested_versions: ["3.10", "3.11", "3.12", "3.13", "3.14"]
min_version: "3.0"
version_note: "split 各版本一致；中文分词需第三方 jieba"
sources:
  - Python 官方文档 str.split
---

# 统计有多少个词

## 功能描述

英文：`len(text.split())` 就是词数。中文：`split()` 只会按空格切，**切不出词**，需要第三方分词。

## 推荐代码

```python
text = "hello starport dictionary"
print(len(text.split()))     # 3  ← 英文按空格切

cn = "星港词典很好用"
print(len(cn))               # 7  ← 这是字符数，不是词数
print(len(cn.split()))       # 1  ← 中文没有空格，只会得到 1 段

# 中文分词需要第三方库（未安装时这段会报 ImportError）
try:
    import jieba
    print(len(list(jieba.cut(cn))))   # 词数
except ImportError:
    print("没装 jieba，中文词数算不了")
```

## 语句解释

### len(text.split())

`split()` 不带参数 = 按任意连续空白切，并丢弃两端空白，所以不会数出空串。

### len(text) 是字符数

对英文是字母数、对中文是汉字数，不等于词数。

### 中文必须分词

中文词与词之间没有空格，`split` 无从下手。

## 原理解释

**一句话：** 统计词数的本质是「先按语言规则把句子切成词，再数切出来的段数」。

**执行逻辑：**

1. 判断文本类型：有空格分隔的英文，还是无空格的中文
2. 英文 → 按空白切，切出的段数就是词数
3. 中文 → 交给分词工具按词典/模型切
4. 数段数

**机器层（可跳过）：** 英文切分是 O(n) 扫描；中文分词要看工具（可能是统计模型）。

**边界（从逻辑推出来）：**

- 第 2 步按空白切，所以标点会粘在词上（`"hello,"` 算一个词）
- 第 3 步说明中文必须换工具，`split` 永远只给 1 段
- `split()` 会丢弃两端空白、合并连续空白，所以不会数出空串
- 中英混排时两种规则都不完美，需要先按语言分段

## 注意事项

- 中文别用 `split()` 数词，会永远得到 1。
- 英文统计前常要 `lower()` 并去掉标点。
- 想要「字数」（不含空格）用 `len(text.replace(" ", ""))`。
- 中文分词质量取决于词典，专有名词容易切错。

## 使用场景

- 文章字数统计（约稿、投稿要求）。
- 输入长度校验（限制多少字）。
- 文本分析前的预处理。
