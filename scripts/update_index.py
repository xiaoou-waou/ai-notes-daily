#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
扫描 notes/ 下的全部笔记，重建 README.md 中的目录索引区块。

用法:
    python3 scripts/update_index.py

设计要点:
  - 目录永远由 notes/ 目录的**实际内容**生成，不做增量拼接，
    因此不会出现"目录滞后 / 漏记 / 重复"的问题。
  - 只替换 README 中两个 HTML 注释标记之间的内容，区块外的手写文字不受影响。
"""

import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
NOTES_DIR = ROOT / "notes"
README = ROOT / "README.md"

START_MARK = "<!-- NOTES_INDEX_START -->"
END_MARK = "<!-- NOTES_INDEX_END -->"

# 文件名日期: 2026-09-02-xxx.md
FNAME_DATE = re.compile(r"^(\d{4}-\d{2}-\d{2})")
# 一级标题: "# 2026-09-02｜标题" / "# 2026-09-02 · 标题"
H1_TITLE = re.compile(r"^#\s+(?:\d{4}-\d{2}-\d{2})?\s*[｜|·•\-–—:：]\s*(.+?)\s*$")
# 普通一级标题兜底
H1_PLAIN = re.compile(r"^#\s+(.+?)\s*$")
TAGS = re.compile(r"^\*\*标签\*\*\s*[:：]?\s*(.+?)\s*$")
SUMMARY = re.compile(r"^>\s*(.+?)\s*$")


def parse_note(path: Path) -> dict:
    text = path.read_text(encoding="utf-8")
    m = FNAME_DATE.match(path.stem)
    date = m.group(1) if m else ""

    title = None
    tags = ""
    summary = ""

    for raw in text.splitlines():
        line = raw.strip()
        if title is None:
            m1 = H1_TITLE.match(line)
            if m1:
                title = m1.group(1)
                continue
            m2 = H1_PLAIN.match(line)
            if m2:
                title = m2.group(1)
                continue
        if not tags:
            m3 = TAGS.match(line)
            if m3:
                tags = m3.group(1)
                continue
        if not summary:
            m4 = SUMMARY.match(line)
            # 跳过纯格式说明行
            if m4 and not m4.group(1).startswith(("生成时间", "信源")):
                summary = m4.group(1)

    return {
        "date": date,
        "title": title or path.stem,
        "tags": tags,
        "summary": summary,
        "file": path.name,
    }


def build_index(notes: list) -> str:
    if not notes:
        return "_暂无笔记。第一篇会在下一个 12:00 自动生成。_"

    latest = notes[0]["date"]
    oldest = notes[-1]["date"]
    span = latest if latest == oldest else f"{oldest} → {latest}"

    lines = [
        f"> 共 **{len(notes)}** 篇 · 覆盖 {span} · 最新在最上\n",
        "| 日期 | 标题 | 标签 |",
        "| :--- | :--- | :--- |",
    ]
    for n in notes:
        link = f"[{n['title']}](notes/{n['file']})"
        tags = n["tags"] or "—"
        lines.append(f"| `{n['date']}` | {link} | {tags} |")
    return "\n".join(lines)


def main() -> int:
    if not README.exists():
        print(f"[ERROR] 找不到 README: {README}", file=sys.stderr)
        return 1

    if not NOTES_DIR.exists():
        NOTES_DIR.mkdir(parents=True)
    notes = [parse_note(p) for p in NOTES_DIR.glob("*.md") if p.is_file()]
    notes.sort(key=lambda n: (n["date"], n["file"]), reverse=True)

    body = build_index(notes)
    block = f"{START_MARK}\n{body}\n{END_MARK}"

    content = README.read_text(encoding="utf-8")
    pattern = re.compile(
        re.escape(START_MARK) + r".*?" + re.escape(END_MARK),
        re.DOTALL,
    )
    if not pattern.search(content):
        print("[ERROR] README 中未找到索引标记区块", file=sys.stderr)
        return 1

    new_content = pattern.sub(lambda _: block, content, count=1)
    if new_content == content:
        print(f"[OK] 目录无变化（{len(notes)} 篇笔记）")
        return 0

    README.write_text(new_content, encoding="utf-8")
    print(f"[OK] 已更新目录：{len(notes)} 篇笔记")
    for n in notes:
        print(f"     {n['date']}  {n['title']}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
