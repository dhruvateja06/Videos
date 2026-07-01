# The Tech Intern — System Design · SFX Philosophy

> **This is the WHY behind every sound-effect decision.**
> This doc defines the 5-sound palette this vertical already references in
> `WORKFLOW.md`'s folder layout (`audio_v2/sfx/` — whoosh, chime, zip, riser,
> swell) but has never had a philosophy written down for. Read this alongside
> `MOTION.md` before authoring any scene's audio cues, and before writing SFX
> placement into `sync_build.py`.

---

## Core principle

**SFX is a third teaching channel — parallel to narration and motion.**

Narration carries meaning. Motion carries structure and timing. SFX carries
*confirmation* — it tells the viewer's ear what the viewer's eye just saw,
or primes it for what's about to happen. In a monitoring-console aesthetic,
sound is also part of the *feel* of the system: a healthy system ticks along
quietly, a stressed one gets tense, a fixed one resolves cleanly.

The test for every SFX decision: *does this sound confirm something the
viewer needs to register, or build tension toward something that matters —
or is it just filling silence?*

If it's filling silence, cut it.

---

## What SFX actually does

**1. It confirms a reveal.**
When a hop box lights up, a latency number pops in, or a fix is shown, a
short `zip` or `chime` tells the brain: *that just happened, process it.*
Without SFX the eye catches it; with SFX the brain registers it. The
difference is retention.

**2. It builds tension.**
This vertical has a scene type the AI vertical doesn't: *"here's what
happens when this doesn't scale."* A `riser` under a load-spike sparkline,
building as the counter climbs toward the point it breaks, does something
narration alone can't — it makes the viewer *feel* the system straining
before Dhruva says the word "breaks."

**3. It signals transitions.**
`whoosh` on the scan-sweep tells the viewer we're moving to a new section.
The ear prepares for new information before the eye fully processes the new
layout — the same cognitive function as a paragraph break in text.

**4. It creates hierarchy.**
Because the 5 sounds carry different weight, the hierarchy of sounds should
map to the hierarchy of content: the single most important insight in a
scene gets `chime`. Secondary confirmations get `zip`. Section changes get
`whoosh`. Building tension gets `riser`. A sustained emotional beat (the fix
landing, or the outro) gets `swell`. The viewer learns this mapping within
the first episode or two and starts navigating by sound as much as by sight.

**5. It gives rhythm.**
In a dense diagram-build scene with many hops, SFX creates a pulse the
viewer can lock into — reducing the cognitive load of tracking every hop
visually, because the ear is doing some of that tracking too.

---

## The 5-sound palette

**One palette for the whole vertical. Don't add a sixth sound casually.**

Consistency is the point — viewers unconsciously learn what each sound means
across episodes. Adding one-off sounds per episode destroys that. These 5
names are already the convention referenced in `WORKFLOW.md`; this section
gives them a fixed meaning.

### `whoosh` — transitions
**Meaning:** we are moving to a new section.
**Use for:** the scan-sweep transition at a section boundary (see
`STYLE.md`). Major layout shifts.
**Never for:** individual element reveals inside a scene.
**Emotional register:** neutral, informational — the punctuation between
sections.

