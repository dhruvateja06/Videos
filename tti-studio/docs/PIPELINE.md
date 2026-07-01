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
| ElevenLabs TTS | `ELEVENLABS_API_KEY` env (needs `text_to_speech` perm) | Dhruva voice; see `docs/VOICEOVER.md` |

> **Voiceover is now a standard phase.** After the silent render, generate the
> creator's Dhruva voice and word-sync the visuals to it (`docs/VOICEOVER.md`,
> reference impl in the previous episode's `sync_build.py`). Deliverables:
> `video-voiced.mp4` + `outro-voiced.mp4`.

> **Fresh clone?** None of the toolchain ships in the repo. Install once:
> `brew install node ffmpeg` then `cd tti-studio && npm install` and
> `npx hyperframes@0.7.5 browser ensure` (uses system Chrome if installed).

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
- **CSS transform vs GSAP — never both on the same element.** Don't put
  `transform: scale(...)` in CSS for an element GSAP also scales — GSAP
  overwrites the whole transform. Use `tl.fromTo(sel, {scale:0}, {scale:1})`
  instead. **This also applies to CSS `@keyframes` animations** (e.g. an
  "ambient background" `animation: drift 18s infinite` on the same element a
  GSAP `tl.to(sel, {x, y, scale, repeat:...})` also drives) — the two
  animation systems fight over `transform` on every paint. It's often
  invisible while scrubbing live in a browser (your eye averages it out) but
  shows up as a faint tearing/glitch artifact in the actual rendered MP4
  frames, because each frame is a frozen capture at one instant where the two
  systems can disagree. If an element needs continuous ambient motion, drive
  it with GSAP alone (`repeat:-1, yoyo:true` or similar) — never a CSS
  `@keyframes` animation in parallel.
- **Flex-centered scene shells stretch pills/badges full-width by default.**
  If your `.scene` shell uses `display:flex; flex-direction:column;
  justify-content:center` to vertically center content (common fix for
  content sitting pinned at the top of a tall canvas with dead space below),
  the default `align-items:stretch` will stretch EVERY direct-child block —
  including small pill/tag/badge elements that should hug their own content
  width — into a full-width bar. Give those specific classes (`.tag`,
  `.badge`, `.divider`, etc.) an explicit `width:fit-content` rather than
  changing `align-items` globally (that would also shrink the multi-column
  grids/cards that *should* stay full-width).
- **Multi-step scenes: persistent header + crossfade, not a wipe per step.**
  If one scene walks through several numbered steps/beats (e.g. "Step 1 →
  Step 2 → Step 3"), don't gate each step as a full `wipe()`/hide-then-show
  cut — that reads as a new scene every time, not steps of one idea. Instead,
  give the scene one persistent header (topic label + optional step-progress
  dial) that stays on screen for the whole scene, and crossfade only the
  step content underneath it. Reserve `wipe()` for real scene-to-scene
  boundaries.
- **Type scale: bigger than you think, especially on 1920×1080.** A type
  scale that looks fine in isolation can still leave a scene feeling sparse
  and empty on a full HD canvas if it was tuned for a taller/narrower format.
  If a scene "looks empty" despite having the right content, check whether
  the type scale itself is just too small for the canvas before adding more
  content — bumping font sizes ~1.3–1.4× is often the actual fix.

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

## ⚠️ Never use `-movflags +faststart` on this Mac

Confirmed on this machine: muxing with `-movflags +faststart` corrupts the
H.264 stream (the AI vertical hit this directly — faststart-muxed episode
renders played back broken while the identical mux without the flag was
clean). All ffmpeg mux commands in this doc and in `VOICEOVER.md` have had
`-movflags +faststart` removed for that reason — **don't add it back**, even
though it's the "normal" flag for web-streamable MP4 (moves the moov atom to
the front). If a delivered file needs faststart for streaming, do it as a
separate, verified remux step and spot-check playback before shipping it.

## Verifying a specific nested composition file (CLI quirk)

