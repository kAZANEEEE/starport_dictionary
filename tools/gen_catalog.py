# -*- coding: utf-8 -*-
"""从条目自动生成知识目录 CATALOG.md。

2026-11-22 立：目录**只能自动生成**，不许手写——手写一定会和条目对不上。
生成位置：knowledge-packs/python-core/CATALOG.md

用法：
    set PYTHONPATH=src
    py -3 tools/gen_catalog.py
"""

from __future__ import annotations

import sys
from collections import defaultdict
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))

from starport_dictionary.knowledge.loader import load_pack  # noqa: E402

PACK_DIR = ROOT / "knowledge-packs" / "python-core"
OUT = PACK_DIR / "CATALOG.md"

ORIGIN_TITLE = {
    "builtin": ("内置能力（不用 import）", "Python 自带，直接写就行"),
    "stdlib": ("标准库（要 import）", "标准库里现成的，import 之后可用"),
    "thirdparty": ("第三方库（要 pip 装）", "需要先 pip install 才能用"),
}


def cell(text: str) -> str:
    """表格单元格：竖线必须转义，否则会把表拆坏。"""
    return str(text).replace("|", "｜")


def one_line(text: str) -> str:
    """描述取第一句，表格里不换行。"""
    first = text.strip().split("。")[0]
    return first.replace("|", "｜").strip()


def main() -> int:
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
    pack = load_pack(PACK_DIR)
    if pack.errors:
        print("有坏条目，先修再生成：", *pack.errors, sep="\n  ")

    groups: dict[str, dict[str, list]] = defaultdict(lambda: defaultdict(list))
    for e in pack.entries:
        origin = e.origin or "stdlib"
        groups[origin][e.module or "未分册"].append(e)

    lines = [
        "# Python 知识目录（自动生成，别手改）",
        "",
        "> 由 `tools/gen_catalog.py` 从条目头生成。改条目内容或加条目后重跑脚本。",
        "> 手改这份会在下次生成时被覆盖。",
        "",
        f"**共 {len(pack.entries)} 条**",
        "",
        "| 层 | 条数 |",
        "|---|---|",
    ]
    order = ["builtin", "stdlib", "thirdparty"]
    for origin in order:
        n = sum(len(v) for v in groups.get(origin, {}).values())
        if n:
            lines.append(f"| {ORIGIN_TITLE[origin][0]} | {n} |")

    for origin in order:
        if origin not in groups:
            continue
        title, note = ORIGIN_TITLE[origin]
        total = sum(len(v) for v in groups[origin].values())
        lines += ["", f"## {title} — {total} 条", "", f"_{note}_", ""]
        for module in sorted(groups[origin]):
            items = sorted(groups[origin][module], key=lambda x: x.qualname or x.id)
            lines += [
                f"### {module} — {len(items)} 条",
                "",
                "| 全名 | 中文名 | 一句话效果 | 要写的 import | id |",
                "|---|---|---|---|---|",
            ]
            for e in items:
                imp = f"`{e.import_stmt}`" if e.import_stmt else "—"
                lines.append(
                    f"| `{cell(e.qualname or e.id)}` | {cell(e.title)} | {one_line(e.description)} "
                    f"| {imp} | `{e.id}` |"
                )
            lines.append("")

    OUT.write_text("\n".join(lines), encoding="utf-8")
    print(f"已生成 {OUT}（{len(pack.entries)} 条）")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
