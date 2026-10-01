#!/usr/bin/env python3
"""Build every static SVG in assets/ (both colour schemes where it matters).

    python scripts/build_assets.py

Pure standard library. Edit the copy or palette here, re-run, commit.
"""
from __future__ import annotations

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

from theme import (  # noqa: E402
    DISPLAY, MONO, MONO_ADVANCE, PALETTES, ROOT, depth, esc, font_faces, mono_width, pct, svg_open,
)
import update_profile  # noqa: E402

ASSETS = ROOT / "assets"
GENERATED = ASSETS / "generated"


# --------------------------------------------------------------------------- header
def header(theme: str) -> str:
    P = PALETTES[theme]
    W, H = 1200, 340
    cx, hw, hh, th, sp = 912, 124, 36, 10, 36          # stack centre, half-width, half-height, slab, pitch
    layers = ["model", "framework", "library", "runtime", "kernel", "silicon"]
    n = len(layers)
    cys = [64 + i * sp for i in range(n)]
    gx = cx - hw - 46                                   # depth gauge x
    lx = cx + hw + 40                                   # label x
    cycle, first, step = 7.6, 0.6, 0.9
    arrive = [first + i * step for i in range(n)]
    hold_end, fade_end = arrive[-1] + 1.5, arrive[-1] + 2.0
    span = cys[-1] - cys[0]

    css = [font_faces("display-bold", "display-italic", "mono")]
    css.append(
        f".name{{font:700 66px {DISPLAY};fill:{P['text']};letter-spacing:-1.5px}}"
        f".tag{{font:400 17px {MONO};fill:{P['muted']}}}"
        f".quote{{font:italic 400 21px {DISPLAY};fill:{P['text']}}}"
        f".desc{{font:400 15px {MONO};fill:{P['muted']}}}"
        f".lbl{{font:400 14.5px {MONO};fill:{P['muted']}}}"
        ".hl,.dot{opacity:0}"
        ".gauge{transform-box:fill-box;transform-origin:50% 0}"
    )

    # one highlight per layer, perfectly in step with the probe
    for i, a in enumerate(arrive):
        off = (hold_end, fade_end) if i == n - 1 else (a + 0.7, a + 1.3)
        css.append(
            f"@keyframes hl{i}{{0%,{pct(a - 0.25, cycle)}{{opacity:0}}{pct(a, cycle)},{pct(off[0], cycle)}{{opacity:1}}"
            f"{pct(off[1], cycle)},100%{{opacity:0}}}}"
            f".hl{i}{{animation:hl{i} {cycle}s ease-in-out infinite}}"
        )

    # probe: travels down the gauge, dwells at each layer
    frames = [f"0%{{opacity:0;transform:translateY(0px)}}",
              f"{pct(arrive[0] - 0.35, cycle)}{{opacity:0;transform:translateY(0px)}}"]
    gframes = ["0%{transform:scaleY(0);opacity:1}", f"{pct(arrive[0], cycle)}{{transform:scaleY(0);opacity:1}}"]
    for i, a in enumerate(arrive):
        y = cys[i] - cys[0]
        frames.append(f"{pct(a, cycle)},{pct(a + 0.45, cycle)}{{opacity:1;transform:translateY({y}px)}}")
        gframes.append(f"{pct(a, cycle)},{pct(a + 0.45, cycle)}{{transform:scaleY({y / span:.4f});opacity:1}}")
    frames += [f"{pct(hold_end, cycle)}{{opacity:1;transform:translateY({span}px)}}",
               f"{pct(fade_end, cycle)},100%{{opacity:0;transform:translateY({span}px)}}"]
    gframes += [f"{pct(hold_end, cycle)}{{transform:scaleY(1);opacity:1}}",
                f"{pct(fade_end, cycle)},100%{{transform:scaleY(1);opacity:0}}"]
    css.append("@keyframes probe{" + "".join(frames) + "}"
               f".dot{{animation:probe {cycle}s ease-in-out infinite}}")
    css.append("@keyframes gauge{" + "".join(gframes) + "}"
               f".gauge{{animation:gauge {cycle}s ease-in-out infinite}}")

    o = [svg_open(W, H, "Deepak Skandh. AI × Systems × Engineering. "
                        "Every abstraction is a promise. I read the fine print.", "".join(css))]
    d0, d1, d2 = P["depth"]
    glow_op = 0.13 if theme == "dark" else 0.07
    o.append(f"""<defs>
<clipPath id="card"><rect width="{W}" height="{H}" rx="20"/></clipPath>
<pattern id="grid" width="22" height="22" patternUnits="userSpaceOnUse"><circle cx="1.5" cy="1.5" r="1" fill="{P['faint']}"/></pattern>
<radialGradient id="fade" cx="{cx}" cy="{H / 2}" r="420" gradientUnits="userSpaceOnUse">
  <stop offset="0" stop-color="#fff" stop-opacity=".55"/><stop offset="1" stop-color="#fff" stop-opacity="0"/></radialGradient>
<mask id="gridmask"><rect width="{W}" height="{H}" fill="url(#fade)"/></mask>
<radialGradient id="glow" cx="{cx}" cy="{H / 2 + 20}" r="300" gradientUnits="userSpaceOnUse">
  <stop offset="0" stop-color="{d1}" stop-opacity="{glow_op}"/><stop offset="1" stop-color="{d1}" stop-opacity="0"/></radialGradient>
<linearGradient id="depthV" x1="0" y1="{cys[0]}" x2="0" y2="{cys[-1]}" gradientUnits="userSpaceOnUse">
  <stop offset="0" stop-color="{d0}"/><stop offset=".5" stop-color="{d1}"/><stop offset="1" stop-color="{d2}"/></linearGradient>
<linearGradient id="quoteBar" x1="0" y1="0" x2="0" y2="1">
  <stop offset="0" stop-color="{d0}"/><stop offset=".5" stop-color="{d1}"/><stop offset="1" stop-color="{d2}"/></linearGradient>
</defs>
<g clip-path="url(#card)">
<rect width="{W}" height="{H}" fill="{P['bg']}"/>
<rect width="{W}" height="{H}" fill="url(#grid)" mask="url(#gridmask)"/>
<rect width="{W}" height="{H}" fill="url(#glow)"/>
</g>
<rect x=".5" y=".5" width="{W - 1}" height="{H - 1}" rx="19.5" fill="none" stroke="{P['line']}"/>
""")

    # identity, left
    o.append(f'<text class="name" x="72" y="132">Deepak Skandh</text>\n')
    o.append(f'<text class="tag" x="74" y="174">AI<tspan fill="{d0}"> × </tspan>Systems'
             f'<tspan fill="{d1}"> × </tspan>Engineering</text>\n')
    o.append('<rect x="72" y="212" width="3" height="34" rx="1.5" fill="url(#quoteBar)"/>\n')
    o.append('<text class="quote" x="90" y="236">“Every abstraction is a promise. I read the fine print.”</text>\n')
    o.append('<text class="desc" x="74" y="282">building, breaking, and understanding things from the inside out.</text>\n')

    # depth gauge
    o.append(f'<rect x="{gx - 0.5}" y="{cys[0]}" width="1" height="{span}" fill="{P["line"]}"/>\n')
    o.append(f'<rect class="gauge" x="{gx - 1}" y="{cys[0]}" width="2" height="{span}" fill="url(#depthV)"/>\n')
    for cy in cys:
        o.append(f'<line x1="{gx - 5}" y1="{cy}" x2="{gx + 5}" y2="{cy}" stroke="{P["faint"]}"/>'
                 f'<line x1="{gx + 10}" y1="{cy}" x2="{cx - hw - 6}" y2="{cy}" stroke="{P["line"]}" stroke-dasharray="2 4"/>\n')

    # the stack, drawn bottom-up so upper layers sit on top
    for i in reversed(range(n)):
        cy, col = cys[i], depth(P, i / (n - 1))
        top = f"{cx - hw},{cy} {cx},{cy - hh} {cx + hw},{cy} {cx},{cy + hh}"
        left = f"{cx - hw},{cy} {cx},{cy + hh} {cx},{cy + hh + th} {cx - hw},{cy + th}"
        right = f"{cx},{cy + hh} {cx + hw},{cy} {cx + hw},{cy + th} {cx},{cy + hh + th}"
        o.append(f'<g><polygon points="{left}" fill="{P["side_l"]}" stroke="{P["line"]}" stroke-linejoin="round"/>'
                 f'<polygon points="{right}" fill="{P["side_r"]}" stroke="{P["line"]}" stroke-linejoin="round"/>'
                 f'<polygon points="{top}" fill="{P["surface"]}" stroke="{P["line"]}" stroke-linejoin="round"/>'
                 f'<g class="hl hl{i}"><polygon points="{top}" fill="{col}" fill-opacity=".16" stroke="{col}" stroke-width="1.6" stroke-linejoin="round"/>'
                 f'<polyline points="{cx - hw},{cy + th} {cx},{cy + hh + th} {cx + hw},{cy + th}" fill="none" stroke="{col}" stroke-opacity=".55"/></g></g>\n')

    # labels
    for i, name in enumerate(layers):
        cy, col = cys[i], depth(P, i / (n - 1))
        o.append(f'<line x1="{cx + hw + 8}" y1="{cy}" x2="{lx - 10}" y2="{cy}" stroke="{P["line"]}"/>'
                 f'<text class="lbl" x="{lx}" y="{cy + 5}">{name}</text>'
                 f'<g class="hl hl{i}"><line x1="{cx + hw + 8}" y1="{cy}" x2="{lx - 10}" y2="{cy}" stroke="{col}"/>'
                 f'<text class="lbl" x="{lx}" y="{cy + 5}" style="fill:{col}">{name}</text></g>\n')

    # probe
    o.append(f'<g class="dot"><circle cx="{gx}" cy="{cys[0]}" r="9" fill="{d1}" fill-opacity=".18"/>'
             f'<circle cx="{gx}" cy="{cys[0]}" r="4" fill="{P["text"]}"/></g>\n')
    o.append("</svg>\n")
    return "".join(o)


