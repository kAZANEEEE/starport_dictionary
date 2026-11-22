r"""本地知识库后端：把现有的 loader + baseline 包成 DTO 契约。

2026-11-22：这是 P0 的核心——UI 之后只跟这一层打交道。
注意这里**做了两件事**，都不是简单的透传：
1. Entry → EntryDTO（含 origin/import/install 的展示逻辑，related 缺失时标成「未收录」）
2. Hit → HitDTO（把 matched_terms 拼成人话，界面直接显示）
"""

from __future__ import annotations

import logging
from pathlib import Path

from starport_dictionary.api.dto import (
    ArgDTO,
    EntryDTO,
    HitDTO,
    LibraryStats,
    RelatedDTO,
    SearchResponse,
)
from starport_dictionary.knowledge.loader import load_all_packs
from starport_dictionary.search.baseline import search as _baseline_search

log = logging.getLogger(__name__)


class LocalKnowledgeBackend:
    """用本地 Markdown 知识库实现的检索后端。"""

    name = "local"

    def __init__(self, packs_root: Path, limit: int = 8) -> None:
        self._packs_root = Path(packs_root)
        self._default_limit = limit
        self._entries = []
        self._by_id: dict[str, object] = {}
        self._errors: list[str] = []
        self.reload()

    # ---------- 加载 ----------
    def reload(self) -> None:
        """重新读知识库。条目改动后调它，不用重启程序。"""
        self._entries = []
        self._by_id = {}
        self._errors = []
        try:
            packs = load_all_packs(self._packs_root)
        except Exception as exc:  # 知识库坏了也不该让界面崩
            log.exception("加载知识库失败")
            self._errors.append(f"知识库加载失败：{exc}")
            return

        for pack in packs:
            self._errors.extend(pack.errors)
            for entry in pack.entries:
                self._entries.append(entry)
                self._by_id[entry.id] = entry
        log.info("载入 %d 条知识条目", len(self._entries))

    # ---------- 协议实现 ----------
    def search(self, query: str, limit: int | None = None) -> SearchResponse:
        text = (query or "").strip()
        if not text:
            return SearchResponse(query=query or "", backend=self.name)

        try:
            hits = _baseline_search(text, self._entries, limit=limit or self._default_limit)
        except Exception:
            log.exception("检索失败：%s", text)
            return SearchResponse(query=text, backend=self.name)

        dtos = tuple(
            HitDTO(
                entry_id=h.entry_id,
                title=getattr(self._by_id.get(h.entry_id), "title", h.entry_id),
                score=h.score,
                matched_terms=tuple(h.matched_terms),
            )
            for h in hits
        )
        return SearchResponse(query=text, hits=dtos, backend=self.name)

    def get_entry(self, entry_id: str) -> EntryDTO | None:
        entry = self._by_id.get(entry_id)
        if entry is None:
            return None
        return self._to_dto(entry)

    def stats(self) -> LibraryStats:
        modules = {getattr(e, "module", "") for e in self._entries}
        modules.discard("")
        return LibraryStats(
            entry_count=len(self._entries),
            module_count=len(modules),
            pack_count=len(list(self._packs_root.glob("*/manifest.json"))),
            errors=tuple(self._errors),
        )

    # ---------- Entry → DTO ----------
    def _to_dto(self, entry) -> EntryDTO:
        related = tuple(
            RelatedDTO(
                entry_id=rid,
                title=getattr(self._by_id.get(rid), "title", ""),  # 缺失就留空 → 界面显示「未收录」
            )
            for rid in getattr(entry, "related_ids", ())
        )
        return EntryDTO(
            id=entry.id,
            title=entry.title,
            description=entry.description,
            language=entry.language,
            category_id=entry.category_id,
            status=entry.status,
            origin=getattr(entry, "origin", ""),
            import_stmt=getattr(entry, "import_stmt", ""),
            install=getattr(entry, "install", ""),
            module=getattr(entry, "module", ""),
            qualname=getattr(entry, "qualname", ""),
            signature=getattr(entry, "signature", ""),
            returns=getattr(entry, "returns", ""),
            principle=entry.principle,
            code=entry.code,
            statement_notes=entry.statement_notes,
            caveats=entry.caveats,
            scenario=entry.scenario,
            args=tuple(
                ArgDTO(
                    name=a.name,
                    required=a.required,
                    default=a.default,
                    accepts=a.accepts,
                    nesting=a.nesting,
                )
                for a in getattr(entry, "args", ())
            ),
            related=related,
            tested_versions=tuple(getattr(entry, "tested_versions", ())),
            min_version=getattr(entry, "min_version", ""),
            version_note=getattr(entry, "version_note", ""),
        )
