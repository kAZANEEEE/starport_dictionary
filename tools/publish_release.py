# -*- coding: utf-8 -*-
"""把 exe 作为 GitHub Release 附件上传。

2026-11-22：老大要「exe 挂附件上」，仓库不塞二进制，发 Release 挂载。
token 从 git 凭据管理器里取（`git credential fill`），不落盘、不打印。

跑法：
    set HTTP_PROXY=http://127.0.0.1:7877
    py -3 tools/publish_release.py
"""

from __future__ import annotations

import os
import subprocess
import sys
from pathlib import Path

import requests

ROOT = Path(__file__).resolve().parents[1]
sys.stdout.reconfigure(encoding="utf-8", errors="replace")

OWNER = "kAZANEEEE"
REPO = "starport_dictionary"
TAG = "v0.1.0"
EXE = ROOT / "dist" / "StarportDictionary.exe"
ASSET_NAME = "StarportDictionary-v0.1.0-win64.exe"

BODY = """## 这是什么

输入一句大白话，告诉你这活该怎么写 Python —— 附带逐句解释、四段式原理和坑。

**双击即用，不需要装 Python，不需要命令行，离线也能查。**

## 怎么用

1. 下载下面的 `StarportDictionary-v0.1.0-win64.exe`
2. 双击（首次启动约 3–5 秒，因为要解压内部资源）
3. 在搜索框里打你想做的事，比如「删除列表中的重复元素」
4. 回车 → 看结果 → 点进详情 → 复制代码

快捷键：`Enter` 搜索 · `↑` `↓` 选候选 · `Esc` 逐级返回 · `Ctrl+K` 回搜索框 · `Ctrl+Q` 退出

## 里面有什么

- 137 条知识，26 个模块（列表 / 字典 / 字符串 / 文件 / JSON / 正则 / 日期 / SQLite / 网络请求 / PySide6 …）
- 每条都带：一句话效果、调用签名、参数怎么填、返回什么、四段式原理、可复制代码、注意事项
- 每条代码都**真跑过一遍**（137 / 137 通过），不是抄的
- 详情页单独标出「使用前要不要 import」：内置能力 / 标准库 / 第三方（带 pip 命令）

## 已知缺口（不掩饰）

- 自然语言检索召回@5 约 72%：条目越多越低，词袋匹配已到天花板，下一步接 AI 重排
- 常用库还不全：GUI 组件、Excel、并发还没写
- 部分「相关知识」指向未收录条目，界面显示「未收录」

## 数据在哪

反馈和最近搜索写在 `%LOCALAPPDATA%\\StarportDictionary\\`，不上传任何数据。

反馈按钮（正确 / 不正确）会记下「原始查询 + 命中条目 + 全部候选」，攒着用来调检索。

---

> 发行说明由肥鱼（鲸鱼娘）撰写，老大已批准并审核。
> 技术内容与验收标准出自老大，文字整理是我做的。
"""


def get_token() -> str:
    out = subprocess.run(
        ["git", "credential", "fill"],
        input="protocol=https\nhost=github.com\n\n",
        capture_output=True,
        text=True,
        encoding="utf-8",
    )
    for line in out.stdout.splitlines():
        if line.startswith("password="):
            return line.split("=", 1)[1].strip()
    raise SystemExit("凭据里没有 github token")


def main() -> int:
    if not EXE.is_file():
        raise SystemExit(f"找不到 exe：{EXE}")

    token = get_token()
    session = requests.Session()
    session.headers.update(
        {
            "Authorization": f"Bearer {token}",
            "Accept": "application/vnd.github+json",
            "X-GitHub-Api-Version": "2022-11-28",
        }
    )
    proxies = {}
    if os.environ.get("HTTPS_PROXY"):
        proxies = {"http": os.environ["HTTPS_PROXY"], "https": os.environ["HTTPS_PROXY"]}
    session.proxies.update(proxies)

    api = f"https://api.github.com/repos/{OWNER}/{REPO}"

    # 1) 找现有 release，没有就建
    r = session.get(f"{api}/releases/tags/{TAG}", timeout=30)
    if r.status_code == 200:
        release = r.json()
        print("已有 release:", release["html_url"])
    else:
        payload = {
            "tag_name": TAG,
            "target_commitish": "main",
            "name": "Starport Dictionary V0.1",
            "body": BODY,
            "draft": False,
            "prerelease": False,
        }
        r = session.post(f"{api}/releases", json=payload, timeout=60)
        if r.status_code >= 300:
            print("建 release 失败:", r.status_code, r.text[:500])
            return 1
        release = r.json()
        print("已建 release:", release["html_url"])

    # 2) 已存在同名附件就先删（重跑不报错）
    for asset in release.get("assets", []):
        if asset["name"] == ASSET_NAME:
            session.delete(f"{api}/releases/assets/{asset['id']}", timeout=30)
            print("删掉旧附件:", ASSET_NAME)

    # 3) 上传
    upload_url = release["upload_url"].split("{")[0]
    size_mb = EXE.stat().st_size / 1024 / 1024
    print(f"上传中：{ASSET_NAME}（{size_mb:.1f} MB）…")
    with EXE.open("rb") as fh:
        r = session.post(
            upload_url,
            params={"name": ASSET_NAME, "label": "Windows x64 单文件"},
            data=fh,
            headers={"Content-Type": "application/octet-stream"},
            timeout=600,
        )
    if r.status_code >= 300:
        print("上传失败:", r.status_code, r.text[:500])
        return 1
    asset = r.json()
    print("上传完成:", asset["browser_download_url"], f"{asset['size'] / 1024 / 1024:.1f} MB")

    # 4) 复核：重新拉一次 release，确认附件在列表里
    check = session.get(f"{api}/releases/tags/{TAG}", timeout=30).json()
    names = [a["name"] for a in check.get("assets", [])]
    print("release 里的附件:", names)
    ok = ASSET_NAME in names
    print("结果:", "✅ 附件已挂上" if ok else "❌ 附件没挂上")
    return 0 if ok else 2


if __name__ == "__main__":
    raise SystemExit(main())
