#!/usr/bin/env python3
"""Offer the kit's CLAUDE.md template lines to a person's own map, section by section.

  map_update.py plan  <map>
      what each section would change; exit 0 nothing to offer, 3 an offer (last line: fingerprint: <16 hex>)
  map_update.py apply <map> --expect <fingerprint> --take "<heading>" ... [--slot 'name=value' ...]
      write only the taken sections; exit 0 written or already current, 1 refused with nothing written
      before writing, the map's bytes are copied to the system temp folder; the last line is the undo:
      "To undo: cp <copy> <map>"
  The heading of the text above the first `##` is "(top of the file)".  Plan never writes.

A line of the map is the kit's only when it matches a line the template ships now or a line an earlier
template shipped.  Every other line is the person's and is never changed, moved or removed.  A `{slot}`
in a template line matches any text; its value is read from the map, or given with --slot.

claude_md_template.retired, beside the template, holds every line an earlier shipped template held and
the current one does not, verbatim, one per line (blank lines ignored, no comments: every line is data).
It is append-only.  kit_promote.py refuses a template change until the lines it retires are on it.
"""
import argparse, difflib, hashlib, re, shlex, sys, tempfile
from pathlib import Path

HERE = Path(__file__).resolve().parent
TEMPLATE, RETIRED = HERE / "claude_md_template.md", HERE / "claude_md_template.retired"
SLOT = re.compile(r"(?<!\{)\{([^{}]+)\}(?!\})")
LITERAL = {"tool"}                      # the two literals /onboard leaves: {tool} and {{System}}
H2 = re.compile(r"^##\s+(.*?)\s*$")
PREAMBLE = "(top of the file)"
SEP = re.compile(r"\|[\s\-:|]+\|")


def sections(text):
    """[[heading, [lines]]]; the first is the preamble (heading None).  Fence-aware."""
    out, fence = [[None, []]], False
    for ln in text.split("\n"):
        if ln.lstrip().startswith("```"):
            fence = not fence
        m = None if fence else H2.match(ln)
        if m:
            out.append([m.group(1), [ln]])
        else:
            out[-1][1].append(ln)
    return out


def norm(s):
    s = re.sub(r"\s+", " ", s.strip())
    return re.sub(r"\s*\|\s*", "|", s) if s.startswith("|") else s


def slots(line):
    return [m.group(1) for m in SLOT.finditer(line) if m.group(1) not in LITERAL]


def pattern(line):
    n, parts, pos = norm(line), [], 0
    for m in SLOT.finditer(n):
        if m.group(1) in LITERAL:
            continue
        parts += [re.escape(n[pos:m.start()]), "(.+?)"]
        pos = m.end()
    parts.append(re.escape(n[pos:]))
    return re.compile("".join(parts) + r"\Z")


def is_unit(line, heading):
    s = line.strip()
    if not s or s.startswith("<!--") or H2.match(s):
        return False
    if heading is None and s.startswith("# "):
        return False                     # the person's title
    if slots(s) and not SLOT.sub("", s).replace("|", "").strip():
        return False                     # a slot-only line: the routing placeholder row
    return True


def kind(line):
    s = line.strip()
    return "table" if s.startswith("|") else "list" if re.match(r"([-*]|\d+\.)\s", s) else "para"


def bare(s):
    return SLOT.sub("", norm(s))


class Kit:
    def __init__(self, template, retired):
        self.template = template
        self.secs = [(h, [l for l in ls if is_unit(l, h)]) for h, ls in sections(template)]
        self.gaps = {}                   # heading -> [a blank line stands before unit j in the template]
        for h, ls in sections(template):
            gaps, blank = [], False
            for l in ls:
                if is_unit(l, h):
                    gaps.append(blank); blank = False
                elif not l.strip():
                    blank = True
            self.gaps[h] = gaps
        self.retired = [(l, pattern(l)) for l in retired.split("\n") if l.strip()]


def capture(mline, tline):
    m = pattern(tline).match(norm(mline))
    return dict(zip(slots(norm(tline)), m.groups())) if m else None


