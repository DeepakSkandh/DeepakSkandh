# Setup

This repo is a GitHub profile README. GitHub shows it on your profile when the
repository has exactly the same name as your username.

## 1. Create the repo

Create a **public** repository named exactly like your username (for example
`deepakskandh/deepakskandh`), with `main` as the default branch. Copy everything
from this folder into it, including the hidden `.github/` folder.

## 2. Fill in your details

```bash
python scripts/personalize.py --user YOUR_USERNAME \
  --linkedin YOUR_LINKEDIN_HANDLE --email you@example.com --portfolio https://your.site
```

Or find-and-replace by hand in `README.md`:

| placeholder | replace with |
| :-- | :-- |
| `YOUR_GITHUB_USERNAME` | your username (appears in every image URL) |
| `YOUR_LINKEDIN_HANDLE` | the part after `linkedin.com/in/` |
| `YOUR_EMAIL` | your email address |
| `YOUR_PORTFOLIO_URL` | a full URL, or delete that link |

## 3. Push, then run the workflow once

```bash
git add -A && git commit -m "profile" && git push
```

Then open **Actions → profile → Run workflow**. The first run replaces the
placeholder activity card, snake and log with real data. After that it runs every
day on its own.

If the run fails on the push step, go to **Settings → Actions → General →
Workflow permissions** and select **Read and write permissions**.

Optional: to include private contributions in the activity card, create a classic
personal access token with the `read:user` scope, add it as a repository secret
named `PROFILE_TOKEN`, and turn on "Include private contributions on my profile"
in your GitHub profile settings.

## 4. Optional GIF

The animated terminal near the top already plays the role of a GIF. If you also
want a real GIF, put it at `assets/coding.gif` and uncomment the block under the
terminal in `README.md`. Keeping it inside the repo is more reliable than
hotlinking from Giphy or Tenor.

## Editing the design

All static artwork is generated from code:

```bash
python scripts/build_assets.py      # header, terminal, pipeline, interests, footer
```

Copy, colours and layout live in `scripts/build_assets.py` and
`scripts/theme.py`. The palette has one rule: colour encodes depth. Cyan is the
surface of a stack, violet is the middle, amber is the bottom.

## What's in here

```text
README.md                         the profile
assets/
  header-{dark,light}.svg         animated hero: a probe descends an abstraction stack
  terminal.svg                    animated terminal session
  pipeline-{dark,light}.svg       animated minidb query path
  interests-{dark,light}.svg      interests panel
  footer-{dark,light}.svg
  generated/                      rewritten daily by the workflow
  fonts/                          subset TeX Gyre Adventor + DejaVu Sans Mono, embedded in every SVG
scripts/
  build_assets.py                 regenerates the static SVGs
  update_profile.py               activity card + ~/log (run by the workflow)
  theme.py                        palette, fonts, helpers
  personalize.py                  fills in placeholders
  subset_fonts.py                 one-time font subsetting (needs fonttools)
.github/workflows/profile.yml     daily refresh
```
