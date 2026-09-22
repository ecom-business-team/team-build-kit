#!/usr/bin/env python3
"""render.py — write an HTML companion beside a gate document.

Usage:
  python3 render.py <path> [<path> ...]   render each markdown file; print the written path
  python3 render.py --stale <dir>         list companions older than their source

Recognises seven documents by file name and header — a build-intent memo, a PRD,
a project log (its last ship review), a state file (the handoff) and the three
knowledge documents (`why_we_build.md`, `worked_example.md`, `lifecycle_map.md`) —
and lays each out in a fixed plan that foregrounds what its reader must decide and
folds the rest into native <details>. Standard library only. Idempotent: the same
input gives the same bytes. Writes only the .html beside the source, never the
markdown. Exit 0 with the written path on stdout; exit 1 with one line on stderr
when a file is none of the seven. A ```chain fence draws as a strip and a ```map
fence as a picture (inline SVG from a declared grid) in any of them.
"""
from __future__ import annotations

import html as _html
import re
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
CSS_PATH = HERE / "companion.css"

# ----------------------------------------------------------------------------
# Blocks
# ----------------------------------------------------------------------------

class Block:
    def __init__(self, kind, raw="", **kw):
        self.kind = kind
        self.raw = raw
        self.__dict__.update(kw)

    def __repr__(self):
        return f"<{self.kind} {getattr(self, 'text', '')[:30]!r}>"


class Item:
    def __init__(self, text, indent=0):
        self.indent = indent
        self.children = []
        self.label = None
        self.mark = None
        self.text = text
        self._classify()

    def _classify(self):
        m = MARK_RE.match(self.text)
        if m:
            self.mark = MARKS[m.group(1)]
            self.text = self.text[m.end():]
        f = FIELD_RE.match(self.text)
        if f:
            self.label, self.text = f.group(1).strip(), f.group(2)


FENCE_RE = re.compile(r"^\s*(```|~~~)")
HEADING_RE = re.compile(r"^(#{1,6})\s+(.*?)\s*#*\s*$")
FIELD_RE = re.compile(r"^\*\*([^*\n]+?)(?::\*\*|\*\*:)\s*(.*)$")
LIST_RE = re.compile(r"^(\s*)(?:([-*+])|(\d+)[.)])\s+(.*)$")
TABLE_ROW_RE = re.compile(r"^\s*\|.*\|\s*$")
TABLE_SEP_RE = re.compile(r"^\s*\|?\s*:?-{2,}:?\s*(?:\|\s*:?-{2,}:?\s*)*\|?\s*$")
HR_RE = re.compile(r"^\s*([-*_])(?:\s*\1){2,}\s*$")
QUOTE_RE = re.compile(r"^\s*>\s?(.*)$")
MARK_RE = re.compile(r"^(\[ \]|\[x\]|\[X\]|✅|✓|✔|☐|❌|✕|▶)\s*")
MARKS = {"[ ]": "todo", "[x]": "done", "[X]": "done", "✅": "done", "✓": "done", "✔": "done",
         "☐": "todo", "❌": "fail", "✕": "fail", "▶": "active"}
GLYPH = {"done": "✅", "todo": "☐", "fail": "❌", "active": "▶"}


def parse(text: str) -> list[Block]:
    """Fence-aware block parser. A heading inside a fence is code, not a section."""
    lines = text.splitlines()
    blocks: list[Block] = []
    para: list[str] = []
    fields: list[list[str]] = []
    i, n = 0, len(lines)

    def flush():
        nonlocal para, fields
        if para:
            blocks.append(Block("para", "\n".join(para), text=" ".join(s.strip() for s in para)))
            para = []
        if fields:
            blocks.append(Block("fields", "\n".join(f"**{k}:** {v}" for k, v in fields),
                                items=[(k, v.strip()) for k, v in fields]))
            fields = []

    while i < n:
        line = lines[i]
        fm = FENCE_RE.match(line)
        if fm:
            flush()
            fence = fm.group(1)
            lang = line.strip()[len(fence):].strip()
            body = []
            i += 1
            while i < n and not (lines[i].strip().startswith(fence)):
                body.append(lines[i])
                i += 1
            i += 1  # closing fence (or EOF)
            blocks.append(Block("code", "\n".join(body), text="\n".join(body), lang=lang))
            continue
        if not line.strip():
            flush()
            i += 1
            continue
        hm = HEADING_RE.match(line)
        if hm:
            flush()
            blocks.append(Block("heading", line, level=len(hm.group(1)), text=hm.group(2).strip()))
            i += 1
            continue
        if line.lstrip().startswith("<!--") and not para and not fields:
            flush()
            start = i
            while i < n and "-->" not in lines[i]:
                i += 1
            i += 1
            blocks.append(Block("comment", "\n".join(lines[start:i]), text=""))
            continue
        if HR_RE.match(line) and not para and not fields:
            blocks.append(Block("hr", line))
            i += 1
            continue
        if TABLE_ROW_RE.match(line) and i + 1 < n and TABLE_SEP_RE.match(lines[i + 1]):
            flush()
            rows = []
            start = i
            while i < n and TABLE_ROW_RE.match(lines[i]):
                if not TABLE_SEP_RE.match(lines[i]):
                    rows.append(split_row(lines[i]))
                i += 1
            header, body = (rows[0], rows[1:]) if rows else ([], [])
            blocks.append(Block("table", "\n".join(lines[start:i]), header=header, rows=body))
            continue
        qm = QUOTE_RE.match(line)
        if qm:
            flush()
            q = []
            start = i
            while i < n and QUOTE_RE.match(lines[i]):
                q.append(QUOTE_RE.match(lines[i]).group(1))
                i += 1
            blocks.append(Block("quote", "\n".join(lines[start:i]), text=" ".join(s.strip() for s in q if s.strip())))
            continue
        lm = LIST_RE.match(line)
        if lm and fields and not para:
            flush()  # `**What breaks:**` followed by bullets: the bullets are a list, not the field's text
        if lm and not para and not fields:
            start = i
            ordered = lm.group(3) is not None
            items: list[Item] = []
            stack: list[Item] = []
            while i < n:
                cur = lines[i]
                if not cur.strip():
                    # a blank line ends the list unless the next non-blank line is another item
                    j = i + 1
                    while j < n and not lines[j].strip():
                        j += 1
                    if j < n and LIST_RE.match(lines[j]) and not FENCE_RE.match(lines[j]):
                        i = j
                        continue
                    break
                m = LIST_RE.match(cur)
                if m and not FENCE_RE.match(cur):
                    indent = len(m.group(1).expandtabs(4))
                    it = Item(m.group(4).strip(), indent)
                    while stack and stack[-1].indent >= indent:
                        stack.pop()
                    (stack[-1].children if stack else items).append(it)
                    stack.append(it)
                    i += 1
                    continue
                if cur[:1].isspace() and stack:
                    stack[-1].text += " " + cur.strip()
                    i += 1
                    continue
                break
            blocks.append(Block("list", "\n".join(lines[start:i]), ordered=ordered, items=items))
            continue
        fmatch = FIELD_RE.match(line)
        if fmatch and not para:
            fields.append([fmatch.group(1).strip(), fmatch.group(2)])
            i += 1
            continue
        if fields:
            fields[-1][1] += " " + line.strip()
            i += 1
            continue
        para.append(line)
        i += 1
    flush()
    return blocks


def split_row(line: str) -> list[str]:
    s = line.strip()
    s = s.replace("\\|", "\x01")
    if s.startswith("|"):
        s = s[1:]
    if s.endswith("|"):
        s = s[:-1]
    return [c.strip().replace("\x01", "|") for c in s.split("|")]


def words(blocks) -> int:
    return sum(len(re.findall(r"\S+", b.raw)) for b in blocks)


# ----------------------------------------------------------------------------
# Inline rendering
# ----------------------------------------------------------------------------

CODE_SPAN_RE = re.compile(r"(`+)(.+?)\1")
TAG_RE = re.compile(r"\*\*\[([^\]\n]+)\]\*\*")
LINK_RE = re.compile(r"\[([^\]\n]+)\]\(([^)\s]+)(?:\s+&quot;[^&]*&quot;)?\)")
BOLD_RE = re.compile(r"\*\*(?=\S)(.+?)(?<=\S)\*\*")
STRIKE_RE = re.compile(r"~~(?=\S)(.+?)(?<=\S)~~")
ITAL_STAR_RE = re.compile(r"(?<![\w*])\*(?=\S)(.+?)(?<=\S)\*(?![\w*])")
ITAL_US_RE = re.compile(r"(?<![\w/`.\\])_(?=\S)(.+?)(?<=\S)_(?![\w])")


