# The Tech Intern — System Design · Motion-Graphics Style

> The look that separates our videos from a slideshow. Every episode must feel
> like an **animated infographic explainer**, NOT slides exported to video, and
> NOT cinematic AI b-roll. The *information* is the visual; motion keeps the eye
> glued for retention. This vertical uses the **Engineer's Terminal** palette
> (see `BRAND.md`): deep navy, cobalt hero, mono annotations.

## The core rule

**No frame is ever frozen, and no cut is ever to a blank screen.** A static deck
loses viewers. If you ever catch the composition doing "fade in → show bullets →
fade to blank → next slide," stop — that's the failure mode.

## The motion language (use all of these)

1. **Living background (always moving), spans the whole composition.**
   A drifting **blueprint dot/line grid** + two slow, soft **cobalt light-blooms**
   that drift and scale on long loops, over the deep-navy paper. It is NOT a clip
   (not gated) — it runs 0→end so it bridges every scene cut and nothing is ever
   still.

2. **Scan-sweep transitions at major section cuts.**
   A thin **cobalt scan line** sweeps across *over* the scene swap, masking the
   cut (a monitoring-console wipe, not the AI vertical's orange bar). Use at
   section boundaries, not every scene.

3. **Kinetic headline reveals.**
   Headlines (Fraunces 600) rise in with an overshoot ease (`back.out`) + a slight
   push-in (scale 0.95→1), not a plain opacity fade. Scenes **exit with motion**
   too (rise + slight scale), never a flat fade-to-nothing. Hard-kill each clip's
   exit (`tl.set(sel,{opacity:0}, end)`) so seeking stays clean.

4. **Breathing / float on hero elements during long holds.**
   A 30–50s narration hold must not freeze. Hero elements get slow perpetual loops
   (scale ±2–4%, y ±10–16px): the request packet pulses, a node glows, a counter
   ticks. Subtle.

5. **Diagrams that BUILD, not appear** — the heart of this vertical:
   - **Boxes pop in** with stagger; **edges draw on** (`stroke-dashoffset`).
   - The **request packet travels** the path (animate `cx/cy` along the wire).
   - Latency numbers **pop in on the beat** as the packet crosses each hop.
   - Sparklines **draw on** flat→spiky; before/after panels **slide in** L/R.

6. **Animated number counters.**
   Count-ups (qps, concurrent users, `ms`) via a GSAP `onUpdate` writing
   `textContent` — seek-safe in HyperFrames. **Always set the DOM's initial text
   to the final value** as a fallback, so a missed update still shows correct.

## Standard diagram primitives (build a small kit, reuse every episode)

These are this vertical's vocabulary — standardize them so episodes compound:

- **Request packet** — a small `--accent-bright` dot/pill travelling a path
  between components, with a `stroke-dasharray` trail. The signature motion.
- **Hop box** — rounded rect (`--panel` fill, `--hair` border, mono label like
  `LOAD BALANCER`), with a monoline **icon** (client / CDN / LB / cache / server /
  database cylinder). Border lights cobalt when "active".
- **Latency annotation** — mono `+NN ms` that pops above a hop as the packet
  crosses; a running total assembles at the end.
- **Load-spike sparkline** — a small line chart, flat then spiking, drawn in
  `--spike` red; pair with a count-up.
- **Architecture box-and-arrow** — the staple; arrows draw on, one idea per arrow.
- **Before/after split** — left vs right (monolith/microservices, 1 server/fleet);
  the "bad" side dims, the "good" side glows cobalt.
- **Live dashboard counter** — qps / users ticking up, `--ok` green while healthy,
  flicking `--spike` red when it crosses a threshold (then the fix is shown).
- **HUD frame** — thin top bar (`THE TECH INTERN // SYSTEM DESIGN … S· E0N`) +
  corner brackets. The console feel; replaces the AI vertical's left spine.

## Teaching shape (per episode)

- **One running example threaded through** the whole episode (don't dump
  definitions). Each concept attaches to that example as it comes up.
- **One idea per scene**; reveal ~one new element every 5–8s to match a calm read.
- Each scene **held long enough to narrate over** (silent render; VO added later).
- Plain language, no jargon, Indian examples first (see `BRAND.md`).

## ⏱️ Pacing & narration sync — the #1 timing rule (Ep 1 got this wrong)

**The failure mode (do NOT repeat):** in Ep 1, every reveal in a scene fired in
the first ~half — a 60s scene finished all its animation by ~35s, then sat frozen
while the voiceover kept reading. Dead air. The motion has to track the *words*,
not race ahead of them.

**The rule:** within each scene, **spread the element reveals evenly across the
scene's full narration length** so each build lands roughly when the voice reaches
that point, and the *last* element arrives near the *end* of the scene's spoken
lines — not at 60% of the way through.

**How to time it concretely:**
1. Take the scene's narration (its lines in `script.md`), count words → spoken
   seconds at **~145 wpm** (`words / 145 × 60`). That is the scene's duration.
2. The scene **enter** takes the first ~0.9s; reserve the **last ~12–15%** as a
   settled hold.
3. Distribute the N reveals across the middle: reveal *i* at roughly
   `enter + (i / N) × (duration − enter − hold)`. So a 60s scene with 4 reveals
   fires at ≈ **8s, 22s, 36s, 50s** — *not* 3s, 5s, 7s, 9s.
4. Each reveal aligns to one `▸` marker in the script (one marker per reveal), so
   the visual lands on the spoken beat.
5. Hero elements **breathe/float** during the hold so even the settled tail is
   never frozen.

**Check before render:** scrub the composition — if a scene is visually *done*
with more than ~15% of its time left, the reveals are bunched. Re-space them.

## What we are NOT doing

- ❌ Cinematic / AI-generated b-roll footage (wrong format, expensive, imprecise).
- ❌ One-line-per-slide decks (can't hold attention for minutes).
- ❌ Headlines longer than ~7 words; bullets are fragments, not sentences.
- ❌ On-screen animation directions in the teleprompter script (keep the read
  clean; see `PIPELINE.md` / `WORKFLOW.md`).

## Thumbnails (series system)

Thumbnails are a **template**, not a one-off, so the series is recognizable on the
channel page (`thumbnails/` template + render script; PNGs live in the episode
folder per `WORKFLOW.md`).

- **Constant (series identity):** the big **SYSTEM DESIGN** title, the request-path
  / client→server→database diagram, the `THE TECH INTERN // SYSTEM DESIGN` tag, and
  the Engineer's-Terminal palette.
- **Per-episode (only these change):** the episode number + the **topic line**
  (the actual episode title), and a ≤7-word hook.
- **Format:** 1280×720 rendered @2x, in this vertical's dark skin so the thumbnail
  matches the video.
