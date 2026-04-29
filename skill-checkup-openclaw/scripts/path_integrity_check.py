#!/usr/bin/env python3
"""Skill/script path integrity scanner for OpenClaw workspaces.

Read-only. Outputs a compact Markdown report for agents to use during Skill Checkup.
"""
from __future__ import annotations
import argparse, os, re
from pathlib import Path

REF_RE = re.compile(r"(?P<ref>(?:\.\.?/[A-Za-z0-9_./@+\-]*[A-Za-z0-9_@+\-][A-Za-z0-9_./@+\-]*|~/[A-Za-z0-9_./@+\-]*[A-Za-z0-9_@+\-][A-Za-z0-9_./@+\-]*|/(?:root|home)/[A-Za-z0-9_./@+\-]*[A-Za-z0-9_@+\-][A-Za-z0-9_./@+\-]*|scripts/[A-Za-z0-9_./@+\-]*[A-Za-z0-9_@+\-][A-Za-z0-9_./@+\-]*)(?:\.(?:sh|py|js|mjs|ts|json|md|txt|yaml|yml))?)")
MD_LINK_RE = re.compile(r"\[[^\]]+\]\((?P<link>[^)#]+)(?:#[^)]+)?\)")


def is_hidden_or_vendor(path: Path) -> bool:
    parts = set(path.parts)
    return any(p in parts for p in {'.git', 'node_modules', '.venv', 'venv', '__pycache__'})


def parse_name(skill: Path) -> str:
    try:
        for line in skill.read_text(errors='ignore').splitlines()[:40]:
            if line.startswith('name:'):
                return line.split(':', 1)[1].strip().strip('"\'') or skill.parent.name
    except Exception:
        pass
    return skill.parent.name


def find_skill_files(root: Path):
    names = {'SKILL.md', 'SKILL.fixture.md'}
    return sorted(p for p in root.rglob('*') if p.is_file() and p.name in names and not is_hidden_or_vendor(p))


def find_skill_roots(root: Path, skill_files):
    roots = set()
    for p in skill_files:
        # nearest skills ancestor, if any
        for anc in p.parents:
            if anc.name == 'skills' or anc == root:
                roots.add(anc)
                break
    return sorted(roots)


def workspace_for_skill_root(root: Path, skill_root: Path) -> Path:
    return skill_root.parent if skill_root.name == 'skills' else root


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument('root', nargs='?', default='.', help='workspace root to scan')
    ap.add_argument('--max-findings', type=int, default=80)
    args = ap.parse_args()

    root = Path(args.root).expanduser().resolve()
    skill_files = find_skill_files(root)
    skill_roots = find_skill_roots(root, skill_files)

    by_name: dict[str, list[Path]] = {}
    for p in skill_files:
        by_name.setdefault(parse_name(p), []).append(p)

    broken_symlinks = []
    for p in root.rglob('*'):
        if is_hidden_or_vendor(p):
            continue
        try:
            if p.is_symlink() and not p.exists():
                broken_symlinks.append(p)
        except OSError:
            pass

    refs = []
    for skill in skill_files:
        text = skill.read_text(errors='ignore')
        skill_dir = skill.parent
        for m in REF_RE.finditer(text):
            ref = m.group('ref').rstrip('.,);`"\'')
            # Skip generic examples and OpenClaw runtime dirs documented as patterns, not skill dependencies.
            if ref in {'/root', '/root/', '/home', '/home/', '~/.openclaw', '~/.openclaw/', './.git', './.git/'}:
                continue
            if ref.startswith('~/.openclaw/') and ref.split('~/.openclaw/', 1)[1] in {'media', 'logs', 'agents'}:
                continue
            if ref.startswith('http'):
                continue
            if ref.startswith('~/'):
                resolved = Path.home() / ref[2:]
                kind = 'home'
            elif ref.startswith('/root/') or ref.startswith('/home/'):
                resolved = Path(ref)
                kind = 'absolute'
            elif ref.startswith('./') or ref.startswith('../'):
                resolved = (skill_dir / ref).resolve()
                kind = 'relative'
            else:  # scripts/ or similar, skill-relative first
                resolved = (skill_dir / ref).resolve()
                kind = 'skill-relative-candidate'
            exists = resolved.exists()
            cross = False
            try:
                cross = exists and root not in [resolved, *resolved.parents]
            except Exception:
                cross = False
            if kind in {'absolute', 'home'} or not exists or cross or '..' in Path(ref).parts:
                refs.append((skill, ref, kind, exists, resolved))

    registry_missing = []
    for reg in list(root.rglob('_registry.md')) + list(root.rglob('README.md')):
        if is_hidden_or_vendor(reg):
            continue
        text = reg.read_text(errors='ignore')
        for m in MD_LINK_RE.finditer(text):
            link = m.group('link').strip()
            if '://' in link or link.startswith('#') or link.startswith('mailto:'):
                continue
            if not (link.endswith('.md') or '/SKILL.md' in link):
                continue
            target = (reg.parent / link).resolve()
            if not target.exists():
                registry_missing.append((reg, link, target))

    print('# Skill Path Integrity Scan')
    print()
    print(f'Root: `{root}`')
    print(f'Skill roots: {len(skill_roots)}')
    for sr in skill_roots[:20]:
        print(f'- `{sr.relative_to(root) if root in [sr, *sr.parents] else sr}` → workspace `{workspace_for_skill_root(root, sr)}`')
    if len(skill_roots) > 20:
        print(f'- ... {len(skill_roots)-20} more')
    print(f'Skills found: {len(skill_files)}')
    print()

    dupes = {k:v for k,v in by_name.items() if len(v) > 1}
    print('## Potential issues')
    findings = 0
    if dupes:
        print('### Duplicate skill names')
        for name, files in sorted(dupes.items())[:args.max_findings]:
            findings += 1
            locs = ', '.join('`'+str(f.relative_to(root))+'`' if root in [f, *f.parents] else '`'+str(f)+'`' for f in files[:5])
            print(f'- `{name}` appears in {len(files)} places: {locs}')
    if broken_symlinks:
        print('### Broken symlinks')
        for p in broken_symlinks[:args.max_findings]:
            findings += 1
            print(f'- `{p.relative_to(root) if root in [p, *p.parents] else p}`')
    if refs:
        print('### Risky or unresolved references in SKILL.md')
        for skill, ref, kind, exists, resolved in refs[:args.max_findings]:
            findings += 1
            srel = skill.relative_to(root) if root in [skill, *skill.parents] else skill
            rdisp = resolved if root not in [resolved, *resolved.parents] else resolved.relative_to(root)
            status = 'exists' if exists else 'missing'
            print(f'- `{srel}` references `{ref}` ({kind}, {status}) → `{rdisp}`')
    if registry_missing:
        print('### Missing registry/README links')
        for reg, link, target in registry_missing[:args.max_findings]:
            findings += 1
            rrel = reg.relative_to(root) if root in [reg, *reg.parents] else reg
            print(f'- `{rrel}` links to missing `{link}`')
    if findings == 0:
        print('- No obvious path integrity issues found by this scanner.')
    print()
    print('## Interpretation')
    print('- Treat this as evidence for the audit, not as the final report.')
    print('- In multi-agent setups, review duplicates and cross-workspace references manually before changing anything.')
    return 0

if __name__ == '__main__':
    raise SystemExit(main())