### `zip` — quick confirmation
**Meaning:** something appeared. Notice it.
**Use for:** a hop box popping in, a latency number landing, a secondary
label appearing. The most frequent sound — most reveals that need
*acknowledgement but not emphasis* get `zip`.
**Never for:** the most important moment in a scene (that's `chime`).
**Emotional register:** brisk, mechanical — a console confirming an event.

### `chime` — the key insight
**Meaning:** this is the point. Register it.
**Use for:** the most important moment in a scene — the payoff reveal, the
fix landing, the contrast the scene built toward. One `chime` per scene,
maximum. Often zero.
**Never for:** secondary elements, transitions, or anything that isn't the
single most important beat.
**Emotional register:** clarity, arrival — "that's the point."

### `riser` — building tension
**Meaning:** something is ramping up toward a threshold.
**Use for:** a load-spike sparkline drawing upward, a counter climbing
toward the number where the system breaks, any "and then it doesn't scale"
buildup. Ends right as the break/payoff moment lands (often handing off to
`chime` or a sharp cut to silence).
**Never for:** calm walkthrough scenes with no tension arc.
**Emotional register:** mounting pressure — the one sound that should make
the viewer lean in.

### `swell` — sustained emphasis
**Meaning:** let this moment breathe.
**Use for:** the fix being revealed and settling, the CTA/outro's close,
any moment that should linger rather than snap. Pairs with a `breathe()`
hold on the hero element, not a hard cut.
**Never for:** quick reveals or mid-scene transitions — it's the slowest,
most spacious sound in the palette.
**Emotional register:** resolution, warmth — the exhale after `riser`'s
inhale.

---

## The firing rules

### One sound per moment
Never fire two SFX simultaneously. If a `whoosh` and a `zip` would land at
the same timestamp, delay the `zip` by 0.1–0.2s so they're distinct.

### SFX fires with or just before the visual
Same rule as motion sync with narration (`MOTION.md`) — SFX should land at
or up to 0.05s before the event it confirms, never noticeably after.

### `chime` is scarce — zero or one per scene
If every reveal gets a `chime`, nothing is important. Across an 8–11 minute
episode, expect roughly one `chime` per scene at most, often none.

### `riser` needs a resolution
Never let a `riser` play out with no payoff — it must resolve into either a
`chime` (insight lands) or a hard cut to silence (the break itself, letting
the visual/narration carry the moment alone). A `riser` that just fades
without resolving reads as an anticlimax.

### Maximum density: one SFX every ~0.5s
If SFX fire faster than roughly twice a second, the scene is over-sonified.
Pull back — each sound needs space to register.

### Silence is a tool
Calm walkthrough scenes and the analogy/mental-model beats don't need SFX
density — let narration and the diagram build do the work. A quiet scene
after a `riser`-heavy one feels like breathing out.

---

## Scene-type SFX patterns

| Scene type | Typical SFX pattern |
|---|---|
| Hook / cold open | `whoosh` on enter · `zip` × 2–3 as key elements arrive · `chime` on the anchor headline |
| System walkthrough (normal load) | `whoosh` on scan-sweep into the scene · `zip` per hop as the packet crosses it |
| "This doesn't scale" | `riser` under the load-spike sparkline, building with the counter · resolves to a hard cut or `chime` at the break |
| The fix revealed | `chime` on the fix landing · `swell` under the settle/hold |
| Comparison / tradeoffs table | `zip` per row · `chime` on the standout row |
| Recap / practical takeaway | `zip` per checklist item, sparingly |
| CTA / outro | `chime` on the main line · `swell` under the close · then silence |

---

## What SFX should NOT do

**Don't sonify every element.**
Not every box-pop-in needs a `zip`. SFX fires on elements the viewer must
register to follow the explanation — background/ambient elements (the
living-background blooms, the HUD frame) get no sound.

**Don't use `whoosh` for individual element reveals.**
`whoosh` is spatial — it signals a section-level change. Using it for a
single hop box appearing is semantically wrong and sonically heavy.

**Don't substitute SFX for diagram clarity.**
If a scene needs SFX on every element to make sense, the diagram is
probably the problem. A well-structured request-path diagram is legible
without sound — SFX confirms, it doesn't explain.

**Don't let a `riser` run with no payoff.**
An unresolved `riser` is the single most jarring mistake in this palette —
it primes the viewer for a moment that never lands.

**Don't fire `chime` on things that aren't insights.**
If it fires on a decorative element or a secondary label, the viewer learns
to ignore it — and it won't land when it actually matters.

---

## Authoring SFX cues in the script/storyboard

Every scene should have an explicit SFX section wherever cues exist, written
like this:

```markdown
**SFX:**
- `whoosh` on scan-sweep entering this scene
- `zip` on each hop box as the packet arrives (one per hop, ~0.3s apart)
- `riser` under the load-spike sparkline, building over ~2s
- `chime` on "and that's when the cache saves you" reveal
```

Be specific: which element, how many, roughly how far apart. Vague notes
("some sound here") produce inconsistent `sync_build.py` implementations —
per `VOICEOVER.md`, SFX placement in the build script is explicit timestamp
math against the word-sync data, so the script is the spec it follows.

---

## The 6 pre-scene SFX questions

Before writing SFX cues for any scene, answer:

1. **What is the single most important moment?** — this gets `chime` (or
   nothing, if the narration carries it alone).
2. **Does this scene build tension toward a break/threshold?** — if yes,
   that's a `riser`, and it needs a resolution.
3. **What elements need quick confirmation?** — these get `zip`.
4. **Where does the scene change section?** — this gets `whoosh`.
5. **Is there a moment that should linger?** — this gets `swell`.
6. **Does any SFX fire within 0.5s of another?** — if yes, stagger or cut
   one.
