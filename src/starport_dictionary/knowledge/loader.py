r"""扫描一个知识包，把里面的条目全读出来。

现在只做最小的事：读 manifest（做存在性检查）+ 逐个解析 entries/*.md。
不做的事：不建数据库、不建索引。那属于明天。
"""

from __future__ import annotations

import json
from dataclasses import dataclass
from pathlib import Path

from starport_dictionary.knowledge.parser import EntryFormatError, parse_entry_file
from starport_dictionary.models.entry import Entry


@dataclass(frozen=True)
class Pack:
    id: str
    name: str
    version: str
    schema_version: int
    min_app_version: str
    language: str
    entries: tuple[Entry, ...]
    errors: tuple[str, ...]


def load_pack(pack_dir: Path) -> Pack:
    """读一个知识包。坏条目只记录错误、不中断整包——一个包不该被一条脏数据拖死。"""
    pack_dir = Path(pack_dir)
    manifest_path = pack_dir / "manifest.json"
    if not manifest_path.is_file():
        raise FileNotFoundError(f"{pack_dir.name}: 找不到 manifest.json")

    manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
    for key in ("id", "name", "version", "schema_version", "min_app_version", "language"):
        if key not in manifest:
            raise ValueError(f"{pack_dir.name}: manifest 缺字段 {key}")

    entries: list[Entry] = []
    errors: list[str] = []
    seen: dict[str, Path] = {}

    for md in sorted((pack_dir / "entries").glob("*.md")):
        try:
            entry = parse_entry_file(md)
        except EntryFormatError as exc:
            errors.append(str(exc))
            continue
        if entry.id in seen:
            errors.append(f"{md.name}: id {entry.id} 与 {seen[entry.id].name} 重复")
            continue
        seen[entry.id] = md
        entries.append(entry)

    declared = manifest.get("entry_count")
    if isinstance(declared, int) and declared != len(entries):
        errors.append(
            f"{pack_dir.name}: manifest 声明 {declared} 条，实际读到 {len(entries)} 条"
        )

    return Pack(
        id=manifest["id"],
        name=manifest["name"],
        version=manifest["version"],
        schema_version=manifest["schema_version"],
        min_app_version=manifest["min_app_version"],
        language=manifest["language"],
        entries=tuple(entries),
        errors=tuple(errors),
    )


def load_all_packs(root: Path) -> list[Pack]:
    """读 root 下所有知识包（子目录里带 manifest.json 的算一个包）。"""
    root = Path(root)
    packs = []
    for child in sorted(root.iterdir()):
        if child.is_dir() and (child / "manifest.json").is_file():
            packs.append(load_pack(child))
    return packs
