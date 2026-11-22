# -*- coding: utf-8 -*-
"""上传 exe 到 v0.1.0 Release 的附件（修好卡住的问题）。

上一版卡住的原因：用文件对象上传时 requests 会走 chunked 编码，
GitHub 的上传端点对此处理很差 → 连接挂着不动。
这次读进内存 + 显式写 Content-Length，并且把进度实时写进文件方便观察。

跑法：
    set HTTP_PROXY=http://127.0.0.1:7877
    py -3 tools/upload_asset.py
"""

from __future__ import annotations

import json
import os
import subprocess
import sys
import time
from pathlib import Path

import requests

ROOT = Path(__file__).resolve().parents[1]
sys.stdout.reconfigure(encoding="utf-8", errors="replace")

OWNER, REPO, TAG = "kAZANEEEE", "starport_dictionary", "v0.1.0"
EXE = ROOT / "dist" / "StarportDictionary.exe"
ASSET_NAME = "StarportDictionary-v0.1.0-win64.exe"
PROGRESS = ROOT / "build" / "upload-progress.log"


def log(msg: str) -> None:
    line = f"{time.strftime('%H:%M:%S')} {msg}"
    print(line, flush=True)
    PROGRESS.parent.mkdir(parents=True, exist_ok=True)
    with PROGRESS.open("a", encoding="utf-8") as f:
        f.write(line + "\n")


def token() -> str:
    out = subprocess.run(
        ["git", "credential", "fill"],
        input="protocol=https\nhost=github.com\n\n",
        capture_output=True, text=True, encoding="utf-8",
    )
    return next(l.split("=", 1)[1].strip() for l in out.stdout.splitlines() if l.startswith("password="))


class ProgressFile:
    """包一层，边传边报进度（requests 要求可读对象有 read）。"""

    def __init__(self, data: bytes) -> None:
        self._data = data
        self._pos = 0
        self._last = 0.0

    def read(self, size: int = -1) -> bytes:
        if size is None or size < 0:
            chunk = self._data[self._pos:]
        else:
            chunk = self._data[self._pos:self._pos + size]
        self._pos += len(chunk)
        now = time.time()
        if now - self._last > 2 or self._pos >= len(self._data):
            pct = self._pos * 100 / len(self._data)
            log(f"  已传 {self._pos / 1024 / 1024:.1f} / {len(self._data) / 1024 / 1024:.1f} MB（{pct:.0f}%）")
            self._last = now
        return chunk

    def __len__(self) -> int:
        return len(self._data)


def main() -> int:
    if not EXE.is_file():
        raise SystemExit(f"找不到 exe：{EXE}")

    data = EXE.read_bytes()
    size = len(data)
    log(f"exe {size / 1024 / 1024:.1f} MB，开始上传")

    s = requests.Session()
    s.headers.update({
        "Authorization": f"Bearer {token()}",
        "Accept": "application/vnd.github+json",
        "X-GitHub-Api-Version": "2022-11-28",
    })
    proxy = os.environ.get("HTTPS_PROXY")
    if proxy:
        s.proxies.update({"http": proxy, "https": proxy})
        log(f"走代理 {proxy}")

    api = f"https://api.github.com/repos/{OWNER}/{REPO}"
    rel = s.get(f"{api}/releases/tags/{TAG}", timeout=30).json()

    for a in rel.get("assets", []):
        if a["name"] == ASSET_NAME:
            s.delete(f"{api}/releases/assets/{a['id']}", timeout=30)
            log("删掉同名旧附件")

    upload_url = rel["upload_url"].split("{")[0]
    started = time.time()
    r = s.post(
        upload_url,
        params={"name": ASSET_NAME, "label": "Windows x64 单文件"},
        data=ProgressFile(data),
        headers={
            "Content-Type": "application/octet-stream",
            "Content-Length": str(size),      # 关键：显式长度，别走 chunked
        },
        timeout=(30, 900),
    )
    log(f"HTTP {r.status_code}，耗时 {time.time() - started:.0f}s")
    if r.status_code >= 300:
        log("失败: " + r.text[:400])
        return 1

    asset = r.json()
    log(f"完成: {asset['browser_download_url']}")

    check = s.get(f"{api}/releases/tags/{TAG}", timeout=30).json()
    names = [a["name"] for a in check.get("assets", [])]
    log(f"复核附件: {names}")
    return 0 if ASSET_NAME in names else 2


if __name__ == "__main__":
    raise SystemExit(main())
