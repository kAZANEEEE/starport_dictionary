r"""utterance 命中测试 —— 这个项目的第一份成绩单。

玩法：把每条条目自己写的用户原话，逐句喂给基线检索器。
检索器**只认识** title / object 别名 / action 别名 / targets，不认识这些原话。

所以命中说明"翻译"真的发生了一次；不命中就是真问题，后面要补分词或加词。

判据：
- direct / questions / short_queries 这三类必须全中（用户就是这么说话的）；
- colloquial 允许挂——挂了就是知道了"这句话现在的模型够不到"。
"""

from __future__ import annotations

from pathlib import Path

import pytest

from starport_dictionary.knowledge.loader import load_all_packs
from starport_dictionary.search.baseline import search

ROOT = Path(__file__).resolve().parents[1]
PACKS = ROOT / "knowledge-packs"

STRICT_CATEGORIES = {"direct", "questions", "short_queries"}


def all_entries():
    entries = []
    for pack in load_all_packs(PACKS):
        entries.extend(pack.entries)
    return entries


def test_核心类别必须命中():
    entries = all_entries()
    assert len(entries) >= 2, "干扰条目太少，测不出区分能力"

    missed = []
    for entry in entries:
        for cat in STRICT_CATEGORIES:
            for utt in entry.utterances.get(cat, ()):
                hits = search(utt, entries)
                top = hits[0].entry_id if hits else None
                if top != entry.id:
                    missed.append((entry.id, cat, utt, top))

    if missed:
        lines = "\n".join(
            f"  [{cat}] {utt!r}  期望 {eid}，实际 {top}" for eid, cat, utt, top in missed
        )
        pytest.fail(f"核心类别有 {len(missed)} 条没命中：\n{lines}")


def test_不同对象不会互相污染():
    """“列表去重”不能被“后缀”那条抢走，反过来也一样。"""
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