def esc(s: str, quote: bool = False) -> str:
    return _html.escape(s, quote=quote)


def inline(text: str) -> str:
    """Markdown inline → HTML: code, tags, links, bold, strikethrough, italic. Everything escaped."""
    codes: list[str] = []

    def stash(m):
        codes.append(f"<code>{esc(m.group(2).strip())}</code>")
        return f"\x00{len(codes) - 1}\x00"

    s = CODE_SPAN_RE.sub(stash, text)
    s = esc(s)
    s = TAG_RE.sub(lambda m: f'<span class="tag">{m.group(1)}</span>', s)
    s = LINK_RE.sub(lambda m: f'<a href="{m.group(2).replace(chr(34), "&quot;")}">{m.group(1)}</a>', s)
    s = BOLD_RE.sub(r"<strong>\1</strong>", s)
    s = STRIKE_RE.sub(r"<del>\1</del>", s)
    s = ITAL_STAR_RE.sub(r"<em>\1</em>", s)
    s = ITAL_US_RE.sub(r"<em>\1</em>", s)
    s = re.sub("\x00(\\d+)\x00", lambda m: codes[int(m.group(1))], s)
    return s


def plain(text: str) -> str:
    """Strip inline markup for <title> and summaries."""
    s = CODE_SPAN_RE.sub(lambda m: m.group(2), text)
    s = re.sub(r"\*\*|__|~~", "", s)
    s = re.sub(r"(?<![\w])[_*](?=\S)(.+?)(?<=\S)[_*](?![\w])", r"\1", s)
    s = LINK_RE.sub(r"\1", s)
    return s.strip()


# ----------------------------------------------------------------------------
# Block rendering (the generic path, used inside every plan)
# ----------------------------------------------------------------------------

PILL_RE = re.compile(r"^(✅|❌|☐|▶|✓|✔|✕)\s*(.*)$", re.S)
PILL_CLASS = {"✅": "ok", "✓": "ok", "✔": "ok", "❌": "fail", "✕": "fail", "☐": "pending", "▶": "pending"}


def pillify(cell: str) -> str:
    m = PILL_RE.match(cell.strip())
    if m:
        rest = f"<span>{inline(m.group(2))}</span>" if m.group(2).strip() else ""
        return f'<span class="pill {PILL_CLASS[m.group(1)]}">{m.group(1)}</span>{rest}'
    if cell.strip().lower() in ("pending", "open", "held", "todo", "queued"):
        return f'<span class="pill pending">{esc(cell.strip())}</span>'
    return inline(cell)


def html_table(b: Block) -> str:
    out = ['<div class="table"><table>']
    if b.header:
        out.append("<thead><tr>" + "".join(f"<th>{inline(h)}</th>" for h in b.header) + "</tr></thead>")
    out.append("<tbody>")
    for row in b.rows:
        out.append("<tr>" + "".join(f"<td>{pillify(c)}</td>" for c in row) + "</tr>")
    out.append("</tbody></table></div>")
    return "".join(out)


def item_body(it: Item) -> str:
    text = inline(it.text)
    if it.label:
        text = f"<strong>{inline(it.label)}:</strong> {text}" if text else f"<strong>{inline(it.label)}</strong>"
    if it.children:
        text += html_list(Block("list", ordered=False, items=it.children))
    return text


def html_checklist(items: list[Item], default: str = "todo", ordered: bool = False) -> str:
    tag = "ol" if ordered else "ul"
    out = [f'<{tag} class="checklist">']
    for it in items:
        mark = it.mark or default
        out.append(f'<li><span class="mark {mark}">{GLYPH[mark]}</span><div>{item_body(it)}</div></li>')
    out.append(f"</{tag}>")
    return "".join(out)


def html_fields_from_items(items: list[Item]) -> str:
    out = ['<dl class="fields">']
    for it in items:
        body = inline(it.text)
        if it.children:
            body += html_list(Block("list", ordered=False, items=it.children))
        out.append(f"<dt>{inline(it.label)}</dt><dd>{body}</dd>")
    out.append("</dl>")
    return "".join(out)


def html_list(b: Block, checklist: bool | None = None) -> str:
    items = b.items
    if not items:
        return ""
    if checklist or (checklist is None and any(it.mark for it in items)):
        return html_checklist(items, ordered=getattr(b, "ordered", False))
    if all(it.label and not it.mark for it in items):
        return html_fields_from_items(items)
    tag = "ol" if getattr(b, "ordered", False) else "ul"
    return f"<{tag}>" + "".join(f"<li>{item_body(it)}</li>" for it in items) + f"</{tag}>"


def html_fields(b: Block, skip=()) -> str:
    rows = [(k, v) for k, v in b.items if k.lower() not in skip]
    if not rows:
        return ""
    return '<dl class="fields">' + "".join(f"<dt>{inline(k)}</dt><dd>{inline(v)}</dd>" for k, v in rows) + "</dl>"


def html_block(b: Block, **opts) -> str:
    if b.kind == "heading":
        lvl = min(max(b.level, 3), 4)
        return f'<h{lvl} class="sub">{inline(b.text)}</h{lvl}>'
    if b.kind == "para":
        return f"<p>{inline(b.text)}</p>"
    if b.kind == "fields":
        return html_fields(b)
    if b.kind == "list":
        return html_list(b, opts.get("checklist"))
    if b.kind == "table":
        return html_table(b)
    if b.kind == "quote":
        return f"<blockquote>{inline(b.text)}</blockquote>"
    if b.kind == "code" and (b.lang or "").strip().lower() == "chain":
        return html_chain(b.text)
    if b.kind == "code" and (b.lang or "").strip().lower() == "map":
        return html_map(b.text)
    if b.kind == "code":
        return f"<pre><code>{esc(b.text)}</code></pre>"
    if b.kind == "hr":
        return "<hr>"
    return ""


def html_blocks(blocks, **opts) -> str:
    return "".join(html_block(b, **opts) for b in blocks)


# ----------------------------------------------------------------------------
# Sections
# ----------------------------------------------------------------------------

def split_sections(blocks, level):
    """(preamble, [(heading_block, body_blocks)]) — a body runs to the next heading of level <= level."""
    pre, secs, cur = [], [], None
    for b in blocks:
        if b.kind == "heading" and b.level <= level:
            if b.level == level:
                cur = (b, [])
                secs.append(cur)
                continue
            cur = None  # a higher heading closes the run
        if cur is None:
            pre.append(b)
        else:
            cur[1].append(b)
    return pre, secs


def find_section(secs, pattern):
    rx = re.compile(pattern, re.I)
    for i, (h, body) in enumerate(secs):
        if rx.search(plain(h.text)):
            return i
    return None



PLAIN_RE = re.compile(r"^\*\*in plain words:?\*\*:?\s*", re.I)


def split_plain(body):
    """(plain_text | None, rest): a body that opens with `> **In plain words:** …` yields that line."""
    if body and body[0].kind == "quote" and PLAIN_RE.match(body[0].text):
        return PLAIN_RE.sub("", body[0].text).strip(), body[1:]
    return None, body


def plain_p(text: str) -> str:
    return f'<p class="plain">{inline(text)}</p>'


def details(body_html: str, count: int | None = None) -> str:
    label = f"Details · {count:,} words" if count is not None else "Details"
    return f'<details class="details"><summary>{label}</summary>{body_html}</details>'


def open_section(title_html, body_html, cls=""):
    c = f"section {cls}".strip()
    return f'<section class="{c}"><h2>{title_html}</h2>{body_html}</section>'


def plain_section(title_html, body_blocks, cls="", render=None):
    """An open section. With a plain line: the line is the visible text and the body folds beneath it."""
    render = render or html_blocks
    text, rest = split_plain(body_blocks)
    if text is None:
        return open_section(title_html, render(body_blocks), cls)
    return open_section(title_html, plain_p(text) + details(render(rest), words(rest)), cls)