# --------------------------------------------------------------------------- terminal
def terminal() -> str:
    P = PALETTES["dark"]
    W, fs, lh = 760, 14, 24
    cw = fs * MONO_ADVANCE
    x0, y0 = 28, 72
    prompt_chars = len("deepak@skandh:~$ ")
    d0, d1, d2 = P["depth"]

    script = [
        ("cmd", "whoami"),
        ("out", "deepak skandh"),
        ("cmd", "cat ~/.focus"),
        ("out", "ai, systems, algorithms, first-principles engineering"),
        ("cmd", "./underneath --list"),
        ("map", "framework", "implementation"),
        ("map", "api", "protocol"),
        ("map", "database", "query engine"),
        ("map", "model", "architecture + optimization"),
        ("map", "library", "algorithm"),
        ("cmd", "echo $STATUS"),
        ("out", "still compiling."),
        ("end",),
    ]

    # timeline
    t, events = 0.5, []
    for item in script:
        kind = item[0]
        if kind == "cmd":
            t_type = t + 0.4
            t_done = t_type + len(item[1]) * 0.075
            events.append((kind, item, t, t_type, t_done))
            t = t_done + 0.35
        elif kind in ("out", "map"):
            events.append((kind, item, t, None, None))
            t += 0.09 if kind == "map" else 0.12
        else:
            events.append((kind, item, t + 0.45, None, None))
            t += 0.45
    cycle = t + 4.2
    H = y0 + (len(script) - 1) * lh + 30

    css = [font_faces("mono"),
           f".t{{font:400 {fs}px {MONO};fill:{P['text']};white-space:pre}}"
           f".m{{fill:{P['muted']}}}"
           f"@keyframes blink{{0%,50%{{opacity:1}}50.01%,100%{{opacity:0}}}}"
           f".blink{{animation:blink 1.1s infinite}}"
           f"@keyframes all{{0%,{pct(cycle - 0.8, cycle)}{{opacity:1}}{pct(cycle - 0.25, cycle)},100%{{opacity:0}}}}"
           f".all{{animation:all {cycle}s linear infinite}}"]

    body = []

    def prompt(y):
        return (f'<text class="t" x="{x0}" y="{y}"><tspan fill="{d0}">deepak@skandh</tspan>'
                f'<tspan class="m">:</tspan><tspan fill="{d1}">~</tspan><tspan class="m">$ </tspan></text>')

    line = 0
    map_idx = 0
    for idx, (kind, item, t_show, t_type, t_done) in enumerate(events):
        y = y0 + line * lh
        cls = f"l{idx}"
        css.append(f"@keyframes {cls}{{0%,{pct(t_show - 0.01, cycle)}{{opacity:0}}{pct(t_show, cycle)},100%{{opacity:1}}}}"
                   f".{cls}{{animation:{cls} {cycle}s linear infinite}}")
        g = [f'<g class="{cls}">']
        if kind == "cmd":
            cmd = item[1]
            cx = x0 + prompt_chars * cw
            wcmd = len(cmd) * cw
            g.append(prompt(y))
            g.append(f'<text class="t" x="{cx:.2f}" y="{y}">{esc(cmd)}</text>')
            cv, cu = f"c{idx}", f"u{idx}"
            css.append(
                f"@keyframes {cv}{{0%,{pct(t_type, cycle)}{{transform:translateX(0px);animation-timing-function:steps({len(cmd)},end)}}"
                f"{pct(t_done, cycle)},100%{{transform:translateX({wcmd:.2f}px)}}}}"
                f".{cv}{{transform:translateX({wcmd:.2f}px);animation:{cv} {cycle}s linear infinite}}"
                f"@keyframes {cu}{{0%,{pct(t_show - 0.01, cycle)}{{opacity:0}}{pct(t_show, cycle)},{pct(t_done + 0.25, cycle)}{{opacity:1}}"
                f"{pct(t_done + 0.26, cycle)},100%{{opacity:0}}}}"
                f".{cu}{{opacity:0;animation:{cu} {cycle}s linear infinite}}"
            )
            g.append(f'<g class="{cv}"><rect x="{cx - 1:.2f}" y="{y - 16}" width="{wcmd + cw + 2:.2f}" height="22" fill="{P["bg"]}"/>'
                     f'<rect class="{cu}" x="{cx:.2f}" y="{y - 14}" width="{cw:.2f}" height="18" fill="{d0}" fill-opacity=".85"/></g>')
        elif kind == "out":
            g.append(f'<text class="t" x="{x0}" y="{y}">{esc(item[1])}</text>')
        elif kind == "map":
            col = depth(P, map_idx / 4)
            map_idx += 1
            g.append(f'<text class="t m" x="{x0 + 2 * cw:.2f}" y="{y}">{esc(item[1])}</text>'
                     f'<text class="t" x="{x0 + 13 * cw:.2f}" y="{y}" style="fill:{col}">→</text>'
                     f'<text class="t" x="{x0 + 16 * cw:.2f}" y="{y}">{esc(item[2])}</text>')
        else:
            g.append(prompt(y))
            g.append(f'<rect class="blink" x="{x0 + prompt_chars * cw:.2f}" y="{y - 14}" width="{cw:.2f}" height="18" fill="{d0}" fill-opacity=".85"/>')
        g.append("</g>")
        body.append("".join(g) + "\n")
        line += 1

    o = [svg_open(W, H, "Terminal: whoami prints deepak skandh; the focus is ai, systems, algorithms, "
                        "first-principles engineering; underneath --list maps framework to implementation, "
                        "api to protocol, database to query engine, model to architecture plus optimization, "
                        "library to algorithm; status: still compiling.", "".join(css))]
    o.append(f'<defs><clipPath id="win"><rect width="{W}" height="{H}" rx="14"/></clipPath></defs>\n'
             f'<g clip-path="url(#win)"><rect width="{W}" height="{H}" fill="{P["bg"]}"/>'
             f'<rect width="{W}" height="38" fill="{P["surface"]}"/>'
             f'<line x1="0" y1="38.5" x2="{W}" y2="38.5" stroke="{P["line"]}"/></g>\n'
             f'<rect x=".5" y=".5" width="{W - 1}" height="{H - 1}" rx="13.5" fill="none" stroke="{P["line"]}"/>\n')
    for i in range(3):
        o.append(f'<circle cx="{22 + i * 18}" cy="19" r="5.5" fill="none" stroke="{P["faint"]}"/>')
    o.append(f'\n<text x="{W / 2}" y="23.5" text-anchor="middle" style="font:400 12px {MONO};fill:{P["faint"]}">deepak@skandh: ~</text>\n')
    o.append('<g class="all">\n' + "".join(body) + "</g>\n</svg>\n")
    return "".join(o)


