# Starport Dictionary

> 描述你想实现什么，而不是搜索你不知道名字的 API。

一本用中文大白话查的代码字典。输入「删除列表里重复的」，它告诉你 `dict.fromkeys`
怎么写、为什么这么写、以及会踩什么坑。

**Windows 桌面程序，双击即用，离线也能查。**

---

## 为什么做这个

（以下这段是老大的原话，我一个字没改——鲸鱼娘注）

> 理由很单纯：**我不太了解基础语句。**
>
> 写代码的时候经常卡在"这一步该用什么"上——知道要干什么，但想不起函数名，或者记不清该用哪个模块。查文档得先知道关键词，而我不知道关键词，得先知道关键词才能查文档，这事本身就绕。
>
> 所以想攒一本倒过来的字典：**我用自己的话描述想做的事，它告诉我该怎么写，并且讲清楚每一句在干嘛。**

不是给搜索引擎用的，是给他自己用的。如果对你也好用，那更好。

---

## 它是什么

输入一句需求，返回一条知识：

```
输入：判断文件后缀

返回：
    from pathlib import Path

    file_path = Path("example.PY")
    if file_path.suffix.lower() == ".py":
        print("这是一个 Python 文件")

    逐句解释 · 四段式原理 · 参数怎么填 · 返回什么 · 注意事项 · 相关知识
```

详情页有一块是**单独拎出来的**——「使用前需要 import 吗？」：

| 情况 | 界面怎么写 |
|---|---|
| Python 内置能力 | `✓ 无需导入` 绿色徽章 |
| 标准库 | 直接把 `import os` 摆出来，旁边一个复制按钮 |
| 第三方库 | 先给 `pip install requests`，再给 `import requests` |
| 条目没标注 | 如实写「暂无法判断」，不猜 |

---

## 它不是什么

- 不是代码生成器——AI 只负责在已有条目里挑和排，不负责现编
- 不是 IDE，不是代码编辑器
- 不是 API 文档浏览器
- 不是聊天机器人

**最关键的一条：没有 AI 也要能用。** 搜索走本地知识库，断网、没配 key 的时候它退化成一本能搜的字典，而不是打不开的软件。

---

## 现在到哪儿了

| 部分 | 状态 |
|---|---|
| 知识条目格式（YAML 头 + 六节正文） | 定了 |
| 对象 / 动作受控词表 | 47 个对象、12 个动作 |
| 知识条目 | **137 条**，26 个模块 |
| 调用形状（签名 / 参数 / 返回值） | 137 条全覆盖 |
| 条目代码验真（真的跑一遍） | **137 / 137 通过** |
| 知识目录 `CATALOG.md` | 自动生成，有测试盯着它不许过期 |
| 检索（别名 + IDF 加权） | 2013 条说法，召回@5 约 72% |
| 桌面界面（PySide6 三屏） | 能用 |
| Windows EXE | **能打包，约 40MB 单文件** |
| 反馈收集（本地 jsonl） | 能用 |
| AI 整理层 | 接口留好了，没接 |
| SQLite / 向量索引 | 还没做 |

---

## 桌面版怎么用

```
dist\StarportDictionary.exe     ← 双击
```

不需要装 Python，不需要命令行，知识库（137 条 Markdown）已经打包在 exe 里。

操作就这么几步：**输入大白话 → 回车 → 看结果 → 点进去看完整内容 → 复制代码**。

快捷键：

| 键 | 作用 |
|---|---|
| `Enter` | 搜索 |
| `↑` `↓` | 选候选 |
| `Enter`（在结果页） | 打开选中的那条 |
| `Esc` | 详情 → 结果 → 首页，逐级返回 |
| `Ctrl+K` | 回到搜索框 |
| `Ctrl+Q` | 退出 |

反馈按钮（正确 / 不正确）会把「原始查询 + 命中条目 + 全部候选 + 判断」写进
`%LOCALAPPDATA%\StarportDictionary\feedback.jsonl`，为以后调检索攒真实数据。

---

## 开发期怎么跑

```powershell
set PYTHONPATH=src

py -3 -m starport_dictionary.ui.app          # 开界面
py -3 -m pytest -q                           # 51 个测试
py -3 tools/api_demo.py 判断文件后缀          # 不开界面，只看检索
py -3 tools/verify_entries.py                # 137 条代码全部实跑一遍
py -3 tools/gen_catalog.py                   # 重生成知识目录
py -3 tools/ui_shot.py                       # 三屏渲染成 PNG（离屏）
```

