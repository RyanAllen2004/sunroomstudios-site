#!/usr/bin/env python3
"""Write sitemap.xml and robots.txt once you know the public address. Standard library only.

    python3 tools/make-sitemap.py https://USERNAME.github.io/REPO
"""
import sys, pathlib
if len(sys.argv) != 2 or not sys.argv[1].startswith("http"):
    sys.exit("usage: python3 tools/make-sitemap.py https://your-public-address")
base = sys.argv[1].rstrip("/")
root = pathlib.Path(__file__).resolve().parent.parent
pages = sorted(p.relative_to(root).as_posix() for p in root.rglob("*.html")
               if not ({"template", "tools", ".git"} & set(p.relative_to(root).parts)))
urls = "".join(f"  <url><loc>{base}/{'' if p == 'index.html' else p}</loc></url>\n" for p in pages)
(root / "sitemap.xml").write_text('<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n' + urls + "</urlset>\n")
(root / "robots.txt").write_text(f"User-agent: *\nAllow: /\nSitemap: {base}/sitemap.xml\n")
print(f"wrote sitemap.xml ({len(pages)} pages) and robots.txt")