# --------------------------------------------------------------------------- pipeline
STAGES = [
    ("parser", "text → tokens → syntax tree", "frontend"),
    ("query planner", "syntax tree → logical plan", "frontend"),
    ("optimizer", "cost model → cheapest physical plan", "frontend"),
    ("execution engine", "iterators, joins, aggregation", "execution"),
    ("storage engine", "pages, buffer pool, heap files", "storage"),
    ("indexes", "B+ trees, hash indexes", "storage"),
    ("transactions", "ACID, isolation levels", "transactions"),
    ("concurrency", "two-phase locking, MVCC", "transactions"),
    ("recovery", "write-ahead log, checkpoints", "transactions"),
]


def pipeline(theme: str) -> str:
    P = PALETTES[theme]
    W = 880
    rail = 88
    qy, s0, pitch = 122, 176, 46
    ys = [s0 + i * pitch for i in range(len(STAGES))]
    ry = ys[-1] + 58
    H = ry + 44
    bx, bw, bh = 112, 236, 34
    ax = 372
    d0, d1, d2 = P["depth"]
    query = "SELECT name FROM users WHERE id = 42;"
    qw = mono_width(query, 12.5) + 26

    cycle = 12.0
    q_at = 0.4
    arrive = [1.1 + i * 0.95 for i in range(len(STAGES))]
    r_at = arrive[-1] + 0.95
    hold_end, fade_end = cycle - 1.0, cycle - 0.45
    span = ry - qy

    css = [font_faces("display-bold", "mono"),
           f".title{{font:700 22px {DISPLAY};fill:{P['text']}}}"
           f".sub{{font:400 12.5px {MONO};fill:{P['muted']}}}"
           f".idx{{font:400 12px {MONO};fill:{P['faint']}}}"
           f".stage{{font:700 15px {DISPLAY};fill:{P['text']}}}"
           f".ann{{font:400 12.5px {MONO};fill:{P['muted']}}}"
           f".grp{{font:400 12px {MONO};fill:{P['muted']}}}"
           f".code{{font:400 12.5px {MONO}}}"
           ".hl,.hla,.dot{opacity:0}"
           ".prog{transform-box:fill-box;transform-origin:50% 0}"]

    def box_frames(name, a, visited=0.3):
        return (f"@keyframes {name}{{0%,{pct(a - 0.2, cycle)}{{opacity:0}}{pct(a, cycle)},{pct(a + 0.55, cycle)}{{opacity:1}}"
                f"{pct(a + 1.1, cycle)},{pct(hold_end, cycle)}{{opacity:{visited}}}{pct(fade_end, cycle)},100%{{opacity:0}}}}"
                f".{name}{{animation:{name} {cycle}s ease-in-out infinite}}")

    def ann_frames(name, a):
        return (f"@keyframes {name}{{0%,{pct(a - 0.2, cycle)}{{opacity:0}}{pct(a, cycle)},{pct(a + 0.55, cycle)}{{opacity:1}}"
                f"{pct(a + 1.0, cycle)},100%{{opacity:0}}}}"
                f".{name}{{animation:{name} {cycle}s ease-in-out infinite}}")

    css.append(box_frames("hq", q_at))
    for i, a in enumerate(arrive):
        css.append(box_frames(f"h{i}", a))
        css.append(ann_frames(f"a{i}", a))
    css.append(f"@keyframes hr{{0%,{pct(r_at - 0.2, cycle)}{{opacity:0}}{pct(r_at, cycle)},{pct(hold_end, cycle)}{{opacity:1}}"
               f"{pct(fade_end, cycle)},100%{{opacity:0}}}}.hr{{animation:hr {cycle}s ease-in-out infinite}}")

    stops = [(q_at, qy, d0)] + [(a, y, depth(P, i / (len(STAGES) - 1))) for i, (a, y) in enumerate(zip(arrive, ys))] \
        + [(r_at, ry, P["text"])]
    frames = [f"0%{{opacity:0;transform:translateY(0px);fill:{d0}}}"]
    prog = ["0%{transform:scaleY(0);opacity:1}"]
    for a, y, col in stops:
        dy = y - qy
        frames.append(f"{pct(a, cycle)},{pct(a + 0.5, cycle)}{{opacity:1;transform:translateY({dy}px);fill:{col}}}")
        prog.append(f"{pct(a, cycle)},{pct(a + 0.5, cycle)}{{transform:scaleY({dy / span:.4f});opacity:1}}")
    frames.append(f"{pct(hold_end, cycle)}{{opacity:1;transform:translateY({span}px);fill:{P['text']}}}")
    frames.append(f"{pct(fade_end, cycle)},100%{{opacity:0;transform:translateY({span}px);fill:{P['text']}}}")
    prog.append(f"{pct(hold_end, cycle)}{{transform:scaleY(1);opacity:1}}")
    prog.append(f"{pct(fade_end, cycle)},100%{{transform:scaleY(1);opacity:0}}")
    css.append("@keyframes dot{" + "".join(frames) + f"}}.dot{{animation:dot {cycle}s ease-in-out infinite}}")
    css.append("@keyframes prog{" + "".join(prog) + f"}}.prog{{animation:prog {cycle}s ease-in-out infinite}}")

    o = [svg_open(W, H, "minidb: a database engine built one layer at a time. A query flows through the parser, "
                        "query planner, optimizer, execution engine, storage engine, indexes, transactions, "
                        "concurrency control and recovery, and returns one row.", "".join(css))]
    o.append(f"""<defs>
<clipPath id="card"><rect width="{W}" height="{H}" rx="18"/></clipPath>
<linearGradient id="rail" x1="0" y1="{qy}" x2="0" y2="{ry}" gradientUnits="userSpaceOnUse">
<stop offset="0" stop-color="{d0}"/><stop offset=".5" stop-color="{d1}"/><stop offset="1" stop-color="{d2}"/></linearGradient>
</defs>
<g clip-path="url(#card)"><rect width="{W}" height="{H}" fill="{P['bg']}"/></g>
<rect x=".5" y=".5" width="{W - 1}" height="{H - 1}" rx="17.5" fill="none" stroke="{P['line']}"/>
<text class="title" x="40" y="54">minidb</text>
<text class="sub" x="40" y="78">a database engine, built one layer at a time</text>
<rect x="{rail - 0.5}" y="{qy}" width="1" height="{span}" fill="{P['line']}"/>
<rect class="prog" x="{rail - 1}" y="{qy}" width="2" height="{span}" fill="url(#rail)"/>
""")

    # query chip
    o.append(f'<circle cx="{rail}" cy="{qy}" r="4" fill="{P["bg"]}" stroke="{P["faint"]}"/>'
             f'<rect x="{bx}" y="{qy - 16}" width="{qw:.1f}" height="32" rx="8" fill="{P["surface"]}" stroke="{P["line"]}"/>'
             f'<rect class="hl hq" x="{bx}" y="{qy - 16}" width="{qw:.1f}" height="32" rx="8" fill="none" stroke="{d0}" stroke-width="1.4"/>'
             f'<text class="code" x="{bx + 13}" y="{qy + 4.5}" fill="{d0}">{esc(query)}</text>\n')

    # stages
    for i, ((name, ann, _), y) in enumerate(zip(STAGES, ys)):
        col = depth(P, i / (len(STAGES) - 1))
        o.append(f'<text class="idx" x="40" y="{y + 4.5}">{i + 1:02d}</text>'
                 f'<circle cx="{rail}" cy="{y}" r="4" fill="{P["bg"]}" stroke="{P["faint"]}"/>'
                 f'<circle class="hl h{i}" cx="{rail}" cy="{y}" r="4" fill="{col}"/>'
                 f'<rect x="{bx}" y="{y - bh / 2}" width="{bw}" height="{bh}" rx="8" fill="{P["surface"]}" stroke="{P["line"]}"/>'
                 f'<rect class="hl h{i}" x="{bx}" y="{y - bh / 2}" width="{bw}" height="{bh}" rx="8" fill="{col}" fill-opacity=".1" stroke="{col}" stroke-width="1.4"/>'
                 f'<text class="stage" x="{bx + 16}" y="{y + 5}">{esc(name)}</text>'
                 f'<text class="ann" x="{ax}" y="{y + 4.5}">{esc(ann)}</text>'
                 f'<text class="ann hla a{i}" x="{ax}" y="{y + 4.5}" style="fill:{P["text"]}">{esc(ann)}</text>\n')

    # group brackets
    gx = 748
    groups: dict[str, list[int]] = {}
    for i, (_, _, g) in enumerate(STAGES):
        groups.setdefault(g, []).append(i)
    for g, idxs in groups.items():
        top, bot = ys[idxs[0]] - bh / 2 + 3, ys[idxs[-1]] + bh / 2 - 3
        mid = (top + bot) / 2
        o.append(f'<path d="M{gx - 8} {top} H{gx} V{bot} H{gx - 8}" fill="none" stroke="{P["line"]}"/>'
                 f'<text class="grp" x="{gx + 12}" y="{mid + 4.5}">{g}</text>\n')

    # result
    res = "(1 row)"
    rw = mono_width(res, 13.5) + 28
    o.append(f'<circle cx="{rail}" cy="{ry}" r="4" fill="{P["bg"]}" stroke="{P["faint"]}"/>'
             f'<rect x="{bx}" y="{ry - 16}" width="{rw:.1f}" height="32" rx="8" fill="none" stroke="{P["line"]}" stroke-dasharray="3 3"/>'
             f'<rect class="hl hr" x="{bx}" y="{ry - 16}" width="{rw:.1f}" height="32" rx="8" fill="{d2}" fill-opacity=".1" stroke="{d2}" stroke-width="1.4"/>'
             f'<text x="{bx + 14}" y="{ry + 5}" style="font:400 13.5px {MONO};fill:{P["text"]}">{res}</text>'
             f'<text class="ann" x="{bx + rw + 18}" y="{ry + 4.5}">returned to the client</text>\n')

    o.append(f'<g class="dot"><circle cx="{rail}" cy="{qy}" r="10" fill-opacity=".18"/>'
             f'<circle cx="{rail}" cy="{qy}" r="4.5"/></g>\n</svg>\n')
    return "".join(o)


