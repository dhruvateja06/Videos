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
