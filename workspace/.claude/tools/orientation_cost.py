#!/usr/bin/env python3
"""Orientation-cost instrument (documentation_standard.md §4 — state vs history).

For each session id prefix given on the command line, read its transcript and report:
  - base context at the first tool call (system prompt + CLAUDE.md + memory + skill expansion)
  - ORIENTATION = every main-chain tool call before the FIRST mutating call: calls, tokens returned,
    minutes, tokens added to context, files read (Read tool, or Bash cat/sed -n/head/grep)
  - compaction events, and re-reads of the orientation set across the whole session
Usage:  python3 .claude/tools/orientation_cost.py <id8> [<id8> …]   (the 8-char session-id prefixes)
Baselines: record them in the workspace's daily log on the day they are measured.
Transcript shape: _practices/claude-code.md → Transcripts."""
import os, sys
import json, re, collections, datetime as dt
from pathlib import Path

WS_ROOT = os.environ.get('CLAUDE_PROJECT_DIR') or str(Path(__file__).resolve().parents[2])
ROOT = Path.home() / '.claude' / 'projects' / re.sub(r'[^A-Za-z0-9]', '-', WS_ROOT)
WS = WS_ROOT.rstrip('/') + '/'
TOP = '|'.join(re.escape(d) for d in sorted(os.listdir(WS_ROOT)) if os.path.isdir(os.path.join(WS_ROOT, d)) and not d.startswith('.'))
SESSIONS = [(a, a) for a in sys.argv[1:]]
if not SESSIONS:
    sys.exit(__doc__)
MUT_TOOLS = {'Edit', 'Write', 'MultiEdit', 'NotebookEdit'}
READ_CMD = re.compile(r'^\s*(cat|head|tail|sed -n|grep|rg|ls|find|wc|git (log|status|diff|show|branch)|tree|awk)\b')

def strip_redirs(cmd):
    return re.sub(r'\d?>\s*&\d|\d?>\s*/dev/null|2>&1', '', cmd)

def bash_is_write(cmd):
    c = strip_redirs(cmd or '')
    if re.search(r'\b(git (commit|push|mv|rm|checkout -b|merge|stash|reset|add)|mv|cp|rm|mkdir|tee|touch|chmod|railway up|vercel (env|deploy|--prod)|npm run (build|deploy)|npx (supabase|vercel)|sed -i|python3? [^|;]*\.py|node [^|;]*\.(m?js|ts))\b', c):
        # a python/node script may be a probe; still counts as "doing", not orienting
        return True
    if re.search(r'(?<![<\w])>\s*[\w./~$"\']', c):  # a real `> path`
        return True
    if re.search(r'curl\s+(-s\s+)?-X\s*(POST|PUT|PATCH|DELETE)', c, re.I):
        return True
    return False

def paths_in(cmd):
    return [p for p in re.findall(rf'({re.escape(WS)}[^\s;"\'`]+|(?<![\w/])(?:{TOP})/[^\s;"\'`]+)', cmd or '') if not p.endswith(('/', '*'))]

def load(sid8):
    f = next(ROOT.glob(f'{sid8}*.jsonl'))
    recs = []
    for line in f.open():
        line = line.strip()
        if line:
            try: recs.append(json.loads(line))
            except Exception: pass
    return f, recs

def mins(a, b):
    fa = dt.datetime.fromisoformat(a.replace('Z', '+00:00')); fb = dt.datetime.fromisoformat(b.replace('Z', '+00:00'))
    return (fb - fa).total_seconds() / 60

ORIENT_SET = ('project_log.md', '_prd.md', 'north_star.md', 'CONTEXT.md', 'system_contracts.md', 'memory/project_', 'testing.md', 'SKILL.md')

