# Thumbnails — The Tech Intern · System Design series

A reusable thumbnail system so every episode looks like the same series.

## The rule
**Constant (never change — this is what makes the series recognizable):**
the big **SYSTEM DESIGN** title, the client→server→database diagram, the
`THE TECH INTERN // SYSTEM DESIGN` tag, and the navy/cyan/orange colours.

**Per-episode (the only things you change):** the episode number and the
**topic line** (Ep 1 = "The Fundamentals", Ep 2 = "Client & Server", …).

## Make a new one
```bash
npm i -D puppeteer-core   # once

node thumbnails/render.mjs \
  --ep "02"  --lead "" --main "Client & Server" \
  --micro "what really happens when you tap" \
  --out assets/thumbnails/sd-ep02.png
```
Output is 2560×1440 (crops to YouTube's 1280×720).

Flags: `--ep` episode label (becomes "EPISODE 02 …"), `--lead` small word before
the topic (often "The" or empty), `--main` the bold topic, `--micro` one-line
hook, `--out` PNG path. Chrome is auto-found, or set `PUPPETEER_EXECUTABLE_PATH`.

## Files
- `template.html` — the design (edit here to change the look for ALL episodes)
- `render.mjs` — fills the template and screenshots it to PNG
- `../assets/thumbnails/` — the rendered PNGs (committed, ready to upload)

Episode 1: `assets/thumbnails/sd-ep01-introduction.png`.
