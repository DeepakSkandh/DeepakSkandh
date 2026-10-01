#!/usr/bin/env python3
"""Refresh the living parts of the profile. Runs daily in .github/workflows/profile.yml.

  1. assets/generated/stats-{dark,light}.svg
       contributions over the past year, current and longest streak, public repos,
       a 52-week activity strip and a language breakdown. Rendered here, in the same
       design language as the rest of the profile, so nothing depends on a
       third-party stats server staying up.
  2. the ~/log block in README.md, between <!-- LOG:START --> and <!-- LOG:END -->
       recent public activity, written as a terminal log.

Environment
  GITHUB_TOKEN    token for the GitHub API (the workflow passes PROFILE_TOKEN if set,
                  otherwise the built-in token)
  PROFILE_USER    username; defaults to the repository owner in Actions
  EXCLUDE_LANGS   comma-separated languages to leave out of the breakdown
                  (default: "Jupyter Notebook", whose stored outputs dwarf real code)

Local testing without network:  python scripts/update_profile.py --fixture sample.json
Pure standard library.
"""
from __future__ import annotations

import argparse
import datetime as dt
import json
import os
import re
import sys
import urllib.request
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

from theme import DISPLAY, MONO, PALETTES, ROOT, esc, font_faces, mono_width, svg_open  # noqa: E402

README = ROOT / "README.md"
GENERATED = ROOT / "assets" / "generated"
API = "https://api.github.com"

QUERY = """
query($login: String!) {
  user(login: $login) {
    repositories(first: 100, ownerAffiliations: OWNER, isFork: false, privacy: PUBLIC) {
      totalCount
      nodes {
        name
        languages(first: 10, orderBy: {field: SIZE, direction: DESC}) {
          edges { size node { name color } }
        }
      }
    }
    contributionsCollection {
      contributionCalendar {
        totalContributions
        weeks { contributionDays { date contributionCount } }
      }
    }
  }
}
"""


# --------------------------------------------------------------------------- GitHub API
def _request(url: str, token: str | None, body: dict | None = None):
    data = json.dumps(body).encode() if body is not None else None
    req = urllib.request.Request(url, data=data, method="POST" if data else "GET")
    req.add_header("Accept", "application/vnd.github+json")
    req.add_header("User-Agent", "profile-refresh")
    if token:
        req.add_header("Authorization", f"Bearer {token}")
    with urllib.request.urlopen(req, timeout=30) as resp:
        return json.load(resp)


def fetch(user: str, token: str | None) -> dict:
    gql = _request(f"{API}/graphql", token, {"query": QUERY, "variables": {"login": user}})
    if gql.get("errors"):
        raise RuntimeError(gql["errors"])
    events = _request(f"{API}/users/{user}/events/public?per_page=100", token)
    return {"graphql": gql["data"], "events": events}


# --------------------------------------------------------------------------- stats
def summarize(data: dict, exclude: set[str]) -> dict:
    user = data["graphql"]["user"]
    cal = user["contributionsCollection"]["contributionCalendar"]
    days = [d for w in cal["weeks"] for d in w["contributionDays"]]
    days.sort(key=lambda d: d["date"])
    counts = [d["contributionCount"] for d in days]

    longest = run = 0
    for c in counts:
        run = run + 1 if c else 0
        longest = max(longest, run)
    current = 0
    tail = counts[:-1] if counts and counts[-1] == 0 else counts   # today may simply not have started yet
    for c in reversed(tail):
        if not c:
            break
        current += 1

    weeks = [sum(d["contributionCount"] for d in w["contributionDays"]) for w in cal["weeks"]][-52:]

    langs: dict[str, list] = {}
    for repo in user["repositories"]["nodes"]:
        for edge in repo["languages"]["edges"]:
            name = edge["node"]["name"]
            if name in exclude:
                continue
            entry = langs.setdefault(name, [0, edge["node"]["color"]])
            entry[0] += edge["size"]
    total = sum(v[0] for v in langs.values()) or 1
    ranked = sorted(langs.items(), key=lambda kv: -kv[1][0])
    top = [(n, v[0] / total, v[1]) for n, v in ranked[:6]]
    rest = 1 - sum(share for _, share, _ in top)
    if ranked[6:] and rest > 0.004:
        top.append(("other", rest, None))

    return {
        "total": cal["totalContributions"], "current": current, "longest": longest,
        "repos": user["repositories"]["totalCount"], "weeks": weeks, "langs": top,
    }


