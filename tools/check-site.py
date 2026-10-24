#!/usr/bin/env python3
"""Sanity-check the site before publishing. Python 3 standard library only.

    python3 tools/check-site.py

Checks:
  - every local href/src/data-img resolves (files, folders, #fragments)
  - every data-img points at assets/<CODE>/preview-1.jpg inside an existing assets/<CODE>/ folder
  - every data-price / data-buy key exists in js/site-config.js
  - no secret-looking strings anywhere in the repo
Also lists external links (not fetched) and anything still marked DRAFT / TODO.
Exit code 1 if any hard error is found.
"""
import re, sys, pathlib
from html.parser import HTMLParser
from urllib.parse import urlsplit, unquote

ROOT = pathlib.Path(__file__).resolve().parent.parent
SKIP_DIRS = {".git", "template", "tools"}
SECRET_RE = re.compile(r"((api[_-]?key|secret|passwd|password|token|private[_-]?key)\w*\s*[:=]\s*[\"'][^\"']{8,}[\"']|BEGIN [A-Z ]*PRIVATE KEY|AKIA[0-9A-Z]{12,}|ghp_[A-Za-z0-9]{20,}|sk_(live|test)_\w{8,}|xox[abp]-[\w-]{10,}|Bearer\s+[A-Za-z0-9._-]{20,})", re.I)


class Page(HTMLParser):
    def __init__(self):
        super().__init__()
        self.refs, self.ids, self.slots, self.keys = [], set(), [], []

    def handle_starttag(self, tag, attrs):
        a = dict(attrs)
        if "id" in a: self.ids.add(a["id"])
        if tag == "a" and "name" in a: self.ids.add(a["name"])
        for k in ("href", "src"):
            if k in a and a[k] is not None: self.refs.append((tag, a[k]))
        if "data-img" in a: self.slots.append(a["data-img"])
        for k in ("data-price", "data-buy"):
            if k in a: self.keys.append(a[k])


def html_files():
    for p in sorted(ROOT.rglob("*.html")):
        if not (set(p.relative_to(ROOT).parts) & SKIP_DIRS):
            yield p


def main():
    errors, external, notes = [], set(), []
    config = (ROOT / "js/site-config.js").read_text(encoding="utf-8")
    config_keys = set(re.findall(r'"([A-Z0-9-]+)":\s*\{\s*price', config))
    pages = {}
    for f in html_files():
        pg = Page(); pg.feed(f.read_text(encoding="utf-8")); pages[f] = pg

    for f, pg in pages.items():
        rel = f.relative_to(ROOT)
        for tag, ref in pg.refs:
            u = urlsplit(ref)
            if u.scheme in ("http", "https"): external.add(ref); continue
            if u.scheme in ("mailto", "data", "tel"): continue
            target = f if not u.path else (f.parent / unquote(u.path)).resolve()
            if target.is_dir(): target = target / "index.html"
            if not target.exists(): errors.append(f"{rel}: broken link {ref}"); continue
            if u.fragment and target.suffix == ".html":
                ids = pages[target].ids if target in pages else set()
                if u.fragment not in ids: errors.append(f"{rel}: missing anchor #{u.fragment} in {ref}")
        for s in pg.slots:
            m = re.fullmatch(r"(?:\.\./)*assets/([A-Za-z0-9_-]+)/preview-1\.jpg", s)
            if not m: errors.append(f"{rel}: bad image slot path {s}")
            elif not (ROOT / "assets" / m.group(1)).is_dir(): errors.append(f"{rel}: no folder assets/{m.group(1)}/")
        for k in pg.keys:
            if k not in config_keys: errors.append(f"{rel}: '{k}' not in js/site-config.js")

    for p in ROOT.rglob("*"):
        if p.is_file() and not (set(p.relative_to(ROOT).parts) & {".git"}) and p.suffix not in (".woff2", ".jpg", ".png"):
            if p.name == "check-site.py": continue
            for n, line in enumerate(p.read_text(encoding="utf-8", errors="ignore").splitlines(), 1):
                if SECRET_RE.search(line): errors.append(f"{p.relative_to(ROOT)}:{n}: secret-looking text: {line.strip()[:80]}")

    drafts = sum(f.read_text(encoding="utf-8").count("DRAFT") + f.read_text(encoding="utf-8").count("draft-tag") for f in pages)
    pending = [k for k in re.findall(r'(\w+):\s*"",', config)] + re.findall(r'"([A-Z0-9-]+)":\s*\{[^}]*etsy:\s*""', config)
    print(f"{len(pages)} pages checked, {len(config_keys)} listings in site-config.js")
    print(f"External links (not fetched): {len(external)}" + "".join(f"\n  {u}" for u in sorted(external)))
    print(f"Draft markers remaining: {drafts}   Empty URLs in site-config.js: {', '.join(pending) or 'none'}")
    for e in errors: print("ERROR", e)
    print("FAILED" if errors else "OK: no broken links, no secrets found")
    sys.exit(1 if errors else 0)


main()
