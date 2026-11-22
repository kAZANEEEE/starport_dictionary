# Starport Dictionary

一本用中文自然语言查的代码字典。

## 为什么做这个

理由很单纯：**我不太了解基础语句。**

写代码的时候经常卡在“这一步该用什么”上——知道要干什么，但想不起函数名，或者记不清该用哪个模块。查文档得先知道关键词，而我不知道关键词，得先知道关键词才能查文档，这事本身就绕。

所以想攒一本倒过来的字典：**我用自己的话描述想做的事，它告诉我该怎么写，并且讲清楚每一句在干嘛。**

不是给搜索引擎用的，是给我自己用的。如果对你也有用，那更好。

## 它是什么

输入一句需求，返回一条知识：能直接用的代码 + 逐句解释 + 原理 + 坑。

```
输入：判断文件后缀
返回：
    from pathlib import Path

    file_path = Path("example.PY")
    if file_path.suffix.lower() == ".py":
        print("这是一个 Python 文件")

    逐句解释、原理解释、注意事项、相关方案
```

## 它不是什么

- 不是代码生成器——AI 只负责在已有条目里挑和排，不负责现编
- 不是 IDE，不是代码编辑器
- 不是 API 文档浏览器
- 不是聊天机器人

**最关键的一条：没有 AI 也要能用。** 搜索走本地知识库，AI 只是把候选结果整理得更贴合你的问法。断网、没配 key 的时候，它退化成一本能搜的字典，而不是打不开的软件。

## 现在到哪儿了

早期。真的早期。

| 部分 | 状态 |
|---|---|
| 知识条目格式（YAML 头 + 六节正文） | 定了 |
| 对象 / 动作受控词表 | 47 个对象、12 个动作 |
| Markdown 解析 + 严格校验 | 能用 |
| 知识包加载 | 能用 |
| 检索（别名 + IDF 加权） | 2013 条说法：召回@5 约 72% |
| 知识条目 | **137 条**（26 个模块） |
| 调用形状（签名 / 参数 / 返回值） | 137 条全覆盖 |
| 条目代码验真（真跑一遍） | 137 条全部实跑通过 |
| 知识目录 CATALOG.md | 自动生成 + 一致性测试防过期 |
| 桌面界面（PySide6 三屏） | **能用** |
| Windows EXE | **能打包，37.6 MB 单文件** |
| AI 整理层 | 接口留好了，没接 |
| SQLite / 索引 | 还没做 |

## 跑起来

### 桌面版（推荐）

```
dist\StarportDictionary.exe
```

双击，输入一句大白话，看结果，复制代码。不需要装 Python，不需要命令行，知识库打包在 exe 里。

### 开发期

```bash
set PYTHONPATH=src
py -3 -m starport_dictionary.ui.app          # 开界面
py -3 -m pytest -q                           # 40 个测试
py -3 tools/api_demo.py 判断文件后缀          # 不开界面，看检索结果
py -3 tools/verify_entries.py                # 137 条代码全部实跑一遍
py -3 tools/gen_catalog.py                   # 重生成知识目录
```

依赖：PyYAML + PySide6（打包还要 PyInstaller）。
打包与排错见 [`docs/BUILD.md`](docs/BUILD.md)，界面分层见 [`docs/UI_ARCHITECTURE.md`](docs/UI_ARCHITECTURE.md)。

## 目录

```
src/starport_dictionary/
    api/                         ★ 前端与后端的唯一契约（DTO / 协议 / 工厂）
    ui/                          ★ 界面：三屏 + 深空主题 + 反馈（只认 api）
    models/entry.py              条目数据对象
    knowledge/parser.py          Markdown → 条目（校验都在这里）
    knowledge/primitives.py      对象/动作受控词表（唯一事实源）
    knowledge/loader.py          扫知识包
    search/baseline.py           别名匹配的检索基线
knowledge-packs/python-core/     知识条目本体（137 条）
    CATALOG.md                   自动生成的知识目录
docs/                            编写规范、格式、词表、打包、界面架构
tests/                           解析 + 检索 + api + 界面冒烟（40 个）
tools/                           验真、目录生成、检索基准、界面截图
run_starport.py                  打包入口
```

**一条硬规矩：`ui/` 里不许 import `knowledge` 或 `search`。** 界面只认 `api` 层的 DTO，将来把检索换成 Rust 或者接 AI，只要实现同样的 `SearchBackend` 协议，界面一行不用改。

## 一条知识长什么样

```yaml
---
id: py.fs.check_extension
title: 判断文件后缀
object:
  id: file.extension          # 必须在词表里
  name: 文件后缀
  aliases: [后缀, 扩展名, suffix]
action:
  id: inspect.check
  name: 判断
  aliases: [检查, 验证, 看看是不是]
utterances:
  direct: [判断文件后缀]
  colloquial: [看看是不是 py 文件]
  short_queries: [后缀, .py]
status: tested
---
```

正文六节：功能描述 / 推荐代码 / 语句解释 / 原理解释 / 注意事项 / 使用场景。缺一节，导入直接拒绝。

## 三条设计上的倔强

**1. 用户原话不进索引。**
每条知识里都记着“用户可能会这么说”，但那些句子只当测试集。存进索引的话，用原话搜原话必然命中，测试就恒真了，什么也没验证。

**2. 对象和动作分开，都要有稳定 ID。**
“文件后缀”和“扩展名”是同一个东西，不能算两条。不这样收口，二十条之后就会出现三种写法，互相串不起来。

**3. 代码没跑过，不许标 tested。**
模型编 API 编得很像。所以每条条目里的代码都得真执行一遍，跑不通的标成草稿，把报错写进注意事项。

## 下一步

桌面版 V0.1 立住了（搜索 → 结果 → 详情 → 复制，全程不用命令行）。接下来两件事：

1. **补内容**：剩下的高频库（PySide6、openpyxl、jieba），目标先把 150 条走完
2. **补查准**：现在召回@5 只有 72%，条目越多越低——词袋匹配到 137 条就到天花板了。真正的解法是接 AI 层（`ai/provider.py` 已经留好空实现），把候选重新排序

顺序上不赶：**内容对了，界面才有意义。** 但界面能用了之后，该反过来催内容了。

## 许可

知识内容 CC-BY-4.0，代码待定。