def folded_section(title_html, body_blocks, cls=""):
    c = f"section {cls}".strip()
    text, rest = split_plain(body_blocks)
    count = words(rest)
    second = plain_p(text) if text is not None else ""
    return (f'<details class="{c}"><summary><h2>{title_html}</h2>'
            f'<span class="count">{count:,} words</span>{second}</summary>{html_blocks(rest)}</details>')


def header_parts(pre):
    """Title, subtitle (a fully italic paragraph), the header fields, and the remaining header paragraphs."""
    title = next((plain(b.text) for b in pre if b.kind == "heading" and b.level == 1), None)
    fields: dict[str, str] = {}
    order: list[str] = []
    subtitle = None
    notes = []
    for b in pre:
        if b.kind == "fields":
            for k, v in b.items:
                fields[k.lower()] = v
                order.append(k)
        elif b.kind == "para":
            t = b.text.strip()
            if subtitle is None and re.fullmatch(r"_[^_].*[^_]_", t, re.S) and not fields:
                subtitle = t[1:-1]
            else:
                notes.append(b)
        elif b.kind in ("list", "table", "quote", "code"):
            notes.append(b)
    return title, subtitle, fields, order, notes


def status_pill(value: str) -> str:
    v = value.strip()
    first = v.split()[0].rstrip(".,;:") if v else ""
    word = plain(first).strip("*_").rstrip(".,;:")
    cls = "ok" if word.lower() in ("approved", "shipped", "live", "done", "reached", "complete", "completed") else "pending"
    return f'<span class="pill {cls}">{esc(word)}</span><span>{inline(v[len(first):].strip())}</span>' if word else inline(v)


def fields_dl(fields: dict, order: list, skip=(), pills=()) -> str:
    rows = []
    for k in order:
        kl = k.lower()
        if kl in skip:
            continue
        v = fields[kl]
        rows.append(f"<dt>{inline(k)}</dt><dd>{status_pill(v) if kl in pills else inline(v)}</dd>")
    return '<dl class="fields">' + "".join(rows) + "</dl>" if rows else ""


# ----------------------------------------------------------------------------
# Plan: memo (Gate 1)
# ----------------------------------------------------------------------------

def boundary_block(body):
    """Group the Scope's blocks into panels by their bold lead: what it is · in · what it is not."""
    panels = []   # [cls, label, [blocks]]
    trailing = []
    def start_panel(lead, rest, raw):
        lead = lead.rstrip(":").strip()
        low = lead.lower()
        cls = "not" if " not" in f" {low}" else "is" if low.startswith("what it is") else "in" if low.startswith("in") else "other"
        panels.append([cls, lead, [Block("para", raw, text=rest.strip())] if rest.strip() else []])

    for b in body:
        if b.kind == "fields":          # `**What it is:** …` parses as a field; each field opens a panel
            for k, v in b.items:
                start_panel(k, v, b.raw)
            continue
        if b.kind == "para":
            m = re.match(r"^\*\*([^*]+?)\*\*\s*(.*)$", b.text, re.S)
            if m:
                start_panel(m.group(1), m.group(2), b.raw)
                continue
        if panels and not any(x.kind == "list" for x in panels[-1][2]) and b.kind in ("para", "list", "table"):
            panels[-1][2].append(b)
        elif panels and b.kind == "list" and not any(x.kind == "list" for x in panels[-1][2]):
            panels[-1][2].append(b)
        else:
            trailing.append(b)
    if not panels:
        return html_blocks(body)
    out = ['<div class="boundary">']
    for cls, label, blocks in panels:
        out.append(f'<div class="panel {cls}"><h3>{inline(label)}</h3>{html_blocks(blocks)}</div>')
    out.append("</div>")
    out.append(html_blocks(trailing))
    return "".join(out)


def verdict_block(body):
    if not body:
        return ""
    first = body[0]
    out = ['<div class="verdict">']
    rest = body
    if first.kind == "para":
        m = re.match(r"^\*\*([^*]+?)\*\*\s*(.*)$", first.text, re.S)
        if m and len(m.group(1).split()) <= 3:
            out.append(f'<div class="verdict-word">{inline(m.group(1).rstrip(".").strip())}</div>')
            if m.group(2).strip():
                out.append(f"<p>{inline(m.group(2).strip())}</p>")
            rest = body[1:]
    out.append(html_blocks(rest))
    out.append("</div>")
    return "".join(out)


def plan_memo(blocks, src: Path) -> tuple[str, str]:
    pre, secs = split_sections(blocks, 2)
    title, subtitle, fields, order, notes = header_parts(pre)
    title = title or src.stem
    out = ['<header class="doc-head">', '<p class="eyebrow">Gate 1 · Build-intent memo</p>', f"<h1>{esc(title)}</h1>"]
    if subtitle:
        out.append(f'<p class="subtitle">{inline(subtitle)}</p>')
    if "constraint" in fields:
        out.append(f'<p class="lede">{inline(fields["constraint"])}</p>')
    out.append(fields_dl(fields, order, skip=("constraint",)))
    for b in notes:
        out.append(f'<p class="note">{inline(b.text)}</p>' if b.kind == "para" else html_block(b))
    out.append("</header>")

    used = set()

    def take(pattern):
        i = find_section(secs, pattern)
        if i is None or i in used:
            return None
        used.add(i)
        return secs[i]

    scope = take(r"\bscope\b")
    success = take(r"\bsuccess\b")
    ask = take(r"\bask\b")
    problem = take(r"\bproblem\b")
    value = take(r"\bvalue\b|why now")

    decisions = []
    if scope:
        h, body = scope
        body_pre, subs = split_sections(body, 3)
        out.append(open_section(inline(h.text), boundary_block(body_pre), "scope"))
        decisions = subs
    if success:
        h, body = success
        out.append(open_section(inline(h.text), html_blocks(body, checklist=True), "success"))
    if ask:
        h, body = ask
        out.append(open_section(inline(h.text), verdict_block(body), "ask"))
    for h, body in decisions:
        out.append(open_section(inline(h.text), html_blocks(body), "decision"))
    for sec in (problem, value):
        if sec:
            out.append(folded_section(inline(sec[0].text), sec[1]))
    for i, (h, body) in enumerate(secs):
        if i not in used:
            out.append(folded_section(inline(h.text), body))
    return title, "".join(out)


# ----------------------------------------------------------------------------
# Plan: PRD (Gate 2)
# ----------------------------------------------------------------------------

WI_RE = re.compile(r"^work item\s+(\d+)\s*[:—–-]\s*(.*)$", re.I)
PRD_KEYWORDS = {
    1: r"beginning state", 2: r"desired state", 3: r"chosen path", 4: r"narrative", 5: r"domain model|erd",
    6: r"lifecycle", 7: r"value stream", 8: r"boundar", 9: r"proposed changes", 10: r"impact map",
    11: r"validation", 12: r"work items", 13: r"rigor", 14: r"pre-mortem|premortem", 15: r"readiness",
}


def number_sections(secs):
    """Map PRD section number → (heading, body), by the leading number, else by keyword."""
    by_num = {}
    for i, (h, body) in enumerate(secs):
        m = re.match(r"^(\d+)\.\s*", plain(h.text))
        if m and int(m.group(1)) not in by_num:
            by_num[int(m.group(1))] = i
    for num, kw in PRD_KEYWORDS.items():
        if num not in by_num:
            j = find_section(secs, kw)
            if j is not None and j not in by_num.values():
                by_num[num] = j
    return by_num


def work_item_cards(body) -> str:
    body_pre, subs = split_sections(body, 3)
    text, body_pre = split_plain(body_pre)
    out = [plain_p(text) if text is not None else "", html_blocks(body_pre)]
    for h, sub in subs:
        m = WI_RE.match(plain(h.text))
        num, name = (m.group(1), m.group(2)) if m else ("", plain(h.text))
        wi_plain, sub = split_plain(sub)
        inner, visible = [], []
        for b in sub:
            if b.kind == "list" and all(it.label for it in b.items):
                if wi_plain is not None:  # what the reviewer grades stays visible; the rest folds
                    shown = [it for it in b.items if it.label.lower().startswith("verif")]
                    rest = [it for it in b.items if not it.label.lower().startswith("verif")]
                    if shown:
                        visible.append(html_fields_from_items(shown))
                    if rest:
                        inner.append(html_fields_from_items(rest))
                else:
                    inner.append(html_fields_from_items(b.items))
            else:
                inner.append(html_block(b))
        label = f'<span class="wi-num">Work item {num}</span>' if num else ""
        body_html = "".join(inner)
        if wi_plain is not None:
            body_html = plain_p(wi_plain) + "".join(visible) + (details(body_html) if body_html else "")
        out.append(f'<article class="wi">{f"<h3>{label}<span>{inline(name)}</span></h3>"}{body_html}</article>')
    return "".join(out)


