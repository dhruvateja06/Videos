# The Tech Intern — System Design · Curriculum

> The System Design vertical of *The Tech Intern* — 30 episodes that take a total
> beginner from "what even is a server" to confidently reasoning about how
> Swiggy, UPI and Hotstar are built. Same format, style, and pipeline as the AI
> vertical (its own branch); this vertical has its own palette and motifs
> (`BRAND.md`, `STYLE.md`). Every episode is produced via `WORKFLOW.md`.

**Promise:** Understand how real systems scale — no CS degree, no jargon, no
skipped steps. By the end you can sketch the architecture behind any app you use.
**Pace:** 2 long-form/week → 15 weeks. 10–12 min each + 3–5 shorts.
**Output:** 30 long-form + ~120 shorts.

## Modules

| # | Module | Eps | Locks in |
|---|---|---|---|
| M1 | Foundations | 1–5 | What a "system" is, the request lifecycle, scale vocabulary (qps, p50/p99). |
| M2 | Data Layer | 6–11 | Where data lives + speed: SQL/NoSQL, indexing, caching, replication, sharding, ACID/BASE. |
| M3 | Service Layer | 12–17 | Routing & services talking: load balancers, CDN, gateways, queues, micro vs mono, idempotency. |
| M4 | Reliability & Operations | 18–23 | Staying up under load: CAP, consistency, rate limiting, resilience, monitoring, deploys. |
| M5 | Real Product Teardowns | 24–30 | Put it together on real Indian products + the interview roadmap. |

## Episode map

Difficulty: 🟢 easy · 🟡 medium · 🔴 hard. Code = a light code-along episode.

