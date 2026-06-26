# EPISODE WORKFLOW — the one true pipeline

> **READ THIS FIRST, EVERY EPISODE. Follow it in order. Do not improvise, do not
> reorder, do not skip the validation gate.** This file exists because we kept
> deviating; this is the agreed process. If something here is wrong, change the
> doc first, then follow it — don't freelance.

This doc is the **orchestrator**. The other docs are the detail:
`BRAND.md` (voice + audience), `STYLE.md` (the look / motion + thumbnail system),
`PIPELINE.md` (HyperFrames render mechanics), `CURRICULUM.md` (the 30-episode map).

---

## The pipeline (6 stages, 2 gates)

```
1. TOPIC      pick the next episode from CURRICULUM.md
2. RESEARCH   deep, simple, example-driven → research.md
3. PPT        build composition.html + navigable deck.html   ──▶  GATE 1: validate the deck
4. SCRIPT     (only after GATE 1) conversational narration → script.md   ──▶ GATE 2: approve voice
5. RENDER     re-time composition to script → video.mp4 (silent)
6. THUMBNAIL  from thumbnails/template.html → thumbnail.png
```

**Deliverables are committed to the episode's git folder — NOT dumped in chat as
the system of record.** (You may show a preview image/clip in chat, but git is
the home. See "Where deliverables live".)

---

### Stage 1 — TOPIC
- The next episode and its title come from **`CURRICULUM.md`** (Season 2 = HLD,
  30 episodes; Season 3 = LLD). Don't invent topics.
- Confirm: episode number, title, and the one-line promise.
- Create the folder (see structure below) and an episode `README.md` stub.

### Stage 2 — RESEARCH → `research.md`
- Use the **`deep-research`** skill. Goal: content a beginner *gets*, in plain
  8th-grade language, **no jargon**, **every concept carried by an example**
  (prefer Indian products — Swiggy/UPI/Hotstar/IRCTC/Ola).
- Follow the **dossier standard in `CURRICULUM.md`** (promise, the teaching
  content, the Indian teardown with **cited** numbers, analogy, misconceptions,
  the 8th-grade explanation, numbers-to-get-right, sources).
- **Sourcing rule:** any number/claim shown on screen must be ✅ verified with a
  source. Flag anything single-source/unconfirmed and keep it off-screen or
  qualitative. (We learned this the hard way — e.g. Hotstar 59M, never 60/61M.)

### Stage 3 — PPT (the HTML deck) → `composition.html` + `deck.html`
- Author **`composition.html`** = the animated HyperFrames source, in the
  **current Season-2 "dark systems-blueprint" theme** (see `STYLE.md`): navy +
  cyan, orange as the hot accent, Inter + JetBrains Mono, HUD frame, the
  boxes-and-arrows motion language, **icons** (phone / server / database
  cylinder / cache / CDN), build-ons, packets, count-ups.
- **Teach with one running example threaded through** (Ep 1 = "baby Instagram").
  Avoid definition-dumps. One idea per scene.
- **Best infographics**: every concept gets a diagram that *builds*, not a bullet.
- Lint must be **0 errors** (see Commands). Re-use the proven kit from the last
  episode's `composition.html` as the starting point.
- Export a **self-contained navigable `deck.html`** (fonts + GSAP inlined, arrow/
  click to step slides, `A` to animate) — this is what the creator clicks through.
- **▶ GATE 1 — VALIDATE.** Deliver the deck (and per-scene preview stills) and
  **STOP. Wait for explicit approval** of content + visuals before continuing.
  Do not write the script or render until the deck is approved.

### Stage 4 — SCRIPT → `script.md`  *(only after GATE 1)*
- Write the **narration / teleprompter** script: **conversational**, like a
  person talking — contractions, direct "you", rhetorical questions, one beat per
  scene, flows as one continuous talk (NOT 13 read-aloud paragraphs). Plain voice
  per `BRAND.md`. Clean read — **no animation directions in the script**.
- Annotate each scene's spoken length (≈140 wpm) — this drives the re-timing.
- **▶ GATE 2 — APPROVE VOICE.** Confirm the script reads right before re-timing,
  because the animation gets locked to these exact words.

### Stage 5 — RENDER → `video.mp4`
- **Re-time `composition.html` to the script**: every scene's `data-duration` and
  internal beats match its narration so builds land on the words.
- Render a **SILENT** MP4 (the creator adds voiceover + music in post) at
  **`--fps 24 --quality standard`**, then `ffmpeg -movflags +faststart`. See
  `PIPELINE.md` for the render-env setup (ffmpeg/ffprobe on PATH, Chrome).