def plan(kit, text):
    """Return (offers, values): offers = [{heading, ops}] with ops as (op, map_index|None, template_line)."""
    msecs = sections(text)
    mhead = {h: i for i, (h, _) in enumerate(msecs)}
    values, offers = {}, []
    for h, units in kit.secs:
        if not units:
            continue
        cur = [(u, pattern(u)) for u in units]
        if h not in mhead:
            offers.append({"heading": h, "new": True, "ops": [("add", None, u) for u in units]})
            continue
        lines = msecs[mhead[h]][1]
        has_table = any(kind(l) == "table" for l in lines if l.strip())
        anchor, missing, used = {}, [], set()
        for j, (u, p) in enumerate(cur):
            hit = next((i for i, l in enumerate(lines) if i not in used and l.strip() and p.match(norm(l))), None)
            if hit is None and has_table and (SEP.fullmatch(u.strip()) or (j + 1 < len(units) and SEP.fullmatch(units[j + 1].strip()))):
                continue                 # a table header or separator: their section already has a table
            if hit is None:
                missing.append(j)
            else:
                used.add(hit); anchor[j] = hit
                values.update({k: v for k, v in (capture(lines[hit], u) or {}).items() if k not in values})
        old = [i for i, l in enumerate(lines) if i not in used and l.strip() and is_unit(l, h)
               and any(p.match(norm(l)) for _, p in kit.retired)]
        for i in old:
            for r, _ in kit.retired:
                values.update({k: v for k, v in (capture(lines[i], r) or {}).items() if k not in values})
        ops, pairs = [], sorted(((difflib.SequenceMatcher(None, bare(units[j]), bare(lines[i])).ratio(), j, i)
                                 for j in missing for i in old), reverse=True)
        paired = {}
        for _, j, i in pairs:             # best match first, so a rewrite pairs with its own old line
            if j not in paired and i not in paired.values():
                paired[j] = i
        for j in missing:
            if j in paired:
                old.remove(paired[j]); anchor[j] = paired[j]
                ops.append(("replace", paired[j], units[j]))
            else:
                ops.append(("insert", j, units[j]))
        ops += [("remove", i, None) for i in old]
        if ops:
            offers.append({"heading": h, "new": False, "ops": ops, "anchor": anchor})
    return offers, values


def fill(line, values):
    return SLOT.sub(lambda m: m.group(0) if m.group(1) in LITERAL else values[m.group(1)], line)


def needed(offers):
    return sorted({s for o in offers for op in o["ops"] if op[2] for s in slots(op[2])})


def write(kit, text, offers, values):
    msecs = sections(text)
    for o in offers:
        if o["new"]:
            continue
        idx = next(i for i, (h, _) in enumerate(msecs) if h == o["heading"])
        lines, anchor = msecs[idx][1], o["anchor"]
        units = dict(kit.secs)[o["heading"]]
        inserts = {}
        for op, where, u in o["ops"]:
            if op == "replace":
                lines[where] = fill(u, values)
            elif op == "remove":
                lines[where] = None
            else:
                prev = [anchor[k] for k in range(where) if k in anchor]
                nxt = [anchor[k] for k in range(where + 1, len(units)) if k in anchor]
                at = max(prev) if prev else (min(nxt) - 1 if nxt else
                                             max((i for i, l in enumerate(lines) if l and l.strip()), default=0))
                inserts.setdefault(at, []).append((where, fill(u, values)))
        gaps, unit_at = kit.gaps[o["heading"]], {i: j for j, i in anchor.items()}

        def apart(prev, prev_j, new, new_j):
            """A blank line between two lines: the template's own spacing between neighbouring kit lines,
            else whenever the kinds differ or both are paragraphs (so a kit line never joins the person's)."""
            if prev_j is not None and new_j is not None and new_j == prev_j + 1:
                return gaps[new_j]
            return kind(prev) != kind(new) or kind(new) == "para"
        out, out_j = [], []
        for i, l in enumerate(lines):
            if l is not None:
                out.append(l); out_j.append(unit_at.get(i))
            for j, new in inserts.get(i, []):
                k = next((x for x in range(len(out) - 1, -1, -1) if out[x].strip()), None)
                if k is not None and out[-1].strip() and apart(out[k], out_j[k], new, j):
                    out.append(""); out_j.append(None)
                out.append(new); out_j.append(j)
            if i in inserts and i + 1 < len(lines) and lines[i + 1] and lines[i + 1].strip() \
                    and apart(out[-1], out_j[-1], lines[i + 1], unit_at.get(i + 1)):
                out.append(""); out_j.append(None)
        msecs[idx][1] = out
    text = "\n".join("\n".join(ls) for _, ls in msecs)
    for o in offers:                      # whole new sections, at the end of the file, in template order
        if not o["new"]:
            continue
        body, gaps = [f"## {o['heading']}", ""], kit.gaps[o["heading"]]
        for j, u in enumerate(o["ops"]):
            if j and gaps[j]:
                body.append("")
            body.append(fill(u[2], values))
        text = text.rstrip("\n") + "\n\n" + "\n".join(body) + "\n"
    return text


