r"""AI 层（留位，不实现）。

2026-11-22 定：这里从今天起是**接口**，不是功能。

为什么要先把空壳摆上：
1. 上层（UI、搜索服务）现在就可以按"有 AI / 没 AI"两种路径写，
   以后接模型是填一个实现，不是改架构；
2. 契约写在 docs/AI_PROTOCOL.md 里，接口和文档一起改，不会跑偏；
3. 没有 key、断网、模型抽风时，NullProvider 保证程序照常能用。

**边界（来自 AUTHORING_SPEC）：AI 只做整理，不生成知识、不改代码。**
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Protocol, Sequence

from starport_dictionary.models.entry import Entry


@dataclass(frozen=True)
class Candidate:
    """发给 AI 的候选摘要。故意不带代码正文——既省 token，也防模型照着改代码。"""

    entry_id: str
    title: str
    description: str
    object_name: str
    action_name: str
    aliases: tuple[str, ...]


@dataclass(frozen=True)
class OrganizedResult:
    """AI 整理完的结果。primary 必须在候选集合里，否则调用方丢弃。"""

    intent: str
    primary_entry_id: str
    related_entry_ids: tuple[str, ...] = ()
    ambiguous: bool = False


class AIProvider(Protocol):
    """所有模型接入方实现的接口。一个方法就够，别的都在调用方做。"""

    name: str

    def organize(
        self, query: str, candidates: Sequence[Candidate]
    ) -> OrganizedResult | None:
        """返回 None 表示"这次不参与"，调用方走本地结果。"""
        ...


class NullProvider:
    """没有 AI 时的实现：什么都不做，直接返回 None。

    这不是"降级路径"，这是**默认路径**——产品原则是没 AI 也能用。
    """

    name = "null"

    def organize(self, query: str, candidates: Sequence[Candidate]) -> OrganizedResult | None:
        return None


def build_candidate(entry: Entry) -> Candidate:
    return Candidate(
        entry_id=entry.id,
        title=entry.title,
        description=entry.description,
        object_name=entry.obj.name,
        action_name=entry.action.name,
        aliases=entry.obj.aliases + entry.action.aliases,
    )


def get_provider(enabled: bool = False) -> AIProvider:
    """拿一个 provider。现在永远是 NullProvider；接模型时改这一处。

    `enabled` 由配置 `ai.enabled` 决定，默认关——**开关默认关**是刻意的，
    免得莫名其妙花别人的 API 额度。
    """
    if not enabled:
        return NullProvider()
    # TODO(接模型时): 读配置里的 key/模型名，返回真实实现。
    return NullProvider()
