# Bootstrap a New Vertical of The Tech Intern

> Use this when starting a brand-new vertical of the channel (System Design,
> DevOps, Security, etc.) on its own branch. Each vertical reuses the
> infrastructure (HyperFrames pipeline, skills, workflow, fonts/GSAP) but
> gets its own palette, curriculum, and signature visual motifs.
>
> **How to use:** in a fresh Claude Code session on the *new* vertical's
> branch, paste the entire prompt below as your first message. The session
> will fetch the AI vertical as a structural reference, install the shared
> infrastructure, and walk you through creating the vertical-specific docs.

---

## When to use this

- A new branch on the same repo, currently empty, slated for a new vertical.
- You want the same disciplined production process (per `WORKFLOW.md`) but
  a visually distinct channel section.

## The bootstrap pattern

Every vertical needs:

| Component | Shared with other verticals? | Source |
|---|---|---|
| HyperFrames CLI, ffmpeg, GSAP, fonts (`assets/`) | ✅ Yes, copy-able | AI vertical |
| `.claude/skills/` (5 skills) | ✅ Yes, copy-able | AI vertical |
| `package.json`, `hyperframes.json`, `SETUP.md` | ✅ Yes, copy-able | AI vertical |
| `docs/WORKFLOW.md` (the 7-phase process) | ✅ Yes, copy-able as-is | AI vertical |
| `docs/PIPELINE.md` (technical render workflow) | ✅ Yes, copy-able as-is | AI vertical |
| `docs/BRAND.md` | ❌ **CUSTOM** | Written fresh per vertical |
| `docs/STYLE.md` | ❌ **CUSTOM** (motion patterns may differ) | Written fresh per vertical |
| `docs/CURRICULUM.md` | ❌ **CUSTOM** | Written fresh per vertical |
| `CLAUDE.md` | ❌ Slight tweak (vertical name) | Adapted from AI vertical |
| `episodes/` | ❌ Empty at bootstrap | Filled per episode |

---

## The bootstrap prompt (paste this into a new session on the new branch)

> Copy everything inside the `<<<BOOTSTRAP>>>` block below into a fresh
> Claude Code session that's checked out on the new vertical's branch.
> The placeholders (`__VERTICAL_NAME__`, `__AI_BRANCH__`, palette hints)
> are filled in for the System Design case — adjust if bootstrapping a
> different vertical.

```text
<<<BOOTSTRAP>>>

You're bootstrapping the **__VERTICAL_NAME__** vertical of *The Tech Intern* —
a faceless YouTube channel that explains tech from day one, beginner-first,
Indian-example-anchored.

The AI vertical of this channel lives on branch `__AI_BRANCH__` of this same
repo and is fully production-ready (5 docs, 5 skills, 2 episodes shipped). You
will reuse its infrastructure but build a visually distinct identity for this
vertical. Don't copy palette/curriculum/style verbatim — read the AI vertical
for structural patterns, then write fresh content for this one.

## Step 1: Fetch the AI vertical as a reference

```bash
cd /path/to/this/repo
git fetch origin __AI_BRANCH__:_ai-ref
git --no-pager log --oneline _ai-ref -5
```

You can now read any file from the AI vertical with:
```bash
git show _ai-ref:tti-studio/docs/WORKFLOW.md      # read the canonical workflow
git show _ai-ref:tti-studio/docs/PIPELINE.md      # read the technical pipeline
git show _ai-ref:tti-studio/docs/BRAND.md         # read the AI brand AS REFERENCE ONLY
git show _ai-ref:tti-studio/CLAUDE.md             # see the session entry point
git show _ai-ref:tti-studio/episodes/ep02/composition.html  # see a reference composition
```

## Step 2: Copy the shared infrastructure

Copy files from the AI vertical that don't differ across verticals:

```bash
# Configs + setup
git checkout _ai-ref -- tti-studio/package.json
git checkout _ai-ref -- tti-studio/hyperframes.json
git checkout _ai-ref -- tti-studio/SETUP.md
git checkout _ai-ref -- tti-studio/.gitignore || true  # if absent, create one
git checkout _ai-ref -- tti-studio/index.html || true  # the brand intro test

# Shared assets — fonts + GSAP
git checkout _ai-ref -- tti-studio/assets/

# Project-scope skills (5 of them)
git checkout _ai-ref -- tti-studio/.claude/skills/

