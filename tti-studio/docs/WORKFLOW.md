# The Tech Intern — Episode Production Workflow

> **READ THIS FIRST in every session that starts new episode work.**
> This is the canonical, locked-in process for producing an episode.
> Deviations cost hours. Stick to it.

## The 8 phases (1-screen summary)

| # | Phase | Output | User gate before next phase? |
|---|---|---|---|
| 1 | **Pick topic** | Episode # confirmed from `CURRICULUM.md` | ✅ Yes |
| 2 | **Content outline** | 1-page outline: 15 scenes, timings, examples, recurring metaphor | ✅ Yes |
| 3 | **Narration script (the storyboard)** | `script.md` — narration + `▸` visual cues + explicit SFX cues per scene | ✅ Yes |
| 4 | **Build deck + composition together** | `deck.html` (navigable) + `composition.html` (timed source) — built *from* the approved script | — |
| 5 | **Deck validation** | User reviews `deck.html` slide-by-slide against the script; iterate until greenlight | ✅ Yes (full greenlight, every slide) |
| 6 | **Render video (silent)** | `video.mp4` + `outro.mp4` (near-lossless, compressed) | — |
| 7 | **Voiceover & word-sync** | `video-voiced.mp4` + `outro-voiced.mp4` (Dhruva voice, animations land on the words) | — |
| 8 | **Deliver** | All files in `episodes/epNN/`, committed and pushed | done |

**Hard rule:** never start phase N+1 until phase N's gate is explicitly approved. No "I'll go ahead and start while you review." That's the deviation that costs us.

**Script before visuals.** The narration script IS the storyboard — every scene's
wording, visual reveals, and SFX cues are decided there first. The deck and
composition are built *to match the approved script*, not the other way
around. Building visuals before the script locks scene lengths and wording
to whatever the HTML happened to have — then the script has to bend around
it, and usually the composition needs a rebuild anyway.

---

## Folder structure (canonical)