# --------------------------------------------------------------------------- interests
INTERESTS = [
    ("Intelligence", "why does it generalize?",
     ["artificial intelligence", "machine learning", "deep learning", "LLMs, generative AI", "NLP", "computer vision"]),
    ("Systems", "where does the time go?",
     ["backend engineering", "database systems", "distributed systems", "HPC", "systems engineering", "automation"]),
    ("Foundations", "what does it cost?",
     ["algorithms", "data structures", "competitive programming", "probability", "statistics"]),
    ("Science", "what does the data say?",
     ["data science", "computational biology", "research", "experimentation"]),
]


def _icon(kind: int, x: float, y: float, col: str) -> str:
    s = f'fill="none" stroke="{col}" stroke-width="1.6" stroke-linecap="round" stroke-linejoin="round"'
    if kind == 0:   # a tiny network
        pts = [(0, 18), (11, 4), (22, 14), (12, 22)]
        lines = "".join(f'<line x1="{x + a[0]}" y1="{y + a[1]}" x2="{x + b[0]}" y2="{y + b[1]}" {s}/>'
                        for a, b in [(pts[0], pts[1]), (pts[1], pts[2]), (pts[2], pts[3]), (pts[3], pts[0]), (pts[1], pts[3])])
        dots = "".join(f'<circle cx="{x + p[0]}" cy="{y + p[1]}" r="2.6" fill="{col}"/>' for p in pts)
        return lines + dots
    if kind == 1:   # layers
        return "".join(f'<path d="M{x} {y + 6 + k * 6} L{x + 11} {y + 1 + k * 6} L{x + 22} {y + 6 + k * 6} L{x + 11} {y + 11 + k * 6} Z" {s}/>'
                       for k in (2, 1, 0))
    if kind == 2:   # sigma
        return f'<path d="M{x + 19} {y + 2} H{x + 3} L{x + 12} {y + 12} L{x + 3} {y + 22} H{x + 19}" {s}/>'
    return f'<path d="M{x} {y + 12} C{x + 4} {y - 2} {x + 7} {y - 2} {x + 11} {y + 12} S{x + 18} {y + 26} {x + 22} {y + 12}" {s}/>'