- Renders are slow (living bg = every frame unique) → run in the **background**.
- Commit a **compressed** `video.mp4` (~10–25 MB) to the episode folder; keep the
  raw `renders/` workdir gitignored.

### Stage 6 — THUMBNAIL → `thumbnail.png`
- Generate from **`thumbnails/template.html`** via `thumbnails/render.mjs`.
- **Constant (series identity, never change):** the big **SYSTEM DESIGN** title,
  the client→server→database diagram, the brand tag, the colours.
- **Per-episode (only these change):** the episode number + the **topic line**
  (the actual episode title — Ep 1 = "Introduction", Ep 2 = "Client & Server").
  No filler like "start here"/"fundamentals" unless that's literally the topic.

---

## Where deliverables live (git, per episode)

One folder per episode under the season. **All deliverables go here and are
committed.** Do not scatter them across `compositions/`, `scripts/`, etc., and do
not treat the chat as the deliverable store.

```
system-design/                                  # Season 2 (HLD)
  ep-01-introduction-to-system-design/
    README.md          # one-liner + status checklist for this episode
    research.md         # Stage 2 dossier
    composition.html    # Stage 3 animated source  (assets via ../../assets/…)
    deck.html           # Stage 3 self-contained navigable PPT (for validation)
    script.md           # Stage 4 narration / teleprompter
    video.mp4           # Stage 5 final silent render (compressed)
    thumbnail.png       # Stage 6 thumbnail
  ep-02-client-and-server/
    …
```

**Naming:** `ep-NN-<kebab-title>`. Episode `README.md` carries a status checklist
so anyone can see where the episode is in the pipeline.

**Shared, NOT per-episode:** `assets/` (fonts, gsap), `thumbnails/` (template +
render.mjs), `docs/` (these brain files). Season 1 (AI) legacy lives in
`compositions/`.

---

## Hard rules (the anti-deviation list)

1. **Order is fixed.** Topic → research → PPT → **validate** → script → render →
   thumbnail. Never write the script or render before the deck is validated.
2. **Two gates, real stops.** GATE 1 (deck approved) and GATE 2 (script approved)
   are hard stops — wait for the creator.
3. **Git is the deliverable store.** Commit ppt/deck/script/research/video/
   thumbnail into the episode folder. Chat is for previews + decisions only.
4. **One theme.** Season 2 uses the dark systems-blueprint skin (`STYLE.md`).
   Don't restyle per episode.
5. **Teach, don't list.** One running example, one idea per scene, every concept
   shown as a building diagram, plain language, no jargon.
6. **Sourced facts only on screen.** No unverified numbers.
7. **Silent render.** VO is added in post; never bake narration into the video.
8. **Lint 0 errors** before any render.

---

## Commands cheat-sheet

```bash
# Lint a composition (must be 0 errors)
npx --yes hyperframes@0.7.5 lint                     # scans the project blocks dir
# Render a specific episode composition → silent MP4 (see PIPELINE.md for ffmpeg setup)
npx --yes hyperframes@0.7.5 render \
  -c system-design/ep-01-introduction-to-system-design/composition.html \
  -o renders/ep01.mp4 --fps 24 --quality standard --workers 4
ffmpeg -i renders/ep01.mp4 -c:v libx264 -crf 30 -preset medium -pix_fmt yuv420p \
  -movflags +faststart system-design/ep-01-…/video.mp4     # compress → commit this

# Thumbnail (constant series look; only --ep / --main / --micro change)
node thumbnails/render.mjs --ep "02" --main "Client & Server" \
  --micro "what really happens when you tap" \
  --out system-design/ep-02-…/thumbnail.png
```

(Preview a deck/scene by screenshotting the composition with headless Chrome,
seeking `window.__timelines["<id>"]` — see how previews were generated for Ep 1.)

---

## Definition of done (an episode is complete when…)
- [ ] `research.md` written, facts sourced.
- [ ] `composition.html` lints 0 errors, theme-correct, infographic-rich.
- [ ] `deck.html` exported and **validated** by the creator (GATE 1).
- [ ] `script.md` written, conversational, **approved** (GATE 2).
- [ ] composition re-timed to the script.
- [ ] `video.mp4` rendered (silent), compressed, committed.
- [ ] `thumbnail.png` generated (correct episode title), committed.
- [ ] episode `README.md` checklist updated; everything pushed to the episode folder.
