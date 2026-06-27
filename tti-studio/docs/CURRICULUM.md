# The Tech Intern — System Design · Curriculum

> The System Design vertical of *The Tech Intern* — 30 episodes that take a total
> beginner from "what even is a server" to confidently designing WhatsApp, UPI
> and Hotstar from scratch. Same format, style, pipeline as the AI vertical (its
> own branch); this vertical has its own palette and motifs (`BRAND.md`,
> `STYLE.md`). Every episode is produced via `WORKFLOW.md`.

**Promise:** Understand how real systems scale — no CS degree, no jargon, no
skipped steps. By the end you can whiteboard the architecture behind any app.
**Pace:** 2 long-form/week → 15 weeks. 10–12 min each + 3–5 shorts.
**Output:** 30 long-form + ~120 shorts.

This curriculum is curated from three references (used as the per-episode research
backbone — see **Sources**): the coverage map from *awesome-system-design-
resources*, the *"what breaks next?"* teaching method from *system-design-
notebook*, and the build-it-piece-by-piece style of *systemdesignlab*.

## The season spine — "what breaks next?"

We don't teach 30 disconnected topics. We build **one app — call it Dabba**
(a Swiggy-style food app) — and **keep scaling it**. Every episode, something
**breaks under load**, and *that's why* we add the next component:

- 10 users → one server is fine. **1 lakh users → it melts** → load balancer (M1).
- Reads get slow → **the database is the bottleneck** → indexing, caching, CDN (M2).
- Services tangle, writes pile up → **decouple** → queues, gateways, microservices (M3).
- A node dies at 2 a.m. → **stay correct & online** → CAP, resilience, monitoring (M4).
- Now you can design the famous apps from scratch (M5).

Each episode also lands on **one explicit trade-off** (see the Tradeoffs table) —
the repeatable "engineer's decision" beat.

## Modules

| # | Module | Eps | Locks in | Triggered by |
|---|---|---|---|---|
| M1 | Foundations | 1–6 | request lifecycle, the network, scale vocab, load balancing, APIs | "one server melts" |
| M2 | Data Layer | 7–12 | SQL/NoSQL, indexing, caching, CDN, replication, sharding + consistent hashing | "the database is the bottleneck" |
| M3 | Talking & Async | 13–18 | queues, pub/sub, gateways, rate limiting, idempotency, micro vs mono | "services tangle, writes pile up" |
| M4 | Reliability & Ops | 19–24 | CAP, consistency, resilience, consensus, monitoring, deploys | "a node dies at 2 a.m." |
| M5 | Design It For Real | 25–30 | the canonical "design X" interview problems, Indian-anchored | "now design it yourself" |

## Episode map

Difficulty: 🟢 easy · 🟡 medium · 🔴 hard. Code = a light code-along.

