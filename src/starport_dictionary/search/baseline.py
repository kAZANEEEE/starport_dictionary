r"""基线检索器：只靠 object/action 的别名去够用户那串字。

第二版（2026-11-22）：条目涨到 10 条之后，第一版暴露出两个真问题，改了两处。

1. **别名要并上词表里的**。同是 `list.element`，有的条目写了「列表」有的没写，
   结果「一个值在不在列表里」被判给了排序条目。别名是**对象**的属性，
   不该由每条条目自己重抄一遍——所以检索时把 primitives 的别名一起并进来。

2. **分数要相加不要取最大**。原来取单个最高分，于是「字符串」+「替换」两个组
   都命中的条目，和只命中「内容」一个组的条目打平。命中的组越多越可信，
   这就得相加。

它**不看 utterances**。一旦把用户原话也当索引，"用原话搜原话"必然命中，测试就废了。
"""

from __future__ import annotations

import math
import re
from dataclasses import dataclass

from starport_dictionary.knowledge import primitives
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
    matched_terms: tuple[str, ...]


def _strength(term: str, query_n: str) -> int:
    """0=没命中，2=整词出现在查询里，1=查询被包含在词里（短查询）。"""
    t = normalize(term)
    if not t:
        return 0
    if t in query_n:
        return 2
    if len(query_n) >= 2 and query_n in t:
        return 1
    return 0


def _best(terms, query_n: str, weight: int, df: dict[str, int], n_entries: int) -> tuple[int, list[str]]:
    """一组同类的词（如某对象的所有别名），返回该组能拿到的最高分和命中的词。

    IDF 加权：像「文件」「列表」这种几乎每条条目都收的词，区分度为零，
    权重必须压低；「isfile」「md5」这种只有一条收的词，命中就是强信号。
    没有 IDF 的话，任何一句话都会命中一堆条目，最后靠 id 字母序决定胜负。
    """
    best_score = 0
    hits: list[str] = []
    for term in terms:
        s = _strength(term, query_n)
        if s == 0:
            continue
        base = weight if s == 2 else int(weight * SHORT_QUERY_FACTOR)
        idf = math.log(1 + n_entries / max(1, df.get(normalize(term), 1)))
        score = round(base * idf)
        if score > best_score:
            best_score = score
            hits = [term]
        elif score == best_score and term not in hits:
            hits.append(term)
    return best_score, hits


def _object_terms(entry: Entry) -> tuple[str, ...]:
    """条目自己写的别名 + 词表里该对象的别名（并集，去重保序）。"""
    vocab = ()
    if entry.obj.id in primitives.OBJECTS:
        vocab = primitives.OBJECTS[entry.obj.id][1]
    merged = [entry.obj.name, *entry.obj.aliases, *vocab]
    return tuple(dict.fromkeys(merged))


def _action_terms(entry: Entry) -> tuple[str, ...]:
    vocab = ()
    if entry.action.id in primitives.ACTIONS:
        vocab = primitives.ACTIONS[entry.action.id][1]
    merged = [entry.action.name, *entry.action.aliases, *vocab]
    return tuple(dict.fromkeys(merged))


def score_entry(entry: Entry, query: str, df: dict[str, int] | None = None, n_entries: int = 1) -> Hit | None:
    q = normalize(query)
    if not q:
        return None
    df = df or {}
    if not df:
        n_entries = max(1, n_entries)

    score = 0
    matched: list[str] = []

    for terms, weight in (
        ((entry.title,), WEIGHT_TITLE),
        (_object_terms(entry), WEIGHT_OBJECT),
        (_action_terms(entry), WEIGHT_ACTION),
        (entry.targets, WEIGHT_TARGET),
    ):
        s, hits = _best(terms, q, weight, df, n_entries)
        score += s
        matched.extend(hits)

    if score == 0:
        return None
    return Hit(entry.id, score, tuple(matched))


def _document_frequency(entries: list[Entry]) -> dict[str, int]:
    """每个词被多少条条目收录——用来算 IDF。"""
    df: dict[str, int] = {}
    for e in entries:
        terms = {normalize(t) for t in (e.title, *_object_terms(e), *_action_terms(e), *e.targets) if t}
        for t in terms:
            df[t] = df.get(t, 0) + 1
    return df


def search(query: str, entries: list[Entry], limit: int = 5) -> list[Hit]:
    df = _document_frequency(entries)
    n = max(1, len(entries))
    hits = [h for h in (score_entry(e, query, df, n) for e in entries) if h is not None]
    hits.sort(key=lambda h: (-h.score, h.entry_id))
    return hits[:limit]
