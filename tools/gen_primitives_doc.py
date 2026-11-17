# -*- coding: utf-8 -*-
"""把 primitives.py 里的受控词表生成成人看的 markdown。

为什么要有这一步：词表只能有**一个**事实源（代码里的 primitives.py）。
手写一份 markdown 备份，两边一定会对不上。所以文档是生成的。

用法：
    set PYTHONPATH=src
    py -3 tools/gen_primitives_doc.py
"""

from __future__ import annotations

import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))

from starport_dictionary.knowledge import primitives  # noqa: E402


def main() -> int:
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")

    lines = [
        "# 语义基元词表（自动生成，别手改）",
        "",
        "> 由 `tools/gen_primitives_doc.py` 从 `src/starport_dictionary/knowledge/primitives.py` 生成。",
        "> 要改就改那个 .py 文件，然后重跑脚本。手改这份会在下次生成时被覆盖。",
        "",
        f"## Object（{len(primitives.OBJECTS)} 个）",
        "",
        "| ID | 标准名称 | 别名 | 说明 |",
        "|---|---|---|---|",
    ]
    for oid, (name, aliases, desc) in primitives.OBJECTS.items():
        lines.append(f"| `{oid}` | {name} | {'、'.join(aliases)} | {desc} |")

    lines += [
        "",
        f"## Action（{len(primitives.ACTIONS)} 个）",
        "",
        "| ID | 标准名称 | 别名 | 说明 |",
        "|---|---|---|---|",
    ]
    for aid, (name, aliases, desc) in primitives.ACTIONS.items():
        lines.append(f"| `{aid}` | {name} | {'、'.join(aliases)} | {desc} |")

    lines += [
        "",
        "## 加新词的规矩",
        "",
        "1. 先查有没有语义相同的 ID，有就复用。",
        "2. 不因为中文叫法不同就新建（后缀 / 扩展名 → 都是 `file.extension`）。",
        "3. 真的新对象或新动作才加，并写清含义和适用范围。",
        "",
    ]

    out = ROOT / "docs" / "SEMANTIC_PRIMITIVES.md"
    out.write_text("\n".join(lines), encoding="utf-8")
    print(f"已生成 {out}（Object {len(primitives.OBJECTS)} 个，Action {len(primitives.ACTIONS)} 个）")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