def checklist_from_table(b: Block) -> str:
    """A table with a Pass / Status / Done column becomes a checklist; otherwise it stays a table."""
    if not b.header:
        return html_table(b)
    idx = next((i for i, h in enumerate(b.header) if re.search(r"pass|status|done|result", h, re.I)), None)
    if idx is None:
        return html_table(b)
    skip_num = 0 if b.header and re.fullmatch(r"#|no\.?|n", b.header[0].strip(), re.I) else None
    items = []
    for row in b.rows:
        if len(row) <= idx:
            continue
        verdict = row[idx].strip()
        v = verdict.lower()
        mark = "done" if re.match(r"^(y|yes|✅|✓|✔|pass|done)", v) else "fail" if re.match(r"^(n|no|❌|✕|fail)\b", v) else "todo"
        cells = [c for i, c in enumerate(row) if i != idx and i != skip_num]
        body = inline(" — ".join(c for c in cells if c.strip()))
        detail = re.sub(r"^(y|yes|n|no|✅|❌|✓|✔|✕)\s*", "", verdict, flags=re.I).strip()
        if detail:
            body += f' <span class="muted">{esc(detail)}</span>'
        items.append((mark, body))
    return ('<ul class="checklist">' + "".join(
        f'<li><span class="mark {mark}">{GLYPH[mark]}</span><div>{body}</div></li>' for mark, body in items) + "</ul>")


def kind_block(kind_text: str, src: Path | None = None) -> str:
    out = ['<div class="kind"><div class="label">Kind of thing built</div>', f'<div class="statement">{inline(kind_text)}</div>']
    table = kind_table(src) if src else {}
    seen = set()
    for word in re.findall(r"\*\*([^*]+?)\*\*", kind_text):
        key = word.strip().lower().rstrip("s")
        if key in table and key not in seen:
            seen.add(key)
            definition, proof = table[key]
            out.append(f'<div class="part"><div class="name">{esc(word.strip().capitalize())}</div>'
                       f'<div class="definition">{inline(definition)}</div>'
                       + (f'<div class="proof">{inline(proof)}</div>' if proof else "") + "</div>")
    out.append("</div>")
    return "".join(out)


def plan_prd(blocks, src: Path) -> tuple[str, str]:
    pre, secs = split_sections(blocks, 2)
    title, subtitle, fields, order, notes = header_parts(pre)
    title = title or src.stem
    kind_key = next((k for k in fields if k.startswith("kind")), None)
    out = ['<header class="doc-head">', '<p class="eyebrow">Gate 2 · PRD</p>', f"<h1>{esc(title)}</h1>"]
    if subtitle:
        out.append(f'<p class="subtitle">{inline(subtitle)}</p>')
    if "constraint" in fields:
        out.append(f'<p class="lede">{inline(fields["constraint"])}</p>')
    out.append(fields_dl(fields, order, skip=("constraint", kind_key or ""), pills=("status",)))
    if kind_key:
        out.append(kind_block(fields[kind_key], src))
    for b in notes:
        out.append(f'<p class="note">{inline(b.text)}</p>' if b.kind == "para" else html_block(b))
    out.append("</header>")

    by_num = number_sections(secs)
    used = set()

    def sec(num):
        i = by_num.get(num)
        if i is None or i in used:
            return None
        used.add(i)
        return secs[i]

    for num in (2, 3, 4):
        s = sec(num)
        if s:
            out.append(plain_section(inline(s[0].text), s[1]))
    s = sec(12)
    if s:  # the plain line shows, then the cards stay visible (each card folds its own fields)
        out.append(open_section(inline(s[0].text), work_item_cards(s[1]), "work-items"))
    s = sec(11)
    if s:
        out.append(plain_section(inline(s[0].text), s[1], "validation"))
    s = sec(13)
    if s:
        rigor = lambda blocks: "".join(checklist_from_table(b) if b.kind == "table" else html_block(b, checklist=True) for b in blocks)
        out.append(plain_section(inline(s[0].text), s[1], "rigor", rigor))
    s = sec(14)
    if s:
        out.append(plain_section(inline(s[0].text), s[1], "pre-mortem"))
    s = sec(15)
    if s:
        out.append(plain_section(inline(s[0].text), s[1], "readiness", lambda blocks: html_blocks(blocks, checklist=True)))
    for num in (1, 5, 6, 7, 8, 9, 10):
        s = sec(num)
        if s:
            out.append(folded_section(inline(s[0].text), s[1]))
    for i, (h, body) in enumerate(secs):
        if i not in used:
            out.append(folded_section(inline(h.text), body))
    return title, "".join(out)


# ----------------------------------------------------------------------------
# Workspace lookups — every one optional, every one with a fallback
# ----------------------------------------------------------------------------

OWNER_RE = re.compile(r"The owner is \*\*([^*\n]+?)\*\*")


def workspace_root(src: Path, *names: str) -> Path | None:
    """The nearest ancestor of `src` holding every named file, else None."""
    for d in [src.resolve().parent, *src.resolve().parents]:
        if all((d / n).is_file() for n in names):
            return d
    return None


def owner_word(src: Path) -> str:
    """The owner's name from the root CLAUDE.md "Words the skills use" block; fallback "the owner"."""
    root = workspace_root(src, "CLAUDE.md")
    while root is not None:
        m = OWNER_RE.search(root.joinpath("CLAUDE.md").read_text(encoding="utf-8", errors="replace"))
        if m:
            return m.group(1).strip()
        root = workspace_root(root.parent / "x", "CLAUDE.md") if root.parent != root else None
    return "the owner"


def kind_table(src: Path) -> dict[str, tuple[str, str]]:
    """kind name (lower, singular) → (glossary definition, proof from the standard's kinds table); {} when absent."""
    root = workspace_root(src, "glossary.md", "documentation_standard.md")
    if root is None:
        return {}
    table: dict[str, tuple[str, str]] = {}
    for b in parse(root.joinpath("glossary.md").read_text(encoding="utf-8", errors="replace")):
        if b.kind == "table" and b.header and re.search(r"^term$", b.header[0].strip(), re.I) and len(b.header) >= 2:
            for row in b.rows:
                if len(row) >= 2:
                    table[plain(row[0]).lower().rstrip("s")] = (row[1], "")
    for b in parse(root.joinpath("documentation_standard.md").read_text(encoding="utf-8", errors="replace")):
        if b.kind == "table" and b.header and re.search(r"^kind$", b.header[0].strip(), re.I):
            proof_i = next((i for i, h in enumerate(b.header) if re.search(r"proof", h, re.I)), None)
            if proof_i is None:
                continue
            for row in b.rows:
                if len(row) > proof_i:
                    key = plain(row[0]).lower().rstrip("s")
                    if key in table:
                        table[key] = (table[key][0], row[proof_i])
    return table


def relative_doc(src: Path, pointer: str) -> Path | None:
    """Resolve a header pointer such as `../../<initiative>/state.md` against the source's folder."""
    m = re.search(r"[\w./~-]+\.md", plain(pointer).replace("`", ""))
    if not m:
        return None
    cand = (src.parent / m.group(0)).resolve()
    return cand if cand.is_file() else None


# ----------------------------------------------------------------------------
# Plan: the project log's last ship review (Gate 3)
# ----------------------------------------------------------------------------

SHIP_RE = re.compile(r"^ship review", re.I)
GO_LIVE_RE = re.compile(r"^go-?live", re.I)
QUESTIONS = ("blast radius", "what breaks", "who notices", "fallback", "contingency", "how we fix it",
             "concludes without testing")
DISPOSITION_RE = re.compile(r"→\s*\*\*(fixed|escalated|filed|accept\w*|verified[^*:]*)", re.I)
DISPOSITION_CLASS = {"fixed": "ok", "verified": "ok", "accept": "pending", "escalated": "fail", "filed": "pending"}


