r"""后端的唯一入口。**未来换 Rust 只改这一个文件。**

UI 代码里一律写：
    from starport_dictionary.api.factory import get_backend
    backend = get_backend()

而不是自己去 new LocalKnowledgeBackend——这样换实现不用改界面。
"""

from __future__ import annotations

from functools import lru_cache

from starport_dictionary.api.backend import SearchBackend
from starport_dictionary.api.local_backend import LocalKnowledgeBackend
from starport_dictionary.paths import packs_root


@lru_cache(maxsize=1)
def get_backend() -> SearchBackend:
    """拿当前启用的检索后端（缓存一份，避免重复加载知识库）。"""
    return LocalKnowledgeBackend(packs_root())


def reset_backend() -> None:
    """清掉缓存——测试和「重新载入知识库」用。"""
    get_backend.cache_clear()
