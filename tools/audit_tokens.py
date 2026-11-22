# -*- coding: utf-8 -*-
"""量化检查：数一数当前 QSS 里有多少颜色/字号/圆角/阴影。

这是"AI 味"能不能被证伪的入口——印象不算证据，计数才算。
"""

from __future__ import annotations

import re
import sys
from pathlib import Path

ROOT = Path(r"D:\some_project\Starport-Dictionary")
sys.stdout.reconfigure(encoding="utf-8", errors="replace")

QSS = ROOT / "src" / "starport_dictionary" / "ui" / "resources" / "dark.qss"


def slug(text: str) -> str:
    """只留 ASCII，避免控制台编码问题。"""
    return re.sub(r"[^\x00-\x7f]", "", text)


def main() -> int:
    t = QSS.read_text(encoding="utf-8")

    hexes = sorted({m.group(0).lower() for m in re.finditer(r"#[0-9a-fA-F]{3,8}\b", t)})
    sizes = sorted({int(m.group(1)) for m in re.finditer(r"font-size:\s*(\d+)px", t)})
    radii = sorted({int(m.group(1)) for m in re.finditer(r"border-radius:\s*(\d+)px", t)})
    pads = sorted({m.group(1) for m in re.finditer(r"padding:\s*([^;]+);", t)})
    fonts = sorted({m.group(1).strip() for m in re.finditer(r"font-family:\s*([^;]+);", t)})
    shadows = len(re.findall(r"box-shadow", t))
    borders = len(re.findall(r"border:\s*1px solid", t))

    print("=== current tokens ===")
    print(f"hex colors      : {len(hexes)}")
    for i in range(0, len(hexes), 6):
        print("   " + " ".join(hexes[i:i + 6]))
    print(f"font sizes      : {len(sizes)} -> {sizes}")
    print(f"border radii    : {len(radii)} -> {radii}")
    print(f"padding variants: {len(pads)}")
    print(f"font families   : {len(fonts)}")
    for f in fonts:
        print("   " + slug(f))
    print(f"box shadows     : {shadows}")
    print(f"hairline borders: {borders}")

    # 规则数 vs 选择器数，看看有多少"盒子"
    print(f"rules           : {len(re.findall(r'\{', t))}")
    print(f"rounded boxes   : {len(re.findall(r'border-radius', t))}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
