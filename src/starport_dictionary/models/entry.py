r"""知识条目：一个 Markdown 文件解析出来的数据对象。

2026-11-17 第二版。跟着 AUTHORING_SPEC 改的：
- 一条条目有且只有一个主要 Object 和一个主要 Action（都可带 id / 名称 / 别名）
- utterances 按六类语气存档，但**不参与检索**，只当测试集用
- 支持 ambiguity：一句话可能对应多条条目时，把候选列出来，不硬猜
"""

from __future__ import annotations

from dataclasses import dataclass, field


@dataclass(frozen=True)
class Semantic:
    """Object 或 Action：一个语义基元在条目里的落地写法。"""

    id: str
    name: str
    aliases: tuple[str, ...]


@dataclass(frozen=True)
class Constraint:
    """附加条件。values 为空表示这是个开关型约束（只判断有没有）。"""

    key: str
    values: tuple[str, ...] = ()
    default: str = ""


@dataclass(frozen=True)
class Ambiguity:
    """歧义说明：这句话还可能指哪条，以及凭什么区分。"""

    note: str
    candidate_ids: tuple[str, ...] = ()


@dataclass(frozen=True)
class Entry:
    """一条知识条目。frozen 是为了防止下游顺手改 id——id 一变引用全断。"""

    id: str
    title: str
    language: str
    category_id: str
    status: str
    obj: Semantic
    action: Semantic

    # 六类用户说法（direct / questions / colloquial / goal_based / technical / short_queries）
    utterances: dict[str, tuple[str, ...]]

    # 正文六节
    description: str
    code: str
    statement_notes: str  # 语句解释（含 ### 小节）
    principle: str
    caveats: str
    scenario: str

    # 可选
    module: str = ""
    origin: str = ""        # builtin / stdlib / thirdparty
    import_stmt: str = ""   # 要写的 import 语句，内置能力留空
    qualname: str = ""      # 准确技术全名，如 dict.get / pathlib.Path.suffix  # os / time / random / pathlib / PySide6 …（按库分册用）
    targets: tuple[str, ...] = ()
    constraints: tuple[Constraint, ...] = ()
    related_ids: tuple[str, ...] = ()
    tested_versions: tuple[str, ...] = ()
    min_version: str = ""
    version_note: str = ""
    ambiguity: tuple[Ambiguity, ...] = ()
    sources: tuple[str, ...] = ()

    def index_terms(self) -> tuple[str, ...]:
        """进索引的词：只放「模型认识的东西」。

        故意不含 utterances——把用户的原话同时当索引和测试集，测试就恒真了。
        """
        terms = [self.title, self.obj.name, self.action.name]
        terms += list(self.obj.aliases)
        terms += list(self.action.aliases)
        terms += list(self.targets)
        return tuple(t for t in terms if t)

    def searchable_text(self) -> str:
        """给全文检索用的文本。不含代码：代码里的括号和变量名会污染命中。"""
        parts = [
            self.title,
            self.description,
            self.scenario,
            " ".join(self.tags_text()),
        ]
        return "\n".join(p for p in parts if p)

    def tags_text(self) -> tuple[str, ...]:
        """把 object/action 的 id 和别名拼成可检索的标签。"""
        return (self.obj.id, self.action.id) + self.obj.aliases + self.action.aliases
