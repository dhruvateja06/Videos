# The Tech Intern — Production Pipeline

> How an episode goes from idea → rendered MP4 → delivered to the creator.
> This is the HyperFrames render workflow, the gotchas we already hit, and the
> exact commands.

## Tooling (already installed in this environment)

| Tool | How it's provided | Note |
|---|---|---|
| HyperFrames CLI 0.7.5 | `tech-intern-videos/node_modules/.bin/hyperframes` | the renderer |
| FFmpeg + FFprobe | npm `@ffmpeg-installer/ffmpeg`, `@ffprobe-installer/ffprobe`, symlinked to `/usr/local/bin` | apt install fails in sandbox; npm binaries work |
| Chrome Headless Shell | `hyperframes browser ensure` (cached in `~/.cache/hyperframes`) | Google CDN is allowed |
| GSAP (local) | `assets/vendor/gsap.min.js` | **never** load GSAP from a CDN |
| Fonts (local) | `assets/fonts/*.woff2` | **never** load Google Fonts |

Recreate after a sandbox reset:
```bash
cd tech-intern-videos && npm i hyperframes @ffmpeg-installer/ffmpeg @ffprobe-installer/ffprobe
node -e "require('fs').symlinkSync(require('@ffmpeg-installer/ffmpeg').path,'/usr/local/bin/ffmpeg')"
node -e "require('fs').symlinkSync(require('@ffprobe-installer/ffprobe').path,'/usr/local/bin/ffprobe')"
node_modules/.bin/hyperframes browser ensure
```

## Hard rules for compositions (the renderer has NO network)

- **All assets local.** Bundle GSAP + fonts under `assets/`. A CDN `<script>` or
  Google-Fonts link silently fails at render → no animation, wrong type.
- **Determinism only.** No `Date.now()`, no `Math.random()`, no `fetch`.
- **Every timed element** needs `class="clip"` + `data-start` + `data-duration`
  + `data-track-index`.
- **One paused timeline**, registered on `window.__timelines["<composition-id>"]`.
  HyperFrames seeks it to each frame's time and screenshots → FFmpeg encodes.
- **Scene exits need a hard kill.** After a fade/scale-out that ends on the next
  clip's start boundary, add `tl.set(sel, { opacity:0 }, t+dur)` or the linter
  flags `gsap_exit_missing_hard_kill` (non-linear seeking can leave stale state).
- **CSS transform vs GSAP.** Don't put `transform: scale(...)` in CSS for an
  element GSAP also scales — GSAP overwrites the whole transform. Use
  `tl.fromTo(sel, {scale:0}, {scale:1})` instead.

## The commands

```bash
cd tti-studio
export PATH="/usr/local/bin:$PATH"          # so npm ffmpeg is found
HF=../tech-intern-videos/node_modules/.bin/hyperframes

# LINT — must be 0 errors before rendering
$HF lint                                     # (warnings about file size/density are OK)

# RENDER — silent MP4 (no audio; voiceover added later by the creator)
$HF render -c compositions/ep01-full.html -o renders/ep01-full.mp4 \
   --fps 24 --quality standard --workers 4
```

- `--fps 24` is plenty for this style and ~20% fewer frames than 30.
- `--workers 4` ≈ cores−2; each worker is a Chrome process (~256 MB).

## Render-time reality (important)

The moving background means **every frame is unique** — the renderer can't dedupe
static frames, so an 11-minute video is **~15,840 frames** and takes **tens of
minutes** (roughly 20–50 min depending on background blur). It's a one-time cost.
Levers to speed it up:
- **Lighter background blur** (blur ~30px, not 60px) — biggest win, near-invisible.
- **24fps** instead of 30.
Kick long renders off with `run_in_background: true` and poll frame count in
`renders/work-*/capture-attempt-0/worker-*/`.

## Delivery (how the creator actually gets the file)

The in-chat file card sometimes shows **no download option** in the creator's
client, and large files (70+ MB) can choke. So:

1. **Compress** for delivery (flat motion-graphics shrink a lot):
   ```bash
   ffmpeg -y -i renders/ep01-full.mp4 -c:v libx264 -profile:v main -pix_fmt yuv420p \
     -crf 20 -preset medium -movflags +faststart -an deliverables/ep01-full.mp4
   ```
   - `--crf 18–20` ≈ near-lossless, ~25–40 MB → for quality checks.
   - `--crf 30` ≈ tiny ~5–6 MB → for a fast preview only (looks soft, not representative).
2. **Commit the compressed file to `tti-studio/deliverables/`** (a *tracked*
   folder — `renders/` is gitignored) and push.
3. Give the creator the **GitHub download link**:
   `https://github.com/dhruvateja06/videos/blob/<branch>/tti-studio/deliverables/<file>.mp4`
   → use the Download / "View raw" button. This always works regardless of the chat card.

## Scripts (teleprompter)

- Keep the read **clean**: plain prose, with a `▸` marker only where the creator
  should advance a click. **No animation descriptions in the script** — they
  confuse the live read.
- Master script style lives in `EP01_script_clean.md` (currently in scratchpad —
  port finalized scripts into `scripts/` so they persist).

## Repo layout

```
tti-studio/
├── CLAUDE.md            # auto-loaded; points here
├── docs/                # the channel brain (BRAND, STYLE, PIPELINE, CURRICULUM)
├── compositions/        # the HTML+GSAP episodes (ep01.html, ep01-full.html, ...)
├── assets/vendor/       # local gsap.min.js
├── assets/fonts/        # local brand woff2
├── deliverables/        # compressed MP4s, tracked, for GitHub download
└── renders/             # raw render output (gitignored)
```
