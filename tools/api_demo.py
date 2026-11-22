# -*- coding: utf-8 -*-
"""P0 命令行 demo：不开界面，先验证「一句大白话 → 候选 → 详情」这条路通。

    set PYTHONPATH=src
    py -3 tools/api_demo.py 判断文件后缀
"""

from __future__ import annotations

import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))
sys.stdout.reconfigure(encoding="utf-8", errors="replace")

from starport_dictionary.api.factory import get_backend  # noqa: E402


def show(query: str) -> None:
    backend = get_backend()
    stats = backend.stats()
    print(f"库：{stats.entry_count} 条 / {stats.module_count} 个模块\n")

    resp = backend.search(query, limit=5)
    print(f"查询：{query}")
    if not resp.has_results:
        print("（没找到）")
        return

    print(f"命中 {len(resp.hits)} 条\n")
    best = resp.best
    print(f"★ 最佳匹配：{best.title}  [{best.entry_id}]  分数 {best.score}")
    print(f"  命中词：{'、'.join(best.matched_terms)}")

    entry = backend.get_entry(best.entry_id)
    if entry:
        hint = entry.import_hint
        if hint.kind == "builtin":
            imp = "内置能力，无需导入"
        elif hint.kind == "thirdparty":
            imp = f"{hint.install} 然后 {hint.statement}"
        elif hint.kind == "stdlib":
            imp = hint.statement
        else:
            imp = "未标注"
        print(f"  导入：{imp}")
        print(f"  效果：{entry.description.splitlines()[0][:60]}")
        print(f"  签名：{entry.signature}")
        print(f"  返回：{entry.returns}")
        print(f"  参数：{len(entry.args)} 个   相关：{len(entry.related)} 条")

    if resp.others:
        print("\n其他候选：")
        for h in resp.others:
            print(f"  · {h.title}  [{h.entry_id}]  {h.score}")


if __name__ == "__main__":
    q = " ".join(sys.argv[1:]) or "判断文件后缀"
    show(q)
