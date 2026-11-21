# -*- coding: utf-8 -*-
"""统计当前命中情况，用于把技术债写清楚（不是裁决，只是报数）。"""
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))
sys.stdout.reconfigure(encoding="utf-8", errors="replace")

from starport_dictionary.knowledge.loader import load_all_packs
from starport_dictionary.search.baseline import search

entries = [e for p in load_all_packs(ROOT / "knowledge-packs") for e in p.entries]
cats = ["direct", "questions", "colloquial", "goal_based", "technical", "short_queries"]

print(f"条目 {len(entries)} 条\n")
grand_total = grand_top1 = grand_top3 = 0
for cat in cats:
    total = top1 = top3 = 0
    misses = []
    for e in entries:
        for utt in e.utterances.get(cat, ()):
            total += 1
            hits = search(utt, entries, limit=5)
            rank = 999
            for i, h in enumerate(hits, start=1):
                if h.entry_id == e.id:
                    rank = i
                    break
            if rank == 1:
                top1 += 1
            if rank <= 3:
                top3 += 1
            if rank != 1:
                misses.append((utt, e.id, rank, hits[0].entry_id if hits else None))
    grand_total += total
    grand_top1 += top1
    grand_top3 += top3
    print(f"{cat:14} 共 {total:3}  排第一 {top1:3}  进前三 {top3:3}")
    for utt, eid, rank, top in misses:
        print(f"      未中：{utt}  期望 {eid}，第 {rank} 名（第一 {top}）")

print()
print(f"合计 {grand_total} 条说法：排第一 {grand_top1}（{grand_top1/grand_total:.0%}），"
      f"进前三 {grand_top3}（{grand_top3/grand_total:.0%}）")
