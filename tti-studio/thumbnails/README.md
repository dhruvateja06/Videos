# Thumbnails — The Tech Intern · System Design series

A reusable thumbnail SYSTEM so every episode looks like the same series, while
each one still depicts its own topic.

## The rule
**Constant (the series skin — never change):** the dark navy bg + grid + glows,
the `EPISODE NN` badge, the corner brackets, the card+wire diagram styling, the
teal/orange palette, the fonts, and the `THE TECH INTERN // SYSTEM DESIGN` tag.

**Per-episode (make each one depict THAT episode):**
- the **hero title** = the episode's topic, big (Ep1 = "SYSTEM DESIGN" because
  it introduces system design; Ep2 = "DNS & HTTP"; etc.). Do NOT repeat
  "SYSTEM DESIGN" as the hero on every episode — it's already in the bottom tag.
- the **right-side diagram** = the thing the episode actually teaches (Ep1 =
  client→server→database; Ep2 = the DNS lookup name→DNS→IP). Don't reuse the
  same diagram every time.
- the **topic line**, **micro hook**, and the ghost episode number.

## Two ways to render
**A) Bespoke per-episode file (preferred for episodes after the intro).**
Copy an existing episode file, change the hero + diagram + text, render it:
```bash
export PUPPETEER_EXECUTABLE_PATH="/Applications/Google Chrome.app/Contents/MacOS/Google Chrome"
node thumbnails/render.mjs --file thumbnails/ep02.html \
  --out assets/thumbnails/sd-ep02-dns-http.png
```

**B) Generic template (quick text-only swap — used for Ep1).**
`template.html` keeps the SYSTEM DESIGN hero + client/server/database diagram and
only swaps text via flags:
```bash
node thumbnails/render.mjs --ep "01" --main "Introduction" \
  --micro "what it is, and why it matters" \
  --out assets/thumbnails/sd-ep01-introduction.png
```
Flags: `--ep`, `--lead`, `--main`, `--micro`, `--file` (html to render, defaults
to template.html), `--out`. Output is 2560×1440 (crops to YouTube 1280×720).
Needs `puppeteer-core` (devDep) + Chrome.

## Files
- `template.html` — the series skin + the generic (text-swap) layout
- `ep02.html` — Ep2's bespoke thumbnail (DNS & HTTP hero + DNS-lookup diagram)
- `render.mjs` — fills + screenshots an html to PNG
- `../assets/thumbnails/` — the rendered PNGs (committed, ready to upload)

## Done so far
- Ep1: `assets/thumbnails/sd-ep01-introduction.png`
- Ep2: `assets/thumbnails/sd-ep02-dns-http.png`

> Palette note: thumbnails use the series teal/orange; the *videos* use the
> cobalt/navy "Engineer's Terminal" palette. Consistent within each set, not
> across — worth aligning at some point.