def field_runs(body):
    """Label → HTML, in order, for a body of `**Label:**` fields where a bare label takes the block that follows."""
    out: dict[str, str] = {}
    order: list[str] = []
    rest = []
    i = 0
    while i < len(body):
        b = body[i]
        if b.kind == "fields":
            for j, (k, v) in enumerate(b.items):
                html = inline(v)
                if not v.strip() and j == len(b.items) - 1 and i + 1 < len(body) and body[i + 1].kind in ("list", "table", "para"):
                    html = html_block(body[i + 1])
                    i += 1
                out[k.lower()] = html
                order.append(k)
        else:
            rest.append(b)
        i += 1
    return out, order, rest


def holes_list(body) -> str | None:
    """The `Holes & dispositions` bullets with a pill per disposition; None when the review has none."""
    for i, b in enumerate(body):
        if b.kind == "fields" and any(k.lower().startswith("holes") for k, _ in b.items):
            nxt = body[i + 1] if i + 1 < len(body) else None
            if nxt is not None and nxt.kind == "list":
                items = []
                for it in nxt.items:
                    m = DISPOSITION_RE.search(it.text)
                    word = m.group(1).strip().rstrip(":") if m else ""
                    cls = next((c for k, c in DISPOSITION_CLASS.items() if word.lower().startswith(k)), "pending")
                    pill = f'<span class="pill {cls}">{esc(word.split()[0].capitalize())}</span> ' if word else ""
                    items.append(f"<li>{pill}{item_body(it)}</li>")
                return '<ul class="holes">' + "".join(items) + "</ul>"
            val = next(v for k, v in b.items if k.lower().startswith("holes"))
            return f"<p>{inline(val)}</p>" if val.strip() else None
    return None


def ship_review_html(body) -> str:
    fields, order, rest = field_runs(body)
    out = []
    notes = [b for b in rest if b.kind == "para"]
    for b in notes:
        out.append(f'<p class="note">{inline(b.text)}</p>')
    rows = [(k, fields[k.lower()]) for k in order if k.lower() in QUESTIONS]
    if rows:
        out.append('<dl class="fields">' + "".join(f"<dt>{inline(k)}</dt><dd>{v}</dd>" for k, v in rows) + "</dl>")
    holes = holes_list(body)
    if holes:
        out.append(f'<h3 class="sub">Holes &amp; dispositions</h3>{holes}')
    tail = [(k, fields[k.lower()]) for k in order if k.lower() not in QUESTIONS and not k.lower().startswith("holes")]
    if tail:
        out.append('<dl class="fields">' + "".join(f"<dt>{inline(k)}</dt><dd>{v}</dd>" for k, v in tail) + "</dl>")
    for b in rest:
        if b.kind not in ("para", "list"):
            out.append(html_block(b))
    return "".join(out)


def last_status(blocks) -> str | None:
    """The most recent top-level `**Status:**` field in the log — the header's, or the close's."""
    status = None
    for b in blocks:
        if b.kind == "fields":
            for k, v in b.items:
                if k.lower() == "status":
                    status = v
    return status


def header_pointers(pre) -> list[tuple[str, str]]:
    """PRD · Memo · Initiative pointers, from header fields or from a `PRD: `x.md`` sentence."""
    found: dict[str, str] = {}
    for b in pre:
        if b.kind == "fields":
            for k, v in b.items:
                if k.lower() in ("prd", "memo", "initiative"):
                    found[k.lower()] = v
        elif b.kind == "para":
            for m in re.finditer(r"\b(PRD|Memo|Initiative):\s*(`[^`]+`|\S+)", b.text):
                found.setdefault(m.group(1).lower(), m.group(2).rstrip("."))
    return [(k.upper() if k == "prd" else k.capitalize(), found[k]) for k in ("prd", "memo", "initiative") if k in found]


def plan_ship(blocks, src: Path) -> tuple[str, str]:
    pre, secs = split_sections(blocks, 2)
    title, subtitle, fields, order, notes = header_parts(pre)
    title = title or src.parent.name
    out = ['<header class="doc-head">', '<p class="eyebrow">Gate 3 · Ship review</p>', f"<h1>{esc(title)}</h1>"]
    if subtitle:
        out.append(f'<p class="subtitle">{inline(subtitle)}</p>')
    status = last_status(blocks)
    rows = ([("Status", status_pill(status))] if status else []) + [(k, inline(v)) for k, v in header_pointers(pre)]
    if rows:
        out.append('<dl class="fields">' + "".join(f"<dt>{k}</dt><dd>{v}</dd>" for k, v in rows) + "</dl>")
    out.append("</header>")

    reviews = [i for i, (h, _) in enumerate(secs) if SHIP_RE.match(plain(h.text))]
    used = set()
    if not reviews:
        out.append('<div class="callout"><h3>Ship review</h3><p class="empty">No ship review recorded in this log yet.</p></div>')
    else:
        last = reviews[-1]
        used.add(last)
        h, body = secs[last]
        out.append(open_section(inline(h.text), ship_review_html(body), "ship"))
        if last + 1 < len(secs) and GO_LIVE_RE.match(plain(secs[last + 1][0].text)):
            used.add(last + 1)
            gh, gbody = secs[last + 1]
            out.append(open_section(inline(gh.text), ship_review_html(gbody), "go-live"))
        for i in reviews[:-1]:
            used.add(i)
            out.append(folded_section(inline(secs[i][0].text), secs[i][1], "earlier-round"))
    for i, (h, body) in enumerate(secs):
        if i not in used:
            out.append(folded_section(inline(h.text), body))
    return title, "".join(out)


# ----------------------------------------------------------------------------
# Plan: the state file (the handoff)
# ----------------------------------------------------------------------------

STATE_LABELS = ("stage", "done", "next", "blocked", "router", "live", "prd", "memo", "initiative", "updated", "project")
LABEL_SPLIT_RE = re.compile(r"\s*(?:·\s*)?\*\*(" + "|".join(STATE_LABELS) + r"):\*\*\s*", re.I)
FRACTION_RE = re.compile(r"(\d+)\s*/\s*(\d+)")
WI_NAME_RE = re.compile(r"\b(?:WI|work item)[-\s]*(\d+)\b", re.I)


def expand_labels(label: str, value: str) -> list[tuple[str, str]]:
    """`Initiative: a · **PRD:** b · **Memo:** c` on one line → three pairs."""
    parts = LABEL_SPLIT_RE.split(value)
    pairs = [(label, parts[0].strip().rstrip("·").strip())]
    for i in range(1, len(parts) - 1, 2):
        pairs.append((parts[i], parts[i + 1].strip().rstrip("·").strip()))
    return pairs


def state_fields(blocks) -> tuple[dict[str, str], list[str]]:
    """Every labelled line of a state file — header fields and Position bullets — as label → text."""
    fields: dict[str, str] = {}
    order: list[str] = []
    def put(k, v):
        for kk, vv in expand_labels(k, v):
            if kk.lower() not in fields:
                fields[kk.lower()] = vv
                order.append(kk)
    for b in blocks:
        if b.kind == "fields":
            for k, v in b.items:
                put(k, v)
        elif b.kind == "list":
            for it in b.items:
                if it.label:
                    put(it.label, it.text)
    return fields, order


def ribbon(stage: str) -> str:
    spans = []
    for piece in re.split(r"\s*·\s*", stage):
        piece = piece.strip()
        if not piece:
            continue
        name, _, rest = piece.partition(" ")
        frac = FRACTION_RE.search(rest)
        if "✅" in rest or "✓" in rest:
            mark = "done"
        elif frac:
            mark = "done" if int(frac.group(1)) >= int(frac.group(2)) else "active"
        elif "▶" in rest or re.search(r"\b(in progress|building|running)\b", rest, re.I):
            mark = "active"
        else:
            mark = "todo"
        show = f"{name} {frac.group(0)}" if frac else f"{name} {GLYPH[mark]}"
        spans.append(f'<span class="{mark}" title="{esc(plain(piece), quote=True)}">{esc(show)}</span>')
    return f'<div class="ribbon">{"".join(spans)}</div>' if spans else ""


