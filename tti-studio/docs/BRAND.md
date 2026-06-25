# The Tech Intern — Brand

> Read this first in any new session. It defines who the channel is for, how it
> sounds, and the exact colours/fonts every video must use.

## What the channel is

**The Tech Intern** — a faceless YouTube channel that explains tech *from day one*,
for anybody just starting out. Beginner-first, jargon-free, real-world examples.

- **Scope:** not only AI. Over time: AI, **system design, DevOps, security**, and
  more. AI is **Season 1**; other domains are future seasons (see `CURRICULUM.md`).
- **Format:** motion-graphics / infographic explainers (10–12 min long-form) +
  3–5 derivative shorts each. **Faceless** — no presenter on camera.
- **Production model:** render a **silent** motion-graphics video with HyperFrames,
  then the creator adds **voiceover later** in their editor. Scenes are timed/held
  long enough to narrate over. (See `PIPELINE.md`.)
- **Tagline in use:** *"tech, explained from day one."*
- **Do NOT** use the name "AI Seekho" or any other old working name anywhere on
  screen or in scripts. The channel is **The Tech Intern**.

## Voice & tone

Calm, conversational, warm. Talks *with* a beginner, never down to them.
Indian, everyday examples are the **primary** illustrations (Swiggy, UPI, Google
Maps, Gmail, UPI fraud, Flipkart). Western examples (OpenAI, Tesla) are secondary.

Non-negotiable language rules (the teaching discipline):
1. **No naked jargon** — every technical term gets a plain-English parenthetical on
   first use.
2. **Example first, concept second** — start with the familiar thing, then name it.
3. **Compare to something they already know.**
4. **The 8th-grade test** — if a Class-8 student in a Tier-3 city can't follow it,
   rewrite it.
5. **Restate every ~2 minutes** — same idea, different words.
6. **Show before tell** — demonstrate visually, then name it.

## Colour palette (exact)

Used as CSS variables in every composition:

| Token | Hex | Use |
|---|---|---|
| `--paper`  | `#FAF8F3` | background (cream) |
| `--panel`  | `#F2EFE7` | panel / card fill |
| `--ink`    | `#16181D` | primary text (charcoal) |
| `--soft`   | `#41444B` | secondary text |
| `--muted`  | `#8E8A80` | labels, captions, axes |
| `--hair`   | `#E0DBD0` | hairlines, borders |
| `--o`      | `#FF6B2C` | **brand orange** — accents, the one hero colour |
| `--osoft`  | `#FFF1E8` | soft-orange callout fill |

Orange is the single hero colour. Use it deliberately (one or two accents per
scene) — not everywhere, or it stops meaning anything.

```css
:root{ --paper:#FAF8F3; --panel:#F2EFE7; --ink:#16181D; --soft:#41444B;
       --muted:#8E8A80; --hair:#E0DBD0; --o:#FF6B2C; --osoft:#FFF1E8; }
```

## Typography

All fonts are **bundled locally** in `assets/fonts/*.woff2` (no CDN — the renderer
has no network; see `PIPELINE.md`).

| Family | Role | Weights on hand |
|---|---|---|
| **Fraunces** (serif) | headlines, big numbers, the "editorial" feel | 400, 400 italic, 600 |
| **Inter** (sans) | body, bullets, labels, UI | 400, 600, 700 |
| **JetBrains Mono** | code blocks | 400 |

- Headlines: Fraunces 600, tight line-height, slight negative letter-spacing.
- Italic Fraunces is the "quote / emphasis" voice (e.g. *really?*, *patterns*).
- Body/labels: Inter. Eyebrow labels: Inter 700, uppercase, wide letter-spacing.

## Signature visual motifs

- An orange **spine** bar down the left edge (22px).
- A scatter-plot / best-fit-line motif (the "patterns" idea, recurring).
- Editorial serif headline + small uppercase eyebrow label above it.