```
tti-studio/
├── CLAUDE.md                     # session entry point — points to docs/
├── docs/                         # channel brain (don't put episode files here)
│   ├── BRAND.md                  # palette, fonts, voice/tone
│   ├── STYLE.md                  # motion-graphics rules
│   ├── MOTION.md                 # animation philosophy — why, not just how
│   ├── SFX.md                    # sound-effect philosophy + the 5-sound palette
│   ├── PIPELINE.md               # HyperFrames technical workflow
│   ├── VOICEOVER.md              # ElevenLabs word-sync pipeline
│   ├── LOCAL-SETUP.md            # local Claude Code + ElevenLabs setup
│   ├── CURRICULUM.md             # 30-episode plan
│   └── WORKFLOW.md               # THIS FILE — production process
├── assets/                       # shared, never duplicated per-episode
│   ├── vendor/gsap.min.js
│   └── fonts/*.woff2
├── .claude/skills/               # project-scope skills (caveman, humanizer,
│                                 # infographic-builder, …)
├── episodes/                     # one folder per episode — ALL deliverables go here
│   ├── ep01/
│   │   ├── script.md                  # narration + visual cues + SFX cues — written FIRST
│   │   ├── composition.html           # main HyperFrames composition (silent source)
│   │   ├── composition-outro.html     # outro composition (silent source)
│   │   ├── composition_synced.html    # re-timed, word-synced render source
│   │   ├── composition-outro_synced.html  # re-timed outro render source
│   │   ├── deck.html                  # single-file navigable HTML deck
│   │   ├── sync_build.py              # voiceover + word-sync pipeline (see VOICEOVER.md)
│   │   ├── audio_v2/                  # TTS clips + alignment cache (GITIGNORED)
│   │   │   └── sfx/                   # SFX files (whoosh, chime, zip, riser, swell)
│   │   ├── script.srt                 # subtitle file (after recording)
│   │   ├── video.mp4                  # silent render (near-lossless CRF 20)
│   │   ├── outro.mp4                  # silent outro render
│   │   ├── video-voiced.mp4           # ⭐ final voiced deliverable (Dhruva, word-synced)
│   │   ├── outro-voiced.mp4           # ⭐ final voiced outro
│   │   ├── short/short.mp4            # YouTube Short recap
│   │   └── youtube.md                 # title + description + tags
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

**Why this phase exists:** without it, we end up writing a script and 600 lines of HTML around the wrong angle. Outline is cheap, script is cheaper than HTML, HTML is expensive.

---

## Phase 3 — Narration script (the storyboard)

The script is written **right after the outline, before any HTML.** It is not
just narration — it's the full storyboard: what's said, what's shown, and
what's heard, scene by scene. The deck and composition get built *from* this
document, so anything vague here becomes a guess later.

1. Draft `episodes/epNN/script.md` in **joyful, conversational voice** — warm, slightly excited, like a teacher who genuinely loves the material:
   - Spoken rhythm (short / short / long / short) — not paragraph prose
   - Asides in dashes, rhetorical questions, self-corrections, direct address
   - Pacing for ~145–170 wpm
2. For every scene, write it as a full storyboard beat:
   - Narration text
   - `▸` markers at each visual reveal, with a bracketed description of what appears — specific enough that Phase 4 can build it without guessing (e.g. `▸ [SERVER box appears, pulses once]`, not `▸ [something happens]`)
   - An explicit **SFX cue block** per scene wherever cues exist, per `SFX.md`'s format:
     ```markdown
     **SFX:**
     - `whoosh` on scan-sweep entering this scene
     - `zip` on each hop box as the packet arrives (one per hop, ~0.3s apart)
     - `chime` on "and that's when the cache saves you" reveal
     ```
     Read `SFX.md`'s 6 pre-scene questions before writing these — vague notes
     ("some sound here") produce inconsistent `sync_build.py` implementations.
   - Read `MOTION.md` before describing reveals — it decides *which* motion
     tier a beat deserves (structural / comprehension / emphasis), not just
     that something should move.
3. Add a "delivery notes" footer with pace/tone cues.
4. **Apply the `humanizer` skill** before sending — strips AI-writing tells (em-dash overuse, rule of three, AI vocab, vague attributions).
5. Send script for review.
6. **Gate:** user approves tone, wording, visual cues, and SFX cues. Iterate any sections that read stiff or under-specified.

**Why this phase exists:** building visuals before the script locks scene
lengths and structure to whatever the HTML happened to have — the script
then bends around it, and the composition usually needs a rebuild anyway.
Writing the full storyboard here means Phase 4 is mechanical translation,
not design-while-building.

---

## Phase 4 — Build deck + composition together

Both files share ~95% of the same HTML markup — build them in parallel to avoid drift. **Build directly from the approved `script.md`** — every scene's visuals, timing, and SFX cues are already decided; this phase translates them into HTML, it doesn't invent them.

1. Read `docs/STYLE.md`, `docs/MOTION.md`, and the `infographic-builder` skill before writing visuals. They encode the patterns.
2. Create the new episode folder: `episodes/epNN/` (script.md already lives here from Phase 3).
3. Build `episodes/epNN/composition.html`:
   - One scene per `script.md` scene, same count, same order
   - Scene duration matches the narration length implied by the script (word count ÷ target wpm), not an arbitrary round number
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

## Phase 5 — Deck validation

The deck is the cheap unit of feedback. Get it right *before* the 40-minute render commits.

1. Push deck.html, send the GitHub raw URL.
2. (Optional but recommended) Render a contact sheet:
   - `npx hyperframes render -c episodes/epNN/composition.html -o renders/_epNN-sheet.mp4 --fps 1 --quality draft --workers 4` (~5 min)
   - Extract one PNG per scene at the visually-settled time
   - Tile into a 5×3 grid → `episodes/epNN/contact-sheet.png`
   - Send to user
3. User reviews **slide by slide**, checked against the script. Common feedback dimensions:
   - **Fidelity to the script** — does the deck show what the script's `▸` cues describe?
   - **Density** — too packed or too sparse
   - **Examples** — Indian anchors right for the layer/concept
   - **Visual hierarchy** — eye drawn to the right element
4. Apply edits. Re-render only the changed contact-sheet stills (not the full video).
5. **Gate:** user explicitly says "approved, all 15 slides good." Single-sentence ambiguous "looks fine" doesn't count.

---

## Phase 6 — Render video

Mechanical phase. Don't reach here until phase 5 is greenlit.

1. Lint: `npx hyperframes lint` — 0 errors on the episode's files.
2. Render main video — in background:
   ```bash
   cd tti-studio && export PATH="/usr/local/bin:$PATH"
   npx hyperframes@0.7.5 render \
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

## Phase 7 — Voiceover & word-sync