CHAIN_LABEL_RE = re.compile(r"^([^→:]{1,60}):\s*(.*→.*)$")


def html_chain(text: str) -> str:
    """Each non-blank line of a ```chain fence is one strip: `Label: A → B → C` or `A → B → C`."""
    rows = []
    for line in text.splitlines():
        line = line.strip()
        if not line:
            continue
        label = None
        m = CHAIN_LABEL_RE.match(line)
        if m:
            label, line = m.group(1).strip(), m.group(2)
        segs = [seg.strip() for seg in line.split("→") if seg.strip()]
        lab = f'<span class="label">{inline(label)}</span>' if label else ""
        items = "".join(f"<li><span>{inline(seg)}</span></li>" for seg in segs)
        rows.append(f'<div class="chain">{lab}<ol>{items}</ol></div>')
    return f'<div class="chains">{"".join(rows)}</div>' if rows else ""


# ----------------------------------------------------------------------------
# The map: a drawn picture from a ```map fence (declared grid → inline SVG)
# ----------------------------------------------------------------------------

NODE_RE = re.compile(r"^node\s+(\w+)\s+(\d+),(\d+)(?:\s+(gate|check|end))?\s*::\s*(.+)$")
BOX_RE = re.compile(r"^box\s+(\w+)\s+(\d+),(\d+)-(\d+),(\d+)\s*::\s*(.+)$")
EDGE_RE = re.compile(r"^(\w+)\s+(->|\.\.>)\s+(\w+)(?:\s*::\s*(.+))?$")

MAP_CELL_W, MAP_CELL_H = 138, 74          # one grid cell
MAP_NODE_W, MAP_NODE_H = 124, 46          # a node, centred in its cell
MAP_END_W = 84                            # an end node is a pill this wide
MAP_MARGIN = 12
MAP_BOX_HEAD = 22                         # a box grows upward this much for its label row
MAP_LANE = 34                             # the first loop lane sits this far below the last row
MAP_LANE_STEP = 26                        # each further loop lane sits this much lower
MAP_LOOP_SPREAD = 18                      # end-points of loops into one node sit this far apart
MAP_LABEL_LINE = 14                       # line pitch of a multi-line edge label
MAP_LABEL_CHAR = 6                        # estimated width per label character (for the refusal)
MAP_NODE_LABEL_MAX = 20
MAP_CHECK_H = 60                          # a check node is a diamond this tall (one label line)


def _num(v: float) -> str:
    return str(int(v)) if float(v).is_integer() else f"{v:.1f}"


class _Shape:
    def __init__(self, sid, x, y, w, h, kind, lines, is_box=False):
        self.id, self.x, self.y, self.w, self.h, self.kind, self.lines, self.is_box = sid, x, y, w, h, kind, lines, is_box

    @property
    def cx(self): return self.x + self.w / 2
    @property
    def cy(self): return self.y + self.h / 2
    @property
    def right(self): return self.x + self.w
    @property
    def bottom(self): return self.y + self.h


def parse_map(text: str):
    """Statements of a ```map fence → (shapes by id in order, edges). ValueError quotes the offending line."""
    shapes, edges = {}, []
    for raw in text.splitlines():
        line = raw.strip()
        if not line:
            continue
        m = NODE_RE.match(line)
        if m:
            sid, col, row, kind, label = m.group(1), int(m.group(2)), int(m.group(3)), m.group(4) or "", m.group(5)
            lines = [s.strip() for s in label.split(" / ")]
            for ln in lines:
                if len(ln) > MAP_NODE_LABEL_MAX:
                    raise ValueError(f"map: node label line over {MAP_NODE_LABEL_MAX} characters: {line!r}")
            if m.group(4) == "check" and len(lines) > 1:
                raise ValueError(f"map: a check node (a diamond) takes one label line: {line!r}")
            shapes[sid] = ("node", col, row, col, row, kind, lines)
            continue
        m = BOX_RE.match(line)
        if m:
            sid = m.group(1)
            c1, r1, c2, r2 = (int(m.group(i)) for i in range(2, 6))
            shapes[sid] = ("box", c1, r1, c2, r2, "", [m.group(6).strip()])
            continue
        m = EDGE_RE.match(line)
        if m:
            a, arrow, b, label = m.groups()
            for ref in (a, b):
                if ref not in shapes:
                    raise ValueError(f"map: edge names an unknown id {ref!r}: {line!r}")
            lines = [s.strip() for s in label.split(" / ")] if label else []
            edges.append((a, b, arrow == "..>", lines, line))
            continue
        raise ValueError(f"map: unreadable line: {line!r}")
    return shapes, edges


def _place(shapes):
    """Grid coordinates → pixel shapes."""
    placed = {}
    for sid, (kind, c1, r1, c2, r2, sub, lines) in shapes.items():
        x0 = MAP_MARGIN + (c1 - 1) * MAP_CELL_W
        y0 = MAP_MARGIN + (r1 - 1) * MAP_CELL_H
        if kind == "box":
            w = (c2 - c1 + 1) * MAP_CELL_W - 8
            h = (r2 - r1 + 1) * MAP_CELL_H + MAP_BOX_HEAD
            placed[sid] = _Shape(sid, x0 + 4, y0 - MAP_BOX_HEAD, w, h, "box", lines, True)
        else:
            w = MAP_END_W if sub == "end" else MAP_NODE_W
            h = MAP_CHECK_H if sub == "check" else MAP_NODE_H
            placed[sid] = _Shape(sid, x0 + (MAP_CELL_W - w) / 2, y0 + (MAP_CELL_H - h) / 2, w, h, sub, lines)
    return placed


def _label(x, y, lines, anchor="middle", cls="elabel"):
    out = []
    for i, ln in enumerate(lines):
        out.append(f'<text class="{cls}" x="{_num(x)}" y="{_num(y + i * MAP_LABEL_LINE)}" text-anchor="{anchor}">{esc(ln)}</text>')
    return "".join(out)


