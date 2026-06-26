# The Tech Intern — Episode Production Workflow

> **READ THIS FIRST in every session that starts new episode work.**
> This is the canonical, locked-in process for producing an episode.
> Deviations cost hours. Stick to it.

## The 7 phases (1-screen summary)

| # | Phase | Output | User gate before next phase? |
|---|---|---|---|
| 1 | **Pick topic** | Episode # confirmed from `CURRICULUM.md` | ✅ Yes |
| 2 | **Content outline** | 1-page outline: 15 scenes, timings, examples, recurring metaphor | ✅ Yes |
| 3 | **Build deck + composition together** | `deck.html` (navigable) + `composition.html` (timed source) | — |
| 4 | **Deck validation** | User reviews `deck.html` slide-by-slide; iterate until greenlight | ✅ Yes (full greenlight, every slide) |
| 5 | **Narration script** | `script.md` — conversational voice, matches the validated deck | ✅ Yes |
| 6 | **Render video** | `video.mp4` + `outro.mp4` (near-lossless, compressed) | — |
| 7 | **Deliver** | All files in `episodes/epNN/`, committed and pushed | done |

**Hard rule:** never start phase N+1 until phase N's gate is explicitly approved. No "I'll go ahead and start while you review." That's the deviation that costs us.

---

## Folder structure (canonical)

```
tti-studio/
├── CLAUDE.md                     # session entry point — points to docs/
├── docs/                         # channel brain (don't put episode files here)
│   ├── BRAND.md                  # palette, fonts, voice/tone
│   ├── STYLE.md                  # motion-graphics rules
│   ├── PIPELINE.md               # HyperFrames technical workflow
│   ├── CURRICULUM.md             # 30-episode plan
│   └── WORKFLOW.md               # THIS FILE — production process
├── assets/                       # shared, never duplicated per-episode
│   ├── vendor/gsap.min.js
│   └── fonts/*.woff2
├── .claude/skills/               # project-scope skills (caveman, humanizer,
│                                 # infographic-builder, …)
├── episodes/                     # one folder per episode — ALL deliverables go here
│   ├── ep01/
│   │   ├── composition.html      # main HyperFrames composition (15 scenes, ~660s)
│   │   ├── composition-outro.html # 30s outro composition
│   │   ├── deck.html             # single-file navigable HTML deck
│   │   ├── script.md             # narration script (conversational)
│   │   ├── script.srt            # subtitle file (after recording)
│   │   ├── contact-sheet.png     # review stills sheet (optional)
│   │   ├── video.mp4             # final main video (near-lossless CRF 20)
│   │   ├── outro.mp4             # final outro video
│   │   └── youtube.md            # title + description + tags (post-record)
│   ├── ep02/ …
│   └── ep03/ …
└── renders/                      # gitignored — raw render staging only
```

**Two things stay shared, everything else is per-episode:**
- `assets/` — fonts + GSAP, used by every composition
- `docs/` — the channel brain
- `.claude/skills/` — skills

**Anything that belongs to a specific episode lives in `episodes/epNN/`.** No more scattering across `compositions/`, `scripts/`, `decks/`, `deliverables/`. That structure caused the deviations.

---

## Phase 1 — Pick topic

1. Open `docs/CURRICULUM.md`, find the next episode in the table.
2. Confirm the topic + difficulty + dependencies with the user.
3. **Gate:** user says "yes, EP03 it is."

That's the whole phase. Don't over-engineer it.

---

## Phase 2 — Content outline

The point: agree on *what the episode covers* before writing on-screen words or narration.

1. Build a 1-page outline:
   - **Episode title** (from curriculum, may refine)
   - **The big idea** — the one mental unlock the viewer leaves with
   - **15-scene map** — each scene's purpose, timing, what's on screen (1-line each), and the Indian/everyday example anchored to it
   - **Recurring metaphor** — pulled from the table in `CURRICULUM.md` ("Rules vs Patterns", "Downhill walker", etc.) and where it's introduced/reused
   - **Cliffhanger to next episode**
