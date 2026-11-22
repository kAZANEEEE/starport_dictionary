# -*- coding: utf-8 -*-
"""验证 Release 附件真的可下载、且内容和本地 exe 一致（比 sha256）。

别只看"上传返回 201"——要证明别人点进去真能下、下到的还是那个文件。
"""

from __future__ import annotations

import hashlib
import os
import sys
import tempfile
from pathlib import Path

import requests

ROOT = Path(__file__).resolve().parents[1]
sys.stdout.reconfigure(encoding="utf-8", errors="replace")

URL = (
    "https://github.com/kAZANEEEE/starport_dictionary/releases/download/"
    "v0.1.0/StarportDictionary-v0.1.0-win64.exe"
)
LOCAL = ROOT / "dist" / "StarportDictionary.exe"


def sha256(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as f:
        for chunk in iter(lambda: f.read(1 << 20), b""):
            h.update(chunk)
    return h.hexdigest()


def main() -> int:
    proxy = os.environ.get("HTTPS_PROXY")
    proxies = {"http": proxy, "https": proxy} if proxy else None

    with requests.get(URL, stream=True, timeout=(30, 300), proxies=proxies) as r:
        print("HTTP", r.status_code)
        print("Content-Length:", r.headers.get("Content-Length"))
        print("Content-Type:", r.headers.get("Content-Type"))
        if r.status_code != 200:
            print(r.text[:300])
            return 1
        with tempfile.NamedTemporaryFile(suffix=".exe", delete=False) as tmp:
            got = 0
            for chunk in r.iter_content(1 << 20):
                tmp.write(chunk)
                got += len(chunk)
            temp_path = Path(tmp.name)

    local_sha, remote_sha = sha256(LOCAL), sha256(temp_path)
    print(f"下载大小: {got / 1024 / 1024:.1f} MB")
    print("本地 sha256:", local_sha)
    print("远端 sha256:", remote_sha)
    same = local_sha == remote_sha
    print("结果:", "✅ 完全一致（下到的就是本机这个 exe）" if same else "❌ 不一致")
    temp_path.unlink(missing_ok=True)
    return 0 if same else 2


if __name__ == "__main__":
    raise SystemExit(main())