def interests(theme: str) -> str:
    P = PALETTES[theme]
    W, H = 880, 298
    pad, colw = 24, (880 - 48) / 4
    css = [font_faces("display-bold", "display-regular", "mono"),
           f".h{{font:700 18px {DISPLAY};fill:{P['text']}}}"
           f".q{{font:400 11.5px {MONO}}}"
           f".i{{font:400 14px {DISPLAY};fill:{P['text']};fill-opacity:.86}}"]
    label = "What I'm into. " + " ".join(f"{t}: {', '.join(items)}." for t, _, items in INTERESTS)
    o = [svg_open(W, H, label, "".join(css))]
    o.append(f'<rect x=".5" y=".5" width="{W - 1}" height="{H - 1}" rx="17.5" fill="{P["bg"]}" stroke="{P["line"]}"/>\n')
    for k, (title, q, items) in enumerate(INTERESTS):
        x = pad + k * colw + 18
        col = depth(P, k / 3)
        if k:
            o.append(f'<line x1="{pad + k * colw}" y1="32" x2="{pad + k * colw}" y2="{H - 32}" stroke="{P["line_soft"]}"/>')
        o.append(_icon(k, x, 30, col))
        o.append(f'<text class="h" x="{x}" y="86">{title}</text>'
                 f'<text class="q" x="{x}" y="108" fill="{col}">{esc(q)}</text>')
        for j, it in enumerate(items):
            o.append(f'<text class="i" x="{x}" y="{146 + j * 23}">{esc(it)}</text>')
        o.append("\n")
    o.append("</svg>\n")
    return "".join(o)


