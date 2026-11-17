# 知识条目格式（KNOWLEDGE_FORMAT v2）

> 2026-11-17 第二版：头部从 TOML 换成 YAML（结构嵌套深，YAML 写起来顺），
> 加入 object / action / utterances / ambiguity / min_version。
> 规则见 `docs/AUTHORING_SPEC.md`。

一条知识条目 = 一个 Markdown 文件，`---` 包起来的 YAML 头 + 六节正文。

## 头部字段

| 字段 | 必填 | 类型 | 说明 |
|---|---|---|---|
| `id` | 是 | 字符串 | `py.fs.check_extension`，发布后不改 |
| `title` | 是 | 字符串 | 功能名称 |
| `description` | 否 | 字符串 | 一句话描述 |
| `language` | 是 | 字符串 | `python` / `c` / `linux` |
| `category_id` | 是 | 字符串 | 主要分类 |
| `object` | 是 | 对象 | `id` / `name` / `aliases`，id 必须在词表里 |
| `action` | 是 | 对象 | 同上 |
| `targets` | 否 | 字符串数组 | 具体目标，如 `[".py", ".jpg"]` |
| `constraints` | 否 | 对象数组 | `key` / `values` / `default` |
| `utterances` | 是 | 分组映射 | 六类，至少 8 条，四类必须有 |
| `ambiguity` | 否 | 对象数组 | `note` / `candidate_ids` |
| `related_ids` | 否 | 字符串数组 | 相关条目 id |
| `status` | 是 | 枚举 | `draft` / `reviewed` / `tested` / `deprecated` |
| `tested_versions` | 否 | 字符串数组 | **实际跑过的具体版本** |
| `min_version` | 条件必填 | 字符串 | 写了 tested_versions 就必须写 |
| `version_note` | 否 | 字符串 | 给人读的补充 |
| `sources` | 否 | 字符串数组 | 依据的文档 |

**出现未定义字段会被解析器拒绝**——规范里那句"不得自行创建顶层字段"，由代码执行。

## 正文六节

顺序固定，缺一节直接拒绝导入：

| 小节 | 内容 |
|---|---|
| `## 功能描述` | 一两句说清干什么 |
| `## 推荐代码` | 一个可运行的代码块 |
| `## 语句解释` | 用 `### 语法点` 逐条解释 |
| `## 原理解释` | 为什么能实现 |
| `## 注意事项` | 坑和边界 |
| `## 使用场景` | 什么时候会用到 |

## 完整例子

见 `knowledge-packs/python-core/entries/py.fs.check_extension.md`。

## 校验清单（解析器自动执行的）

1. 头尾 `---` 成对
2. YAML 能解析
3. 必填字段齐、未知字段无
4. `object.id` / `action.id` 在词表里
5. `object` / `action` 的 aliases 非空
6. `utterances` 四类齐、总数 ≥ 8
7. `status` 在枚举里
8. `id` 形如 `py.fs.xxx`（三段以上、小写）
9. 写了 `tested_versions` 必须有 `min_version`
10. 正文六节齐且非空
11. 「推荐代码」里有 ``` 代码块

## 不自动校验的部分（靠人）

- 语句解释是否真的讲清了语法（不是复读代码）
- 原理解释有没有编造底层细节
- 别名是不是真的同义
- related_ids 是否指向**存在**的条目（等条目多了再加这道检查）
