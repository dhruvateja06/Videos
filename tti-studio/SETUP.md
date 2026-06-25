# HyperFrames — The Tech Intern — Setup & Usage

HyperFrames turns HTML/CSS + a GSAP timeline into a deterministic MP4. Our whole deck system is already HTML/CSS, so this lets us render episodes (or intros, shorts, lower-thirds) to video **without screen recording** — pixel-perfect, repeatable, audio-synced.

## What got installed (this environment)

| Dependency | How | Status |
|---|---|---|
| Node.js 22 | already present | ✅ |
| HyperFrames CLI 0.7.5 | `npm i hyperframes` (in `tech-intern-videos/`) | ✅ |
| FFmpeg + FFprobe | `@ffmpeg-installer/ffmpeg` + `@ffprobe-installer/ffprobe` (npm — binary ships in tarball), symlinked to `/usr/local/bin` | ✅ |
| Chrome Headless Shell | `hyperframes browser ensure` (cached in `~/.cache/hyperframes`) | ✅ |
| GSAP (local) | `npm i gsap` → copied to `assets/vendor/gsap.min.js` | ✅ |
| Fonts (local) | `@fontsource/fraunces` + `@fontsource/inter` → `assets/fonts/*.woff2` | ✅ |

> **Why local GSAP + fonts?** The render runs in headless Chrome with no outbound network. CDN `<script>`/Google-Fonts links silently fail and the animation/typography break. Everything must be bundled locally. The linter enforces this (`npm run check`).

## Project layout

```
tti-studio/
├── index.html              # the composition (HTML + GSAP timeline)
├── hyperframes.json        # config
├── package.json            # dev / check / render scripts
├── assets/
│   ├── vendor/gsap.min.js  # local GSAP
│   └── fonts/*.woff2        # local brand fonts (Fraunces, Inter)
└── renders/                # output MP4s
```

## The three commands

```bash
cd tti-studio

# PREVIEW — live browser preview with reload (run on your own machine)
npm run dev

# CHECK — lint + validate (must be 0 errors before render)
npm run check

# RENDER — produce an MP4 in renders/
npm run render
```

> In this remote sandbox, set `export PATH="/usr/local/bin:$PATH"` first so the npm-installed
> FFmpeg is found, and use the CLI at `../tech-intern-videos/node_modules/.bin/hyperframes`.
> On your own machine you'd `npm i -g hyperframes` (or use `npx`) and `npm run …` directly.

## How a composition works (the model)

1. A `#root` element carries `data-composition-id`, `data-duration` (seconds), `data-width/height`.
2. Every timed element gets `class="clip"` + `data-start` / `data-duration` / `data-track-index`.
3. All animation lives in **one paused GSAP timeline** registered on `window.__timelines["main"]`.
4. HyperFrames seeks that timeline to each frame's time and screenshots it → FFmpeg encodes → MP4. Deterministic: same input → identical output, every time.

**Rules:** no `Date.now()`, no `Math.random()`, no network fetches — everything must be local and deterministic.

## Adding audio (for full episodes)

- Put narration in `assets/` and reference a `<audio>` element; HyperFrames muxes it into the MP4 and you time the GSAP reveals to the voiceover. This is how we'd render a fully-automated episode (no presenter) — visuals + voice perfectly in sync.

## Turning our EP01 deck into a HyperFrames episode

Our current EP01 deck advances on **keypress** (manual reveals). HyperFrames is **time-based**. To render EP01 automatically we re-express each reveal as a GSAP timeline keyed to the narration timestamps (i.e., we need the voiceover first, then place each reveal at its second-mark). That's the next step when you want a render-instead-of-record episode.

## Re-create the env quickly (if the sandbox resets)

```bash
cd tech-intern-videos && npm i hyperframes @ffmpeg-installer/ffmpeg @ffprobe-installer/ffprobe
node -e "require('fs').symlinkSync(require('@ffmpeg-installer/ffmpeg').path,'/usr/local/bin/ffmpeg')"
node -e "require('fs').symlinkSync(require('@ffprobe-installer/ffprobe').path,'/usr/local/bin/ffprobe')"
node_modules/.bin/hyperframes browser ensure
```
