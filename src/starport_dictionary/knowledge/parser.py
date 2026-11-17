r"""把一条 Markdown 知识条目解析成 Entry（第二版：YAML 头 + 严格校验）。

格式见 docs/AUTHORING_SPEC.md 与 docs/KNOWLEDGE_FORMAT.md。

三条硬规矩：
1. **未知字段直接报错**——规范里写了"不得自行创建未经定义的顶层字段"，
   不落成代码校验，这话就只是一句口号。
2. **object.id / action.id 必须在受控词表里**，且 object/action 必须自带别名。
3. **utterances 只做测试集**，不参与索引（Entry.index_terms 里不含它），
   否则"用原话搜原话"会让测试恒真。
"""

from __future__ import annotations

import re
from pathlib import Path

import yaml

from starport_dictionary.knowledge import primitives
from starport_dictionary.models.entry import Ambiguity, Constraint, Entry, Semantic

# —— 允许出现的顶层字段（多一个都不行）——
ALLOWED_TOP_FIELDS = {
    "id",
    "title",
    "description",
    "language",
    "category_id",
    "object",
    "action",
    "targets",
    "constraints",
    "utterances",
    "related_ids",
    "status",
    "tested_versions",
    "min_version",
    "version_note",
    "ambiguity",
    "sources",
}
REQUIRED_TOP_FIELDS = ("id", "title", "language", "category_id", "object", "action", "utterances", "status")

# —— 正文六节 ——
REQUIRED_SECTIONS = ("功能描述", "推荐代码", "语句解释", "原理解释", "注意事项", "使用场景")

VALID_STATUS = {"draft", "reviewed", "tested", "deprecated"}
ID_PATTERN = re.compile(r"^[a-z][a-z0-9_]*(\.[a-z0-9_]+){2,}$")

UTTERANCE_CATEGORIES = {
    "direct",
    "questions",
    "colloquial",
    "goal_based",
    "technical",
    "short_queries",
}
# 四类是底线；technical / goal_based 认不认真写，看条目性质
REQUIRED_UTTERANCE_CATEGORIES = {"direct", "questions", "colloquial", "short_queries"}
MIN_UTTERANCES = 8


class EntryFormatError(Exception):
    """条目格式不对。message 必须带出文件名和具体哪个字段。"""


def parse_entry_file(path: Path) -> Entry:
    path = Path(path)
    text = path.read_text(encoding="utf-8")
    front, body = _split_front_matter(path, text)
    meta = _load_yaml(path, front)
    _check_top_fields(path, meta)
    obj = _parse_semantic(path, "object", meta["object"], primitives.object_ids())
    action = _parse_semantic(path, "action", meta["action"], primitives.action_ids())
    utterances = _parse_utterances(path, meta["utterances"])
    sections = _split_sections(path, body)
    return _build(path, meta, obj, action, utterances, sections)


# ---------- 头部 ----------
def _split_front_matter(path: Path, text: str) -> tuple[str, str]:
    """--- 包起来的 YAML 头 + 正文。"""
    lines = text.lstrip("\ufeff").splitlines()
    if not lines or lines[0].strip() != "---":
        raise EntryFormatError(f"{path.name}: 文件第一行必须是 ---")

    for idx in range(1, len(lines)):
        if lines[idx].strip() == "---":
            return "\n".join(lines[1:idx]), "\n".join(lines[idx + 1 :])
    raise EntryFormatError(f"{path.name}: 缺少与开头配对的 --- ")


def _load_yaml(path: Path, front: str) -> dict:
    try:
        meta = yaml.safe_load(front)
    except yaml.YAMLError as exc:
        raise EntryFormatError(f"{path.name}: 头部不是合法 YAML（{exc}）") from exc
    if not isinstance(meta, dict):
        raise EntryFormatError(f"{path.name}: 头部必须是一个映射")
    return meta


def _check_top_fields(path: Path, meta: dict) -> None:
    missing = [f for f in REQUIRED_TOP_FIELDS if f not in meta]
    if missing:
        raise EntryFormatError(f"{path.name}: 缺必填字段 {missing}")

    unknown = [f for f in meta if f not in ALLOWED_TOP_FIELDS]
    if unknown:
        raise EntryFormatError(
            f"{path.name}: 出现未定义字段 {unknown}；要加字段请先改 AUTHORING_SPEC"
        )

    for f in ("id", "title", "language", "category_id", "status"):
        if not isinstance(meta[f], str) or not meta[f].strip():
            raise EntryFormatError(f"{path.name}: 字段 {f} 必须是非空字符串")

    if meta["status"] not in VALID_STATUS:
        raise EntryFormatError(
            f"{path.name}: status={meta['status']!r} 不在 {sorted(VALID_STATUS)} 里"
        )
    if not ID_PATTERN.match(meta["id"]):
        raise EntryFormatError(
            f"{path.name}: id={meta['id']!r} 不符合格式，应形如 py.fs.check_extension"
        )


def _parse_semantic(path: Path, field_name: str, raw, vocabulary: set[str]) -> Semantic:
    if not isinstance(raw, dict):
        raise EntryFormatError(f"{path.name}: {field_name} 必须是对象（含 id/name/aliases）")

    for k in ("id", "name", "aliases"):
        if k not in raw:
            raise EntryFormatError(f"{path.name}: {field_name} 缺 {k}")

    sid = raw["id"]
    if not isinstance(sid, str) or sid not in vocabulary:
        raise EntryFormatError(
            f"{path.name}: {field_name}.id={sid!r} 不在受控词表里；"
            f"已有：{sorted(vocabulary)[:6]} …（要新增请改 primitives.py）"
        )

    aliases = raw["aliases"]
    if not isinstance(aliases, list) or not aliases or not all(isinstance(a, str) for a in aliases):
        raise EntryFormatError(f"{path.name}: {field_name}.aliases 必须是非空字符串数组")

    name = raw["name"]
    if not isinstance(name, str) or not name.strip():
        raise EntryFormatError(f"{path.name}: {field_name}.name 必须是非空字符串")

    return Semantic(id=sid, name=name.strip(), aliases=tuple(a.strip() for a in aliases))


