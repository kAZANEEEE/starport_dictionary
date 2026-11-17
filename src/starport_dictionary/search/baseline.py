r"""基线检索器：只靠 object/action 的别名去够用户那串字。

这是 11/17 晚的起点，故意做得笨——目的是**先量出「只靠语义基元能覆盖多少说法」**，
后面再上分词、FTS5、BM25 才有对比基准。

它**不看 utterances**。一旦把用户原话也当索引，"用原话搜原话"必然命中，测试就废了。

两个已经踩过的坑，写在这儿免得再踩：
1. 归一化不能把点也删掉。`".py"` 变成 `"py"` 之后，`"numpy"` 里就能搜到它。
2. 短查询要能命中长词：「重复」应该够到「重复项」，所以匹配是双向的，
   但短查询只给一半分——不然一个「值」字能命中文档里一切带值的条目。
"""

from __future__ import annotations

import re
from dataclasses import dataclass

from starport_dictionary.models.entry import Entry

WEIGHT_TITLE = 10
WEIGHT_OBJECT = 9
WEIGHT_ACTION = 7
WEIGHT_TARGET = 5
SHORT_QUERY_FACTOR = 0.5  # 反向包含（查询比词短）时打折

# 只去空白和中英文标点，**保留 . _ + -**：这些是技术词的一部分
_PUNCT = re.compile(r"[\s，。、?!？！,;；:：\"'“”‘’()（）\[\]【】<>《》~`|\\/]+")


def normalize(text: str) -> str:
    return _PUNCT.sub("", text.lower())


@dataclass(frozen=True)
class Hit:
    entry_id: str
    score: int
    matched_term: str


def _score_term(term: str, query_n: str) -> int:
    """返回命中强度 0/1/2：2=整词出现在查询里，1=查询被包含在词里。"""
    t = normalize(term)
    if not t:
        return 0
    if t in query_n:
        return 2
    if len(query_n) >= 2 and query_n in t:
        return 1
    return 0


def score_entry(entry: Entry, query: str) -> Hit | None:
    q = normalize(query)
    if not q:
        return None

    candidates: list[tuple[str, int]] = [(entry.title, WEIGHT_TITLE)]
    candidates += [(entry.obj.name, WEIGHT_OBJECT)]
    candidates += [(a, WEIGHT_OBJECT) for a in entry.obj.aliases]
    candidates += [(entry.action.name, WEIGHT_ACTION)]
    candidates += [(a, WEIGHT_ACTION) for a in entry.action.aliases]
    candidates += [(t, WEIGHT_TARGET) for t in entry.targets]

    best: Hit | None = None
    for term, weight in candidates:
        strength = _score_term(term, q)
        if strength == 0:
            continue
        score = weight if strength == 2 else int(weight * SHORT_QUERY_FACTOR)
        if best is None or score > best.score:
            best = Hit(entry.id, score, term)
    return best


def search(query: str, entries: list[Entry], limit: int = 5) -> list[Hit]:
    hits = [h for h in (score_entry(e, query) for e in entries) if h is not None]
    hits.sort(key=lambda h: (-h.score, h.entry_id))
    return hits[:limit]
