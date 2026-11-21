# -*- coding: utf-8 -*-
"""手动跑一遍：读整个知识包 → 打印条目摘要 → 用几种说法搜一遍。

    set PYTHONPATH=src
    py -3 demo_parse.py
"""

from __future__ import annotations

import sys
from pathlib import Path

sys.stdout.reconfigure(encoding="utf-8", errors="replace")

from starport_dictionary.knowledge.loader import load_all_packs
from starport_dictionary.search.baseline import search

ROOT = Path(__file__).resolve().parent
packs = load_all_packs(ROOT / "knowledge-packs")

entries = []
for pack in packs:
    print(f"知识包 {pack.id} v{pack.version}：{len(pack.entries)} 条，错误 {len(pack.errors)} 条")
    for err in pack.errors:
        print("   ", err)
    entries.extend(pack.entries)
print()

for e in entries:
    print(f"[{e.id}] {e.title}")
    print(f"    对象 {e.obj.id}（{e.obj.name}）  动作 {e.action.id}（{e.action.name}）")
    print(f"    别名 {len(e.obj.aliases)} + {len(e.action.aliases)} 条，"
          f"说法 {sum(len(v) for v in e.utterances.values())} 条")
    print(f"    版本 {e.min_version}+，实测 {', '.join(e.tested_versions)}")
    if e.ambiguity:
        print(f"    歧义提示：{e.ambiguity[0].note}")
print()

queries = [
    "后缀",
    "判断文件后缀",
    "看看是不是 py 文件",
    "我想知道文件名最后面是什么",
    "列表去重",
    "去重",
    "怎么用 numpy 做矩阵乘法",
]
print("搜索演示：")
for q in queries:
    hits = search(q, entries)
    if hits:
        top = hits[0]
        terms = "、".join(top.matched_terms)
        print(f"  {q!r:32} → {top.entry_id}  (分数 {top.score}, 命中 {terms})")
    else:
        print(f"  {q!r:32} → 没找到")
