# The Tech Intern — Curriculum

> The channel covers tech broadly (AI, system design, DevOps, security, …).
> **Season 1 is AI** and **Season 2 is System Design** — both fully sequenced
> below (30 episodes each). Later seasons — DevOps, security — reuse the same
> format, style, and pipeline.

## Season 1 — AI (30 episodes)

**Promise:** Zero to understanding modern AI. No PhD, no jargon, no skipped steps.
**Pace:** 2 long-form/week (Mon + Thu) → 15 weeks. 10–12 min each + 3–5 shorts.
**Output:** 30 long-form + ~120 shorts.

### Modules

| # | Module | Eps | Locks in |
|---|---|---|---|
| M1 | Foundations | 1–5 | What AI even is. Vocabulary. Mental map. |
| M2 | How Machines Learn | 6–11 | The learning mechanism. First code. |
| M3 | Neural Networks | 12–17 | The building blocks. Second code. |
| M4 | Modern Architectures | 18–23 | CNN, RNN, Transformer, attention, embeddings. |
| M5 | Generative AI Era | 24–30 | LLMs, RAG, RLHF, agents, diffusion, what's next. |

### Episode map

| Ep | Title | Diff | Code | Status |
|---|---|---|---|---|
| 1 | What is AI, really? | 🟢 | – | **DONE** — `compositions/ep01-full.html` |
| 2 | AI vs ML vs Deep Learning vs GenAI — finally clear | 🟢 | – | |
| 3 | DATA → MODEL → PREDICTION: the framework every AI system uses | 🟢 | – | |
| 4 | Supervised, Unsupervised, Reinforcement — three ways to learn | 🟢 | – | |
| 5 | Why AI is having a moment NOW (compute + data + algorithms) | 🟢 | – | |
| 6 | What does "learn from data" actually mean? | 🟢 | – | |
| 7 | The loss function: how a machine knows it's wrong | 🟡 | – | |
| 8 | Gradient descent: the "walking downhill" mental model | 🟡 | – | |
| 9 | Train / validation / test: why we split data | 🟢 | – | |
| 10 | Overfitting: when the model memorizes instead of learns | 🟡 | – | |
| 11 | Your first ML model in Python (code-along) | 🟡 | ✅ | |
| 12 | The neuron: just a weighted sum + activation | 🟡 | – | |
| 13 | Why layers? Building from simple to complex | 🟡 | – | |
| 14 | Activation functions: ReLU, Sigmoid, Softmax | 🟡 | – | |
| 15 | Backpropagation: how networks actually update | 🔴 | – | |
| 16 | Why depth matters (deep vs shallow) | 🟡 | – | |
| 17 | Build a tiny neural net in Python (code-along) | 🔴 | ✅ | |
| 18 | CNN: how computers actually see | 🟡 | – | |
| 19 | RNN / LSTM: how computers process sequences | 🔴 | – | |
| 20 | The Transformer: the most important paper of the decade | 🔴 | – | |
| 21 | Attention is all you need: what that actually means | 🔴 | – | |
| 22 | Embeddings: turning words into math | 🟡 | – | |
| 23 | Tokens, context windows, and why ChatGPT forgets | 🟡 | – | |
| 24 | What is a Large Language Model, really? | 🟡 | – | |
| 25 | Pre-training vs fine-tuning vs RLHF | 🔴 | – | |
| 26 | RAG: giving an LLM your own knowledge | 🟡 | – | |
| 27 | Prompt engineering: what actually works | 🟢 | – | |
| 28 | AI agents: when models can act, not just talk | 🟡 | – | |
| 29 | Diffusion models: how images and videos are generated | 🔴 | – | |
| 30 | The roadmap from here: what to learn after Season 1 | 🟢 | – | |

## The 4-beat teaching pattern (every episode)

```
1. HOOK with something they already do   → "You just opened Swiggy. Watch this..."
2. SURFACE the question                   → "How does it know 32 minutes?"
3. EXPLAIN in 8th-grade language          → 1 visual analogy + 1 simple sentence
4. CONNECT BACK                           → "That's what just happened on your phone."
```

## Recurring mental models (the compounding moat)

Introduce a metaphor once, then *invoke* it later (never re-explain):

