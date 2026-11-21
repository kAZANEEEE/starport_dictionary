# -*- coding: utf-8 -*-
"""量一下：条目变多之后，现在这套全量遍历的检索会不会变慢。

做法：把现有 16 条复制若干份（改 id 避免冲突），模拟更大规模，测单次搜索耗时。
"""
import sys
import time
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))
sys.stdout.reconfigure(encoding="utf-8", errors="replace")

from dataclasses import replace

from starport_dictionary.knowledge.loader import load_all_packs
from starport_dictionary.search.baseline import search

base = [e for p in load_all_packs(ROOT / "knowledge-packs") for e in p.entries]
print(f"基础条目：{len(base)} 条\n")

QUERY = "怎么判断文件后缀"
REPEAT = 200

for mult in (1, 10, 30, 60):
    entries = [replace(e, id=f"{e.id}_v{i}") for i in range(mult) for e in base]
    # 预热
    search(QUERY, entries)
    t0 = time.perf_counter()
    for _ in range(REPEAT):
        search(QUERY, entries)
    dt = (time.perf_counter() - t0) / REPEAT
    print(f"条目 {len(entries):5} 条 → 单次搜索 {dt*1000:7.2f} ms")
