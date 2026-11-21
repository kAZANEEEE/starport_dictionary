r"""utterance 命中测试 —— 这个项目的第一份成绩单。

玩法：把每条条目自己写的用户原话，逐句喂给检索器。
检索器**只认识** title / object 别名 / action 别名 / targets，不认识这些原话。

判据分档（2026-11-22 第三次校准，条目 16 条后定的）：
- direct / questions：含动作词，要求**排第一**。
- short_queries：只有一个名词，可能同时属于两条条目（「后缀」既是判断也是获取），
  要求**进前三**。
- colloquial / goal_based / technical：允许挂，挂掉的在 tools/report_hits.py 里列出来。

底下 KNOWN_TOP1_MISSES / KNOWN_TOP3_MISSES 是**明确记账的技术债**：
每条都得写清为什么现在认不出来。清单不许悄悄长大——新挂的说法会让测试红。
当前真实水平（253 条说法）：排第一 77%，进前三 82%。
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

# “词袋匹配分不清宾语和结果”：句子里提到的东西不是被操作的对象
_OBJ_CONFUSION = "宾语/结果词抢了对象的位置，词袋分不清"

KNOWN_TOP1_MISSES = {
    "按 key 取值": "「key」没进任何别名，只剩「取值」这种泛词",
    "检查文件有没有": "「有没有」被当作存在性泛词，压过了动作",
    "把文件读成字符串": _OBJ_CONFUSION,
    "校验文件有没有被改过": _OBJ_CONFUSION,
    "把 json 读成字典": "「字典」是结果不是对象（json 才是）",
    "把一行拆成多段": "「多段」不是词表里的词",
    "字符串转列表": _OBJ_CONFUSION,
    "怎么算程序跑了多久": "「跑了多久」= 计时，词表里没有这个概念",
    "键不存在的时候怎么返回默认值": "整句是条件+动作，无对象词命中",
    "怎么区分文件还是目录": "「区分」属于比较类，但对象是文件类型，跨了两个基元",
    "如何比较两个文件是否相同": "「相同」需要比较基元+文件对象组合，当前无此条目",
    "如何按字典里的某个键排序": "「字典」与排序对象错配（排序的是列表）",
    "怎么去掉多余的空格再切": "两个动作叠加（去空格 + 切分），词袋只能取一个",
}

KNOWN_TOP3_MISSES = {
    "取值": "「取值」是动作泛词，被列表查找抢走",
    "校验": "「校验」同时属于判断和哈希，两处都命中",
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

    unknown = []
    for entry in entries:
        for cat in TOP1_CATEGORIES:
            for utt in entry.utterances.get(cat, ()):
                if utt in KNOWN_TOP1_MISSES:
                    continue
                hits = search(utt, entries, limit=5)
                top = hits[0].entry_id if hits else None
                if top != entry.id:
                    unknown.append((entry.id, cat, utt, top))

    if unknown:
        lines = "\n".join(
            f"  [{cat}] {utt!r}  期望 {eid}，实际 {top}" for eid, cat, utt, top in unknown
        )
        pytest.fail(f"出现 {len(unknown)} 条**新的**没排第一（不在技术债清单里）：\n{lines}")


def test_只有名词的短查询要进前三():
    entries = all_entries()
    unknown = []
    for entry in entries:
        for utt in entry.utterances.get("short_queries", ()):
            if utt in KNOWN_TOP3_MISSES:
                continue
            hits = search(utt, entries, limit=5)
            rank = _rank_of(entry.id, hits)
            if rank > 3:
                unknown.append((entry.id, utt, rank, hits[0].entry_id if hits else None))

    if unknown:
        lines = "\n".join(
            f"  {utt!r}  期望 {eid} 进前三，实际第 {rank} 名（第一是 {top}）"
            for eid, utt, rank, top in unknown
        )
        pytest.fail(f"出现 {len(unknown)} 条**新的**短查询没进前三：\n{lines}")


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
    assert total > 0
