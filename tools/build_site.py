#!/usr/bin/env python3
"""Build the GitHub Pages site from the project's 3D viewer.

The viewer (house3d.html) embeds the house model as a base64 string. For the
web we pull that model out into site/binyam_house.glb and have index.html load
it with a relative URL, so the page is small, the model is cached by the
browser, and everything works under https://<user>.github.io/<repo>/.

Usage:  python3 tools/build_site.py path/to/house3d.html
"""
import base64, re, sys
from pathlib import Path

src = Path(sys.argv[1] if len(sys.argv) > 1 else "house3d.html")
out = Path(__file__).resolve().parent.parent / "site"
out.mkdir(exist_ok=True)

html = src.read_text(encoding="utf-8")
m = re.search(r'const B64="([^"]+)";\n?', html)
if not m:
    sys.exit("No embedded model (const B64=...) found in " + str(src))
glb = base64.b64decode(m.group(1))
(out / "binyam_house.glb").write_bytes(glb)
html = html[:m.start()] + html[m.end():]

old = "const bin=Uint8Array.from(atob(B64),c=>c.charCodeAt(0)).buffer;"
new = "const bin=await (await fetch('./binyam_house.glb')).arrayBuffer();"
if old not in html:
    sys.exit("Model decode line not found; the viewer changed, update this script.")
html = html.replace(old, new)

# Claude-only meta tag is meaningless on the web.
html = html.replace('<meta name="claude:viewport-fit-sides" content="cover">\n', "")
if not html.lstrip().lower().startswith("<!doctype"):
    html = ('<!doctype html>\n<html lang="en">\n<head>\n<meta charset="utf-8">\n'
            '<meta name="viewport" content="width=device-width, initial-scale=1, viewport-fit=cover">\n'
            + html + "\n</html>\n")
(out / "index.html").write_text(html, encoding="utf-8")
(out / ".nojekyll").write_text("")

mb = len(glb) / 1e6
print(f"site/index.html {len(html)/1e3:.0f} KB, site/binyam_house.glb {mb:.1f} MB")
if mb > 100:
    print("WARNING: model is over GitHub's 100 MB file limit; compress it (Draco/meshopt).")
