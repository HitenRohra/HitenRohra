# fonts

[JetBrains Mono](https://github.com/JetBrains/JetBrainsMono) v2.304, SIL OFL 1.1.
The licence travels with the files — see `OFL.txt`. Only an OFL-or-similar face
can be used here, because the font ships inside a public repository.

Each graphic inlines its own subset as a base64 data URI. An external font URL
cannot work: these SVGs load through an `<img>` tag, and browsers refuse
subresource fetches for image documents. That means every file carries its own
copy, so the subsets are cut per role rather than shipped whole — the full TTFs
would be roughly 4.5 MB across the page instead of ~12 KB.

| file | weight | covers | size |
|------|--------|--------|------|
| `jbmono-ramp.woff2` | 400 | the 13 ramp characters, for the portrait | 1.3 KB |
| `jbmono-head.woff2` | 600 | only the letters the section headings use | 1.3 KB |
| `jbmono-400.woff2` | 400 | basic latin + en/em dash, for the data graphics | 4.5 KB |
| `jbmono-600.woff2` | 600 | basic latin + en/em dash, for the data graphics | 4.5 KB |

JetBrains Mono is 600/1000 units — an advance width of exactly 0.600 em, which
is what `make_portrait.py`'s character grid assumes (`CHAR_W / FONT_SIZE`).
That is not only a typographic preference. A viewer whose default monospace is
narrower (Consolas is ≈0.55) would see the portrait about 7% too narrow, so
inlining the face pins the geometry for everyone.

## Regenerating

Needed only when a heading gains a letter the `head` subset does not cover, or
when the portrait's ramp changes.

```bash
pip install fonttools brotli
TTF=path/to/JetBrainsMono/fonts/ttf

# the 13 ramp characters — keep in step with RAMP in make_portrait.py
printf ' .`:-=+*cs#%%@' > /tmp/ramp.txt
pyftsubset "$TTF/JetBrainsMono-Regular.ttf" --text-file=/tmp/ramp.txt \
  --flavor=woff2 --layout-features='' --no-hinting \
  --output-file=jbmono-ramp.woff2

# only the letters HEADINGS in generate_stats.py actually draws
printf ' abcehjklnoprstu' > /tmp/head.txt
pyftsubset "$TTF/JetBrainsMono-SemiBold.ttf" --text-file=/tmp/head.txt \
  --flavor=woff2 --layout-features='' --no-hinting \
  --output-file=jbmono-head.woff2

# both weights for the data graphics
pyftsubset "$TTF/JetBrainsMono-Regular.ttf" --unicodes='U+0020-007E,U+2013,U+2014' \
  --flavor=woff2 --layout-features='' --no-hinting \
  --output-file=jbmono-400.woff2
pyftsubset "$TTF/JetBrainsMono-SemiBold.ttf" --unicodes='U+0020-007E,U+2013,U+2014' \
  --flavor=woff2 --layout-features='' --no-hinting \
  --output-file=jbmono-600.woff2
```