def render_stats(theme: str, s: dict | None, synced: str | None = None) -> str:
    """The activity card. With s=None it renders an honest empty state."""
    P = PALETTES[theme]
    d0, d1, d2 = P["depth"]
    W, H = 880, 300
    x0, x1 = 32, W - 32
    css = [font_faces("display-bold", "mono"),
           f".t{{font:700 17px {DISPLAY};fill:{P['text']}}}"
           f".n{{font:700 32px {DISPLAY};fill:{P['text']}}}"
           f".l{{font:400 11.5px {MONO};fill:{P['muted']}}}"
           f".s{{font:400 11px {MONO};fill:{P['faint']}}}"
           ".bar{transform-box:fill-box;transform-origin:50% 100%;animation:grow .9s cubic-bezier(.2,.7,.2,1) backwards}"
           "@keyframes grow{from{transform:scaleY(0)}}"]
    label = "GitHub activity over the past year" + (
        f": {s['total']} contributions, current streak {s['current']} days, longest streak {s['longest']} days, "
        f"{s['repos']} public repositories. Languages: "
        + ", ".join(f"{n} {share * 100:.1f}%" for n, share, _ in s["langs"]) if s else ": awaiting first sync.")
    o = [svg_open(W, H, label, "".join(css))]
    o.append(f'<rect x=".5" y=".5" width="{W - 1}" height="{H - 1}" rx="17.5" fill="{P["bg"]}" stroke="{P["line"]}"/>\n')
    o.append(f'<text class="t" x="{x0}" y="46">The past twelve months</text>')
    o.append(f'<text class="s" x="{x1}" y="46" text-anchor="end">'
             f'{esc("synced " + synced + " UTC" if synced else "not synced yet")}</text>\n')

    metrics = [("contributions", s and s["total"]), ("current streak, days", s and s["current"]),
               ("longest streak, days", s and s["longest"]), ("public repositories", s and s["repos"])]
    colw = (x1 - x0) / 4
    for k, (lab, val) in enumerate(metrics):
        x = x0 + k * colw
        o.append(f'<text class="n" x="{x}" y="104">{"–" if val is None else f"{val:,}"}</text>'
                 f'<text class="l" x="{x}" y="126">{esc(lab)}</text>')
    o.append("\n")

    # 52-week strip, coloured from surface (old) to depth (recent)
    weeks = (s["weeks"] if s else []) or [0] * 52
    weeks = ([0] * 52 + weeks)[-52:]
    peak = max(weeks) or 1
    pitch = (x1 - x0) / 52
    base, tall = 210, 60
    for i, v in enumerate(weeks):
        h = max(2.0, tall * v / peak)
        fill = P["line_soft"] if v == 0 else d0
        op = 1 if v == 0 else 0.35 + 0.65 * v / peak
        o.append(f'<rect class="bar" style="animation-delay:{i * 12}ms" x="{x0 + i * pitch + 1.5:.1f}" y="{base - h:.1f}" '
                 f'width="{pitch - 3:.1f}" height="{h:.1f}" rx="1.5" fill="{fill}" fill-opacity="{op:.2f}"/>')
    o.append(f'\n<text class="s" x="{x0}" y="{base + 18}">52 weeks ago</text>'
             f'<text class="s" x="{x1}" y="{base + 18}" text-anchor="end">this week</text>\n')

    # language breakdown
    by, bh = 248, 8
    o.append(f'<clipPath id="lb"><rect x="{x0}" y="{by}" width="{x1 - x0}" height="{bh}" rx="4"/></clipPath>')
    o.append(f'<g clip-path="url(#lb)"><rect x="{x0}" y="{by}" width="{x1 - x0}" height="{bh}" fill="{P["line_soft"]}"/>')
    langs = s["langs"] if s else []
    cursor = x0
    for name, share, color in langs:
        w = (x1 - x0) * share
        o.append(f'<rect x="{cursor:.1f}" y="{by}" width="{w:.1f}" height="{bh}" fill="{color or P["faint"]}"/>')
        cursor += w
    o.append("</g>\n")
    lx = x0
    if langs:
        for name, share, color in langs:
            text = f"{name} {share * 100:.1f}%"
            need = 14 + mono_width(text, 11.5) + 22
            if lx + need > x1 + 22:
                break
            o.append(f'<circle cx="{lx + 4}" cy="{by + 27}" r="4" fill="{color or P["faint"]}"/>'
                     f'<text class="l" x="{lx + 14}" y="{by + 31}">{esc(text)}</text>')
            lx += need
    else:
        o.append(f'<text class="l" x="{x0}" y="{by + 31}">languages appear after the first sync of the profile workflow</text>')
    o.append("\n</svg>\n")
    return "".join(o)


