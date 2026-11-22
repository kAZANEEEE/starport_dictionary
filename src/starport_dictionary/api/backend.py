r"""检索后端的**协议**（Ports & Adapters 里的 Port）。

UI 只依赖这个协议，不依赖具体实现：
    现在 → LocalKnowledgeBackend（Python，词袋匹配）
    将来 → RustBackend / AiBackend（实现同样三个方法即可）

三个方法刻意做得很少，因为每多一个方法，将来换实现就多一份负担。
"""

from __future__ import annotations

from typing import Protocol

from starport_dictionary.api.dto import EntryDTO, LibraryStats, SearchResponse


class SearchBackend(Protocol):
    """任何检索后端都要满足这个形状。"""

    name: str

    def search(self, query: str, limit: int = 8) -> SearchResponse:
        """按自然语言查询返回候选。**不抛异常**：内部错误返回空结果 + 记录日志。"""
        ...

    def get_entry(self, entry_id: str) -> EntryDTO | None:
        """按 id 取一条完整条目；不存在返回 None（界面显示「未收录」）。"""
        ...

    def stats(self) -> LibraryStats:
        """库的规模信息，给状态栏和出错提示用。"""
        ...
