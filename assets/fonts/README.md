# fonts

Subsets of two freely licensed typefaces, embedded as base64 inside every SVG in
`assets/` so the images render the same in every browser (SVGs shown through an
`<img>` tag cannot fetch web fonts).

| file | typeface | license |
| :-- | :-- | :-- |
| `display-*.woff` | TeX Gyre Adventor | GUST Font License, see `LICENSE-TeX-Gyre-Adventor.txt` |
| `mono*.woff` | DejaVu Sans Mono | Bitstream Vera / DejaVu license, see `LICENSE-DejaVu-Sans-Mono.txt` |

Regenerate with `python scripts/subset_fonts.py` (needs `fonttools`).
