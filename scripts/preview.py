#!/usr/bin/env python3
"""Render README.md the way GitHub will, locally, before committing.

    GITHUB_TOKEN=$(gh auth token) python3 scripts/preview.py
    python3 -m http.server 8765      # then open /preview.html

Writes preview.html (gitignored) plus a preview-frozen/ directory. Three
things make this more than "open the markdown in a viewer", and each one cost
a wrong answer first:

  * Mode matters. POST /markdown with mode="gfm" is the *comment* renderer:
    it turns every newline into a hard break, so a paragraph hard-wrapped with
    explicit <br> comes out double-spaced. README files are rendered with
    mode="markdown", which is what this uses. The API is still the right test
    either way, because it applies the same sanitiser as the site — anything
    stripped here is stripped on your profile.

  * Screenshots restart SMIL. Every graphic reveals itself from width 0 or
    opacity 0, so a screenshot of the live file captures t=0 and shows a blank
    box. freeze() resolves each animation to the state it freezes at.

  * An <img>-loaded SVG follows the OS colour scheme, not the page it sits in,
    so a two-pane light/dark preview cannot work by styling the panes alone.
    pin_theme() bakes one scheme into each copy.
"""
import json
import os
import re
import subprocess
import sys
import urllib.request

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
OUT_DIR = os.path.join(ROOT, "preview-frozen")
GRAPHICS = ("stats", "streak", "langs", "year",
            "hd-about", "hd-stack", "hd-projects", "hd-stats")


def freeze(svg):
    """Resolve every SMIL animation to its final, frozen state."""
    # cursor blocks animate x and end hidden — they contribute nothing at rest
    svg = re.sub(r'<rect[^>]*opacity="0"\s*>\s*<animate attributeName="x"'
                 r'.*?</rect>', '', svg, flags=re.S)
    # clipPath wipes: width goes 0 -> W and freezes
    svg = re.sub(r'(<rect[^>]*?)width="0"(>)\s*<animate attributeName="width" '
                 r'from="0" to="([\d.]+)"[^>]*/>(\s*</rect>)',
                 lambda m: f'{m.group(1)}width="{m.group(3)}"'
                           f'{m.group(2)}{m.group(4)}', svg)
    # fades: opacity goes 0 -> 1 and freezes
    svg = re.sub(r'opacity="0"(>)(\s*)<animate attributeName="opacity" '
                 r'from="0" to="1"[^>]*/>',
                 lambda m: f'opacity="1"{m.group(1)}{m.group(2)}', svg)
    svg = re.sub(r'<animate\b[^>]*/>', '', svg)
    return re.sub(r'<set\b[^>]*/>', '', svg)


MEDIA = r'@media\(prefers-color-scheme:dark\)\{(.*)\}(?=</style>)'


def pin_theme(svg, want):
    if want == "light":                    # drop the dark override
        return re.sub(MEDIA, '', svg, flags=re.S)
    # unwrap it, so the dark rules always win over the light ones above
    return re.sub(MEDIA, lambda m: m.group(1), svg, flags=re.S)


def render(md, token):
    req = urllib.request.Request(
        "https://api.github.com/markdown",
        data=json.dumps({"text": md, "mode": "markdown"}).encode(),
        headers={"Authorization": f"bearer {token}",
                 "Accept": "application/vnd.github+json",
                 "User-Agent": "profile-preview"})
    with urllib.request.urlopen(req, timeout=30) as r:
        return r.read().decode()


CSS = """
body{margin:0;background:#fff;color:#1f2328;font:16px/1.5 -apple-system,
 BlinkMacSystemFont,"Segoe UI",Helvetica,Arial,sans-serif}
.wrap{max-width:1012px;margin:0 auto;padding:24px}
.pane{border:1px solid #d1d9e0;border-radius:6px;padding:32px 40px;
 margin-bottom:32px}
.lbl{font:600 11px ui-monospace,monospace;letter-spacing:1.5px;
 text-transform:uppercase;color:#59636e;margin:0 0 24px}
img{max-width:100%}
samp{font:12px ui-monospace,SFMono-Regular,Menlo,monospace}
blockquote{margin:0 0 16px;padding:0 1em;color:#59636e;
 border-left:.25em solid #d1d9e0}
p{margin:0 0 16px}
a{color:#0969da;text-decoration:none}
code{background:#eff1f3;padding:.2em .4em;border-radius:6px;
 font:12px ui-monospace,monospace}
sub{font-size:12px;color:#59636e}
.dark{background:#0d1117;color:#f0f6fc;border-color:#3d444d}
.dark .lbl,.dark sub{color:#9198a1}
.dark blockquote{color:#9198a1;border-left-color:#3d444d}
.dark a{color:#4493f8}
.dark code{background:#151b23}
"""


def main():
    token = os.environ.get("GITHUB_TOKEN")
    if not token:
        token = subprocess.run(["gh", "auth", "token"], capture_output=True,
                               text=True).stdout.strip()
    if not token:
        sys.exit("GITHUB_TOKEN is not set and `gh auth token` returned nothing")

    os.makedirs(OUT_DIR, exist_ok=True)
    missing = []
    for name in GRAPHICS:
        src_path = os.path.join(ROOT, f"{name}.svg")
        if not os.path.exists(src_path):
            missing.append(f"{name}.svg")
            continue
        with open(src_path, encoding="utf-8") as f:
            src = f.read()
        for want in ("light", "dark"):
            svg = pin_theme(freeze(src), want)
            with open(os.path.join(OUT_DIR, f"{name}.{want}.svg"), "w",
                      encoding="utf-8") as f:
                f.write(svg)

    with open(os.path.join(ROOT, "README.md"), encoding="utf-8") as f:
        body = render(f.read(), token)

    def pane(theme):
        return re.sub(r'src="\./([a-z-]+)\.svg"',
                      rf'src="./preview-frozen/\1.{theme}.svg"', body)

    html = (f'<!doctype html><meta charset="utf-8"><title>README preview</title>'
            f'<style>{CSS}</style><div class="wrap">'
            f'<div class="pane"><p class="lbl">GitHub &mdash; light</p>'
            f'{pane("light")}</div>'
            f'<div class="pane dark"><p class="lbl">GitHub &mdash; dark</p>'
            f'{pane("dark")}</div></div>')
    with open(os.path.join(ROOT, "preview.html"), "w", encoding="utf-8") as f:
        f.write(html)

    kept = {tag: len(re.findall(rf'<{tag}[ >]', body))
            for tag in ("img", "samp", "sub", "blockquote", "br")}
    print("survived the sanitiser: "
          + ", ".join(f"{k} {v}" for k, v in kept.items()))
    if missing:
        print("missing (not drawn yet): " + ", ".join(missing))
    print("wrote preview.html — serve the repo and open /preview.html")


if __name__ == "__main__":
    main()
