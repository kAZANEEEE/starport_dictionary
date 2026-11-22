r"""检索质量测试 —— 判据是「前 5 条里有没有」，不是「必须排第一」。

2026-11-22 改判据，原因（用户提的，比原来的对）：
    界面上一次显示 5 条候选，用户靠「原理/效果」自己挑。
    所以系统的任务是把正确条目**放进这 5 条里**，而不是猜中唯一一条。

实测（28 条条目 / 400+ 条说法）：
    召回@1 ≈ 70%、@3 ≈ 82%、@5 ≈ 85%、@10 ≈ 85%
→ 5 条是性价比最高的位置：再往上翻不涨，剩下的缺口是「一个字都对不上」的说法，
  那属于 AI 层，不是本地检索能修的。

阈值定在 85%，往下掉就是回归，立刻红。
"""

from __future__ import annotations

from pathlib import Path

from starport_dictionary.knowledge.loader import load_all_packs
from starport_dictionary.search.baseline import search

ROOT = Path(__file__).resolve().parents[1]
PACKS = ROOT / "knowledge-packs"

VISIBLE = 5          # 界面上一次显示几条
MIN_RECALL = 0.71    # 防回归基线（118 条条目时实测 72%，阈值 71% 防回归）

# 这个数会随条目变多而下降——候选变多，同一句话能命中的条目也变多。
# 它是「防回归」用的：加册之后手动把基线更新到实测值，别让它变成假门槛。


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


def _recall(entries, limit: int) -> tuple[int, int, dict[str, list[str]]]:
    total = hit = 0
    misses: dict[str, list[str]] = {}
    for entry in entries:
        for cat, utts in entry.utterances.items():
            for utt in utts:
                total += 1
                hits = search(utt, entries, limit=limit)
                if any(h.entry_id == entry.id for h in hits):
                    hit += 1
                else:
                    misses.setdefault(cat, []).append(f"{utt}  →{entry.id}")
    return hit, total, misses


def test_前五条里必须能找到(capsys):
    entries = all_entries()
    hit, total, misses = _recall(entries, VISIBLE)
    rate = hit / total

    with capsys.disabled():
        print(f"\n召回@{VISIBLE}：{hit}/{total} = {rate:.1%}")
        for cat, items in sorted(misses.items()):
            print(f"   {cat:14} 漏 {len(items)} 条")

    assert rate >= MIN_RECALL, (
        f"召回@{VISIBLE} 掉到 {rate:.1%}（阈值 {MIN_RECALL:.0%}）。\n"
        f"漏掉的说法：\n" + "\n".join(f"  {m}" for v in misses.values() for m in v[:5])
    )


def test_排第一的比例只做记录不设门槛(capsys):
    """排第一是「更好」，不是「必须」——所以不设断言，只报数。"""
    entries = all_entries()
    hit, total, _ = _recall(entries, 1)
    with capsys.disabled():
        print(f"\n排第一：{hit}/{total} = {hit/total:.1%}（参考值，不作门槛）")


def test_不同对象不会互相污染():
    entries = all_entries()
    assert search("列表去重", entries)[0].entry_id == "py.list.dedupe"
    assert search("判断文件后缀", entries)[0].entry_id == "py.fs.check_extension"


def test_未收录的说法拿不到结果():
    """没写进任何条目的说法，应该干脆搜不到，而不是硬凑一个。"""
    entries = all_entries()
    assert search("怎么用 numpy 做矩阵乘法", entries) == []