| Ep | Title | Diff | Code | Status |
|---|---|---|---|---|
| 1 | What even *is* a "system"? (a request's journey) | 🟢 | – | next |
| 2 | Client & server — what happens when you open Swiggy | 🟢 | – | |
| 3 | Latency vs throughput — the two numbers that rule everything | 🟢 | – | |
| 4 | Scale vocabulary — qps, p50/p99, what "1M users" actually means | 🟡 | – | |
| 5 | Scaling up vs out — a bigger box vs more boxes | 🟢 | – | |
| 6 | Databases 101 — SQL vs NoSQL without the holy war | 🟡 | – | |
| 7 | Indexing — finding one row in a billion | 🟡 | – | |
| 8 | Caching — your first cache (and your first cache miss) | 🟡 | ✅ | |
| 9 | Replication — copies that keep you online when a box dies | 🟡 | – | |
| 10 | Sharding — splitting one giant database across machines | 🔴 | – | |
| 11 | ACID vs BASE — when "mostly correct" is allowed | 🟡 | – | |
| 12 | Load balancers — the waiter that picks the kitchen (code-along) | 🟡 | ✅ | |
| 13 | CDN — how Hotstar gets the video close to you | 🟡 | – | |
| 14 | API gateways — one front door for many services | 🟡 | – | |
| 15 | Message queues — "I'll handle it later" | 🟡 | – | |
| 16 | Monolith vs microservices — one big app or many small ones | 🟡 | – | |
| 17 | Idempotency & retries — why double-tapping "Pay" doesn't pay twice | 🔴 | – | |
| 18 | The CAP theorem — consistency vs availability, finally clear | 🔴 | – | |
| 19 | Strong vs eventual consistency — why your like-count lags | 🟡 | – | |
| 20 | Rate limiting — surviving the IRCTC Tatkal rush | 🟡 | – | |
| 21 | Retries, timeouts & circuit breakers — failing gracefully | 🔴 | – | |
| 22 | Monitoring & alerting — knowing it's on fire before users do | 🟡 | – | |
| 23 | Zero-downtime deploys — blue-green & canary | 🟡 | – | |
| 24 | How Swiggy delivers in 30 minutes | 🟡 | – | |
| 25 | How UPI handles a billion+ payments a day | 🔴 | – | |
| 26 | How Hotstar streamed the IPL final to tens of millions | 🔴 | – | |
| 27 | How IRCTC survives Tatkal — failures & fixes | 🟡 | – | |
| 28 | How Flipkart handles Big Billion Day | 🟡 | – | |
| 29 | How Aadhaar authenticates 100M+ times a day | 🔴 | – | |
| 30 | Design-it-yourself — the system-design interview roadmap | 🟢 | – | |

## The 4-beat teaching pattern (every episode)

```
1. HOOK with something they already do   → "It's 8pm. You and a lakh others open Swiggy…"
2. SURFACE the question                   → "How does ONE app not just fall over?"
3. EXPLAIN in 8th-grade language          → 1 visual analogy + the request-path diagram
4. CONNECT BACK                           → "That's the load balancer you never saw."
```

## Recurring mental models (the compounding moat)

The kitchen metaphor is the spine — introduce a piece once, then *invoke* it later
(never re-explain):

| Metaphor | Introduced | Reused in | Explains |
|---|---|---|---|
| **The kitchen** (cooks serve dishes) | Ep 2 | 12, 16, 24 | a server / app |
| **The waiter** (picks a free kitchen) | Ep 12 | 13, 14, 24 | a load balancer |
| **The menu** (read once, reuse many) | Ep 8 | 13, 26 | a cache |
| **The bill counter** (writes are careful) | Ep 6 | 9, 11, 25 | the database |
| **The food rush** (sudden crowd) | Ep 3 | 20, 26, 28 | a load spike |
| **The takeaway shelf** (parcels stack up) | Ep 15 | 17, 24 | a queue |
| **qps / p99** (the two numbers) | Ep 3–4 | every later ep | how we measure scale |

Concepts compound: Ep 3 introduces **qps/latency** → reused everywhere without
re-explaining. Ep 8 introduces **cache hit ratio** → Ep 26 (Hotstar) invokes it as
established shorthand. Ep 17's **idempotency** → load-bearing in Ep 25 (UPI). Don't
re-teach a locked-in term; invoke it.

## Indian example matrix (use ≥2 per episode)

| Example | First in | Concept it anchors |
|---|---|---|
| Swiggy (order → ETA → delivery) | Ep 1 | request lifecycle, consumer scale |
| UPI payments | Ep 17 | idempotency, transactional reliability |
| IRCTC Tatkal 10am rush | Ep 20 | rate limiting, spikes, locking |
| Hotstar IPL live stream | Ep 13 | CDN, extreme concurrency |
| Flipkart Big Billion Day | Ep 5 | horizontal scaling, sale-day load |
| Aadhaar auth | Ep 29 | massive read/auth throughput |

Western examples (AWS, FAANG) are **secondary** — name them, don't lead with them.

## Shorts derivation (3–5 per long-form)

| Type | Source | Hook |
|---|---|---|
| Definition | the 30s "what it is" opener | "Load balancers in 60 seconds — finally clear" |
| Teardown | the Indian-product segment | "How Hotstar streams the IPL without crashing" |
| Visual | the request-path / architecture diagram | "The simplest way to picture sharding" |
| Cliffhanger | the end-of-episode tease | "Caching is easy. Cache *invalidation* isn't…" |
| Hot take | one contrarian moment | "You probably don't need microservices" |

## Pre-record quality checklist

- [ ] First 15s = familiar Indian scenario, no jargon
- [ ] One specific question the viewer would ask themselves
- [ ] Core concept in ≤2 sentences, 8th-grade level
- [ ] One running example threaded through the whole episode
- [ ] The episode's diagram **builds** (request packet / boxes / sparkline), never appears static
- [ ] Concept restated 2–3× in different words
- [ ] Every jargon term defined in plain English on first use; mono labels on diagrams
- [ ] Every on-screen number is **sourced** (verified) — no invented stats
- [ ] Last 30s calls back to the opening scenario + a concrete cliffhanger to next ep
