"""Design tokens shared by every generated SVG.

The one idea behind the palette: colour encodes depth. Anything near the
surface of a stack (a model, a parser, the top of a call) is cyan; the deeper
you go the more violet it gets; the bottom (silicon, disk, recovery) is amber,
like heat near a core. Every diagram in the profile uses the same scale, so the
colour of a thing tells you how far down it sits.
"""
from __future__ import annotations

import base64
from functools import lru_cache
from pathlib import Path
from xml.sax.saxutils import escape

ROOT = Path(__file__).resolve().parents[1]
FONT_DIR = ROOT / "assets" / "fonts"

PALETTES = {
    "dark": {
        "bg": "#0d1117",        # GitHub's own dark canvas, so the art bleeds into the page
        "surface": "#121923",
        "side_l": "#0f151e",
        "side_r": "#151d28",
        "line": "#263040",
        "line_soft": "#1a222e",
        "text": "#e6edf3",
        "muted": "#8b949e",
        "faint": "#5d6774",
        "depth": ["#67e8f9", "#a78bfa", "#f5b45c"],   # surface → middle → core
    },
    "light": {
        "bg": "#ffffff",
        "surface": "#f6f8fa",
        "side_l": "#e7ebf0",
        "side_r": "#eef1f5",
        "line": "#d0d7de",
        "line_soft": "#e4e8ed",
        "text": "#1f2328",
        "muted": "#59636e",
        "faint": "#8c959f",
        "depth": ["#0e7490", "#6d28d9", "#b45309"],
    },
}

# DejaVu Sans Mono advance width (1233 / 2048 em); exact, because the font is embedded
MONO_ADVANCE = 1233 / 2048

DISPLAY = "'Skandh Display','TeX Gyre Adventor','Avenir Next','Century Gothic',sans-serif"
MONO = "'Skandh Mono','DejaVu Sans Mono',ui-monospace,Menlo,Consolas,monospace"

_FACES = {
    "display-bold": ("Skandh Display", "display-bold.woff", 700, "normal"),
    "display-regular": ("Skandh Display", "display-regular.woff", 400, "normal"),
    "display-italic": ("Skandh Display", "display-italic.woff", 400, "italic"),
    "mono": ("Skandh Mono", "mono.woff", 400, "normal"),
    "mono-bold": ("Skandh Mono", "mono-bold.woff", 700, "normal"),
}


@lru_cache(maxsize=None)
def _font_b64(filename: str) -> str:
    return base64.b64encode((FONT_DIR / filename).read_bytes()).decode("ascii")


def font_faces(*keys: str) -> str:
    """@font-face rules with the fonts inlined as data URIs."""
    rules = []
    for key in keys:
        family, filename, weight, style = _FACES[key]
        rules.append(
            f"@font-face{{font-family:'{family}';font-weight:{weight};font-style:{style};"
            f"src:url(data:font/woff;base64,{_font_b64(filename)}) format('woff');}}"
        )
    return "".join(rules)


REDUCED_MOTION = "@media (prefers-reduced-motion: reduce){*{animation:none!important;}}"


def mono_width(text: str, size: float) -> float:
    return len(text) * size * MONO_ADVANCE


def _hex(c: str) -> tuple[int, int, int]:
    c = c.lstrip("#")
    return int(c[0:2], 16), int(c[2:4], 16), int(c[4:6], 16)


def mix(a: str, b: str, t: float) -> str:
    ra, ga, ba = _hex(a)
    rb, gb, bb = _hex(b)
    return "#{:02x}{:02x}{:02x}".format(
        round(ra + (rb - ra) * t), round(ga + (gb - ga) * t), round(ba + (bb - ba) * t)
    )


def depth(palette: dict, t: float) -> str:
    """Colour at depth t in [0, 1]: 0 is the surface, 1 is the core."""
    s0, s1, s2 = palette["depth"]
    t = max(0.0, min(1.0, t))
    return mix(s0, s1, t * 2) if t <= 0.5 else mix(s1, s2, (t - 0.5) * 2)


def esc(text: str) -> str:
    return escape(text, {'"': "&quot;"})


def pct(seconds: float, cycle: float) -> str:
    return f"{max(0.0, min(100.0, seconds / cycle * 100)):.2f}%"


def svg_open(width: int, height: int, label: str, css: str) -> str:
    return (
        '<?xml version="1.0" encoding="UTF-8"?>\n'
        f'<svg xmlns="http://www.w3.org/2000/svg" width="{width}" height="{height}" '
        f'viewBox="0 0 {width} {height}" role="img" aria-label="{esc(label)}">\n'
        f"<title>{esc(label)}</title>\n<style>{css}{REDUCED_MOTION}</style>\n"
    )