2. Apply the **teaching discipline** in `CURRICULUM.md` (4-beat pattern, plain language rules, Indian example matrix).
3. Send outline to user.
4. **Gate:** user approves outline. May request topic shifts, example swaps, scene reordering.

**Why this phase exists:** without it, we end up writing 600 lines of HTML and a 2,000-word script around the wrong angle. Outline is cheap, HTML is expensive.

---

## Phase 3 — Build deck + composition together

Both files share ~95% of the same HTML markup — build them in parallel to avoid drift.

1. Read `docs/STYLE.md` and the `infographic-builder` skill before writing visuals. They encode the patterns.
2. Create the new episode folder: `episodes/epNN/`.
3. Build `episodes/epNN/composition.html`:
   - 15 scenes, total 660s (~11 min)
   - Living background, wipes, breathing holds, building diagrams
   - `data-composition-id="epNNfull"`
   - Use the helper functions (`scene/head/kick/rise/pop/cellL/cellR/breathe/floaty/wipe`) from a previous episode as the starting kit
   - Asset paths: `<script src="../../assets/vendor/gsap.min.js">`, `src:url("../../assets/fonts/...")` (two `../` because the file is now two levels deep)
4. Build `episodes/epNN/deck.html` from the same scenes:
   - Standalone single-file, Google Fonts CDN
   - Same visuals as the composition but no GSAP timeline
   - Keyboard nav (arrows, space, F, 1-9), click-to-advance, slide counter, deep-link hash
   - Same boilerplate as `ep02/deck.html`
5. `cd tti-studio && npx hyperframes lint` — must pass 0 errors on the new files.

**Do not render the video yet.** The deck is what the user validates first.

---

## Phase 4 — Deck validation

The deck is the cheap unit of feedback. Get it right *before* the 40-minute render commits.

1. Push deck.html, send the GitHub raw URL.
2. (Optional but recommended) Render a contact sheet:
   - `npx hyperframes render -c episodes/epNN/composition.html -o renders/_epNN-sheet.mp4 --fps 1 --quality draft --workers 4` (~5 min)
   - Extract one PNG per scene at the visually-settled time
   - Tile into a 5×3 grid → `episodes/epNN/contact-sheet.png`
   - Send to user
3. User reviews **slide by slide**. Common feedback dimensions:
   - **Wording** — too long, jargon-y, unclear
   - **Density** — too packed or too sparse
   - **Examples** — Indian anchors right for the layer/concept
   - **Visual hierarchy** — eye drawn to the right element
4. Apply edits. Re-render only the changed contact-sheet stills (not the full video).
5. **Gate:** user explicitly says "approved, all 15 slides good." Single-sentence ambiguous "looks fine" doesn't count.

---

## Phase 5 — Narration script

The script gets written **after** the visuals are validated, so the words serve the visuals (not the other way around).