# --------------------------------------------------------------------------- log
def _describe(ev: dict, user: str):
    kind, p = ev["type"], ev.get("payload", {})
    repo = ev["repo"]["name"]
    if repo.lower() == f"{user}/{user}".lower():
        return None                      # skip edits to this profile repo itself
    short = repo.split("/", 1)[1] if repo.lower().startswith(user.lower() + "/") else repo
    if kind == "PushEvent":
        branch = p.get("ref", "").removeprefix("refs/heads/")
        n = len(p.get("commits") or [])
        return "push", short, f"{branch}" + (f", {n} commit{'s' * (n != 1)}" if n else "")
    if kind == "CreateEvent":
        if p.get("ref_type") == "repository":
            return "create", short, "new repository"
        if p.get("ref_type") == "tag":
            return "tag", short, p.get("ref", "")
        return None
    if kind == "PullRequestEvent" and p.get("action") in ("opened", "closed"):
        pr = p.get("pull_request", {})
        state = "merged" if pr.get("merged") else p["action"]
        return "pr", short, f"#{pr.get('number', '?')} {state}"
    if kind == "IssuesEvent" and p.get("action") == "opened":
        return "issue", short, f"#{p.get('issue', {}).get('number', '?')} opened"
    if kind == "ReleaseEvent" and p.get("action") == "published":
        return "release", short, p.get("release", {}).get("tag_name", "")
    if kind == "WatchEvent":
        return "star", short, "starred"
    if kind == "ForkEvent":
        return "fork", short, "forked"
    return None


def render_log(events: list, user: str, limit: int = 8) -> str:
    rows, seen = [], set()
    for ev in events:
        d = _describe(ev, user)
        if not d:
            continue
        day = ev["created_at"][:10]
        key = (day, d[0], d[1])
        if d[0] == "push" and key in seen:  # one line per repo per day
            continue
        seen.add(key)
        rows.append((day, *d))
        if len(rows) >= limit:
            break
    lines = [f'$ git log --author="{user}" --all --oneline -n {limit}']
    if not rows:
        lines.append("  (no recent public activity)")
    for day, kind, repo, detail in rows:
        repo = repo if len(repo) <= 26 else repo[:25] + "…"
        lines.append(f"  {day}  {kind:<8} {repo:<27} {detail}".rstrip())
    return "\n".join(lines)


def write_log(block: str) -> bool:
    text = README.read_text(encoding="utf-8")
    new = re.sub(r"(<!-- LOG:START -->\n).*?(\n<!-- LOG:END -->)",
                 lambda m: f"{m.group(1)}```text\n{block}\n```{m.group(2)}", text, flags=re.S)
    if new != text:
        README.write_text(new, encoding="utf-8")
        return True
    return False


# --------------------------------------------------------------------------- main
def main() -> None:
    ap = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    ap.add_argument("--fixture", help="JSON file with {graphql, events} instead of calling the API")
    ap.add_argument("--user", default=os.environ.get("PROFILE_USER") or os.environ.get("GITHUB_REPOSITORY_OWNER"))
    args = ap.parse_args()
    if not args.user:
        sys.exit("set PROFILE_USER or pass --user")

    data = json.loads(Path(args.fixture).read_text()) if args.fixture else fetch(args.user, os.environ.get("GITHUB_TOKEN"))
    exclude = {x.strip() for x in os.environ.get("EXCLUDE_LANGS", "Jupyter Notebook").split(",") if x.strip()}
    stats = summarize(data, exclude)
    today = dt.datetime.now(dt.timezone.utc).strftime("%Y-%m-%d")

    GENERATED.mkdir(parents=True, exist_ok=True)
    for theme in ("dark", "light"):
        (GENERATED / f"stats-{theme}.svg").write_text(render_stats(theme, stats, today), encoding="utf-8")
    changed = write_log(render_log(data["events"], args.user))
    print(f"stats: {stats['total']} contributions, streak {stats['current']}/{stats['longest']}, "
          f"{len(stats['langs'])} languages; log {'updated' if changed else 'unchanged'}")


if __name__ == "__main__":
    main()
