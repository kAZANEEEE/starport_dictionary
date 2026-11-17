# 知识条目格式

一条知识条目 = 一个 Markdown 文件。

## 为什么用 Markdown + TOML 头

三个选择之间比较过：

| 方案 | 好处 | 坏处 |
|---|---|---|
| 纯 Markdown + 手写解析 | 零依赖 | 字段一多就容易解析错，出错报不到行 |
| YAML 头（`---`） | 最常见 | 要多装 PyYAML；YAML 的缩进规则对写内容的人不友好 |
| **TOML 头（`+++`）** | 零依赖（Python 3.11+ 自带 tomllib）、语法死板不易写错 | 嵌套多了会啰嗦 |

选第三个。正文用 Markdown 给人写，头部用 TOML 给程序读，两边各干各的。

---

## 文件长什么样

```markdown
+++
id = "py.fs.check_extension"
title = "判断文件后缀"
language = "python"
category_id = "programming.filesystem"
status = "tested"
aliases = ["判断文件扩展名", "检查是不是py文件"]
tags = ["python", "pathlib", "file", "suffix"]
scenario = "只处理某种格式的文件时"
tested_versions = ["3.10", "3.11", "3.12"]
related_ids = ["py.fs.get_suffixes"]
sources = ["Python 文档 pathlib.Path.suffix"]
+++

## 代码

```python
from pathlib import Path
...
```

## 功能描述
...

## 逐句解释
...

## 原理解释
...

## 注意事项
...
```

最终的文件里，正文中的代码块是三反引号包起来的；上面为了写在这里才缩进。

---

## 字段说明

| 字段 | 必填 | 类型 | 说明 |
|---|---|---|---|
| `id` | 是 | 字符串 | 全局唯一，形如 `py.fs.check_extension`。发布后不改 |
| `title` | 是 | 字符串 | 功能名称，一句话 |
| `description` | 否 | 字符串 | 简短描述；不写就从正文「功能描述」取第一段 |
| `aliases` | 是 | 字符串数组 | 用户可能怎么问，至少 2 条 |
| `tags` | 是 | 字符串数组 | 跨分类检索用 |
| `language` | 是 | 字符串 | `python` / `c` / `linux` … |
| `category_id` | 是 | 字符串 | 主要分类，见 KNOWLEDGE_TAXONOMY |
| `status` | 是 | 枚举 | `draft` / `reviewed` / `tested` / `deprecated` |
| `scenario` | 是 | 字符串 | 什么情况下会用到它 |
| `tested_versions` | 是 | 字符串数组 | 实测过的 Python 版本 |
| `related_ids` | 否 | 字符串数组 | 相关条目 ID |
| `sources` | 否 | 字符串数组 | 依据哪份文档 |

## 正文五节（固定标题）

| 标题 | 内容 |
|---|---|
| `## 代码` | 可直接运行的代码块，只有一个 |
| `## 功能描述` | 这段代码干什么，一两句 |
| `## 逐句解释` | 逐行/逐句讲每个语法点 |
| `## 原理解释` | 背后的机制，为什么这么写 |
| `## 注意事项` | 容易踩的坑、边界情况 |

标题必须按这个顺序出现，解析器靠它切段。缺哪一节就报错——宁可不收这条，也不收一条解释不全的。

---

## id 命名规则

```
<语言或领域>.<分类>.<动作或对象>

py.fs.check_extension        判断文件后缀
py.fs.get_suffixes           获取多个后缀
py.list.dedupe               列表去重
py.algorithm.binary_search   二分查找
linux.process.get_pid        获取进程号
sql.query.select             查询
```

- 全小写，下划线分词
- 发布后**不能因为改标题或改分类而改 id**
- 一个 id 只能有一个文件；导入时发现重复直接报错

---

## 审核状态怎么用

| 状态 | 含义 | 能不能展示给用户 |
|---|---|---|
| `draft` | 有草稿，没验证 | 不展示 |
| `reviewed` | 人读过，写法合理 | 可展示，标注「未实测」 |
| `tested` | 在 `tested_versions` 里跑通过 | 正常展示 |
| `deprecated` | 有更好写法，保留作历史 | 可搜索，标注「已过时」 |

**第一版只展示 `reviewed` 和 `tested`。** 未经验证的代码混进结果里，比搜不到更伤人。