| Ep | Title | Diff | Code | Status |
|---|---|---|---|---|
| 1 | What even *is* a "system"? (a request's journey) | 🟢 | – | ✅ done |
| 2 | Client, server & the network — DNS & HTTP when you open Swiggy | 🟢 | – | ✅ done |
| 3 | Latency vs throughput vs bandwidth — the numbers that rule everything | 🟢 | – | |
| 4 | Scale vocabulary — qps, p50/p99, and availability "nines" | 🟡 | – | |
| 5 | Scaling up vs out + load balancers — the waiter that picks the kitchen | 🟢 | – | |
| 6 | APIs — how services talk (REST & the contract) | 🟢 | – | |
| 7 | Databases 101 — SQL vs NoSQL without the holy war | 🟡 | – | |
| 8 | Indexing — finding one row in a billion | 🟡 | – | |
| 9 | Caching — your first cache, and the strategies (code-along) | 🟡 | ✅ | |
| 10 | CDN — how Hotstar gets the video close to you | 🟡 | – | |
| 11 | Replication — copies that keep you online when a box dies | 🟡 | – | |
| 12 | Sharding + consistent hashing — splitting a giant database | 🔴 | – | |
| 13 | Message queues — "I'll handle it later" | 🟡 | – | |
| 14 | Pub/Sub & event-driven — one event, many listeners | 🟡 | – | |
| 15 | API gateways — one front door for many services | 🟡 | – | |
| 16 | Rate limiting — surviving the IRCTC Tatkal rush | 🟡 | – | |
| 17 | Idempotency & retries — why double-tapping "Pay" doesn't pay twice | 🔴 | – | |
| 18 | Monolith vs microservices — one big app or many small ones | 🟡 | – | |
| 19 | The CAP theorem — consistency vs availability, finally clear | 🔴 | – | |
| 20 | Strong vs eventual consistency — why your like-count lags | 🟡 | – | |
| 21 | Resilience — timeouts, retries & circuit breakers | 🔴 | – | |
| 22 | Consensus & leader election — how machines agree (Raft, plain English) | 🔴 | – | |
| 23 | Monitoring & observability — metrics, logs & traces | 🟡 | – | |
| 24 | Zero-downtime deploys — blue-green & canary | 🟡 | – | |
| 25 | Design a URL shortener — the classic first interview question | 🟡 | – | |
| 26 | Design a chat app (WhatsApp) — delivered, then those blue ticks | 🔴 | – | |
| 27 | Design a news feed (Instagram) — fan-out explained | 🔴 | – | |
| 28 | Design live streaming (Hotstar / IPL) — CDN + extreme concurrency | 🔴 | – | |
| 29 | Design a payment system (UPI) — money must never be wrong | 🔴 | – | |
| 30 | Design ride-hailing (Ola / Uber) + the system-design interview roadmap | 🔴 | – | |

> **Ep01 note:** the shipped long-form anchors on a **baby Instagram** example
> (post a photo → friends see it), not Dabba. The Dabba food-app season spine
> resumes from later episodes.

## The 4-beat teaching pattern (every episode)

```
1. HOOK with something they already do   → "It's 8pm. You and a lakh others open Swiggy…"
2. SURFACE the question                   → "Why did the app just slow to a crawl?"
3. EXPLAIN in 8th-grade language          → 1 visual analogy + the request-path diagram
4. CONNECT BACK                           → "That's the load balancer you never saw — and the trade-off it costs."
```

## Recurring mental models (the kitchen spine — the compounding moat)

Introduce a piece once, then *invoke* it later (never re-explain):

| Metaphor | Introduced | Reused in | Explains |
|---|---|---|---|
| **The kitchen** (cooks serve dishes) | Ep 2 | 5, 18, 25 | a server / app |
| **The waiter** (picks a free kitchen) | Ep 5 | 10, 15 | a load balancer |
| **The menu** (read once, reuse many) | Ep 9 | 10, 28 | a cache |
| **The bill counter** (writes are careful) | Ep 7 | 11, 29 | the database |
| **The food rush** (sudden crowd) | Ep 3 | 16, 28 | a load spike |
| **The takeaway shelf** (parcels stack up) | Ep 13 | 14, 17 | a queue |
| **qps / p99** (the two numbers) | Ep 3–4 | every later ep | how we measure scale |

## The Tradeoffs lens (the recurring "engineer's decision" beat)

Most episodes end on one explicit trade-off — the repeatable teaching device:

| Trade-off | Lands in |
|---|---|
| Latency vs throughput | Ep 3 |
| Scale up vs scale out · stateful vs stateless | Ep 5 |
| REST vs RPC/GraphQL | Ep 6 |
| SQL vs NoSQL | Ep 7 |
| Read-through vs write-through cache | Ep 9 |
| Sync vs async (request-response vs events) | Ep 13–14 |
| Monolith vs microservices | Ep 18 |
| Consistency vs availability (CAP) | Ep 19 |
| Strong vs eventual consistency | Ep 20 |
| Push vs pull (fan-out) | Ep 27 |
| Long-polling vs WebSockets | Ep 26 |

## Indian example matrix (use ≥2 per episode; Western examples secondary)

| Example | First in | Concept it anchors |
|---|---|---|
| Swiggy ("Dabba", the running app) | Ep 1 | request lifecycle, the whole-season build |
| Flipkart Big Billion Day | Ep 5 | horizontal scaling, sale-day load |
| Hotstar IPL live stream | Ep 10 | CDN, extreme concurrency |
| IRCTC Tatkal 10am rush | Ep 16 | rate limiting, spikes, locking |
| UPI payments | Ep 17 | idempotency, transactional reliability |
| Aadhaar auth | Ep 23 | auth throughput, monitoring |
| WhatsApp / Instagram / Ola | Ep 26–30 | the design-it-for-real teardowns |

## Shorts derivation (3–5 per long-form)

| Type | Source | Hook |
|---|---|---|
| Definition | the 30s "what it is" opener | "Load balancers in 60 seconds — finally clear" |
| What-breaks | the failure that triggers the episode | "Your app just hit 1M users. Here's what breaks first." |
| Teardown | the Indian-product segment | "How Hotstar streams the IPL without crashing" |
| Tradeoff | the episode's decision beat | "SQL or NoSQL? The honest answer." |
| Hot take | one contrarian moment | "You probably don't need microservices" |

## Sources (per-episode research backbone)

- **[awesome-system-design-resources](https://github.com/ashishps1/awesome-system-design-resources)** — coverage map + concept reference + the "design X" case-study set + the tradeoffs catalogue.
- **[system-design-notebook](https://github.com/bregman-arie/system-design-notebook)** — the *"what breaks next?"* evolving-exercise method (the season spine) + clarifying-question prompts.
- **[systemdesignlab](https://systemdesignlab.netlify.app/)** — build-the-architecture-piece-by-piece reference; sanity-checks the visual build order of each diagram.

Each episode's research (`WORKFLOW.md` Phase 2/3) cross-checks facts/numbers
against authoritative primaries (System Design Primer, official engineering
blogs) — every on-screen number must be sourced.

## Pre-record quality checklist

- [ ] First 15s = familiar Indian scenario, no jargon
- [ ] The episode is triggered by a concrete "what breaks" moment in the Dabba app
- [ ] Core concept in ≤2 sentences, 8th-grade level
- [ ] One running example threaded through; diagram **builds** (request packet / boxes / sparkline)
- [ ] Concept restated 2–3× in different words; mono labels on diagrams
- [ ] Lands on one explicit **trade-off**
- [ ] Every on-screen number is **sourced** (verified) — no invented stats
- [ ] Last 30s calls back to the opening + a concrete cliffhanger to next ep