依赖：`PyYAML` + `PySide6`（打包还要 `PyInstaller`，图标转换要 `Pillow`）。

打包与排错：见 [`docs/BUILD.md`](docs/BUILD.md)
界面分层：见 [`docs/UI_ARCHITECTURE.md`](docs/UI_ARCHITECTURE.md)
编写规范：见 [`docs/AUTHORING_SPEC.md`](docs/AUTHORING_SPEC.md)

---

## 目录

```
src/starport_dictionary/
    api/                         ★ 前端与后端的唯一契约（DTO / 协议 / 工厂）
    ui/                          ★ 三屏界面 + 深空主题 + 过渡动画 + 反馈
    models/entry.py              条目数据对象
    knowledge/parser.py          Markdown → 条目（校验都在这里）
    knowledge/primitives.py      对象/动作受控词表（唯一事实源）
    knowledge/loader.py          扫知识包
    search/baseline.py           别名匹配的检索基线
knowledge-packs/python-core/     知识条目本体（137 条）
    CATALOG.md                   自动生成的知识目录
docs/                            编写规范 / 格式 / 词表 / 打包 / 界面架构
tests/                           解析 + 检索 + api + 界面冒烟 + 真按键（51 个）
tools/                           验真、目录生成、检索基准、界面截图、图标转换
run_starport.py                  打包入口
assets/                          图标（png / ico / 原图）
```

**一条硬规矩：`ui/` 里不许 import `knowledge` 或 `search`。**

界面只认 `api` 层的 DTO。将来把检索换成 Rust、或者接上 AI 重排，只要实现同样的
`SearchBackend` 协议，改一个 `factory.get_backend()`，界面一行都不用动。

这不是洁癖，是为了**换引擎的时候不用重做界面**。

---

## 一条知识长什么样

```yaml
---
id: py.dict.get
title: 取字典里的值
description: 安全地按键取值，键不存在时给默认值
origin: builtin           # builtin / stdlib / thirdparty
import: ""                # 要写的 import 语句，内置留空
install: ""               # 第三方才需要，如 pip install requests
qualname: "dict.get"      # 准确技术全名
signature: "d.get(key, default=None)"
args:
  - name: key
    required: true
    accepts: 要查的键
    nesting: 可以，可以是变量
returns: 键存在返回值本身，不存在返回 default；不报错也不写入
---
```

正文六节：功能描述 / 推荐代码 / 语句解释 / 原理解释 / 注意事项 / 使用场景。
缺一节，导入直接拒绝。

**「原理解释」是四段固定的**，顺序不许换：

1. **一句话** —— 小白能懂
2. **执行逻辑** —— 逐步：先做什么、数据从哪来、到哪去（这部分是主体）
3. **机器层（可跳过）** —— 对底层好奇时看
4. **边界（从逻辑推出来）** —— 哪些情况会坑你，为什么

---

## 三条设计上的倔强

（这三条是老大的原话，我原样搬过来）

**1. 用户原话不进索引。**
每条知识里都记着"用户可能会这么说"，但那些句子只当测试集。存进索引的话，用原话搜原话必然命中，测试就恒真了，什么也没验证。

**2. 对象和动作分开，都要有稳定 ID。**
"文件后缀"和"扩展名"是同一个东西，不能算两条。不这样收口，二十条之后就会出现三种写法，互相串不起来。

**3. 代码没跑过，不许标 tested。**
模型编 API 编得很像。所以每条条目里的代码都得真执行一遍，跑不通的标成草稿，把报错写进注意事项。

---

## 我知道的缺口（不掩饰）

| 缺口 | 现状 | 打算 |
|---|---|---|
| 召回@5 只有 ~72% | 条目越多越低，词袋匹配到 137 条已到天花板 | 接 AI 层重排候选 |
| 缺常用库 | 没 GUI 组件、没 Excel、没并发 | 按老大的实际使用顺序补 |
| 相关知识跳不过去 | 部分 `related_ids` 指向未收录条目 | 界面已容错显示「未收录」 |
| 反馈还没用起来 | 只落盘，没回灌测试 | 攒够样本后做成评测集 |

---

## 关于这份 README

**这份 README 由肥鱼（鲸鱼娘）撰写，已获老大批准与审核。**

技术内容、条目、界面需求、验收标准出自老大；文字整理与结构排布是我做的。
如果哪句话不对，那是我写歪了，找老大确认过的口径为准。

---

## 许可

知识内容 CC-BY-4.0，代码待定。