# --------------------------------------------------------------------------- footer & placeholders
def footer(theme: str) -> str:
    P = PALETTES[theme]
    W, H = 880, 72
    d0, d1, d2 = P["depth"]
    css = font_faces("mono") + f".f{{font:400 12.5px {MONO};fill:{P['faint']}}}"
    return (svg_open(W, H, "still compiling.", css) +
            f'<defs><linearGradient id="r" x1="0" x2="1"><stop offset="0" stop-color="{d0}" stop-opacity="0"/>'
            f'<stop offset=".25" stop-color="{d0}"/><stop offset=".5" stop-color="{d1}"/><stop offset=".75" stop-color="{d2}"/>'
            f'<stop offset="1" stop-color="{d2}" stop-opacity="0"/></linearGradient></defs>'
            f'<rect x="120" y="18" width="{W - 240}" height="1" fill="url(#r)"/>'
            f'<text class="f" x="{W / 2}" y="52" text-anchor="middle">// still compiling.</text>\n</svg>\n')


def snake_placeholder(theme: str) -> str:
    P = PALETTES[theme]
    W, H = 880, 160
    css = font_faces("mono") + f".f{{font:400 12.5px {MONO};fill:{P['muted']}}}"
    cells = []
    for c in range(53):
        for r in range(7):
            cells.append(f'<rect x="{25 + c * 15.7:.1f}" y="{22 + r * 15.7:.1f}" width="11" height="11" rx="2.5" fill="{P["line_soft"]}"/>')
    return (svg_open(W, H, "Contribution graph appears after the first workflow run.", css) +
            "".join(cells) +
            f'<rect x="{W / 2 - 230}" y="{H / 2 - 18}" width="460" height="36" rx="8" fill="{P["bg"]}" stroke="{P["line"]}"/>'
            f'<text class="f" x="{W / 2}" y="{H / 2 + 4.5}" text-anchor="middle">contribution graph appears after the first workflow run</text>\n</svg>\n')


def main() -> None:
    GENERATED.mkdir(parents=True, exist_ok=True)
    out = {
        ASSETS / "terminal.svg": terminal(),
    }
    for theme in ("dark", "light"):
        out[ASSETS / f"header-{theme}.svg"] = header(theme)
        out[ASSETS / f"pipeline-{theme}.svg"] = pipeline(theme)
        out[ASSETS / f"interests-{theme}.svg"] = interests(theme)
        out[ASSETS / f"footer-{theme}.svg"] = footer(theme)
        # placeholders, overwritten by the workflow on its first run
        snake = GENERATED / f"snake-{theme}.svg"
        if not snake.exists():
            out[snake] = snake_placeholder(theme)
        stats = GENERATED / f"stats-{theme}.svg"
        if not stats.exists():
            out[stats] = update_profile.render_stats(theme, None)
    for path, svg in out.items():
        path.write_text(svg, encoding="utf-8")
        print(f"{path.relative_to(ROOT)!s:40s} {len(svg.encode()) / 1024:6.1f} KB")


if __name__ == "__main__":
    main()
