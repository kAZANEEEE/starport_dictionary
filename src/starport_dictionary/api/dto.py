r"""前端与检索之间的**唯一数据契约**。

2026-11-22 立的三条规矩：
1. 这里全是纯数据（dataclass），不引用 Entry / Hit / 任何检索实现——UI 只认这些。
2. 字段按「界面要显示什么」来定，不按「知识库怎么存」来定。
3. 未来把检索换成 Rust，只要它产出同样的 DTO，界面一行都不用改。
"""

from __future__ import annotations

from dataclasses import dataclass, field


@dataclass(frozen=True)
class ArgDTO:
    """参数契约（详情页的「参数」表用）。"""

    name: str
    required: bool = True
    default: str = ""
    accepts: str = ""
    nesting: str = ""


@dataclass(frozen=True)
class RelatedDTO:
    """相关条目。title 为空表示「知识库里没有这条」。"""

    entry_id: str
    title: str = ""

    @property
    def exists(self) -> bool:
        return bool(self.title)


@dataclass(frozen=True)
class ImportHint:
    """「用之前要不要 import」这块的展示数据。

    界面按 kind 三选一渲染，不做任何猜测：
        builtin    → 内置能力，无需导入
        stdlib     → 显示 import 语句
        thirdparty → 显示安装命令 + import 语句
        unknown    → 数据缺失，如实说「未标注」
    """

    kind: str = "unknown"        # builtin / stdlib / thirdparty / unknown
    statement: str = ""          # 例如 import os
    install: str = ""            # 例如 pip install requests

    @property
    def needs_import(self) -> bool:
        return self.kind in {"stdlib", "thirdparty"}


@dataclass(frozen=True)
class EntryDTO:
    """一条知识条目的界面视图。"""

    id: str
    title: str
    description: str
    language: str
    category_id: str
    status: str

    origin: str = ""
    import_stmt: str = ""
    install: str = ""
    module: str = ""
    qualname: str = ""
    signature: str = ""
    returns: str = ""

    principle: str = ""
    code: str = ""
    statement_notes: str = ""
    caveats: str = ""
    scenario: str = ""

    args: tuple[ArgDTO, ...] = ()
    related: tuple[RelatedDTO, ...] = ()
    tested_versions: tuple[str, ...] = ()
    min_version: str = ""
    version_note: str = ""

    # —— 派生给界面用的展示字段 ——
    @property
    def import_hint(self) -> ImportHint:
        kind = self.origin if self.origin in {"builtin", "stdlib", "thirdparty"} else "unknown"
        return ImportHint(kind=kind, statement=self.import_stmt, install=self.install)

    @property
    def origin_label(self) -> str:
        return {
            "builtin": "内置能力",
            "stdlib": "标准库",
            "thirdparty": "第三方库",
        }.get(self.origin, "未标注")

    @property
    def module_label(self) -> str:
        return self.module or "未分册"


@dataclass(frozen=True)
class HitDTO:
    """一条搜索结果。matched_terms 用于展示「凭什么命中」。"""

    entry_id: str
    title: str
    score: int
    matched_terms: tuple[str, ...] = ()


@dataclass(frozen=True)
class SearchResponse:
    """一次搜索的完整结果。"""

    query: str
    hits: tuple[HitDTO, ...] = ()
    backend: str = "local"          # 哪个后端给的（local / rust / ai）
    intent: str = ""                # 有 AI 时才有值；V0.1 恒为空
    ambiguous: bool = False

    @property
    def has_results(self) -> bool:
        return bool(self.hits)

    @property
    def best(self) -> HitDTO | None:
        return self.hits[0] if self.hits else None

    @property
    def others(self) -> tuple[HitDTO, ...]:
        return self.hits[1:] if self.hits else ()


@dataclass(frozen=True)
class LibraryStats:
    """状态栏用：库里有多少东西。"""

    entry_count: int = 0
    module_count: int = 0
    pack_count: int = 0
    errors: tuple[str, ...] = field(default_factory=tuple)