# Workflow + Pipeline (vertical-agnostic)
mkdir -p tti-studio/docs
git checkout _ai-ref -- tti-studio/docs/WORKFLOW.md
git checkout _ai-ref -- tti-studio/docs/PIPELINE.md
git checkout _ai-ref -- tti-studio/docs/NEW-VERTICAL-BOOTSTRAP.md
```

DO NOT copy BRAND.md, STYLE.md, CURRICULUM.md, or CLAUDE.md — those are
vertical-specific and you'll write fresh ones below.

## Step 3: Verify the HyperFrames environment

```bash
cd tti-studio
ls assets/vendor/gsap.min.js      # must exist
ls assets/fonts/*.woff2 | wc -l    # should be ~7
ls .claude/skills/                 # should list 5 skill folders
```

If anything is missing, check `SETUP.md` for the re-install commands.

## Step 4: Define this vertical's BRAND (deliberately distinct from AI's)

This is where you commit to a visual identity. Open the AI vertical's BRAND.md
as reference (`git show _ai-ref:tti-studio/docs/BRAND.md`) and note its choices:
cream paper `#FAF8F3` + vivid orange `#FF6B2C`, Fraunces + Inter, scatter-plot
motif.

For __VERTICAL_NAME__, you must pick a DIFFERENT palette and signature motif.

For System Design specifically, suggested directions (let the user pick before
finalizing):

- **Palette option A — "Engineer's Terminal":** deep navy paper `#0F1729`,
  cool slate text `#E6ECF5`, electric cobalt accent `#3B7BFF`, muted grey
  `#7B8AA5`. Mood: serious, technical, "I'm reading a system diagram at 2 AM".
- **Palette option B — "Blueprint Paper":** off-white `#F1F4F9` paper, ink
  `#0E1729`, controlled teal-cyan `#0FBFBF` accent, warm grey `#8A95A3`.
  Mood: architect's drafting table, clean schematics.
- **Palette option C — "Datacenter Heat Map":** off-white `#FAF8F4` paper
  (closer to AI but not identical), ink `#16181D`, red-orange `#FF4530` accent
  (NOT the AI's `#FF6B2C` — different enough to read as a separate channel),
  cool slate `#5A6B82`. Mood: traffic-monitoring console, latency spikes.

**Typography:** keep Fraunces (serif) for headlines — it's the Tech Intern
voice — but elevate JetBrains Mono significantly. System design = lots of
labels on diagrams (query types, latencies, throughput numbers), and mono fits
that vocabulary perfectly.

**Signature motif:** the AI vertical's motif was a scatter plot + best-fit
line. For System Design, the equivalent should be **an animated request-path
diagram** — a request packet (small dot) traveling through `client → CDN →
load balancer → cache → application server → database`, with each hop's
latency annotated. It captures the whole "how does a system actually work"
mental model in one image.

Ask the user to pick the palette (A/B/C/other) BEFORE writing BRAND.md. Don't
guess. The palette decision cascades into STYLE.md.

Then write `tti-studio/docs/BRAND.md` with:
- Channel identity: "The Tech Intern — System Design vertical"
- Voice & tone: still warm and beginner-first, but with builder-vocabulary
  creeping in ("the request hops through three services", "this DB query
  would melt under load", "she added a Redis cache and bought herself six
  more months")
- Exact color tokens (CSS variables) with usage notes
- Typography rules with mono used for diagram annotations
- Signature motifs (request paths, throughput numbers, before/after load-line
  graphs, before/after architecture diagrams)

## Step 5: Write STYLE.md (motion-graphics rules for this vertical)

Adapt the AI vertical's STYLE.md but customize for system design's needs.

Read `git show _ai-ref:tti-studio/docs/STYLE.md` for the structure. Keep:
- The "infographic, never slideshow" rule
- Living background (always-moving so no frame freezes)
- Wipe transitions at section cuts
- Kinetic headline reveals with overshoot
- Breathing/float on hero elements during long holds
- Building diagrams (not appearing)

Customize for system design:
- Background dot-grid stays but with the new palette's hues
- Background blobs use the new accent color
- New diagram primitives to standardize:
  - **Request packet animation:** small dot/pill traveling along a path
    between system components, with `stroke-dasharray` trail
  - **Latency annotations:** `mono-font` ms numbers appearing as the packet
    crosses each hop
  - **Load-spike sparkline:** a small line chart that animates from flat → spiky
  - **Architecture box-and-arrow:** rounded rectangles with clear labels,
    arrows that draw on
  - **Before/after split-screen:** monolith on left, microservices on right
  - **Live-counter dashboards:** counts (qps, concurrent users) that tick up

## Step 6: Write CURRICULUM.md (30 episodes for system design)

Open `git show _ai-ref:tti-studio/docs/CURRICULUM.md` for the structural template
(modules, dependency graph, recurring metaphors, Indian examples matrix,
4-beat teaching pattern, quality checklist).

Suggested 5-module structure for System Design (refine with the user):

- **M1 — Foundations (Eps 1–5):** What is a "system", request lifecycle,
  client-server, latency basics, scale vocabulary (qps, throughput, p50/p99).
- **M2 — Data Layer (Eps 6–11):** Databases (SQL vs NoSQL), indexing,
  caching, replication, sharding, ACID vs BASE, your first cache miss
  (code-along).
- **M3 — Service Layer (Eps 12–17):** Load balancers, CDN, API gateways,
  queues, microservices vs monoliths, your first load balancer (code-along).
- **M4 — Reliability & Operations (Eps 18–23):** CAP theorem, consistency
  models, monitoring & alerting, rate limiting, retry/backoff, deployment
  strategies.
- **M5 — Real Product Teardowns (Eps 24–30):** How Swiggy delivers in 30
  min, how UPI handles 1B+ daily txns, how Hotstar streamed IPL to 25M
  concurrent, how WhatsApp scaled with 50 engineers, how Aadhaar handles
  100M+ daily auths, the system-design roadmap to senior engineer.

Recurring metaphors to seed:
- **The kitchen** — a server (cooks food / serves requests)
- **The waiter** — a load balancer (takes order, picks the right kitchen)
- **The menu** — a cache (read once, reuse many times)
- **The bill counter** — the database (writes have to be careful)
- **The food rush** — a load spike (Hotstar IPL final)
- **The takeaway parcel** — a queue (orders stack up when kitchen's busy)

Indian example matrix:
- Swiggy (every episode about consumer-scale ETL), UPI (transactional
  reliability), IRCTC (legendary scaling failures + recoveries), Hotstar
  (extreme spike), Flipkart Big Billion Day (sale-day scale), Bhashini
  (multilingual real-time), Aadhaar (massive auth throughput).

DO NOT just list topics. Map dependencies: which episode depends on which.
EP 1 introduces "qps" — EP 4 reuses it without re-explaining. EP 7 introduces
"cache hit ratio" — EP 26 (Hotstar teardown) invokes it as established
shorthand. This is the compounding moat.

## Step 7: Write CLAUDE.md

Adapt the AI vertical's `CLAUDE.md` to surface WORKFLOW.md as #1 read, but
make it clear this is the system design vertical. Reference the AI branch by
name so future sessions don't mix the two up.

## Step 8: Quality gates before committing

- [ ] All 5 docs exist (WORKFLOW, BRAND, STYLE, PIPELINE, CURRICULUM)
- [ ] BRAND.md palette is visually distinct from the AI vertical's
- [ ] STYLE.md customizes the diagram primitives for system design
- [ ] CURRICULUM.md has all 30 episodes mapped with dependencies + Indian
       example matrix
- [ ] WORKFLOW.md is the AI vertical's verbatim (it's universal)
- [ ] CLAUDE.md surfaces WORKFLOW.md as #1, names this vertical clearly
- [ ] `npx hyperframes lint` passes (should — no episodes yet, just config)
- [ ] `git status` shows the right files staged
- [ ] No accidental BRAND.md / CURRICULUM.md copied from AI vertical

## Step 9: Commit + push

```bash
git add tti-studio/
git status --short
git commit -m "Bootstrap __VERTICAL_NAME__ vertical of The Tech Intern

Sets up the channel brain for the __VERTICAL_NAME__ branch using the
production patterns from the AI vertical (branch __AI_BRANCH__):
- Shared infrastructure: HyperFrames + FFmpeg setup, assets (fonts +
  GSAP), 5 project-scope skills, WORKFLOW + PIPELINE docs
- Vertical-specific: BRAND, STYLE, CURRICULUM rewritten for
  __VERTICAL_NAME__ with its own palette and signature motifs
- CLAUDE.md surfaces WORKFLOW.md as the canonical process

Ready to build episodes. Follow docs/WORKFLOW.md for every episode."

git push -u origin $(git branch --show-current)
```

## Step 10: Verify by starting EP01

Before declaring bootstrap done, walk through phase 1 of WORKFLOW.md for the
first episode:
- Open CURRICULUM.md
- Pick EP01 of this vertical
- Confirm topic with the user
- Send a Phase 2 content outline for approval

If you can do that smoothly, the bootstrap worked. If anything's missing
(skill not loading, asset not found, lint failure), fix it before starting
actual episode work.

## Hard rules — don't deviate

1. **Follow WORKFLOW.md gates.** No script-first, no skip-validation. The
   AI vertical learned this the painful way.
2. **No cinematic AI-generated b-roll.** Infographic / motion-graphics only.
3. **No on-screen text longer than 7 words per headline.** Bullets as
   fragments. Read STYLE.md.
4. **Per-episode folders, never scattered.** All files in
   `tti-studio/episodes/epNN/`.
5. **The deck is the validation unit before any render.** Always.
6. **Indian examples first.** Western examples (AWS, FAANG) are secondary.

<<<END BOOTSTRAP>>>
```

---

## After this prompt has been used

Once a vertical is bootstrapped, episodes follow the standard `WORKFLOW.md`
process — no special handling needed. The vertical's branch contains
everything it needs to operate independently.

To start an episode in any vertical:

```text
You're on the [VERTICAL] branch. Read docs/WORKFLOW.md, then start EP01.
```

## Reusing this pattern for future verticals

The bootstrap prompt above is templated. To bootstrap a *DevOps* vertical
next, just swap:

- `__VERTICAL_NAME__` → `DevOps`
- `__AI_BRANCH__` → either the AI branch or any other already-bootstrapped
  vertical as the reference (whichever is most current)
- Palette suggestions and signature motif → DevOps-appropriate (e.g.,
  pipeline/CI-flow diagrams, terminal-green accent)
- Curriculum module names → DevOps modules

The shared infrastructure (workflow, pipeline, skills, assets) stays
identical across all verticals. Only the BRAND, STYLE, and CURRICULUM are
vertical-specific.
