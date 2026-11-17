r"""知识条目：一个 Markdown 文件解析出来的数据对象。

2026-11-17 定：字段和 docs/KNOWLEDGE_FORMAT.md 一一对应。
这里只做「装数据」，校验放在 parser 里——分开之后，加字段不用动校验逻辑，
改校验规则也不会碰到数据结构。
"""

from __future__ import annotations

from dataclasses import dataclass, field


@dataclass(frozen=True)
class Entry:
    """一条知识条目。frozen 是为了防止下游顺手改字段——id 一旦变了，引用全断。"""

    id: str
    title: str
    language: str
    category_id: str
    status: str
    scenario: str
    aliases: tuple[str, ...]
    tags: tuple[str, ...]
    tested_versions: tuple[str, ...]

    # —— 正文五节 ——
    code: str
    description: str
    explanation: str
    principle: str
    caveats: str

    # —— 可选 ——
    related_ids: tuple[str, ...] = ()
    sources: tuple[str, ...] = ()
    extra: dict[str, str] = field(default_factory=dict)

    def searchable_text(self) -> str:
        """拼给搜索引擎用的可检索文本。

        故意不把 code 拼进去：代码里的语法噪音太大（括号、缩进、变量名），
        会让全文检索把「文件名」这类词命中到不相干的条目上。
        """
        parts = [
            self.title,
            self.description,
            self.scenario,
            " ".join(self.aliases),
            " ".join(self.tags),
        ]
        return "\n".join(p for p in parts if p)