| Metaphor | Introduced | Reused in | Explains |
|---|---|---|---|
| **Rules vs Patterns** | Ep 1 | 2, 6, 25 | Why AI ≠ traditional software |
| **Downhill walker** (gradient descent) | Ep 8 | 11, 15 | How models improve |
| **Weighted sum** (neuron) | Ep 12 | 13, 14, 16 | Building block |
| **Memorize vs generalize** | Ep 10 | 11, 17, 25 | The eternal trap |
| **Spotlight** (attention) | Ep 21 | 23, 24 | What Transformers do |
| **Map of meanings** (embeddings) | Ep 22 | 23, 26, 27 | Why LLMs feel like they understand |

## Indian example matrix (use ≥2 per episode)

| Example | First in | Concept |
|---|---|---|
| Swiggy delivery ETA | Ep 1 | Regression |
| UPI fraud detection | Ep 1 | Binary classification |
| Bhashini multilingual | Ep 5 | Embeddings / multilingual transformers |
| Flipkart recommendations | Ep 4 | Unsupervised / similarity |
| Indian Railways seat allocation | Ep 4 | Reinforcement learning |
| Krishi agri AI (Karnataka) | Ep 18 | CNN / computer vision |
| Diffusion poster generation | Ep 29 | Diffusion |

## Shorts derivation (3–5 per long-form)

| Type | Source | Hook |
|---|---|---|
| Definition | the 30s "what it is" opener | "X in 60 seconds — finally clear" |
| Example | the Indian-example portion | "Why [product] uses [concept]" |
| Visual | the mental-model diagram | "The simplest way to understand [concept]" |
| Cliffhanger | the roadmap ending | "[Concept] is just the beginning…" |
| Hot take | one contrarian moment | "Most people get [concept] wrong" |

## Pre-record quality checklist