def html_map(text: str) -> str:
    """A ```map fence → one inline SVG: boxes behind, then edges, then nodes. Three connector cases only."""
    shapes, edges = parse_map(text)
    if not shapes:
        return ""
    placed = _place(shapes)
    ncols = max(max(v[1], v[3]) for v in shapes.values())
    nrows = max(max(v[2], v[4]) for v in shapes.values())
    width = 2 * MAP_MARGIN + ncols * MAP_CELL_W
    rows_bottom = MAP_MARGIN + nrows * MAP_CELL_H

    # loop edges (target to the left) share the lane below the last row; the k-th sits one step lower
    loops = [i for i, (a, b, *_rest) in enumerate(edges) if placed[b].cx < placed[a].cx]
    lane_of = {i: rows_bottom + MAP_LANE + k * MAP_LANE_STEP for k, i in enumerate(loops)}
    height = rows_bottom + MAP_MARGIN
    if loops:
        height = max(lane_of.values()) + MAP_LABEL_LINE + MAP_MARGIN

    # end-points of several loops into one node (or out of one node) spread apart; the lower lane takes the left slot
    def spread(key):
        groups = {}
        for i in loops:
            groups.setdefault(key(edges[i]), []).append(i)
        out = {}
        for members in groups.values():
            n = len(members)
            for j, i in enumerate(sorted(members, key=lambda i: -lane_of[i])):
                out[i] = (j - (n - 1) / 2) * MAP_LOOP_SPREAD
        return out
    dx_target = spread(lambda e: e[1])
    dx_source = spread(lambda e: e[0])

    svg = [f'<div class="map"><svg class="map-svg" viewBox="0 0 {width} {_num(height)}" width="{width}" height="{_num(height)}" '
           f'role="img" aria-label="the lifecycle map">',
           '<defs><marker id="arrow" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="7" markerHeight="7" '
           'orient="auto-start-reverse"><path d="M0,0 L10,5 L0,10 z"/></marker></defs>']

    for s in placed.values():
        if s.is_box:
            svg.append(f'<g class="box"><rect x="{_num(s.x)}" y="{_num(s.y)}" width="{_num(s.w)}" height="{_num(s.h)}" rx="8"/>'
                       + _label(s.x + 10, s.y + 15, s.lines, "start", "") + "</g>")

    for i, (a, b, dashed, lines, line) in enumerate(edges):
        s, t = placed[a], placed[b]
        cls = "edge dashed" if dashed else "edge"
        label_html = ""
        if abs(t.cx - s.cx) < 0.5:                                   # case 1: same column
            if t.cy > s.cy:
                y1, y2 = s.bottom, t.y
            else:
                y1, y2 = s.y, t.bottom
            d = f"M{_num(s.cx)},{_num(y1)} V{_num(y2)}"
            if lines:
                mid = (y1 + y2) / 2
                label_html = _label(s.cx - 8, mid + 4 - (len(lines) - 1) * MAP_LABEL_LINE / 2, lines, "end")
        elif t.cx > s.cx:                                            # case 2: target to the right
            x1, x2 = s.right, t.x
            if abs(t.cy - s.cy) < 0.5:
                if lines and max(len(ln) for ln in lines) * MAP_LABEL_CHAR > (x2 - x1) + MAP_CELL_W:
                    raise ValueError(f"map: same-row label wider than the gap between its nodes: {line!r}")
                d = f"M{_num(x1)},{_num(s.cy)} H{_num(x2)}"
                if lines:
                    narrow = max(len(ln) for ln in lines) * MAP_LABEL_CHAR > (x2 - x1)
                    base = min(s.y, t.y) - 4 if narrow else s.cy - 7      # a label wider than its gap sits above the node tops
                    label_html = _label((x1 + x2) / 2, base - (len(lines) - 1) * MAP_LABEL_LINE, lines)
            elif s.kind == "check":                                  # a diamond's exits leave from its top or bottom point
                y1 = s.y if t.cy < s.cy else s.bottom
                d = f"M{_num(s.cx)},{_num(y1)} V{_num(t.cy)} H{_num(x2)}"
                if lines:                                            # label right-aligned left of the vertical
                    mid = (y1 + t.cy) / 2
                    label_html = _label(s.cx - 8, mid + 4 - (len(lines) - 1) * MAP_LABEL_LINE / 2, lines, "end")
            else:
                adjacent = (x2 - x1) < MAP_CELL_W
                vx = (x1 + x2) / 2 if adjacent else x2 - (MAP_CELL_W - MAP_NODE_W) / 2
                d = f"M{_num(x1)},{_num(s.cy)} H{_num(vx)} V{_num(t.cy)} H{_num(x2)}"
                if lines:
                    mid = (s.cy + t.cy) / 2
                    if abs(t.cy - s.cy) > 40:
                        label_html = _label(vx + 8, mid + 4 - (len(lines) - 1) * MAP_LABEL_LINE / 2, lines, "start")
                    else:
                        label_html = _label((x1 + x2) / 2, min(s.cy, t.cy) - 7 - (len(lines) - 1) * MAP_LABEL_LINE, lines)
        else:                                                        # case 3: target to the left — a loop beneath
            lane = lane_of[i]
            sx = s.cx + dx_source.get(i, 0)
            tx = t.cx + dx_target.get(i, 0)
            d = f"M{_num(sx)},{_num(s.bottom)} V{_num(lane)} H{_num(tx)} V{_num(t.bottom)}"
            if lines:
                label_html = _label((sx + tx) / 2, lane + MAP_LABEL_LINE, lines)
        svg.append(f'<path class="{cls}" d="{d}" marker-end="url(#arrow)"/>' + label_html)

    for s in placed.values():
        if s.is_box:
            continue
        cls = f"node {s.kind}".strip()
        rx = MAP_NODE_H / 2 if s.kind == "end" else 6
        if s.kind == "check":
            pts = f"{_num(s.cx)},{_num(s.y)} {_num(s.right)},{_num(s.cy)} {_num(s.cx)},{_num(s.bottom)} {_num(s.x)},{_num(s.cy)}"
            g = [f'<g class="{cls}"><polygon points="{pts}"/>']
        else:
            g = [f'<g class="{cls}"><rect x="{_num(s.x)}" y="{_num(s.y)}" width="{_num(s.w)}" height="{_num(s.h)}" rx="{_num(rx)}"/>']
        if len(s.lines) == 1:
            g.append(f'<text x="{_num(s.cx)}" y="{_num(s.cy + 5)}" text-anchor="middle">{esc(s.lines[0])}</text>')
        else:
            g.append(f'<text x="{_num(s.cx)}" y="{_num(s.cy - 3)}" text-anchor="middle">{esc(s.lines[0])}</text>')
            for j, ln in enumerate(s.lines[1:]):
                g.append(f'<text class="sub" x="{_num(s.cx)}" y="{_num(s.cy + 13 + j * 13)}" text-anchor="middle">{esc(ln)}</text>')
        g.append("</g>")
        svg.append("".join(g))
    svg.append("</svg></div>")
    return "".join(svg)


def progress_list(rows: list[tuple[str, str, str, str]]) -> str:
    """rows of (number, name, status text, mark) → an ordered progress list."""
    out = ['<ol class="progress">']
    for num, name, status, mark in rows:
        n = f'<span class="num">{esc(num)}</span>' if num else ""
        st = f'<span class="status">{status}</span>' if status else "<span></span>"
        out.append(f'<li class="{mark}"><span class="mark {mark}">{GLYPH[mark]}</span><span class="name">{n}{name}</span>{st}</li>')
    out.append("</ol>")
    return "".join(out)


def work_item_progress(prd_path: Path, fields: dict[str, str]) -> str:
    blocks = parse(prd_path.read_text(encoding="utf-8", errors="replace"))
    items = []
    for b in blocks:
        if b.kind == "heading" and b.level == 3:
            m = WI_RE.match(plain(b.text))
            if m:
                items.append((int(m.group(1)), m.group(2)))
    if not items:
        return ""
    done = {int(n) for n in WI_NAME_RE.findall(fields.get("done", ""))}
    nxt = {int(n) for n in WI_NAME_RE.findall(fields.get("next", ""))}
    frac = FRACTION_RE.search(fields.get("stage", ""))
    built = int(frac.group(1)) if frac and "build" in fields.get("stage", "").lower() else 0
    rows = []
    for num, name in items:
        mark = "active" if num in nxt and num not in done else "done" if num in done or num <= built else "todo"
        rows.append((str(num), inline(name), "", mark))
    return f'<h3 class="sub">Work items</h3>{progress_list(rows)}'


def milestone_progress(blocks, heading: bool = True) -> str:
    for b in blocks:
        if b.kind == "table" and b.header and any(re.search(r"milestone", h, re.I) for h in b.header):
            name_i = next(i for i, h in enumerate(b.header) if re.search(r"milestone", h, re.I))
            status_i = next((i for i, h in enumerate(b.header) if re.search(r"status", h, re.I)), len(b.header) - 1)
            rows = []
            for row in b.rows:
                if len(row) <= max(name_i, status_i):
                    continue
                status = plain(row[status_i])
                low = status.lower()
                mark = ("done" if re.match(r"^(shipped|reached|complete|done|live|closed)", low)
                        else "active" if re.match(r"^(building|in flight|designing|memo|prd|ship|open)", low)
                        else "todo")
                num = row[0].strip() if name_i != 0 else ""
                rows.append((num, inline(row[name_i]), inline(row[status_i]), mark))
            return (('<h3 class="sub">Milestones</h3>' if heading else "") + progress_list(rows)) if rows else ""
    return ""


def accepted_residuals(log_path: Path) -> str:
    blocks = parse(log_path.read_text(encoding="utf-8", errors="replace"))
    _, secs = split_sections(blocks, 2)
    reviews = [i for i, (h, _) in enumerate(secs) if SHIP_RE.match(plain(h.text))]
    if not reviews:
        return ""
    body = secs[reviews[-1]][1]
    for i, b in enumerate(body):
        if b.kind == "fields" and any(k.lower().startswith("holes") for k, _ in b.items) and i + 1 < len(body) and body[i + 1].kind == "list":
            acc = [it for it in body[i + 1].items if re.search(r"→\s*\*\*accept", it.text, re.I)]
            if acc:
                return '<h3 class="sub">Accepted residuals</h3><ul class="residuals">' + "".join(f"<li>{item_body(it)}</li>" for it in acc) + "</ul>"
    return ""