1. Read the validated `deck.html` slide by slide.
2. Draft `episodes/epNN/script.md` in **conversational voice**:
   - Spoken rhythm (short / short / long / short) — not paragraph prose
   - Asides in dashes, rhetorical questions, self-corrections, direct address
   - One `▸` marker per visual reveal (matches the deck's click points)
   - Pacing for ~150–170 wpm
   - Add a "delivery notes" footer with pace/tone cues
3. **Apply the `humanizer` skill** before sending — strips AI-writing tells (em-dash overuse, rule of three, AI vocab, vague attributions).
4. Send script for review.
5. **Gate:** user approves tone & wording. Iterate any sections that read stiff.

---

## Phase 6 — Render video

Mechanical phase. Don't reach here until phases 4 and 5 are both greenlit.

1. Lint: `npx hyperframes lint` — 0 errors on the episode's files.
2. Render main video — in background:
   ```bash
   cd tti-studio && export PATH="/usr/local/bin:$PATH"
   ../tech-intern-videos/node_modules/.bin/hyperframes render \
     -c episodes/epNN/composition.html \
     -o renders/epNN-full.mp4 \
     --fps 24 --quality standard --workers 4
   ```
3. Render outro: same command on `composition-outro.html` → `renders/epNN-outro.mp4`.
4. Compress near-lossless to deliverables:
   ```bash
   ffmpeg -y -i renders/epNN-full.mp4 \
     -c:v libx264 -profile:v high -pix_fmt yuv420p \
     -crf 20 -preset medium -movflags +faststart -an \
     episodes/epNN/video.mp4
   ```
   Repeat for outro.
5. **QA:** extract a few key frames with `ffprobe` / `ffmpeg -ss`. Verify the signature visual + any phone mockups + the recap.
6. **⏱️ Pacing QA (Ep 1 lesson — do not skip):** scrub each scene. If a scene is
   visually *done* with more than ~15% of its time left, the reveals are bunched
   at the start and will fall out of sync with the voiceover. Re-space them across
   the scene's full narration length before the final render. See `STYLE.md` →
   "Pacing & narration sync".

---

## Phase 7 — Deliver

1. `git add episodes/epNN/`
2. Commit with a clear message naming the episode + what's inside.
3. Push to `claude/gifted-brown-7e7t72` (the dev branch).
4. Reply with GitHub download URLs for each deliverable:
   - `https://github.com/dhruvateja06/videos/blob/claude/gifted-brown-7e7t72/tti-studio/episodes/epNN/video.mp4`
   - `…/script.md`, `…/deck.html`, `…/outro.mp4`, etc.

---

## Common deviations to avoid

| Deviation | Why it bit us before | What to do instead |
|---|---|---|
| Writing narration script before the deck is validated | We had to rewrite the script after content changed — 2× the work | Outline → deck → script. Never script first. |
| Building the composition without showing the deck for review | 40 min of render wasted on content that needed wording changes | Always send deck (or contact sheet) for validation first |
| Scattering files across `compositions/`, `scripts/`, `decks/`, `deliverables/` | Hard to find what belongs to which episode | Everything in `episodes/epNN/` |
| Re-rendering the whole video to fix one scene | The moving background means partial-range renders are seamless-broken | Lint + QA the composition before render, not after |
| Using cinematic AI-generated b-roll | Wrong format for the channel | Infographic / motion-graphics only (see `STYLE.md`) |
| Writing on-screen text in long sentences | Reads like slides, not infographics | Headlines ≤7 words, bullets as fragments |
| **Animations bunched at the start of a scene** | **Ep 1: a ~60s scene finished all its animation by ~35s, then froze while the voiceover kept reading — badly out of sync** | **Spread reveals across the scene's full narration length (~1 every 5–8s); the last reveal lands near the end. See `STYLE.md` → "Pacing & narration sync".** |
| **Scripts that read like written paragraphs** | **Ep 1 short: the hook was dense prose, named "system design" too early, and was em-dash heavy — robotic and hard to teleprompt** | **Spoken rhythm: short lines, one thought per breath; show the scenario and build to the concept before naming it; run the `humanizer` skill (Phase 5). Read it out loud — if it doesn't sound like talking, rewrite.** |

---

## Quality gates (what each phase must produce before the next can start)

| Gate | Looks like |
|---|---|
| **1→2** | "Yes, EP03." |
| **2→3** | "Outline approved. Go build the deck." |
| **3→4** | Lint passes, deck.html opens cleanly in a browser, all 15 slides render |
| **4→5** | "Approved, all 15 slides good — go write the script." |
| **5→6** | "Script approved. Render the video." |
| **6→7** | Video probe shows 660s @ 24fps, key QA frames inspected, file size sane |

If the gate isn't met, you're not done with the phase. Don't move on.