for sid, label in SESSIONS:
    path, recs = load(sid)
    main = [r for r in recs if not r.get('isSidechain')]
    tool_uses, results = [], {}
    compactions = 0; first_ts = None
    for r in main:
        ts = r.get('timestamp'); first_ts = first_ts or ts
        if r.get('type') == 'attachment':
            a = r.get('attachment') or {}
            if a.get('hookName', '').startswith('SessionStart:compact') or 'compact' in json.dumps(a)[:400].lower():
                compactions += 1
        if r.get('type') == 'user':
            c = r.get('message', {}).get('content')
            if isinstance(c, list):
                for x in c:
                    if isinstance(x, dict) and x.get('type') == 'tool_result':
                        b = x.get('content')
                        n = sum(len(i.get('text', '')) for i in b if isinstance(i, dict)) if isinstance(b, list) else len(str(b or ''))
                        results[x.get('tool_use_id')] = n
        elif r.get('type') == 'assistant':
            m = r.get('message', {}); u = m.get('usage') or {}
            ctx = u.get('input_tokens', 0) + u.get('cache_creation_input_tokens', 0) + u.get('cache_read_input_tokens', 0)
            for x in (m.get('content') or []):
                if isinstance(x, dict) and x.get('type') == 'tool_use':
                    tool_uses.append({'id': x.get('id'), 'ts': ts, 'name': x.get('name'), 'input': x.get('input') or {}, 'ctx': ctx})
    # classify
    first_mut = None
    for i, t in enumerate(tool_uses):
        n, inp = t['name'], t['input']
        mut = n in MUT_TOOLS or (n == 'Bash' and bash_is_write(inp.get('command', ''))) \
            or (n.startswith('mcp__supabase') and (n.endswith('apply_migration') or (n.endswith('execute_sql') and re.search(r'\b(insert|update|delete|create|alter|drop|grant|revoke|refresh)\b', inp.get('query', ''), re.I)))) \
            or (n.startswith('mcp__todoist__') and re.search(r'(add|update|complete|delete|reschedule|move)', n))
        if mut:
            first_mut = i; break
    orient = tool_uses[:first_mut] if first_mut is not None else tool_uses
    o_chars = sum(results.get(t['id'], 0) for t in orient)
    o_files = collections.Counter()
    for t in orient:
        if t['name'] == 'Read': o_files[t['input'].get('file_path', '?')] += 1
        elif t['name'] == 'Bash' and READ_CMD.match(t['input'].get('command', '') or ''):
            for p in paths_in(t['input'].get('command', '')): o_files[p] += 1
    o_agents = sum(1 for t in orient if t['name'] == 'Agent')
    o_min = mins(first_ts, tool_uses[first_mut]['ts']) if first_mut is not None else None
    ctx0 = tool_uses[0]['ctx'] if tool_uses else 0
    ctx_fm = tool_uses[first_mut]['ctx'] if first_mut is not None else None
    # whole-session re-reads of the orientation set
    rereads = collections.Counter()
    for t in tool_uses:
        ps = [t['input'].get('file_path', '')] if t['name'] == 'Read' else (paths_in(t['input'].get('command', '')) if t['name'] == 'Bash' and READ_CMD.match(t['input'].get('command', '') or '') else [])
        for p in ps:
            if any(k in p for k in ORIENT_SET): rereads[p.replace(WS, '')] += 1
    print(f"\n### {label} ({sid}) — {len(tool_uses)} tool calls")
    print(f"  base context at first tool call: {ctx0:,} tokens (system prompt + CLAUDE.md + memory + skill expansion)")
    print(f"  ORIENTATION before first mutating call #{first_mut}: {len(orient)} calls · {o_agents} subagents · {o_chars:,} chars returned (~{o_chars//4:,} tokens) · {o_min and round(o_min,1)} min")
    print(f"  context at first mutating call: {ctx_fm:,} → orientation added ~{(ctx_fm or 0) - ctx0:,} tokens to context")
    if first_mut is not None:
        t = tool_uses[first_mut]; print(f"  first mutating call: {t['name']} {str(t['input'])[:150]!r}")
    print(f"  files read while orienting:")
    for f, n in o_files.most_common(20): print(f"    {n}× {f.replace(WS, '')}")
    print(f"  compaction events in session: {compactions}")
    print(f"  re-reads of the orientation set across the WHOLE session:")
    for f, n in rereads.most_common(12): print(f"    {n}× {f}")