def changed_words(a, b):
    """The words that change, in plain pairs: 'the one door' becomes 'the one starting point'."""
    wa, wb, out = a.split(), b.split(), []
    for tag, i1, i2, j1, j2 in difflib.SequenceMatcher(None, wa, wb).get_opcodes():
        if tag == "replace":
            out.append(f"'{' '.join(wa[i1:i2])}' becomes '{' '.join(wb[j1:j2])}'")
        elif tag == "delete":
            out.append(f"'{' '.join(wa[i1:i2])}' is removed")
        elif tag == "insert":
            out.append(f"'{' '.join(wb[j1:j2])}' is added after '{' '.join(wa[max(i1 - 3, 0):i1])}'")
    return out


def show(offers, text, values):
    lines_of = {h: ls for h, ls in sections(text)}
    for o in offers:
        h = o["heading"] or PREAMBLE
        if o["new"]:
            print(f"\n## {h}: not in your map. The kit's section would be added at the end, {len(o['ops'])} lines:")
            for _, _, u in o["ops"]:
                print(f"  + {fill(u, {k: values.get(k, '{' + k + '}') for k in slots(u)})}")
            continue
        print(f"\n## {h}")
        for op, where, u in o["ops"]:
            new = u and fill(u, {k: values.get(k, "{" + k + "}") for k in slots(u)})
            if op == "replace":
                mine = lines_of[o["heading"]][where].strip()
                words = changed_words(mine, new.strip())
                if len(words) <= 3 and len(mine) > 160:
                    print(f"  ~ in the line starting \"{' '.join(mine.split()[:6])} …\": " + "; ".join(words))
                else:
                    print(f"  ~ your line:  {mine}\n    becomes:    {new.strip()}")
            elif op == "remove":
                print(f"  - removed (the kit no longer ships it):  {lines_of[o['heading']][where].strip()}")
            else:
                print(f"  + added:  {new.strip()}")


def load_kit(template=TEMPLATE, retired=RETIRED):
    return Kit(template.read_text(encoding="utf-8"), retired.read_text(encoding="utf-8") if retired.exists() else "")


def main(argv=None):
    ap = argparse.ArgumentParser()
    ap.add_argument("mode", choices=["plan", "apply"])
    ap.add_argument("map")
    ap.add_argument("--take", action="append", default=[])
    ap.add_argument("--slot", action="append", default=[])
    ap.add_argument("--expect", help="the fingerprint plan printed; apply refuses when the map changed since")
    a = ap.parse_args(argv)
    kit, path = load_kit(), Path(a.map)
    raw = path.read_bytes()
    try:
        text = raw.decode("utf-8")       # no newline translation: untouched lines keep their bytes
    except UnicodeDecodeError:
        print("Your map is not UTF-8 text, so it cannot be read. Nothing was written."); return 1
    crlf = "\n" in text and text.count("\r\n") == text.count("\n")   # a map saved with Windows line endings
    offers, values = plan(kit, text)
    fp = hashlib.sha256(raw).hexdigest()[:16]
    if a.mode == "plan":
        if not offers:
            print("Your map carries the kit's current lines. Nothing to offer.")
            return 0
        show(offers, text, values)
        need = [s for s in needed(offers) if s not in values]
        if need:
            print("\nValues to ask for before these can be written: " + "; ".join(need))  # a slot name can hold a comma
        print(f"\nfingerprint: {fp}")
        return 3
    names = {(o["heading"] or PREAMBLE) for o in offers}
    kit_names = {(h or PREAMBLE) for h, units in kit.secs if units}
    bad = [t for t in a.take if t not in kit_names]
    if bad:
        print("Not a section of the kit's template: " + ", ".join(bad)); return 1
    if not any(t in names for t in a.take):
        print("Already current: " + ", ".join(a.take) + ". Nothing written."); return 0
    if a.expect != fp:
        print("Refused: the map changed since the offer was made (or no --expect was given). Run plan again; nothing written."); return 1
    taken = [o for o in offers if (o["heading"] or PREAMBLE) in a.take]
    values.update(dict(s.split("=", 1) for s in a.slot))
    need = [s for s in needed(taken) if s not in values]
    if need:
        print("Missing values: " + "; ".join(need)); return 1
    new = write(kit, text, taken, values)
    left, _ = plan(kit, new)
    if any((o["heading"] or PREAMBLE) in a.take for o in left):
        print("Refused: a taken section still differs after writing; nothing written."); return 1
    if crlf:
        new = re.sub(r"(?<!\r)\n", "\r\n", new)   # the kit's lines take the map's own line endings
    before = Path(tempfile.gettempdir()) / f"map_update-before-{fp}.md"
    try:
        before.write_bytes(raw)
    except OSError:
        print(f"Refused: could not keep a copy of the map for undo at {before}; nothing written."); return 1
    path.write_bytes(new.encode("utf-8"))
    print(f"Wrote {len(taken)} section(s): " + ", ".join(o["heading"] or PREAMBLE for o in taken))
    print(f"To undo: cp {shlex.quote(str(before))} {shlex.quote(str(path))}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
