r"""把一条 Markdown 知识条目解析成 Entry。

格式见 docs/KNOWLEDGE_FORMAT.md：
    +++ 开头、+++ 结束的 TOML 头
    正文固定五节：代码 / 功能描述 / 逐句解释 / 原理解释 / 注意事项

设计取舍：
1. 用 tomllib（3.11+ 自带）解析头部，不引入 PyYAML——少一个依赖少一处踩坑。
2. 正文按 "## 标题" 切段，标题顺序必须对。缺节直接报错，
   因为「代码有、解释没有」的条目用起来比搜不到还难受。
3. 报错要带文件名和具体字段，不然知识包一多根本查不出是哪条坏了。
"""

from __future__ import annotations

import re
import tomllib
from pathlib import Path

from starport_dictionary.models.entry import Entry

FRONT_MATTER_MARK = "+++"
REQUIRED_FIELDS = (
    "id",
    "title",
    "language",
    "category_id",
    "status",
    "scenario",
    "aliases",
    "tags",
    "tested_versions",
)
REQUIRED_SECTIONS = ("代码", "功能描述", "逐句解释", "原理解释", "注意事项")
VALID_STATUS = {"draft", "reviewed", "tested", "deprecated"}
ID_PATTERN = re.compile(r"^[a-z][a-z0-9_]*(\.[a-z0-9_]+){2,}$")


class EntryFormatError(Exception):
    """条目格式不对。message 里必须带出文件名和具体哪个字段。"""


def parse_entry_file(path: Path) -> Entry:
    path = Path(path)
    text = path.read_text(encoding="utf-8")
    front, body = _split_front_matter(path, text)
    meta = _parse_toml(path, front)
    _check_required_fields(path, meta)
    sections = _split_sections(path, body)
    return _build_entry(path, meta, sections)


# ---------- 头部 ----------
def _split_front_matter(path: Path, text: str) -> tuple[str, str]:
    """把文件切成 (TOML 头, 正文)。找不到成对的 +++ 就报错。"""
    stripped = text.lstrip("\ufeff")
    if not stripped.startswith(FRONT_MATTER_MARK):
        raise EntryFormatError(f"{path.name}: 文件开头缺少 +++ 头")

    parts = stripped.split(FRONT_MATTER_MARK)
    if len(parts) < 3:
        raise EntryFormatError(f"{path.name}: +++ 没有成对出现")
    # parts[0] 是空串，parts[1] 是 TOML，parts[2:] 拼回正文
    return parts[1], FRONT_MATTER_MARK.join(parts[2:])


def _parse_toml(path: Path, front: str) -> dict:
    try:
        return tomllib.loads(front)
    except tomllib.TOMLDecodeError as exc:
        raise EntryFormatError(f"{path.name}: 头部不是合法 TOML（{exc}）") from exc


def _check_required_fields(path: Path, meta: dict) -> None:
    missing = [f for f in REQUIRED_FIELDS if f not in meta]
    if missing:
        raise EntryFormatError(f"{path.name}: 缺字段 {missing}")

    for f in ("id", "title", "language", "category_id", "status", "scenario"):
        if not isinstance(meta[f], str) or not meta[f].strip():
            raise EntryFormatError(f"{path.name}: 字段 {f} 必须是非空字符串")

    for f in ("aliases", "tags", "tested_versions"):
        v = meta[f]
        if not isinstance(v, list) or not v or not all(isinstance(x, str) for x in v):
            raise EntryFormatError(f"{path.name}: 字段 {f} 必须是非空字符串数组")

    if meta["status"] not in VALID_STATUS:
        raise EntryFormatError(
            f"{path.name}: status={meta['status']!r} 不在 {sorted(VALID_STATUS)} 里"
        )

    if not ID_PATTERN.match(meta["id"]):
        raise EntryFormatError(
            f"{path.name}: id={meta['id']!r} 不符合格式，应形如 py.fs.check_extension"
        )


# ---------- 正文 ----------
def _split_sections(path: Path, body: str) -> dict[str, str]:
    """按 '## 标题' 切段，返回 {标题: 内容}。"""
    sections: dict[str, str] = {}
    current = None
    buffer: list[str] = []

    for line in body.splitlines():
        if line.startswith("## "):
            if current is not None:
                sections[current] = "\n".join(buffer).strip()
            current = line[3:].strip()
            buffer = []
        elif current is not None:
            buffer.append(line)
    if current is not None:
        sections[current] = "\n".join(buffer).strip()

    missing = [s for s in REQUIRED_SECTIONS if s not in sections]
    if missing:
        raise EntryFormatError(f"{path.name}: 正文缺小节 {missing}")
    for s in REQUIRED_SECTIONS:
        if not sections[s]:
            raise EntryFormatError(f"{path.name}: 小节「{s}」是空的")
    return sections


def _extract_code(path: Path, text: str) -> str:
    """从「代码」一节里取出第一个 ``` 代码块的内容。"""
    match = re.search(r"```[a-zA-Z0-9_+-]*\n(.*?)```", text, re.DOTALL)
    if not match:
        raise EntryFormatError(f"{path.name}: 「代码」小节里没有 ``` 代码块")
    return match.group(1).strip("\n")


def _build_entry(path: Path, meta: dict, sections: dict[str, str]) -> Entry:
    return Entry(
        id=meta["id"],
        title=meta["title"],
        language=meta["language"],
        category_id=meta["category_id"],
        status=meta["status"],
        scenario=meta["scenario"],
        aliases=tuple(meta["aliases"]),
        tags=tuple(meta["tags"]),
        tested_versions=tuple(meta["tested_versions"]),
        code=_extract_code(path, sections["代码"]),
        description=sections["功能描述"],
        explanation=sections["逐句解释"],
        principle=sections["原理解释"],
        caveats=sections["注意事项"],
        related_ids=tuple(meta.get("related_ids", [])),
        sources=tuple(meta.get("sources", [])),
    )
