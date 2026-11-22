# -*- coding: utf-8 -*-
"""把 Starport 图标从 webp 转成应用要用的两种格式。

    assets/starport_icon.webp   原始图（1254x1254）
    assets/icon.png             512x512，窗口图标 / 首页展示
    assets/icon.ico             多尺寸，exe 图标（Windows 任务栏/资源管理器）

跑法： py -3 tools/make_icon.py
"""

from __future__ import annotations

import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.stdout.reconfigure(encoding="utf-8", errors="replace")

from PIL import Image  # noqa: E402

ASSETS = ROOT / "assets"
SRC = ASSETS / "starport_icon.webp"
PNG = ASSETS / "icon.png"
ICO = ASSETS / "icon.ico"

# Windows 图标标准尺寸（小到任务栏 16，大到 256）
ICO_SIZES = [(16, 16), (24, 24), (32, 32), (48, 48), (64, 64), (128, 128), (256, 256)]


def main() -> int:
    if not SRC.is_file():
        print("找不到原图:", SRC)
        return 1

    img = Image.open(SRC).convert("RGBA")
    print("原图:", img.size)

    # 窗口图标：512 够用，体积也小
    img.resize((512, 512), Image.LANCZOS).save(PNG, format="PNG", optimize=True)
    print("已写:", PNG, PNG.stat().st_size // 1024, "KB")

    # exe 图标：把最大尺寸那张作为基准，其余交给 Pillow 生成
    img.resize((256, 256), Image.LANCZOS).save(ICO, format="ICO", sizes=ICO_SIZES)
    print("已写:", ICO, ICO.stat().st_size // 1024, "KB")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
