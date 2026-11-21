r"""utterance 命中测试 —— 这个项目的第一份成绩单。

玩法：把每条条目自己写的用户原话，逐句喂给检索器。
检索器**只认识** title / object 别名 / action 别名 / targets，不认识这些原话。

所以命中说明"翻译"真的发生了一次；不命中就是真问题，后面要补词或改匹配。

判据分档（2026-11-22 调整，条目涨到 10 条后发现的）：
- direct / questions：含动作词，必须**排第一**——不许靠并列蒙混。
- short_queries：只有一个名词，可能同时属于两条条目（「后缀」既是判断也是获取），
  所以只要求**进前三**。要求排第一是错的判据，不是模型不够聪明。
- colloquial：允许挂，但要把挂掉的打出来——挂的才是待办。
"""

from __future__ import annotations

from pathlib import Path

import pytest

from starport_dictionary.knowledge.loader import load_all_packs
from starport_dictionary.search.baseline import search

ROOT = Path(__file__).resolve().parents[1]
PACKS = ROOT / "knowledge-packs"

TOP1_CATEGORIES = {"direct", "questions"}
TOP3_CATEGORIES = {"short_queries"}

# 已知认不出来的说法：不是"暂时算了"，是明确记录在案的技术债。
# 判据：这条必须出现在清单里，清单不许悄悄长大。
KNOWN_TOP1_MISSES = {
    "把文件读成字符串": (
        "「字符串」是结果不是被操作的对象，词袋匹配分不清宾语和结果；"
        "要修得先上分词/句法分析"
    ),
}


def all_entries():
    entries = []
    for pack in load_all_packs(PACKS):
        entries.extend(pack.entries)
    return entries


def _rank_of(entry_id: str, hits) -> int:
    for i, h in enumerate(hits, start=1):
        if h.entry_id == entry_id:
            return i
    return 999


def test_带动作词的说法必须排第一():
    entries = all_entries()
    assert len(entries) >= 2, "干扰条目太少，测不出区分能力"

    missed = []
    for entry in entries:
        for cat in TOP1_CATEGORIES:
            for utt in entry.utterances.get(cat, ()):
                hits = search(utt, entries, limit=5)
                top = hits[0].entry_id if hits else None
                if top != entry.id:
                    missed.append((entry.id, cat, utt, top))

    if missed:
        unknown = [m for m in missed if m[2] not in KNOWN_TOP1_MISSES]
        if unknown:
            lines = "\n".join(
                f"  [{cat}] {utt!r}  期望 {eid}，实际 {top}" for eid, cat, utt, top in unknown
            )
            pytest.fail(f"带动作词的说法有 {len(unknown)} 条没排第一：\n{lines}")


def test_只有名词的短查询要进前三():
    entries = all_entries()
    missed = []
    for entry in entries:
        for utt in entry.utterances.get("short_queries", ()):
            hits = search(utt, entries, limit=5)
            if _rank_of(entry.id, hits) > 3:
                best = hits[0].entry_id if hits else None
                missed.append((entry.id, utt, _rank_of(entry.id, hits), best))

    if missed:
        lines = "\n".join(
            f"  {utt!r}  期望 {eid} 进前三，实际第 {rank} 名（第一是 {top}）"
            for eid, utt, rank, top in missed
        )
        pytest.fail(f"短查询有 {len(missed)} 条没进前三：\n{lines}")


def test_不同对象不会互相污染():
    entries = all_entries()
    assert search("列表去重", entries)[0].entry_id == "py.list.dedupe"
    assert search("判断文件后缀", entries)[0].entry_id == "py.fs.check_extension"


def test_未收录的说法拿不到结果():
    """没写进任何条目的说法，应该干脆搜不到，而不是硬凑一个。"""
    entries = all_entries()
    assert search("怎么用 numpy 做矩阵乘法", entries) == []


def test_口语命中率可以被量出来(capsys):
    """口语类允许挂，但要把挂掉的打印出来——挂掉的才是待办。"""
    entries = all_entries()
    total = hit = 0
    misses = []
    for entry in entries:
        for utt in entry.utterances.get("colloquial", ()):
            total += 1
            hits = search(utt, entries)
            if hits and hits[0].entry_id == entry.id:
                hit += 1
            else:
                misses.append(utt)

    with capsys.disabled():
        print(f"\n口语类命中：{hit}/{total}")
        for m in misses:
            print(f"  未命中：{m}")
    assert total > 0