Add the creator's **Dhruva** voice (joyful tone) and sync the visuals to it so
every animation/transition lands on the spoken words. **Full process in
`docs/VOICEOVER.md`** — follow it exactly.

1. Copy the previous episode's `sync_build.py` as the starting kit; fill in the new
   episode's beat maps (narration chunks → element ids) and scene table —
   this should be a direct translation of the SFX cue blocks already written
   into `script.md` at Phase 3, not a fresh design pass.
2. Run `python3 sync_build.py` — generates joyful TTS with timestamps, re-times
   each scene to its narration, pins reveals to word times, writes
   `composition_synced.html` + `composition-outro_synced.html` and the audio cache.
3. Re-render the `_synced` compositions, then ffmpeg-mux the voice into
   `video-voiced.mp4` + `outro-voiced.mp4` (commands in `VOICEOVER.md`).
4. QA: duration matches, voice energy at every scene start, spot-check a reveal
   before/after its cue, tone sounds joyful (not strict), SFX matches the cue
   blocks from the script.

**Why this phase exists:** scene-boundary-only sync fires animations early and
leaves dead air. Word-level sync (ElevenLabs `/with-timestamps`) fixes it.

---

## Phase 8 — Deliver

1. `git add episodes/epNN/` (the `audio_v2/` cache is gitignored — that's expected).
2. Commit with a clear message naming the episode + what's inside.
3. Push to the current branch.
4. Reply with GitHub download URLs for each deliverable:
   - `https://github.com/dhruvateja06/videos/blob/<branch>/tti-studio/episodes/epNN/video-voiced.mp4`
   - `…/video.mp4` (silent), `…/script.md`, `…/deck.html`, `…/outro-voiced.mp4`, etc.

---

## Common deviations to avoid

| Deviation | Why it bit us before | What to do instead |
|---|---|---|
| Building the composition/deck before the script | Ep03: visuals were built ahead of the script and came out completely mismatched — had to redo the composition around the script afterward | Outline → script (the storyboard) → deck/composition. Never visuals first. |
| Writing narration with no visual or SFX cues, then figuring out visuals later | Vague `▸ [something happens]` notes produce guesswork in Phase 4 and inconsistent `sync_build.py` SFX placement in Phase 7 | Every scene's script gets specific `▸` visual cues AND an explicit SFX cue block at Phase 3 — see `SFX.md` and `MOTION.md` |
| Scattering files across `compositions/`, `scripts/`, `decks/`, `deliverables/` | Hard to find what belongs to which episode | Everything in `episodes/epNN/` |
| Re-rendering the whole video to fix one scene | The moving background means partial-range renders are seamless-broken | Lint + QA the composition before render, not after |
| Using cinematic AI-generated b-roll | Wrong format for the channel | Infographic / motion-graphics only (see `STYLE.md`) |
| Writing on-screen text in long sentences | Reads like slides, not infographics | Headlines ≤7 words, bullets as fragments |
| **Animations bunched at the start of a scene** | **Ep 1: a ~60s scene finished all its animation by ~35s, then froze while the voiceover kept reading — badly out of sync** | **Spread reveals across the scene's full narration length (~1 every 5–8s); the last reveal lands near the end. See `STYLE.md` → "Pacing & narration sync".** |
| **Scripts that read like written paragraphs** | **Ep 1 short: the hook was dense prose, named "system design" too early, and was em-dash heavy — robotic and hard to teleprompt** | **Spoken rhythm: short lines, one thought per breath; show the scenario and build to the concept before naming it; run the `humanizer` skill (Phase 3). Read it out loud — if it doesn't sound like talking, rewrite.** |

---

## Quality gates (what each phase must produce before the next can start)

| Gate | Looks like |
|---|---|
| **1→2** | "Yes, EP04." |
| **2→3** | "Outline approved. Go write the script." |
| **3→4** | "Script approved — wording, visual cues, and SFX cues all good. Go build the deck." |
| **4→5** | Lint passes, deck.html opens cleanly in a browser, all 15 slides render, and match the script's `▸` cues |
| **5→6** | "Approved, all 15 slides good — render the video." |
| **6→7** | Video probe shows correct duration @ 24fps, key QA frames inspected, file size sane |
| **7→8** | `video-voiced.mp4` QA'd — duration matches, voice energy is joyful, spot reveals land on the right words, SFX matches the script's cue blocks |

If the gate isn't met, you're not done with the phase. Don't move on.