def _parse_utterances(path: Path, raw) -> dict[str, tuple[str, ...]]:
    if not isinstance(raw, dict):
        raise EntryFormatError(f"{path.name}: utterances 必须是按类别分组的映射")

    unknown = [k for k in raw if k not in UTTERANCE_CATEGORIES]
    if unknown:
        raise EntryFormatError(
            f"{path.name}: utterances 出现未知类别 {unknown}；"
            f"允许：{sorted(UTTERANCE_CATEGORIES)}"
        )

    missing = [k for k in REQUIRED_UTTERANCE_CATEGORIES if k not in raw]
    if missing:
        raise EntryFormatError(f"{path.name}: utterances 缺类别 {missing}")

    groups: dict[str, tuple[str, ...]] = {}
    total = 0
    for cat, items in raw.items():
        if not isinstance(items, list) or not items or not all(isinstance(x, str) for x in items):
            raise EntryFormatError(f"{path.name}: utterances.{cat} 必须是非空字符串数组")
        cleaned = tuple(x.strip() for x in items if x.strip())
        if not cleaned:
            raise EntryFormatError(f"{path.name}: utterances.{cat} 全是空字符串")
        groups[cat] = cleaned
        total += len(cleaned)

    if total < MIN_UTTERANCES:
        raise EntryFormatError(
            f"{path.name}: utterances 一共只有 {total} 条，至少要 {MIN_UTTERANCES} 条"
        )
    return groups


# ---------- 正文 ----------
def _split_sections(path: Path, body: str) -> dict[str, str]:
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
    match = re.search(r"```[a-zA-Z0-9_+-]*\n(.*?)```", text, re.DOTALL)
    if not match:
        raise EntryFormatError(f"{path.name}: 「推荐代码」里没有 ``` 代码块")
    return match.group(1).strip("\n")


def _parse_constraints(path: Path, raw) -> tuple[Constraint, ...]:
    if raw is None:
        return ()
    if not isinstance(raw, list):
        raise EntryFormatError(f"{path.name}: constraints 必须是数组")
    out = []
    for i, item in enumerate(raw):
        if not isinstance(item, dict) or "key" not in item:
            raise EntryFormatError(f"{path.name}: constraints[{i}] 必须是含 key 的对象")
        key = item["key"]
        if not isinstance(key, str) or not key.strip():
            raise EntryFormatError(f"{path.name}: constraints[{i}].key 必须是非空字符串")
        values = item.get("values") or []
        if not isinstance(values, list) or not all(isinstance(v, str) for v in values):
            raise EntryFormatError(f"{path.name}: constraints[{i}].values 必须是字符串数组")
        default = item.get("default", "")
        out.append(Constraint(key=key.strip(), values=tuple(values), default=str(default)))
    return tuple(out)


def _parse_ambiguity(path: Path, raw) -> tuple[Ambiguity, ...]:
    if raw is None:
        return ()
    if not isinstance(raw, list):
        raise EntryFormatError(f"{path.name}: ambiguity 必须是数组")
    out = []
    for i, item in enumerate(raw):
        if not isinstance(item, dict) or not str(item.get("note", "")).strip():
            raise EntryFormatError(f"{path.name}: ambiguity[{i}] 必须含非空 note")
        cands = item.get("candidate_ids") or []
        if not isinstance(cands, list) or not all(isinstance(c, str) for c in cands):
            raise EntryFormatError(f"{path.name}: ambiguity[{i}].candidate_ids 必须是字符串数组")
        out.append(Ambiguity(note=item["note"].strip(), candidate_ids=tuple(cands)))
    return tuple(out)


def _build(path, meta, obj, action, utterances, sections) -> Entry:
    tested = meta.get("tested_versions") or []
    if not isinstance(tested, list) or not all(isinstance(v, str) for v in tested):
        raise EntryFormatError(f"{path.name}: tested_versions 必须是字符串数组")
    if tested and not meta.get("min_version"):
        raise EntryFormatError(
            f"{path.name}: 写了 tested_versions 就必须写 min_version（程序要它算版本范围）"
        )

    targets = meta.get("targets") or []
    if not isinstance(targets, list) or not all(isinstance(t, str) for t in targets):
        raise EntryFormatError(f"{path.name}: targets 必须是字符串数组")

    return Entry(
        id=meta["id"],
        title=meta["title"],
        language=meta["language"],
        category_id=meta["category_id"],
        status=meta["status"],
        obj=obj,
        action=action,
        utterances=utterances,
        description=sections["功能描述"],
        code=_extract_code(path, sections["推荐代码"]),
        statement_notes=sections["语句解释"],
        principle=sections["原理解释"],
        caveats=sections["注意事项"],
        scenario=sections["使用场景"],
        targets=tuple(t.strip() for t in targets),
        constraints=_parse_constraints(path, meta.get("constraints")),
        related_ids=tuple(meta.get("related_ids") or ()),
        tested_versions=tuple(tested),
        min_version=str(meta.get("min_version") or "").strip(),
        version_note=str(meta.get("version_note") or "").strip(),
        ambiguity=_parse_ambiguity(path, meta.get("ambiguity")),
        sources=tuple(meta.get("sources") or ()),
    )
