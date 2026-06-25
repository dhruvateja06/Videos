# The Tech Intern — Motion-Graphics Style

> The look that separates our videos from a slideshow. Every episode must feel
> like an **animated infographic explainer**, NOT slides exported to video, and
> NOT cinematic AI b-roll. The *information* is the visual; motion keeps the eye
> glued for retention.

## The core rule

**No frame is ever frozen, and no cut is ever to a blank screen.** A static
deck loses viewers. If you ever catch the composition doing "fade in → show
bullets → fade to blank → next slide," stop — that's the failure mode we fixed.

## The motion language (use all of these)

1. **Living background (always moving), spans the whole composition.**
   A drifting dot-grid + two slow, soft **orange light-blooms** that drift and
   scale on long loops. It is NOT a clip (not gated) — it runs 0→end so it bridges
   every scene cut and nothing is ever still.

2. **Wipe transitions at major section cuts.**
   An orange bar sweeps across the screen *over* the scene swap, masking the cut
   instead of cutting to blank cream. Use at section boundaries, not every scene.

3. **Kinetic headline reveals.**
   Headlines rise in with an overshoot ease (`back.out`) + a slight push-in
   (scale 0.95→1), not a plain opacity fade. Scenes **exit with motion** too
   (rise up + slight scale), never a flat fade-to-nothing.

4. **Breathing / float on hero elements during long holds.**
   A 40–55s narration hold must not freeze. Hero elements get slow perpetual
   loops: the phone hovers, the "model" box and the **PATTERNS** word pulse, the
   prediction dot throbs, the title accent glows. Subtle (scale ±3–4%, y ±10–16px).

5. **Diagrams that BUILD, not appear.**
   - Scatter dots **drop in** with stagger.
   - The best-fit line **draws on** (animate `stroke-dashoffset`).
   - Table rows **slide in directionally** (old-way from left, AI from right).
   - Prediction crosshair **traces** up to the line and across to the axis.

6. **Animated number counters.**
   Count-ups (e.g. the Swiggy timer 8 → 32 min) via a GSAP `onUpdate` that writes
   `textContent`. This **is** seek-safe in HyperFrames (verified). Always set the
   DOM's initial text to the **final** value as a fallback, so a missed update
   still shows the correct number.

## Pacing (for narration-ready silent renders)

- Each scene is **held long enough to talk over** (the creator adds voiceover after).
- Element reveals inside a scene are spaced to match a calm read (~one new idea
  every 5–8 seconds), so the visual lands just before/with the spoken point.
- Episode 1 = 660s (11:00) across 16 scenes. Use that as the density baseline.

## Reference implementation

`compositions/ep01-full.html` is the canonical example of all of the above
(background, wipes, kinetic type, breathing, building diagrams, the count-up).
Copy its `<style>` tokens and the GSAP helper functions
(`scene/head/kick/rise/pop/cellL/cellR/breathe/floaty/wipe`) as the starting kit
for any new episode.

## What we are NOT doing

- ❌ Cinematic / AI-generated b-roll footage (wrong format, expensive, imprecise).
- ❌ One-line-per-slide decks (can't hold attention for minutes).
- ❌ On-screen animation descriptions in the teleprompter script (confuses the
  live read — keep the script clean; see `PIPELINE.md`).

---

## Per-season "skins" (same motion language, different look)

The motion language above (living bg, wipes, kinetic type, breathing, diagrams
that build, counters) is **shared by every season**. Each season gets its own
**skin** — palette + typography + signature motif — so seasons don't blur
together. The skin changes; the discipline doesn't.

### Season 1 — AI · "warm editorial"
Cream `--paper #FAF8F3`, brand orange `--o #FF6B2C`, **Fraunces** serif
headlines + Inter, left orange spine bar, scatter-plot / best-fit-line motif.
Reference: `compositions/ep01-full.html`.

### Season 2 — System Design (HLD) · "dark systems-blueprint"
Deliberately the **opposite** of S1's warm editorial look (a different season
must not look like the last one). Reference: `compositions/sd-ep01-full.html`.

| Token | Hex | Use |
|---|---|---|
| `--bg`    | `#0E1420` | deep navy canvas |
| `--panel` | `#161E2E` | card / node fill |
| `--node`  | `#16233A` | diagram node fill |
| `--ink`   | `#E8EFF7` | primary text (cool near-white) |
| `--soft`  | `#A7B8CC` | secondary text |
| `--muted` | `#5F7287` | mono labels, captions |
| `--hair`  | `rgba(125,170,210,.18)` | grid lines, borders, edges |
| `--cyan`  | `#2DD4BF` | **primary accent** (the hero colour) |
| `--cyanb` | `#5EEAD4` | bright cyan — glows, big numbers |
| `--o`     | `#FF6B2C` | brand orange kept as the **secondary "hot"** accent (the DB, the danger, the one critical highlight) |

- **Typography:** **Inter** for headlines (700, tight) and body — **no serif**
  (that's S1's signature). **JetBrains Mono** for eyebrows (`// LIKE THIS`),
  node labels, captions, and big count-up numbers (monospace digits read techy).
- **Signature frame (replaces the orange spine):** a top HUD bar
  (`THE TECH INTERN // SYSTEM DESIGN … S2 · E01`) over a hairline, plus blueprint
  **corner brackets**. Section cuts use a **cyan scan-sweep** (not the orange wipe).
- **Signature motif = boxes & arrows** (because that *is* HLD): blueprint
  micro-grid background, nodes that pop in, edges that **draw on**
  (`stroke-dashoffset`), and **packets** (small cyan dots) flowing along edges.
- **Orange discipline:** still one or two hot accents per scene — now it marks
  the *thing that matters* (the database of record, an overloaded/failing box),
  against the cool cyan field.

> Brand DNA preserved: orange is still present, the typography is still
> disciplined, and the "no frozen frame / no cut to blank" rule still governs —
> so it's unmistakably *The Tech Intern*, just a different season.

### Season 3 — LLD · skin TBD
Will need its own skin (code is on screen) — decide when S3 production starts.

---

## Thumbnails (series system)

Thumbnails are a **template**, not a one-off, so the whole series is recognizable
on the channel page. System in `thumbnails/` (template + `render.mjs`); rendered
PNGs in `assets/thumbnails/`.

- **Constant across every episode** (series identity): the big **SYSTEM DESIGN**
  title, the client→server→database diagram, the `THE TECH INTERN // SYSTEM
  DESIGN` tag, and the dark navy + cyan + orange palette.
- **Per-episode (only these change):** the episode number and the **topic line**
  (Ep 1 = "The Fundamentals", Ep 2 = "Client & Server", …) + a one-line hook.
- **Format:** 1280×720 rendered @2x (2560×1440), built in the Season-2
  dark-blueprint skin so the thumbnail matches the video frame-for-frame.
- New episode = one command (`node thumbnails/render.mjs --ep … --main … --micro …`);
  see `thumbnails/README.md`.
