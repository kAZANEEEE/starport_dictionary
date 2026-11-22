# Starport Dictionary —— 前端架构与实现说明

> 2026-11-22 · V0.1 · 面向开发者的自然语言能力检索工具
> 一句话：**描述你想实现什么，而不是搜索你不知道名字的 API。**

---

## 一、分层：UI 不认识检索

```
src/starport_dictionary/
├── api/                       ← 前端与后端的唯一契约
│   ├── dto.py                 纯数据：EntryDTO / HitDTO / SearchResponse / ImportHint
│   ├── backend.py             SearchBackend 协议（search / get_entry / stats）
│   ├── local_backend.py       用 loader + baseline 实现的本地后端
│   └── factory.py             get_backend()：换后端只改这里
├── ui/                        ← 只 import api，绝不 import knowledge/search
│   ├── theme.py               深空色板 + 星空背景
│   ├── resources/dark.qss     全部样式集中在这里
│   ├── widgets.py             徽章 / 代码块（Python 高亮）/ 区块 / 候选行
│   ├── views.py               首页 / 结果 / 详情 三屏
│   ├── main_window.py         单窗口 + 三屏切换 + 快捷键 + 反馈落盘
│   ├── store.py               反馈 jsonl / 最近搜索 json
│   └── app.py                 入口（含 --smoke 自检）
├── knowledge/                 知识库解析（前端不碰）
└── search/                    检索算法（前端不碰）
```

**三条硬规矩**

1. `ui/` 里不允许出现 `from ..knowledge` 或 `from ..search`——只有 `api`。
2. 页面控件只发信号，**不直接调后端**；后端调用统一在 `main_window.py`。
3. 换实现（Rust / AI 检索）只需要满足 `SearchBackend` 协议，改 `factory.get_backend()`，界面一行不动。

---

## 二、三屏结构

| 屏 | 内容 | 交互 |
|---|---|---|
| **首页** | 品牌行 + 中央大搜索框（视觉中心）+ 4 个示例 chip + 最近搜索 | Enter 搜索、点 chip 即搜、Ctrl+K 聚焦 |
| **结果** | 小搜索框 + 候选数 + 最佳匹配大卡 + 其他候选 + 反馈按钮 | 点条目进详情、Esc 回首页 |
| **详情** | 标题 + 层级/模块徽章 + 一句话效果 + **import 面板** + 调用形状 + 原理解释 + 代码（可复制）+ 参数表 + 返回值 + 注意事项 + 相关知识 | 复制、返回 |

**import 面板是详情页的重点**，三种状态各自诚实渲染，不做猜测：

- `builtin` → `✓ 无需导入 — 这是 Python 内置能力，直接写就行`
- `stdlib` → 显示 `import` 语句（如 `from pathlib import Path`）
- `thirdparty` → 先显示安装命令（`pip install requests`），再显示 import
- `unknown` → `该条目未标注所属层级，暂无法判断是否需要导入`

---

## 三、视觉

深空主题 token（`theme.py` 与 `dark.qss` 保持同一套值）：

| 用途 | 色值 |
|---|---|
| 背景 | `#0b1020` |
| 卡面 / 卡面深 | `#121a33` / `#131c38` |
| 边框 | `#1f2a4a` |
| 主强调（紫） | `#7c6cff` |
| 次强调（青） | `#4cc9f0` |
| 正文 / 次要文字 | `#e6e9f5` / `#8b93b0` |

克制的地方：星空只做一次性静态点阵（固定随机种子，每次启动一致），不做闪烁；动画只有代码块「已复制」1.2 秒回弹。搜索框是唯一的大字号元素。

---

## 四、反馈数据

`%LOCALAPPDATA%\StarportDictionary\feedback.jsonl`，一行一条：

```json
{"query":"判断一个文件的后缀名","verdict":"ok","best_entry_id":"py.fs.check_extension",
 "best_title":"判断文件后缀","candidates":["py.fs.check_extension","py.string.is_family"],
 "backend":"local","app_version":"0.1.0","created_at":"2026-11-22T14:20:31"}
```

为什么记这么多：要能**复现用户当时看到的界面**——只看 verdict 无法判断是「找错了」还是「找不到」。

最近搜索：`recent.json`，最多 5 条，去重，新的在前。

---

## 五、快捷键

| 键 | 作用 |
|---|---|
| `Enter` | 搜索 |
| `Ctrl+K` | 回到搜索框（结果页时聚焦小搜索框） |
| `Esc` | 详情 → 结果 → 首页，逐级返回 |
| `Ctrl+Q` | 退出 |

---

## 六、测试

| 文件 | 覆盖 |
|---|---|
| `tests/test_api.py` | DTO 契约、后端适配、缺失数据容错（14 个） |
| `tests/test_ui_smoke.py` | 离屏构造窗口、切屏、搜索、反馈落盘、坏数据不崩（11 个） |
| `tests/test_parser.py` / `test_utterances.py` / `test_catalog.py` | 知识库本身（15 个） |

UI 测试用 `QT_QPA_PLATFORM=offscreen` + `FakeBackend` 注入——**这本身就是解耦的证据**：界面能在一个假的检索后端上完整跑通。

---

## 七、已知待办（V0.2）

- 条目内搜索高亮
- 相关知识可点击跳转（现在只显示标题与「未收录」）
- 全部条目浏览页（CATALOG 已有数据）
- 反馈导出成评测集，接回 `tests/test_utterances.py`
- 检索后端接 AI 层（`ai/provider.py` 已留空实现）
