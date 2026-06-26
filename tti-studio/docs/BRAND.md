# The Tech Intern — System Design · Brand

> Read this first in any new session on this branch. It defines who this vertical
> is for, how it sounds, and the exact colours/fonts every video must use.
> **This is the System Design vertical.** The AI vertical (cream + orange) lives
> on its own branch — do not mix the two looks.

## What this vertical is

**The Tech Intern — System Design** — the same faceless, beginner-first channel,
now teaching how real systems are built and scaled, *from day one*. No CS degree
assumed. We start at "what even is a server" and end at "how Hotstar streamed the
IPL final to tens of millions at once."

- **Format:** silent motion-graphics / infographic explainers (10–12 min) + 3–5
  derivative shorts each. **Faceless** — no presenter on camera.
- **Production model:** render a **silent** video with HyperFrames; the creator
  adds **voiceover later**. Scenes are held long enough to narrate over. (See
  `PIPELINE.md`, and `WORKFLOW.md` for the per-episode process.)
- **Tagline:** *"systems, explained from day one."*

## Voice & tone

Calm, conversational, warm — talks *with* a beginner, never down to them. The AI
vertical's teaching discipline carries over, but the vocabulary now picks up a
little **builder's swagger** — said plainly, always explained on first use:

- "the request hops through three services before it ever hits the database"
- "that one query would *melt* under load"
- "she added a Redis cache and bought herself six more months of runway"

Non-negotiable language rules:
1. **No naked jargon** — every term gets a plain-English parenthetical on first use
   (e.g. "latency *(how long one request takes)*").
2. **Example first, concept second** — start with the familiar thing, then name it.
3. **Compare to something they already know** (a kitchen, a queue at the bank).
4. **The 8th-grade test** — if a Class-8 student in a Tier-3 city can't follow it,
   rewrite it.
5. **Restate every ~2 minutes** — same idea, different words.
6. **Show before tell** — animate it, then name it.

Indian, everyday examples are the **primary** illustrations (Swiggy, UPI, IRCTC,
Hotstar, Flipkart, Aadhaar). Western examples (AWS, FAANG) are **secondary**.

## Colour palette — "Engineer's Terminal" (exact)

Dark, cool, technical — the opposite of the AI vertical's warm cream. Used as CSS
variables in every composition:

| Token | Hex | Use |
|---|---|---|
| `--paper` | `#0F1729` | background (deep navy) |
| `--panel` | `#16223C` | panel / node / card fill |
| `--panel2` | `#1B2A47` | raised card / hover fill |
| `--ink` | `#E6ECF5` | primary text (cool near-white) |
| `--soft` | `#B7C2D6` | secondary text |
| `--muted` | `#7B8AA5` | labels, captions, axes, mono annotations |
| `--hair` | `rgba(123,138,165,.22)` | hairlines, borders, edges |
| `--accent` | `#3B7BFF` | **electric cobalt — the one hero colour** |
| `--accent-bright` | `#6AA0FF` | glows, highlights, the live request packet |
| `--accent-soft` | `rgba(59,123,255,.14)` | soft callout / panel-accent fill |
| `--spike` | `#FF6B6B` | **load spikes, errors, "melts under load"** (sparingly) |
| `--ok` | `#34D399` | healthy / cache-hit / success / "p99 in budget" |

```css
:root{
  --paper:#0F1729; --panel:#16223C; --panel2:#1B2A47;
  --ink:#E6ECF5; --soft:#B7C2D6; --muted:#7B8AA5; --hair:rgba(123,138,165,.22);
  --accent:#3B7BFF; --accent-bright:#6AA0FF; --accent-soft:rgba(59,123,255,.14);
  --spike:#FF6B6B; --ok:#34D399;
}
```

**Cobalt is the single hero colour** — one or two accents per scene, not
everywhere. `--spike` (red) and `--ok` (green) are **functional status colours**
only: red for load spikes / failures, green for healthy / cache hits. They make
the dashboards read instantly; they are not decoration.

## Typography

All fonts are **bundled locally** in `assets/fonts/*.woff2` (no CDN — the renderer
has no network; see `PIPELINE.md`).

| Family | Role | Weights on hand |
|---|---|---|
| **Fraunces** (serif) | headlines, big numbers, the editorial Tech-Intern feel | 400, 400 italic, 600 |
| **Inter** (sans) | body, bullets, UI labels | 400, 600, 700 |
| **JetBrains Mono** | **elevated here** — every diagram annotation | 400 |

- Headlines: **Fraunces 600**, tight line-height, slight negative letter-spacing —
  keeps the channel's voice consistent with the AI vertical.
- **JetBrains Mono does the heavy lifting on diagrams:** latencies (`42 ms`),
  throughput (`12k qps`), percentiles (`p99`), component labels (`LOAD BALANCER`),
  status (`cache HIT`). System design is a labelled discipline; mono reads as
  "real engineering," not marketing.
- Eyebrow labels: Inter 700 uppercase wide-tracked — OR mono for a more technical
  eyebrow (`// REQUEST PATH`).

## Signature visual motifs

The motif that *is* this vertical:

- **The request-path diagram** — a request packet (a small glowing cobalt dot)
  travels left→right through `client → CDN → load balancer → cache → app server →
  database`, each hop a labelled rounded box, each connection drawing on, the
  packet leaving a `stroke-dasharray` trail. The whole "how a system actually
  works" mental model in one moving image. This is our scatter-plot equivalent.
- **Latency annotations** — mono `ms` numbers that pop in as the packet crosses
  each hop (`+8 ms`, `+30 ms` …), totalling at the end.
- **Load-spike sparkline** — a small line chart that animates flat → spiky (the
  IPL-final traffic surge), drawn in `--spike` red.
- **Architecture box-and-arrow** — rounded rectangles, clear mono labels, arrows
  that draw on; the staple diagram.
- **Before/after split-screen** — monolith (left) vs microservices (right); one
  server vs a scaled-out fleet.
- **Live-counter dashboards** — qps / concurrent-users counters ticking up, `--ok`
  green while healthy, flicking to `--spike` red past a threshold.

No left "spine" bar (that's the AI vertical's mark). This vertical's frame is a
thin **HUD** top bar + corner brackets — a monitoring-console feel.
