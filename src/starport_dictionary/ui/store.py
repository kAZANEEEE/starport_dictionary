r"""反馈与最近搜索的本地存储（json / jsonl），不需要服务器。

2026-11-22 设计：
- 反馈文件是 **jsonl（一行一条）**：追加写、坏一行不影响别的行，方便以后直接当训练/评测数据。
- 每条反馈记下「原始查询 + 命中 + 候选 + 判断」，这样才可能复现用户当时看到的界面。
- 最近搜索只保存查询词（最多 5 条，去重），不记录任何个人信息。
"""

from __future__ import annotations

import json
import logging
from dataclasses import asdict, dataclass, field
from datetime import datetime
from pathlib import Path

from starport_dictionary.paths import feedback_file, recent_file

log = logging.getLogger(__name__)
MAX_RECENT = 5


@dataclass
class FeedbackRecord:
    query: str
    verdict: str                     # "ok" | "bad"
    best_entry_id: str = ""
    best_title: str = ""
    candidates: list[str] = field(default_factory=list)
    backend: str = "local"
    app_version: str = "0.1.0"
    created_at: str = ""

    def __post_init__(self) -> None:
        if not self.created_at:
            self.created_at = datetime.now().isoformat(timespec="seconds")


class FeedbackStore:
    """反馈落盘：追加写 jsonl，写失败只记日志、不打断用户操作。"""

    def __init__(self, path: Path | None = None) -> None:
        self.path = Path(path) if path else feedback_file()

    def add(self, record: FeedbackRecord) -> bool:
        try:
            self.path.parent.mkdir(parents=True, exist_ok=True)
            with self.path.open("a", encoding="utf-8") as f:
                f.write(json.dumps(asdict(record), ensure_ascii=False) + "\n")
            return True
        except OSError:
            log.exception("写反馈失败")
            return False

    def count(self) -> int:
        if not self.path.is_file():
            return 0
        try:
            with self.path.open("r", encoding="utf-8") as f:
                return sum(1 for line in f if line.strip())
        except OSError:
            return 0

    def load_all(self) -> list[dict]:
        if not self.path.is_file():
            return []
        out: list[dict] = []
        try:
            with self.path.open("r", encoding="utf-8") as f:
                for line in f:
                    line = line.strip()
                    if not line:
                        continue
                    try:
                        out.append(json.loads(line))
                    except json.JSONDecodeError:
                        continue          # 坏行跳过，不影响其他数据
        except OSError:
            log.exception("读反馈失败")
        return out


class RecentStore:
    """最近搜索：最多 5 条，新的在前，重复的提到最前。"""

    def __init__(self, path: Path | None = None, limit: int = MAX_RECENT) -> None:
        self.path = Path(path) if path else recent_file()
        self.limit = limit

    def load(self) -> list[str]:
        if not self.path.is_file():
            return []
        try:
            data = json.loads(self.path.read_text(encoding="utf-8"))
        except (OSError, json.JSONDecodeError):
            return []
        if not isinstance(data, list):
            return []
        return [str(x) for x in data][: self.limit]

    def add(self, query: str) -> list[str]:
        q = (query or "").strip()
        items = self.load()
        if not q:
            return items
        items = [x for x in items if x != q]
        items.insert(0, q)
        items = items[: self.limit]
        self._save(items)
        return items

    def clear(self) -> None:
        self._save([])

    def _save(self, items: list[str]) -> None:
        try:
            self.path.parent.mkdir(parents=True, exist_ok=True)
            self.path.write_text(json.dumps(items, ensure_ascii=False), encoding="utf-8")
        except OSError:
            log.exception("写最近搜索失败")
