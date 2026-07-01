# The Tech Intern — System Design · Video Studio

> **This is the System Design vertical** of *The Tech Intern*. The **AI vertical**
> lives on branch `claude/gifted-brown-7e7t72` — its docs are a structural
> reference only; never mix its cream/orange look into this vertical.
>
> **NEW SESSION? READ THESE IN ORDER:**
>
> 1. **`docs/WORKFLOW.md`** — ⭐ **THE EPISODE PRODUCTION PROCESS.**
>    The 8 phases (topic → outline → script → deck → validate → render → voiceover → deliver),
>    the gates between them, the per-episode folder structure. **Follow this
>    every time. Don't deviate.** Deviations cost hours and trigger
>    "we already did this differently last time" feedback.
> 2. **`docs/BRAND.md`** — audience, voice/tone, exact palette & fonts
>    (Engineer's Terminal: deep navy `#0F1729` + cobalt `#3B7BFF`).
> 3. **`docs/STYLE.md`** — the motion-graphics style (living bg, scan-sweeps,
>    request-path diagrams, building infographics). Keeps videos from looking
>    like slides.
> 4. **`docs/MOTION.md`** — ⭐ **MOTION PHILOSOPHY.** The WHY behind every
>    animation choice — how motion serves comprehension, the animation
>    hierarchy (structural → comprehension → emphasis → section transition),
>    restraint rules, emotional palette per scene type. Read before authoring
>    any GSAP.
> 5. **`docs/SFX.md`** — ⭐ **SFX PHILOSOPHY.** The WHY behind every sound
>    cue. Defines the 5-sound palette (`whoosh`/`chime`/`zip`/`riser`/`swell`)
>    referenced in `WORKFLOW.md`'s folder layout, what each one means, firing
>    rules, and scene-type patterns. No gain values calibrated yet — set
>    those when the sound files are first generated/recorded, the same way
>    the AI vertical did in `DESIGN.md §7.2`. Read before writing SFX cues in
>    the script or `sync_build.py`.
> 6. **`docs/PIPELINE.md`** — HyperFrames render technical details: commands,
>    gotchas, asset paths, compression + delivery.
> 7. **`docs/CURRICULUM.md`** — the 30-episode System Design plan, recurring
>    metaphors, Indian-example matrix, the teaching discipline.
> 8. **`docs/VOICEOVER.md`** — ElevenLabs word-sync pipeline (voice settings,
>    beat maps, sync_build.py reference, SFX mixing).
> 9. **`docs/LOCAL-SETUP.md`** — one-time local Claude Code + ElevenLabs setup
>    (needed for voice generation, which the cloud sandbox can't do).
>
> **TL;DR of this vertical:** *The Tech Intern — System Design* — faceless,
> beginner-first explainers of how real systems scale. We render **silent**
> motion-graphics episodes with HyperFrames (HTML/CSS + GSAP → MP4), then add
> the creator's **Dhruva voice** (ElevenLabs) with **word-level sync** so every
> animation lands on the spoken word. Cobalt `#3B7BFF` on deep navy `#0F1729`.
> Infographic/motion-graphics style, **never** slideshow, **never** cinematic
> AI b-roll. Signature motif: the animated request-path diagram.
>
> **All episode files live in `episodes/epNN/`** (per `WORKFLOW.md`). Never put
> episode files in top-level `compositions/`, `scripts/`, `decks/`,
> `deliverables/` — those folders are not used here.

---

# HyperFrames Composition Project

## Skills — USE THESE FIRST

**Always invoke the relevant skill before writing or modifying compositions.** Skills encode framework-specific patterns (e.g., `window.__timelines` registration, `data-*` attribute semantics, shader-compatible CSS rules) that are NOT in generic web docs. Skipping them produces broken compositions.

**Doing anything with HyperFrames?** Start at `/hyperframes` — it routes every "make me a video" intent to the right skill or workflow. The project-scope skills bundled here: `infographic-builder` (diagram/infographic patterns), `humanizer`, `caveman`, `karpathy-guidelines`, `find-skills`.

> **Skills not available or need updating?** Run `npx skills add heygen-com/hyperframes`
> and restart the agent session so the new skills load.

## Commands

```bash
npm run dev          # preview server (long-running — run with run_in_background:true)
npm run check        # lint + validate + inspect
npm run render       # render to MP4
npx hyperframes docs <topic>    # local reference docs (no network)
```

> **`npm run dev` is a long-running server.** In Claude Code always run it with
> `run_in_background: true`; never as a foreground command (it will time out).

## Project Structure

- `episodes/epNN/` — **everything for one episode** (composition.html, deck.html,
  script.md, research.md, video.mp4, thumbnail.png). `paths.blocks` = `episodes`.
- `docs/` — the channel brain (read order above).
- `assets/` — bundled fonts + GSAP (no CDN; the renderer has no network).
- `.claude/skills/` — project-scope skills.
- `index.html` — root composition / brand-intro test.
- `thumbnails/` — the series thumbnail template + render script (per `STYLE.md`).

## Linting — ALWAYS RUN AFTER CHANGES

After creating or editing any `.html` composition, run `npm run check` and fix all
errors before presenting. Review inspect warnings before rendering.

## Key Rules

1. Every timed element needs `data-start`, `data-duration`, `data-track-index`.
2. Elements with timing **MUST** have `class="clip"` (visibility control).
3. Timelines are paused and registered on `window.__timelines["composition-id"]`.
4. Videos use `muted` + a separate `<audio>` element for audio.
5. Sub-compositions referenced via `data-composition-src="…"`.
6. Only deterministic logic — no `Date.now()`, no `Math.random()`, no network fetches.
7. **Never `-movflags +faststart`** in any ffmpeg mux — corrupts H.264 on this Mac. See `docs/PIPELINE.md`.
8. **Never a CSS `@keyframes` animation and a GSAP tween on the same element's `transform`** — they fight every paint; invisible while scrubbing live, shows as a tearing artifact in rendered frames. Drive ambient motion with GSAP alone. See `docs/PIPELINE.md`.
9. **Multi-step scenes (Step 1 → Step 2 → …) get one persistent header + crossfade, not a `wipe()`/cut per step** — a wipe per step reads as a new scene each time. See `docs/PIPELINE.md`.
10. **`lint`/`validate`/`snapshot` need a directory (project root), not a file path** — `render -c <path>` is the one that accepts a specific composition file. See `docs/PIPELINE.md` for the verification workflow via `project-root-preview` in `.claude/launch.json`.
