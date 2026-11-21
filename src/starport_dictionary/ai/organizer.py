r"""搜索结果的"整理层"。今天它只做一件事：原样返回本地排序。

等 AI 接上之后，这里负责：
    本地候选 → 交给 provider.organize() → 校验返回值 → 重排/分组

**校验是这一步的核心**（见 docs/AI_PROTOCOL.md）：
模型回来的 ID 必须存在于本次候选集合里，否则整份结果丢弃，退回本地排序。
理由很简单——模型最擅长的错就是"编一个看起来很对的 id"。
"""

from __future__ import annotations

from dataclasses import dataclass

from starport_dictionary.ai.provider import AIProvider, Candidate, build_candidate
from starport_dictionary.models.entry import Entry
from starport_dictionary.search.baseline import Hit


@dataclass(frozen=True)
class SearchOutcome:
    """一次搜索的最终结果：本地排序 + 是否经过 AI 整理。"""

    hits: tuple[Hit, ...]
    organized_by: str = "local"  # "local" 或 provider 名字
    intent: str = ""
    ambiguous: bool = False


def organize(
    query: str,
    hits: list[Hit],
    entries: dict[str, Entry],
    provider: AIProvider,
) -> SearchOutcome:
    if not hits:
        return SearchOutcome(hits=())

    candidates = [build_candidate(entries[h.entry_id]) for h in hits if h.entry_id in entries]
    result = provider.organize(query, candidates)

    if result is None:
        return SearchOutcome(hits=tuple(hits))

    # —— 校验：不合法就整份退回本地结果，不做"部分采纳" ——
    valid_ids = {c.entry_id for c in candidates}
    if result.primary_entry_id not in valid_ids:
        return SearchOutcome(hits=tuple(hits))
    if any(rid not in valid_ids for rid in result.related_entry_ids):
        return SearchOutcome(hits=tuple(hits))

    ordered = sorted(
        hits,
        key=lambda h: (
            0 if h.entry_id == result.primary_entry_id else 1,
            result.related_entry_ids.index(h.entry_id)
            if h.entry_id in result.related_entry_ids
            else len(result.related_entry_ids),
        ),
    )
    return SearchOutcome(
        hits=tuple(ordered),
        organized_by=provider.name,
        intent=result.intent,
        ambiguous=result.ambiguous,
    )
