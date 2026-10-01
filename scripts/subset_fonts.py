#!/usr/bin/env python3
"""One-time helper: subset the two typefaces used by every SVG in this repo.

You do not need this in CI. The subset .woff files are committed in
assets/fonts/, and the SVG builders embed them as base64 so every image renders
identically everywhere (GitHub serves SVGs as images, and images cannot load
web fonts from the network).

Typefaces
  TeX Gyre Adventor  (GUST Font License)          display: names, titles
  DejaVu Sans Mono   (Bitstream Vera / DejaVu)    everything technical

Requires: pip install fonttools
"""
from pathlib import Path

from fontTools import subset

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "assets" / "fonts"

GYRE = "/usr/share/texmf/fonts/opentype/public/tex-gyre"
DEJAVU = "/usr/share/fonts/truetype/dejavu"
SOURCES = {
    "display-bold.woff": f"{GYRE}/texgyreadventor-bold.otf",
    "display-regular.woff": f"{GYRE}/texgyreadventor-regular.otf",
    "display-italic.woff": f"{GYRE}/texgyreadventor-italic.otf",
    "mono.woff": f"{DEJAVU}/DejaVuSansMono.ttf",
    "mono-bold.woff": f"{DEJAVU}/DejaVuSansMono-Bold.ttf",
}

# printable ASCII plus the handful of symbols the designs use
TEXT = "".join(chr(c) for c in range(0x20, 0x7F)) + "×→←↓↑·—–“”‘’…█├└│─✓"


def main() -> None:
    OUT.mkdir(parents=True, exist_ok=True)
    for name, src in SOURCES.items():
        opts = subset.Options()
        opts.flavor = "woff"
        opts.layout_features = ["kern", "liga"]
        opts.notdef_outline = True
        font = subset.load_font(src, opts)
        sub = subset.Subsetter(opts)
        sub.populate(text=TEXT)
        sub.subset(font)
        subset.save_font(font, str(OUT / name), opts)
        print(f"{name:22s} {(OUT / name).stat().st_size / 1024:5.1f} KB")


if __name__ == "__main__":
    main()