- [ ] First 15s = familiar Indian scenario, no jargon
- [ ] One specific question the viewer would ask themselves
- [ ] Core concept in ≤2 sentences, 8th-grade level
- [ ] One visual analogy (the episode's recurring metaphor)
- [ ] Concept restated 2–3× in different words
- [ ] Last 30s calls back to the opening scenario
- [ ] Every jargon term defined in plain English on first use
- [ ] A "verify on your phone right now" moment
- [ ] Concrete cliffhanger to the next episode

---

## Season 2 — System Design (30 episodes)

> Same channel, same format, same pipeline. Where Season 1 answered *"what is
> the machine thinking?"*, Season 2 answers *"what happens after you tap the
> button — and how does it still work when a million people tap at once?"*
> Worked examples are **Indian product teardowns** (Swiggy, UPI, Hotstar, IRCTC,
> Flipkart, WhatsApp, Ola) — the apps the viewer already has open.

**Promise:** Zero to designing real systems. From "what is a server" to "how
Hotstar streams the IPL final to 50 million people" — no CS degree, no jargon,
no skipped steps.
**Pace:** 2 long-form/week (Mon + Thu) → 15 weeks. 10–12 min each + 3–5 shorts.
**Output:** 30 long-form + ~120 shorts.

### The two lenses — HLD & LLD (read this first)

Every system-design topic can be looked at two ways, and interviews test **both**.
We tag every episode with the lens(es) it teaches so the season covers the whole
discipline, not just the famous half:

- **HLD — High-Level Design** (the *boxes-and-arrows* view): components and how
  they connect — servers, load balancers, caches, databases, queues, CDNs — plus
  the trade-offs that decide which box goes where. "Draw the system on a
  whiteboard." Beginner-reachable with no code.
- **LLD — Low-Level Design** (the *inside-one-box* view): turning a single
  component into actual classes, methods, data structures and state machines —
  the LRU cache, the token bucket, the circuit-breaker state machine, the
  payment ledger. "Now write the code for that box." Assumes light OOP fluency.

Lens tags: **🅗 HLD** · **🅛 LLD** · **🅗🅛 Both**. Most foundation episodes are
HLD-led; the LLD lens switches on the moment a topic has a clean, teachable
data-structure or class behind it (caching → LRU, rate limiting → token bucket,
resilience → circuit breaker), and the Module 5 "design X" episodes are fully
both. The per-episode HLD/LLD angles are spelled out in the breakdown below the
episode map.

> **Known gap (decision needed):** pure **LLD fundamentals** — OOP, the SOLID
> principles, the core design patterns (strategy/factory/observer/state), basic
> UML — currently have **no home**, yet several LLD lenses below assume them. For
> a beginner-first channel that's a real cliff. Recommendation: fold a 3-minute
> "what LLD even is + objects 101" primer into **Ep 1**, and add **2 optional
> LLD-primer episodes** (OOP & SOLID; the 4 patterns we actually reuse) as
> **Ep 0a/0b** or as a short bridge before Ep 25. Flagged, not yet inserted —
> your call before we lock the count.

### Modules

| # | Module | Eps | Locks in |
|---|---|---|---|
| M1 | What a system even is | 1–6 | Client/server, the request, latency, the API, where data lives. |
| M2 | Scaling the basics | 7–12 | More users than one box can serve. Load balancers, caching, CDN. |
| M3 | Data at scale | 13–18 | SQL vs NoSQL, indexes, replication, sharding, CAP, consistency. |
| M4 | Talking & staying up | 19–24 | Queues, async, rate limits, idempotency, retries, micro vs mono. |
| M5 | Designing real systems | 25–30 | The whiteboard interview classics, end-to-end, the Indian way. |

### Episode map

Lens: **🅗** HLD · **🅛** LLD · **🅗🅛** Both.

| Ep | Title | Diff | Lens | Code | Status |
|---|---|---|---|---|---|
| 1 | What is system design, really? (one user → one million) | 🟢 | 🅗🅛 | – | |
| 2 | Client & server: what actually happens when you open Swiggy | 🟢 | 🅗 | – | |
| 3 | The request's journey: DNS → server → screen, in plain English | 🟢 | 🅗 | – | |
| 4 | Latency vs throughput: the two numbers that decide everything | 🟢 | 🅗 | – | |
| 5 | The API: how apps talk to each other (the waiter analogy) | 🟢 | 🅗🅛 | – | |
| 6 | Where data lives: databases for absolute beginners | 🟢 | 🅗🅛 | – | |
| 7 | Vertical vs horizontal scaling: bigger box vs more boxes | 🟢 | 🅗 | – | |
| 8 | Load balancers: the traffic cop in front of your servers | 🟡 | 🅗🅛 | – | |
| 9 | Stateless vs stateful: the rule that makes scaling possible | 🟡 | 🅗🅛 | – | |
| 10 | Caching: why your feed loads before you blink | 🟡 | 🅗🅛 | – | |
| 11 | Cache invalidation: the "two hard problems" one, made simple | 🟡 | 🅗🅛 | – | |
| 12 | CDN: how Hotstar streams the IPL to 50 million phones | 🟡 | 🅗 | – | |
| 13 | SQL vs NoSQL: picking the right database (no holy war) | 🟡 | 🅗🅛 | – | |
| 14 | Indexing: how a query finds one row out of a billion | 🟡 | 🅗🅛 | – | |
| 15 | Replication: copies that keep you online when a server dies | 🟡 | 🅗 | – | |
| 16 | Sharding: splitting one giant database across many machines | 🔴 | 🅗🅛 | – | |
| 17 | The CAP theorem: consistency vs availability, finally clear | 🔴 | 🅗 | – | |
| 18 | Eventual consistency: why your like-count lags for a second | 🟡 | 🅗 | – | |
| 19 | Message queues: how an app says "I'll handle this later" | 🟡 | 🅗🅛 | – | |
| 20 | Sync vs async: why your order confirms instantly but ships later | 🟡 | 🅗🅛 | – | |
| 21 | Rate limiting: stopping abuse and the thundering herd | 🟡 | 🅗🅛 | – | |
| 22 | Idempotency: why double-tapping "Pay" doesn't pay twice | 🔴 | 🅗🅛 | – | |
| 23 | Retries, timeouts & circuit breakers: failing gracefully | 🔴 | 🅗🅛 | – | |
| 24 | Monolith vs microservices: one big app or many small ones | 🟡 | 🅗 | – | |
| 25 | Design a URL shortener (the classic first interview question) | 🟡 | 🅗🅛 | – | |
| 26 | Design a news feed (Instagram / X): fan-out explained | 🔴 | 🅗🅛 | – | |
| 27 | Design a chat app (WhatsApp): delivered, then those blue ticks | 🔴 | 🅗🅛 | – | |
| 28 | Design a ride-hailing match (Ola / Uber): finding the nearest cab | 🔴 | 🅗🅛 | – | |
| 29 | Design a payment system (UPI): money must never be wrong | 🔴 | 🅗🅛 | – | |
| 30 | Putting it together: how Swiggy survives New Year's Eve | 🟡 | 🅗 | – | |

### HLD vs LLD per episode (the meticulous breakdown)

For each episode: the **🅗 HLD angle** (boxes & trade-offs) and the **🅛 LLD angle**
(the class / data-structure / state machine to actually code). "–" means the lens
isn't a natural fit and we won't force it.

| Ep | 🅗 HLD angle | 🅛 LLD angle |
|---|---|---|
| 1 | The discipline: requirements → capacity estimate → components → trade-offs | Preview the *other* lens: one box → classes/objects; why both exist |
| 2 | Client/server split, request/response, who holds what state | Model a `Request`/`Response`/`Client` — anatomy of one call (thin) |
| 3 | DNS → TCP/TLS handshake → server → render path | – |
| 4 | The two numbers; p50/p95/p99 percentiles & tail latency | Per-item vs **batched** processing in code (why batching lifts throughput) |
| 5 | API as the contract between services; REST vs gRPC | **Design the endpoints**: resources, verbs, request/response DTOs, status codes |
| 6 | DB as a component; OLTP vs OLAP; SQL/NoSQL preview | First **schema**: tables, an entity, primary keys, light normalization |
| 7 | Scale up vs scale out; when each wins; the ceiling of one box | – |
| 8 | LB tier; L4 vs L7; health checks & failover | **Implement** round-robin / least-connections / weighted as a class |
| 9 | Why statelessness enables horizontal scale; push state to Redis | A `SessionStore` interface; the sticky-session trap in code |
| 10 | Cache tiers (client/CDN/app/DB); cache-aside read path | **Build an LRU cache** (HashMap + doubly-linked list) — the classic LLD Q |
| 11 | Write-through / write-back / write-around; TTL strategy | Implement write-through + TTL eviction; a **stampede lock** (single-flight) |
| 12 | Edge PoPs; pull vs push; `Cache-Control`; surge offload | – |
| 13 | Relational vs document/KV/wide-column/graph; ACID vs BASE | Model the **same data both ways**: normalize (SQL) vs access-pattern-first (NoSQL) |
| 14 | Index as a read accelerator; the write/space cost | **B-tree vs hash index**; designing a composite index for a query |
| 15 | Leader–follower; sync vs async replication; failover | Handling **replication lag** in code (read-your-writes) (light) |
| 16 | Partition strategies (range/hash/geo); hotspots & rebalancing | **Consistent-hashing ring** class (virtual nodes) |
| 17 | Pick 2 under partition; PACELC; what "CA" really means | – |
| 18 | Convergence; read-your-writes; conflict resolution | LWW vs **vector-clock** resolver (light) |
| 19 | Broker/queue tier; decoupling; Kafka vs SQS/RabbitMQ | Producer/consumer with **at-least-once** + ack; a bounded `Queue` |
| 20 | Request-response vs event-driven; when to go async | Callbacks → futures/promises; an async handler & the order of execution |
| 21 | Where the limiter sits (edge/gateway); distributed counters | **Token-bucket / sliding-window-log** limiter class — classic LLD |
| 22 | Idempotent endpoints; the "exactly-once" illusion | **Idempotency-key store + dedup**; the double-tap-Pay guard |
| 23 | Resilience patterns; backoff + jitter; bulkheads | **Circuit-breaker state machine** (closed/open/half-open) class |
| 24 | Service boundaries; coupling; independent deploys | Defining a clean **service interface/contract** (light) |
| 25 | Write/read path; key-gen service; DB + cache choice | **base62 encode/decode**, collision handling, the schema — both lenses meet |
| 26 | Fan-out-on-write vs on-read; the celebrity problem | `FeedItem` model; ranking function; merging N timelines |
| 27 | Gateway, presence, queues, delivery guarantees | **Message delivery state machine** (sent → delivered → read ticks) |
| 28 | Geo-sharding; matching service; real-time location updates | **Geohash/quadtree** index + nearest-driver matching |
| 29 | PSP/bank rails; strong consistency; reconciliation | **Payment state machine** + double-entry **ledger** + idempotency key |
| 30 | Assemble every component end-to-end under NYE surge | Callback to the LLD pieces built across the season (recap, no new code) |

## The 4-beat teaching pattern (still every episode)

Same discipline as Season 1 — only the worked examples change:

```
1. HOOK with something they already do   → "It's 8pm. You and a lakh others open Swiggy..."
2. SURFACE the question                   → "How does ONE app not just fall over?"
3. EXPLAIN in 8th-grade language          → 1 visual analogy + 1 simple sentence
4. CONNECT BACK                           → "That's the load balancer you never saw."
```

## Recurring mental models (the Season-2 moat)

Introduce a metaphor once, then *invoke* it later (never re-explain):

| Metaphor | Introduced | Reused in | Explains |
|---|---|---|---|
| **The busy restaurant** (host, waiters, kitchen) | Ep 2 | 5, 7, 8, 30 | Client/server, APIs, scaling, load balancing |
| **Express checkout lane** | Ep 10 | 11, 12 | Caching & CDN (keep the popular thing nearby) |
| **The library catalogue** | Ep 14 | 16 | Indexing (don't read every book to find one) |
| **Photocopies of the ledger** | Ep 15 | 17, 18 | Replication & consistency |
| **Splitting the guest list A–M / N–Z** | Ep 16 | 28, 29 | Sharding & partitioning |
| **The courier / post office** | Ep 19 | 20, 21 | Queues & async ("drop it, I'll process later") |
| **The fuse box** (trips to protect the house) | Ep 23 | 30 | Circuit breakers & graceful failure |

## Indian product teardown matrix (use ≥2 per episode)

| Product | First in | Concept it anchors |
|---|---|---|
| Swiggy / Zomato dinner rush | Ep 1 | Load, scaling, the whole-system finale |
| UPI payment | Ep 5 | APIs, idempotency, strong consistency |
| Hotstar IPL live stream | Ep 12 | CDN, read-heavy fan-out, surge |
| IRCTC Tatkal 10am rush | Ep 21 | Rate limiting, concurrency, locking |
| Flipkart Big Billion Days | Ep 10 | Caching, queues, horizontal scaling |
| WhatsApp message delivery | Ep 27 | Queues, delivery guarantees, ticks |
| Ola / Uber cab matching | Ep 28 | Geo-sharding, nearest-neighbour, real-time |

## Shorts derivation (3–5 per long-form)

Same five shapes as Season 1 — sourced from each system-design episode:

| Type | Source | Hook |
|---|---|---|
| Definition | the 30s "what it is" opener | "Load balancers in 60 seconds — finally clear" |
| Teardown | the Indian product segment | "How Hotstar streams the IPL without crashing" |
| Visual | the build-up diagram | "The simplest way to picture sharding" |
| Cliffhanger | the end-of-episode tease | "Caching is easy. Cache *invalidation* isn't…" |
| Hot take | one contrarian moment | "You probably don't need microservices" |

> **Status:** Season 2 is fully sequenced and **HLD/LLD-tagged** (tables above).
> No episodes built yet. Production is now **research-gated**: each episode is
> only ready to author once its research dossier (below) exists. Ep 1
> (`compositions/sd-ep01-full.html`) is the first target, after its dossier.

## Per-topic research dossier (the standard)

> The rule for this season: **no episode is authored until its dossier is written
> and fact-checked.** We go *one topic at a time, maximum depth* — strong,
> sourced research per topic, not thin coverage across all 30.

Each dossier lives at **`docs/research/sd-epNN-<slug>.md`** and must contain, in
this order:

1. **One-line promise** — what the viewer can do/explain after watching.
2. **🅗 HLD section** — the components, the trade-offs, and *why* each choice;
   the boxes-and-arrows the episode will build on screen.
3. **🅛 LLD section** — the class / data structure / state machine, with a tiny
   correct code sketch (the thing we animate building).
4. **The Indian teardown** — the real product example with **real, cited
   numbers** (concurrency records, RPS, data volumes, outage post-mortems). No
   invented figures — every number carries a source.
5. **The analogy** — the one everyday mental model (restaurant, checkout lane,
   ledger…) and exactly how it maps to the tech, where it breaks down.
6. **Common misconceptions** — 3–5 "most people get this wrong" beats (great
   shorts + the episode's hot-take).
7. **8th-grade explanation** — the core idea in ≤2 plain sentences (the test
   from BRAND.md).
8. **Numbers to get right** — the handful of figures/definitions that must be
   accurate, each with a source link.
9. **Sources** — every claim cited; mark each ✅ verified / ⚠️ single-source /
   ❓ couldn't confirm. Anything not ✅ does **not** go on screen as fact.

**Research method:** use the `deep-research` skill (fan-out web search → fetch →
adversarially verify → cited synthesis) per topic. Beginner framing is on us;
the *facts and numbers* must be sourced and verified — that is the bar the
creator asked for.

**Dossier status tracker:**

| Ep | Dossier | State |
|---|---|---|
| 1 | `docs/research/sd-ep01-what-is-system-design.md` | ⬜ not started |
| 2–30 | — | ⬜ queued (one at a time, on pick) |

## Future seasons (placeholders)

- **Season 3 — DevOps** (CI/CD, containers, Kubernetes, observability, infra-as-code).
- **Season 4 — Security** (auth, encryption, OWASP, the UPI-fraud thread from S1).

Both reuse the same format, style, and pipeline; teardowns of Indian product/infra
teams as the worked examples.
