#!/usr/bin/env python3
"""Fill in the README placeholders in one go.

    python scripts/personalize.py --user deepakskandh \
        --linkedin deepak-skandh --email you@domain.com --portfolio https://your.site

Anything you leave out stays as a placeholder (or, for --portfolio, you can pass
--no-portfolio to remove that link entirely).
"""
import argparse
import re
from pathlib import Path

README = Path(__file__).resolve().parents[1] / "README.md"


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--user", required=True, help="GitHub username (also the repo name)")
    ap.add_argument("--linkedin", help="the part after linkedin.com/in/")
    ap.add_argument("--email")
    ap.add_argument("--portfolio", help="full URL")
    ap.add_argument("--no-portfolio", action="store_true", help="remove the portfolio link")
    a = ap.parse_args()

    text = README.read_text(encoding="utf-8")
    text = text.replace("YOUR_GITHUB_USERNAME", a.user)
    if a.linkedin:
        text = text.replace("YOUR_LINKEDIN_HANDLE", a.linkedin)
    if a.email:
        text = text.replace("YOUR_EMAIL", a.email)
    if a.no_portfolio:
        text = re.sub(r'&nbsp;\n<a href="YOUR_PORTFOLIO_URL"><kbd>&nbsp;portfolio&nbsp;</kbd></a>', "", text)
    elif a.portfolio:
        text = text.replace("YOUR_PORTFOLIO_URL", a.portfolio)
    README.write_text(text, encoding="utf-8")

    left = sorted(set(re.findall(r"YOUR_[A-Z_]+", text)))
    print("done." + (f" still to fill: {', '.join(left)}" if left else " no placeholders left."))


if __name__ == "__main__":
    main()