`hyperframes lint` / `validate` / `snapshot` only accept a **directory**
argument (a project root containing `index.html`), not a path to a specific
`.html` file — passing `episodes/epNN/composition.html` errors with "No
index.html file found." `render` is the exception: `-c <path>` does accept a
specific file, resolved against the `DIR` you pass (usually `.` from the
project root), which is why the render commands throughout this doc use
`render . -c episodes/epNN/...`.

Don't try to work around the lint/validate/snapshot limitation by copying a
composition into a fake nested folder and renaming it `index.html` — that
folder becomes the tool's notion of "project root," so the composition's own
`../../assets/...` paths (correct from the real project root) now point
*outside* that fake root and 404 (fonts, GSAP, everything fails to load, and
you'll see a misleadingly blank/broken capture that has nothing to do with
your actual composition).

The reliable way to spot-check a nested composition with real asset paths:
serve the **real project root** with a static file server and open the
composition's real URL path in an actual browser — this is what the
`thumbnail-preview`-style launch.json entries are for (see `.claude/launch.json`).
Once loaded, `window.__timelines["<composition-id>"].seek(t)` jumps to any
timestamp and a screenshot at that moment is a faithful preview — far more
reliable than the sandboxed lint/snapshot tools for anything nested under
`episodes/`.

## Delivery (how the creator actually gets the file)

The in-chat file card sometimes shows **no download option** in the creator's
client, and large files (70+ MB) can choke. So:

1. **Compress** for delivery (flat motion-graphics shrink a lot):
   ```bash
   ffmpeg -y -i renders/ep01-full.mp4 -c:v libx264 -profile:v main -pix_fmt yuv420p \
     -crf 20 -preset medium -an deliverables/ep01-full.mp4
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
├── CLAUDE.md             # auto-loaded; points to docs/
├── docs/                 # the channel brain
│   ├── WORKFLOW.md       # ⭐ the 7-phase episode process
│   ├── BRAND.md, STYLE.md, PIPELINE.md (this file), CURRICULUM.md
├── .claude/skills/       # project-scope skills (caveman, humanizer,
│                         # infographic-builder, …)
├── assets/               # shared, used by every episode composition
│   ├── vendor/gsap.min.js
│   └── fonts/*.woff2
├── episodes/             # one folder per episode, ALL deliverables go here
│   ├── ep01/
│   │   ├── composition.html      # main 11-min HyperFrames composition
│   │   ├── composition-outro.html
│   │   ├── deck.html             # navigable HTML deck
│   │   ├── script.md             # narration script
│   │   ├── script.srt            # subtitles (after recording)
│   │   ├── contact-sheet.png     # review stills (optional)
│   │   ├── video.mp4             # final compressed deliverable
│   │   ├── outro.mp4
│   │   └── youtube.md            # title + description (optional, post-record)
│   └── ep02/ …
└── renders/              # raw render output, gitignored — staging only
```

**Asset paths from a composition** (now two levels deep at `episodes/epNN/`):

```html
<script src="../../assets/vendor/gsap.min.js"></script>
<link … src="../../assets/fonts/inter-latin-700-normal.woff2" …>
```

**Per-episode commands** (replace `epNN` with the episode number):

```bash
cd tti-studio
export PATH="/usr/local/bin:$PATH"
HF=../tech-intern-videos/node_modules/.bin/hyperframes

# Lint
$HF lint

# Render main → renders/ (gitignored staging)
$HF render -c episodes/epNN/composition.html \
   -o renders/epNN-full.mp4 \
   --fps 24 --quality standard --workers 4

# Render outro
$HF render -c episodes/epNN/composition-outro.html \
   -o renders/epNN-outro.mp4 \
   --fps 24 --quality standard --workers 4

# Compress to deliverable (near-lossless CRF 20)
ffmpeg -y -i renders/epNN-full.mp4 \
   -c:v libx264 -profile:v high -pix_fmt yuv420p \
   -crf 20 -preset medium -an \
   episodes/epNN/video.mp4
ffmpeg -y -i renders/epNN-outro.mp4 \
   -c:v libx264 -profile:v high -pix_fmt yuv420p \
   -crf 20 -preset medium -an \
   episodes/epNN/outro.mp4
```