def callout(label: str, body_blocks) -> str:
    text = " ".join(plain(getattr(b, "text", "") or b.raw) for b in body_blocks).strip()
    if not body_blocks or re.fullmatch(r"[-—·\s]*none\.?[-—·\s]*", text, re.I):
        return f'<div class="callout"><h3>{esc(label)}</h3><p class="empty">none</p></div>'
    return f'<div class="callout"><h3>{esc(label)}</h3>{html_blocks(body_blocks)}</div>'


def plan_handoff(blocks, src: Path) -> tuple[str, str]:
    pre, secs = split_sections(blocks, 2)
    title, subtitle, _, _, notes = header_parts(pre)
    title = title or src.parent.name
    fields, order = state_fields(blocks)
    owner = owner_word(src)
    is_project = "stage" in fields or "done" in fields or "next" in fields and "milestones" not in {plain(h.text).lower() for h, _ in secs}
    out = ['<header class="doc-head">', f'<p class="eyebrow">{"Handoff" if is_project else "Initiative state"}</p>', f"<h1>{esc(title)}</h1>"]
    header_rows = [(k, fields[k.lower()]) for k in order if k.lower() in ("initiative", "prd", "memo", "updated")]
    if header_rows:
        out.append('<dl class="fields">' + "".join(f"<dt>{inline(k)}</dt><dd>{inline(v)}</dd>" for k, v in header_rows) + "</dl>")
    for b in notes:
        if b.kind == "para":
            out.append(f'<p class="note">{inline(b.text)}</p>')
    out.append("</header>")

    used = set()

    def take(pattern):
        i = find_section(secs, pattern)
        if i is None or i in used:
            return None
        used.add(i)
        return secs[i]

    if is_project:
        if "stage" in fields:
            out.append(ribbon(fields["stage"]))
        pos = take(r"^position")
        rows = [(k, fields[k.lower()]) for k in order if k.lower() in ("live", "done", "next", "blocked", "router")]
        extra = [b for b in (pos[1] if pos else []) if b.kind != "list"]
        out.append(open_section("Position", ('<dl class="fields">' + "".join(f"<dt>{inline(k)}</dt><dd>{inline(v)}</dd>" for k, v in rows) + "</dl>" if rows else "") + html_blocks(extra), "position"))
        needs = take(r"^needs\b")
        out.append(callout(f"Needs {owner}", needs[1] if needs else []))
        prd_path = relative_doc(src, fields["prd"]) if "prd" in fields else None
        if prd_path is None:
            cands = sorted(src.parent.glob("*_prd.md"))
            prd_path = cands[0] if cands else None
        if prd_path:
            out.append(work_item_progress(prd_path, fields))
        init_path = relative_doc(src, fields["initiative"]) if "initiative" in fields else None
        if init_path and init_path != src.resolve():
            out.append(milestone_progress(parse(init_path.read_text(encoding="utf-8", errors="replace"))))
        log_path = src.with_name("project_log.md")
        if log_path.is_file():
            out.append(accepted_residuals(log_path))
    else:
        flight = take(r"^in flight")
        if flight:
            out.append(open_section(inline(flight[0].text), html_blocks(flight[1]), "in-flight"))
        ms = take(r"^milestones")
        if ms:
            out.append(open_section(inline(ms[0].text), milestone_progress(ms[1], heading=False) or html_blocks(ms[1]), "milestones"))
        tray = take(r"inherit|tray")
        if tray:
            out.append(open_section(inline(tray[0].text), html_blocks(tray[1]), "tray"))
    for i, (h, body) in enumerate(secs):
        if i not in used:
            out.append(folded_section(inline(h.text), body))
    return title, "".join(out)


# ----------------------------------------------------------------------------
# The explainer: every section open in document order, the verification table folded
# ----------------------------------------------------------------------------

KNOWLEDGE_NAMES = {"why_we_build.md": "The explainer", "worked_example.md": "The worked example",
                   "lifecycle_map.md": "The lifecycle map"}
VERIFY_RE = re.compile(r"comes from|verification|sources", re.I)  # "where each" alone folded a section that merely used the words


def plan_explainer(blocks, src: Path) -> tuple[str, str]:
    pre, secs = split_sections(blocks, 2)
    title, subtitle, fields, order, notes = header_parts(pre)
    title = title or src.stem.replace("_", " ")
    eyebrow = KNOWLEDGE_NAMES.get(src.name, "The explainer")
    out = ['<header class="doc-head">', f'<p class="eyebrow">{eyebrow}</p>', f"<h1>{inline(title)}</h1>"]
    if subtitle:
        out.append(f'<p class="subtitle">{inline(subtitle)}</p>')
    out.append(html_blocks(notes))
    out.append("</header>")
    for h, body in secs:
        if VERIFY_RE.search(plain(h.text)):
            out.append(folded_section(inline(h.text), body, "verification"))
        else:
            out.append(plain_section(inline(h.text), body))
    return plain(title), "".join(out)


PLANS = {"memo": plan_memo, "prd": plan_prd, "ship": plan_ship, "handoff": plan_handoff, "explainer": plan_explainer}
OUTPUT_NAME = {"ship": "ship_review.html", "handoff": "handoff.html"}


# ----------------------------------------------------------------------------
# Detection, page, CLI
# ----------------------------------------------------------------------------

def detect(path: Path, text: str) -> str | None:
    name = path.name
    if name.endswith("_prd.md"):
        return "prd"
    if name == "project_log.md":
        return "ship"
    if name == "state.md":
        return "handoff"
    if name in KNOWLEDGE_NAMES:
        return "explainer"
    head = text[:3000]
    if re.search(r"^_.*build-intent memo", head, re.I | re.M) or "/memos/" in path.resolve().as_posix():
        return "memo"
    return None


def output_path(path: Path, kind: str) -> Path:
    return path.with_name(OUTPUT_NAME.get(kind, f"{path.stem}.html"))


def page(title: str, body: str, source_name: str) -> str:
    css = CSS_PATH.read_text(encoding="utf-8")
    return (
        "<!doctype html>\n<html lang=\"en\">\n<head>\n<meta charset=\"utf-8\">\n"
        "<meta name=\"viewport\" content=\"width=device-width, initial-scale=1\">\n"
        f"<title>{esc(title)}</title>\n<style>\n{css}\n</style>\n</head>\n<body>\n"
        f"<main class=\"companion\">\n{body}\n"
        f"<footer class=\"doc-foot\">Companion of <code>{esc(source_name)}</code>. Generated from the markdown, "
        "which stays the source; regenerated by the skill step that writes the document, never edited by hand.</footer>\n"
        "</main>\n</body>\n</html>\n"
    )


def render_text(path: Path) -> tuple[Path, str]:
    """The page a source would get, without writing it: (the companion's path, its text)."""
    text = path.read_text(encoding="utf-8")
    kind = detect(path, text)
    if kind is None:
        raise ValueError(f"{path}: not a memo, PRD, project log, state file, the explainer, the worked example or the lifecycle map")
    plan = PLANS[kind]
    blocks = parse(text)
    title, body = plan(blocks, path)
    return output_path(path, kind), page(title, body, path.name)


def render(path: Path) -> Path:
    out, text = render_text(path)
    out.write_text(text, encoding="utf-8")
    return out


def source_for(html_path: Path) -> Path | None:
    if html_path.name == "ship_review.html":
        cand = html_path.with_name("project_log.md")
    elif html_path.name == "handoff.html":
        cand = html_path.with_name("state.md")
    else:
        cand = html_path.with_suffix(".md")
    if not cand.exists():
        return None
    try:
        return cand if detect(cand, cand.read_text(encoding="utf-8")) else None
    except OSError:
        return None


def stale(root: Path) -> list[Path]:
    found = []
    for h in sorted(root.rglob("*.html")):
        src = source_for(h)
        if src and src.stat().st_mtime > h.stat().st_mtime:
            found.append(h)
    return found


def main(argv: list[str]) -> int:
    if not argv or argv[0] in ("-h", "--help"):
        print(__doc__.strip())
        return 0 if argv else 1
    if argv[0] == "--stale":
        if len(argv) != 2:
            print("usage: render.py --stale <dir>", file=sys.stderr)
            return 1
        for p in stale(Path(argv[1])):
            print(p)
        return 0
    rc = 0
    for arg in argv:
        p = Path(arg)
        try:
            print(render(p))
        except (ValueError, OSError) as e:
            print(str(e), file=sys.stderr)
            rc = 1
    return rc


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
